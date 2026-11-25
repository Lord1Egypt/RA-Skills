/*!
 * sketchy-deck.js — slides in a sketchbook
 * A 1920 x 1080 stage scaled to the window, page turns that swing away on
 * rotateY like the leaves of a real book, step reveals, receipt-printer
 * reveals, counters, overview, presenter notes, print and video modes.
 * Needs sketchy.js. MIT License. https://github.com/OthmanAdi/sketchy
 *
 * <main class="sk-deck" data-seed="q3-update" data-transition="page">
 *   <section class="sk-slide" data-layout="title" data-duration="6" data-notes="...">...</section>
 * </main>
 * <script>SketchyDeck.mount()</script>
 */
(function (global) {
  'use strict';

  var doc = global.document;
  var W = 1920, H = 1080;
  var S = global.Sketchy;
  var P = (S && S.params) || {};

  /* ------------------------------------------------------------------ *
   * Stylesheet: stage, transitions, layouts. Sizes are stage pixels.
   * ------------------------------------------------------------------ */
  var CSS = [
    '.sk-deck { position: fixed; inset: 0; overflow: hidden; perspective: 1400px; perspective-origin: 50% 50%; }',
    '.sk-viewport { position: absolute; inset: 0; }',
    '.sk-stage { position: absolute; left: 50%; top: 50%; width: 1920px; height: 1080px; transform-origin: 0 0; transform-style: preserve-3d; perspective: 1400px;',
    '  --sk-size-hero: 132px; --sk-size-title: 84px; --sk-size-big: 62px; --sk-size-sub: 40px; --sk-size-body: 34px; --sk-size-fine: 28px; font-size: var(--sk-size-body); line-height: 1.25; }',
    '.sk-sky { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }',
    '.sk-slide { position: absolute; inset: 0; width: 1920px; height: 1080px; padding: 92px 120px 104px; visibility: hidden; pointer-events: none; display: grid; transform-style: preserve-3d; backface-visibility: hidden; }',
    '.sk-slide.is-current, .sk-slide.is-leaving { visibility: visible; }',
    '.sk-slide.is-current { pointer-events: auto; z-index: 2; }',
    '.sk-slide.is-leaving { z-index: 3; pointer-events: none; }',
    '.sk-slide.is-leaving.is-under { z-index: 1; }',
    /* transitions: page (default), slide, fade, none, cover */
    '.sk-slide.in-page, .sk-slide.in-cover { animation: sk-sheet-in 360ms var(--sk-ease) both; animation-delay: 140ms; }',
    '.sk-slide.out-page { transform-origin: left center; animation: sk-page-over 650ms var(--sk-ease-page) both; }',
    '.sk-slide.out-page-back { transform-origin: right center; animation: sk-page-back 650ms var(--sk-ease-page) both; }',
    '.sk-slide.out-cover { transform-origin: left center; animation: sk-deck-cover 800ms var(--sk-ease-cover) both; }',
    '.sk-slide.in-slide { animation: sk-deck-slide-in 520ms var(--sk-ease) both; }',
    '.sk-slide.in-slide-back { animation: sk-deck-slide-in-back 520ms var(--sk-ease) both; }',
    '.sk-slide.out-slide { animation: sk-deck-slide-out 360ms var(--sk-ease-page) both; }',
    '.sk-slide.out-slide-back { animation: sk-deck-slide-out-back 360ms var(--sk-ease-page) both; }',
    '.sk-slide.in-fade { animation: sk-veil-in 420ms ease-out both; }',
    '.sk-slide.out-fade { animation: sk-veil-in 260ms ease-in reverse both; }',
    '@keyframes sk-deck-cover { 0% { transform: rotateY(0); } 100% { transform: rotateY(-165deg); opacity: 0; } }',
    '@keyframes sk-deck-slide-in { from { opacity: 0; transform: translateX(60px) rotate(.6deg); } }',
    '@keyframes sk-deck-slide-in-back { from { opacity: 0; transform: translateX(-60px) rotate(-.6deg); } }',
    '@keyframes sk-deck-slide-out { to { opacity: 0; transform: translateX(-40px); } }',
    '@keyframes sk-deck-slide-out-back { to { opacity: 0; transform: translateX(40px); } }',
    '@keyframes sk-deck-bump { 0%, 100% { transform: translateX(0); } 40% { transform: translateX(var(--bump, 12px)); } }',
    '@keyframes sk-line-in { from { opacity: 0; transform: translateY(5px); } }',
    '.sk-stage.is-bump { animation: sk-deck-bump 260ms var(--sk-ease); }',
    /* steps and print-style reveals */
    '.sk-slide [data-step] { transition: opacity 260ms var(--sk-ease), transform 260ms var(--sk-ease); }',
    '.sk-slide [data-step].is-hidden { opacity: 0; transform: translateY(10px) rotate(-.6deg); }',
    '.sk-slide.is-current [data-reveal="print"] > * { animation: sk-line-in 380ms var(--sk-ease) both; animation-delay: calc(180ms + var(--i, 0) * 95ms); }',
    '.sk-slide.is-current [data-reveal="sheet"] { animation: sk-sheet-in 260ms var(--sk-ease) both; animation-delay: var(--delay, 0ms); }',
    '.sk-slide.is-current .sk-stamp[data-slam] { animation: sk-slam 360ms var(--sk-ease-slam) both; animation-delay: var(--delay, 600ms); }',
    '.sk-slide.is-current .sk-postcard[data-reveal] { animation: sk-card-in 420ms var(--sk-ease-card) both; animation-delay: var(--delay, 200ms); }',
    /* HUD */
    '.sk-hud { position: fixed; left: 0; right: 0; bottom: 0; z-index: 20; display: flex; justify-content: space-between; align-items: flex-end; gap: 12px; padding: 12px max(14px, env(safe-area-inset-right)) max(12px, env(safe-area-inset-bottom)) max(14px, env(safe-area-inset-left)); pointer-events: none; transition: opacity 400ms var(--sk-ease); }',
    '.sk-hud > * { pointer-events: auto; }',
    '.sk-hud .sk-group { display: flex; gap: 8px; align-items: center; }',
    '.sk-hud .sk-btn { min-height: 44px; min-width: 44px; padding: 2px 12px 4px; font-size: 23px; }',
    '.sk-page-label { font: 400 20px/1 var(--sk-font-hand); opacity: .78; padding: 0 6px; font-variant-numeric: tabular-nums; }',
    '.sk-deck.is-idle .sk-hud { opacity: 0; }',
    'html.sk-clean .sk-hud, html.sk-static .sk-hud, html.sk-clean .sk-presenter, html.sk-static .sk-presenter { display: none !important; }',
    '.sk-deck.is-idle .sk-hud:hover { opacity: 1; }',
    'html.sk-clean, html.sk-clean * { cursor: none !important; }',
    '.sk-presenter { position: fixed; left: 50%; bottom: 74px; transform: translateX(-50%); z-index: 21; width: min(980px, 92vw); max-height: 38vh; overflow: auto; display: none; }',
    '.sk-deck.is-presenting .sk-presenter { display: block; }',
    '.sk-presenter .sk-presenter-meta { display: flex; justify-content: space-between; font-size: 18px; opacity: .7; margin-bottom: 6px; }',
    '.sk-presenter .sk-presenter-notes { font-size: 22px; line-height: 1.3; white-space: pre-wrap; }',
    /* overview: every slide at a fifth of its size */
    '.sk-deck.is-overview { overflow: auto; perspective: none; }',
    '.sk-deck.is-overview .sk-viewport { position: static; }',
    '.sk-deck.is-overview .sk-stage { position: static; transform: none !important; width: auto; height: auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(384px, 1fr)); gap: 28px; padding: 40px; perspective: none; }',
    '.sk-deck.is-overview .sk-slide { position: relative; visibility: visible; zoom: .2; pointer-events: auto; cursor: pointer; animation: none !important; transform: none !important; opacity: 1 !important; outline: 6px solid transparent; }',
    '.sk-deck.is-overview .sk-slide:hover, .sk-deck.is-overview .sk-slide.is-current { outline-color: var(--sk-red); outline-style: dashed; }',
    '.sk-deck.is-overview .sk-slide::after { content: attr(data-number); position: absolute; left: 24px; bottom: 16px; font: 600 64px/1 var(--sk-font-hand); opacity: .55; }',
    '.sk-deck.is-overview .sk-slide [data-step].is-hidden { opacity: 1; transform: none; }',
    /* print and export: one slide per page, each on its own paper */
    'html.sk-print, html.sk-print body { width: 1920px; overflow: visible; background-attachment: scroll; }',
    'html.sk-print .sk-deck { position: static; overflow: visible; perspective: none; }',
    'html.sk-print .sk-viewport { position: static; }',
    'html.sk-print .sk-stage { position: static; transform: none !important; display: block; perspective: none; }',
    'html.sk-print .sk-slide { position: relative; visibility: visible; break-after: page; page-break-after: always; overflow: hidden; background-color: var(--sk-paper); background-image: radial-gradient(130% 100% at 50% 45%, transparent 35%, rgba(var(--sk-shadow), .09) 60%, rgba(var(--sk-shadow), .38) 100%), var(--sk-paper-pattern), var(--sk-paper-texture); }',
    'html.sk-print .sk-slide [data-step].is-hidden { opacity: 1; transform: none; }',
    'html.sk-print .sk-hud, html.sk-print .sk-presenter { display: none !important; }',
    '@page { size: 1920px 1080px; margin: 0; }',
    /* ------- layouts ------- */
    '.sk-slide { align-content: start; }',
    '.sk-slide :is(.sk-stack, .sk-sheet, header) > :is(.sk-tape, .sk-stamp, .sk-btn, .sk-door, .sk-kicker) { justify-self: start; }',
    '.sk-slide :is(.sk-center, [data-layout="title"] .sk-sheet, [data-layout="big-number"]) > :is(.sk-stamp, .sk-btn, .sk-kicker) { justify-self: center; }',
    '.sk-slide .sk-kicker { font: 600 var(--sk-size-fine)/1 var(--sk-font-hand); opacity: .86; letter-spacing: .12em; text-transform: uppercase; }',
    '.sk-slide .sk-corner { position: absolute; left: 44px; top: 34px; display: grid; gap: 6px; max-width: 900px; z-index: 4; }',
    '.sk-slide .sk-corner .sk-corner-title { font: 600 40px/1.05 var(--sk-font-hand); }',
    '.sk-slide .sk-corner .sk-corner-task { font: 400 31px/1.12 var(--sk-font-hand); }',
    '.sk-slide .sk-corner .sk-corner-hint { font: 400 26px/1.15 var(--sk-font-hand); opacity: .88; }',
    '.sk-slide .sk-margin { position: absolute; right: 48px; top: 40px; max-width: 640px; z-index: 4; font-size: 26px; }',
    '.sk-slide .sk-disclose { position: absolute; left: 44px; bottom: 34px; font: 400 26px/1.2 var(--sk-font-hand); max-width: 900px; }',
    '.sk-slide .sk-source { position: absolute; right: 48px; bottom: 34px; font: 400 26px/1.2 var(--sk-font-hand); max-width: 760px; text-align: right; }',
    '.sk-slide .sk-source::before { content: "§ "; color: var(--sk-red-ink); font-weight: 600; }',
    /* cover */
    '.sk-slide[data-layout="cover"] { padding: 40px; }',
    '.sk-slide[data-layout="cover"] > .sk-cover { position: absolute; inset: 40px; min-height: 0; }',
    '.sk-slide[data-layout="cover"] .sk-label { min-width: 980px; padding: 56px 120px 46px; }',
    '.sk-slide[data-layout="cover"] .sk-label-title { font-size: 150px; }',
    '.sk-slide[data-layout="cover"] .sk-label-sub { font-size: 44px; }',
    '.sk-slide[data-layout="cover"] .sk-door { font-size: 40px; padding: 18px 40px 20px; cursor: pointer; }',
    '.sk-slide[data-layout="cover"] .sk-cover-foot { font-size: 24px; bottom: 36px; }',
    /* title and section: one centred sheet */
    '.sk-slide[data-layout="title"], .sk-slide[data-layout="section"], .sk-slide[data-layout="end"] { place-content: center; justify-items: center; text-align: center; }',
    '.sk-slide[data-layout="title"] > .sk-sheet { width: 1180px; padding: 64px 90px 58px; display: grid; gap: 18px; justify-items: center; }',
    '.sk-slide[data-layout="title"] h1 { font-size: 112px; }',
    '.sk-slide[data-layout="section"] .sk-chapter { font: 600 34px/1 var(--sk-font-hand); color: var(--sk-red-ink); }',
    '.sk-slide[data-layout="section"] h1 { font-size: 150px; }',
    /* split: picture left, words right (the how-to page) */
    '.sk-slide[data-layout="split"] { grid-template-columns: 760px minmax(0, 1fr); gap: 72px; align-content: center; align-items: center; }',
    '.sk-slide[data-layout="split"].is-flipped { grid-template-columns: minmax(0, 1fr) 760px; }',
    '.sk-slide[data-layout="split"] h2 { font-size: 72px; margin-bottom: 18px; }',
    /* steps: numbered how-to with a picture per step */
    '.sk-slide[data-layout="steps"] { align-content: center; gap: 34px; }',
    '.sk-slide[data-layout="steps"] .sk-step-list { display: grid; grid-template-columns: repeat(var(--cols, 3), minmax(0, 1fr)); gap: 44px; counter-reset: sk-step; }',
    '.sk-slide[data-layout="steps"] .sk-step { display: grid; gap: 10px; align-content: start; counter-increment: sk-step; }',
    '.sk-slide[data-layout="steps"] .sk-step h3 { font-size: 40px; }',
    '.sk-slide[data-layout="steps"] .sk-step h3::before { content: counter(sk-step) ". "; }',
    '.sk-slide[data-layout="steps"] .sk-step svg[data-sketch] { width: 300px; }',
    /* chart: corner title, big chart, margin maths */
    '.sk-slide[data-layout="chart"] { padding: 190px 120px 120px; }',
    '.sk-slide[data-layout="chart"] .sk-chart { width: 100%; height: 100%; margin: 0; }',
    /* big number */
    '.sk-slide[data-layout="big-number"] { place-content: center; justify-items: center; text-align: center; gap: 10px; }',
    '.sk-slide[data-layout="big-number"] .sk-number { font: 700 260px/0.95 var(--sk-font-mono); color: var(--sk-figure); letter-spacing: -.04em; font-variant-numeric: tabular-nums; }',
    '.sk-slide[data-layout="big-number"] .sk-number small { font-size: .32em; letter-spacing: 0; }',
    '.sk-slide[data-layout="big-number"] .sk-number-label { font: 600 54px/1.1 var(--sk-font-hand); max-width: 1300px; }',
    '.sk-slide[data-layout="big-number"] .sk-number-bench { font: 400 34px/1.2 var(--sk-font-hand); opacity: .88; }',
    /* compare: plan vs record, before vs after */
    '.sk-slide[data-layout="compare"] { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 64px; align-content: center; }',
    '.sk-slide[data-layout="compare"] > header { grid-column: 1 / -1; }',
    '.sk-slide[data-layout="compare"] .sk-sheet { display: grid; gap: 16px; align-content: start; min-height: 520px; }',
    /* quote */
    '.sk-slide[data-layout="quote"] { place-content: center; padding: 120px 240px; }',
    '.sk-slide[data-layout="quote"] blockquote { margin: 0; font: 600 92px/1.08 var(--sk-font-hand); color: var(--sk-ink); text-wrap: balance; }',
    '.sk-slide[data-layout="quote"] blockquote::before { content: "\\201C"; color: var(--sk-red); margin-left: -.45em; padding-right: .05em; }',
    '.sk-slide[data-layout="quote"] cite { display: block; margin-top: 30px; font: 400 36px/1.1 var(--sk-font-hand); font-style: normal; opacity: .88; }',
    /* timeline, ledger, board, letter */
    '.sk-slide[data-layout="timeline"] { align-content: center; gap: 40px; }',
    '.sk-slide[data-layout="ledger"] { grid-template-columns: minmax(0, 1fr) 760px; gap: 80px; align-content: center; align-items: center; }',
    '.sk-slide[data-layout="board"] { align-content: start; gap: 28px; padding-top: 170px; }',
    '.sk-slide[data-layout="board"] .sk-plates { display: grid; grid-template-columns: repeat(var(--cols, 3), minmax(0, 1fr)); gap: 30px; }',
    '.sk-slide[data-layout="letter"] { place-content: center; justify-items: center; }',
    '.sk-slide[data-layout="letter"] > .sk-sheet { width: 1100px; padding: 54px 70px 50px; display: grid; gap: 12px; text-align: left; }',
    '.sk-slide[data-layout="letter"] .sk-letter-kicker { text-align: center; font-size: 30px; opacity: .9; }',
    '.sk-slide[data-layout="letter"] h2 { text-align: center; font-size: 86px; margin-bottom: 8px; }',
    '.sk-slide[data-layout="letter"] .sk-letter-row { font-size: 34px; line-height: 1.25; }',
    '.sk-slide[data-layout="letter"] .sk-letter-row b { font-weight: 600; }',
    '.sk-slide[data-layout="letter"] .sk-letter-hint { text-align: center; font-size: 28px; opacity: .88; margin-top: 4px; }',
    '.sk-slide[data-layout="letter"] .sk-letter-actions { display: flex; justify-content: center; gap: 18px; margin-top: 14px; }',
    '.sk-slide[data-layout="end"] .sk-postcard { width: 1180px; text-align: left; font-size: 40px; }',
    '.sk-slide[data-layout="end"] .sk-postcard h2 { font-size: 92px !important; }',
    '.sk-slide[data-layout="end"] .sk-postcard .sk-line { font-size: 44px; }',
    /* buttons on the stage are bigger */
    '.sk-stage .sk-btn { min-height: 64px; font-size: 34px; padding: 6px 28px 9px; }',
    '.sk-stage .sk-stamp { font-size: 30px; }',
    '.sk-stage .sk-stamp.is-big { font-size: 84px; border-width: 5px; outline-width: 2px; outline-offset: -11px; }',
    '.sk-stage .sk-maths { font-size: 27px; }',
    '.sk-stage .sk-callout { font-size: 26px; padding: 14px 20px 16px; }',
    '.sk-stage .sk-slip { font-size: 26px; max-width: 520px; }',
    '.sk-stage .sk-rlabel { font-size: 26px; }',
    '.sk-stage .sk-rlabel small { font-size: .82em; }',
    '@media (prefers-reduced-motion: reduce) {',
    '  .sk-slide.out-page, .sk-slide.out-page-back, .sk-slide.out-cover, .sk-slide.out-slide, .sk-slide.out-slide-back { animation: sk-veil-in 200ms reverse both; }',
    '  .sk-slide.in-page, .sk-slide.in-cover, .sk-slide.in-slide, .sk-slide.in-slide-back { animation: none; }',
    '  .sk-slide.is-current [data-reveal="print"] > *, .sk-slide.is-current .sk-stamp[data-slam] { animation: none; }',
    '}'
  ].join('\n');

  function injectCSS() {
    if (doc.getElementById('sk-deck-css')) return;
    var s = doc.createElement('style');
    s.id = 'sk-deck-css';
    s.textContent = CSS;
    (doc.head || doc.documentElement).appendChild(s);
  }

  /* ------------------------------------------------------------------ *
   * State
   * ------------------------------------------------------------------ */
  var reduced = !!(S && S.reducedMotion);
  var mode = {
    print: 'print' in P, still: 'static' in P || 'print' in P,
    overview: 'overview' in P, autoplay: 'autoplay' in P || 'video' in P,
    video: 'video' in P, presenter: 'presenter' in P, clean: 'video' in P || 'clean' in P
  };
  var deck = {
    el: null, stage: null, slides: [], index: -1, count: 0,
    steps: [], stepAt: [], visited: [], listeners: {}, busy: false,
    transition: 'page', duration: 6, ready: null, music: null
  };
  var readyResolve;
  deck.ready = new Promise(function (r) { readyResolve = r; });

  function emit(name, detail) {
    (deck.listeners[name] || []).forEach(function (fn) { try { fn(detail); } catch (e) { console.error(e); } });
    try { doc.dispatchEvent(new CustomEvent('sk:' + name, { detail: detail })); } catch (e) { /* old engine */ }
  }
  /* 'change' is the documented name; 'slide' is the event name on document */
  function on(name, fn) { if (name === 'change') name = 'slide'; (deck.listeners[name] = deck.listeners[name] || []).push(fn); return deck; }

  /* ------------------------------------------------------------------ *
   * Mount
   * ------------------------------------------------------------------ */
  function mount(main) {
    injectCSS();
    main = main || doc.querySelector('main.sk-deck, .sk-deck');
    if (!main) { console.warn('[sketchy-deck] no <main class="sk-deck"> found'); return deck; }
    deck.el = main;
    var html = doc.documentElement;
    if (mode.print) html.classList.add('sk-print');
    if (mode.clean) html.classList.add('sk-clean');
    if (mode.still) html.classList.add('sk-static');
    if (!main.getAttribute('data-seed')) console.warn('[sketchy-deck] add data-seed to <main class="sk-deck"> so every render draws the same lines');
    deck.transition = main.getAttribute('data-transition') || 'page';
    deck.duration = parseFloat(main.getAttribute('data-duration')) || 6;
    deck.music = main.getAttribute('data-music') || null;

    var viewport = doc.createElement('div'); viewport.className = 'sk-viewport';
    var stage = doc.createElement('div'); stage.className = 'sk-stage';
    deck.slides = Array.prototype.slice.call(main.querySelectorAll(':scope > .sk-slide'));
    deck.slides.forEach(function (s, i) {
      s.setAttribute('data-number', String(i + 1));
      s.setAttribute('aria-roledescription', 'slide');
      s.setAttribute('aria-label', (i + 1) + ' of ' + deck.slides.length);
      if (!s.id) s.id = 'slide-' + (i + 1);
      // number receipt lines so they print one after another
      s.querySelectorAll('[data-reveal="print"]').forEach(function (box) {
        Array.prototype.forEach.call(box.children, function (c, k) { c.style.setProperty('--i', k); });
      });
      stage.appendChild(s);
    });
    deck.count = deck.slides.length;
    deck.steps = deck.slides.map(function (s) {
      return Array.prototype.slice.call(s.querySelectorAll('[data-step]')).sort(function (a, b) {
        return (parseFloat(a.getAttribute('data-step')) || 0) - (parseFloat(b.getAttribute('data-step')) || 0);
      });
    });
    deck.stepAt = deck.slides.map(function () { return 0; });
    deck.visited = deck.slides.map(function () { return false; });
    viewport.appendChild(stage);
    main.appendChild(viewport);
    deck.stage = stage;
    if (main.getAttribute('data-sky') !== 'plain') buildSky(main.getAttribute('data-seed') || 'sketchy', main.getAttribute('data-sky') || 'stars');

    if (!mode.print && !mode.clean) buildHud();
    if (S) S.mount(doc);
    fit();
    global.addEventListener('resize', fit);
    bindInput();

    var start = startIndex();
    if (mode.print || mode.still) {
      deck.steps.forEach(function (list, i) { list.forEach(function (el) { el.classList.remove('is-hidden'); }); deck.stepAt[i] = list.length; });
      settleCounters(doc);
    } else {
      deck.steps.forEach(function (list) { list.forEach(function (el) { el.classList.add('is-hidden'); }); });
    }
    if (mode.overview) toggleOverview(true);
    go(start, { instant: true });
    var fontsReady = doc.fonts && doc.fonts.ready ? doc.fonts.ready : Promise.resolve();
    fontsReady.then(function () {
      if (S) S.mount(doc);
      global.requestAnimationFrame(function () { global.requestAnimationFrame(function () { readyResolve(deck); emit('ready', { count: deck.count }); }); });
    });
    if (mode.autoplay) deck.ready.then(function () { schedule(deck.index); });
    return deck;
  }

  /* The sky of the sketchbook: coloured-pencil specks and two soft smudges
     of nebula, seeded by the deck, fixed to the paper (it does not turn
     with the pages). data-sky="plain" leaves the paper empty. */
  function buildSky(seed, kind) {
    if (!S) return;
    var NS = 'http://www.w3.org/2000/svg';
    var svg = doc.createElementNS(NS, 'svg');
    svg.setAttribute('class', 'sk-sky');
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.setAttribute('preserveAspectRatio', 'xMidYMid slice');
    svg.setAttribute('aria-hidden', 'true');
    var r = S.rng(seed + ':sky'), C = S.tokens();
    var defs = doc.createElementNS(NS, 'defs');
    svg.appendChild(defs);
    var cols = [C.red, C.blue, C.yellow, C.violet];
    var puffs = kind === 'dust' ? 0 : 2;
    for (var i = 0; i < puffs; i++) {
      var id = 'sk-neb-' + i, g = doc.createElementNS(NS, 'radialGradient');
      g.setAttribute('id', id);
      g.innerHTML = '<stop offset="0" stop-color="' + cols[Math.floor(r() * cols.length)] + '" stop-opacity=".34"/><stop offset=".55" stop-color="' + cols[Math.floor(r() * cols.length)] + '" stop-opacity=".12"/><stop offset="1" stop-color="' + C.paper + '" stop-opacity="0"/>';
      defs.appendChild(g);
      var e = doc.createElementNS(NS, 'ellipse');
      var edge = i % 2 === 0;
      e.setAttribute('cx', edge ? 120 + r() * 260 : W - 120 - r() * 260);
      e.setAttribute('cy', 150 + r() * (H - 300));
      e.setAttribute('rx', 160 + r() * 140); e.setAttribute('ry', 110 + r() * 90);
      e.setAttribute('fill', 'url(#' + id + ')');
      svg.appendChild(e);
    }
    S.specks(svg, W, H, { seed: seed + ':stars', count: kind === 'dust' ? 60 : 150, opacity: 0.85 });
    deck.el.insertBefore(svg, deck.el.firstChild);
    // in print, every page carries its own sky
    if (mode.print) deck.slides.forEach(function (sl) { var c = svg.cloneNode(true); c.style.zIndex = '0'; sl.insertBefore(c, sl.firstChild); });
  }

  function startIndex() {
    var n = parseInt(P.slide, 10);
    if (!n && global.location.hash) n = parseInt(global.location.hash.slice(1), 10);
    return Math.min(Math.max((n || 1) - 1, 0), Math.max(0, deck.count - 1));
  }

  function fit() {
    if (!deck.stage || mode.print) return;
    if (deck.el.classList.contains('is-overview')) { deck.stage.style.transform = ''; return; }
    var vw = global.innerWidth, vh = global.innerHeight;
    var s = Math.min(vw / W, vh / H);
    deck.scale = s;
    deck.stage.style.transform = 'scale(' + s + ') translate(-50%, -50%)';
  }

  /* ------------------------------------------------------------------ *
   * Navigation
   * ------------------------------------------------------------------ */
  function transitionFor(from, to) {
    var leaving = deck.slides[from];
    var t = (leaving && leaving.getAttribute('data-layout') === 'cover' && to > from) ? 'cover'
      : ((deck.slides[to] && deck.slides[to].getAttribute('data-transition')) || deck.transition);
    if (reduced && t !== 'none') t = 'fade';
    return t;
  }

  function go(i, opts) {
    opts = opts || {};
    if (i < 0 || i >= deck.count) { bump(i < 0 ? 1 : -1); return deck; }
    if (i === deck.index && !opts.force) return deck;
    var from = deck.index, back = i < from;
    var leaving = deck.slides[from], entering = deck.slides[i];
    deck.slides.forEach(function (s) { s.classList.remove('in-page', 'in-cover', 'in-slide', 'in-slide-back', 'in-fade'); });
    if (leaving && !opts.instant && !mode.still) {
      var t = transitionFor(from, i);
      var outCls = t === 'none' ? null : 'out-' + (t === 'page' ? (back ? 'page-back' : 'page') : t === 'slide' ? (back ? 'slide-back' : 'slide') : t);
      var inCls = t === 'none' ? null : 'in-' + (t === 'slide' ? (back ? 'slide-back' : 'slide') : t === 'page' || t === 'cover' ? 'page' : t);
      leaving.classList.remove('is-current');
      if (outCls) {
        leaving.classList.add('is-leaving', outCls);
        var done = function () { leaving.classList.remove('is-leaving', outCls); leaving.removeEventListener('animationend', done); };
        leaving.addEventListener('animationend', done);
        global.setTimeout(done, t === 'cover' ? 900 : 760);
      }
      if (inCls) entering.classList.add(inCls);
    } else if (leaving) {
      leaving.classList.remove('is-current', 'is-leaving');
    }
    entering.classList.add('is-current');
    deck.index = i;
    // returning to a slide shows all its steps; arriving fresh hides them
    if (!mode.still) {
      var list = deck.steps[i];
      if (back && !opts.fresh) { list.forEach(function (el) { el.classList.remove('is-hidden'); }); deck.stepAt[i] = list.length; }
      else { list.forEach(function (el) { el.classList.add('is-hidden'); }); deck.stepAt[i] = 0; }
    }
    enter(entering, i, !deck.visited[i] && !opts.instant);
    deck.visited[i] = true;
    if (!mode.print && !mode.overview) {
      try { global.history.replaceState(null, '', '#' + (i + 1)); } catch (e) { /* file:// in some browsers */ }
    }
    updateHud();
    emit('slide', { index: i, from: from, slide: entering, back: back });
    if (mode.autoplay && deck.ready && !opts.instant) schedule(i);
    return deck;
  }

  function next() {
    var list = deck.steps[deck.index] || [];
    if (!mode.still && deck.stepAt[deck.index] < list.length) {
      var el = list[deck.stepAt[deck.index]++];
      el.classList.remove('is-hidden');
      drawIn(el);
      emit('step', { index: deck.index, step: deck.stepAt[deck.index], el: el });
      updateHud();
      return deck;
    }
    return go(deck.index + 1);
  }
  function prev() {
    if (!mode.still && deck.stepAt[deck.index] > 0) {
      var list = deck.steps[deck.index];
      list[--deck.stepAt[deck.index]].classList.add('is-hidden');
      updateHud();
      return deck;
    }
    return go(deck.index - 1);
  }
  function bump(dir) {
    if (!deck.stage || reduced) return;
    deck.stage.style.setProperty('--bump', (dir * 12) + 'px');
    deck.stage.classList.remove('is-bump');
    void deck.stage.offsetWidth;
    deck.stage.classList.add('is-bump');
  }

  /* What happens when a slide arrives: pictures trace themselves in the
     first time, counters count, stamps slam (CSS), print lines print (CSS). */
  function enter(slide, i, fresh) {
    if (mode.still) return;
    if (fresh) drawIn(slide);
    runCounters(slide);
  }

  function drawIn(root) {
    if (!S || mode.still || (deck.el && deck.el.getAttribute('data-draw') === 'off')) return;
    var svgs = root.matches && root.matches('svg[data-sketch], .sk-chart svg, svg[data-draw]') ? [root]
      : Array.prototype.slice.call(root.querySelectorAll('svg[data-sketch], .sk-chart svg, svg[data-draw]'));
    svgs.forEach(function (svg, k) { S.drawOn(svg, { stagger: 10, duration: 520, delay: 220 + k * 120 }); });
  }

  /* ------------------------------------------------------------------ *
   * Counters: <span data-count>1,240</span> counts up from zero in
   * 900 ms (cubic out), keeping prefix, suffix, separators, decimals and
   * the true minus sign. data-count-from sets another start.
   * ------------------------------------------------------------------ */
  function parseFigure(text) {
    var m = text.match(/^([^0-9−+\-−±]*)([−+\-−±]?)([0-9][0-9,.   ]*)(.*)$/);
    if (!m) return null;
    var raw = m[3].trim(), sep = /,/.test(raw) && /\./.test(raw) ? ',' : (/,\d{3}(\D|$)/.test(raw) ? ',' : (/[   ]/.test(raw) ? ' ' : ''));
    var clean = raw.replace(/[,   ]/g, '');
    var dec = (clean.split('.')[1] || '').length;
    var sign = m[2] === '-' || m[2] === '−' ? -1 : 1;
    return { prefix: m[1], sign: m[2], value: sign * parseFloat(clean), dec: dec, sep: sep, suffix: m[4] };
  }
  function formatFigure(spec, v) {
    var abs = Math.abs(v).toFixed(spec.dec), parts = abs.split('.');
    if (spec.sep) parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, spec.sep);
    var sign = spec.sign ? (v < 0 ? '−' : spec.sign === '±' ? '±' : spec.sign === '+' ? '+' : '') : (v < 0 ? '−' : '');
    return spec.prefix + sign + parts.join('.') + spec.suffix;
  }
  function runCounters(slide) {
    if (S && S.countUp) { slide.querySelectorAll('[data-count]').forEach(S.countUp); return; }
    slide.querySelectorAll('[data-count]').forEach(function (el) {
      if (!el.__skFig) el.__skFig = parseFigure(el.textContent.trim());
      var spec = el.__skFig;
      if (!spec || reduced) return;
      var from = parseFloat(el.getAttribute('data-count-from')) || 0;
      var delay = parseFloat(el.getAttribute('data-count-delay')) || 300;
      var dur = parseFloat(el.getAttribute('data-count-ms')) || 900;
      var t0 = null;
      el.textContent = formatFigure(spec, from);
      el.style.minWidth = el.style.minWidth || (el.offsetWidth ? el.offsetWidth + 'px' : '');
      function tick(now) {
        if (t0 === null) t0 = now + delay;
        var p = Math.min(1, Math.max(0, (now - t0) / dur));
        var e = 1 - Math.pow(1 - p, 3);
        el.textContent = formatFigure(spec, from + (spec.value - from) * e);
        if (p < 1) global.requestAnimationFrame(tick);
      }
      global.requestAnimationFrame(tick);
    });
  }
  function settleCounters(root) {
    root.querySelectorAll('[data-count]').forEach(function (el) { el.__skFig = el.__skFig || parseFigure(el.textContent.trim()); });
  }

  /* ------------------------------------------------------------------ *
   * Autoplay and timeline (used by kiosk mode and the video renderer)
   * ------------------------------------------------------------------ */
  var timer = null, stepTimers = [];
  function durationOf(i) {
    var s = deck.slides[i];
    return parseFloat(s && s.getAttribute('data-duration')) || deck.duration;
  }
  function schedule(i) {
    global.clearTimeout(timer);
    stepTimers.forEach(global.clearTimeout); stepTimers = [];
    var d = durationOf(i) * 1000, list = deck.steps[i] || [];
    list.forEach(function (el, k) {
      stepTimers.push(global.setTimeout(function () { if (deck.index === i) next(); }, (k + 1) * d * 0.6 / (list.length + 1)));
    });
    if (i < deck.count - 1) timer = global.setTimeout(function () { if (deck.index === i) go(i + 1); }, d);
    else timer = global.setTimeout(function () { emit('end', { index: i }); }, d);
  }
  function timeline() {
    var t = 0;
    return deck.slides.map(function (s, i) {
      var d = durationOf(i), list = deck.steps[i] || [];
      var row = { index: i, start: t, duration: d, layout: s.getAttribute('data-layout') || '', title: titleOf(s),
        steps: list.map(function (el, k) { return t + (k + 1) * d * 0.6 / (list.length + 1); }),
        musicSection: s.getAttribute('data-music-section') || null };
      t += d;
      return row;
    });
  }
  function seek(seconds) {
    var rows = timeline(), row = rows[rows.length - 1];
    for (var k = 0; k < rows.length; k++) if (seconds < rows[k].start + rows[k].duration) { row = rows[k]; break; }
    go(row.index, { instant: true, force: true, fresh: true });
    var list = deck.steps[row.index];
    list.forEach(function (el, k) { if (seconds >= row.steps[k]) { el.classList.remove('is-hidden'); deck.stepAt[row.index] = k + 1; } });
    return row;
  }
  function titleOf(s) {
    var h = s.querySelector('h1, h2, .sk-corner-title, .sk-label-title, blockquote');
    return h ? h.textContent.trim().replace(/\s+/g, ' ').slice(0, 80) : '';
  }

  /* ------------------------------------------------------------------ *
   * HUD: the control bar at the bottom, as in the sketchbook
   * ------------------------------------------------------------------ */
  var hud = null, idleTimer = null;
  function sketchButton(label, title, extra) {
    var b = doc.createElement('button');
    b.className = 'sk-btn';
    b.type = 'button';
    b.setAttribute('data-sk', 'button');
    b.setAttribute('data-sk-seed', 'hud-' + label);
    b.title = title; b.setAttribute('aria-label', title);
    b.innerHTML = '<span>' + label + '</span>';
    if (extra) Object.keys(extra).forEach(function (k) { b.setAttribute(k, extra[k]); });
    return b;
  }
  function buildHud() {
    hud = doc.createElement('nav');
    hud.className = 'sk-hud sk-noprint';
    hud.setAttribute('aria-label', 'Slide controls');
    var left = doc.createElement('div'); left.className = 'sk-group';
    var right = doc.createElement('div'); right.className = 'sk-group';
    var prevB = sketchButton('‹', 'Previous (←)'), nextB = sketchButton('›', 'Next (→ or space)');
    var label = doc.createElement('span'); label.className = 'sk-page-label'; label.setAttribute('aria-live', 'polite');
    prevB.addEventListener('click', function () { prev(); });
    nextB.addEventListener('click', function () { next(); });
    left.appendChild(prevB); left.appendChild(label); left.appendChild(nextB);
    var notesB = sketchButton('notes', 'Speaker notes (p)');
    notesB.addEventListener('click', function () { togglePresenter(); });
    var overB = sketchButton('overview', 'All slides (o)');
    overB.addEventListener('click', function () { toggleOverview(); });
    right.appendChild(notesB);
    if (global.SketchySound) {
      var soundB = sketchButton('muted', 'Sound on or off (s)', { 'data-sk-sound-toggle': '' });
      soundB.querySelector('span').setAttribute('data-sk-sound-label', '');
      soundB.addEventListener('click', function () { global.setTimeout(maybeMusic, 0); });
      right.appendChild(soundB);
    }
    right.appendChild(overB);
    var fsB = sketchButton('⛶', 'Full screen (f)');
    fsB.addEventListener('click', toggleFullscreen);
    right.appendChild(fsB);
    hud.appendChild(left); hud.appendChild(right);
    doc.body.appendChild(hud);
    hud.__label = label;
    var pres = doc.createElement('aside');
    pres.className = 'sk-presenter sk-sheet sk-noprint';
    pres.setAttribute('data-sk', 'sheet');
    pres.innerHTML = '<div class="sk-presenter-meta"><span class="sk-presenter-clock">0:00</span><span class="sk-presenter-next"></span></div><div class="sk-presenter-notes"></div>';
    doc.body.appendChild(pres);
    hud.__pres = pres;
    if (mode.presenter) deck.el.classList.add('is-presenting');
    var started = Date.now();
    global.setInterval(function () {
      var s = Math.floor((Date.now() - started) / 1000);
      var c = pres.querySelector('.sk-presenter-clock'); if (c) c.textContent = Math.floor(s / 60) + ':' + ('0' + s % 60).slice(-2);
    }, 1000);
    var wake = function () {
      deck.el.classList.remove('is-idle');
      global.clearTimeout(idleTimer);
      idleTimer = global.setTimeout(function () { deck.el.classList.add('is-idle'); }, 2600);
    };
    ['mousemove', 'pointerdown', 'keydown', 'touchstart'].forEach(function (e) { global.addEventListener(e, wake, { passive: true }); });
    wake();
  }
  function updateHud() {
    if (!hud) return;
    var steps = deck.steps[deck.index] || [];
    hud.__label.textContent = 'p. ' + (deck.index + 1) + ' of ' + deck.count + (steps.length && deck.stepAt[deck.index] < steps.length ? ' ·' : '');
    var s = deck.slides[deck.index];
    var notes = s.getAttribute('data-notes') || (s.querySelector('.sk-notes-speaker') ? s.querySelector('.sk-notes-speaker').textContent.trim() : '');
    hud.__pres.querySelector('.sk-presenter-notes').textContent = notes || 'No notes on this page.';
    var nx = deck.slides[deck.index + 1];
    hud.__pres.querySelector('.sk-presenter-next').textContent = nx ? 'next: ' + (titleOf(nx) || 'p. ' + (deck.index + 2)) : 'last page';
  }
  function togglePresenter() { if (deck.el) deck.el.classList.toggle('is-presenting'); }
  function toggleOverview(force) {
    var on = deck.el.classList.toggle('is-overview', force);
    fit();
    if (on) {
      var cur = deck.slides[deck.index];
      if (cur) global.setTimeout(function () { cur.scrollIntoView({ block: 'center' }); }, 30);
    }
    return on;
  }
  function toggleFullscreen() {
    try {
      if (doc.fullscreenElement) doc.exitFullscreen();
      else doc.documentElement.requestFullscreen();
    } catch (e) { /* not allowed here */ }
  }
  function maybeMusic() {
    var snd = global.SketchySound;
    if (!snd || !deck.music || deck.music === 'none') return;
    if (snd.isOn && snd.music && !snd.music.playing) snd.music.start({ mood: deck.music, seed: deck.el.getAttribute('data-seed') || 'sketchy' });
  }

  /* ------------------------------------------------------------------ *
   * Input: keys, clicks, swipes
   * ------------------------------------------------------------------ */
  function bindInput() {
    doc.addEventListener('keydown', function (e) {
      if (e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey) return;
      var tag = (e.target && e.target.tagName) || '';
      if (/INPUT|TEXTAREA|SELECT/.test(tag) || (e.target && e.target.isContentEditable)) return;
      var k = e.key;
      if (deck.el.classList.contains('is-overview')) {
        if (k === 'Escape' || k === 'o' || k === 'Enter') { toggleOverview(false); e.preventDefault(); }
        return;
      }
      if (k === 'ArrowRight' || k === 'PageDown' || k === ' ' || k === 'ArrowDown') { next(); e.preventDefault(); }
      else if (k === 'ArrowLeft' || k === 'PageUp' || k === 'ArrowUp' || k === 'Backspace') { prev(); e.preventDefault(); }
      else if (k === 'Home') { go(0); e.preventDefault(); }
      else if (k === 'End') { go(deck.count - 1); e.preventDefault(); }
      else if (k === 'o') { toggleOverview(); }
      else if (k === 'f') { toggleFullscreen(); }
      else if (k === 'p') { togglePresenter(); }
      else if (k === 's' && global.SketchySound) { global.SketchySound.toggle(); global.setTimeout(maybeMusic, 0); }
    });
    deck.el.addEventListener('click', function (e) {
      var nx = !deck.el.classList.contains('is-overview') && e.target.closest('.sk-slide .sk-door, [data-next]');
      if (nx) { e.preventDefault(); next(); return; }
      if (deck.el.classList.contains('is-overview')) {
        var s = e.target.closest('.sk-slide');
        if (s) { toggleOverview(false); go(deck.slides.indexOf(s), { instant: true }); }
      }
    });
    var x0 = null, y0 = null;
    deck.el.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') { x0 = e.clientX; y0 = e.clientY; } }, { passive: true });
    deck.el.addEventListener('pointerup', function (e) {
      if (x0 === null) return;
      var dx = e.clientX - x0, dy = e.clientY - y0;
      x0 = null;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.4) { if (dx < 0) next(); else prev(); }
    }, { passive: true });
    doc.addEventListener('sk:slide', function () { maybeMusic(); });
  }

  var SketchyDeck = {
    mount: mount, go: function (i, o) { return go(i, o); }, next: next, prev: prev,
    on: on, timeline: timeline, seek: seek, fit: fit,
    overview: toggleOverview, presenter: togglePresenter,
    parseFigure: parseFigure, formatFigure: formatFigure,
    get ready() { return deck.ready; },
    get count() { return deck.count; },
    get index() { return deck.index; },
    get slides() { return deck.slides; },
    get mode() { return mode; }
  };
  global.SketchyDeck = SketchyDeck;
})(typeof window !== 'undefined' ? window : this);
