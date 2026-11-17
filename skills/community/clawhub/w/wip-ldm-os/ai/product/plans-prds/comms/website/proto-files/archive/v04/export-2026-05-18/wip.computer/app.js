const TOP_RESOLVED = "Every AI.";
const TOP_CYCLE = "Your AIs:";
const BOTTOM_RESOLVED = "One experience.";
const PAYOFFS = [
  ["remember you.", "remember everything.", "forget when you say."],
  ["know who does what.", "talk to each other.", "work together."],
  ["go where you go.", "live on every device.", "never start over."],
  ["ask before they act.", "wait for your yes.", "work for you."],
];

const BUCKY_IMAGES = [
  "assets/bucky-patent-1.gif",
  "assets/bucky-patent-2.gif",
  "assets/bucky-patent-3.gif",
  "assets/bucky-patent-4.gif",
  "assets/bucky-patent-5.gif",
];

// In bundled previews the assets are inlined as data URIs on hidden <img data-bucky-preload>
// tags. Prefer those at runtime so the bucky bg actually shows when the page
// is served from a single-file bundle (no /assets/ directory available).
function buckyImageSrc(index) {
  const preload = document.querySelector(`[data-bucky-preload="${index}"]`);
  if (preload && preload.src) return preload.src;
  return BUCKY_IMAGES[Math.min(Math.max(0, index - 1), BUCKY_IMAGES.length - 1)];
}

const BUCKY_PRESETS = [
  { img: 3, rot: 0, y: 4, dx: 154, dy: -757 },
  { img: 1, rot: 0, y: 0, dx: 185, dy: 214 },
  { img: 2, rot: 0, y: 0, dx: -14, dy: -804 },
  { img: 1, rot: 0, y: 0, dx: -97, dy: 171 },
  { img: 5, rot: 0, y: 0, dx: 127, dy: -527 },
  { img: 3, rot: 90, y: 0, dx: 32, dy: -283 },
  { img: 5, rot: 180, y: 0, dx: -342, dy: -176 },
  { img: 1, rot: 90, y: -12, dx: 0, dy: 0 },
  { img: 1, rot: 0, y: 6, dx: -60, dy: -33 },
  { img: 1, rot: 0, y: 0, dx: -223, dy: 169 },
  { img: 2, rot: 0, y: 0, dx: -3, dy: -592 },
  { img: 3, rot: 0, y: 0, dx: 13, dy: 278 },
  { img: 5, rot: 0, y: 0, dx: 26, dy: -414 },
];

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const prefersReducedMotion = () => window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function pickPreset(previous) {
  const pool = previous && BUCKY_PRESETS.length > 1
    ? BUCKY_PRESETS.filter((preset) => preset !== previous)
    : BUCKY_PRESETS;
  return pool[Math.floor(Math.random() * pool.length)];
}

function presetToImage(preset) {
  const imageIndex = Math.min(Math.max(0, preset.img - 1), BUCKY_IMAGES.length - 1);
  return BUCKY_IMAGES[imageIndex];
}

function initHeader() {
  const header = document.querySelector(".site-header");
  const cta = document.querySelector(".site-header__cta");
  if (!header || !cta) return;
  const brand = document.querySelector(".site-header__brand");

  if (brand) {
    brand.addEventListener("click", (event) => {
      event.preventDefault();
      window.dispatchEvent(new CustomEvent("wip:toggle-bucky-readout"));
    });
  }

  let ticking = false;
  const update = () => {
    ticking = false;
    header.classList.toggle("is-scrolled", window.scrollY > 8);

    const heroCta = document.querySelector(".hero__ctas");
    const headerBottomY = 70;
    let opacity = 0;
    if (heroCta) {
      const rect = heroCta.getBoundingClientRect();
      const height = rect.height || 1;
      if (rect.top >= headerBottomY) opacity = 0;
      else if (rect.bottom <= headerBottomY) opacity = 1;
      else opacity = (headerBottomY - rect.top) / height;
    } else if (window.scrollY > 500) {
      opacity = 1;
    }

    cta.style.opacity = String(opacity);
    cta.style.pointerEvents = opacity > 0.5 ? "auto" : "none";
    cta.setAttribute("aria-hidden", opacity > 0.5 ? "false" : "true");
  };

  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  };

  update();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", update);
}

function initHeroTitle() {
  if (prefersReducedMotion()) return;

  const top = document.querySelector("[data-hero-top]");
  const bottom = document.querySelector("[data-hero-bottom]");
  const topLine = document.querySelector("[data-hero-top-line]");
  const bottomLine = document.querySelector("[data-hero-bottom-line]");
  const topGhost = document.querySelector("[data-hero-top-ghost]");
  const bottomGhost = document.querySelector("[data-hero-bottom-ghost]");
  const caret = document.querySelector("[data-hero-caret]");
  if (!top || !bottom || !topLine || !bottomLine || !topGhost || !bottomGhost || !caret) return;

  let topText = TOP_RESOLVED;
  let bottomText = BOTTOM_RESOLVED;
  let cancelled = false;

  const syncCaret = () => {
    const activeText = caret.parentElement === topLine ? top : bottom;
    const width = activeText.getBoundingClientRect().width;
    caret.style.setProperty("--hero-caret-x", `${(width / 2) + 6}px`);
  };

  const setTop = (value) => {
    topText = value;
    top.textContent = value;
    if (caret.parentElement === topLine) requestAnimationFrame(syncCaret);
  };

  const setBottom = (value) => {
    bottomText = value;
    bottom.textContent = value;
    if (caret.parentElement === bottomLine) requestAnimationFrame(syncCaret);
  };

  const placeCaret = (line) => {
    caret.remove();
    caret.hidden = false;
    if (line === "top") topLine.appendChild(caret);
    else bottomLine.appendChild(caret);
    requestAnimationFrame(syncCaret);
  };

  const setGhostText = (element, value) => {
    element.setAttribute("data-hero-ghost-text", value);
  };

  const typeTop = async (target, ms = 95) => {
    while (!cancelled && topText.length < target.length) {
      setTop(target.slice(0, topText.length + 1));
      await sleep(ms);
    }
  };

  const eraseTop = async (ms = 53) => {
    while (!cancelled && topText.length > 0) {
      setTop(topText.slice(0, -1));
      await sleep(ms);
    }
  };

  const typeBottom = async (target, ms = 95) => {
    while (!cancelled && bottomText.length < target.length) {
      setBottom(target.slice(0, bottomText.length + 1));
      await sleep(ms);
    }
  };

  const eraseBottom = async (ms = 53) => {
    while (!cancelled && bottomText.length > 0) {
      setBottom(bottomText.slice(0, -1));
      await sleep(ms);
    }
  };

  (async () => {
    await sleep(6500);
    if (cancelled) return;
    caret.classList.remove("is-calm");
    placeCaret("bottom");

    while (!cancelled) {
      for (const group of PAYOFFS) {
        placeCaret("bottom");
        caret.classList.remove("is-calm");
        await eraseBottom();
        await sleep(200);

        placeCaret("top");
        await eraseTop();
        await sleep(120);
        setGhostText(topGhost, TOP_CYCLE);
        await typeTop(TOP_CYCLE);
        await sleep(280);
        placeCaret("bottom");

        for (let index = 0; index < group.length; index += 1) {
          setGhostText(bottomGhost, group[index]);
          await typeBottom(group[index]);
          await sleep(2200);
          await eraseBottom();
          if (index < group.length - 1) await sleep(650);
        }

        placeCaret("top");
        await sleep(700);
        await eraseTop();
        await sleep(140);
        setGhostText(topGhost, TOP_RESOLVED);
        await typeTop(TOP_RESOLVED);
        await sleep(220);
        placeCaret("bottom");
        setGhostText(bottomGhost, BOTTOM_RESOLVED);
        await typeBottom(BOTTOM_RESOLVED);
        caret.classList.add("is-calm");
        await sleep(5000);
        caret.classList.remove("is-calm");
      }
    }
  })();

  window.addEventListener("pagehide", () => {
    cancelled = true;
  });
}

function initBucky() {
  const bg = document.querySelector("[data-bucky-bg]");
  if (!bg) return;
  const hero = bg.closest(".hero");

  let currentPreset = pickPreset(null);
  let visible = false;
  let readoutOn = false;
  let manualPauseUntil = 0;
  let drift = 0;
  let scroll = window.scrollY || 0;
  let direction = Math.random() < 0.5 ? 1 : -1;
  let lastFrame = performance.now();
  let nextFlip = lastFrame + 45000 + Math.random() * 45000;
  const reduce = prefersReducedMotion();
  const state = {
    img: currentPreset.img,
    rot: currentPreset.rot,
    y: currentPreset.y,
    dx: currentPreset.dx,
    dy: currentPreset.dy,
  };
  let readout = null;

  const syncStateFromPreset = () => {
    state.img = currentPreset.img;
    state.rot = currentPreset.rot;
    state.y = currentPreset.y;
    state.dx = currentPreset.dx;
    state.dy = currentPreset.dy;
  };

  const flashSnapshot = (message) => {
    const toast = document.createElement("div");
    toast.className = "bucky-toast";
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add("is-on"), 10);
    setTimeout(() => {
      toast.classList.remove("is-on");
      setTimeout(() => toast.remove(), 300);
    }, 1400);
  };

  const snapshotText = () => (
    `I${state.img} rot ${state.rot}deg y ${state.y}% dx ${Math.round(state.dx)} dy ${Math.round(state.dy)}`
  );

  const jumpTo = (imageIndex, rotation) => {
    manualPauseUntil = Date.now() + 30000;
    state.img = imageIndex + 1;
    state.rot = rotation;
    state.y = 0;
    state.dx = 0;
    state.dy = 0;
    visible = true;
    render();
  };

  const copySnapshot = () => {
    const text = snapshotText();
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(
        () => flashSnapshot(`Copied: ${text}`),
        () => flashSnapshot(`Snapshot: ${text}`),
      );
    } else {
      flashSnapshot(`Snapshot: ${text}`);
    }
  };

  const renderReadout = () => {
    if (!readout) return;
    readout.querySelector("[data-bucky-value='img']").textContent = `I${state.img}`;
    readout.querySelector("[data-bucky-value='rot']").textContent = `${state.rot}deg`;
    readout.querySelector("[data-bucky-value='y']").textContent = `${state.y > 0 ? "+" : ""}${state.y}%`;
    readout.querySelector("[data-bucky-value='dx']").textContent = String(Math.round(state.dx));
    readout.querySelector("[data-bucky-value='dy']").textContent = String(Math.round(state.dy));
    readout.querySelectorAll("[data-bucky-jump]").forEach((button) => {
      const active = Number(button.dataset.image) === state.img && Number(button.dataset.rotation) === state.rot;
      button.classList.toggle("is-active", active);
    });
  };

  const ensureReadout = () => {
    if (readout || !hero) return;
    readout = document.createElement("div");
    readout.className = "bucky-readout";
    readout.setAttribute("aria-hidden", "true");
    readout.innerHTML = `
      <div class="bucky-readout__row"><span>img</span><b data-bucky-value="img"></b></div>
      <div class="bucky-readout__row"><span>rot</span><b data-bucky-value="rot"></b></div>
      <div class="bucky-readout__row"><span>y</span><b data-bucky-value="y"></b></div>
      <div class="bucky-readout__row"><span>dx</span><b data-bucky-value="dx"></b></div>
      <div class="bucky-readout__row"><span>dy</span><b data-bucky-value="dy"></b></div>
      <div class="bucky-readout__sep"></div>
      <div class="bucky-readout__row bucky-readout__row--label"><span>0deg</span></div>
      <div class="bucky-readout__grid">
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="1" data-rotation="0">1</button>
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="2" data-rotation="0">2</button>
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="3" data-rotation="0">3</button>
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="4" data-rotation="0">4</button>
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="5" data-rotation="0">5</button>
      </div>
      <div class="bucky-readout__row bucky-readout__row--label"><span>90deg</span></div>
      <div class="bucky-readout__grid">
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="1" data-rotation="90">6</button>
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="2" data-rotation="90">7</button>
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="3" data-rotation="90">8</button>
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="4" data-rotation="90">9</button>
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="5" data-rotation="90">10</button>
      </div>
      <div class="bucky-readout__row bucky-readout__row--label"><span>180deg</span></div>
      <div class="bucky-readout__grid">
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="1" data-rotation="180">11</button>
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="2" data-rotation="180">12</button>
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="3" data-rotation="180">13</button>
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="4" data-rotation="180">14</button>
        <button type="button" class="bucky-readout__btn" data-bucky-jump data-image="5" data-rotation="180">15</button>
      </div>
    `;
    readout.querySelectorAll("[data-bucky-jump]").forEach((button) => {
      button.addEventListener("click", () => {
        jumpTo(Number(button.dataset.image) - 1, Number(button.dataset.rotation));
      });
    });
    hero.appendChild(readout);
  };

  const toggleReadout = () => {
    if (!hero) return;
    readoutOn = !readoutOn;
    hero.classList.toggle("is-bucky-readout-on", readoutOn);
    if (readoutOn) {
      ensureReadout();
      readout.hidden = false;
      renderReadout();
    } else if (readout) {
      readout.hidden = true;
    }
  };

  const render = () => {
    bg.src = buckyImageSrc(state.img);
    bg.style.opacity = visible ? "0.07" : "0";
    bg.style.transform = `translate(calc(-50% + ${state.dx}px), calc(-50% + ${state.y}% + ${state.dy}px + ${scroll * 0.4}px + ${drift}px)) rotate(${state.rot}deg)`;
    renderReadout();
  };

  const tick = (now) => {
    if (!reduce) {
      const delta = (now - lastFrame) / 1000;
      if (now > nextFlip) {
        direction *= -1;
        nextFlip = now + 45000 + Math.random() * 45000;
      }
      drift += direction * 1.2 * delta;
    }
    lastFrame = now;
    render();
    requestAnimationFrame(tick);
  };

  const onScroll = () => {
    scroll = window.scrollY || 0;
    render();
  };

  if (hero) {
    let dragging = false;
    let startX = 0;
    let startY = 0;
    let baseX = 0;
    let baseY = 0;
    let moved = false;

    hero.addEventListener("pointerdown", (event) => {
      if (event.target.closest("a, button, .bucky-readout")) return;
      dragging = true;
      moved = false;
      startX = event.clientX;
      startY = event.clientY;
      baseX = state.dx;
      baseY = state.dy;
      hero.classList.add("is-dragging");
      hero.setPointerCapture(event.pointerId);
    });

    hero.addEventListener("pointermove", (event) => {
      if (!dragging) return;
      const dx = event.clientX - startX;
      const dy = event.clientY - startY;
      if (!moved && (Math.abs(dx) > 3 || Math.abs(dy) > 3)) moved = true;
      state.dx = baseX + dx;
      state.dy = baseY + dy;
      manualPauseUntil = Date.now() + 30000;
      render();
      if (moved && event.cancelable) event.preventDefault();
    });

    const stopDrag = (event) => {
      if (!dragging) return;
      dragging = false;
      hero.classList.remove("is-dragging");
      if (hero.hasPointerCapture(event.pointerId)) hero.releasePointerCapture(event.pointerId);
      if (!moved && readoutOn) copySnapshot();
    };

    hero.addEventListener("pointerup", stopDrag);
    hero.addEventListener("pointercancel", stopDrag);
  }

  window.addEventListener("wip:toggle-bucky-readout", toggleReadout);
  window.addEventListener("scroll", onScroll, { passive: true });

  currentPreset = pickPreset(null);
  syncStateFromPreset();
  render();
  setTimeout(() => {
    visible = true;
    render();
  }, 30);

  if (!reduce) requestAnimationFrame(tick);

  setInterval(() => {
    if (Date.now() < manualPauseUntil) return;
    visible = false;
    render();
    setTimeout(() => {
      currentPreset = pickPreset(currentPreset);
      syncStateFromPreset();
      visible = true;
      render();
    }, reduce ? 0 : 700);
  }, 50000);
}

function initArchitectureReveal() {
  const explore = document.getElementById("explore");
  const openLink = document.querySelector("[data-arch-open]");
  const closeButton = document.querySelector("[data-arch-close]");
  if (!explore || !openLink || !closeButton) return;

  const setOpen = (open) => {
    explore.classList.toggle("is-open", open);
    explore.setAttribute("aria-hidden", open ? "false" : "true");
    openLink.hidden = open;
  };

  openLink.addEventListener("click", (event) => {
    event.preventDefault();
    setOpen(true);
    requestAnimationFrame(() => {
      explore.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  closeButton.addEventListener("click", () => {
    setOpen(false);
    const letterCta = document.querySelector(".letter__cta");
    if (!letterCta) return;
    const y = letterCta.getBoundingClientRect().top + window.scrollY - 120;
    window.scrollTo({ top: y, behavior: "smooth" });
  });
}

function initAnchorCleanup() {
  const cleanHash = () => {
    if (window.location.hash !== "#letter") return;
    window.history.replaceState(null, "", `${window.location.pathname}${window.location.search}`);
  };

  document.querySelectorAll('a[href="#letter"]').forEach((link) => {
    link.addEventListener("click", (event) => {
      const target = document.getElementById("letter");
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      cleanHash();
    });
  });

  if (window.location.hash === "#letter") {
    requestAnimationFrame(cleanHash);
  }

  window.addEventListener("hashchange", () => {
    requestAnimationFrame(cleanHash);
  });
}

function initPasskeys() {
  const button = document.querySelector("[data-passkeys]");
  const label = document.querySelector("[data-passkeys-label]");
  if (!button || !label) return;

  let on = false;
  const render = () => {
    button.classList.toggle("is-on", on);
    button.setAttribute("aria-pressed", on ? "true" : "false");
    button.setAttribute("aria-label", `Local passkeys ${on ? "on" : "off"}`);
    label.textContent = `Local passkeys ${on ? "on" : "off"}`;
  };

  button.addEventListener("click", () => {
    on = !on;
    render();
  });
}

function initPasskeysInfo() {
  const button = document.querySelector("[data-passkeys-info]");
  if (!button) return;
  button.setAttribute("aria-expanded", "false");
  const wrap = button.parentElement;
  const popover = wrap && wrap.querySelector(".site-footer__info-popover");
  let scrollAtOpen = window.scrollY;

  function positionPopover() {
    if (!popover || !wrap) return;
    // Measure based on the icon's position and the popover's intrinsic width
    // so the calculation doesn't depend on the popover's current transform.
    const iconRect = wrap.getBoundingClientRect();
    const popoverWidth = popover.offsetWidth || 240;
    const margin = 12;
    const iconCenter = iconRect.left + iconRect.width / 2;
    const idealLeft = iconCenter - popoverWidth / 2;
    const idealRight = iconCenter + popoverWidth / 2;
    let shift = 0;
    if (idealRight > window.innerWidth - margin) {
      shift = (window.innerWidth - margin) - idealRight;
    } else if (idealLeft < margin) {
      shift = margin - idealLeft;
    }
    popover.style.setProperty("--shift", `${shift}px`);
  }

  button.addEventListener("click", (event) => {
    event.preventDefault();
    event.stopPropagation();
    const open = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", open ? "false" : "true");
    if (!open) {
      scrollAtOpen = window.scrollY;
      requestAnimationFrame(positionPopover);
    }
  });

  document.addEventListener("click", (event) => {
    if (wrap && !wrap.contains(event.target)) {
      button.setAttribute("aria-expanded", "false");
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      button.setAttribute("aria-expanded", "false");
    }
  });

  window.addEventListener("scroll", () => {
    if (button.getAttribute("aria-expanded") !== "true") {
      scrollAtOpen = window.scrollY;
      return;
    }
    if (Math.abs(window.scrollY - scrollAtOpen) > 24) {
      button.setAttribute("aria-expanded", "false");
    }
  }, { passive: true });

  window.addEventListener("resize", () => {
    if (button.getAttribute("aria-expanded") === "true") positionPopover();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initHeader();
  initHeroTitle();
  initBucky();
  initAnchorCleanup();
  initArchitectureReveal();
  initPasskeys();
  initPasskeysInfo();
});
