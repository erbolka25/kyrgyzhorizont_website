// =====================================================
// Kyrgyz Horizont — Smart WhatsApp Handler
// Авто-сбор сообщения + источник (какая страница, какая кнопка)
// Работает с .wa-btn и data-атрибутами
// =====================================================

(function () {
  "use strict";

  // Без документа не работаем
  if (typeof document === "undefined") return;

  document.addEventListener("DOMContentLoaded", function () {
    const body = document.body;
    if (!body) return;

    // Номер WhatsApp, который передаём из base.html (data-wa-number)
    const waNumber = body.getAttribute("data-wa-number");
    if (!waNumber) {
      console.warn("[WA] data-wa-number is missing on <body>");
    }

    // Текущий endpoint (index_lang, tours_lang и т.д.)
    const pageEndpoint = body.getAttribute("data-page") || "";

    // Красивые названия для страниц
    const pageLabels = {
      "index_lang":   "Home",
      "tours_lang":   "Tours",
      "gallery_lang": "Gallery",
      "solo_lang":    "Solo Travelers",
      "plan_lang":    "Plan My Trip",
      "regions_lang": "Regions",
      "about_lang":   "About",
      "contact_lang": "Contact"
    };

    const pageLabel = pageLabels[pageEndpoint] || "Website";

    // Все WhatsApp-кнопки
    const buttons = Array.from(document.querySelectorAll(".wa-btn"));
    if (!buttons.length) return;

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        // Если href="#" или пустой — перехватываем
        const href = btn.getAttribute("href") || "#";
        const isDummyLink = href === "#" || href === "";

        if (isDummyLink) {
          e.preventDefault();
        }

        // Базовый текст из data-msg
        const baseMsg = btn.getAttribute("data-msg") || "Hi! I have a question about your tours.";

        // Контекст: откуда нажали
        const context = btn.getAttribute("data-wa-context") || "button";
        const labelForContext = (function () {
          if (context === "nav") return "Navigation";
          if (context === "hero") return "Hero section";
          if (context === "tours") return "Tours section";
          if (context === "footer") return "Footer";
          return "Button";
        })();

        // Финальное сообщение
        let text = baseMsg.trim();

        // Добавим инфо про страницу и источник (для аналитики и удобства)
        text += ` (from ${labelForContext} on ${pageLabel} page)`;

        // Если нет номера — fallback: просто оставляем обычный href
        if (!waNumber) {
          if (isDummyLink) {
            // Если совсем нет href — не ломаем, просто ничего не делаем
            console.warn("[WA] No number provided and no real href on button.");
          }
          return;
        }

        const encoded = encodeURIComponent(text);
        const waUrl = `https://wa.me/${waNumber}?text=${encoded}`;

        // Открываем в новой вкладке
        window.open(waUrl, "_blank", "noopener,noreferrer");
      });
    });
  });
})();
