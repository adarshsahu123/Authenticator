/**
 * OTP Email Verification - Client Side Scripts
 * Handles timer, form validation, and UI interactions
 */

/**
 * Start countdown timer for OTP expiry
 * @param {number} duration - Timer duration in seconds
 */
function startTimer(duration) {
    let timer = duration;
    let display = document.getElementById("timer");
    let resendBtn = document.getElementById("resend-btn");

    // Update timer every second
    let interval = setInterval(() => {
        let minutes = parseInt(timer / 60, 10);
        let seconds = parseInt(timer % 60, 10);

        display.textContent = `⏱️ OTP expires in: ${minutes}:${seconds < 10 ? "0" + seconds : seconds}`;
        
        // Show resend button when timer expires
        if (--timer < 0) {
            clearInterval(interval);
            display.textContent = "⚠️ OTP Expired";
            resendBtn.style.display = "block";
        }
    }, 1000);
}

/**
 * Format OTP input - only allow numbers
 */
document.addEventListener('DOMContentLoaded', function() {
    const otpInput = document.querySelector('input[name="otp"]');
    
    if (otpInput) {
        otpInput.addEventListener('input', function() {
            // Remove non-numeric characters
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    }
});

