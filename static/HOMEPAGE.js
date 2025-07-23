// HOMEPAGE.js — Frontend Enhancements for Vikkie's Online Shop

document.addEventListener("DOMContentLoaded", function () {
  // 1. Dark Mode Toggle (future ready)
  const toggle = document.querySelector('input[name="dark_mode"]');
  if (toggle) {
    toggle.addEventListener("change", function () {
      alert("Dark mode feature coming soon!");
    });
  }

  // 2. Flash Sale Countdown
  const countdownElements = document.querySelectorAll(".flash-countdown");
  countdownElements.forEach(elem => {
    const endTime = new Date(elem.dataset.end);
    setInterval(() => {
      const now = new Date();
      const diff = endTime - now;
      if (diff <= 0) {
        elem.textContent = "Expired";
        return;
      }
      const hours = Math.floor(diff / (1000 * 60 * 60));
      const minutes = Math.floor((diff / (1000 * 60)) % 60);
      const seconds = Math.floor((diff / 1000) % 60);
      elem.textContent = `${hours}h ${minutes}m ${seconds}s`;
    }, 1000);
  });

  // 3. Smooth scroll to sections
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // 4. Wishlist toggler
  document.querySelectorAll('.wishlist-btn').forEach(btn => {
    btn.addEventListener("click", function () {
      this.classList.toggle("active");
      this.textContent = this.classList.contains("active") ? "❤️ In Wishlist" : "🤍 Add to Wishlist";
    });
  });

  // 5. Discount Preview on Points Converter
  const pointsInput = document.querySelector('input[name="points_to_convert"]');
  if (pointsInput) {
    const preview = document.createElement("p");
    pointsInput.after(preview);
    pointsInput.addEventListener("input", function () {
      const val = parseInt(this.value);
      preview.textContent = val ? `You will get a KES ${val} discount.` : "";
    });
  }

  // 6. Scroll to top button (optional)
  const scrollBtn = document.createElement("button");
  scrollBtn.textContent = "⬆ Top";
  scrollBtn.id = "scrollTopBtn";
  scrollBtn.style = "position:fixed;bottom:30px;right:30px;padding:10px;display:none;";
  document.body.appendChild(scrollBtn);

  scrollBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  window.addEventListener("scroll", () => {
    scrollBtn.style.display = window.scrollY > 300 ? "block" : "none";
  });
});
