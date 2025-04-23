const checkboxes = document.querySelectorAll('.cell-checkbox');
const impactPercentEl = document.getElementById('impactPercent');
const chartCtx = document.getElementById('impactChart').getContext('2d');


const traitRepere35Plugin = {
    id: 'traitRepere35',
    afterDatasetDraw(chart, args, pluginOptions) {
        const { ctx, chartArea: { width, height, top, left } } = chart;
        const meta = chart.getDatasetMeta(0);
        if (!meta.data.length) return;

        const donutArc = meta.data[0];

        const centerX = left + width / 2;
        const centerY = top + height / 2;
        const outerRadius = donutArc.outerRadius;
        const innerRadius = donutArc.innerRadius;
        const midRadius = (outerRadius + innerRadius) / 2;

        const startAngle = chart.options.rotation || -0.5 * Math.PI;
        const angleAt35 = startAngle + (0.35 * 2 * Math.PI);

        // Position du trait au bord du donut
        const x1 = centerX + Math.cos(angleAt35) * (innerRadius - 5);
        const y1 = centerY + Math.sin(angleAt35) * (innerRadius - 5);
        const x2 = centerX + Math.cos(angleAt35) * (outerRadius + 5);
        const y2 = centerY + Math.sin(angleAt35) * (outerRadius + 5);

        ctx.save();
        ctx.beginPath();
        ctx.strokeStyle = '#FF0000'; // Couleur rouge pour bien voir
        ctx.lineWidth = 2;
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();

        // --- 2. Ajouter le texte ---
        ctx.font = 'bold 14px Arial';
        ctx.fillStyle = '#FF0000';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        const textOffset = 20; // distance du texte par rapport au trait
        const textX = centerX + Math.cos(angleAt35) * (outerRadius + textOffset);
        const textY = centerY + Math.sin(angleAt35) * (outerRadius + textOffset);

        ctx.fillText('35%', textX, textY);

        ctx.restore();
    }
};




// Création du donut simple
let impactChart = new Chart(chartCtx, {
    type: 'doughnut',
    data: {
        labels: ['Impact', 'Reste'],
        datasets: [{
            data: [0, maxScore],
            backgroundColor: ['#FF0000', '#ddd'], // commence en rouge
            borderWidth: 2
        }]
    },
    options: {
        cutout: '70%',
        responsive: true,
        rotation: -0.5 * Math.PI, // IMPORTANT pour démarrer en haut
        plugins: {
            legend: {
                display: false,
            }
        }
    },
    plugins: [traitRepere35Plugin] // <<< ici

});



// Fonction pour mettre à jour impact et couleur
function updateImpact() {
    let total = 10; // by default, due to structural evolution, 10% of reduction

    checkboxes.forEach(checkbox => {
        const cell = checkbox.closest('td');
        if (checkbox.checked) {
            total += parseInt(cell.dataset.weight);
            cell.classList.add('selected');
        } else {
            cell.classList.remove('selected');
        }
    });

    const percent = ((total / maxScore) * 100).toFixed(1);

    impactPercentEl.textContent = percent;

    let color = '#FF0000'; // par défaut rouge
    if (percent >= 35) {
        color = '#4CAF50'; // vert
    } else if (percent >= 20) {
        color = '#FFC107'; // orange
    }

    impactChart.data.datasets[0].backgroundColor = [color, '#ddd'];
    impactChart.data.datasets[0].data = [total, maxScore - total];
    impactChart.update();
}

// Quand on clique
checkboxes.forEach(cb => {
    cb.addEventListener('change', updateImpact);
});

// Fonction pour remettre l'état initial des cases
function resetSelection() {
    // Parcourir toutes les cases et réinitialiser leur état
    const checkboxes = document.querySelectorAll('.cell-checkbox');

    checkboxes.forEach((checkbox, index) => {
        let rowIndex = 0
        let tmp = index
        for (let i = 0; i < initialCheckedState.length; i++) {
            if (tmp >= initialCheckedState[i]["parts"].length) {
                tmp -= initialCheckedState[i]["parts"].length
                rowIndex += 1
            }
            else {
                break
            }
        }
        Math.floor(index / initialCheckedState.length);  // Calcule l'index de ligne
        // Calculer l'indice global en fonction des lignes précédentes
        let previousColumnsCount = 0;
        for (let i = 0; i < rowIndex; i++) {
            previousColumnsCount += initialCheckedState[i]["parts"].length;
        }
        const colIndex = index - previousColumnsCount;  // Calcule l'index de colonne
        // Si la case doit être cochée, coche-la
        if (initialCheckedState[rowIndex]["parts"][colIndex].checked) {
            checkbox.checked = true;
        } else {
            checkbox.checked = false;
        }
    });

    // Recalculer l'impact après le reset
    updateImpact();
}


// Nouvelle fonction pour forcer une seule case cochée par ligne
function handleCheckboxClick(event) {
    const clickedCheckbox = event.target;
    const row = clickedCheckbox.closest('tr');

    // Désélectionner tous les autres checkboxes dans la même ligne
    row.querySelectorAll('.cell-checkbox').forEach(checkbox => {
        if (checkbox !== clickedCheckbox) {
            checkbox.checked = false;
        }
    });

    // Mettre à jour l'impact après modification
    updateImpact();
}

// Lier l'événement 'click' à chaque checkbox
checkboxes.forEach(cb => {
    cb.addEventListener('click', handleCheckboxClick);
});


// Appel automatique au chargement de la page
updateImpact();
