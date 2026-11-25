/*!
 * sketchy.js — the pencil engine
 * Hand-drawn graphite lines, coloured-pencil hatching, boiling lines, stamps,
 * postmarks and paper for HTML pages, decks, charts and video frames.
 * Zero dependencies. MIT License. https://github.com/OthmanAdi/sketchy
 *
 * Load order: sketchy.css, sketchy.js, then optional sketches.js,
 * sketchy-charts.js, sketchy-sound.js, sketchy-deck.js, then Sketchy.mount().
 *
 * Three rules hold everything together:
 *  1. Everything is seeded. The same seed draws the same wobble on every load,
 *     every device, in the PDF and in the video.
 *  2. Every drawing exists in four variants that swap ten times a second on one
 *     shared clock (the "boil" of hand-drawn animation). Geometry is never
 *     re-randomised per frame. Reduced motion slows the boil to 2 fps.
 *  3. Colour comes only from CSS tokens (--sk-*), so a theme recolours it all.
 */
(function (global) {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';
  var doc = global.document;

  /* ------------------------------------------------------------------ *
   * Seeded randomness
   * ------------------------------------------------------------------ */
  function hash(str) {
    var h = 2166136261;
    str = String(str);
    for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
    return (h >>> 0) || 1;
  }
  function rng(seed) {
    var a = typeof seed === 'number' ? seed >>> 0 : hash(seed);
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function f(n) { return Math.round(n * 100) / 100; }

  /* ------------------------------------------------------------------ *
   * Config and tokens
   * ------------------------------------------------------------------ */
  var reduced = false;
  try { reduced = global.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { /* old engine */ }
  var params = {};
  try { (new URLSearchParams(global.location.search)).forEach(function (v, k) { params[k] = v === '' ? true : v; }); } catch (e) { /* file:// quirks */ }

  var config = {
    variants: 4,            // drawings per object, swapped by the boil clock
    boilFps: 10,            // hand-drawn shimmer; 2 when reduced motion is on
    boil: !('static' in params) && !('print' in params),
    grain: true             // graphite tooth on strokes and fills
  };

  var TOKEN_NAMES = ['paper', 'paper-deep', 'paper-light', 'sheet', 'halo', 'graphite', 'graphite-soft', 'graphite-faint', 'ink',
    'red', 'red-ink', 'red-frame', 'red-soft', 'blue', 'green', 'yellow', 'orange', 'violet', 'rose', 'teal', 'peach',
    'gold', 'figure', 'cream', 'stamp', 'stamp-blue', 'stamp-green', 'tape', 'tape-text', 'shadow'];
  function tokens(el) {
    var cs = global.getComputedStyle(el || doc.documentElement);
    var t = {};
    TOKEN_NAMES.forEach(function (n) { t[n] = cs.getPropertyValue('--sk-' + n).trim(); });
    // sketch-board compatibility names
    t.pencil = t.graphite; t.signal = t.yellow; t.keep = t.green; t.remove = t.red;
    t.plate = t['paper-light']; t.muted = t['graphite-soft'];
    // data series order; red stays reserved for the one thing that matters
    t.pencils = [t.blue, t.green, t.yellow, t.orange, t.violet, t.rose, t.teal].filter(Boolean);
    return t;
  }

  /* ------------------------------------------------------------------ *
   * Geometry: hand-drawn path data
   * ------------------------------------------------------------------ */

  /* A straight stroke: jittered ends, a little overshoot, a bow.
     Long strokes drift in a few smooth segments like a real hand. */
  function handLine(x1, y1, x2, y2, r, rough) {
    var dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy) || 1;
    var ux = dx / len, uy = dy / len, nx = -uy, ny = ux;
    var j = Math.min(len * 0.010, 1.8) * rough;
    var ov = Math.min(len * 0.025, 3.2) * rough;
    var sO = (r() - 0.35) * ov, eO = (r() - 0.35) * ov;
    var sx = x1 - ux * sO + (r() - 0.5) * j * nx, sy = y1 - uy * sO + (r() - 0.5) * j * ny;
    var ex = x2 + ux * eO + (r() - 0.5) * j * nx, ey = y2 + uy * eO + (r() - 0.5) * j * ny;
    if (len < 160) {
      var bow = (r() - 0.5) * Math.min(len * 0.02, 2.8) * rough * 1.3;
      return 'M' + f(sx) + ' ' + f(sy) +
        'C' + f(x1 + dx * 0.33 + nx * bow * (0.7 + r() * 0.6)) + ' ' + f(y1 + dy * 0.33 + ny * bow * (0.7 + r() * 0.6)) +
        ' ' + f(x1 + dx * 0.67 + nx * bow * (0.7 + r() * 0.6)) + ' ' + f(y1 + dy * 0.67 + ny * bow * (0.7 + r() * 0.6)) +
        ' ' + f(ex) + ' ' + f(ey);
    }
    var segs = Math.min(9, Math.ceil(len / 130));
    var pts = [[sx, sy]], drift = 0;
    for (var i = 1; i < segs; i++) {
      drift = drift * 0.75 + (r() - 0.5) * 1.7 * rough;
      var t = i / segs;
      pts.push([x1 + dx * t + nx * drift, y1 + dy * t + ny * drift]);
    }
    pts.push([ex, ey]);
    return smoothPath(pts, false);
  }

  /* Catmull-Rom through points, as cubic Béziers. */
  function smoothPath(pts, closed) {
    if (pts.length < 2) return '';
    var d = 'M' + f(pts[0][0]) + ' ' + f(pts[0][1]);
    var n = pts.length;
    for (var i = 0; i < (closed ? n : n - 1); i++) {
      var p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n], p3 = pts[(i + 2) % n];
      if (!closed) { if (i === 0) p0 = p1; if (i + 2 >= n) p3 = p2; }
      d += 'C' + f(p1[0] + (p2[0] - p0[0]) / 6) + ' ' + f(p1[1] + (p2[1] - p0[1]) / 6) +
        ' ' + f(p2[0] - (p3[0] - p1[0]) / 6) + ' ' + f(p2[1] - (p3[1] - p1[1]) / 6) +
        ' ' + f(p2[0]) + ' ' + f(p2[1]);
    }
    return d;
  }

  /* A circle or ellipse drawn freehand. The radius breathes on the 2nd, 3rd
     and 5th harmonics; the stroke overshoots its own start by 3 to 10 degrees
     and drifts outward a little at the end. Pass 1 is a partial retrace. */
  function handEllipse(cx, cy, rx, ry, r, rough, retrace) {
    var R = (rx + ry) / 2;
    var h = (0.6 + R * 0.015) * rough;
    var harm = [2, 3, 5].map(function (k) { return [k, (h / k) * (0.8 + r() * 0.4), r() * Math.PI * 2]; });
    var start = r() * Math.PI * 2;
    var sweep = retrace ? Math.PI * 2 * (0.2 + r() * 0.35) : Math.PI * 2 + (0.05 + r() * 0.12) * Math.min(1.4, rough + 0.2);
    var drift = (r() < 0.5 ? -1 : 1) * (0.8 + r() * 0.8) * rough;
    var off = retrace ? (r() - 0.5) * 2.2 : 0;
    var per = Math.PI * (rx + ry) * (sweep / (Math.PI * 2));
    var n = Math.max(8, Math.min(72, Math.round(per / 9)));
    var pts = [];
    for (var i = 0; i <= n; i++) {
      var m = i / n, a = start + sweep * m;
      var dr = 0;
      for (var k = 0; k < 3; k++) dr += harm[k][1] * Math.sin(harm[k][0] * a + harm[k][2]);
      dr += retrace ? off * Math.sin(Math.PI * m) : drift * m * m;
      pts.push([cx + Math.cos(a) * (rx + dr * rx / R), cy + Math.sin(a) * (ry + dr * ry / R)]);
    }
    return smoothPath(pts, false);
  }

  function handPoly(points, r, rough, closed) {
    var d = '', n = points.length;
    for (var i = 0; i < (closed ? n : n - 1); i++) {
      var a = points[i], b = points[(i + 1) % n];
      d += handLine(a[0], a[1], b[0], b[1], r, rough);
    }
    return d;
  }

  function handCurve(points, r, rough) {
    var pts = points.map(function (p) { return [p[0] + (r() - 0.5) * 1.2 * rough, p[1] + (r() - 0.5) * 1.2 * rough]; });
    return smoothPath(pts, false);
  }

  /* ------------------------------------------------------------------ *
   * SVG plumbing
   * ------------------------------------------------------------------ */
  function el(tag, attrs, parent) {
    var e = doc.createElementNS(NS, tag);
    if (attrs) for (var k in attrs) if (attrs[k] != null) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  var uid = 0;
  function nextId(p) { uid += 1; return (p || 'sk') + '-' + uid; }

  /* Filters, once per document.
     sk-grain: punches a power-curve speckle out of the drawing (graphite on tooth).
     sk-ink: blotchy rubber-stamp coverage with a slightly eaten edge. */
  var DEFS_HTML =
    '<filter id="sk-grain" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">' +
    '<feTurbulence type="fractalNoise" baseFrequency="1.05" numOctaves="2" seed="99" result="n"/>' +
    '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1.6 0 0 0 -0.42" result="a"/>' +
    '<feComponentTransfer in="a" result="m"><feFuncA type="gamma" amplitude="0.8" exponent="2.2" offset="0"/></feComponentTransfer>' +
    '<feComposite in="SourceGraphic" in2="m" operator="out"/></filter>' +
    '<filter id="sk-ink" x="-15%" y="-15%" width="130%" height="130%" color-interpolation-filters="sRGB">' +
    '<feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="3" seed="3" result="n"/>' +
    '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.4 1.95" result="m"/>' +
    '<feComposite in="SourceGraphic" in2="m" operator="in" result="c"/>' +
    '<feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="1" seed="9" result="w"/>' +
    '<feDisplacementMap in="c" in2="w" scale="1.4" xChannelSelector="R" yChannelSelector="G"/></filter>';
  function ensureDefs() {
    if (doc.getElementById('sk-defs')) return;
    var svg = el('svg', { id: 'sk-defs', width: 0, height: 0, 'aria-hidden': 'true', focusable: 'false' });
    svg.style.cssText = 'position:absolute;width:0;height:0;overflow:hidden;pointer-events:none';
    svg.innerHTML = DEFS_HTML;
    (doc.body || doc.documentElement).appendChild(svg);
  }

  /* ------------------------------------------------------------------ *
   * The pen. One pen draws into one SVG or <g>. Primitives return the <g>.
   * Options: stroke, width, passes (0..3), rough (0..2), opacity, fill,
   * fillStyle ('body' | 'hatch' | 'cross' | 'solid' | 'scribble' | 'none'),
   * gap, angle, fillOpacity, dash, grain, cls.
   * 'body' is the house fill: a 38% wash, hatching at about -41 degrees and a
   * lighter cross-hatch at +95 degrees, the way a coloured pencil fills a planet.
   * ------------------------------------------------------------------ */
  function pen(target, opts) {
    ensureDefs();
    opts = opts || {};
    var seed = opts.seed != null ? (typeof opts.seed === 'number' ? opts.seed : hash(opts.seed))
      : hash((target.getAttribute && (target.getAttribute('data-sketch') || target.id)) || 'sketchy');
    var r = rng(seed);
    var C = opts.tokens || tokens();
    var baseRough = opts.rough != null ? opts.rough : 1;
    var baseWidth = opts.width || 1.5;
    var root = target;
    var labels = opts.labels || null;       // where text goes (outside grain and boil)
    var skipText = !!opts.skipText;         // boil variants 2..4 do not repeat labels
    var grainOn = opts.grain != null ? opts.grain : config.grain;

    function style(o) {
      o = o || {};
      return {
        stroke: o.stroke || opts.stroke || C.graphite || '#4a4a4a',
        width: o.width != null ? o.width : baseWidth,
        passes: o.passes != null ? o.passes : (opts.passes != null ? opts.passes : 2),
        rough: o.rough != null ? o.rough : baseRough,
        opacity: o.opacity != null ? o.opacity : 0.9,
        fill: o.fill, fillStyle: o.fillStyle || (o.fill ? 'body' : 'none'),
        gap: o.gap || 2.3, angle: (o.angle != null ? o.angle : -41) + (r() - 0.5) * 10,
        fillOpacity: o.fillOpacity != null ? o.fillOpacity : 1,
        dash: o.dash, grain: o.grain != null ? o.grain : grainOn, cls: o.cls
      };
    }

    function strokeGroup(s, builder) {
      var g = el('g', { 'class': 'sk-stroke' + (s.cls ? ' ' + s.cls : '') }, root);
      if (s.grain && !opts.grainAtRoot) g.setAttribute('filter', 'url(#sk-grain)');
      for (var p = 0; p < s.passes; p++) {
        var main = p === 0;
        el('path', {
          d: builder(p),
          fill: 'none', stroke: s.stroke,
          'stroke-width': f(main ? s.width : s.width * 0.8),
          'stroke-opacity': f(main ? s.opacity : s.opacity * 0.6),
          'stroke-linecap': 'round', 'stroke-linejoin': 'round',
          'stroke-dasharray': s.dash || null, pathLength: s.dash ? null : 1,
          'class': 'sk-path' + (main ? '' : ' sk-path-2')
        }, g);
      }
      if (s.dash) g.classList.add('sk-plan');
      return g;
    }

    function hatchLines(clip, bbox, angle, gap, weight, colour, alpha, parent) {
      var rad = angle * Math.PI / 180, ca = Math.cos(rad), sa = Math.sin(rad);
      var cx = bbox.x + bbox.w / 2, cy = bbox.y + bbox.h / 2;
      var R = Math.hypot(bbox.w, bbox.h) / 2 + 3;
      var d = '';
      for (var o = -R; o <= R; o += gap * (0.82 + r() * 0.36)) {
        var x1 = cx - ca * R - sa * o, y1 = cy - sa * R + ca * o;
        var x2 = cx + ca * R - sa * o, y2 = cy + sa * R + ca * o;
        var t0 = r() * 0.04, t1 = 1 - r() * 0.04;
        d += 'M' + f(x1 + (x2 - x1) * t0) + ' ' + f(y1 + (y2 - y1) * t0) +
          'L' + f(x1 + (x2 - x1) * t1 + (r() - 0.5) * 0.8) + ' ' + f(y1 + (y2 - y1) * t1 + (r() - 0.5) * 0.8);
      }
      el('path', { d: d, fill: 'none', stroke: colour, 'stroke-width': f(weight), 'stroke-opacity': f(alpha), 'stroke-linecap': 'round', 'class': 'sk-hatch', 'clip-path': clip }, parent);
    }

    function fillShape(shapeD, bbox, s) {
      if (!s.fill || s.fillStyle === 'none') return null;
      var g = el('g', { 'class': 'sk-fill' });
      if (s.grain && !opts.grainAtRoot) g.setAttribute('filter', 'url(#sk-grain)');
      var a = s.fillOpacity;
      if (s.fillStyle === 'solid') {
        el('path', { d: shapeD, fill: s.fill, 'fill-opacity': f(0.85 * a), 'class': 'sk-wash' }, g);
        return g;
      }
      var clipId = nextId('skc');
      var cp = el('clipPath', { id: clipId }, g);
      el('path', { d: shapeD }, cp);
      var clip = 'url(#' + clipId + ')';
      if (s.fillStyle === 'body') {
        el('path', { d: shapeD, fill: s.fill, 'fill-opacity': f(0.38 * a), 'class': 'sk-wash' }, g);
        hatchLines(clip, bbox, s.angle, s.gap * 0.95, 1.3, s.fill, a, g);
        hatchLines(clip, bbox, s.angle + 95, s.gap * 1.45, 1.0, s.fill, 0.65 * a, g);
      } else if (s.fillStyle === 'cross') {
        hatchLines(clip, bbox, s.angle, s.gap, 1.2, s.fill, a, g);
        hatchLines(clip, bbox, s.angle + 95, s.gap * 1.4, 1.0, s.fill, 0.7 * a, g);
      } else if (s.fillStyle === 'scribble') {
        hatchLines(clip, bbox, s.angle, s.gap * 0.7, 1.4, s.fill, a, g);
      } else {
        hatchLines(clip, bbox, s.angle, s.gap, 1.2, s.fill, a, g);
      }
      return g;
    }

    function shape(fillD, bbox, s, builder) {
      var wrap = el('g', { 'class': 'sk-shape' }, root);
      var fg = fillShape(fillD, bbox, s);
      if (fg) wrap.appendChild(fg);
      var saved = root; root = wrap;
      if (s.passes > 0) strokeGroup(s, builder);
      root = saved;
      return wrap;
    }

    var api = {
      seed: seed, random: r, tokens: C,
      into: function (g) { root = g; return api; },
      root: function () { return root; },
      group: function (attrs) { return el('g', attrs || {}, root); },

      line: function (x1, y1, x2, y2, o) {
        var s = style(o);
        return strokeGroup(s, function () { return handLine(x1, y1, x2, y2, r, s.rough); });
      },
      rect: function (x, y, w, h, o) {
        var s = style(o);
        var outline = 'M' + x + ' ' + y + 'H' + (x + w) + 'V' + (y + h) + 'H' + x + 'Z';
        return shape(outline, { x: x, y: y, w: w, h: h }, s, function () {
          return handPoly([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], r, s.rough, true);
        });
      },
      /* The sketch frame used by sheets and buttons: an optional paper
         backing, then an outline drawn twice by a quick hand. */
      frame: function (x, y, w, h, o) {
        o = o || {};
        var s = style(o);
        var g = el('g', { 'class': 'sk-frame-g' }, root);
        if (o.backing) {
          var bj = 1.2 * s.rough;
          el('path', {
            d: 'M' + f(x + 1 + (r() - 0.5) * bj) + ' ' + f(y + 1 + (r() - 0.5) * bj) + 'L' + f(x + w - 1 + (r() - 0.5) * bj) + ' ' + f(y + 1 + (r() - 0.5) * bj) +
              'L' + f(x + w - 1 + (r() - 0.5) * bj) + ' ' + f(y + h - 1 + (r() - 0.5) * bj) + 'L' + f(x + 1 + (r() - 0.5) * bj) + ' ' + f(y + h - 1 + (r() - 0.5) * bj) + 'Z',
            'class': 'sk-backing'
          }, g);
        }
        if (o.lit) {
          var clipId = nextId('skc');
          var cp = el('clipPath', { id: clipId }, g);
          el('rect', { x: x + 2, y: y + 2, width: w - 4, height: h - 4 }, cp);
          var lg = el('g', { 'class': 'sk-lit' }, g);
          hatchLines('url(#' + clipId + ')', { x: x, y: y, w: w, h: h }, -41 + (r() - 0.5) * 10, 4.2, 1.7, o.lit, 0.8, lg);
        }
        var saved = root; root = g;
        s.passes = 2;
        strokeGroup(s, function (p) {
          var k = p ? 1.6 * s.rough : 0;
          return handPoly([[x + (r() - 0.5) * k, y + (r() - 0.5) * k], [x + w + (r() - 0.5) * k, y + (r() - 0.5) * k],
            [x + w + (r() - 0.5) * k, y + h + (r() - 0.5) * k], [x + (r() - 0.5) * k, y + h + (r() - 0.5) * k]], r, s.rough * 1.15, true);
        });
        root = saved;
        return g;
      },
      circle: function (cx, cy, d, o) { return api.ellipse(cx, cy, d, d, o); },
      ellipse: function (cx, cy, w, h, o) {
        var s = style(o);
        var rx = w / 2, ry = h / 2;
        var outline = 'M' + (cx - rx) + ' ' + cy + 'a' + rx + ' ' + ry + ' 0 1 0 ' + (2 * rx) + ' 0a' + rx + ' ' + ry + ' 0 1 0 ' + (-2 * rx) + ' 0Z';
        return shape(outline, { x: cx - rx, y: cy - ry, w: w, h: h }, s, function (p) {
          return handEllipse(cx, cy, rx, ry, r, s.rough, p > 0);
        });
      },
      poly: function (points, o) {
        var s = style(o);
        var xs = points.map(function (p) { return p[0]; }), ys = points.map(function (p) { return p[1]; });
        var bx = Math.min.apply(null, xs), by = Math.min.apply(null, ys);
        var outline = 'M' + points.map(function (p) { return p[0] + ' ' + p[1]; }).join('L') + 'Z';
        return shape(outline, { x: bx, y: by, w: Math.max.apply(null, xs) - bx, h: Math.max.apply(null, ys) - by }, s,
          function () { return handPoly(points, r, s.rough, true); });
      },
      polyline: function (points, o) {
        var s = style(o);
        return strokeGroup(s, function () { return handPoly(points, r, s.rough, false); });
      },
      curve: function (points, o) {
        var s = style(o);
        return strokeGroup(s, function () { return handCurve(points, r, s.rough); });
      },
      /* Raw path data with the pen's stroke and grain (no geometry wobble). */
      path: function (d, o) {
        var s = style(o);
        var bb = { x: 0, y: 0, w: 2000, h: 2000 };
        if (s.fill) {
          // measure in the always-rendered defs svg: hidden boil variants cannot be measured in every browser
          var host = doc.getElementById('sk-defs') || root;
          var probe = el('path', { d: d }, host);
          try { var b = probe.getBBox(); bb = { x: b.x, y: b.y, w: b.width, h: b.height }; } catch (e) { /* not rendered yet */ }
          host.removeChild(probe);
        }
        return shape(d, bb, s, function () { return d; });
      },
      /* Curved arrow with a two-stroke head at plus and minus 0.45 rad. */
      arrow: function (x1, y1, x2, y2, o) {
        o = o || {};
        var s = style(o);
        var bend = o.bend != null ? o.bend : 0.18;
        var mx = (x1 + x2) / 2, my = (y1 + y2) / 2, dx = x2 - x1, dy = y2 - y1;
        var cx = mx - dy * bend, cy = my + dx * bend;
        var g = strokeGroup(s, function () {
          return 'M' + f(x1) + ' ' + f(y1) + 'Q' + f(cx + (r() - 0.5) * 2) + ' ' + f(cy + (r() - 0.5) * 2) + ' ' + f(x2) + ' ' + f(y2);
        });
        var ang = Math.atan2(y2 - cy, x2 - cx), hl = o.head || Math.max(7, Math.min(14, Math.hypot(dx, dy) * 0.12));
        var saved = root; root = g;
        [-0.45, 0.45].forEach(function (k) {
          var a = ang + Math.PI + k + (r() - 0.5) * 0.1;
          strokeGroup(Object.assign({}, s, { passes: 1, dash: null }), function () {
            return handLine(x2, y2, x2 + Math.cos(a) * hl, y2 + Math.sin(a) * hl, r, s.rough * 0.5);
          });
        });
        root = saved;
        return g;
      },
      /* Handwriting in SVG. Labels carry a paper-coloured halo so they stay
         readable over lines (paint-order: stroke, set in CSS). */
      text: function (x, y, str, o) {
        if (typeof o === 'string') o = { anchor: o };
        o = o || {};
        if (skipText) return null;
        var t = el('text', {
          x: f(x), y: f(y), 'class': 'sk-text' + (o.mono ? ' sk-text-mono' : '') + (o.note ? ' sk-text-note' : '') + (o.cls ? ' ' + o.cls : ''),
          'text-anchor': o.anchor || 'start',
          transform: o.rotate ? 'rotate(' + o.rotate + ' ' + f(x) + ' ' + f(y) + ')' : null
        }, labels || root);
        if (o.size) t.style.fontSize = o.size + 'px';
        if (o.color) t.style.fill = o.color;
        if (o.weight) t.style.fontWeight = o.weight;
        if (o.opacity != null) t.style.opacity = o.opacity;
        if (o.halo === false) t.style.stroke = 'none';
        t.textContent = str;
        return t;
      },
      dot: function (x, y, d, o) {
        o = o || {};
        return api.ellipse(x, y, d, d * (0.9 + r() * 0.2), Object.assign({ fill: o.fill || o.stroke || C.graphite, fillStyle: 'solid', passes: 1, width: 0.8 }, o));
      }
    };
    return api;
  }

  /* ------------------------------------------------------------------ *
   * Variants: draw the same thing four times with different jitter, one
   * group per variant. The boil clock shows one group at a time.
   *   Sketchy.variants(svg, function (p, v) { p.rect(...) }, { seed })
   * Labels are drawn once, on top, outside the grain filter.
   * ------------------------------------------------------------------ */
  function variants(target, draw, opts) {
    opts = opts || {};
    var n = opts.variants || (config.boil ? config.variants : 1);
    var base = typeof opts.seed === 'number' ? opts.seed : hash(opts.seed || 'sketchy');
    var C = opts.tokens || tokens();
    var holder = el('g', { 'class': 'sk-variants' }, target);
    var labels = el('g', { 'class': 'sk-labels' });
    for (var v = 0; v < n; v++) {
      var g = el('g', { 'class': 'sk-v sk-v' + v }, holder);
      if (config.grain && opts.grain !== false) g.setAttribute('filter', 'url(#sk-grain)');
      var p = pen(g, {
        seed: (base * 31 + v + 1) >>> 0, tokens: C, width: opts.width, rough: opts.rough, passes: opts.passes,
        stroke: opts.stroke, grainAtRoot: true, labels: labels, skipText: v > 0
      });
      draw(p, v, C);
    }
    if (n === 1) holder.firstChild.classList.add('sk-v-only');
    target.appendChild(labels);
    return holder;
  }

  /* ------------------------------------------------------------------ *
   * Boil clock: one shared, non-repeating 60-step sequence of variant
   * indices, read at 10 fps (2 fps with reduced motion). Sets
   * <html data-sk-boil="0..3">; CSS shows the matching variant group.
   * ------------------------------------------------------------------ */
  var boilSeq = (function () {
    var r = rng(7), s = [0];
    for (var i = 1; i < 60; i++) s.push((s[i - 1] + 1 + Math.floor(r() * 3)) % 4);
    if (s[59] === s[0]) s[59] = (s[59] + 1) % 4;
    if (s[59] === s[58]) s[59] = (s[59] + 2) % 4;
    return s;
  })();
  var boilRunning = false, boilShown = -1;
  function boilFrame(seconds) {
    var fps = reduced ? 2 : config.boilFps;
    return boilSeq[Math.floor(seconds * fps) % 60];
  }
  function startBoil() {
    var html = doc.documentElement;
    if (!config.boil) { html.setAttribute('data-sk-boil', 'off'); return; }
    if (boilRunning) return;
    boilRunning = true;
    (function tick() {
      if (!boilRunning) return;
      var v = boilFrame(global.performance.now() / 1000);
      if (v !== boilShown) { boilShown = v; html.setAttribute('data-sk-boil', String(v)); }
      global.requestAnimationFrame(tick);
    })();
  }
  function stopBoil() { boilRunning = false; boilShown = -1; doc.documentElement.setAttribute('data-sk-boil', 'off'); }

  /* ------------------------------------------------------------------ *
   * Postal objects (draw with any pen)
   * ------------------------------------------------------------------ */
  function postmark(p, cx, cy, rad, top, bottom, o) {
    o = o || {};
    var C = p.tokens, col = o.color || C['red-ink'] || C.graphite;
    var g = p.group({ 'class': 'sk-postmark', opacity: o.opacity != null ? o.opacity : 0.8 });
    var saved = p.root();
    p.into(g);
    p.circle(cx, cy, rad * 2, { stroke: col, width: 2.4, passes: 1, rough: 0.6 });
    p.circle(cx, cy, rad * 1.32, { stroke: col, width: 1.3, passes: 1, rough: 0.6 });
    var defs = el('defs', null, g), id1 = nextId('skpm'), id2 = nextId('skpm'), rr = rad * 0.83;
    el('path', { id: id1, d: 'M' + (cx - rr) + ' ' + cy + 'A' + rr + ' ' + rr + ' 0 0 1 ' + (cx + rr) + ' ' + cy }, defs);
    el('path', { id: id2, d: 'M' + (cx - rr) + ' ' + cy + 'A' + rr + ' ' + rr + ' 0 0 0 ' + (cx + rr) + ' ' + cy }, defs);
    [[id1, top, rad * 0.08], [id2, bottom, rad * 0.16]].forEach(function (a) {
      if (!a[1]) return;
      var t = el('text', { 'class': 'sk-postmark-text', dy: a[2] }, g);
      t.style.fill = col; t.style.fontSize = (rad * 0.24) + 'px';
      var tp = el('textPath', { href: '#' + a[0], startOffset: '50%', 'text-anchor': 'middle' }, t);
      tp.textContent = a[1];
    });
    if (o.center) {
      var c = el('text', { x: cx, y: cy + rad * 0.1, 'text-anchor': 'middle', 'class': 'sk-postmark-text' }, g);
      c.style.fill = col; c.style.fontSize = (rad * 0.3) + 'px'; c.textContent = o.center;
    }
    p.into(saved);
    return g;
  }

  function cancelWaves(p, x, y, w, o) {
    o = o || {};
    var col = o.color || p.tokens.graphite, n = o.lines || 5, step = o.step || 11 * (o.scale || 0.6);
    var g = p.group({ 'class': 'sk-cancel', opacity: o.opacity != null ? o.opacity : 0.55 });
    var saved = p.root(); p.into(g);
    for (var s = 0; s < n; s++) {
      var pts = [];
      for (var u = 0; u <= 30; u++) pts.push([x + w * u / 30, y + s * step + Math.sin(u * 0.7 + s) * 3 * (o.scale || 0.6)]);
      p.curve(pts, { stroke: col, width: 1.2, passes: 1 });
    }
    p.into(saved);
    return g;
  }

  /* Perforated postage stamp; draw its picture with o.inner(p, box). */
  function postage(p, x, y, w, h, o) {
    o = o || {};
    var C = p.tokens;
    var g = p.group({ 'class': 'sk-postage' });
    var saved = p.root(); p.into(g);
    var hole = Math.max(1.8, w * 0.032), step = hole * 2.2;
    var mask = nextId('skm'), defs = el('defs', null, g), m = el('mask', { id: mask }, defs);
    el('rect', { x: x - 2, y: y - 2, width: w + 4, height: h + 4, fill: '#fff' }, m);
    var holes = function (x1, y1, x2, y2) {
      var len = Math.hypot(x2 - x1, y2 - y1), k = Math.round(len / step);
      for (var i = 0; i <= k; i++) el('circle', { cx: f(x1 + (x2 - x1) * i / k), cy: f(y1 + (y2 - y1) * i / k), r: f(hole), fill: '#000' }, m);
    };
    holes(x, y, x + w, y); holes(x + w, y, x + w, y + h); holes(x, y + h, x + w, y + h); holes(x, y, x, y + h);
    el('rect', { x: x, y: y, width: w, height: h, fill: o.paper || '#FBFAF6', mask: 'url(#' + mask + ')', 'class': 'sk-postage-paper' }, g);
    var inset = Math.max(5, w * 0.075);
    var box = { x: x + inset, y: y + inset, w: w - 2 * inset, h: h - 2 * inset };
    el('rect', { x: box.x, y: box.y, width: box.w, height: box.h, fill: C.paper }, g);
    if (o.tint) el('rect', { x: box.x, y: box.y, width: box.w, height: box.h, fill: o.tint, 'fill-opacity': 0.25 }, g);
    if (o.inner) o.inner(p, box);
    p.rect(box.x, box.y, box.w, box.h, { width: 1.2, passes: 1, opacity: 0.6, rough: 0.5 });
    if (o.label) p.text(x + w / 2, box.y + Math.max(7, w * 0.085) + 1, o.label, { anchor: 'middle', size: Math.max(6, w * 0.075), weight: 600, halo: false });
    if (o.value) p.text(x + w / 2, box.y + box.h - 5, o.value, { anchor: 'middle', size: Math.max(9, w * 0.14), weight: 600, halo: false });
    p.into(saved);
    return g;
  }

  /* ------------------------------------------------------------------ *
   * Sketch catalog (viewBox 0 0 140 110), filled by sketches.js
   * ------------------------------------------------------------------ */
  var catalog = {};
  function register(name, fn) { catalog[name] = fn; }

  var sketchParts = {
    magnifier: function (d, x, y, rr) {
      d.circle(x, y, rr * 2, { width: 2.2 });
      d.line(x + rr * 0.7, y + rr * 0.7, x + rr * 1.6, y + rr * 1.6, { width: 3.4 });
    },
    person: function (d, x, y, C, o) {
      d.circle(x, y, 16, o);
      d.path('M' + (x - 13) + ' ' + (y + 26) + ' Q' + x + ' ' + (y + 6) + ' ' + (x + 13) + ' ' + (y + 26), o);
    },
    envelope: function (d, x, y, w, h, C, o) {
      d.rect(x, y, w, h, o);
      d.polyline([[x, y], [x + w / 2, y + h * 0.55], [x + w, y]]);
    },
    globe: function (d, x, y, rr, C) {
      d.circle(x, y, rr * 2, { fill: C.blue });
      d.ellipse(x, y, rr * 0.9, rr * 2);
      d.line(x - rr, y, x + rr, y);
    },
    clock: function (d, x, y, rr) {
      d.circle(x, y, rr * 2);
      d.line(x, y, x, y - rr * 0.65);
      d.line(x, y, x + rr * 0.5, y + rr * 0.2);
    },
    check: function (d, x, y, s, C) {
      d.polyline([[x, y], [x + s * 0.4, y + s * 0.4], [x + s, y - s * 0.5]], { stroke: C.green, width: 3 });
    },
    planet: function (d, x, y, rr, colour, C, ring) {
      d.circle(x, y, rr * 2, { fill: colour });
      if (ring) d.ellipse(x, y, rr * 3.6, rr * 0.9, { width: 1.1 });
    }
  };

  function drawSketch(svg, C) {
    var name = svg.getAttribute('data-sketch');
    var fn = catalog[name];
    if (!svg.getAttribute('viewBox')) svg.setAttribute('viewBox', '0 0 140 110');
    if (!fn) return false;
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    svg.classList.add('sk-sketch');
    variants(svg, function (p) { fn(p, C, sketchParts); },
      { seed: name + (svg.getAttribute('data-seed') || ''), tokens: C, width: 1.6 });
    return true;
  }

  /* ------------------------------------------------------------------ *
   * DOM decorators: data-sk="frame|sheet|button|box|underline|circle|
   * strike|highlight|bracket"
   * data-sk-color picks a token (red, blue ...), data-sk-seed fixes it.
   * ------------------------------------------------------------------ */
  var DECOS = {
    frame: function (p, w, h, o) { p.frame(3, 3, w - 6, h - 6, { stroke: o.color, width: o.width || 1.4, rough: 1.25, opacity: 0.95, backing: o.backing }); },
    sheet: function (p, w, h, o) { p.frame(3, 3, w - 6, h - 6, { stroke: o.color, width: o.width || 1.45, rough: 1.3, opacity: 0.95, backing: true }); },
    button: function (p, w, h, o) {
      p.frame(3, 3, w - 6, h - 6, { stroke: o.color, width: o.width || (o.accent ? 1.7 : 1.3), rough: 1.3, opacity: 0.95, backing: true, lit: o.lit });
    },
    box: function (p, w, h, o) { p.rect(3, 3, w - 6, h - 6, { stroke: o.color, width: o.width || 1.2, passes: 2 }); },
    underline: function (p, w, h, o) { p.line(1, h - 2, w - 1, h - 1, { stroke: o.color, width: o.width || 1.8, passes: 2 }); },
    circle: function (p, w, h, o) { p.ellipse(w / 2, h / 2, w + 10, h + 6, { stroke: o.color, width: o.width || 1.6, passes: 2, rough: 1.2 }); },
    strike: function (p, w, h, o) { p.line(0, h * 0.58, w, h * 0.46, { stroke: o.color, width: o.width || 1.8, passes: 1 }); },
    highlight: function (p, w, h, o) {
      p.rect(-2, h * 0.18, w + 4, h * 0.7, { fill: o.color, fillStyle: 'hatch', gap: 1.8, angle: -62, passes: 0, fillOpacity: 0.85 });
    },
    bracket: function (p, w, h, o) { p.polyline([[10, 2], [3, 3], [3, h - 3], [10, h - 2]], { stroke: o.color, width: o.width || 1.5 }); }
  };
  var OUTSET = { frame: 6, sheet: 6, button: 4, box: 4, underline: 0, circle: 12, strike: 0, highlight: 2, bracket: 0 };
  var INK_DECOS = { circle: 1, underline: 1, strike: 1 };

  function decorate(node, C) {
    var kind = node.getAttribute('data-sk');
    if (!DECOS[kind]) return;
    var w = node.offsetWidth, h = node.offsetHeight;
    if (!w || !h) return;
    var key = w + 'x' + h + '|' + (node.getAttribute('aria-pressed') || '') + '|' + node.className + '|' + (doc.documentElement.getAttribute('data-theme') || '');
    if (node.__skKey === key && node.querySelector(':scope > svg.sk-deco')) return;
    node.__skKey = key;
    var old = node.querySelector(':scope > svg.sk-deco');
    if (old) old.remove();
    var out = OUTSET[kind] || 0;
    if (global.getComputedStyle(node).position === 'static') node.style.position = 'relative';
    var W = w + out * 2, H = h + out * 2;
    var svg = el('svg', { 'class': 'sk-deco sk-deco-' + kind, 'aria-hidden': 'true', focusable: 'false', width: W, height: H, viewBox: (-out) + ' ' + (-out) + ' ' + W + ' ' + H });
    svg.style.cssText = 'position:absolute;left:' + (-out) + 'px;top:' + (-out) + 'px;width:' + W + 'px;height:' + H + 'px;max-width:none;margin:0;pointer-events:none;overflow:visible;z-index:' + (kind === 'highlight' || kind === 'sheet' || kind === 'button' || kind === 'frame' ? '-1' : '0') + ';';
    node.insertBefore(svg, node.firstChild);
    if (kind === 'sheet' || kind === 'button' || kind === 'frame' || kind === 'highlight') node.style.isolation = 'isolate';
    var colorName = node.getAttribute('data-sk-color');
    var accent = node.classList.contains('is-accent');
    var color = colorName ? (C[colorName] || colorName) : (accent ? C['red-frame'] : (INK_DECOS[kind] ? C.red : C.graphite));
    if (kind === 'highlight') color = colorName ? (C[colorName] || colorName) : C.yellow;
    var lit = (node.getAttribute('aria-pressed') === 'true' || node.classList.contains('is-on')) ? C.orange : null;
    var seed = node.getAttribute('data-sk-seed') || (kind + ':' + (node.id || (node.textContent || '').trim().slice(0, 24)));
    variants(svg, function (p) {
      DECOS[kind](p, w, h, { color: color, width: parseFloat(node.getAttribute('data-sk-width')) || null, accent: accent, lit: lit, backing: node.hasAttribute('data-sk-backing') });
    }, { seed: seed, tokens: C });
  }

  /* ------------------------------------------------------------------ *
   * Motion helpers. CSS transitions and animations are used on purpose:
   * they show up in document.getAnimations(), so the video renderer can
   * pause and seek them frame by frame.
   * ------------------------------------------------------------------ */
  /* Trace every pencil stroke inside root, as if drawn now (opt-in: explainers, video). */
  function drawOn(root, opts) {
    opts = opts || {};
    root = root || doc;
    if (reduced || opts.instant || 'static' in params || 'print' in params) return Promise.resolve();
    // Only the first variant is traced (hidden variants never run transitions);
    // while it draws, the element holds that variant instead of boiling.
    var paths = Array.prototype.slice.call(root.querySelectorAll('.sk-path, .sk-hatch, .sk-wash')).filter(function (p) {
      var v = p.closest('.sk-v');
      return !v || v.classList.contains('sk-v0') || v.classList.contains('sk-v-only');
    });
    if (!paths.length) return Promise.resolve();
    var holders = Array.prototype.slice.call(root.matches && root.matches('svg') ? [root] : root.querySelectorAll('svg'));
    holders.forEach(function (s) { s.classList.add('sk-drawing'); });
    var stagger = opts.stagger != null ? opts.stagger : 14, delay = opts.delay || 0, dur = opts.duration || 560;
    var ease = opts.ease || 'cubic-bezier(.35,.1,.25,1)';
    var last = 0;
    // 1. start state with no transition, so nothing animates towards it
    paths.forEach(function (pth) {
      pth.style.transition = 'none';
      if (pth.classList.contains('sk-path') && !pth.getAttribute('stroke-dasharray')) {
        pth.__skTrace = true; pth.style.strokeDasharray = '1 1'; pth.style.strokeDashoffset = '1';
      } else { pth.__skTrace = false; pth.style.opacity = '0'; }
    });
    // 2. flush the start state before any transition exists
    void global.getComputedStyle(paths[0]).strokeDashoffset;
    void root.getBoundingClientRect;
    // 3. transitions plus end values: the pencil traces, then shading lays down
    paths.forEach(function (pth, i) {
      var at = delay + i * stagger;
      if (pth.__skTrace) {
        pth.style.transition = 'stroke-dashoffset ' + dur + 'ms ' + ease + ' ' + at + 'ms';
        pth.style.strokeDashoffset = '0';
      } else {
        pth.style.transition = 'opacity ' + Math.round(dur * 1.3) + 'ms ease-out ' + (at + dur * 0.6) + 'ms';
        pth.style.opacity = '';
      }
      last = Math.max(last, at + dur * 1.9);
    });
    return new Promise(function (res) {
      global.setTimeout(function () {
        holders.forEach(function (s) { s.classList.remove('sk-drawing'); });
        res();
      }, last + 30);
    });
  }

  /* ------------------------------------------------------------------ *
   * Paper: a seeded tile (tooth, mottling, fibres) used as a CSS
   * background so it prints, scales and works from file://. Soft blotches
   * and the blue-black vignette are CSS gradients in sketchy.css.
   * ------------------------------------------------------------------ */
  var paperCache = {};
  function paperTexture(kind) {
    kind = kind || 'day';
    if (paperCache[kind]) return paperCache[kind];
    var size = 384, c = doc.createElement('canvas');
    c.width = c.height = size;
    var x = c.getContext('2d');
    var r = rng(1609 + kind.length);
    var dark = kind === 'night';
    // coarse mottling: a small noise grid scaled up so it reads as clouds
    var g = 24, small = doc.createElement('canvas'); small.width = small.height = g;
    var sx = small.getContext('2d'), si = sx.createImageData(g, g);
    for (var i = 0; i < si.data.length; i += 4) {
      var v = r();
      if (v < 0.5) { si.data[i] = dark ? 0 : 130; si.data[i + 1] = dark ? 0 : 112; si.data[i + 2] = dark ? 10 : 85; si.data[i + 3] = (0.5 - v) * (dark ? 60 : 26); }
      else { si.data[i] = 255; si.data[i + 1] = 255; si.data[i + 2] = 250; si.data[i + 3] = (v - 0.5) * (dark ? 14 : 40); }
    }
    sx.putImageData(si, 0, 0);
    x.imageSmoothingEnabled = true;
    x.drawImage(small, 0, 0, size, size);
    // fine tooth: per-pixel speckle, mostly faint
    var img = x.getImageData(0, 0, size, size);
    for (var k = 0; k < img.data.length; k += 4) {
      var n = r(), a;
      if (n < 0.5) {
        a = Math.pow(0.5 - n, 1.5) * (dark ? 0.35 : 0.22) * 255;
        img.data[k] = (img.data[k] * img.data[k + 3] + (dark ? 0 : 95) * a) / Math.max(1, img.data[k + 3] + a);
        img.data[k + 1] = (img.data[k + 1] * img.data[k + 3] + (dark ? 0 : 82) * a) / Math.max(1, img.data[k + 3] + a);
        img.data[k + 2] = (img.data[k + 2] * img.data[k + 3] + (dark ? 8 : 60) * a) / Math.max(1, img.data[k + 3] + a);
      } else {
        a = (n - 0.5) * (dark ? 0.06 : 0.14) * 255;
        img.data[k] = 255; img.data[k + 1] = 255; img.data[k + 2] = 250;
      }
      img.data[k + 3] = Math.min(255, img.data[k + 3] + a);
    }
    x.putImageData(img, 0, 0);
    // fibres: short bowed hairs pressed into the sheet
    x.lineCap = 'round';
    var fibres = Math.round(size * size / 1400);
    for (var q = 0; q < fibres; q++) {
      var fx = r() * size, fy = r() * size, ang = r() * Math.PI * 2, len = 3 + r() * r() * 24;
      var light = r() < 0.35;
      x.strokeStyle = dark ? (light ? 'rgba(255,255,255,' + (0.04 + r() * 0.06) + ')' : 'rgba(0,0,0,' + (0.1 + r() * 0.15) + ')')
        : (light ? 'rgba(255,253,246,' + (0.25 + r() * 0.35) + ')' : 'rgba(125,108,80,' + (0.04 + r() * 0.08) + ')');
      x.lineWidth = 0.3 + r() * 0.5;
      var bow = (r() - 0.5) * 0.6 * len;
      x.beginPath(); x.moveTo(fx, fy);
      x.quadraticCurveTo(fx + Math.cos(ang) * len / 2 - Math.sin(ang) * bow, fy + Math.sin(ang) * len / 2 + Math.cos(ang) * bow, fx + Math.cos(ang) * len, fy + Math.sin(ang) * len);
      x.stroke();
    }
    var url = 'url(' + c.toDataURL('image/png') + ')';
    paperCache[kind] = url;
    return url;
  }

  /* Sky of the sketchbook: dots, plus signs, sparkles, asterisks in graphite
     with a little sun, blue and red pencil. */
  function specks(svg, w, h, opts) {
    opts = opts || {};
    var p = pen(svg, { seed: opts.seed || 'specks', width: 1, grain: false });
    var C = p.tokens, r = p.random, n = opts.count || Math.round(w * h / 12000);
    var cols = opts.colors || [C.graphite, C.graphite, C.graphite, C.yellow, C.blue, C.red];
    var holder = el('g', { 'class': 'sk-specks-g', opacity: opts.opacity || 0.75 }, svg);
    for (var i = 0; i < n; i++) {
      var x = r() * w, y = r() * h, col = cols[Math.floor(r() * cols.length)], s = 2 + r() * 4, k = r(), a = f(0.35 + r() * 0.5);
      if (k < 0.5) el('circle', { cx: f(x), cy: f(y), r: f(0.6 + r() * 1.1), fill: col, opacity: a }, holder);
      else if (k < 0.72) el('path', { d: 'M' + f(x - s) + ' ' + f(y) + 'H' + f(x + s) + 'M' + f(x) + ' ' + f(y - s) + 'V' + f(y + s), stroke: col, 'stroke-width': 0.9, opacity: a, 'stroke-linecap': 'round' }, holder);
      else if (k < 0.88) {
        var s2 = s * 1.6;
        el('path', { d: 'M' + f(x) + ' ' + f(y - s2) + 'Q' + f(x) + ' ' + f(y) + ' ' + f(x + s2) + ' ' + f(y) + 'Q' + f(x) + ' ' + f(y) + ' ' + f(x) + ' ' + f(y + s2) + 'Q' + f(x) + ' ' + f(y) + ' ' + f(x - s2) + ' ' + f(y) + 'Q' + f(x) + ' ' + f(y) + ' ' + f(x) + ' ' + f(y - s2) + 'Z', fill: col, opacity: a }, holder);
      } else {
        var d = '';
        for (var j = 0; j < 3; j++) { var aa = j * Math.PI / 3 + r() * 0.3; d += 'M' + f(x - Math.cos(aa) * s) + ' ' + f(y - Math.sin(aa) * s) + 'L' + f(x + Math.cos(aa) * s) + ' ' + f(y + Math.sin(aa) * s); }
        el('path', { d: d, stroke: col, 'stroke-width': 0.9, opacity: a, 'stroke-linecap': 'round' }, holder);
      }
    }
    return holder;
  }

  /* ------------------------------------------------------------------ *
   * Figures: count a number up the way a receipt total settles.
   * <span data-count>1,240</span> keeps prefix, suffix, separators,
   * decimals and the true minus sign (U+2212). data-count-from, -delay, -ms.
   * ------------------------------------------------------------------ */
  function parseFigure(text, lang) {
    var m = String(text).match(/^([^0-9\u2212+\-±]*)([\u2212+\-±]?)([0-9][0-9,.\u202f\u00a0 ]*)(.*)$/);
    if (!m) return null;
    var raw = m[3].replace(/[\s\u202f\u00a0]+$/, ''), suffix = m[3].slice(raw.length) + m[4];
    // which mark is the decimal point? the last of two different marks; a lone
    // comma is decimal in comma locales (de, fr, ...) unless it groups three digits twice
    var commaLocale = /^(de|fr|es|it|pt|nl|pl|cs|da|fi|nb|sv|tr|ru|uk|id)/i.test(lang || doc.documentElement.lang || '');
    var lastC = raw.lastIndexOf(','), lastD = raw.lastIndexOf('.'), decMark = '';
    if (lastC > -1 && lastD > -1) decMark = lastC > lastD ? ',' : '.';
    else if (lastC > -1) decMark = (commaLocale ? /^\d{1,3}(,\d{3}){2,}$/ : /^\d{1,3}(,\d{3})+$/).test(raw) ? '' : ',';
    else if (lastD > -1) decMark = /^\d{1,3}(\.\d{3}){2,}$/.test(raw) || (commaLocale && /^\d{1,3}\.\d{3}$/.test(raw)) ? '' : '.';
    var group = (raw.match(/[,.\u202f\u00a0 ]/g) || []).filter(function (c) { return c !== decMark; })[0] || '';
    var intPart = decMark ? raw.slice(0, raw.lastIndexOf(decMark)) : raw, frac = decMark ? raw.slice(raw.lastIndexOf(decMark) + 1) : '';
    var value = parseFloat(intPart.replace(/[^0-9]/g, '') + (frac ? '.' + frac : ''));
    var neg = m[2] === '-' || m[2] === '\u2212';
    return { prefix: m[1], sign: m[2], value: (neg ? -1 : 1) * value, dec: frac.length, decMark: decMark || '.', sep: group === ' ' || group === '\u00a0' ? '\u202f' : group, suffix: suffix };
  }
  function formatFigure(spec, v) {
    var parts = Math.abs(v).toFixed(spec.dec).split('.');
    if (spec.sep) parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, spec.sep);
    var sign = v < 0 ? '\u2212' : (spec.sign === '+' || spec.sign === '±' ? spec.sign : '');
    return spec.prefix + sign + parts.join(spec.decMark || '.') + spec.suffix;
  }
  function countUp(el) {
    if (!el.__skFig) el.__skFig = parseFigure(el.textContent.trim());
    var spec = el.__skFig;
    if (!spec || reduced || 'static' in params || 'print' in params) return;
    var from = parseFloat(el.getAttribute('data-count-from')) || 0;
    var delay = parseFloat(el.getAttribute('data-count-delay')) || 300;
    var dur = parseFloat(el.getAttribute('data-count-ms')) || 900;
    if (!el.style.minWidth && el.offsetWidth) { el.style.display = el.style.display || 'inline-block'; el.style.minWidth = el.offsetWidth + 'px'; }
    el.textContent = formatFigure(spec, from);
    var t0 = null;
    function tick(now) {
      if (t0 === null) t0 = now + delay;
      var q = Math.min(1, Math.max(0, (now - t0) / dur));
      el.textContent = formatFigure(spec, from + (spec.value - from) * (1 - Math.pow(1 - q, 3)));
      if (q < 1) global.requestAnimationFrame(tick);
    }
    global.requestAnimationFrame(tick);
  }

  /* Pages (not decks): sheets settle in, pictures trace themselves and
     numbers count up the first time they scroll into view. */
  var revealIO = null;
  function revealPage(root) {
    if (doc.querySelector('main.sk-deck') || !global.IntersectionObserver) return;
    var still = reduced || 'static' in params || 'print' in params;
    root.querySelectorAll('[data-reveal="print"]').forEach(function (box) { Array.prototype.forEach.call(box.children, function (c, k) { c.style.setProperty('--i', k); }); });
    var targets = root.querySelectorAll('[data-reveal], svg[data-sketch][data-draw], .sk-chart[data-draw], [data-count]:not(svg)');
    if (still) { targets.forEach(function (t) { t.classList.add('is-in'); }); return; }
    if (!revealIO) revealIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var t = e.target;
        revealIO.unobserve(t);
        t.classList.add('is-in');
        if (t.hasAttribute('data-count')) countUp(t);
        if (t.hasAttribute('data-draw')) drawOn(t.matches('svg') ? t : t.querySelector('svg') || t, { stagger: 10, duration: 520, delay: 120 });
        t.querySelectorAll && t.querySelectorAll('[data-count]').forEach(countUp);
      });
    }, { threshold: 0.25 });
    targets.forEach(function (t) { if (!t.classList.contains('is-in')) { t.classList.add('is-waiting'); revealIO.observe(t); } });
  }

  /* ------------------------------------------------------------------ *
   * Mount
   * ------------------------------------------------------------------ */
  var ro = null, hooks = [];
  function onMount(fn) { hooks.push(fn); }

  function mount(root, opts) {
    root = root || doc;
    opts = opts || {};
    ensureDefs();
    var html = doc.documentElement;
    if ('static' in params || 'print' in params) { config.boil = false; html.classList.add('sk-static'); }
    var C = tokens();
    var kindToken = global.getComputedStyle(html).getPropertyValue('--sk-paper-kind').trim();
    var paper = html.getAttribute('data-paper') || (kindToken === 'dark' ? 'night' : kindToken === 'light' ? 'day' : (html.getAttribute('data-theme') === 'night' ? 'night' : 'day'));
    html.style.setProperty('--sk-paper-texture', paperTexture(paper));
    root.querySelectorAll('svg[data-sketch]').forEach(function (s) { drawSketch(s, C); });
    root.querySelectorAll('[data-sk]').forEach(function (n) { n.__skKey = null; decorate(n, C); });
    root.querySelectorAll('svg[data-specks]').forEach(function (s) {
      var vb = (s.getAttribute('viewBox') || '0 0 1600 900').split(/\s+/).map(Number);
      while (s.firstChild) s.removeChild(s.firstChild);
      specks(s, vb[2], vb[3], { seed: s.getAttribute('data-specks') || 'specks', count: +(s.getAttribute('data-specks-count') || s.getAttribute('data-count')) || null });
    });
    root.querySelectorAll('svg[data-postmark]').forEach(function (s) {
      while (s.firstChild) s.removeChild(s.firstChild);
      if (!s.getAttribute('viewBox')) s.setAttribute('viewBox', '0 0 160 110');
      var parts = (s.getAttribute('data-postmark') || '').split('|');
      variants(s, function (p) {
        if (s.hasAttribute('data-cancel')) cancelWaves(p, 4, 30, 66, { lines: 5 });
        var pc = s.getAttribute('data-postmark-color');
        postmark(p, s.hasAttribute('data-cancel') ? 110 : 80, 56, 44, parts[0] || '', parts[1] || '', { center: s.getAttribute('data-postmark-center') || '', color: pc ? (C[pc] || pc) : null });
      }, { seed: 'postmark:' + (s.getAttribute('data-postmark') || ''), tokens: C });
    });
    hooks.forEach(function (fn) { try { fn(root, C); } catch (e) { global.console && console.error(e); } });
    revealPage(root);
    if (global.ResizeObserver && !ro) {
      var pending = new Set(), raf = 0;
      ro = new ResizeObserver(function (entries) {
        entries.forEach(function (e) { pending.add(e.target); });
        if (!raf) raf = global.requestAnimationFrame(function () {
          raf = 0; var CC = tokens();
          pending.forEach(function (n) { decorate(n, CC); }); pending.clear();
        });
      });
    }
    if (ro) root.querySelectorAll('[data-sk]').forEach(function (n) { ro.observe(n); });
    if (!mount._watching) {
      mount._watching = true;
      // frames are drawn to the element's size; print layout differs, so redraw around printing
      var redrawAll = function () { var CC = tokens(); doc.querySelectorAll('[data-sk]').forEach(function (n) { n.__skKey = null; decorate(n, CC); }); };
      global.addEventListener('beforeprint', redrawAll);
      global.addEventListener('afterprint', redrawAll);
      new MutationObserver(function () { paperCache = {}; mount(doc, opts); })
        .observe(html, { attributes: true, attributeFilter: ['data-theme', 'data-paper'] });
      // buttons redraw when pressed state changes
      new MutationObserver(function (list) {
        var CC = tokens();
        list.forEach(function (m) { if (m.target.hasAttribute && m.target.hasAttribute('data-sk')) decorate(m.target, CC); });
      }).observe(doc.body || html, { subtree: true, attributes: true, attributeFilter: ['aria-pressed', 'class'] });
    }
    if (doc.fonts && doc.fonts.ready && !mount._fonts) {
      mount._fonts = true;
      doc.fonts.ready.then(function () { var CC = tokens(); doc.querySelectorAll('[data-sk]').forEach(function (n) { n.__skKey = null; decorate(n, CC); }); });
    }
    startBoil();
    return Sketchy;
  }

  function toSVGString(svg) {
    var clone = svg.cloneNode(true);
    clone.setAttribute('xmlns', NS);
    var d = el('defs'); d.innerHTML = DEFS_HTML;
    clone.insertBefore(d, clone.firstChild);
    return new XMLSerializer().serializeToString(clone);
  }

  var Sketchy = {
    version: '0.1.0',
    config: config, params: params,
    hash: hash, rng: rng, tokens: tokens,
    pen: pen, variants: variants,
    geometry: { line: handLine, ellipse: handEllipse, poly: handPoly, curve: handCurve, smooth: smoothPath },
    postmark: postmark, cancelWaves: cancelWaves, postage: postage, specks: specks,
    catalog: catalog, parts: sketchParts, register: register, drawSketch: drawSketch,
    decorate: decorate, decorators: DECOS,
    drawOn: drawOn, boil: { start: startBoil, stop: stopBoil, frame: boilFrame, sequence: boilSeq },
    figure: { parse: parseFigure, format: formatFigure }, countUp: countUp, revealPage: revealPage,
    paperTexture: paperTexture,
    mount: mount, onMount: onMount, toSVGString: toSVGString,
    get reducedMotion() { return reduced; }
  };
  global.Sketchy = Sketchy;
  // sketch-board compatibility: older pages call Sketch.drawAll()
  if (!global.Sketch) global.Sketch = {
    register: function (n, fn) { register(n, function (p, C) { fn(p, C); }); },
    drawAll: function (root) { (root || doc).querySelectorAll('svg[data-sketch]').forEach(function (s) { drawSketch(s, tokens()); }); },
    watchTheme: function () { mount(); }
  };
})(typeof window !== 'undefined' ? window : this);
