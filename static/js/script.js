// ========================================================
// Kyrgyz Horizont — Main JavaScript
// Sticky header, smooth scroll, reveal, contact AJAX, WA auto-message
// ========================================================

(function () {
  "use strict";

  const $  = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  // ------------------------------
  // Sticky Header
  // ------------------------------
  const header = $("#site-header");
  if (header) {
    const onScroll = () => {
      header.classList.toggle("is-sticky", window.scrollY > 10);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // ------------------------------
  // Smooth scroll for #anchors
  // ------------------------------
  document.addEventListener(
    "click",
    (e) => {
      const a = e.target.closest('a[href^="#"]');
      if (!a) return;
      const id = a.getAttribute("href").slice(1);
      const target = document.getElementById(id);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    },
    { passive: false }
  );

  // ------------------------------
  // Reveal on scroll
  // ------------------------------
  const revealEls = $$(".reveal");
  if (revealEls.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            en.target.classList.add("active");
            obs.unobserve(en.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("active"));
  }

  // ------------------------------
  // Back To Top
  // ------------------------------
  const back = $("#backToTop");
  if (back) {
    const toggleBack = () => {
      back.style.display = window.scrollY > 300 ? "flex" : "none";
    };
    toggleBack();
    window.addEventListener("scroll", toggleBack, { passive: true });
    back.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // ------------------------------
  // Contact form AJAX
  // ------------------------------
  const form = $("#contact-form");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      form.classList.add("was-validated");
      if (!form.checkValidity()) return;

      try {
        const fd = new FormData(form);
        const res = await fetch(form.action, { method: "POST", body: fd });
        const data = await res.json();

        if (data.ok) {
          alert("Message sent! 👌 We will reply soon.");
          form.reset();
          form.classList.remove("was-validated");
        } else {
          alert("Error sending message.");
        }
      } catch (err) {
        alert("Network error — try again.");
      }
    });
  }

  // ------------------------------
  // WhatsApp auto-message
  // ------------------------------
  const waNumber = document.body.dataset.waNumber;
  const waButtons = $$(".wa-btn");

  if (waNumber && waButtons.length) {
    waButtons.forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();

        const ctx = btn.dataset.waContext || "general";
        const tourTitle = btn.dataset.tourTitle || "";
        const lang = document.documentElement.lang || "en";

        let text;

        switch (ctx) {
          case "tour":
            text = `Hi! I found the tour "${tourTitle}" on your website. I travel solo and want to know dates and price details.`;
            break;
          case "solo":
            text = "Hi! I'm a solo traveler and I want you to help me plan a safe and affordable trip in Kyrgyzstan.";
            break;
          case "plan":
            text = "Hi! I want a custom itinerary. Here are my dates and budget:";
            break;
          case "regions":
            text = "Hi! I'm interested in tours in your regions (Issyk-Kul / Naryn / Chui). Can you suggest programs?";
            break;
          case "nav":
          default:
            text = "Hi! I found your website Kyrgyz Horizont and I want to ask about tours in Kyrgyzstan.";
        }

        const waUrl = `https://wa.me/${waNumber}?text=${encodeURIComponent(text)}`;
        window.open(waUrl, "_blank");
      });
    });
  }
})();
