/* ==========================================================================
   CloudDeploy — script.js
   Vanilla JS only. Handles:
   1. Typing animation for the hero terminal mockup
   2. Mobile navigation toggle
   3. Scroll-reveal for cards / pipeline steps
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  initTerminalTyping();
  initMobileNav();
  initScrollReveal();
});

/* --------------------------------------------------------------------
   1. Terminal typing animation
   -------------------------------------------------------------------- */
function initTerminalTyping() {
  const el = document.getElementById("terminal-body");
  if (!el) return;

  const lines = [
    { text: "Connecting to AWS...", cls: "" },
    { text: "Connected to AWS successfully (region: ap-south-1)", cls: "ok" },
    { text: "", cls: "" },
    { text: "STEP 1/5: BUCKET SETUP", cls: "warn" },
    { text: "Bucket 'my-static-website-bucket' created successfully.", cls: "ok" },
    { text: "", cls: "" },
    { text: "STEP 4/5: STATIC WEBSITE HOSTING", cls: "warn" },
    { text: "Static website hosting enabled.", cls: "ok" },
    { text: "", cls: "" },
    { text: "STEP 5/5: FILE UPLOAD", cls: "warn" },
    { text: "Uploaded: index.html   (text/html)", cls: "" },
    { text: "Uploaded: style.css    (text/css)", cls: "" },
    { text: "Uploaded: script.js    (application/javascript)", cls: "" },
    { text: "", cls: "" },
    { text: "DEPLOYMENT SUCCESSFUL", cls: "ok" },
    { text: "Website URL: http://my-static-website-bucket.s3-website-us-east-1.amazonaws.com", cls: "ok" },
  ];

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (prefersReducedMotion) {
    el.textContent = lines.map((l) => l.text).join("\n");
    return;
  }

  let lineIndex = 0;
  let charIndex = 0;
  const speed = 18; // ms per character

  function typeNextChar() {
    if (lineIndex >= lines.length) {
      // Restart the loop after a pause, so the hero stays alive on long visits
      setTimeout(() => {
        el.textContent = "";
        lineIndex = 0;
        charIndex = 0;
        typeNextChar();
      }, 3200);
      return;
    }

    const current = lines[lineIndex];
    const span = document.createElement("span");
    span.className = current.cls;

    if (charIndex === 0) {
      el.appendChild(document.createTextNode(lineIndex === 0 ? "" : "\n"));
    }

    // Render the whole line into a span so class-based coloring applies
    renderLineChar(el, current, charIndex);
    charIndex++;

    if (charIndex > current.text.length) {
      lineIndex++;
      charIndex = 0;
      setTimeout(typeNextChar, 120);
    } else {
      setTimeout(typeNextChar, speed);
    }
  }

  function renderLineChar(container, line, idx) {
    // Rebuild the current line's span each tick (simple + reliable for short lines)
    let lastSpan = container.querySelector('span[data-current="true"]');
    if (!lastSpan) {
      lastSpan = document.createElement("span");
      lastSpan.dataset.current = "true";
      if (line.cls) lastSpan.className = line.cls;
      container.appendChild(lastSpan);
    }
    lastSpan.textContent = line.text.slice(0, idx);

    if (idx >= line.text.length && lastSpan) {
      lastSpan.removeAttribute("data-current");
    }
  }

  typeNextChar();
}

/* --------------------------------------------------------------------
   2. Mobile navigation toggle
   -------------------------------------------------------------------- */
function initMobileNav() {
  const burger = document.getElementById("burger");
  const links = document.querySelector(".nav__links");
  if (!burger || !links) return;

  burger.addEventListener("click", () => {
    const isOpen = links.classList.toggle("nav__links--open");
    burger.setAttribute("aria-expanded", String(isOpen));
  });

  links.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => links.classList.remove("nav__links--open"));
  });
}

/* --------------------------------------------------------------------
   3. Scroll reveal for cards and pipeline steps
   -------------------------------------------------------------------- */
function initScrollReveal() {
  const targets = document.querySelectorAll(".card, .pipeline__step");
  if (!("IntersectionObserver" in window) || targets.length === 0) {
    targets.forEach((t) => (t.style.opacity = 1));
    return;
  }

  targets.forEach((t) => {
    t.style.opacity = "0";
    t.style.transform = "translateY(14px)";
    t.style.transition = "opacity 0.5s ease, transform 0.5s ease";
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );

  targets.forEach((t) => observer.observe(t));
}