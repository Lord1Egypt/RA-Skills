/*!
 * sketchy-sound.js: procedural sound effects and generative music
 * No audio files. Every sound is built from oscillators and seeded noise. The same
 * seed plays the same notes live and gives the same samples in an offline render.
 * MIT License. https://github.com/OthmanAdi/sketchy
 *
 * Load order: after sketchy.js (optional), before or after sketchy-deck.js.
 * Sound is off until the viewer turns it on. Music never starts by itself.
 *
 * Layout of this file:
 *   1. random numbers, music theory, mood and section tables
 *   2. master chain (one function that works on any BaseAudioContext)
 *   3. voice primitives and the sound effects
 *   4. the generative music (phrases are generated as data, then scheduled)
 *   5. offline rendering and WAV encoding
 *   6. live state: enable, unlock, persistence, events, toggles
 */
(function (global) {
  'use strict';

  var doc = global.document;
  var STORE_KEY = 'sketchy:sound';

  /* Levels are linear gains. The master is quiet on purpose: the viewer sets the
     loudness with their own volume control, and the video script normalizes later. */
  var MASTER = 0.15;
  var SFX_LEVEL = 2.0;       // effects sit a little above the music bed
  var CEILING = 0.84;        // -1.5 dBFS: the offline safety trim never lets a render go above this
  var REVERB_SECONDS = 4.5;
  var REVERB_SEED = 4217;

  /* ------------------------------------------------------------------ *
   * 1. Randomness, theory, tables
   * ------------------------------------------------------------------ */
  function hash(str) {
    var h = 2166136261;
    str = String(str);
    for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
    return (h >>> 0) || 1;
  }
  // mulberry32: one small seeded stream. Every consumer gets its own, so adding a
  // sound effect never changes the music and the other way round.
  function mulberry(seed) {
    var a = (typeof seed === 'number' ? seed : hash(seed)) >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function clamp(x, a, b) { return x < a ? a : (x > b ? b : x); }
  function pick(r, list) { return list[Math.floor(r() * list.length)]; }
  function weighted(r, w) {
    var s = 0, i;
    for (i = 0; i < w.length; i++) s += w[i];
    var x = r() * s;
    for (i = 0; i < w.length; i++) { x -= w[i]; if (x <= 0) return i; }
    return w.length - 1;
  }

  var MODES = {
    aeolian: [0, 2, 3, 5, 7, 8, 10],
    dorian: [0, 2, 3, 5, 7, 9, 10],
    ionian: [0, 2, 4, 5, 7, 9, 11]
  };
  var KEY_NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'];
  var NOTE_PC = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };

  function degMidi(tonic, scale, deg) {
    var n = scale.length, oct = Math.floor(deg / n);
    return tonic + 12 * oct + scale[deg - oct * n];
  }
  function midiHz(m) { return 440 * Math.pow(2, (m - 69) / 12); }
  // highest scale degree whose pitch is at or below the given MIDI note
  function midiDeg(tonic, scale, midi) {
    var d = Math.floor((midi - tonic) / 12 * scale.length);
    while (degMidi(tonic, scale, d + 1) <= midi) d++;
    while (degMidi(tonic, scale, d) > midi) d--;
    return d;
  }
  function foldInto(midi, lo, hi) {
    while (midi < lo) midi += 12;
    while (midi > hi) midi -= 12;
    return midi;
  }
  function keyToTonic(k) {
    var pc;
    if (typeof k === 'number') pc = k;
    else {
      var s = String(k).trim(), L = s.charAt(0).toUpperCase();
      pc = NOTE_PC[L];
      if (pc == null) return null;
      var acc = s.charAt(1);
      if (acc === '#') pc += 1; else if (acc === 'b' || acc === 'B') pc -= 1;
    }
    return 45 + ((((pc - 45) % 12) + 12) % 12);   // tonic lives between A2 and G#3
  }

  /* Chord transitions over scale degrees 0..6. Rows are "from", columns "to".
     The masks switch off the one diatonic triad that sounds wrong as a pad
     (the diminished one) for each mode. */
  var MARKOV_MINOR = [
    /* i   ii   III  iv   v    VI   VII */
    [0.04, 0.08, 0.16, 0.24, 0.12, 0.22, 0.14],
    [0.15, 0.00, 0.10, 0.20, 0.35, 0.00, 0.20],
    [0.18, 0.05, 0.00, 0.22, 0.08, 0.30, 0.17],
    [0.26, 0.08, 0.12, 0.00, 0.16, 0.12, 0.26],
    [0.40, 0.02, 0.08, 0.10, 0.00, 0.24, 0.16],
    [0.14, 0.04, 0.16, 0.20, 0.10, 0.00, 0.36],
    [0.38, 0.03, 0.30, 0.08, 0.05, 0.16, 0.00]
  ];
  var MARKOV_MAJOR = [
    /* I   ii   iii  IV   V    vi   vii */
    [0.02, 0.10, 0.08, 0.30, 0.20, 0.30, 0],
    [0.10, 0.00, 0.05, 0.15, 0.55, 0.15, 0],
    [0.05, 0.10, 0.00, 0.35, 0.10, 0.40, 0],
    [0.30, 0.15, 0.03, 0.00, 0.35, 0.17, 0],
    [0.50, 0.03, 0.07, 0.15, 0.00, 0.25, 0],
    [0.08, 0.25, 0.07, 0.35, 0.25, 0.00, 0],
    [0.50, 0.00, 0.00, 0.00, 0.50, 0.00, 0]
  ];
  var MASKS = {
    aeolian: [1, 0, 1, 1, 1, 1, 1],
    dorian: [1, 1, 1, 1, 1, 0, 1],
    ionian: [1, 1, 1, 1, 1, 1, 0]
  };
  // The last chord of a phrase leans towards a chord that wants to resolve to the tonic.
  var END_BIAS_MINOR = [1, 1, 1, 2, 3, 1, 3];
  var END_BIAS_MAJOR = [1, 1, 1, 2.5, 3.5, 1, 1];

  function markov(r, table, mask, from, bias) {
    var row = table[from], w = [], i;
    for (i = 0; i < 7; i++) w.push(row[i] * mask[i] * (bias ? bias[i] : 1));
    return weighted(r, w);
  }

  /* Moods. `level` is the base gain of each layer before the section table is
     applied. `dens` is the long-form density curve: two slow sines whose periods
     (in bars) do not divide each other, so the density never repeats exactly. */
  var MOODS = {
    sketchbook: {
      mode: 'aeolian', bpm: [88, 98], bpc: [2, 2, 4], phrase: [4, 8, 8], repeat: 0.4, rest: 0.18,
      arp: { inst: 'musicbox', range: [69, 93], sub: 2, ghost: 0.35, decay: 0.8, peak: 0.17 },
      lead: { inst: 'celesta', range: [60, 81], decay: 2.2, peak: 0.16, p: 0.6 },
      bass: { pats: [[0], [0, 10], [0, 6, 10], [0, 8]], wave: 'sawtooth', peak: 0.3, long: false },
      hatSteps: [2, 6, 10, 14], hatGhost: true, kickSteps: [0, 8],
      level: { pad: 0.55, drone: 0.14, wind: 0.5, arp: 0.8, lead: 0.55, bass: 0.34, hat: 0.5, kick: 0.4 },
      padCut: 1000, pump: 1, fb: 0.42, bassFloor: 0, trim: 1.44,
      dens: { base: 0.72, a1: 0.2, p1: 24, a2: 0.12, p2: 11 }
    },
    ledger: {
      mode: 'dorian', bpm: [64, 72], bpc: [2, 4], phrase: [4, 8, 8], repeat: 0.5, rest: 0.25,
      arp: { inst: 'pluck', range: [60, 84], sub: 4, ghost: 0.25, decay: 1.2, peak: 0.14 },
      lead: { inst: 'bell', ratio: 3.5, range: [62, 86], decay: 4.2, peak: 0.15, p: 0.75 },
      bass: { pats: [[0], [0, 8], [0, 10]], wave: 'triangle', peak: 0.36, long: true },
      hatSteps: [4, 12], hatGhost: false, kickSteps: [0, 8],
      level: { pad: 0.6, drone: 0.2, wind: 0.6, arp: 0.5, lead: 0.7, bass: 0.5, hat: 0.3, kick: 0.35 },
      padCut: 760, pump: 0.6, fb: 0.45, bassFloor: 0.45, trim: 1.03,
      dens: { base: 0.58, a1: 0.18, p1: 32, a2: 0.1, p2: 13 }
    },
    focus: {
      mode: 'aeolian', bpm: [72, 80], bpc: [4, 4, 2], phrase: [8, 8, 4], repeat: 0.55, rest: 0.3,
      arp: { inst: 'celesta', range: [62, 82], sub: 4, ghost: 0, decay: 1.0, peak: 0.1 },
      lead: { inst: 'bell', ratio: 2, range: [60, 79], decay: 3.0, peak: 0.1, p: 0.35 },
      bass: { pats: [[0], [0, 8]], wave: 'triangle', peak: 0.26, long: true },
      hatSteps: [2, 6, 10, 14], hatGhost: false, kickSteps: [],
      level: { pad: 0.5, drone: 0.14, wind: 0.5, arp: 0.55, lead: 0.45, bass: 0.3, hat: 0.25, kick: 0 },
      padCut: 640, pump: 0.3, fb: 0.4, bassFloor: 0.3, trim: 0.84,
      dens: { base: 0.42, a1: 0.12, p1: 28, a2: 0.08, p2: 15 }
    },
    calm: {
      mode: 'ionian', bpm: [60, 66], bpc: [4, 2, 4], phrase: [4, 8, 8], repeat: 0.5, rest: 0.25,
      arp: { inst: 'celesta', range: [64, 88], sub: 4, ghost: 0.3, decay: 1.6, peak: 0.13 },
      lead: { inst: 'bell', ratio: 2, range: [62, 84], decay: 4.5, peak: 0.12, p: 0.5 },
      bass: { pats: [[0], [0, 8]], wave: 'sine', peak: 0.3, long: true },
      hatSteps: [], hatGhost: false, kickSteps: [],
      level: { pad: 0.65, drone: 0.16, wind: 0.5, arp: 0.5, lead: 0.5, bass: 0.22, hat: 0, kick: 0 },
      padCut: 820, pump: 0, fb: 0.4, bassFloor: 0.5, trim: 0.99,
      dens: { base: 0.5, a1: 0.14, p1: 28, a2: 0.1, p2: 12 }
    }
  };

  /* Sections switch layers in and out. Each value multiplies the mood's base level;
     `cut` scales the pad's filter, `pump` is the pad ducking depth on the beat,
     `dens` scales how many of the generated notes are allowed to sound. */
  var SECTIONS = {
    calm:    { pad: 1.0, drone: 1.0, wind: 1.0, arp: 0.55, lead: 0.55, bass: 0.0,  hat: 0.0,  kick: 0, cut: 0.7,  pump: 0.0,  dens: 0.62 },
    build:   { pad: 1.0, drone: 1.0, wind: 0.8, arp: 0.85, lead: 0.8,  bass: 0.75, hat: 0.55, kick: 0, cut: 0.95, pump: 0.08, dens: 0.9 },
    flight:  { pad: 1.0, drone: 0.9, wind: 0.6, arp: 1.0,  lead: 1.0,  bass: 1.0,  hat: 1.0,  kick: 1, cut: 1.3,  pump: 0.18, dens: 1.15 },
    resolve: { pad: 0.9, drone: 1.0, wind: 1.0, arp: 0.5,  lead: 0.9,  bass: 0.45, hat: 0.0,  kick: 0, cut: 0.8,  pump: 0.0,  dens: 0.7 }
  };

  /* The key a piece plays in comes from its seed alone, so a script can ask for it
     before rendering and so sound effects can be tuned to it. */
  function header(seed, mood, o) {
    o = o || {};
    var M = MOODS[mood] || MOODS.sketchbook;
    var rk = mulberry(hash(seed + '|' + mood + '|key'));
    var tonic = o.key != null ? keyToTonic(o.key) : null;
    var drawn = 45 + Math.floor(rk() * 12);
    var bpmDraw = M.bpm[0] + rk() * (M.bpm[1] - M.bpm[0]);
    if (tonic == null) tonic = drawn;
    return {
      mood: MOODS[mood] ? mood : 'sketchbook', mode: M.mode, scale: MODES[M.mode],
      tonic: tonic, keyName: KEY_NAMES[tonic % 12],
      bpm: o.bpm ? +o.bpm : Math.round(bpmDraw)
    };
  }

  /* ------------------------------------------------------------------ *
   * 2. Buffers and the master chain
   * ------------------------------------------------------------------ */
  function makeNoise(ctx, seconds, seed) {
    var n = Math.floor(ctx.sampleRate * seconds), buf = ctx.createBuffer(1, n, ctx.sampleRate);
    var d = buf.getChannelData(0), r = mulberry(seed);
    for (var i = 0; i < n; i++) d[i] = r() * 2 - 1;
    return buf;
  }

  // Pink noise with the common seven-pole approximation; the last 50 ms are blended
  // into the first 50 ms so the loop seam cannot be heard.
  function makePink(ctx, seconds, seed) {
    var n = Math.floor(ctx.sampleRate * seconds), buf = ctx.createBuffer(1, n, ctx.sampleRate);
    var d = buf.getChannelData(0), r = mulberry(seed);
    var b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0, i;
    for (i = 0; i < n; i++) {
      var w = r() * 2 - 1;
      b0 = 0.99886 * b0 + w * 0.0555179; b1 = 0.99332 * b1 + w * 0.0750759;
      b2 = 0.96900 * b2 + w * 0.1538520; b3 = 0.86650 * b3 + w * 0.3104856;
      b4 = 0.55000 * b4 + w * 0.5329522; b5 = -0.7616 * b5 - w * 0.0168980;
      d[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + w * 0.5362) * 0.11;
      b6 = w * 0.115926;
    }
    var xf = Math.floor(ctx.sampleRate * 0.05);
    for (i = 0; i < xf; i++) {
      var m = i / xf;
      d[n - xf + i] = d[n - xf + i] * (1 - m) + d[i] * m;
    }
    return buf;
  }

  /* A stereo impulse response from seeded noise. Two channels with different noise
     make the tail wide. The tail fades with a cubic curve, loses treble as it ages
     (a one-pole filter that closes with time), and starts with a 4 ms ramp so it
     never clicks. */
  function impulseData(sr, seconds, seed) {
    var n = Math.floor(sr * seconds), r = mulberry(seed), atk = Math.floor(sr * 0.004), out = [];
    for (var ch = 0; ch < 2; ch++) {
      var d = new Float32Array(n), lp = 0;
      for (var i = 0; i < n; i++) {
        var t = i / n, a = 1 - 0.78 * Math.sqrt(t);
        lp += a * ((r() * 2 - 1) - lp);
        var fade = Math.pow(1 - t, 3);
        d[i] = lp * fade * (i < atk ? i / atk : 1);
      }
      out.push(d);
    }
    return out;
  }
  function makeImpulse(ctx, seconds, seed) {
    var data = impulseData(ctx.sampleRate, seconds, seed), buf = ctx.createBuffer(2, data[0].length, ctx.sampleRate);
    buf.copyToChannel(data[0], 0); buf.copyToChannel(data[1], 1);
    return buf;
  }

  /* Why the graph is built from trees and slots.
     A browser sums the connections that reach one node in an order it does not
     promise, and floating-point addition is not associative, so three or more
     sounding inputs on one node make two renders of the same piece differ in the
     last bits. Two inputs are always exact. So every merge point in this file is a
     balanced tree of two-input gains (sumTree), and note voices play through a fixed
     pool of slots (Sink) where only one voice sounds at a time. Silent, finished
     voices that stay connected add exact zeros and change nothing. */
  function sumTree(ctx, nodes) {
    nodes = nodes.slice();
    if (!nodes.length) return null;
    while (nodes.length > 1) {
      var next = [];
      for (var i = 0; i < nodes.length; i += 2) {
        if (i + 1 < nodes.length) {
          var g = ctx.createGain();
          nodes[i].connect(g); nodes[i + 1].connect(g);
          next.push(g);
        } else next.push(nodes[i]);
      }
      nodes = next;
    }
    return nodes[0];
  }

  /* A pool of `size` slots. take(t, until) hands out the first slot that is free at t
     and keeps it until `until`; null means the pool is full and the voice is skipped
     (a polyphony limit, the same in every render). With sends, each slot also feeds a
     reverb tap and an echo tap whose amounts are set when the slot is taken. */
  function Sink(ctx, size, sends) {
    var i, dry = [], wet = [], echo = [];
    this.slots = []; this.free = []; this.sw = sends ? [] : null; this.se = sends ? [] : null;
    for (i = 0; i < size; i++) {
      var s = ctx.createGain();
      this.slots.push(s); this.free.push(0); dry.push(s);
      if (sends) {
        var w = ctx.createGain(), e = ctx.createGain();
        w.gain.value = 0; e.gain.value = 0;
        s.connect(w); s.connect(e);
        this.sw.push(w); this.se.push(e); wet.push(w); echo.push(e);
      }
    }
    this.dry = sumTree(ctx, dry);
    this.wet = sends ? sumTree(ctx, wet) : null;
    this.echo = sends ? sumTree(ctx, echo) : null;
  }
  Sink.prototype.take = function (t, until, wet, echo) {
    for (var i = 0; i < this.slots.length; i++) {
      if (this.free[i] <= t) {
        this.free[i] = until;
        if (this.sw) { this.sw[i].gain.setValueAtTime(wet || 0, t); this.se[i].gain.setValueAtTime(echo || 0, t); }
        return this.slots[i];
      }
    }
    return null;
  };

  /* The master chain. It takes any BaseAudioContext, so the same graph runs live
     and inside an OfflineAudioContext.
       music.dry/wet/echo and sfx.dry/wet/echo  ->  master  ->  compressor  ->  limiter
     `wet` feeds the reverb, `echo` the delay. The sends are tapped after each
     category's level, so turning a category down also silences its tails. */
  function masterChain(ctx) {
    var master = ctx.createGain();
    master.gain.value = 0;
    var comp = ctx.createDynamicsCompressor();
    comp.threshold.value = -14; comp.knee.value = 12; comp.ratio.value = 5;
    comp.attack.value = 0.01; comp.release.value = 0.35;
    var limiter = ctx.createDynamicsCompressor();
    limiter.threshold.value = -3; limiter.knee.value = 0; limiter.ratio.value = 20;
    limiter.attack.value = 0.002; limiter.release.value = 0.12;
    // a gentle high-pass keeps sub-bass rumble out of the mix (small speakers cannot play it anyway)
    var hpf = ctx.createBiquadFilter(); hpf.type = 'highpass'; hpf.frequency.value = 38; hpf.Q.value = 0.5;
    master.connect(hpf); hpf.connect(comp); comp.connect(limiter); limiter.connect(ctx.destination);
    return { master: master, comp: comp, limiter: limiter };
  }

  /* opts.split builds only the part in front of the reverb and the master chain and
     exposes R.premix (music, effects, echo) and R.revSend (the reverb send). The offline
     renderer uses it: see renderOnce for why. */
  function buildMaster(ctx, opts) {
    opts = opts || {};
    var split = !!opts.split;
    var R = {
      ctx: ctx, offline: !!opts.offline, last: {},
      rand: mulberry(hash(String(opts.seed != null ? opts.seed : 'sketchy') + '|sfx')),
      key: null, lastDeg: -1
    };
    var chain = split ? null : masterChain(ctx);

    var revIn = ctx.createGain(); revIn.gain.value = 0.5;
    var revLP = ctx.createBiquadFilter(); revLP.type = 'lowpass'; revLP.frequency.value = 4200; revLP.Q.value = 0.5;
    revIn.connect(revLP);
    var conv = null;
    if (!split) { conv = ctx.createConvolver(); conv.buffer = makeImpulse(ctx, REVERB_SECONDS, REVERB_SEED); revLP.connect(conv); }

    // The echo is a chain of five repeats, each a little quieter and darker. A feedback
    // loop would do the same job, but a loop in the graph makes the browser's processing
    // order matter, and a chain keeps renders identical.
    var dlyIn = ctx.createGain(); dlyIn.gain.value = 0.22;
    var echoTaps = [], prev = dlyIn;
    for (var h = 0; h < 5; h++) {
      var dl = ctx.createDelay(1); dl.delayTime.value = 0.45;
      var dlp = ctx.createBiquadFilter(); dlp.type = 'lowpass'; dlp.frequency.value = 2500;
      if (h > 0) { var hop = ctx.createGain(); hop.gain.value = 0.3; prev.connect(hop); prev = hop; }
      prev.connect(dl); dl.connect(dlp); echoTaps.push(dlp); prev = dlp;
    }
    var echoOut = sumTree(ctx, echoTaps);

    function category() {
      var dry = ctx.createGain(), wet = ctx.createGain(), echo = ctx.createGain();
      wet.connect(revIn); echo.connect(dlyIn);
      return { dry: dry, wet: wet, echo: echo };
    }
    R.music = category(); R.sfx = category();
    [R.sfx.dry, R.sfx.wet, R.sfx.echo].forEach(function (g) { g.gain.value = SFX_LEVEL; });
    // the things that reach the master: music, effects, reverb, echo
    var parts = [R.music.dry, R.sfx.dry];
    if (conv) parts.push(conv);
    parts.push(echoOut);
    var mix = sumTree(ctx, parts);
    if (split) { R.premix = mix; R.revSend = revLP; }
    else { mix.connect(chain.master); R.master = chain.master; R.comp = chain.comp; R.limiter = chain.limiter; }
    // every effect voice plays through this pool, with its own reverb and echo taps
    R.sfxSink = new Sink(ctx, 32, true);
    R.sfxSink.dry.connect(R.sfx.dry); R.sfxSink.wet.connect(R.sfx.wet); R.sfxSink.echo.connect(R.sfx.echo);
    R.noise = makeNoise(ctx, 2, 7);
    R.noiseHat = makeNoise(ctx, 1, 11);
    R.pink = null;
    R.pinkBuffer = function () { return R.pink || (R.pink = makePink(ctx, 6, 99)); };
    R.setLevel = function (which, v, tau) {
      var c = R[which], t = ctx.currentTime;
      [c.dry, c.wet, c.echo].forEach(function (g) { g.gain.setTargetAtTime(v, t, tau || 0.08); });
    };
    R.sfxEnv = { R: R, sink: R.sfxSink, rnd: R.rand };
    return R;
  }

  function masterTo(R, v, sec) {
    var g = R.master.gain, now = R.ctx.currentTime;
    g.cancelScheduledValues(now);
    g.setValueAtTime(g.value, now);
    g.linearRampToValueAtTime(v, now + Math.max(0.01, sec));
  }

  /* ------------------------------------------------------------------ *
   * 3. Voice primitives
   *    E = { R: rig, sink: default Sink for effects, rnd: random stream }
   *    Every primitive takes a slot from a Sink first and returns quietly when the
   *    pool is full. o.t is the start time; o.until is when the slot is free again.
   * ------------------------------------------------------------------ */
  // 0 -> peak (linear, short) -> 0.0001 (exponential). Everything decays to silence.
  function envelope(p, t, peak, atk, dur) {
    peak = Math.max(peak, 0.0002);
    dur = Math.max(dur, atk + 0.01);
    p.setValueAtTime(0, t);
    p.linearRampToValueAtTime(peak, t + atk);
    p.exponentialRampToValueAtTime(0.0001, t + dur);
  }

  function grab(E, o) {
    o.until = o.t + o.dur + 0.06;
    return (o.out || E.sink).take(o.t, o.until, o.wet, o.echo);
  }

  // Connect a finished voice to its slot, with an optional (static or moving) pan, and
  // tidy up when the source ends in a live context.
  function finish(E, node, o, slot, src, extra) {
    var c = E.R.ctx, made = [node], out = node;
    if (c.createStereoPanner && (o.pan || o.panFrom != null)) {
      var p = c.createStereoPanner();
      if (o.panFrom != null) { p.pan.setValueAtTime(o.panFrom, o.t); p.pan.linearRampToValueAtTime(o.panTo, o.t + o.dur); }
      else p.pan.value = clamp(o.pan, -1, 1);
      node.connect(p); out = p; made.push(p);
    }
    out.connect(slot);
    if (!E.R.offline && src) {
      var all = made.concat(extra || []);
      src.onended = function () {
        try { out.disconnect(slot); } catch (err) { /* already gone */ }
        for (var i = 0; i < all.length; i++) { try { all[i].disconnect(); } catch (err2) { /* already gone */ } }
      };
    }
  }

  function noiseSource(E, t, dur, buf) {
    var s = E.R.ctx.createBufferSource();
    s.buffer = buf || E.R.noise; s.loop = true;
    s.start(t, E.rnd() * (s.buffer.duration - 0.4));
    s.stop(t + dur + 0.05);
    return s;
  }

  // One oscillator with an exponential glide. o: t, f0, f1, dur, peak, type, lp, atk, glide, pan, wet, echo, out
  function tone(E, o) {
    var slot = grab(E, o);
    if (!slot) return;
    var c = E.R.ctx, t = o.t, dur = o.dur;
    var osc = c.createOscillator(); osc.type = o.type || 'sine';
    osc.frequency.setValueAtTime(o.f0, t);
    if (o.f1 && o.f1 !== o.f0) osc.frequency.exponentialRampToValueAtTime(o.f1, t + (o.glide || dur * 0.6));
    var g = c.createGain(); envelope(g.gain, t, o.peak, o.atk || 0.008, dur);
    var extra = [];
    if (o.lp) {
      var lp = c.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = o.lp; lp.Q.value = 1;
      osc.connect(lp); lp.connect(g); extra.push(lp);
    } else osc.connect(g);
    finish(E, g, o, slot, osc, extra);
    osc.start(t); osc.stop(t + dur + 0.03);
  }

  // A noise burst through one filter. o: t, type, freq, q, dur, peak, atk, buf, pan, wet, echo, out
  function hit(E, o) {
    var slot = grab(E, o);
    if (!slot) return;
    var c = E.R.ctx, t = o.t;
    var src = noiseSource(E, t, o.dur, o.buf);
    var f = c.createBiquadFilter(); f.type = o.type; f.frequency.value = o.freq; f.Q.value = o.q == null ? 0.8 : o.q;
    var g = c.createGain(); envelope(g.gain, t, o.peak, o.atk || 0.004, o.dur);
    src.connect(f); f.connect(g);
    finish(E, g, o, slot, src, [f]);
  }

  /* A bell: a sine carrier with an FM modulator whose depth collapses over the first
     40 % of the decay, so the attack is glassy and the tail is a pure sine.
     o: t, f, peak, decay, ratio (0 = pure), depth, pan, wet, echo, out */
  function bellVoice(E, o) {
    o.dur = o.decay;
    var slot = grab(E, o);
    if (!slot) return;
    var c = E.R.ctx, t = o.t, f = o.f, extra = [];
    var car = c.createOscillator(); car.type = 'sine'; car.frequency.value = f;
    var g = c.createGain(); envelope(g.gain, t, o.peak, o.atk || 0.01, o.decay);
    if (o.ratio > 0) {
      var mod = c.createOscillator(); mod.type = 'sine'; mod.frequency.value = f * o.ratio;
      var md = c.createGain();
      md.gain.setValueAtTime(f * (o.depth || 1.6), t);
      md.gain.exponentialRampToValueAtTime(f * 0.02, t + o.decay * 0.4);
      mod.connect(md); md.connect(car.frequency);
      mod.start(t); mod.stop(t + o.decay + 0.03);
      extra.push(mod, md);
    }
    car.connect(g);
    finish(E, g, o, slot, car, extra);
    car.start(t); car.stop(t + o.decay + 0.03);
  }

  /* Filtered noise with a path for the filter frequency and for the loudness.
     o: t, dur, type, freqs [[dt, Hz]...] (exponential), q0, q1, amp [[dt, level, 1 = exponential]...],
        am {rate, depth}, hp, panFrom, panTo, pan, wet, echo */
  function sweep(E, o) {
    var slot = grab(E, o);
    if (!slot) return;
    var c = E.R.ctx, t = o.t, i;
    var src = noiseSource(E, t, o.dur);
    var bp = c.createBiquadFilter(); bp.type = o.type || 'bandpass';
    bp.frequency.setValueAtTime(o.freqs[0][1], t);
    for (i = 1; i < o.freqs.length; i++) bp.frequency.exponentialRampToValueAtTime(o.freqs[i][1], t + o.freqs[i][0]);
    bp.Q.setValueAtTime(o.q0 == null ? 0.8 : o.q0, t);
    if (o.q1 != null) bp.Q.linearRampToValueAtTime(o.q1, t + o.dur);
    var g = c.createGain();
    g.gain.setValueAtTime(0, t);
    for (i = 0; i < o.amp.length; i++) {
      var a = o.amp[i], v = Math.max(a[1], 0.0001);
      if (a[2]) g.gain.exponentialRampToValueAtTime(v, t + a[0]); else g.gain.linearRampToValueAtTime(a[1], t + a[0]);
    }
    src.connect(bp);
    var extra = [bp], last = bp;
    if (o.hp) { var hp = c.createBiquadFilter(); hp.type = 'highpass'; hp.frequency.value = o.hp; last.connect(hp); last = hp; extra.push(hp); }
    if (o.am) {
      var am = c.createGain(); am.gain.value = 1 - o.am.depth;
      var lfo = c.createOscillator(); lfo.type = 'sine'; lfo.frequency.setValueAtTime(o.am.rate, t);
      if (o.am.rate2) lfo.frequency.linearRampToValueAtTime(o.am.rate2, t + o.dur);
      var ld = c.createGain(); ld.gain.value = o.am.depth;
      lfo.connect(ld); ld.connect(am.gain);
      last.connect(am); last = am;
      lfo.start(t); lfo.stop(t + o.dur + 0.05);
      extra.push(am, lfo, ld);
    }
    last.connect(g);
    finish(E, g, o, slot, src, extra);
  }

  /* Graphite on paper: noise squeezed into a narrow band and chopped by a fast,
     irregular sawtooth tremolo. The band slides up on one stroke and down on the
     next. No pitch, so it never fights the music.
     o: t, dur, strokes | seg, f0, f1, q, rate, depth, peak, pan */
  function scratch(E, o) {
    var slot = grab(E, o);
    if (!slot) return;
    var c = E.R.ctx, r = E.rnd, t = o.t, dur = o.dur, end = t + dur;
    var src = noiseSource(E, t, dur);
    var hp = c.createBiquadFilter(); hp.type = 'highpass'; hp.frequency.value = 800;
    var bp = c.createBiquadFilter(); bp.type = 'bandpass'; bp.Q.value = o.q;
    var am = c.createGain(); am.gain.value = 0.55;
    var lfo = c.createOscillator(); lfo.type = 'sawtooth';
    var ld = c.createGain(); ld.gain.value = o.depth;
    lfo.connect(ld); ld.connect(am.gain);
    var env = c.createGain();
    src.connect(hp); hp.connect(bp); bp.connect(am); am.connect(env);
    var up = r() < 0.5, a = t;
    env.gain.setValueAtTime(0, t);
    bp.frequency.setValueAtTime(up ? o.f0 : o.f1, t);
    lfo.frequency.setValueAtTime(o.rate, t);
    while (a < end - 0.005) {
      var len = o.seg ? o.seg * (0.7 + r() * 0.6) : dur / o.strokes;
      var b = Math.min(a + len, end), last = b >= end - 0.005;
      var pk = o.peak * (0.7 + r() * 0.6);
      var fa = (up ? o.f0 : o.f1) * (1 + (r() - 0.5) * 0.12), fb = (up ? o.f1 : o.f0) * (1 + (r() - 0.5) * 0.12);
      bp.frequency.setValueAtTime(fa, a);
      bp.frequency.linearRampToValueAtTime(fb, b);
      lfo.frequency.setValueAtTime(o.rate * (0.8 + r() * 0.5), a);
      env.gain.linearRampToValueAtTime(pk, a + Math.min(0.012, (b - a) * 0.3));
      env.gain.linearRampToValueAtTime(pk * 0.55, a + (b - a) * 0.6);
      env.gain.linearRampToValueAtTime(last || r() < 0.25 ? 0 : pk * 0.18, b);
      a = b; up = !up;
    }
    finish(E, env, o, slot, src, [hp, bp, am, lfo, ld]);
    lfo.start(t); lfo.stop(end + 0.05);
  }

  /* ------------------------------------------------------------------ *
   * 3b. Sound effects
   *     fn(E, t, v)  v = { g: gain, p: pitch ratio, pan, o: caller options }
   * ------------------------------------------------------------------ */
  var SFX = {};
  var NAMES = ['pencil', 'scribble', 'page', 'flip', 'stamp', 'tap', 'tick', 'pop', 'whoosh', 'bell', 'chime', 'success', 'fail', 'paper'];
  // Minimum seconds between two sounds of the same name, so a loop that fires every
  // frame still sounds like a person, not a machine gun.
  var LIMITS = { pencil: 0.09, scribble: 0.5, page: 0.3, flip: 0.12, stamp: 0.3, tap: 0.05, tick: 0.04, pop: 0.06,
    whoosh: 0.25, bell: 0.1, chime: 0.25, success: 0.8, fail: 0.6, paper: 0.25 };
  // Sounds that sit in the music's key keep their pitch variation to a few cents.
  var TONAL = { bell: 1, chime: 1, success: 1, fail: 1 };
  // Per-effect trim, measured with offline renders so the quietest recurring sounds sit
  // roughly 10 dB under the stamp, which is the loudest.
  var CAL = { pencil: 2.05, scribble: 1.18, page: 1.38, flip: 1.7, stamp: 0.83, tap: 1.33, tick: 1.6, pop: 1.1,
    whoosh: 1.8, bell: 2.2, chime: 1.9, success: 1.55, fail: 0.67, paper: 2.0 };

  function keyNote(R, deg, lift) {
    var k = R.key;
    return midiHz(degMidi(k.tonic + (lift == null ? 24 : lift), k.scale, deg));
  }
  var BELL_DEGREES = [0, 2, 4, 7, 9, 11, 4];
  function bellDegree(R, v) {
    if (v.o.degree != null) return v.o.degree;
    var d, n = 0;
    do { d = pick(R.rand, BELL_DEGREES); n++; } while (d === R.lastDeg && n < 6);   // never the same bell twice in a row
    R.lastDeg = d;
    return d;
  }

  SFX.pencil = function (E, t, v) {
    var r = E.rnd;
    scratch(E, { t: t, dur: 0.13 + r() * 0.09, strokes: r() < 0.45 ? 2 : 1,
      f0: (2200 + r() * 700) * v.p, f1: (3300 + r() * 900) * v.p, q: 1.2, rate: 22 + r() * 12, depth: 0.45,
      peak: 0.42 * v.g, pan: v.pan != null ? v.pan : (r() - 0.5) * 0.3 });
  };

  SFX.scribble = function (E, t, v) {
    var r = E.rnd, len = clamp(+v.o.length || 1.2, 0.25, 8);
    scratch(E, { t: t, dur: len, seg: 0.11, f0: 2000 * v.p, f1: 3600 * v.p, q: 1.0, rate: 20 + r() * 10, depth: 0.5,
      peak: 0.32 * v.g, pan: v.pan != null ? v.pan : (r() - 0.5) * 0.2 });
  };

  SFX.page = function (E, t, v) {
    var r = E.rnd, p = v.p, g = v.g;
    var j = function (x) { return x * (1 + (r() - 0.5) * 0.16); };
    var n = 0.2 + r() * 0.1, body = 0.02 + n, L = body + 0.2;
    var pan = v.pan != null ? v.pan : 0;
    sweep(E, { t: t, dur: L, freqs: [[0, j(1400) * p], [0.02 + 0.7 * n, j(4200) * p], [L, j(2100) * p]],
      q0: 0.7, amp: [[0.025, 0.2 * g], [body, 0.2 * g], [L, 0.0001, 1]], am: { rate: 9 + r() * 5, depth: 0.22 }, hp: 500, pan: pan });
    var k, ticks = [0.005, 0.04 + r() * 0.015, 0.075 + r() * 0.02];
    for (k = 0; k < ticks.length; k++) hit(E, { t: t + ticks[k], type: 'highpass', freq: 3600, q: 0.7, dur: 0.02, peak: 0.08 * g, pan: pan });
    for (k = 0; k < 4; k++) hit(E, { t: t + 0.1 + r() * (n + 0.12), type: 'highpass', freq: 4000 + r() * 2500, q: 0.7, dur: 0.015 + r() * 0.025, peak: (0.025 + r() * 0.03) * g, pan: pan });
    hit(E, { t: t + L - 0.09, type: 'lowpass', freq: 600, q: 0.7, dur: 0.1, peak: 0.2 * g, pan: pan });
    tone(E, { t: t + L - 0.09, f0: 84 * p, f1: 76 * p, dur: 0.07, peak: 0.12 * g, lp: 300, pan: pan });
  };

  SFX.flip = function (E, t, v) {
    var r = E.rnd, p = v.p, g = v.g, pan = v.pan != null ? v.pan : 0;
    var L = 0.15 + r() * 0.04;
    sweep(E, { t: t, dur: L, freqs: [[0, 2400 * p], [L * 0.5, 5800 * p], [L, 3000 * p]], q0: 1.4,
      amp: [[0.015, 0.16 * g], [L * 0.6, 0.16 * g], [L, 0.0001, 1]], am: { rate: 17 + r() * 6, depth: 0.2 }, hp: 900, pan: pan });
    hit(E, { t: t + L - 0.02, type: 'highpass', freq: 4500, q: 0.7, dur: 0.014, peak: 0.07 * g, pan: pan });
    tone(E, { t: t + L - 0.02, f0: 125 * p, f1: 95 * p, dur: 0.05, peak: 0.07 * g, lp: 300, pan: pan });
  };

  SFX.stamp = function (E, t, v) {
    var p = v.p, g = v.g, pan = v.pan != null ? v.pan : 0;
    tone(E, { t: t, f0: 175 * p, f1: 55 * p, dur: 0.26, peak: 0.6 * g, lp: 520, wet: 0.05, pan: pan });
    hit(E, { t: t, type: 'lowpass', freq: 1900, q: 0.7, dur: 0.055, peak: 0.34 * g, wet: 0.04, pan: pan });
    hit(E, { t: t, type: 'bandpass', freq: 1500 * p, q: 1.8, dur: 0.014, atk: 0.002, peak: 0.28 * g, pan: pan });
  };

  SFX.tap = function (E, t, v) {
    var p = v.p, g = v.g;
    tone(E, { t: t, f0: 560 * p, f1: 380 * p, dur: 0.07, atk: 0.003, peak: 0.16 * g, pan: v.pan });
    hit(E, { t: t, type: 'lowpass', freq: 2500, q: 0.7, dur: 0.012, atk: 0.001, peak: 0.06 * g, pan: v.pan });
  };

  SFX.tick = function (E, t, v) {
    var p = v.p, g = v.g;
    tone(E, { t: t, f0: 1760 * p, dur: 0.03, atk: 0.002, peak: 0.11 * g, pan: v.pan });
    hit(E, { t: t, type: 'bandpass', freq: 3400 * p, q: 3, dur: 0.01, atk: 0.001, peak: 0.13 * g, pan: v.pan });
  };

  SFX.pop = function (E, t, v) {
    var p = v.p, g = v.g;
    tone(E, { t: t, f0: 280 * p, f1: 820 * p, dur: 0.1, atk: 0.003, peak: 0.32 * g, pan: v.pan });
    hit(E, { t: t, type: 'highpass', freq: 2000, q: 0.7, dur: 0.012, atk: 0.001, peak: 0.08 * g, pan: v.pan });
  };

  SFX.whoosh = function (E, t, v) {
    var r = E.rnd, p = v.p, g = v.g, L = 0.75 + r() * 0.25, side = r() < 0.5 ? -1 : 1;
    sweep(E, { t: t, dur: L, freqs: [[0, 220 * p], [L * 0.45, 2600 * p], [L, 500 * p]], q0: 1.0, q1: 2.5,
      amp: [[L * 0.4, 0.26 * g], [L, 0.0001, 1]], wet: 0.25,
      panFrom: v.pan != null ? v.pan : -0.5 * side, panTo: v.pan != null ? v.pan : 0.5 * side });
  };

  SFX.bell = function (E, t, v) {
    var R = E.R, r = E.rnd, f = keyNote(R, bellDegree(R, v)) * v.p;
    bellVoice(E, { t: t, f: f, peak: 0.16 * v.g, decay: 2.8, ratio: 2, pan: v.pan != null ? v.pan : (r() - 0.5) * 0.5, wet: 0.75, echo: 0.3 });
  };

  SFX.chime = function (E, t, v) {
    var R = E.R, r = E.rnd, d = bellDegree(R, v), pan = v.pan != null ? v.pan : (r() - 0.5) * 0.4;
    bellVoice(E, { t: t, f: keyNote(R, d) * v.p, peak: 0.12 * v.g, decay: 2.4, ratio: 2, pan: pan, wet: 0.75, echo: 0.3 });
    bellVoice(E, { t: t + 0.13 + r() * 0.02, f: keyNote(R, d + 4) * v.p, peak: 0.1 * v.g, decay: 2.8, ratio: 2, pan: -pan, wet: 0.75, echo: 0.3 });
  };

  // delivered: a small rising arpeggio of pure bells in the music's key
  SFX.success = function (E, t, v) {
    var R = E.R, r = E.rnd, base = v.o.degree != null ? v.o.degree : 0, steps = [0, 2, 4, 7], i;
    for (i = 0; i < steps.length; i++) {
      var last = i === steps.length - 1;
      bellVoice(E, { t: t + i * 0.15 + r() * 0.01, f: keyNote(R, base + steps[i]) * v.p, peak: (last ? 0.14 : 0.11) * v.g,
        decay: last ? 3.4 : 2.6, ratio: last ? 2 : 0, pan: v.pan != null ? v.pan : (i - 1.5) * 0.15, wet: 0.7, echo: last ? 0.35 : 0 });
    }
  };

  // a soft low sigh that glides down a semitone, never a buzzer
  SFX.fail = function (E, t, v) {
    var R = E.R, f = keyNote(R, 2, 0) * v.p;
    tone(E, { t: t, f0: f, f1: f * 0.944, dur: 1.5, atk: 0.04, peak: 0.34 * v.g, type: 'triangle', lp: 420, wet: 0.3, pan: v.pan });
    tone(E, { t: t, f0: f * 0.5, f1: f * 0.472, dur: 1.2, atk: 0.05, peak: 0.16 * v.g, lp: 300, wet: 0.2, pan: v.pan });
    hit(E, { t: t, type: 'bandpass', freq: 500, q: 0.9, dur: 0.6, atk: 0.06, peak: 0.05 * v.g, pan: v.pan });
  };

  // a sheet sliding on the table: low, soft, with a fine rustle
  SFX.paper = function (E, t, v) {
    var r = E.rnd, p = v.p, g = v.g, L = 0.4 + r() * 0.15;
    sweep(E, { t: t, dur: L, freqs: [[0, 700 * p], [L * 0.5, 1500 * p], [L, 900 * p]], q0: 0.6,
      amp: [[0.08, 0.13 * g], [L * 0.6, 0.13 * g], [L, 0.0001, 1]], am: { rate: 34 + r() * 8, depth: 0.14 }, hp: 250,
      pan: v.pan != null ? v.pan : (r() - 0.5) * 0.4 });
  };

  /* Trigger one effect at absolute time t on a rig. Used by live play() and by cues
     in offline renders, so both paths share the rate limit and the variation. */
  function trigger(R, name, t, o) {
    var fn = SFX[name];
    if (!fn) return false;
    o = o || {};
    var lim = LIMITS[name] || 0.05;
    if (!o.force && R.last[name] != null && t - R.last[name] < lim) return false;
    R.last[name] = t;
    var r = R.rand;
    var v = {
      o: o,
      g: (o.gain != null ? o.gain : 1) * (CAL[name] || 1) * (0.9 + r() * 0.2),
      p: (o.pitch || 1) * (TONAL[name] ? 1 + (r() - 0.5) * 0.006 : 1 + (r() - 0.5) * 0.07),
      pan: o.pan != null ? clamp(+o.pan, -1, 1) : null
    };
    fn(R.sfxEnv, t + r() * 0.008, v);
    return true;
  }

  /* ------------------------------------------------------------------ *
   * 4. Musical voices
   *    All take (E, sink, t, f, vel, dur, pan, peak) and play through a slot of
   *    the layer's sink. A voice that finds the pool full is skipped.
   * ------------------------------------------------------------------ */
  function voiceEnd(E, src, slot, made) {
    if (E.R.offline) return;
    src.onended = function () {
      try { made[0].disconnect(slot); } catch (err) { /* gone */ }
      for (var k = 0; k < made.length; k++) { try { made[k].disconnect(); } catch (err2) { /* gone */ } }
    };
  }
  // Join a voice's last node to its slot, through a panner when it has a pan.
  function toSlot(c, node, pan, slot, made) {
    var out = node;
    if (pan && c.createStereoPanner) {
      var p = c.createStereoPanner(); p.pan.value = clamp(pan, -1, 1); node.connect(p); out = p; made.push(p);
    }
    out.connect(slot);
    made.unshift(out);
    return out;
  }
  function partials(E, sink, t, f, vel, dur, pan, peak, parts, atk) {
    var slot = sink.take(t, t + dur + 0.06);
    if (!slot) return;
    var c = E.R.ctx, cents = (E.rnd() - 0.5) * 10, first = null, gs = [], oscs = [], i;
    for (i = 0; i < parts.length; i++) {
      var fr = f * parts[i][0];
      if (fr > 11000) continue;
      var d = dur * parts[i][2];
      var o = c.createOscillator(); o.frequency.value = fr; o.detune.value = cents;
      var g = c.createGain(); envelope(g.gain, t, peak * vel * parts[i][1], atk, d);
      o.connect(g);
      o.start(t); o.stop(t + d + 0.03);
      gs.push(g); oscs.push(o);
      if (!first) first = o;
    }
    var mix = sumTree(c, gs), made = gs.slice();
    if (mix !== gs[0]) made.push(mix);
    toSlot(c, mix, pan, slot, made);
    voiceEnd(E, first, slot, made);
  }

  var INST = {};
  // tine-like: a clear fundamental with two fast-dying upper partials
  INST.musicbox = function (E, sink, t, f, vel, dur, pan, peak) {
    partials(E, sink, t, f, vel, dur, pan, peak, [[1, 1, 1], [3, 0.14, 0.32], [6.27, 0.06, 0.14]], 0.003);
  };
  INST.celesta = function (E, sink, t, f, vel, dur, pan, peak) {
    partials(E, sink, t, f, vel, dur, pan, peak, [[1, 1, 1], [2, 0.18, 0.5], [4, 0.1, 0.25], [5.4, 0.035, 0.12]], 0.004);
  };
  INST.pluck = function (E, sink, t, f, vel, dur, pan, peak) {
    var slot = sink.take(t, t + dur + 0.06);
    if (!slot) return;
    var c = E.R.ctx;
    var o = c.createOscillator(); o.type = 'triangle'; o.frequency.value = f;
    var lp = c.createBiquadFilter(); lp.type = 'lowpass'; lp.Q.value = 1.2;
    lp.frequency.setValueAtTime(f * 4.5, t); lp.frequency.exponentialRampToValueAtTime(f * 1.3, t + 0.25);
    var g = c.createGain(); envelope(g.gain, t, peak * vel, 0.004, dur);
    o.connect(lp); lp.connect(g);
    var made = [lp, g];
    toSlot(c, g, pan, slot, made);
    o.start(t); o.stop(t + dur + 0.03);
    voiceEnd(E, o, slot, made);
  };
  INST.bell = function (E, sink, t, f, vel, dur, pan, peak, ratio) {
    bellVoice(E, { t: t, f: f, peak: peak * vel, decay: dur, ratio: ratio || 2, depth: ratio > 3 ? 1.1 : 1.6, pan: pan, out: sink });
  };

  function bassNote(E, sink, t, f, vel, dur, wave, peak) {
    var end = t + dur, slot = sink.take(t, end + 0.6);
    if (!slot) return;
    var c = E.R.ctx;
    var o1 = c.createOscillator(); o1.type = 'sine'; o1.frequency.value = f;
    var o2 = c.createOscillator(); o2.type = wave; o2.frequency.value = f;
    var g2 = c.createGain(); g2.gain.value = wave === 'sine' ? 0 : 0.4;
    var lp = c.createBiquadFilter(); lp.type = 'lowpass'; lp.Q.value = 1;
    lp.frequency.setValueAtTime(Math.min(f * 7, 900), t); lp.frequency.exponentialRampToValueAtTime(Math.max(f * 2.4, 140), t + 0.12);
    var g = c.createGain(), pk = peak * vel;
    g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(pk, t + 0.012);
    g.gain.setValueAtTime(pk, end); g.gain.setTargetAtTime(0, end, 0.06);
    o1.connect(lp); o2.connect(g2); g2.connect(lp); lp.connect(g); g.connect(slot);
    o1.start(t); o2.start(t); o1.stop(end + 0.5); o2.stop(end + 0.5);
    voiceEnd(E, o1, slot, [g, lp, g2]);
  }

  /* ------------------------------------------------------------------ *
   * 4b. The piece
   * ------------------------------------------------------------------ */
  var LAYERS = ['pad', 'drone', 'wind', 'arp', 'lead', 'bass', 'hat', 'kick'];
  // voices that can sound at once on each layer; a note beyond that is skipped
  var SINK_SIZE = { pad: 8, arp: 10, lead: 8, bass: 3, hat: 4, kick: 3 };
  // fixed [reverb send, echo send] per layer
  var SENDS = { pad: [0.55, 0], drone: [0.25, 0], wind: [0.2, 0], arp: [0.3, 0], lead: [0.6, 0.25], bass: [0, 0], hat: [0.12, 0], kick: [0.02, 0] };
  var LEAD_TEMPLATES = [[[0, 8]], [[0, 6], [8, 4], [12, 4]], [[4, 4], [8, 8]], [[0, 4], [4, 4], [8, 8]], [[0, 12], [12, 4]], [[6, 2], [8, 8]], []];
  var LEAD_WEIGHTS = [3, 2, 2, 2, 2, 1, 2];

  function isChordTone(deg, c) {
    var k = (((deg - c) % 7) + 7) % 7;
    return k === 0 || k === 2 || k === 4;
  }
  // the nearest chord tone to deg inside [lo, hi], never the pitch `avoid`
  function snap(r, deg, c, lo, hi, avoid) {
    for (var off = 0; off <= 4; off++) {
      var a = deg - off, b = deg + off;
      var okA = a >= lo && a <= hi && a !== avoid && isChordTone(a, c);
      var okB = b >= lo && b <= hi && b !== avoid && isChordTone(b, c);
      if (okA && okB && off > 0) return r() < 0.5 ? a : b;
      if (okA) return a;
      if (okB) return b;
    }
    return clamp(deg, lo, hi);
  }
  // a constrained random walk: steps preferred, leaps rare, drift pulled back to the middle
  function walk(r, cur, prev, lo, hi) {
    var D = [-3, -2, -1, 0, 1, 2, 3], W = [0.04, 0.15, 0.30, 0.03, 0.30, 0.15, 0.04];
    var mid = (lo + hi) / 2, span = Math.max(1, hi - lo), tot = 0, ws = [], i;
    for (i = 0; i < 7; i++) {
      var d = D[i], n = cur + d, w = W[i];
      if (n < lo || n > hi) w = 0;
      else {
        if (d !== 0 && prev !== 0 && (d > 0) === (prev > 0)) w *= 1.3;
        if (Math.abs(prev) >= 3 && d !== 0 && (d > 0) !== (prev > 0)) w *= 2.2;
        w *= Math.max(0.3, 1 + 2 * (Math.abs(cur - mid) - Math.abs(n - mid)) / span);
      }
      ws.push(w); tot += w;
    }
    if (tot <= 0) return clamp(cur, lo, hi);
    var x = r() * tot;
    for (i = 0; i < 7; i++) { x -= ws[i]; if (x <= 0) return cur + D[i]; }
    return cur;
  }

  function Music(R, o) {
    var c = R.ctx, M, i, k;
    this.R = R; this.c = c;
    var H = header(o.seed, o.mood, o);
    this.mood = H.mood; M = this.M = MOODS[H.mood];
    this.seed = String(o.seed);
    this.tonic = H.tonic; this.scale = H.scale; this.bpm = H.bpm; this.keyName = H.keyName; this.mode = H.mode;
    this.stepDur = 60 / this.bpm / 4; this.barDur = this.stepDur * 16;
    var base = this.seed + '|' + this.mood;
    this.rp = mulberry(hash(base + '|piece'));   // phrases: chords, notes
    this.rv = mulberry(hash(base + '|voice'));   // voices: detune, pan, noise offsets
    var rm = mulberry(hash(base + '|mod'));      // slow modulation periods and phases
    this.ph1 = rm(); this.ph2 = rm();
    this.E = { R: R, sink: null, rnd: this.rv };

    var t0 = this.t0 = o.t0;
    this.stepNo = 0; this.phrase = null; this.phraseIdx = 0; this.lastPhrase = null; this.lastDeg = 0;
    this.arpCur = null; this.leadCur = null;
    this.sections = []; this.sectionName = null;
    this.on = {}; this.secDens = 1; this.dens = 0.7; this.thr = 0.7; this.pump = 0;
    this.nextWind = t0;
    this.persist = []; this.pads = [];
    this.stopped = false;

    // everything the piece makes passes through three fade gains, so start, stop and
    // the final fade of a render are one ramp
    this.fade = [c.createGain(), c.createGain(), c.createGain()];
    this.fade[0].connect(R.music.dry); this.fade[1].connect(R.music.wet); this.fade[2].connect(R.music.echo);
    var fadeIn = o.fadeIn == null ? 4 : o.fadeIn;
    for (i = 0; i < 3; i++) {
      this.fade[i].gain.setValueAtTime(0, t0);
      this.fade[i].gain.linearRampToValueAtTime(1, t0 + Math.max(0.05, fadeIn));
    }

    // One bus per layer. Note layers play through a Sink (a pool of slots) into their
    // bus; the buses meet in sumTrees on the way to the fade gains.
    this.bus = {}; this.sink = {};
    var dryIns = [], wetIns = [];
    for (i = 0; i < LAYERS.length; i++) {
      k = LAYERS[i];
      var g = c.createGain(); g.gain.setValueAtTime(0, t0);
      dryIns.push(g);
      if (SENDS[k][0] > 0) { var w = c.createGain(); w.gain.value = SENDS[k][0]; g.connect(w); wetIns.push(w); }
      if (SENDS[k][1] > 0) { var e = c.createGain(); e.gain.value = SENDS[k][1]; g.connect(e); e.connect(this.fade[2]); }
      this.bus[k] = g;
      if (SINK_SIZE[k]) {
        this.sink[k] = new Sink(c, SINK_SIZE[k], false);
        if (k !== 'pad') this.sink[k].dry.connect(g);
      }
    }
    this.pump = 0;

    // pad chain: voices -> lowpass (drifting) -> ducking gain -> bus
    this.padLP = c.createBiquadFilter(); this.padLP.type = 'lowpass'; this.padLP.Q.value = 0.6;
    this.padLP.frequency.setValueAtTime(M.padCut * 0.7, t0);
    this.padPump = c.createGain(); this.padPump.gain.setValueAtTime(1, t0);
    this.sink.pad.dry.connect(this.padLP);
    this.padLP.connect(this.padPump); this.padPump.connect(this.bus.pad);
    var drift = c.createOscillator(); drift.type = 'sine'; drift.frequency.value = 1 / (24 + rm() * 21);
    var driftDepth = c.createGain(); driftDepth.gain.value = M.padCut * 0.22;
    drift.connect(driftDepth); driftDepth.connect(this.padLP.frequency);
    drift.start(t0); this.persist.push(drift);

    // drone: a sine an octave under the tonic plus a quiet triangle on it, breathing slowly
    var droneG = c.createGain(); droneG.gain.value = 0.8;
    var dparts = [[this.tonic, 'sine', 1], [this.tonic - 12, 'sine', 0.3], [this.tonic + 12, 'triangle', 0.25]], dgs = [];
    for (i = 0; i < dparts.length; i++) {
      var dosc = c.createOscillator(); dosc.type = dparts[i][1]; dosc.frequency.value = midiHz(dparts[i][0]);
      var dg = c.createGain(); dg.gain.value = dparts[i][2];
      dosc.connect(dg); dosc.start(t0); dgs.push(dg); this.persist.push(dosc);
    }
    sumTree(c, dgs).connect(droneG); droneG.connect(this.bus.drone);
    var breathe = c.createOscillator(); breathe.type = 'sine'; breathe.frequency.value = 1 / (10 + rm() * 6);
    var breatheDepth = c.createGain(); breatheDepth.gain.value = 0.2;
    breathe.connect(breatheDepth); breatheDepth.connect(droneG.gain);
    breathe.start(t0); this.persist.push(breathe);

    // wind: slow pink noise whose band wanders
    var ws = c.createBufferSource(); ws.buffer = R.pinkBuffer(); ws.loop = true;
    this.windBP = c.createBiquadFilter(); this.windBP.type = 'bandpass'; this.windBP.Q.value = 0.9;
    this.windBP.frequency.setValueAtTime(450, t0);
    ws.connect(this.windBP); this.windBP.connect(this.bus.wind);
    ws.start(t0, 0); this.persist.push(ws);

    // ping-pong echo for the arpeggio: one dotted eighth (three steps) per hop, six hops,
    // each quieter, alternating left and right. Written as a chain, not a feedback loop.
    var ppIn = c.createGain(); ppIn.gain.value = 0.55;
    var ppLP = c.createBiquadFilter(); ppLP.type = 'lowpass'; ppLP.frequency.value = 2400; ppLP.Q.value = 0.5;
    ppIn.connect(ppLP);
    var tapsL = [], tapsR = [], prev = ppLP;
    for (i = 0; i < 6; i++) {
      var dl = c.createDelay(2); dl.delayTime.value = this.stepDur * 3;
      if (i > 0) { var hop = c.createGain(); hop.gain.value = M.fb; prev.connect(hop); prev = hop; }
      prev.connect(dl); prev = dl;
      (i % 2 ? tapsR : tapsL).push(dl);
    }
    var oL = sumTree(c, tapsL), oR = sumTree(c, tapsR);
    if (c.createStereoPanner) {
      var pL = c.createStereoPanner(); pL.pan.value = -0.65; oL.connect(pL); oL = pL;
      var pR = c.createStereoPanner(); pR.pan.value = 0.65; oR.connect(pR); oR = pR;
    }
    this.bus.arp.connect(ppIn);

    sumTree(c, dryIns.concat([oL, oR])).connect(this.fade[0]);
    sumTree(c, wetIns).connect(this.fade[1]);

    // sections, then the first one
    this.queue = [];
    this.queueSection(o.section || 'calm', t0);
  }

  Music.prototype.queueSection = function (name, t) {
    if (!SECTIONS[name]) return;
    this.queue.push({ t: t, name: name });
  };

  // Retarget layer gains with a slow exponential approach: no clicks, no jumps.
  Music.prototype.applySection = function (name, t) {
    var S = SECTIONS[name], M = this.M, L = M.level, k, i;
    this.sectionName = name;
    for (i = 0; i < LAYERS.length; i++) {
      k = LAYERS[i];
      var mult = S[k] == null ? 1 : S[k], target;
      if (k === 'bass') mult = Math.max(mult, M.bassFloor);
      target = (L[k] || 0) * mult * M.trim;
      this.bus[k].gain.setTargetAtTime(target, t, 0.8);
      this.on[k] = target > 0.01;
    }
    this.padLP.frequency.setTargetAtTime(M.padCut * S.cut, t, 2.5);
    this.pump = M.pump > 0 ? S.pump * M.pump : 0;
    this.secDens = S.dens;
  };

  Music.prototype.genPhrase = function (idx) {
    var rp = this.rp, M = this.M, S = this.scale, T = this.tonic, last = this.lastPhrase;
    var bars = pick(rp, M.phrase), bpc = Math.min(pick(rp, M.bpc), bars);
    var cadence = this.sectionName === 'resolve';
    var major = M.mode === 'ionian';
    var table = major ? MARKOV_MAJOR : MARKOV_MINOR, mask = MASKS[M.mode], endBias = major ? END_BIAS_MAJOR : END_BIAS_MINOR;
    var n = Math.max(1, Math.floor(bars / bpc)), degs = [], i, b, s;

    // chords: repeat the last progression sometimes, otherwise walk the Markov chain
    if (last && !cadence && last.bars === bars && last.bpc === bpc && rp() < M.repeat) {
      degs = last.degs.slice();
    } else {
      var prev = this.lastDeg;
      for (i = 0; i < n; i++) {
        var d;
        if (i === 0) d = (idx === 0 || rp() < 0.65) ? 0 : markov(rp, table, mask, prev, null);
        else d = markov(rp, table, mask, prev, i === n - 1 ? endBias : null);
        if (cadence && i === n - 1) d = 0;
        degs.push(d); prev = d;
      }
    }
    var barChord = function (bar) { return degs[Math.min(Math.floor(bar / bpc), n - 1)]; };
    var ph = { bars: bars, bpc: bpc, degs: degs, steps: new Array(bars * 16), chordAt: {}, motif: null };
    for (i = 0; i < n; i++) ph.chordAt[i * bpc] = { deg: degs[i], bars: i === n - 1 ? bars - i * bpc : bpc };
    var put = function (bar, step, layer, ev) {
      var at = bar * 16 + step, slot = ph.steps[at] || (ph.steps[at] = {});
      (slot[layer] || (slot[layer] = [])).push(ev);
    };

    // arpeggio line
    var A = M.arp, aLo = midiDeg(T, S, A.range[0]), aHi = midiDeg(T, S, A.range[1]);
    var cur = this.arpCur != null ? this.arpCur : Math.round((aLo + aHi) / 2 - 2), prevD = 0, prevPrev = null;
    var restBar = (bars >= 4 && rp() < M.rest) ? 1 + Math.floor(rp() * (bars - 1)) : -1;
    var carry = (last && last.motif && rp() < 0.55) ? last.motif : null;
    for (b = 0; b < bars; b++) {
      var c = barChord(b);
      var useMotif = b === 0 ? carry : (b >= 2 && ph.motif && rp() < 0.4 ? ph.motif : null);
      var list = [];
      for (s = 0; s < 16; s++) {
        if (s % A.sub === 0) list.push([s, 0]);
        else if (A.ghost > 0 && s % Math.max(1, A.sub / 2) === 0 && rp() < A.ghost) list.push([s, 1]);
      }
      var deltas = [], kk = 0, pd = null;
      for (var li = 0; li < list.length; li++) {
        s = list[li][0];
        var ghost = list[li][1], strong = (s & 7) === 0, beat = (s & 3) === 0, deg;
        // never a third identical note in a row, and a repeat of the last note only now and then
        var avoid = kk === 0 ? null : (kk >= 2 && pd === prevPrev ? pd : (rp() < 0.65 ? pd : null));
        if (kk === 0) deg = snap(rp, cur, c, aLo, aHi, null);
        else if (useMotif && useMotif[kk] != null) deg = clamp(pd + useMotif[kk], aLo, aHi);
        else deg = walk(rp, pd, prevD, aLo, aHi);
        if (strong) deg = snap(rp, deg, c, aLo, aHi, avoid);
        else if (beat && rp() < 0.55) deg = snap(rp, deg, c, aLo, aHi, avoid);
        if (avoid != null && deg === avoid && !strong) deg = clamp(deg + (rp() < 0.5 ? 1 : -1), aLo, aHi);
        deltas.push(kk === 0 ? 0 : deg - pd);
        var rank = strong ? rp() * 0.15 : beat ? 0.12 + rp() * 0.25 : ghost ? 0.72 + rp() * 0.27 : 0.28 + rp() * 0.45;
        if (b === restBar) rank += 2;
        if (b === bars - 1 && s >= 10) rank += 0.35;   // the phrase breathes out
        var vel = (strong ? 1 : beat ? 0.85 : ghost ? 0.5 : 0.68) * (0.92 + rp() * 0.16);
        put(b, s, 'arp', { deg: deg, vel: vel, rank: rank, jit: (rp() - 0.5) * 0.016, pan: (rp() - 0.5) * 0.5, strong: strong });
        prevD = deg - (pd == null ? deg : pd); prevPrev = pd; pd = deg; kk++;
      }
      cur = pd == null ? cur : pd;
      if (b === 0) ph.motif = deltas;
    }
    this.arpCur = cur;

    // lead: slower notes that land on chord tones, a long note to close the phrase
    var Ld = M.lead, lLo = midiDeg(T, S, Ld.range[0]), lHi = midiDeg(T, S, Ld.range[1]);
    var lc = this.leadCur != null ? this.leadCur : Math.round((lLo + lHi) / 2), lprev = 0;
    for (b = 0; b < bars; b++) {
      var cl = barChord(b), tpl = LEAD_TEMPLATES[weighted(rp, LEAD_WEIGHTS)];
      if (b === 0 && !tpl.length) tpl = LEAD_TEMPLATES[0];
      if (b === bars - 1) tpl = [[0, 12]];
      for (var ti = 0; ti < tpl.length; ti++) {
        var ls = tpl[ti][0], ld = walk(rp, lc, lprev, lLo, lHi);
        if (ti === 0 || b === bars - 1 || rp() < 0.6) ld = snap(rp, ld, cl, lLo, lHi);
        lprev = ld - lc; lc = ld;
        var lr = (ti === 0 ? rp() * 0.3 : 0.2 + rp() * 0.5) + (1 - Ld.p) * 0.4;
        put(b, ls, 'lead', { deg: ld, vel: 0.85 + rp() * 0.25, rank: lr, jit: (rp() - 0.5) * 0.02, pan: (rp() - 0.5) * 0.6 });
      }
    }
    this.leadCur = lc;

    // bass: one pattern per phrase, root on the downbeat, a fifth now and then
    var pat = pick(rp, M.bass.pats);
    for (b = 0; b < bars; b++) {
      var rootDeg = barChord(b);
      for (var bi = 0; bi < pat.length; bi++) {
        var bs = pat[bi], bd = (bs !== 0 && rp() < 0.4) ? rootDeg + 4 : rootDeg;
        var len = (bi + 1 < pat.length ? pat[bi + 1] : 16) - bs;
        put(b, bs, 'bass', { deg: bd, vel: 0.85 + rp() * 0.15, rank: bs === 0 ? rp() * 0.1 : 0.25 + rp() * 0.5, len: len });
      }
    }

    // percussion
    for (b = 0; b < bars; b++) {
      for (i = 0; i < M.hatSteps.length; i++) {
        s = M.hatSteps[i];
        put(b, s, 'hat', { vel: 0.6 + rp() * 0.4, rank: rp() * 0.3, open: s === 14 && rp() < 0.3, jit: (rp() - 0.5) * 0.012 });
      }
      if (M.hatGhost) for (s = 3; s < 16; s += 4) put(b, s, 'hat', { vel: 0.35, rank: 0.7 + rp() * 0.3, open: false, jit: (rp() - 0.5) * 0.012 });
      for (i = 0; i < M.kickSteps.length; i++) put(b, M.kickSteps[i], 'kick', { vel: 1, rank: M.kickSteps[i] === 0 ? 0 : 0.1 });
      if (M.kickSteps.length) {
        put(b, 4, 'kick', { vel: 0.7, rank: 0.55 + rp() * 0.4 });
        put(b, 12, 'kick', { vel: 0.7, rank: 0.55 + rp() * 0.4 });
        if (rp() < 0.3) put(b, 14, 'kick', { vel: 0.6, rank: 0.85 });
      }
    }
    return ph;
  };

  Music.prototype.padChord = function (t, chord) {
    var c = this.c, rv = this.rv, S = this.scale, base = this.tonic + 12, M = this.M;
    var dur = chord.bars * this.barDur, fade = Math.min(1.6, dur * 0.4), tEnd = t + dur;
    var root = chord.deg >= 4 ? chord.deg - 7 : chord.deg;
    var degs = [root, root + 4, root + 9], x = rv();
    if (x < 0.35) degs.push(root + 6); else if (x < 0.6) degs.push(root + 8);
    var pk = 0.2 / Math.sqrt(degs.length);
    for (var i = 0; i < degs.length; i++) {
      var f = midiHz(degMidi(base, S, degs[i])), u = 4 + rv() * 4;
      var slot = this.sink.pad.take(t, tEnd + fade + 0.06);
      if (!slot) continue;
      var g = c.createGain();
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(pk, t + fade);
      g.gain.setValueAtTime(pk, tEnd); g.gain.linearRampToValueAtTime(0, tEnd + fade);
      g.connect(slot);
      for (var j = 0; j < 2; j++) {
        var o = c.createOscillator(); o.type = 'sawtooth'; o.frequency.value = f; o.detune.value = j ? -u : u;
        o.connect(g); o.start(t); o.stop(tEnd + fade + 0.05);
        this.pads.push({ o: o, end: tEnd + fade + 0.05 });
        if (j === 1 && !this.R.offline) o.onended = (function (gg, ss) { return function () { try { gg.disconnect(ss); } catch (err) { /* gone */ } }; })(g, slot);
      }
    }
    // forget voices that have ended so the list stays short in a long session
    if (this.pads.length > 80) { var now = this.R.offline ? -1 : c.currentTime; this.pads = this.pads.filter(function (p) { return p.end > now; }); }
  };

  Music.prototype.barStart = function (t, bar, absBar) {
    var D = this.M.dens;
    var d = D.base + D.a1 * Math.sin(2 * Math.PI * (absBar / D.p1 + this.ph1)) + D.a2 * Math.sin(2 * Math.PI * (absBar / D.p2 + this.ph2));
    this.dens = clamp(d, 0.15, 1);
    var ch = this.phrase.chordAt[bar];
    if (ch) { this.padChord(Math.max(t, this.R.offline ? t : this.c.currentTime), ch); this.lastDeg = ch.deg; }
    if (t >= this.nextWind) {
      var len = 10 + this.rv() * 10;
      this.windBP.frequency.linearRampToValueAtTime(250 + this.rv() * 550, t + len);
      this.nextWind = t + len;
    }
  };

  Music.prototype.runStep = function (t) {
    var q = this.queue;
    while (q.length && q[0].t <= t) { var s0 = q.shift(); this.applySection(s0.name, Math.max(s0.t, this.t0)); }
    var sNo = this.stepNo;
    if (!this.phrase || sNo - this.phrase.step0 >= this.phrase.bars * 16) {
      this.phrase = this.genPhrase(this.phraseIdx++);
      this.phrase.step0 = sNo;
      this.lastPhrase = this.phrase;
    }
    var ph = this.phrase, local = sNo - ph.step0, bar = local >> 4, step = local & 15;
    var late = !this.R.offline && t < this.c.currentTime - 0.02;
    if (step === 0) this.barStart(t, bar, sNo >> 4);
    if (late) return;
    if ((step & 3) === 0 && this.pump > 0.01) {
      this.padPump.gain.setTargetAtTime(1 - this.pump, t, 0.006);
      this.padPump.gain.setTargetAtTime(1, t + 0.04, 0.11);
    }
    var ev = ph.steps[local];
    if (!ev) return;
    var thr = clamp(this.dens * this.secDens, 0, 1.2), M = this.M, E = this.E, S = this.scale, T = this.tonic, i, n, tt;
    if (ev.arp && this.on.arp) {
      for (i = 0; i < ev.arp.length; i++) {
        n = ev.arp[i];
        if (n.rank >= thr) continue;
        INST[M.arp.inst](E, this.sink.arp, Math.max(this.t0, t + n.jit), midiHz(degMidi(T, S, n.deg)), n.vel, M.arp.decay * (0.8 + 0.4 * n.vel), n.pan, M.arp.peak, M.arp.ratio);
      }
    }
    if (ev.lead && this.on.lead) {
      for (i = 0; i < ev.lead.length; i++) {
        n = ev.lead[i];
        if (n.rank >= thr) continue;
        INST[M.lead.inst](E, this.sink.lead, Math.max(this.t0, t + n.jit), midiHz(degMidi(T, S, n.deg)), n.vel, M.lead.decay, n.pan, M.lead.peak, M.lead.ratio);
      }
    }
    if (ev.bass && this.on.bass) {
      for (i = 0; i < ev.bass.length; i++) {
        n = ev.bass[i];
        if (n.rank >= thr) continue;
        var bm = foldInto(degMidi(T - 12, S, n.deg), 43, 57);
        var bd = M.bass.long ? n.len * this.stepDur * 0.92 : Math.min(n.len, 6) * this.stepDur * 0.9;
        bassNote(E, this.sink.bass, t, midiHz(bm), n.vel, bd, M.bass.wave, M.bass.peak);
      }
    }
    if (ev.hat && this.on.hat) {
      for (i = 0; i < ev.hat.length; i++) {
        n = ev.hat[i];
        if (n.rank >= thr) continue;
        hit(E, { t: Math.max(this.t0, t + n.jit), type: 'highpass', freq: 7200, q: 0.7, dur: n.open ? 0.16 : 0.035 + n.vel * 0.03, atk: 0.002,
          peak: 0.07 * n.vel, buf: this.R.noiseHat, out: this.sink.hat });
      }
    }
    if (ev.kick && this.on.kick) {
      for (i = 0; i < ev.kick.length; i++) {
        n = ev.kick[i];
        if (n.rank >= thr) continue;
        tone(E, { t: t, f0: 120, f1: 58, dur: 0.28, glide: 0.08, atk: 0.004, peak: 0.55 * n.vel, lp: 240, out: this.sink.kick });
      }
    }
  };

  // Schedule every step that starts before `until`. The time of step n is t0 + n * stepDur
  // (a product, not a running sum), so the schedule is the same however the calls are chunked.
  Music.prototype.schedule = function (until) {
    for (;;) {
      var t = this.t0 + this.stepNo * this.stepDur;
      if (t >= until) break;
      this.runStep(t);
      this.stepNo++;
    }
  };

  // ramp the whole piece to silence between t and t + len (used for the end of a render)
  Music.prototype.fadeOutAt = function (t, len) {
    for (var i = 0; i < 3; i++) {
      this.fade[i].gain.setValueAtTime(1, t);
      this.fade[i].gain.linearRampToValueAtTime(0, t + len);
    }
  };

  Music.prototype.info = function () {
    return { mood: this.mood, seed: this.seed, key: this.keyName, mode: this.mode, bpm: this.bpm, section: this.sectionName, tonic: this.tonic };
  };

  /* ------------------------------------------------------------------ *
   * 5. Offline rendering and WAV
   * ------------------------------------------------------------------ */
  function peakOf(buf) {
    var pk = 0;
    for (var ch = 0; ch < buf.numberOfChannels; ch++) {
      var d = buf.getChannelData(ch);
      for (var i = 0; i < d.length; i++) { var a = d[i] < 0 ? -d[i] : d[i]; if (a > pk) pk = a; }
    }
    return pk;
  }

  /* Offline reverb. A browser's ConvolverNode did not give the same samples twice for
     long renders (its late partitions are not deterministic), so an offline render
     convolves the reverb send itself, with an FFT in plain JavaScript, which does. It
     uses the same impulse response and the same normalization the ConvolverNode applies
     (unit RMS of the response, a fixed -58 dB calibration, scaled by sample rate), so
     the live and offline reverbs have the same level. Two real signals are transformed
     as one complex signal (left in the real part, right in the imaginary part). */
  function nextPow2(n) { var p = 1; while (p < n) p <<= 1; return p; }
  function makeTwiddles(n) {
    var h = n >> 1, c = new Float64Array(h), s = new Float64Array(h);
    for (var i = 0; i < h; i++) { var a = 2 * Math.PI * i / n; c[i] = Math.cos(a); s[i] = Math.sin(a); }
    return { cos: c, sin: s };
  }
  function fftInPlace(re, im, tw, inverse) {
    var n = re.length, i, j, k, m, t;
    for (i = 1, j = 0; i < n; i++) {
      var bit = n >> 1;
      for (; j & bit; bit >>= 1) j ^= bit;
      j ^= bit;
      if (i < j) { t = re[i]; re[i] = re[j]; re[j] = t; t = im[i]; im[i] = im[j]; im[j] = t; }
    }
    for (var len = 2; len <= n; len <<= 1) {
      var half = len >> 1, step = n / len;
      for (i = 0; i < n; i += len) {
        for (k = 0, m = 0; k < half; k++, m += step) {
          var wr = tw.cos[m], wi = inverse ? tw.sin[m] : -tw.sin[m];
          var x = i + k, y = x + half;
          var tr = re[y] * wr - im[y] * wi, ti = re[y] * wi + im[y] * wr;
          re[y] = re[x] - tr; im[y] = im[x] - ti; re[x] += tr; im[x] += ti;
        }
      }
    }
    if (inverse) for (i = 0; i < n; i++) { re[i] /= n; im[i] /= n; }
  }
  function convolveReverb(xl, xr, sr) {
    var ir = impulseData(sr, REVERB_SECONDS, REVERB_SEED), irLen = ir[0].length, len = xl.length, i, k;
    var pw = 0;
    for (i = 0; i < irLen; i++) pw += ir[0][i] * ir[0][i] + ir[1][i] * ir[1][i];
    pw = Math.sqrt(pw / (2 * irLen));
    if (!isFinite(pw) || pw < 0.000125) pw = 0.000125;
    var scale = (1 / pw) * Math.pow(10, -58 / 20) * (44100 / sr);
    var N = nextPow2(irLen + 32768), B = N - irLen + 1, tw = makeTwiddles(N);
    var hlr = new Float64Array(N), hli = new Float64Array(N), hrr = new Float64Array(N), hri = new Float64Array(N);
    for (i = 0; i < irLen; i++) { hlr[i] = ir[0][i] * scale; hrr[i] = ir[1][i] * scale; }
    fftInPlace(hlr, hli, tw, false); fftInPlace(hrr, hri, tw, false);
    var accL = new Float64Array(len), accR = new Float64Array(len);
    var zr = new Float64Array(N), zi = new Float64Array(N), yr = new Float64Array(N), yi = new Float64Array(N);
    for (var s0 = 0; s0 < len; s0 += B) {
      var n = Math.min(B, len - s0), any = false;
      zr.fill(0); zi.fill(0);
      for (i = 0; i < n; i++) { zr[i] = xl[s0 + i]; zi[i] = xr[s0 + i]; if (zr[i] !== 0 || zi[i] !== 0) any = true; }
      if (!any) continue;
      fftInPlace(zr, zi, tw, false);
      for (k = 0; k < N; k++) {
        var kk = (N - k) & (N - 1);
        var ar = zr[k], ai = zi[k], br = zr[kk], bi = -zi[kk];
        var xlr = (ar + br) * 0.5, xli = (ai + bi) * 0.5, xrr = (ai - bi) * 0.5, xri = -(ar - br) * 0.5;
        var ylr = xlr * hlr[k] - xli * hli[k], yli = xlr * hli[k] + xli * hlr[k];
        var yrr = xrr * hrr[k] - xri * hri[k], yri = xrr * hri[k] + xri * hrr[k];
        yr[k] = ylr - yri; yi[k] = yli + yrr;
      }
      fftInPlace(yr, yi, tw, true);
      var lim = Math.min(N, len - s0);
      for (i = 0; i < lim; i++) { accL[s0 + i] += yr[i]; accR[s0 + i] += yi[i]; }
    }
    return [accL, accR];
  }

  function runOffline(ctx) {
    return new Promise(function (resolve, reject) {
      var p = ctx.startRendering();
      if (p && p.then) p.then(resolve, reject);
      else ctx.oncomplete = function (e) { resolve(e.renderedBuffer); };
    });
  }

  /* renderOnce({ duration, seed, mood, cues, sections, sampleRate, fadeIn, fadeOut, key, bpm, level })
     builds the graph on offline contexts, schedules the whole piece and the cues up
     front, and resolves with the rendered AudioBuffer. Three passes, all deterministic:
       1. the music, effects and echo go to channels 0 and 1, the reverb send to 2 and 3;
       2. the send is convolved with the impulse response in JavaScript and added;
       3. the sum runs through the master gain, high-pass, compressor and limiter. */
  function renderOnce(o) {
    var OAC = global.OfflineAudioContext || global.webkitOfflineAudioContext;
    if (!OAC) return Promise.reject(new Error('OfflineAudioContext is not available in this browser'));
    var sr = o.sampleRate || 48000, dur = Math.max(0.2, +o.duration || 10), len = Math.ceil(dur * sr);
    var seed = o.seed != null ? String(o.seed) : 'sketchy';
    var ctx = new OAC(4, len, sr);
    var R = buildMaster(ctx, { offline: true, seed: seed, split: true });

    var moodName = o.mood === undefined ? 'sketchbook' : o.mood;
    var m = null;
    if (moodName && moodName !== 'none' && MOODS[moodName]) {
      var fadeIn = o.fadeIn == null ? 1.5 : o.fadeIn, fadeOut = o.fadeOut == null ? 2 : o.fadeOut;
      var secs = (o.sections || []).slice().sort(function (a, b) { return a.t - b.t; });
      var first = secs.length && secs[0].t <= 0 ? secs.shift().name : 'calm';
      m = new Music(R, { seed: seed, mood: moodName, key: o.key, bpm: o.bpm, t0: 0, fadeIn: fadeIn, section: first });
      for (var i = 0; i < secs.length; i++) m.queueSection(secs[i].name, Math.max(0, +secs[i].t || 0));
      m.fadeOutAt(Math.max(fadeIn, dur - fadeOut), Math.min(fadeOut, dur));
      R.key = { tonic: m.tonic, scale: m.scale };
      m.schedule(dur);
    } else {
      var H = header(seed, 'sketchbook', o);
      R.key = { tonic: H.tonic, scale: H.scale };
    }
    var cues = (o.cues || []).slice().sort(function (a, b) { return a.t - b.t; });
    for (var k = 0; k < cues.length; k++) {
      if (cues[k].t >= 0 && cues[k].t < dur) trigger(R, cues[k].name, +cues[k].t, cues[k].opts);
    }
    var sp1 = ctx.createChannelSplitter(2), sp2 = ctx.createChannelSplitter(2), mg = ctx.createChannelMerger(4);
    R.premix.connect(sp1); R.revSend.connect(sp2);
    sp1.connect(mg, 0, 0); sp1.connect(mg, 1, 1); sp2.connect(mg, 0, 2); sp2.connect(mg, 1, 3);
    mg.connect(ctx.destination);

    return runOffline(ctx).then(function (stems) {
      var wet = convolveReverb(stems.getChannelData(2), stems.getChannelData(3), sr);
      var ctx3 = new OAC(2, len, sr);
      var mix = ctx3.createBuffer(2, len, sr), a = mix.getChannelData(0), b = mix.getChannelData(1);
      var d0 = stems.getChannelData(0), d1 = stems.getChannelData(1);
      for (var j = 0; j < len; j++) { a[j] = d0[j] + wet[0][j]; b[j] = d1[j] + wet[1][j]; }
      var src = ctx3.createBufferSource(); src.buffer = mix;
      var chain = masterChain(ctx3), level = MASTER * (o.level == null ? 1 : o.level);
      chain.master.gain.setValueAtTime(0, 0);
      chain.master.gain.linearRampToValueAtTime(level, 0.03);
      chain.master.gain.setValueAtTime(level, Math.max(0.04, dur - 0.1));
      chain.master.gain.linearRampToValueAtTime(0, dur);
      src.connect(chain.master); src.start(0);
      return runOffline(ctx3);
    }).then(function (buf) {
      // safety trim: only ever turns a loud render down, never up
      var pk = peakOf(buf);
      if (pk > CEILING) {
        var sc = CEILING / pk;
        for (var ch = 0; ch < buf.numberOfChannels; ch++) { var d = buf.getChannelData(ch); for (var j = 0; j < d.length; j++) d[j] *= sc; }
      }
      return buf;
    });
  }

  // A hash of the sample bits, for comparing two renders.
  function hashBuffer(buf) {
    var h = 2166136261 >>> 0;
    for (var c = 0; c < buf.numberOfChannels; c++) {
      var d = buf.getChannelData(c), u = new Uint32Array(d.buffer, d.byteOffset, d.length);
      for (var i = 0; i < u.length; i++) { h ^= u[i]; h = Math.imul(h, 16777619) >>> 0; }
    }
    return h.toString(16);
  }

  /* renderOffline(options) is renderOnce plus an optional self-check. With check: true
     the render runs twice and, if the two differ (a thread-timing difference in the
     browser, rare in testing), a third time, and the majority wins. */
  function renderOffline(o) {
    o = o || {};
    if (!o.check) return renderOnce(o);
    return renderOnce(o).then(function (a) {
      return renderOnce(o).then(function (b) {
        if (hashBuffer(a) === hashBuffer(b)) return a;
        return renderOnce(o).then(function (c) { return hashBuffer(c) === hashBuffer(a) ? a : c; });
      });
    });
  }

  // 16-bit stereo PCM WAV. A mono buffer is written to both channels.
  function toWav(buf) {
    var n = buf.length, sr = buf.sampleRate;
    var L = buf.getChannelData(0), Rr = buf.numberOfChannels > 1 ? buf.getChannelData(1) : L;
    var bytes = n * 4, ab = new ArrayBuffer(44 + bytes), v = new DataView(ab), i, p = 0;
    function str(s) { for (var k = 0; k < s.length; k++) v.setUint8(p++, s.charCodeAt(k)); }
    str('RIFF'); v.setUint32(p, 36 + bytes, true); p += 4; str('WAVE'); str('fmt '); v.setUint32(p, 16, true); p += 4;
    v.setUint16(p, 1, true); p += 2; v.setUint16(p, 2, true); p += 2; v.setUint32(p, sr, true); p += 4;
    v.setUint32(p, sr * 4, true); p += 4; v.setUint16(p, 4, true); p += 2; v.setUint16(p, 16, true); p += 2;
    str('data'); v.setUint32(p, bytes, true); p += 4;
    for (i = 0; i < n; i++) {
      var a = clamp(L[i], -1, 1), b = clamp(Rr[i], -1, 1);
      v.setInt16(p, a < 0 ? Math.round(a * 32768) : Math.round(a * 32767), true); p += 2;
      v.setInt16(p, b < 0 ? Math.round(b * 32768) : Math.round(b * 32767), true); p += 2;
    }
    return ab;
  }

  /* ------------------------------------------------------------------ *
   * 6. Live state
   * ------------------------------------------------------------------ */
  var state = {
    on: false, ctx: null, R: null, music: null, want: null, section: null,
    userEnabled: false, sleeping: false, armed: false, timer: 0, hideTimer: 0, ready: false
  };
  var UNLOCK_EVENTS = ['pointerdown', 'pointerup', 'touchend', 'click', 'keydown'];

  function readPref() { try { return global.localStorage.getItem(STORE_KEY); } catch (e) { return null; } }
  function writePref(on) { try { global.localStorage.setItem(STORE_KEY, on ? 'on' : 'off'); } catch (e) { /* private mode */ } }
  function reducedMotion() { try { return !!(global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches); } catch (e) { return false; } }
  function AudioCtor() { return global.AudioContext || global.webkitAudioContext; }

  function deckSeed() {
    var n = doc && doc.querySelector('[data-music][data-seed], [data-seed]');
    return (n && n.getAttribute('data-seed')) || 'sketchy';
  }

  function ensureContext() {
    if (state.ctx) return state.ctx;
    var Ctor = AudioCtor(), ctx;
    if (!Ctor) return null;
    try { ctx = new Ctor({ latencyHint: 'playback' }); }
    catch (e) { try { ctx = new Ctor(); } catch (e2) { return null; } }
    state.ctx = ctx;
    // Live effects vary from the deck's seed, never from the clock: the same deck makes
    // the same sequence of small variations on every load.
    state.R = buildMaster(ctx, { seed: deckSeed() });
    var H = header(deckSeed(), 'sketchbook');
    state.R.key = { tonic: H.tonic, scale: H.scale };
    if (ctx.addEventListener) ctx.addEventListener('statechange', onStateChange);
    return ctx;
  }

  function onStateChange() {
    var ctx = state.ctx;
    if (!ctx) return;
    if (ctx.state === 'running') onRunning();
    else if (!state.sleeping && state.on) armUnlock();
  }

  function onRunning() {
    var R = state.R;
    disarmUnlock();
    if (!R || !state.on || state.sleeping) return;
    masterTo(R, MASTER, state.ready ? 0.3 : 1.5);
    state.ready = true;
    syncMusic();
  }

  // Unlock: the first gesture after enable resumes the context and plays one silent
  // sample, which is what iOS needs. The listeners remove themselves once it runs.
  function onGesture() {
    if (!state.on) return;
    var ctx = ensureContext();
    if (!ctx) return;
    if (ctx.state !== 'running' && !state.sleeping) {
      try {
        var b = ctx.createBuffer(1, 1, 22050), s = ctx.createBufferSource();
        s.buffer = b; s.connect(ctx.destination); s.start(0);
      } catch (e) { /* ignore */ }
      resumeContext();
    } else if (ctx.state === 'running') disarmUnlock();
  }
  function armUnlock() {
    if (state.armed || !doc) return;
    state.armed = true;
    for (var i = 0; i < UNLOCK_EVENTS.length; i++) global.addEventListener(UNLOCK_EVENTS[i], onGesture, true);
  }
  function disarmUnlock() {
    if (!state.armed) return;
    state.armed = false;
    for (var i = 0; i < UNLOCK_EVENTS.length; i++) global.removeEventListener(UNLOCK_EVENTS[i], onGesture, true);
  }
  function resumeContext() {
    var ctx = state.ctx;
    if (!ctx) return Promise.resolve();
    var p;
    try { p = ctx.resume(); } catch (e) { p = null; }
    return Promise.resolve(p).then(function () { if (ctx.state === 'running') onRunning(); }, function () { /* blocked until a gesture */ });
  }

  function enable() {
    var was = state.on;
    state.on = true; state.userEnabled = true; state.sleeping = false;
    if (!was) writePref(true);
    var ctx = ensureContext();
    refreshToggles(); announce();
    if (!ctx) return Promise.resolve(false);
    if (ctx.state !== 'running') armUnlock();
    return resumeContext().then(function () { return ctx.state === 'running'; });
  }

  function disable() {
    if (state.on) writePref(false);
    state.on = false;
    stopMusicNow(0.3);
    var R = state.R, ctx = state.ctx;
    if (R) {
      masterTo(R, 0, 0.25);
      setTimeout(function () { if (!state.on && ctx.state === 'running') { try { ctx.suspend(); } catch (e) { /* ignore */ } } }, 350);
    }
    disarmUnlock();
    refreshToggles(); announce();
    return false;
  }

  function toggle() {
    if (state.on) return disable();
    enable();
    return true;
  }

  function announce() {
    if (!doc || !global.CustomEvent) return;
    doc.dispatchEvent(new global.CustomEvent('sk:sound', { detail: { on: state.on } }));
  }

  /* Effects */
  function play(name, opts) {
    var R = state.R;
    if (!state.on || !R || state.ctx.state !== 'running' || state.sleeping) return false;
    return trigger(R, name, R.ctx.currentTime + 0.005, opts);
  }

  /* Music */
  function startMusicNow(want) {
    var R = state.R, ctx = state.ctx;
    stopMusicNow(1.5);
    var m = new Music(R, { seed: want.seed, mood: want.mood, key: want.key, bpm: want.bpm,
      t0: ctx.currentTime + 0.15, fadeIn: want.fadeIn == null ? 4 : want.fadeIn, section: state.section || 'calm' });
    state.music = m;
    R.key = { tonic: m.tonic, scale: m.scale };
    state.timer = setInterval(function () {
      if (ctx.state !== 'running' || state.music !== m) return;
      m.schedule(ctx.currentTime + 0.12);
    }, 25);
    m.timer = state.timer;
  }

  function stopMusicNow(fadeOut) {
    var m = state.music;
    if (!m) return;
    state.music = null;
    if (m.timer) clearInterval(m.timer);
    var ctx = state.ctx, now = ctx.currentTime, len = Math.max(0.05, fadeOut);
    for (var i = 0; i < 3; i++) {
      var g = m.fade[i].gain;
      g.cancelScheduledValues(now); g.setValueAtTime(g.value, now); g.linearRampToValueAtTime(0, now + len);
    }
    setTimeout(function () {
      var k;
      for (k = 0; k < m.persist.length; k++) { try { m.persist[k].stop(); } catch (e) { /* stopped */ } }
      for (k = 0; k < m.pads.length; k++) { try { m.pads[k].o.stop(); } catch (e2) { /* stopped */ } }
      for (k = 0; k < 3; k++) { try { m.fade[k].disconnect(); } catch (e3) { /* gone */ } }
    }, len * 1000 + 250);
  }

  function syncMusic() {
    var ctx = state.ctx;
    if (!state.on || !ctx || ctx.state !== 'running' || state.sleeping) return;
    if (state.want && !state.music) {
      // a remembered "on" plus a deck that declares data-music is not an invitation to
      // start music for someone who asked the browser to reduce motion
      if (state.want.auto && reducedMotion() && !state.userEnabled) return;
      startMusicNow(state.want);
    }
  }

  var music = {
    start: function (o) {
      o = o || {};
      state.want = { mood: MOODS[o.mood] ? o.mood : 'sketchbook', seed: o.seed != null ? String(o.seed) : deckSeed(),
        key: o.key, bpm: o.bpm, fadeIn: o.fadeIn, auto: !!o.auto };
      if (state.music) { stopMusicNow(1.5); }
      syncMusic();
      return state.on;
    },
    stop: function () { state.want = null; stopMusicNow(2); },
    section: function (name) {
      if (!SECTIONS[name]) return false;
      state.section = name;
      if (state.music) state.music.queueSection(name, state.ctx.currentTime);
      return true;
    },
    info: function () { return state.music ? state.music.info() : null; },
    get playing() { return !!state.music; },
    get mood() { return state.music ? state.music.mood : (state.want ? state.want.mood : null); }
  };

  /* Tab visibility: fade out fast and suspend, resume with a slower fade. */
  function onVisibility() {
    var R = state.R, ctx = state.ctx;
    if (!R || !state.on) return;
    if (doc.hidden) {
      masterTo(R, 0, 0.15);
      clearTimeout(state.hideTimer);
      state.hideTimer = setTimeout(function () {
        if (doc.hidden && ctx.state === 'running') { state.sleeping = true; try { ctx.suspend(); } catch (e) { /* ignore */ } }
      }, 200);
    } else {
      clearTimeout(state.hideTimer);
      if (state.sleeping) {
        state.sleeping = false;
        resumeContext();
      }
      if (ctx.state === 'running') masterTo(R, MASTER, 1.2);
    }
  }

  /* Toggle buttons. Clicks are delegated, so toggles added later work too; call
     SketchySound.bind() after adding one to refresh its label. */
  function setLabel(btn, text) {
    var span = btn.querySelector('[data-sk-sound-label]');
    if (span) { if (span.textContent !== text) span.textContent = text; return; }
    // keep the pencil overlay the engine inserts as the first child: touch text nodes only
    for (var i = 0; i < btn.childNodes.length; i++) {
      var n = btn.childNodes[i];
      if (n.nodeType === 3 && n.nodeValue.trim()) { if (n.nodeValue !== text) n.nodeValue = text; return; }
    }
    btn.appendChild(doc.createTextNode(text));
  }
  function refreshToggles() {
    if (!doc) return;
    var list = doc.querySelectorAll('[data-sk-sound-toggle]');
    for (var i = 0; i < list.length; i++) {
      var b = list[i], on = state.on;
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      if (b.classList) b.classList.toggle('is-on', on);
      if (b.tagName !== 'BUTTON' && b.tagName !== 'A' && !b.getAttribute('role')) { b.setAttribute('role', 'button'); if (!b.hasAttribute('tabindex')) b.setAttribute('tabindex', '0'); }
      setLabel(b, on ? (b.getAttribute('data-label-on') || 'sound') : (b.getAttribute('data-label-off') || 'muted'));
    }
  }

  function declaredMusic() {
    var n = doc && doc.querySelector('[data-music]');
    if (!n) return;
    var mood = (n.getAttribute('data-music') || '').trim();
    if (!MOODS[mood]) return;
    state.want = { mood: mood, seed: n.getAttribute('data-seed') || 'sketchy', auto: true };
  }

  function init() {
    if (!doc) return;
    // events from the deck
    doc.addEventListener('sk:slide', function (e) {
      if (!state.on) return;
      var d = e.detail || {}, slide = d.slide, sec = slide && slide.getAttribute && slide.getAttribute('data-music-section');
      if (sec) music.section(sec);
      play('page');
    });
    doc.addEventListener('sk:step', function () { if (state.on) play('pencil'); });
    doc.addEventListener('click', function (e) {
      var n = e.target && e.target.closest ? e.target.closest('[data-sk-sound-toggle]') : null;
      if (n) { e.preventDefault(); toggle(); }
    });
    doc.addEventListener('keydown', function (e) {
      var tg = e.target;
      if (tg && tg.hasAttribute && tg.hasAttribute('data-sk-sound-toggle') && tg.tagName !== 'BUTTON' && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); toggle(); return; }
      if ((e.key !== 's' && e.key !== 'S') || e.metaKey || e.ctrlKey || e.altKey || e.defaultPrevented) return;
      if (tg && (tg.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(tg.tagName))) return;
      if (global.SketchyDeck) return;   // the deck owns its keyboard map and calls toggle() itself
      toggle();
    });
    doc.addEventListener('visibilitychange', onVisibility);
    declaredMusic();
    var pref = readPref();
    if (pref === 'on') { state.on = true; armUnlock(); }
    refreshToggles();
  }

  var SketchySound = {
    version: '0.1.0',
    enable: enable, disable: disable, toggle: toggle,
    get isOn() { return state.on; },
    play: play,
    music: music,
    renderOffline: renderOffline,
    toWav: toWav,
    hashBuffer: hashBuffer,
    bind: refreshToggles,
    /* the key, mode and tempo a seed and mood will play in, without making any sound */
    describe: function (o) {
      o = o || {};
      var H = header(o.seed != null ? String(o.seed) : 'sketchy', o.mood || 'sketchbook', o);
      return { mood: H.mood, key: H.keyName, mode: H.mode, bpm: H.bpm, tonic: H.tonic };
    },
    names: NAMES.slice(),
    moods: Object.keys(MOODS),
    sections: Object.keys(SECTIONS),
    /* for tools that want the graph on their own context */
    buildMaster: buildMaster
  };
  global.SketchySound = SketchySound;

  if (doc) {
    if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', init); else init();
  }
})(typeof window !== 'undefined' ? window : this);
