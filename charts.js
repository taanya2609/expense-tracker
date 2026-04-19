const ctx = document.getElementById('trendChart').getContext('2d');
const gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(0, 217, 165, 0.2)');
gradient.addColorStop(1, 'rgba(0, 217, 165, 0)');

new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Day 1', 'Day 7', 'Day 14', 'Day 21', 'Day 30'],
        datasets: [{
            label: 'Spending (₹)',
            data: [2000, 8000, 15000, 22000, 31000], 
            borderColor: '#00d9a5',
            backgroundColor: gradient,
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            x: { grid: { display: false }, ticks: { color: '#888' } },
            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#888' } }
        }
    }
});