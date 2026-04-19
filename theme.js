document.addEventListener('DOMContentLoaded', () => {
    // Auto-hide toast messages after 4 seconds
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 500);
        }, 4000);
    });

    // Dark/Light Mode logic (optional expansion)
    console.log("CloudSpend Theme Engine Loaded");
});