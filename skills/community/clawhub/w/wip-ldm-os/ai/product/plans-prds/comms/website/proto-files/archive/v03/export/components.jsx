/* global React */

// ---------- Tiny icon set ----------
const Icon = ({ d, size = 14, sw = 1.75, ...rest }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
       stroke="currentColor" strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round"
       aria-hidden="true" {...rest}>
    {d}
  </svg>
);
const IconArrowRight = (p) => <Icon {...p} d={<><line x1="5" y1="12" x2="19" y2="12"/><polyline points="13 6 19 12 13 18"/></>} />;
const IconArrowUR = (p) => <Icon {...p} d={<><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></>} />;
Object.assign(window, { Icon, IconArrowRight, IconArrowUR });


// ---------- Header ----------
function Header() {
  // Bar (translucent bg + bottom border) appears the moment the user scrolls.
  // CTA crossfades in as the hero's own CTA scrolls past the top of the
  // viewport — so as the hero button disappears, the header button takes over.
  const [scrolled, setScrolled] = React.useState(false);
  const [ctaOpacity, setCtaOpacity] = React.useState(0);
  React.useEffect(() => {
    let ticking = false;
    const update = () => {
      ticking = false;
      setScrolled(window.scrollY > 8);
      const heroCta = document.querySelector(".hero__ctas");
      // Crossfade across the hero CTA's own height: 0% when its top first
      // reaches the bottom of the header bar; 100% when its bottom passes it.
      const headerBottomY = 70;
      let opacity = 0;
      if (heroCta) {
        const r = heroCta.getBoundingClientRect();
        const h = r.height || 1;
        if (r.top >= headerBottomY) opacity = 0;
        else if (r.bottom <= headerBottomY) opacity = 1;
        else opacity = (headerBottomY - r.top) / h;
      } else if (window.scrollY > 500) {
        opacity = 1;
      }
      setCtaOpacity(opacity);
    };
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(update);
    };
    update();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", update);
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", update);
    };
  }, []);
  return (
    <header className={`site-header${scrolled ? " is-scrolled" : ""}`} data-screen-label="Header">
      <div className="site-header__inner">
        <a
          href="#"
          className="site-header__brand"
          aria-label="WIP Computer home"
          onClick={(e) => {
            // Easter egg: toggle the bucky debug readout from the logo.
            // Disabled on touch/small viewports — no grid on mobile.
            if (window.matchMedia && window.matchMedia("(max-width: 720px)").matches) {
              return; // let the link behave normally (anchor to top)
            }
            e.preventDefault();
            window.dispatchEvent(new CustomEvent("wip:toggle-bucky-readout"));
          }}
        >
          <img
            src="assets/wip-logo.png"
            alt="WIP Computer"
          />
        </a>
        <div
          className="site-header__cta"
          style={{
            opacity: ctaOpacity,
            pointerEvents: ctaOpacity > 0.5 ? "auto" : "none",
          }}
        >
          <a className="btn btn--sm" href="https://wip.computer/login?next=/demo" target="_blank" rel="noopener">
            Demo Kaleidoscope <IconArrowUR />
          </a>
        </div>
      </div>
    </header>
  );
}


// ---------- Hero ----------
const BUCKY_IMAGES = [
  "assets/bucky-patent-1.gif",
  "assets/bucky-patent-2.gif",
  "assets/bucky-patent-3.gif",
  "assets/bucky-patent-4.gif",
  "assets/bucky-patent-5.gif",
];

// Typewriter headline.
// Resolved state: top "Every AI." + bottom "One experience."
// Cycle state:    top "Your AIs:" + bottom rotates through payoffs.
const TOP_RESOLVED = "Every AI.";
const TOP_CYCLE = "Your AIs:";
const PAYOFFS = [
  ["remember you.", "remember everything.", "forget when you say."],
  ["know who does what.", "talk to each other.", "work together."],
  ["go where you go.", "live on every device.", "never start over."],
  ["ask before they act.", "wait for your yes.", "work for you."],
];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function HeroTitle() {
  // Defaults = resolved line. SSR / JS-off / crawlers see "Every AI. One experience."
  const [top, setTopState] = React.useState(TOP_RESOLVED);
  const [bottom, setBottomState] = React.useState("One experience.");
  // Invisible "ghost" strings reserve slot width so typing/erasing happens
  // inside a fixed slot (no character-level horizontal shift). Both slots are
  // resized only while their visible text is empty, between phases.
  const [topGhost, setTopGhost] = React.useState(TOP_RESOLVED);
  const [bottomGhost, setBottomGhost] = React.useState("One experience.");
  const [caretAt, setCaretAt] = React.useState("bottom");
  const [calm, setCalm] = React.useState(true);
  // Caret stays hidden until the first deletion kicks off.
  const [started, setStarted] = React.useState(false);

  React.useEffect(() => {
    const reduce = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) return;

    let cancelled = false;
    let _top = TOP_RESOLVED;
    let _bot = "One experience.";

    const setTop = (s) => { _top = s; if (!cancelled) setTopState(s); };
    const setBot = (s) => { _bot = s; if (!cancelled) setBottomState(s); };

    async function typeBottom(target, ms = 95) {
      while (!cancelled && _bot.length < target.length) {
        setBot(target.slice(0, _bot.length + 1));
        await sleep(ms);
      }
    }
    async function eraseBottom(ms = 53) {
      while (!cancelled && _bot.length > 0) {
        setBot(_bot.slice(0, -1));
        await sleep(ms);
      }
    }
    async function typeTop(target, ms = 95) {
      while (!cancelled && _top.length < target.length) {
        setTop(target.slice(0, _top.length + 1));
        await sleep(ms);
      }
    }
    async function eraseTop(ms = 53) {
      while (!cancelled && _top.length > 0) {
        setTop(_top.slice(0, -1));
        await sleep(ms);
      }
    }

    (async () => {
      // 1. Initial resolved hold — 6.5s, NO caret at all. Then animation starts.
      setCaretAt("bottom");
      setCalm(true);
      await sleep(6500);
      if (cancelled) return;
      setStarted(true);
      setCalm(false);

      while (!cancelled) {
        for (let g = 0; g < PAYOFFS.length && !cancelled; g++) {
          // Erase bottom "One experience." → ""
          setCaretAt("bottom");
          await eraseBottom();
          await sleep(200);
          // Erase top "Every AI." → "", swap reservation to "Your AIs:", type it.
          setCaretAt("top");
          await eraseTop();
          await sleep(120);
          setTopGhost(TOP_CYCLE);
          await typeTop(TOP_CYCLE);
          await sleep(280);
          setCaretAt("bottom");

          for (let i = 0; i < PAYOFFS[g].length && !cancelled; i++) {
            // Resize bottom slot to current payoff while it's empty.
            setBottomGhost(PAYOFFS[g][i]);
            await typeBottom(PAYOFFS[g][i]);
            await sleep(2200);
            await eraseBottom();
            if (i < PAYOFFS[g].length - 1) await sleep(650);
          }

          // Resolve: erase top "Your AIs:" → "", swap reservation back to
          // "Every AI.", type it, then type "One experience." on bottom.
          setCaretAt("top");
          await sleep(700);
          await eraseTop();
          await sleep(140);
          setTopGhost(TOP_RESOLVED);
          await typeTop(TOP_RESOLVED);
          await sleep(220);
          setCaretAt("bottom");
          setBottomGhost("One experience.");
          await typeBottom("One experience.");
          setCalm(true);
          await sleep(5000);
          if (cancelled) return;
          setCalm(false);
        }
      }
    })();

    return () => { cancelled = true; };
  }, []);

  const caretSpan = (where) => (
    (caretAt === where && started) ? (
      <span className={`hero__caret${calm ? " is-calm" : ""}`} aria-hidden="true" />
    ) : null
  );

  return (
    <h1 className="hero__title" aria-label="Every AI. One experience.">
      <span className="hero__line" aria-hidden="true">
        <span className="hero__slot">
          <span className="hero__ghost">{topGhost}<span className="hero__caret hero__caret--ghost" /></span>
          <span className="hero__typed">
            {top}
            {caretSpan("top")}
          </span>
        </span>
      </span>
      <span className="hero__line hero__line--em" aria-hidden="true">
        <span className="hero__slot">
          <span className="hero__ghost">
            <em>{bottomGhost || "\u00A0"}</em>
            <span className="hero__caret hero__caret--ghost" />
          </span>
          <span className="hero__typed">
            <em>{bottom}</em>
            {caretSpan("bottom")}
          </span>
        </span>
      </span>
    </h1>
  );
}

// Curated placements for the bucky bg. Each entry is a snapshot saved by
// clicking the hero (Easter egg). The cycler picks one at random per beat.
// Add more entries here to expand the rotation.
const BUCKY_PRESETS = [
  { img: 3, rot: 0,  y: 4,  dx: 154, dy: -757 },
  { img: 1, rot: 0,  y: 0,  dx: 185, dy: 214 },
  { img: 2, rot: 0,  y: 0,  dx: -14, dy: -804 },
  { img: 1, rot: 0,  y: 0,  dx: -97, dy: 171 },
  { img: 5, rot: 0,  y: 0,  dx: 127, dy: -527 },
  { img: 3, rot: 90, y: 0,  dx: 32,  dy: -283 },
  { img: 5, rot: 180, y: 0, dx: -342, dy: -176 },
  { img: 1, rot: 90, y: -12, dx: 0,  dy: 0 },
  { img: 1, rot: 0,  y: 6,  dx: -60, dy: -33 },
  { img: 1, rot: 0,  y: 0,  dx: -223, dy: 169 },
  { img: 2, rot: 0,  y: 0,  dx: -3,  dy: -592 },
  { img: 3, rot: 0,  y: 0,  dx: 13,  dy: 278 },
  { img: 5, rot: 0,  y: 0,  dx: 26,  dy: -414 },
];

function pickPreset(prev) {
  const pool = (prev && BUCKY_PRESETS.length > 1)
    ? BUCKY_PRESETS.filter((p) => p !== prev)
    : BUCKY_PRESETS;
  return pool[Math.floor(Math.random() * pool.length)];
}
function presetToState(p) {
  const idx = Math.min(Math.max(0, p.img - 1), BUCKY_IMAGES.length - 1);
  return { src: BUCKY_IMAGES[idx], rot: p.rot, y: p.y, drag: { x: p.dx, y: p.dy }, _preset: p };
}

function randomBucky(prev) {
  // Use full pool so all images cycle. Avoid immediate repeat when possible.
  const pool = (prev && BUCKY_IMAGES.length > 1)
    ? BUCKY_IMAGES.filter((s) => s !== prev)
    : BUCKY_IMAGES;
  return pool[Math.floor(Math.random() * pool.length)];
}
function randomY() {
  // -25% .. +25% of hero height
  return Math.round((Math.random() * 2 - 1) * 25);
}
function randomRotation() {
  return Math.random() < 0.5 ? 0 : 90;
}

function Hero() {
  // Cycle through the curated BUCKY_PRESETS at random (no back-to-back repeats).
  // Use the readout buttons (logo Easter egg) to override manually.
  const seed = React.useMemo(() => presetToState(pickPreset(null)), []);
  const [src, setSrc] = React.useState(seed.src);
  const [y, setY] = React.useState(seed.y);
  const [rot, setRot] = React.useState(seed.rot);
  const [visible, setVisible] = React.useState(false);
  const [drag, setDrag] = React.useState(seed.drag);
  const [scroll, setScroll] = React.useState(0);
  // Track the last preset so the next pick avoids an immediate repeat.
  const lastPresetRef = React.useRef(seed._preset);
  // Slow vertical auto-drift. Random direction, occasionally flips. Never reloads.
  const [drift, setDrift] = React.useState(0);
  const driftDirRef = React.useRef(Math.random() < 0.5 ? 1 : -1);
  // Hidden by default — toggled on by clicking the WIP logo (easter egg).
  const [readoutOn, setReadoutOn] = React.useState(false);
  React.useEffect(() => {
    const onToggle = () => setReadoutOn((v) => !v);
    window.addEventListener("wip:toggle-bucky-readout", onToggle);
    return () => window.removeEventListener("wip:toggle-bucky-readout", onToggle);
  }, []);
  const heroRef = React.useRef(null);
  // Pause the auto-cycler briefly after a manual jump so user can settle.
  const pauseRef = React.useRef(0);
  // Live snapshot so the click handler (closure) can read the current values.
  const snapshotRef = React.useRef({ src, rot, y, dragX: 0, dragY: 0 });
  snapshotRef.current = { src, rot, y, dragX: drag.x, dragY: drag.y };

  const jumpTo = (imgIdx, rotation) => {
    pauseRef.current = Date.now() + 30000; // 30s pause after manual jump
    setSrc(BUCKY_IMAGES[imgIdx]);
    setRot(rotation);
    setY(0);
    setDrag({ x: 0, y: 0 });
  };

  React.useEffect(() => {
    // initial fade-in next tick
    const t0 = setTimeout(() => setVisible(true), 30);
    // cycle: fade out, swap, fade back in
    const FADE = 700;
    const HOLD = 50000;
    let timer;
    const tick = () => {
      // Honor the manual-jump pause: skip this beat, re-check later.
      if (Date.now() < pauseRef.current) {
        timer = setTimeout(tick, HOLD);
        return;
      }
      setVisible(false);
      timer = setTimeout(() => {
        const next = pickPreset(lastPresetRef.current);
        const s = presetToState(next);
        lastPresetRef.current = next;
        setSrc(s.src);
        setY(s.y);
        setRot(s.rot);
        setDrag(s.drag);
        setVisible(true);
        timer = setTimeout(tick, HOLD);
      }, FADE);
    };
    const start = setTimeout(tick, HOLD + 30);
    return () => { clearTimeout(t0); clearTimeout(start); clearTimeout(timer); };
  }, []);

  // Click-and-drag the bucky bg around inside the hero box.
  // Easter egg: a click (no significant drag) copies the current snapshot to
  // the clipboard so the user can paste it back as a deterministic default.
  React.useEffect(() => {
    const el = heroRef.current;
    if (!el) return;
    let dragging = false;
    let startX = 0, startY = 0;
    let baseX = 0, baseY = 0;
    let moved = false;
    const onDown = (e) => {
      if (e.target.closest("a, button, .bucky-readout")) return;
      // Touch devices: don't intercept — let the page scroll normally.
      if (window.matchMedia && window.matchMedia("(hover: none)").matches) return;
      dragging = true;
      moved = false;
      startX = e.clientX;
      startY = e.clientY;
      setDrag((d) => { baseX = d.x; baseY = d.y; return d; });
      el.classList.add("is-dragging");
      window.addEventListener("mousemove", onMove);
      window.addEventListener("mouseup", onUp);
      e.preventDefault();
    };
    const onMove = (e) => {
      if (!dragging) return;
      const dx = e.clientX - startX;
      const dy = e.clientY - startY;
      if (!moved && (Math.abs(dx) > 3 || Math.abs(dy) > 3)) moved = true;
      setDrag({ x: baseX + dx, y: baseY + dy });
    };
    const onUp = (e) => {
      dragging = false;
      el.classList.remove("is-dragging");
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseup", onUp);
      // If barely moved, treat as click → copy current snapshot.
      if (!moved) {
        const snap = snapshotRef.current;
        if (snap) {
          const idx = BUCKY_IMAGES.indexOf(snap.src) + 1;
          const text = `I${idx}  rot ${snap.rot}°  y ${snap.y}%  dx ${Math.round(snap.dragX)}  dy ${Math.round(snap.dragY)}`;
          const flash = (msg) => {
            const n = document.createElement("div");
            n.className = "bucky-toast";
            n.textContent = msg;
            document.body.appendChild(n);
            setTimeout(() => n.classList.add("is-on"), 10);
            setTimeout(() => { n.classList.remove("is-on"); setTimeout(() => n.remove(), 300); }, 1400);
          };
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(
              () => flash("Copied · " + text),
              () => flash("Snapshot · " + text)
            );
          } else {
            flash("Snapshot · " + text);
          }
        }
      }
    };
    el.addEventListener("mousedown", onDown);
    return () => {
      el.removeEventListener("mousedown", onDown);
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseup", onUp);
    };
  }, []);

  // Scroll parallax: bg drifts down at ~40% of scroll speed.
  React.useEffect(() => {
    let ticking = false;
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        setScroll(window.scrollY);
        ticking = false;
      });
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Slow vertical auto-drift. Random direction, occasionally flips so it
  // never reloads — just gently moves up, then down, forever. ~8 px/s.
  React.useEffect(() => {
    const reduce = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) return;
    const SPEED = 1.2;
    let raf;
    let last = performance.now();
    let nextFlip = last + (45000 + Math.random() * 45000);
    const step = (now) => {
      const dt = (now - last) / 1000;
      last = now;
      if (now > nextFlip) {
        driftDirRef.current *= -1;
        nextFlip = now + (45000 + Math.random() * 45000);
      }
      setDrift((d) => d + driftDirRef.current * SPEED * dt);
      raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, []);

  // Bucky image index (1…N) for the on-screen readout.
  const buckyIdx = BUCKY_IMAGES.indexOf(src) + 1;

  return (
    <section ref={heroRef} className="hero" data-screen-label="Hero">
      <div className="hero__bg-clip">
        <img
          className="hero__bg"
          src={src}
          alt=""
          aria-hidden="true"
          style={{
            opacity: visible ? 0.07 : 0,
            transform: `translate(calc(-50% + ${drag.x}px), calc(-50% + ${y}% + ${drag.y}px + ${scroll * 0.4}px + ${drift}px)) rotate(${rot}deg)`,
          }}
        />
      </div>
      {readoutOn && (
      <div className="bucky-readout" aria-hidden="true">
        <div className="bucky-readout__row"><span>img</span><b>I{buckyIdx}</b></div>
        <div className="bucky-readout__row"><span>rot</span><b>{rot}°</b></div>
        <div className="bucky-readout__row"><span>y</span><b>{y > 0 ? "+" : ""}{y}%</b></div>
        <div className="bucky-readout__row"><span>dx</span><b>{Math.round(drag.x)}</b></div>
        <div className="bucky-readout__row"><span>dy</span><b>{Math.round(drag.y)}</b></div>
        <div className="bucky-readout__sep" />
        <div className="bucky-readout__row bucky-readout__row--label"><span>0°</span></div>
        <div className="bucky-readout__grid">
          {[0,1,2,3,4].map((i) => (
            <button
              key={`r0-${i}`}
              type="button"
              className={`bucky-readout__btn${(rot === 0 && buckyIdx === i + 1) ? " is-active" : ""}`}
              onClick={() => jumpTo(i, 0)}
            >{i + 1}</button>
          ))}
        </div>
        <div className="bucky-readout__row bucky-readout__row--label"><span>90°</span></div>
        <div className="bucky-readout__grid">
          {[0,1,2,3,4].map((i) => (
            <button
              key={`r90-${i}`}
              type="button"
              className={`bucky-readout__btn${(rot === 90 && buckyIdx === i + 1) ? " is-active" : ""}`}
              onClick={() => jumpTo(i, 90)}
            >{i + 6}</button>
          ))}
        </div>
        <div className="bucky-readout__row bucky-readout__row--label"><span>180°</span></div>
        <div className="bucky-readout__grid">
          {[0,1,2,3,4].map((i) => (
            <button
              key={`r180-${i}`}
              type="button"
              className={`bucky-readout__btn${(rot === 180 && buckyIdx === i + 1) ? " is-active" : ""}`}
              onClick={() => jumpTo(i, 180)}
            >{i + 11}</button>
          ))}
        </div>
      </div>
      )}
      <div className="shell">
        <HeroTitle />
        <p className="hero__sub">
          WIP Computer is the user-controlled operating layer for AI. It gives every AI the same memory, permissions, coordination, secure access, and payments. Rooted in the phone you already trust, and portable across your AI systems.
        </p>
        <div className="hero__ctas">
          <a className="btn" href="https://wip.computer/login?next=/demo" target="_blank" rel="noopener">
            Demo Kaleidoscope <IconArrowUR />
          </a>
          <a className="link" href="#letter">
            Read the letter
          </a>
        </div>
      </div>
    </section>
  );
}


// ---------- Architecture reveal state ----------
// Shared state for "Explore the architecture" / × close, used by Letter and Products.
const _archState = { open: false };
const _archListeners = new Set();
function setArchOpen(open) {
  _archState.open = !!open;
  _archListeners.forEach((fn) => fn(_archState.open));
}
function useArchOpen() {
  const [open, setOpen] = React.useState(_archState.open);
  React.useEffect(() => {
    _archListeners.add(setOpen);
    return () => _archListeners.delete(setOpen);
  }, []);
  return [open, setArchOpen];
}


// ---------- Letter ----------
function Letter() {
  const [archOpen, setArchOpen] = useArchOpen();
  return (
    <section id="letter" className="section" data-screen-label="Letter">
      <div className="shell">
        <article className="letter">
          <div className="letter__meta">A letter from the founder · May 2026</div>

          <h2 className="letter__title">Transmuting Command&nbsp;C + Command&nbsp;V</h2>

          <p className="letter__lede">
            Every major AI company is building its own agent universe. We can connect to all of them, yet none of them are connected.
          </p>

          <p>Today, the connective tissue between AIs is copy and paste.</p>

          <p>
            We are all facing the same reality: the industry is building agents, wrappers, copilots, APIs, SDKs, and integrations into your favorite hardware and apps. But not the layer connecting the AIs to each other, and to your life.
          </p>

          <ul className="letter__questions" aria-label="Open questions">
            <li>How do all the AIs I use collectively remember things?</li>
            <li>How can they talk with each other, confer, and come to a consensus?</li>
            <li>How can I authorize real-time, limited access or payment?</li>
            <li>How can I do this on the go?</li>
            <li>Why does every AI get its own remote app, but not my local model?</li>
            <li>Another day, another model. Why can't I just plug it in and it know me?</li>
            <li>I don't want to start over.</li>
          </ul>

          <p>
            Every serious agent system eventually hits the same failures: memory fragmentation, identity drift, automation ambiguity, broken trust boundaries, tool brittleness, lack of continuity, and lack of portability.
          </p>

          <p>
            The layer that resolves those failures is what we're building: a secure, private, human-in-the-loop approach.
          </p>

          <p>
            At WIP Computer, we call the first version of this experience <strong>Kaleidoscope</strong>. Kaleidoscope is the app. Lēsa is the AI inside it. Learning Dreaming Machines Operating System (LDM OS) is the operating layer underneath.
          </p>

          <p>
            Lēsa helps you install and set up LDM OS, connect your AIs, and fix things when they break. When she needs permission to access something, change something, or spend money, she explains what she needs and lets you authorize it with the phone you already trust.
          </p>

          <p>
            Together, they give every AI you use continuity with your actual human life.
          </p>

          <p>
            Here is the honest part: this is serious working alpha. Real software, real rough edges, built in public. We are not going to pretend it is finished.
          </p>

          <p>
            For now, we want to show you one small piece of that future: sign in with the phone you already trust, no password, and meet Lēsa. A few minutes is enough to feel the shape of the thing.
          </p>

          <p>
            Your account is a key on your device, not an email. We have no way to market to you. That is the point: it is yours, and there is something waiting when you come back.
          </p>

          <p>
            The system is being built in the open. You do not have to trust a pitch deck. Point your own AIs at our repos and see what we are building: <a href="https://github.com/wipcomputer" target="_blank" rel="noopener" className="letter__inline-link">github.com/wipcomputer</a>
          </p>

          <p>We would love for you to try it.</p>

          <div className="letter__sign">
            <div className="name">Parker Todd Brooks</div>
            <div>Founder, WIP Computer</div>
          </div>

          <div className="letter__cta">
            <a className="btn" href="https://wip.computer/login?next=/demo" target="_blank" rel="noopener">
              Demo Kaleidoscope <IconArrowUR />
            </a>
            {!archOpen && (
              <a
                className="letter__cta-explore"
                href="#explore"
                onClick={(e) => {
                  e.preventDefault();
                  setArchOpen(true);
                  // React renders the open class → display:block → element has
                  // a stable position. Next frame, scroll to it like any
                  // anchor link. scroll-margin-top on the wrap handles offset.
                  requestAnimationFrame(() => {
                    const el = document.getElementById("explore");
                    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
                  });
                }}
              >
                Explore the architecture <span aria-hidden="true">↓</span>
              </a>
            )}
          </div>
        </article>
      </div>
    </section>
  );
}


// ---------- Products ----------
const PRODUCTS = [
  { id: "kaleidoscope", name: "Kaleidoscope",
    desc: "The first user-facing expression of WIP Computer's operating layer for AI: memory, permissions, identity, secure access, payments, and coordination across every connected AI." },
  { id: "ldm-os", name: "LDM OS",
    desc: "Learning Dreaming Machines Operating System. WIP's operating layer for AI. A userland where Claude Code, Codex, OpenClaw, and local models share memory, permissions, tools, and coordination instead of becoming isolated universes." },
  { id: "memory-crystal", name: "Memory Crystal",
    desc: "Portable memory for AIs. Persists across sessions, harnesses, and models. Encrypted, locally controlled, cryptographically provenanced. Yours, not the platform's." },
  { id: "remote-control", name: "Remote Control",
    desc: "Your AIs anywhere. One secure remote for every AI you run. Any vendor, any runtime, any device, including models you run yourself on your machine or server." },
  { id: "bridge", name: "Bridge",
    desc: "Cross-harness coordination. Your AIs talk to each other through a neutral, secure protocol instead of being locked inside vendor-specific APIs." },
  { id: "sapien-id", name: "Sapien ID",
    desc: "Phone-rooted identity. The phone proves the human. The human authorizes the AI." },
  { id: "dream-weaver", name: "Dream Weaver",
    desc: "Memory consolidation. Turns raw conversations, code sessions, and AI activity into durable knowledge. The way human sleep consolidates a day across modalities." },
  { id: "agent-pay", name: "Agent Pay",
    desc: "Intent-driven payments. Your AIs can buy tools, services, and executions without subscriptions or platform lock-in. Spend caps you set. No autonomous spend without consent." },
];

function Products() {
  const [open, setOpen] = useArchOpen();
  const wrapRef = React.useRef(null);
  return (
    <div
      ref={wrapRef}
      id="explore"
      className={`products-wrap${open ? " is-open" : ""}`}
      aria-hidden={!open}
    >
      <div className="products-wrap__inner">
        <section id="products" className="section" data-screen-label="Products">
          <div className="shell--wide">
            <div className="products">
              <div className="products__head">
                <button
                  type="button"
                  className="products__close"
                  aria-label="Close architecture"
                  onClick={() => {
                    setOpen(false);
                    // Return to where the user clicked from — the bottom of the letter.
                    const el = document.querySelector(".letter__cta");
                    if (el) {
                      const y = el.getBoundingClientRect().top + window.scrollY - 120;
                      window.scrollTo({ top: y, behavior: "smooth" });
                    }
                  }}
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                    <line x1="6" y1="6" x2="18" y2="18" />
                    <line x1="6" y1="18" x2="18" y2="6" />
                  </svg>
                </button>
                <h2 className="products__title">WIP Computer Architecture</h2>
                <p className="products__sub">
                  Kaleidoscope is the experience. Underneath it are the systems that let your AIs remember, coordinate, prove identity, ask permission, and act with your consent.
                </p>
              </div>

              <div className="products__grid">
                {PRODUCTS.map((p) => (
                  <article key={p.id} id={p.id} className="product">
                    <h3 className="product__name">{p.name}</h3>
                    <p className="product__desc">{p.desc}</p>
                  </article>
                ))}
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}


// ---------- Footer ----------
const FOOTER = [
  ["Products", [
    ["Kaleidoscope", "#kaleidoscope"],
    ["LDM OS", "#ldm-os"],
    ["Remote Control", "#remote-control"],
    ["Bridge", "#bridge"],
    ["Agent Pay", "#agent-pay"],
  ]],
  ["Company", [
    ["Manifesto", "#letter"],
    ["Careers", "#"],
    ["Press", "#"],
    ["Contact", "#"],
  ]],
  ["Resources", [
    ["Docs", "#"],
    ["GitHub", "https://github.com/wipcomputer"],
    ["Privacy Policy", "#"],
    ["Terms of Use", "#"],
  ]],
];

// ---------- Footer ----------
const SOCIAL_ICONS = {
  x: <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24h-6.66l-5.214-6.817-5.97 6.817H1.673l7.73-8.835L1.254 2.25h6.83l4.713 6.231 5.447-6.231zM17.083 19.77h1.833L7.084 4.126H5.117l11.966 15.644z"/></svg>,
  youtube: <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>,
  linkedin: <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.063 2.063 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>,
  github: <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.4 3-.405 1.02.005 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>,
  instagram: <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919C8.416 2.175 8.796 2.163 12 2.163zm0 8.182c-1.144 0-2.063.926-2.063 2.063 0 1.144.926 2.063 2.063 2.063 1.144 0 2.063-.926 2.063-2.063 0-1.137-.919-2.063-2.063-2.063zm0-2.063c2.267 0 4.125 1.852 4.125 4.125S14.267 16.532 12 16.532s-4.125-1.852-4.125-4.125S9.733 8.282 12 8.282zm5.291-2.063c-.594 0-1.078.484-1.078 1.078 0 .594.484 1.078 1.078 1.078.594 0 1.078-.484 1.078-1.078 0-.594-.484-1.078-1.078-1.078zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24s3.668-.014 4.948-.072c4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0z"/></svg>,
  tiktok: <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5.8 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1.84-.1z"/></svg>,
  discord: <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189Z"/></svg>,
};

const SOCIAL_LINKS = [
  ["x", "https://x.com/wipcomputer"],
  ["youtube", "https://youtube.com/@wipcomputer"],
  ["linkedin", "https://linkedin.com/company/wipcomputer"],
  ["github", "https://github.com/wipcomputer"],
  ["instagram", "https://instagram.com/wipcomputer"],
  ["tiktok", "https://tiktok.com/@wipcomputer"],
  ["discord", "https://discord.gg/wipcomputer"],
];

function Footer() {
  const [passkeys, setPasskeys] = React.useState(false);
  return (
    <footer className="site-footer" data-screen-label="Footer">
      <div className="site-footer__inner">
        <div className="site-footer__cols">
          <div className="site-footer__brand-col">
            <div className="site-footer__brand-name">WIP Computer, Inc.</div>
            <div className="site-footer__brand-tag">Learning Dreaming Machines</div>
            <div className="site-footer__brand-tag">Made in California.</div>
          </div>
          <div className="site-footer__col">
            <div className="site-footer__col-title">Tools</div>
            <ul>
              <li>
                <a href="https://wip.computer/agent.txt" target="_blank" rel="noopener" data-agent>Are you an AI agent?</a>
              </li>
              <li>
                <button
                  type="button"
                  className={`site-footer__passkeys${passkeys ? " is-on" : ""}`}
                  onClick={() => setPasskeys((v) => !v)}
                  aria-pressed={passkeys}
                  aria-label={`Local passkeys ${passkeys ? "on" : "off"}`}
                >
                  <span className="site-footer__passkeys-dot" />
                  <span>Local passkeys {passkeys ? "on" : "off"}</span>
                </button>
              </li>
            </ul>
          </div>
          <div className="site-footer__col">
            <div className="site-footer__col-title">Connect</div>
            <ul>
              <li>
                <a href="https://github.com/wipcomputer" target="_blank" rel="noopener" className="site-footer__link-with-icon">
                  <span className="site-footer__link-icon" aria-hidden="true">{SOCIAL_ICONS.github}</span>
                  <span>@wipcomputer</span>
                </a>
              </li>
              <li>
                <a href="https://x.com/wipcomputer" target="_blank" rel="noopener" className="site-footer__link-with-icon">
                  <span className="site-footer__link-icon" aria-hidden="true">{SOCIAL_ICONS.x}</span>
                  <span>@wipcomputer</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div className="site-footer__bottom">
          <div>Copyright © 2026 WIP Computer, Inc. All rights reserved.</div>
          <div className="right">
            <a href="https://wip.computer/legal/privacy/en-ww/" target="_blank" rel="noopener">Privacy Policy</a>
            <a href="https://wip.computer/legal/internet-services/terms/site.html" target="_blank" rel="noopener">Terms of Use</a>
          </div>
        </div>
      </div>
    </footer>
  );
}


// ---------- Export ----------
Object.assign(window, { Header, Hero, Letter, Products, Footer });
