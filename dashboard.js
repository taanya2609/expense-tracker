document.addEventListener('DOMContentLoaded', () => {
    // 1. Line Chart: Monthly Spending Trend
    const trendCtx = document.getElementById('trendChart').getContext('2d');
    
    // Gradient fill for that "High-End" look
    const gradient = trendCtx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(0, 217, 165, 0.3)');
    gradient.addColorStop(1, 'rgba(0, 217, 165, 0)');

    new Chart(trendCtx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'], // Dynamic labels can be passed from Flask
            datasets: [{
                label: 'Spending (₹)',
                data: [4500, 12000, 7000, 9500],
                borderColor: '#00d9a5',
                borderWidth: 3,
                pointBackgroundColor: '#00d9a5',
                tension: 0.4,
                fill: true,
                backgroundColor: gradient
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { grid: { display: false }, ticks: { color: '#888' } },
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#888' } }
            }
        }
    });

    console.log("Analytics Engine Initialized");
});