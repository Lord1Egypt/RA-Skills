/*!
 * sketches.js: the sketch catalog
 * Small hand-drawn pictures of things, used on slides and explainers instead of
 * icons. Every sketch lives in a 140 x 110 viewBox, is drawn with the sketchy
 * pen, takes its colors from tokens and is seeded by its name, so it looks the
 * same on every load, in the PDF and in the video.
 *
 *   <svg data-sketch="rocket" viewBox="0 0 140 110"></svg>      then Sketchy.mount()
 *
 * Load order: sketchy.css, sketchy.js, sketches.js. The first 21 sketches come
 * from sketch-board (their German notes are gone, the pictures speak). The rest
 * are grouped in families: Sketchy.sketchFamilies = { business: [...], ... }.
 *
 * Rules every sketch keeps: 5 to 14 primitives, at most one accent color of
 * fill, green only for checks, red only for stop, wrong or "the one thing",
 * labels only when the text belongs to the object itself ("{ }", "!").
 * Register your own with Sketchy.register(name, function (p, C, parts) { ... }).
 * MIT License. https://github.com/OthmanAdi/sketchy
 */
(function (global) {
  'use strict';
  var S = global.Sketchy;
  if (!S || !S.register) {
    if (global.console) global.console.warn('sketches.js: load sketchy.js first');
    return;
  }
  var PI = Math.PI, parts = S.parts, FAM = {};
  S.sketchFamilies = FAM;

  /* ------------------------------------------------------------------ *
   * Small helpers (private). Every one draws through the pen it is given.
   * ------------------------------------------------------------------ */
  function reg(family, name, fn) {
    var list = FAM[family] = FAM[family] || [];
    if (list.indexOf(name) < 0) list.push(name);
    S.register(name, fn);
  }
  function rad(a) { return a * PI / 180; }
  function copy(o, extra) { var r = {}, k; for (k in o) r[k] = o[k]; for (k in extra) r[k] = extra[k]; return r; }

  /* Points along an elliptical arc. Degrees, 0 = right, 90 = down (SVG). */
  function arcPts(cx, cy, rx, ry, a0, a1, n) {
    n = n || Math.max(4, Math.ceil(Math.abs(a1 - a0) / 28));
    var pts = [];
    for (var i = 0; i <= n; i++) {
      var a = rad(a0 + (a1 - a0) * i / n);
      pts.push([cx + Math.cos(a) * rx, cy + Math.sin(a) * ry]);
    }
    return pts;
  }
  function arc(p, cx, cy, rx, ry, a0, a1, o) { return p.curve(arcPts(cx, cy, rx, ry, a0, a1), o); }
  function quadPts(x0, y0, cx, cy, x1, y1, n) {
    n = n || 6;
    var pts = [];
    for (var i = 0; i <= n; i++) {
      var t = i / n, u = 1 - t;
      pts.push([u * u * x0 + 2 * u * t * cx + t * t * x1, u * u * y0 + 2 * u * t * cy + t * t * y1]);
    }
    return pts;
  }
  function quad(p, x0, y0, cx, cy, x1, y1, o) { return p.curve(quadPts(x0, y0, cx, cy, x1, y1), o); }

  /* Catmull-Rom sampled into plain points, the same curve the pen draws. */
  function dense(pts, closed, per) {
    per = per || 5;
    var out = [], n = pts.length;
    for (var i = 0; i < (closed ? n : n - 1); i++) {
      var p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n], p3 = pts[(i + 2) % n];
      if (!closed) { if (i === 0) p0 = p1; if (i + 2 >= n) p3 = p2; }
      var c1x = p1[0] + (p2[0] - p0[0]) / 6, c1y = p1[1] + (p2[1] - p0[1]) / 6;
      var c2x = p2[0] - (p3[0] - p1[0]) / 6, c2y = p2[1] - (p3[1] - p1[1]) / 6;
      for (var k = 0; k < per; k++) {
        var t = k / per, u = 1 - t;
        out.push([u * u * u * p1[0] + 3 * u * u * t * c1x + 3 * u * t * t * c2x + t * t * t * p2[0],
          u * u * u * p1[1] + 3 * u * u * t * c1y + 3 * u * t * t * c2y + t * t * t * p2[1]]);
      }
    }
    if (!closed) out.push(pts[n - 1]);
    return out;
  }

  /* Fill only (no outline): the colored pencil inside a shape drawn separately. */
  function fillOnly(p, pts, o) { return p.poly(pts, copy(o, { passes: 0 })); }

  /* A smooth closed shape: filled inside, outlined by one hand-wobbled loop. */
  function blob(p, pts, o) {
    o = o || {};
    if (o.fill) fillOnly(p, dense(pts, true, 5), o);
    return p.curve(pts.concat([pts[0], pts[1]]), copy(o, { fill: null, fillStyle: null }));
  }

  /* Rounded rectangle as a polygon: long edges wobble, corners stay crisp.
     tail = { x: base centre on the bottom edge, hw: half base, tx, ty: the tip } */
  function rrPts(x, y, w, h, r, tail) {
    r = Math.min(r, w / 2, h / 2);
    var pts = [];
    function corner(cx, cy, a0) {
      for (var i = 0; i <= 3; i++) { var a = rad(a0 + 30 * i); pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); }
    }
    corner(x + r, y + r, 180);
    corner(x + w - r, y + r, 270);
    corner(x + w - r, y + h - r, 0);
    if (tail) {
      var hw = tail.hw || 6;
      pts.push([tail.x + hw, y + h], [tail.tx, tail.ty], [tail.x - hw, y + h]);
    }
    corner(x + r, y + h - r, 90);
    return pts;
  }
  function rrect(p, x, y, w, h, r, o) { return p.poly(rrPts(x, y, w, h, r), o); }

  /* Four-point sparkle as one concave polygon. */
  function sparkle(p, x, y, s, o) {
    var k = 0.24 * s;
    return p.poly([[x, y - s], [x + k, y - k], [x + s, y], [x + k, y + k], [x, y + s], [x - k, y + k], [x - s, y], [x - k, y - k]],
      copy({ width: 1.2, passes: 1 }, o || {}));
  }

  /* Draw a block inside a transformed group, then return to the old root. */
  function xf(p, transform, fn) {
    var g = p.group({ transform: transform }), parent = g.parentNode;
    p.into(g);
    fn(p);
    p.into(parent);
    return g;
  }
  function rot(p, deg, cx, cy, fn) { return xf(p, 'rotate(' + deg + ' ' + cx + ' ' + cy + ')', fn); }
  function shift(p, dx, dy, fn) { return xf(p, 'translate(' + dx + ' ' + dy + ')', fn); }

  /* Many tiny raw strokes (pins, ticks, legs) as one path. Segments: [[x1,y1,x2,y2], ...] */
  function ticks(p, segs, o) {
    var d = '';
    segs.forEach(function (s) { d += 'M' + s[0] + ' ' + s[1] + 'L' + s[2] + ' ' + s[3]; });
    return p.path(d, copy({ passes: 1 }, o || {}));
  }
  /* A row of round beads or dots drawn as one dashed, round-capped line. */
  function beads(p, x1, y1, x2, y2, d, step, o) {
    return p.line(x1, y1, x2, y2, copy({ width: d, dash: '0.01 ' + step, passes: 1, rough: 0.3 }, o || {}));
  }

  /* ------------------------------------------------------------------ *
   * Six reusable parts, added to Sketchy.parts (existing ones are kept).
   * ------------------------------------------------------------------ */
  function addPart(name, fn) { if (!parts[name]) parts[name] = fn; }

  /* Oblique box: front face, lid and right side. o styles the front face. */
  addPart('box3d', function (p, x, y, w, h, depth, o) {
    var dx = depth * 0.72, dy = -depth * 0.55, C = p.tokens;
    var edge = { fill: o && o.sideFill };
    p.poly([[x + w, y], [x + w + dx, y + dy], [x + w + dx, y + h + dy], [x + w, y + h]], edge.fill ? { fill: edge.fill } : {});
    p.poly([[x, y], [x + dx, y + dy], [x + w + dx, y + dy], [x + w, y]], {});
    p.rect(x, y, w, h, copy(o || {}, { sideFill: null }));
    return { dx: dx, dy: dy, C: C };
  });

  /* Gear with n teeth around (cx, cy); ro = outer radius. Hub hole is painted over. */
  addPart('gear', function (p, cx, cy, ro, n, o) {
    o = o || {};
    var ri = ro * 0.78, pts = [], w = 2 * PI / n, off = rad(o.turn || 0), i;
    for (i = 0; i < n; i++) {
      var a = off + i * w;
      [[ri, -0.29], [ro, -0.16], [ro, 0.16], [ri, 0.29]].forEach(function (t) {
        pts.push([cx + Math.cos(a + t[1] * w) * t[0], cy + Math.sin(a + t[1] * w) * t[0]]);
      });
    }
    p.poly(pts, copy(o, { turn: null, hole: null }));
    if (o.hole !== false) p.circle(cx, cy, ro * 0.62, { fill: p.tokens['paper-light'], fillStyle: 'solid', width: 1.3 });
  });

  /* Cloud outline centred on (cx, cy), w wide, about 0.55 w tall. */
  addPart('cloud', function (p, cx, cy, w, o) {
    var k = w / 96, base = [[-30, 22], [-46, 12], [-44, -6], [-26, -12], [-18, -26], [0, -30], [18, -24], [28, -10], [44, -8], [48, 10], [34, 22], [0, 24]];
    blob(p, base.map(function (q) { return [cx + q[0] * k, cy + q[1] * k]; }), o);
  });

  /* Star with n points; ro outer radius, ri inner. */
  addPart('star', function (p, cx, cy, ro, ri, n, o) {
    var pts = [];
    n = n || 5;
    for (var i = 0; i < n * 2; i++) {
      var a = -PI / 2 + i * PI / n, r = i % 2 ? (ri || ro * 0.45) : ro;
      pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]);
    }
    return p.poly(pts, o);
  });

  /* n short text lines (scribbles standing for writing) starting at (x, y). */
  addPart('lines', function (p, x, y, w, n, gap, o) {
    var f = [1, 0.82, 0.94, 0.6, 0.88, 0.7];
    for (var i = 0; i < n; i++) p.line(x, y + i * gap, x + w * f[i % f.length], y + i * gap, copy({ width: 1.3, passes: 1 }, o || {}));
  });

  /* Speech bubble with rounded corners and a tail on the bottom edge:
     tail = { x, tx, ty, hw }. Without a tail it is a plain rounded card. */
  addPart('bubble', function (p, x, y, w, h, tail, o) {
    return p.poly(rrPts(x, y, w, h, Math.min(10, h / 3), tail), o);
  });

  /* Outline of an open hand, fingers up, thumb on the left, in the 140 x 110 box. */
  function handPts() {
    var pts = [[50, 102], [48, 84], [41, 75], [31, 65], [26, 57], [28, 51], [34, 50], [40, 56], [47, 66]];
    function finger(l, r, top, base) {
      var m = (l + r) / 2, hw = (r - l) / 2;
      pts.push([l, base]);
      for (var a = 180; a <= 360; a += 30) pts.push([m + Math.cos(rad(a)) * hw, top + hw + Math.sin(rad(a)) * hw]);
      pts.push([r, base]);
    }
    finger(51, 64, 22, 57); finger(66, 79, 14, 55); finger(81, 93, 20, 57); finger(95, 106, 34, 61);
    pts.push([105, 80], [100, 94], [98, 102]);
    return pts;
  }

  /* plate: opaque paper-light wash that hides lines behind it */
  function plate(C, o) { return copy({ fill: C['paper-light'], fillStyle: 'solid' }, o || {}); }
  var DASH = { dash: '4 5', passes: 1 };

  /* ================================================================== *
   * board: the 21 sketches that came from sketch-board. Same names, same
   * pictures; the German hand notes are gone. Text stays only where it is
   * part of the object ("{ }" on the laptop, "!" in the triangle).
   * ================================================================== */
  var P = parts;

  reg('board', 'bug-button', function (p, C) {
    shift(p, 0, 6, function () {
      p.rect(14, 30, 112, 52, { fill: C.signal });
      p.ellipse(70, 60, 26, 32, plate(C));
      p.circle(70, 40, 15, plate(C));
      p.line(70, 46, 70, 74);
      p.line(57, 52, 46, 46); p.line(57, 60, 44, 60); p.line(57, 68, 46, 74);
      p.line(83, 52, 94, 46); p.line(83, 60, 96, 60); p.line(83, 68, 94, 74);
      p.line(66, 34, 60, 26); p.line(74, 34, 80, 26);
    });
  });

  reg('board', 'people-risk', function (p, C) {
    P.person(p, 28, 42, C); P.person(p, 56, 34, C);
    p.poly([[76, 96], [90, 72], [104, 96]], { fill: C.signal });
    p.text(90, 93, '!', 'middle');
    P.magnifier(p, 58, 50, 20);
  });

  reg('board', 'cloud-person', function (p, C) {
    P.cloud(p, 70, 54, 108, { fill: C.signal });
    p.circle(70, 48, 18, plate(C));
    quad(p, 54, 76, 70, 56, 86, 76);
  });

  reg('board', 'clock-waves', function (p, C) {
    shift(p, 0, 4, function () {
      P.clock(p, 34, 44, 22);
      p.rect(70, 30, 20, 16, { fill: C.signal });
      p.rect(92, 52, 20, 16, { fill: C.signal });
      p.rect(114, 74, 20, 16, { fill: C.signal });
      quad(p, 58, 38, 64, 41, 68, 38);
    });
  });

  reg('board', 'folder-watch', function (p, C) {
    shift(p, 0, 2, function () {
      p.poly([[14, 40], [40, 40], [46, 48], [92, 48], [92, 92], [14, 92]], { fill: C.signal });
      P.magnifier(p, 96, 46, 18);
    });
  });

  reg('board', 'notebook-check', function (p, C) {
    p.rect(28, 20, 62, 76, plate(C));
    [30, 44, 58, 72, 86].forEach(function (y) { p.circle(28, y, 7); });
    p.line(42, 36, 80, 36); p.line(42, 50, 80, 50); p.line(42, 64, 70, 64);
    P.check(p, 84, 74, 36, C);
  });

  reg('board', 'key-speech', function (p, C) {
    p.circle(34, 64, 30, { fill: C.signal });
    p.circle(34, 64, 10, plate(C));
    p.line(49, 64, 112, 64, { width: 2.4 });
    p.line(98, 64, 98, 78); p.line(108, 64, 108, 75);
    P.bubble(p, 70, 12, 58, 28, { x: 88, tx: 82, ty: 50, hw: 6 }, plate(C));
    p.line(80, 22, 118, 22); p.line(80, 30, 108, 30);
  });

  reg('board', 'mail-checklist', function (p, C) {
    P.envelope(p, 12, 40, 76, 50, C);
    p.rect(92, 18, 36, 50, plate(C));
    P.check(p, 98, 34, 14, C); P.check(p, 98, 52, 14, C);
  });

  reg('board', 'dead-stop-button', function (p, C) {
    shift(p, 0, 4, function () {
      p.rect(34, 66, 60, 26);
      p.circle(64, 52, 42, { fill: C.remove });
      quad(p, 94, 80, 106, 82, 112, 72);
      quad(p, 120, 64, 126, 58, 132, 60);
    });
  });

  reg('board', 'linked-folders', function (p, C) {
    shift(p, 0, 8, function () {
      p.poly([[8, 34], [28, 34], [33, 40], [58, 40], [58, 76], [8, 76]], { fill: C.signal });
      p.poly([[82, 34], [102, 34], [107, 40], [132, 40], [132, 76], [82, 76]]);
      p.ellipse(62, 58, 22, 12, { width: 2.2 });
      p.ellipse(78, 58, 22, 12, { width: 2.2 });
    });
  });

  reg('board', 'crossed-slip', function (p, C) {
    shift(p, 0, 4, function () {
      p.rect(20, 34, 100, 42, plate(C));
      p.text(70, 60, 'FLAG=true', { anchor: 'middle', mono: true, size: 13 });
      p.line(26, 30, 114, 82, { stroke: C.remove, width: 3 });
      p.line(114, 30, 26, 82, { stroke: C.remove, width: 3 });
    });
  });

  reg('board', 'globe-search', function (p, C) {
    P.globe(p, 52, 50, 34, C);
    P.magnifier(p, 98, 70, 14);
  });

  reg('board', 'calendar-checks', function (p, C) {
    p.rect(20, 26, 96, 70, plate(C));
    p.line(20, 42, 116, 42, { width: 2.2 });
    p.line(40, 18, 40, 32); p.line(96, 18, 96, 32);
    P.check(p, 32, 62, 16, C); P.check(p, 60, 62, 16, C); P.check(p, 88, 62, 16, C);
  });

  reg('board', 'moving-box', function (p, C) {
    p.rect(8, 20, 30, 72); p.rect(102, 20, 30, 72, { fill: C.signal });
    p.rect(52, 58, 34, 28, plate(C));
    p.line(52, 68, 86, 68);
    quad(p, 46, 40, 70, 20, 94, 40);
    p.poly([[94, 40], [85, 38], [90, 31]], { fill: C.graphite, fillStyle: 'solid' });
  });

  reg('board', 'four-eyes', function (p, C) {
    [[36, 38], [60, 38], [80, 70], [104, 70]].forEach(function (q) {
      p.ellipse(q[0], q[1], 22, 14);
      p.dot(q[0] + 2, q[1], 6);
    });
  });

  reg('board', 'globe-download', function (p, C) {
    P.globe(p, 44, 50, 30, C);
    p.line(104, 16, 104, 64, { width: 2.4 });
    p.poly([[94, 56], [114, 56], [104, 70]], { fill: C.graphite, fillStyle: 'solid' });
    p.polyline([[86, 78], [86, 92], [122, 92], [122, 78]]);
  });

  reg('board', 'mail-bell', function (p, C) {
    P.envelope(p, 12, 40, 80, 50, C, { fill: C.signal });
    blob(p, [[116, 25], [127, 36], [128, 50], [133, 57], [99, 57], [104, 50], [105, 36]], plate(C));
    p.circle(116, 62, 6);
  });

  reg('board', 'speech-tag', function (p, C) {
    P.bubble(p, 12, 18, 86, 46, { x: 36, tx: 26, ty: 82, hw: 7 }, plate(C));
    p.line(24, 32, 84, 32); p.line(24, 44, 70, 44);
    p.poly([[80, 72], [120, 72], [132, 84], [120, 96], [80, 96]], { fill: C.signal });
    p.circle(122, 84, 5);
  });

  reg('board', 'two-servers-crown', function (p, C) {
    shift(p, 0, 2, function () {
      p.rect(22, 34, 36, 62, plate(C));
      p.rect(82, 34, 36, 62, plate(C));
      [48, 60, 72].forEach(function (y) { p.line(28, y, 52, y); p.line(88, y, 112, y); });
      p.poly([[24, 30], [30, 14], [40, 24], [50, 12], [56, 30]], { fill: C.signal });
    });
  });

  reg('board', 'gear-clock', function (p, C) {
    p.circle(48, 58, 44, { fill: C.signal });
    for (var i = 0; i < 8; i++) {
      var a = i * PI / 4;
      p.line(48 + Math.cos(a) * 22, 58 + Math.sin(a) * 22, 48 + Math.cos(a) * 30, 58 + Math.sin(a) * 30, { width: 3 });
    }
    p.circle(48, 58, 14, plate(C));
    P.clock(p, 108, 36, 16);
  });

  reg('board', 'laptop-wrench', function (p, C) {
    p.rect(26, 22, 72, 48, plate(C));
    p.poly([[16, 76], [108, 76], [118, 88], [6, 88]]);
    p.text(62, 52, '{ }', 'middle');
    p.circle(118, 34, 20);
    p.line(108, 46, 90, 70, { width: 4 });
  });

  /* ================================================================== *
   * business: money, goods, goals and the road between them
   * ================================================================== */

  /* plate under an accent: hides what is behind the shape, then colors it */
  function solid(p, pts, C, fill, o) {
    p.poly(pts, plate(C, o));
    if (fill) fillOnly(p, pts, { fill: fill });
  }

  reg('business', 'piggy-bank', function (p, C) {
    p.polyline([[42, 84], [42, 98], [55, 98], [55, 88]]);                      // legs behind the body
    p.polyline([[78, 88], [78, 98], [91, 98], [91, 84]]);
    p.ellipse(64, 62, 78, 52, { fill: C.rose });                                // body
    p.ellipse(108, 66, 15, 20, plate(C));                                      // snout
    p.dot(106, 62, 3); p.dot(110, 70, 3);
    p.poly([[80, 40], [90, 26], [98, 44]], plate(C));                          // ear
    p.dot(92, 56, 4.5);                                                         // eye
    p.curve([[27, 58], [18, 58], [14, 50], [20, 44], [25, 49]]);                // curly tail
    p.line(54, 38, 76, 37, { width: 2.6 });                                     // coin slot
    p.circle(66, 15, 15, plate(C));                                             // falling coin
    p.circle(66, 15, 8, { width: 1.1, passes: 1 });
  });

  /* a column of coins: sides and bottom in one stroke, ridges between the coins */
  function coinStack(p, C, cx, top, n, w, t, o) {
    var rx = w / 2, ry = w * 0.17, bot = top + n * t;
    p.polyline([[cx - rx, top]].concat(arcPts(cx, bot, rx, ry, 180, 0, 9), [[cx + rx, top]]));
    for (var k = 1; k < n; k++) arc(p, cx, top + k * t, rx, ry, 8, 172, { width: 1.2, passes: 1 });
    p.ellipse(cx, top, w, ry * 2, o);
  }
  reg('business', 'coin-stack', function (p, C) {
    coinStack(p, C, 40, 44, 4, 42, 12, { fill: C.yellow });
    coinStack(p, C, 92, 64, 3, 42, 12, plate(C));
    rot(p, 18, 92, 38, function () {                                            // a coin flipping above
      p.ellipse(92, 38, 11, 24, plate(C));
      p.line(92, 30, 92, 46, { width: 1.1, passes: 1 });
    });
  });

  reg('business', 'handshake', function (p, C) {
    p.rect(4, 30, 26, 42, plate(C));                                            // left cuff
    p.rect(110, 30, 26, 42, { fill: C.blue });                                  // right cuff
    blob(p, [[30, 40], [52, 33], [76, 35], [98, 41], [110, 42], [110, 62], [98, 68], [78, 77], [54, 72], [34, 63]], plate(C));
    fillOnly(p, dense([[30, 40], [52, 33], [76, 35], [98, 41], [110, 42], [110, 62], [98, 68], [78, 77], [54, 72], [34, 63]], true, 4), { fill: C.rose });
    p.curve([[48, 42], [62, 37], [80, 40], [90, 51]]);                          // the thumb over the hand
    p.path('M58 72 a5 5 0 0 0 10 0 M70 75 a5 5 0 0 0 10 0 M82 73 a5 5 0 0 0 10 0', { passes: 1, width: 1.4 });  // fingers
    p.curve([[40, 54], [52, 50], [64, 56]], { width: 1.1, passes: 1 });
  });

  reg('business', 'target-arrow', function (p, C) {
    p.circle(60, 60, 78);
    p.circle(60, 60, 52);
    p.circle(60, 60, 26, { fill: C.red });
    var ux = 0.76, uy = -0.65, nx = 0.65, ny = 0.76, ex = 114, ey = 18;            // arrow: shaft, then two vanes
    p.line(62, 58, ex, ey, { width: 2.2 });
    [1, -1].forEach(function (s) {
      var ax = ex - ux * 18, ay = ey - uy * 18, bx = ex - ux * 5, by = ey - uy * 5;
      p.poly([[ax, ay], [bx, by], [bx + nx * s * 9 + ux * 3, by + ny * s * 9 + uy * 3], [ax + nx * s * 9 - ux * 4, ay + ny * s * 9 - uy * 4]], plate(C, { width: 1.2 }));
    });
    sparkle(p, 20, 14, 5);
  });

  reg('business', 'trophy', function (p, C) {
    var bowl = arcPts(70, 20, 32, 46, 0, 180, 10);
    fillOnly(p, bowl, { fill: C.yellow });
    p.curve(bowl);
    p.line(38, 20, 102, 20, { width: 2.2 });                                    // rim
    arc(p, 42, 34, 14, 12, 95, 265);                                            // handles
    arc(p, 98, 34, 14, 12, -85, 85);
    p.line(70, 66, 70, 80);
    p.poly([[56, 80], [84, 80], [88, 90], [52, 90]], plate(C));
    p.rect(46, 90, 48, 9, plate(C));
    P.star(p, 70, 38, 10, 4.4, 5, { width: 1.3, passes: 1 });
  });

  reg('business', 'rocket', function (p, C) {
    xf(p, 'translate(70 56) rotate(36) scale(.86) translate(-70 -54)', function () {
      p.poly([[60, 72], [70, 100], [80, 72]], { fill: C.orange });                // flame
      p.poly([[55, 50], [38, 78], [56, 70]], plate(C));                            // fins
      p.poly([[85, 50], [102, 78], [84, 70]], plate(C));
      blob(p, [[70, 5], [82, 24], [86, 48], [84, 72], [56, 72], [54, 48], [58, 24]], plate(C));
      p.circle(70, 38, 17, plate(C));
      p.line(60, 62, 80, 62, { width: 1.2, passes: 1 });
    });
    sparkle(p, 22, 28, 6);
    sparkle(p, 116, 84, 5);
  });

  reg('business', 'megaphone', function (p, C) {
    p.poly([[44, 70], [58, 75], [54, 94], [42, 90]], plate(C));                  // grip
    p.poly([[12, 48], [32, 46], [32, 66], [12, 64]], plate(C));                  // mouthpiece
    p.poly([[32, 46], [88, 22], [88, 86], [32, 66]], { fill: C.orange });        // cone
    p.ellipse(88, 54, 14, 64, plate(C, { fillOpacity: 0.5 }));                   // rim
    arc(p, 92, 54, 22, 22, -36, 36);
    arc(p, 92, 54, 34, 34, -34, 34);
    arc(p, 92, 54, 46, 46, -32, 32);
  });

  reg('business', 'briefcase', function (p, C) {
    p.curve([[52, 40], [52, 28], [57, 22], [70, 20], [83, 22], [88, 28], [88, 40]], { width: 2 });   // handle
    rrect(p, 18, 38, 104, 60, 7, { fill: C.orange });
    p.line(18, 62, 122, 62);
    p.rect(62, 56, 16, 13, plate(C));
    p.dot(70, 63, 3.5);
    p.line(30, 46, 30, 54, { width: 1.1, passes: 1 });
  });

  reg('business', 'receipt', function (p, C) {
    p.poly([[34, 8], [106, 8], [106, 94], [99, 101], [92, 94], [85, 101], [78, 94], [71, 101], [64, 94], [57, 101], [50, 94], [43, 101], [34, 94]], plate(C));
    p.line(50, 20, 90, 20, { width: 2.4 });
    ticks(p, [[44, 34, 68, 34], [82, 34, 96, 34], [44, 44, 62, 44], [82, 44, 96, 44], [44, 54, 72, 54], [82, 54, 96, 54]], { width: 1.3 });
    p.line(44, 64, 96, 64, DASH);
    p.rect(42, 70, 56, 16, { fill: C.yellow });
    ticks(p, [[48, 78, 66, 78], [80, 78, 92, 78]], { width: 2 });
  });

  reg('business', 'invoice-stamp', function (p, C) {
    p.rect(10, 8, 78, 92, plate(C));
    p.line(20, 20, 54, 20, { width: 2.4 });
    P.lines(p, 20, 34, 56, 3, 9);
    rot(p, -13, 62, 78, function () {                                           // the impression in red pencil
      rrect(p, 36, 64, 52, 28, 5, { stroke: C.red, width: 2.2 });
      rrect(p, 40, 68, 44, 20, 3, { stroke: C.red, width: 1.2 });
      ticks(p, [[46, 76, 78, 76], [50, 82, 74, 82]], { stroke: C.red, width: 1.6 });
    });
    p.rect(100, 40, 12, 20, plate(C));                                          // the stamp, lifted
    p.rect(92, 60, 28, 9, plate(C));
    p.ellipse(106, 28, 26, 22, { fill: C.blue });
  });

  reg('business', 'price-tag', function (p, C) {
    rot(p, -16, 70, 56, function () {
      p.poly([[16, 56], [42, 28], [118, 28], [118, 84], [42, 84]], { fill: C.yellow });
      p.circle(36, 56, 9, plate(C));
      p.curve([[36, 56], [26, 44], [14, 34], [6, 32]], { width: 1.3 });
      p.line(58, 46, 102, 46, { width: 2.6 });
      p.line(58, 58, 92, 58);
      p.line(58, 70, 80, 70);
    });
  });

  reg('business', 'shop-front', function (p, C) {
    p.rect(20, 46, 100, 54, plate(C));
    p.poly([[22, 20], [118, 20], [128, 44], [116, 49], [104, 44], [92, 49], [80, 44], [68, 49], [56, 44], [44, 49], [32, 44], [12, 44]], { fill: C.orange });
    ticks(p, [[44, 20, 40, 44], [68, 20, 66, 44], [92, 20, 92, 44], [116, 20, 118, 44]], { width: 1.2 });
    p.rect(30, 62, 26, 38, plate(C));
    p.dot(50, 82, 3.5);
    p.rect(68, 60, 42, 28, plate(C));
    ticks(p, [[89, 60, 89, 88], [68, 74, 110, 74]], { width: 1.2 });
    p.line(8, 100, 132, 100);
  });

  reg('business', 'factory', function (p, C) {
    shift(p, 0, 3, function () {
      p.rect(12, 50, 78, 48, plate(C));
      p.poly([[12, 50], [12, 32], [38, 50], [38, 32], [64, 50], [64, 32], [90, 50]], { fill: C.blue });
      p.rect(90, 28, 14, 70, plate(C));
      p.rect(20, 64, 15, 13, plate(C));
      P.gear(p, 51, 72, 11, 8, { width: 1.3 });
      p.rect(67, 64, 15, 13, plate(C));
      p.circle(97, 19, 9); p.circle(106, 8, 12);
      p.line(4, 98, 134, 98);
    });
  });

  reg('business', 'truck', function (p, C) {
    p.rect(6, 26, 68, 54, { fill: C.yellow });
    p.poly([[74, 44], [98, 44], [118, 62], [118, 80], [74, 80]], plate(C));
    p.poly([[80, 50], [95, 50], [107, 62], [80, 62]], plate(C));
    p.line(4, 80, 120, 80);
    p.circle(28, 84, 21, plate(C)); p.dot(28, 84, 6);
    p.circle(96, 84, 21, plate(C)); p.dot(96, 84, 6);
    ticks(p, [[1, 38, 5, 38], [1, 50, 7, 50]], { width: 1.2 });
  });

  reg('business', 'pie-slice-hand', function (p, C) {
    // an open hand, palm up, fingers to the left: the raised hand turned on its side
    p.poly(handPts().map(function (q) { return [q[1] + 6, q[0] - 4]; }), plate(C));
    p.polyline([[108, 48], [136, 46]]);
    p.polyline([[108, 94], [136, 98]]);
    ticks(p, [[30, 54, 50, 54]], { width: 1.1 });
    var apex = [96, 46], sl = [apex].concat(arcPts(96, 46, 40, 40, -125, -55, 8));
    solid(p, sl, C, C.orange);
    arc(p, 96, 46, 31, 31, -123, -57, { width: 1.3, passes: 1 });                  // inner edge of the crust
    var cr = [];
    for (var a = -121; a <= -59; a += 8) cr.push([96 + Math.cos(rad(a)) * 31, 46 + Math.sin(rad(a)) * 31, 96 + Math.cos(rad(a)) * 40, 46 + Math.sin(rad(a)) * 40]);
    ticks(p, cr, { width: 1.2 });                                                 // the crimped crust
  });

  /* a leaf is a smooth loop from its base to its tip */
  function leaf(p, bx, by, tx, ty, wd, o) {
    var mx = (bx + tx) / 2, my = (by + ty) / 2, dx = tx - bx, dy = ty - by, len = Math.hypot(dx, dy) || 1, nx = -dy / len * wd, ny = dx / len * wd;
    blob(p, [[bx, by], [mx + nx, my + ny], [tx, ty], [mx - nx, my - ny]], o);
  }
  reg('business', 'growth-plant', function (p, C) {
    p.curve([[70, 70], [69, 56], [71, 42], [70, 26]], { width: 2 });
    leaf(p, 70, 60, 40, 48, 8); leaf(p, 70, 60, 100, 46, 8);
    leaf(p, 70, 44, 46, 28, 7); leaf(p, 70, 44, 94, 26, 7);
    leaf(p, 70, 30, 70, 8, 6);
    p.poly([[46, 78], [94, 78], [88, 102], [52, 102]], { fill: C.orange });
    p.rect(42, 70, 56, 10, plate(C));
  });

  reg('business', 'ladder-up', function (p, C) {
    p.circle(108, 28, 34, { fill: C.yellow });
    var lx = function (y) { return 34 + (102 - y) / 90 * 12; }, rx = function (y) { return 90 - (102 - y) / 90 * 12; };
    p.line(34, 102, 46, 12, { width: 2 });
    p.line(90, 102, 78, 12, { width: 2 });
    [28, 46, 64, 82].forEach(function (y) { p.line(lx(y), y, rx(y), y); });
    p.line(18, 103, 106, 103);
  });

  reg('business', 'bridge', function (p, C) {
    p.rect(6, 84, 128, 20, { fill: C.blue });
    p.rect(36, 26, 8, 62, plate(C)); p.rect(96, 26, 8, 62, plate(C));
    p.rect(5, 64, 130, 6, plate(C));
    quad(p, 40, 28, 70, 66, 100, 28);
    p.line(40, 28, 6, 62); p.line(100, 28, 134, 62);
    var hs = [];
    [52, 61, 70, 79, 88].forEach(function (x) {
      var t = (x - 40) / 60, y = (1 - t) * (1 - t) * 28 + 2 * (1 - t) * t * 66 + t * t * 28;
      hs.push([x, y + 1, x, 64]);
    });
    ticks(p, hs, { width: 1.1 });
  });

  reg('business', 'scale-balance', function (p, C) {
    p.poly([[46, 102], [94, 102], [86, 94], [54, 94]], plate(C));
    p.line(70, 94, 70, 30, { width: 2 });
    p.line(24, 38, 116, 24, { width: 2 });
    p.circle(70, 31, 9, plate(C));
    p.polyline([[10, 66], [24, 38], [38, 66]], { width: 1.2 });
    p.polyline([[100, 52], [116, 24], [132, 52]], { width: 1.2 });
    p.poly(arcPts(24, 66, 17, 9, 0, 180, 8), plate(C));
    p.poly(arcPts(116, 52, 17, 9, 0, 180, 8), plate(C));
    p.rect(15, 52, 18, 14, { fill: C.orange });
    p.circle(116, 44, 10);
  });

  reg('business', 'hourglass', function (p, C) {
    p.polyline([[38, 18], [38, 92]]); p.polyline([[102, 18], [102, 92]]);
    fillOnly(p, [[47, 36], [93, 36], [76, 52], [64, 52]], { fill: C.yellow });
    fillOnly(p, [[46, 90], [94, 90], [72, 68], [68, 68]], { fill: C.yellow });
    p.poly([[42, 18], [98, 18], [98, 32], [74, 54], [98, 76], [98, 90], [42, 90], [42, 76], [66, 54], [42, 32]]);
    p.line(70, 54, 70, 70, DASH);
    p.rect(32, 8, 76, 10, plate(C));
    p.rect(32, 90, 76, 10, plate(C));
  });

  reg('business', 'calendar-page', function (p, C) {
    p.rect(22, 20, 96, 80, plate(C));
    p.rect(22, 20, 96, 20, { fill: C.blue });
    ticks(p, [[46, 12, 46, 28], [94, 12, 94, 28]], { width: 2.6 });
    [56, 70, 84].forEach(function (y) { beads(p, 36, y, 104, y, 3.6, 17); });
    p.ellipse(70, 70, 19, 15, { stroke: C.red, width: 2 });
  });

  reg('business', 'signpost', function (p, C) {
    p.rect(62, 6, 12, 98, plate(C));
    solid(p, [[22, 16], [96, 16], [112, 29], [96, 42], [22, 42]], C, C.yellow);
    p.poly([[118, 50], [44, 50], [28, 63], [44, 76], [118, 76]], plate(C));
    ticks(p, [[32, 29, 82, 29], [52, 63, 100, 63]], { width: 1.4 });
    p.line(38, 104, 98, 104);
  });

  reg('business', 'crossroads', function (p, C) {
    p.rect(58, 43, 24, 24, { fill: C.yellow, passes: 0 });
    p.polyline([[4, 43], [58, 43], [58, 6]]);
    p.polyline([[136, 43], [82, 43], [82, 6]]);
    p.polyline([[4, 67], [58, 67], [58, 104]]);
    p.polyline([[136, 67], [82, 67], [82, 104]]);
    p.line(4, 55, 54, 55, DASH); p.line(86, 55, 136, 55, DASH); p.line(70, 6, 70, 40, DASH);
    p.curve([[70, 102], [70, 82], [74, 62], [92, 55], [126, 55]], { stroke: C.red, width: 2.2 });
    p.poly([[126, 55], [118, 50], [118, 60]], { fill: C.red, fillStyle: 'solid', stroke: C.red });
  });

  reg('business', 'flag-summit', function (p, C) {
    p.polyline([[6, 100], [42, 58], [57, 75]]);
    p.poly([[40, 100], [88, 30], [134, 100]], plate(C));
    p.polyline([[76, 48], [81, 52], [88, 44], [94, 52], [100, 48]]);
    p.line(88, 30, 88, 8, { width: 2 });
    p.poly([[88, 8], [112, 14], [88, 21]], { fill: C.red });
    ticks(p, [[100, 62, 108, 80], [110, 70, 116, 84]], { width: 1.2 });
  });

  /* ================================================================== *
   * people: figures, talk and thought
   * ================================================================== */

  /* Head and shoulders. s scales the figure, the body stops at `bottom`. */
  function bust(p, C, cx, cy, s, bottom, fill) {
    var hr = 11 * s, ny = cy + hr + 3 * s;
    var sh = [[cx - 26 * s, bottom], [cx - 23 * s, ny + 13 * s], [cx - 12 * s, ny + 3 * s], [cx, ny], [cx + 12 * s, ny + 3 * s], [cx + 23 * s, ny + 13 * s], [cx + 26 * s, bottom]];
    solid(p, dense(sh, false, 4), C, fill);
    p.circle(cx, cy, hr * 2, plate(C));
  }

  reg('people', 'person', function (p, C) {
    bust(p, C, 70, 32, 1.35, 100, C.blue);
    p.dot(64, 31, 3.4); p.dot(77, 31, 3.4);
    arc(p, 70, 36, 6.5, 4.5, 25, 155, { width: 1.3, passes: 1 });
  });

  reg('people', 'two-people-talk', function (p, C) {
    bust(p, C, 30, 66, 0.8, 102, null);
    bust(p, C, 110, 66, 0.8, 102, C.blue);
    P.bubble(p, 4, 6, 66, 36, { x: 28, tx: 26, ty: 53, hw: 6 }, { fill: C.yellow });
    P.lines(p, 14, 18, 46, 2, 10);
    P.bubble(p, 76, 20, 60, 28, { x: 108, tx: 110, ty: 54, hw: 6 }, plate(C));
    beads(p, 90, 34, 122, 34, 4, 14);
  });

  reg('people', 'team-of-three', function (p, C) {
    bust(p, C, 70, 30, 1.0, 100, C.blue);
    bust(p, C, 30, 48, 0.9, 100, null);
    bust(p, C, 110, 48, 0.9, 100, null);
    p.line(4, 100, 136, 100, { width: 1.2 });
  });

  reg('people', 'speech-bubbles', function (p, C) {
    P.bubble(p, 52, 8, 80, 48, { x: 106, tx: 116, ty: 74, hw: 7 }, { fill: C.blue });
    P.lines(p, 62, 22, 56, 2, 11);
    P.bubble(p, 8, 40, 76, 46, { x: 30, tx: 20, ty: 104, hw: 7 }, plate(C));
    beads(p, 28, 63, 66, 63, 5, 14);
  });

  reg('people', 'lightbulb-idea', function (p, C) {
    var rays = [];
    [-165, -135, -105, -75, -45, -15].forEach(function (a) {
      rays.push([70 + Math.cos(rad(a)) * 31, 42 + Math.sin(rad(a)) * 31, 70 + Math.cos(rad(a)) * 40, 42 + Math.sin(rad(a)) * 40]);
    });
    ticks(p, rays, { width: 1.8 });
    p.circle(70, 42, 48, { fill: C.yellow });
    p.line(59, 64, 61, 76); p.line(81, 64, 79, 76);
    p.rect(60, 76, 20, 11, plate(C));
    p.line(60, 82, 80, 82, { width: 1.2, passes: 1 });
    arc(p, 70, 87, 8, 4, 0, 180);
    p.curve([[62, 66], [62, 53], [70, 47], [78, 53], [78, 66]], { width: 1.4, passes: 1 });
  });

  reg('people', 'thought-cloud', function (p, C) {
    P.cloud(p, 72, 40, 112, { fill: C.blue });
    beads(p, 52, 38, 94, 38, 5, 14);
    p.circle(38, 80, 12, plate(C));
    p.circle(24, 92, 7, plate(C));
    p.circle(14, 100, 4, plate(C));
  });

  reg('people', 'raised-hand', function (p, C) {
    shift(p, 0, 2, function () {
      p.poly(handPts(), { fill: C.rose });
      p.curve([[58, 80], [70, 86], [90, 80]], { width: 1.2, passes: 1 });
      arc(p, 68, 56, 56, 50, 203, 232, { width: 1.3, passes: 1 });
      arc(p, 68, 56, 56, 50, -52, -23, { width: 1.3, passes: 1 });
    });
    sparkle(p, 18, 24, 5); sparkle(p, 122, 20, 6);
  });

  reg('people', 'heart', function (p, C) {
    function heart(cx, cy, s, o) {
      var pts = [];
      for (var i = 0; i < 28; i++) {
        var t = i / 28 * 2 * PI;
        pts.push([cx + 16 * Math.pow(Math.sin(t), 3) * s, cy - (13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t)) * s]);
      }
      blob(p, pts, o);
    }
    heart(68, 58, 2.3, { fill: C.red });
    heart(120, 20, 0.8, null);
    heart(18, 28, 0.65, null);
    ticks(p, [[112, 58, 122, 54], [114, 68, 126, 68], [20, 84, 28, 80]], { width: 1.4 });
  });

  reg('people', 'eye', function (p, C) {
    quad(p, 10, 56, 70, 4, 130, 56);
    quad(p, 10, 56, 70, 108, 130, 56);
    p.circle(70, 56, 32, { fill: C.blue });
    p.dot(70, 56, 15);
    p.circle(63, 49, 7, plate(C, { fillOpacity: 1 }));
    ticks(p, [[40, 30, 34, 20], [56, 24, 52, 12], [70, 22, 70, 10], [84, 24, 88, 12], [100, 30, 106, 20]], { width: 1.7 });
  });

  reg('people', 'ear-listen', function (p, C) {
    var ear = [[56, 96], [42, 86], [38, 60], [46, 30], [66, 14], [92, 22], [100, 46], [92, 68], [80, 80], [76, 94], [66, 100]].map(function (q) { return [q[0] + 14, q[1]]; });
    blob(p, ear, { fill: C.rose });
    p.curve([[78, 36], [96, 38], [102, 54], [92, 66], [82, 60], [86, 50], [94, 52]].map(function (q) { return [q[0] + 0, q[1]]; }), { width: 1.4 });
    p.curve([[78, 62], [72, 70], [80, 76]], { width: 1.3, passes: 1 });
    [18, 29, 40].forEach(function (r) { arc(p, 2, 56, r, r + 4, -34, 34, { width: 1.8 }); });
  });

  /* ================================================================== *
   * tech: machines, networks and the people who fix them
   * ================================================================== */

  reg('tech', 'laptop', function (p, C) {
    p.rect(26, 12, 88, 62, plate(C));
    p.rect(32, 18, 76, 50, { width: 1.2, passes: 1 });
    P.lines(p, 40, 28, 40, 3, 9);
    p.rect(40, 50, 30, 12, { fill: C.blue });
    p.poly([[10, 80], [130, 80], [120, 96], [20, 96]], plate(C));
    p.line(56, 85, 84, 85, { width: 1.2, passes: 1 });
    p.line(26, 74, 114, 74);
  });

  reg('tech', 'phone', function (p, C) {
    rrect(p, 42, 5, 56, 100, 9, plate(C));
    p.rect(48, 18, 44, 66, { width: 1.2, passes: 1 });
    p.line(62, 11, 78, 11, { width: 2 });
    p.circle(70, 94, 7);
    p.rect(54, 26, 16, 16, { fill: C.blue });
    p.rect(74, 26, 12, 16);
    ticks(p, [[54, 52, 86, 52], [54, 60, 80, 60], [54, 68, 68, 68]], { width: 1.3 });
  });

  reg('tech', 'server-rack', function (p, C) {
    P.box3d(p, 22, 18, 70, 84, 24, plate(C));
    [26, 50, 74].forEach(function (y, i) {
      p.rect(28, y, 58, 20, i === 1 ? { fill: C.blue } : plate(C));
      p.dot(37, y + 10, 5);
      ticks(p, [[50, y + 7, 80, y + 7], [50, y + 13, 80, y + 13]], { width: 1.2 });
    });
    ticks(p, [[30, 102, 30, 106], [84, 102, 84, 106]], { width: 2.4 });
  });

  reg('tech', 'database-cylinders', function (p, C) {
    var cx = 70, rx = 34, ry = 10;
    p.polyline([[cx - rx, 24]].concat(arcPts(cx, 90, rx, ry, 180, 0, 10), [[cx + rx, 24]]));
    arc(p, cx, 47, rx, ry, 6, 174, { width: 1.5 });
    arc(p, cx, 68, rx, ry, 6, 174, { width: 1.5 });
    p.ellipse(cx, 24, rx * 2, ry * 2, { fill: C.blue });
    [37, 58, 80].forEach(function (y) { p.dot(51, y, 5); });
    ticks(p, [[62, 38, 90, 38], [62, 59, 90, 59], [62, 81, 90, 81]], { width: 1.3 });
  });

  reg('tech', 'cloud-upload', function (p, C) {
    P.cloud(p, 70, 44, 108, { fill: C.blue });
    p.polyline([[34, 86], [34, 100], [106, 100], [106, 86]]);
    p.arrow(70, 94, 70, 50, { bend: 0, width: 2.4, head: 14 });
    p.circle(48, 78, 6); p.circle(94, 72, 5);
  });

  reg('tech', 'lock', function (p, C) {
    p.curve([[50, 52], [50, 34], [58, 21], [70, 17], [82, 21], [90, 34], [90, 52]], { width: 2.4 });
    rrect(p, 32, 50, 76, 54, 8, { fill: C.yellow });
    p.dot(70, 72, 11);
    p.poly([[67, 76], [73, 76], [75, 92], [65, 92]], { fill: C.graphite, fillStyle: 'solid' });
    p.line(41, 60, 41, 94, { width: 1.1, passes: 1 });
  });

  reg('tech', 'key', function (p, C) {
    rot(p, -26, 70, 55, function () {
      p.circle(26, 55, 38, { fill: C.yellow });
      p.circle(26, 55, 15, plate(C));
      p.rect(44, 51, 78, 9, plate(C));
      p.poly([[98, 60], [98, 74], [107, 74], [107, 60]], plate(C));
      p.poly([[112, 60], [112, 70], [121, 70], [121, 60]], plate(C));
      p.line(54, 51, 54, 60, { width: 1.2, passes: 1 });
    });
  });

  reg('tech', 'shield-check', function (p, C) {
    var pts = [[70, 8], [112, 22]].concat(quadPts(112, 50, 106, 86, 70, 102, 8), quadPts(70, 102, 34, 86, 28, 50, 8).slice(1), [[28, 22]]);
    p.poly(pts, { fill: C.blue });
    p.poly(pts.map(function (q) { return [70 + (q[0] - 70) * 0.8, 56 + (q[1] - 56) * 0.8]; }), { width: 1.1, passes: 1, dash: '4 5' });
    p.polyline([[48, 56], [64, 73], [94, 36]], { stroke: C.green, width: 4.5 });
    sparkle(p, 124, 16, 5); sparkle(p, 14, 70, 4);
  });

  reg('tech', 'gear-pair', function (p, C) {
    P.gear(p, 48, 60, 32, 10, { turn: 18 });
    P.gear(p, 98, 38, 22, 8, { fill: C.yellow, turn: 5 });
    arc(p, 48, 60, 40, 40, 200, 250, { width: 1.3, passes: 1 });
    arc(p, 98, 38, 29, 29, -60, -10, { width: 1.3, passes: 1 });
  });

  reg('tech', 'robot-head', function (p, C) {
    p.line(70, 28, 70, 13, { width: 2 });
    p.circle(70, 9, 9, plate(C));
    p.rect(18, 46, 14, 24, plate(C)); p.rect(108, 46, 14, 24, plate(C));
    rrect(p, 30, 28, 80, 66, 10, { fill: C.blue });
    p.circle(52, 54, 19, plate(C)); p.circle(88, 54, 19, plate(C));
    p.dot(54, 55, 8); p.dot(90, 55, 8);
    p.rect(52, 76, 36, 10, plate(C));
    ticks(p, [[61, 76, 61, 86], [70, 76, 70, 86], [79, 76, 79, 86]], { width: 1.2 });
  });

  reg('tech', 'chip', function (p, C) {
    var segs = [];
    [50, 60, 70, 80, 90].forEach(function (x) { segs.push([x, 10, x, 28], [x, 82, x, 100]); });
    [36, 46, 56, 66, 76].forEach(function (y) { segs.push([20, y, 38, y], [102, y, 120, y]); });
    ticks(p, segs, { width: 2.2 });
    p.rect(38, 28, 64, 54, plate(C));
    p.rect(45, 34, 50, 42, { width: 1.1, passes: 1 });
    p.rect(52, 41, 36, 28, { fill: C.violet });
    p.dot(48, 38, 4);
  });

  reg('tech', 'plug-socket', function (p, C) {
    p.curve([[10, 60], [4, 72], [8, 88], [24, 98]], { width: 2.2 });
    p.rect(8, 52, 10, 16, plate(C));
    rrect(p, 16, 38, 44, 44, 7, { fill: C.orange });
    p.rect(60, 46, 17, 7, plate(C)); p.rect(60, 67, 17, 7, plate(C));
    rrect(p, 94, 24, 40, 70, 7, plate(C));
    p.rect(104, 42, 6, 16); p.rect(118, 42, 6, 16);
    p.circle(114, 76, 8);
    ticks(p, [[80, 44, 85, 38], [82, 56, 88, 56], [80, 70, 85, 76]], { width: 1.4 });
  });

  reg('tech', 'wifi-waves', function (p, C) {
    [20, 36, 52, 68].forEach(function (r) { arc(p, 70, 90, r, r, -137, -43, { width: 2.2 }); });
    p.circle(70, 90, 13, { fill: C.blue });
  });

  reg('tech', 'bug', function (p, C) {
    ticks(p, [[54, 56, 38, 46], [53, 66, 34, 66], [54, 76, 38, 88]], { width: 1.8 });
    ticks(p, [[86, 56, 102, 46], [87, 66, 106, 66], [86, 76, 102, 88]], { width: 1.8 });
    p.ellipse(70, 66, 36, 46, { fill: C.red });
    p.line(70, 44, 70, 89);
    p.circle(70, 36, 20, plate(C));
    quad(p, 63, 28, 58, 14, 48, 10);
    quad(p, 77, 28, 82, 14, 92, 10);
    p.circle(60, 62, 8, plate(C)); p.circle(81, 72, 7, plate(C));
  });

  reg('tech', 'terminal-prompt', function (p, C) {
    rrect(p, 10, 12, 120, 86, 6, plate(C));
    p.line(10, 30, 130, 30);
    p.dot(21, 21, 5); p.dot(33, 21, 5); p.dot(45, 21, 5);
    p.polyline([[24, 46], [38, 56], [24, 66]], { width: 2.6 });
    p.rect(46, 62, 18, 7, { fill: C.yellow });
    ticks(p, [[46, 46, 100, 46], [24, 82, 76, 82]], { width: 1.4 });
  });

  reg('tech', 'api-plugs', function (p, C) {
    rrect(p, 4, 34, 52, 46, 6, { fill: C.violet });
    p.text(30, 63, '{ }', { anchor: 'middle', mono: true, size: 17 });
    ticks(p, [[56, 49, 74, 49], [56, 65, 74, 65]], { width: 2.6 });
    rrect(p, 84, 34, 52, 46, 6, plate(C));
    p.circle(92, 49, 7); p.circle(92, 65, 7);
    P.lines(p, 104, 46, 24, 3, 9);
    p.arrow(34, 24, 106, 24, { bend: -0.32, width: 1.4 });
    p.arrow(106, 92, 34, 92, { bend: -0.32, width: 1.4 });
  });

  reg('tech', 'magnifier-doc', function (p, C) {
    p.poly([[22, 8], [72, 8], [86, 22], [86, 98], [22, 98]], plate(C));
    p.polyline([[72, 8], [72, 22], [86, 22]]);
    P.lines(p, 32, 34, 44, 4, 11);
    p.circle(90, 66, 44, { fill: C.yellow, passes: 0, fillOpacity: 0.7 });
    P.magnifier(p, 90, 66, 22);
  });

  /* ================================================================== *
   * teaching: the classroom, the lab and the map
   * ================================================================== */

  reg('teaching', 'open-book', function (p, C) {
    shift(p, 0, -4, function () {
      p.polyline([[10, 22], [10, 94], [70, 106], [130, 94], [130, 22]]);
      p.poly([[70, 28], [16, 16], [16, 88], [70, 100]], plate(C));
      p.poly([[70, 28], [124, 16], [124, 88], [70, 100]], plate(C));
      P.lines(p, 28, 38, 34, 4, 12);
      P.lines(p, 82, 38, 32, 3, 12);
      p.poly([[63, 98], [77, 98], [77, 110], [70, 105], [63, 110]], { fill: C.orange });
    });
  });

  reg('teaching', 'graduation-cap', function (p, C) {
    p.poly([[36, 50], [36, 72]].concat(quadPts(36, 72, 70, 100, 104, 72, 8), [[104, 50]]), plate(C));
    solid(p, [[70, 14], [132, 40], [70, 66], [8, 40]], C, C.violet);
    p.dot(70, 40, 6);
    p.curve([[70, 40], [98, 48], [118, 50]], { width: 1.4, passes: 1 });
    p.line(118, 50, 118, 72);
    p.poly([[112, 72], [124, 72], [126, 88], [110, 88]], plate(C));
  });

  reg('teaching', 'pencil', function (p, C) {
    p.curve([[24, 94], [34, 100], [42, 90], [52, 101], [62, 91], [74, 101], [88, 92]], { width: 1.4, passes: 1 });
    rot(p, -34, 70, 55, function () {
      p.rect(32, 46, 68, 18, { fill: C.yellow });
      p.line(32, 55, 100, 55, { width: 1.1, passes: 1 });
      p.rect(100, 46, 9, 18, plate(C));
      p.rect(109, 46, 15, 18, plate(C));
      p.poly([[32, 46], [10, 55], [32, 64]], plate(C));
      p.poly([[10, 55], [19, 51], [19, 59]], { fill: C.graphite, fillStyle: 'solid' });
    });
  });

  reg('teaching', 'ruler-triangle', function (p, C) {
    p.poly([[12, 98], [12, 12], [98, 98]], { fill: C.yellow });
    p.poly([[30, 86], [30, 44], [72, 86]], plate(C));
    var segs = [];
    for (var y = 20; y <= 90; y += 7) segs.push([12, y, ((y - 20) % 35 === 0) ? 24 : 18, y]);
    ticks(p, segs, { width: 1.2 });
    p.rect(56, 8, 78, 22, plate(C));
    var t = [];
    for (var x = 62; x <= 128; x += 6) t.push([x, 30, x, ((x - 62) % 24 === 0) ? 20 : 25]);
    ticks(p, t, { width: 1.2 });
    arc(p, 98, 98, 18, 18, 180, 225, { width: 1.3, passes: 1 });
  });

  reg('teaching', 'microscope', function (p, C) {
    p.rect(26, 92, 80, 12, plate(C));
    p.curve([[92, 92], [106, 82], [108, 60], [98, 42], [82, 32]], { width: 2.6 });
    xf(p, 'translate(0 7) rotate(-20 70 40)', function () {
      p.rect(62, 8, 20, 46, { fill: C.blue });
      p.rect(65, 0, 14, 8, plate(C));
      p.rect(67, 54, 10, 10, plate(C));
    });
    p.line(40, 78, 96, 78, { width: 3 });
    p.rect(54, 72, 28, 6, plate(C));
    p.line(66, 78, 66, 92, { width: 1.3, passes: 1 });
  });

  reg('teaching', 'flask', function (p, C) {
    fillOnly(p, [[43.6, 64], [96.4, 64], [112, 92], [28, 92]], { fill: C.blue });
    p.polyline([[58, 12], [58, 38], [28, 92], [112, 92], [82, 38], [82, 12]], { width: 2 });
    p.line(50, 12, 90, 12, { width: 2.4 });
    p.curve([[44, 64], [56, 61], [70, 65], [84, 61], [96, 64]], { width: 1.4, passes: 1 });
    p.circle(62, 78, 8, plate(C)); p.circle(80, 84, 6, plate(C)); p.circle(74, 72, 4, plate(C));
    ticks(p, [[58, 24, 66, 24], [58, 30, 64, 30]], { width: 1.2 });
  });

  reg('teaching', 'atom', function (p, C) {
    [0, 60, 120].forEach(function (a) { rot(p, a, 70, 55, function () { p.ellipse(70, 55, 100, 34); }); });
    p.circle(70, 55, 16, { fill: C.orange });
    [[0, 35], [60, 160], [120, 280]].forEach(function (e) {
      var al = rad(e[0]), t = rad(e[1]), ex = 50 * Math.cos(t), ey = 17 * Math.sin(t);
      p.dot(70 + ex * Math.cos(al) - ey * Math.sin(al), 55 + ex * Math.sin(al) + ey * Math.cos(al), 8, { fill: C.graphite });
    });
  });

  reg('teaching', 'brain', function (p, C) {
    p.poly([[66, 76], [70, 100], [84, 98], [82, 78]], plate(C));
    blob(p, [[38, 68], [24, 56], [22, 40], [32, 27], [50, 19], [72, 15], [94, 19], [110, 29], [116, 46], [110, 62], [96, 70], [86, 80], [72, 82], [64, 74], [52, 74]], { fill: C.violet });
    p.curve([[46, 28], [56, 38], [50, 50], [58, 62]], { width: 1.4 });
    p.curve([[70, 20], [78, 34], [68, 44], [78, 56], [72, 68]], { width: 1.4 });
    p.curve([[92, 26], [86, 38], [98, 46], [92, 60]], { width: 1.4 });
    p.curve([[30, 48], [42, 52], [38, 64]], { width: 1.4 });
    p.curve([[106, 40], [100, 48], [106, 58]], { width: 1.4 });
  });

  reg('teaching', 'globe-stand', function (p, C) {
    p.ellipse(70, 100, 46, 11, plate(C));
    p.line(70, 82, 70, 95, { width: 2.2 });
    p.circle(70, 44, 78, { width: 1.8 });
    p.circle(70, 44, 56, { fill: C.blue });
    p.ellipse(70, 44, 24, 56);
    arc(p, 70, 44, 28, 7, 8, 172, { width: 1.5 });
    blob(p, [[54, 30], [64, 26], [72, 34], [66, 46], [56, 44]], plate(C, { width: 1.3 }));
    blob(p, [[80, 52], [90, 50], [92, 62], [84, 64]], plate(C, { width: 1.3 }));
  });

  reg('teaching', 'compass', function (p, C) {
    p.circle(70, 55, 90);
    p.circle(70, 55, 74, { width: 1.2 });
    var t = [];
    for (var i = 0; i < 16; i++) { var a = i * PI / 8, r0 = i % 4 === 0 ? 33 : 37; t.push([70 + Math.cos(a) * r0, 55 + Math.sin(a) * r0, 70 + Math.cos(a) * 44, 55 + Math.sin(a) * 44]); }
    ticks(p, t, { width: 1.3 });
    p.poly([[70, 20], [60, 55], [80, 55]], { fill: C.red });
    p.poly([[60, 55], [80, 55], [70, 90]], plate(C));
    p.dot(70, 55, 7, { fill: C.graphite });
  });

  reg('teaching', 'map-pin', function (p, C) {
    p.ellipse(70, 101, 50, 10, DASH);
    p.curve([[8, 92], [20, 80], [32, 94], [44, 84]], { width: 1.3, dash: '3 5', passes: 1 });
    p.poly(arcPts(70, 40, 26, 26, 128, 412, 14).concat([[70, 98]]), { fill: C.red });
    p.circle(70, 40, 18, plate(C));
    ticks(p, [[106, 90, 116, 100], [116, 90, 106, 100]], { width: 1.8 });
  });

  reg('teaching', 'light-switch', function (p, C) {
    rrect(p, 36, 6, 68, 98, 7, plate(C));
    p.rect(59, 30, 22, 50, plate(C));
    p.rect(59, 30, 22, 26, { fill: C.yellow });
    p.dot(70, 17, 6); p.dot(70, 93, 6);
    ticks(p, [[112, 24, 126, 18], [114, 38, 130, 38], [112, 52, 126, 58]], { width: 1.8 });
    ticks(p, [[28, 24, 14, 18], [26, 38, 10, 38], [28, 52, 14, 58]], { width: 1.8 });
  });

  reg('teaching', 'abacus', function (p, C) {
    p.rect(10, 12, 120, 86, plate(C));
    [34, 55, 76].forEach(function (y) { p.line(18, y, 122, y, { width: 1.5 }); });
    var B = { stroke: C.orange, width: 10 };
    beads(p, 28, 34, 52, 34, 10, 12, B); beads(p, 98, 34, 111, 34, 10, 12, B);
    beads(p, 28, 55, 29, 55, 10, 12, B); beads(p, 76, 55, 112, 55, 10, 12, B);
    beads(p, 28, 76, 65, 76, 10, 12, B); beads(p, 110, 76, 111, 76, 10, 12, B);
    p.line(10, 98, 130, 98, { width: 2.4 });
  });

  reg('teaching', 'chalkboard', function (p, C) {
    ticks(p, [[24, 86, 14, 106], [116, 86, 126, 106]], { width: 2.2 });
    p.rect(6, 6, 128, 80, plate(C));
    p.rect(12, 12, 116, 68, { fill: C.blue });
    p.poly([[22, 68], [22, 34], [54, 68]], plate(C, { fillOpacity: 0.6 }));
    ticks(p, [[22, 60, 30, 60], [30, 60, 30, 68]], { width: 1.2 });
    ticks(p, [[66, 28, 116, 28], [66, 40, 102, 40], [66, 52, 112, 52]], { width: 1.5 });
    p.line(6, 92, 134, 92, { width: 2 });
    p.rect(92, 87, 14, 5, plate(C));
  });

  /* ================================================================== *
   * postal: the house motif. Letters, parcels and the sky they cross.
   * ================================================================== */

  reg('postal', 'envelope', function (p, C) {
    p.rect(12, 22, 116, 70, plate(C));
    p.polyline([[12, 22], [70, 64], [128, 22]]);
    p.line(12, 92, 56, 54, { width: 1.3, passes: 1 });
    p.line(128, 92, 84, 54, { width: 1.3, passes: 1 });
    p.circle(70, 66, 20, { fill: C.red });
    p.circle(70, 66, 9, { width: 1.2, passes: 1 });
  });

  reg('postal', 'parcel-string', function (p, C) {
    var b = P.box3d(p, 16, 40, 74, 54, 24, { fill: C.orange });
    p.line(53, 40, 53, 94, { width: 2 });
    p.line(53, 40, 53 + b.dx / 2 + 2, 40 + b.dy / 2 - 1, { width: 2 });
    p.line(16, 66, 90, 66, { width: 1.6 });
    p.line(90, 66, 90 + b.dx, 66 + b.dy, { width: 1.6 });
    blob(p, [[60, 31], [50, 22], [41, 26], [44, 34], [53, 35]], plate(C, { width: 1.4 }));
    blob(p, [[60, 31], [70, 22], [79, 26], [76, 34], [67, 35]], plate(C, { width: 1.4 }));
    p.dot(60, 32, 5);
    p.rect(60, 72, 22, 16, plate(C));
    ticks(p, [[64, 78, 78, 78], [64, 83, 74, 83]], { width: 1.2 });
  });

  reg('postal', 'postage-stamp', function (p, C) {
    S.postage(p, 22, 10, 62, 82, {
      paper: C.cream, tint: C.blue,
      inner: function (pp, b) {
        pp.circle(b.x + b.w * 0.5, b.y + b.h * 0.4, b.w * 0.5, { fill: C.yellow });
        pp.polyline([[b.x + 3, b.y + b.h * 0.8], [b.x + b.w * 0.35, b.y + b.h * 0.66], [b.x + b.w * 0.6, b.y + b.h * 0.8], [b.x + b.w - 3, b.y + b.h * 0.7]]);
      }
    });
    S.postmark(p, 94, 70, 20, '', '', { color: C.graphite, opacity: 0.85 });
    S.cancelWaves(p, 74, 32, 60, { lines: 3, scale: 0.6, color: C.graphite, opacity: 0.8 });
  });

  reg('postal', 'postcard', function (p, C) {
    rot(p, -5, 70, 55, function () {
      p.rect(8, 16, 124, 80, plate(C));
      p.rect(16, 24, 56, 64);
      p.circle(46, 44, 17, { fill: C.yellow });
      p.polyline([[16, 80], [32, 62], [46, 76], [58, 58], [72, 74]]);
      p.line(80, 26, 80, 86, { width: 1.3, passes: 1 });
      p.rect(106, 24, 20, 24, plate(C));
      p.curve([[84, 32], [90, 26], [96, 34], [100, 28]], { width: 1.3, passes: 1 });
      ticks(p, [[86, 62, 124, 62], [86, 72, 124, 72], [86, 82, 114, 82]], { width: 1.3 });
    });
  });

  reg('postal', 'mailbox', function (p, C) {
    p.rect(60, 70, 12, 34, plate(C));
    p.line(34, 104, 98, 104);
    p.poly([[14, 72], [14, 56]].concat(arcPts(60, 56, 46, 22, 180, 360, 10), [[106, 72]]), plate(C));
    p.ellipse(106, 64, 12, 36, plate(C));
    p.dot(106, 64, 4);
    p.line(30, 70, 30, 18, { width: 2 });
    p.poly([[30, 18], [56, 18], [56, 32], [30, 32]], { fill: C.red });
    p.poly([[88, 44], [100, 38], [102, 50], [90, 56]], plate(C, { width: 1.1 }));
  });

  reg('postal', 'planet-ringed', function (p, C) {
    rot(p, -18, 70, 56, function () {
      arc(p, 70, 56, 66, 17, 180, 360, { width: 1.6 });
      arc(p, 70, 56, 55, 13, 180, 360, { width: 1.2, passes: 1 });
    });
    p.circle(70, 56, 52, plate(C));
    fillOnly(p, arcPts(70, 56, 26, 26, 0, 360, 24), { fill: C.orange });
    p.curve([[46, 46], [70, 50], [94, 46]], { width: 1.1, passes: 1 });
    p.curve([[45, 64], [70, 69], [95, 64]], { width: 1.1, passes: 1 });
    rot(p, -18, 70, 56, function () {
      arc(p, 70, 56, 66, 17, 0, 180, { width: 1.6 });
      arc(p, 70, 56, 55, 13, 0, 180, { width: 1.2, passes: 1 });
    });
    sparkle(p, 18, 20, 5); sparkle(p, 122, 96, 5);
  });

  reg('postal', 'satellite', function (p, C) {
    rot(p, -30, 70, 55, function () {
      p.line(70, 40, 70, 28);
      p.circle(70, 24, 8, plate(C));
      p.line(50, 55, 58, 55, { width: 2 }); p.line(82, 55, 90, 55, { width: 2 });
      p.rect(8, 42, 42, 26, plate(C)); p.rect(90, 42, 42, 26, plate(C));
      ticks(p, [[22, 42, 22, 68], [36, 42, 36, 68], [8, 55, 50, 55], [104, 42, 104, 68], [118, 42, 118, 68], [90, 55, 132, 55]], { width: 1.1 });
      p.rect(58, 40, 24, 30, { fill: C.yellow });
      p.poly(arcPts(70, 72, 13, 9, 0, 180, 8), plate(C));
    });
    arc(p, 84, 76, 16, 16, 15, 70, { width: 1.4, passes: 1 });
    arc(p, 84, 76, 26, 26, 15, 70, { width: 1.4, passes: 1 });
    sparkle(p, 20, 90, 4);
  });

  reg('postal', 'telescope', function (p, C) {
    ticks(p, [[60, 66, 34, 104], [64, 68, 62, 104], [68, 66, 92, 104]], { width: 2.2 });
    rot(p, -24, 66, 52, function () {
      p.poly([[12, 46], [36, 43], [100, 32], [100, 70], [36, 59], [12, 56]], { fill: C.blue });
      ticks(p, [[36, 43, 36, 59], [68, 38, 68, 64]], { width: 1.4 });
      p.ellipse(100, 51, 9, 38, plate(C, { fillOpacity: 0.6 }));
      p.rect(4, 47, 9, 8, plate(C));
    });
    p.circle(63, 64, 9, plate(C));
    sparkle(p, 116, 16, 6); sparkle(p, 24, 22, 4);
  });

  reg('postal', 'star-sparkle', function (p, C) {
    P.star(p, 68, 58, 42, 18, 5, { fill: C.yellow });
    sparkle(p, 18, 26, 9); sparkle(p, 122, 30, 7); sparkle(p, 116, 94, 9);
    p.dot(24, 84, 4); p.dot(124, 62, 3);
  });

  reg('postal', 'comet', function (p, C) {
    var hx = 100, hy = 36, dx = -0.74, dy = 0.67, nx = 0.67, ny = 0.74;
    [-14, -7, 0, 7, 14].forEach(function (s) {
      var L = 104 - Math.abs(s) * 2.4, sp = s * (1 + L / 70);
      var mx = hx + dx * L * 0.5 + nx * s * 1.3, my = hy + dy * L * 0.5 + ny * s * 1.3;
      p.curve([[hx + dx * 10 + nx * s, hy + dy * 10 + ny * s], [mx, my], [hx + dx * L + nx * sp, hy + dy * L + ny * sp]], { width: s === 0 ? 1.8 : 1.3, passes: 1 });
    });
    p.circle(hx, hy, 36, { fill: C.yellow });
    p.dot(93, 31, 5); p.dot(107, 44, 4);
    sparkle(p, 26, 16, 6); sparkle(p, 124, 92, 5);
  });

  reg('postal', 'moon-phases', function (p, C) {
    var R = 12.5;
    [[15, 1, 62], [42, 0.5, 52], [70, 0, 48], [98, -0.5, 52], [125, -1, 62]].forEach(function (m) {
      var cx = m[0], k = m[1], cy = m[2], dark = [];
      if (k > -1) {
        dark = arcPts(cx, cy, R, R, 270, 90, 8);
        for (var a = 90; a >= -90; a -= 22.5) dark.push([cx + R * k * Math.cos(rad(a)), cy + R * Math.sin(rad(a))]);
        fillOnly(p, dark, { fill: C.blue, gap: 2 });
      }
      p.circle(cx, cy, R * 2);
    });
    sparkle(p, 30, 26, 6); sparkle(p, 106, 24, 5); sparkle(p, 70, 90, 6);
  });

  /* ================================================================== *
   * health and life science: the lab bench, the body and the leaf
   * ================================================================== */
  var HL = 'health and life science';

  reg(HL, 'syringe', function (p, C) {
    rot(p, -32, 70, 55, function () {
      p.line(22, 55, 3, 55, { width: 1.4 });                                     // needle
      p.poly([[30, 50], [21, 52], [21, 58], [30, 60]], plate(C));                // hub
      p.rect(30, 45, 58, 20, plate(C));                                          // barrel
      p.rect(34, 48, 38, 14, { fill: C.blue, passes: 0 });                       // the dose
      ticks(p, [[44, 45, 44, 51], [54, 45, 54, 50], [64, 45, 64, 51], [74, 45, 74, 50]], { width: 1.2 });
      p.line(88, 55, 114, 55, { width: 2.4 });                                   // plunger rod
      p.rect(112, 43, 6, 24, plate(C));                                          // thumb rest
      p.line(88, 41, 88, 69, { width: 2.6 });                                    // finger flange
    });
    p.circle(15, 98, 6, plate(C));
  });

  reg(HL, 'virus', function (p, C) {
    var d = '';
    for (var k = 0; k < 12; k++) {
      var a = rad(k * 30 + 15), c = Math.cos(a), s = Math.sin(a), hx = 70 + c * 40, hy = 55 + s * 40;
      d += 'M' + (70 + c * 24).toFixed(1) + ' ' + (55 + s * 24).toFixed(1) + 'L' + (70 + c * 36).toFixed(1) + ' ' + (55 + s * 36).toFixed(1) +
        'M' + (hx - 3.6).toFixed(1) + ' ' + hy.toFixed(1) + 'a3.6 3.6 0 1 0 7.2 0a3.6 3.6 0 1 0 -7.2 0';
    }
    p.path(d, { passes: 1, width: 1.7 });                                        // spikes with round heads
    p.circle(70, 55, 52, { fill: C.orange });
    p.circle(58, 46, 11, plate(C)); p.circle(82, 52, 9, plate(C)); p.circle(66, 69, 10, plate(C));
    p.curve([[56, 44], [60, 48], [58, 52]], { width: 1.2, passes: 1 });
  });

  reg(HL, 'bacterium', function (p, C) {
    rot(p, -15, 74, 55, function () {
      p.curve([[34, 51], [24, 44], [16, 54], [8, 46]], { width: 1.4 });          // flagella
      p.curve([[34, 59], [24, 66], [18, 57], [8, 64]], { width: 1.4 });
      var pili = [];
      for (var x = 48; x <= 112; x += 9) pili.push([x, 37, x + 1, 31], [x + 4, 73, x + 3, 79]);
      ticks(p, pili, { width: 1.2 });
      rrect(p, 34, 37, 90, 36, 18, { fill: C.teal });
      p.curve([[52, 56], [60, 48], [68, 61], [78, 49], [88, 60], [98, 51]], { width: 1.3, passes: 1 });
      p.dot(60, 64, 4); p.dot(104, 46, 4); p.dot(110, 62, 4);
    });
  });

  reg(HL, 'cell', function (p, C) {
    blob(p, [[18, 56], [24, 34], [48, 18], [80, 14], [108, 24], [124, 48], [118, 76], [96, 92], [62, 97], [34, 88]], plate(C));
    p.circle(56, 50, 32, { fill: C.violet });
    p.circle(52, 48, 11, plate(C));
    rot(p, -28, 100, 40, function () { p.ellipse(100, 40, 28, 15, plate(C)); ticks(p, [[90, 40, 94, 35], [94, 35, 99, 45], [99, 45, 104, 35], [104, 35, 108, 44]], { width: 1.1 }); });
    rot(p, 22, 94, 76, function () { p.ellipse(94, 76, 26, 14, plate(C)); ticks(p, [[85, 76, 89, 71], [89, 71, 94, 81], [94, 81, 99, 71], [99, 71, 103, 77]], { width: 1.1 }); });
    p.path('M24 72 q11 -7 22 0 M26 78 q9 -6 18 0 M28 84 q7 -5 14 0', { passes: 1, width: 1.4 });
    p.circle(74, 86, 9, plate(C)); p.circle(34, 38, 7, plate(C));
  });

  reg(HL, 'antibody', function (p, C) {
    shift(p, 0, 5, function () {
      p.poly([[62, 98], [78, 98], [78, 64], [104, 30], [92, 20], [70, 48], [48, 20], [36, 30], [62, 64]], { fill: C.violet });
      ticks(p, [[62, 74, 78, 74], [53, 40, 67, 52], [87, 40, 73, 52]], { width: 1.3 });
    });
    p.poly([[30, 4], [42, 4], [36, 14]], { fill: C.graphite, fillStyle: 'solid' });   // antigens at the tips
    p.circle(104, 10, 10, { fill: C.graphite, fillStyle: 'solid' });
    ticks(p, [[36, 17, 38, 22], [104, 17, 100, 23]], { width: 1.6 });
  });

  reg(HL, 'dna-helix', function (p, C) {
    rot(p, 24, 70, 55, function () {
      var N = 28, A = 20, y0 = 11, H = 88, s1 = [], s2 = [], rungs = [], i, t, y, x1, x2;
      for (i = 0; i <= N; i++) {
        t = i / N * 4 * PI; y = y0 + i * H / N;
        s1.push([70 + A * Math.sin(t), y]); s2.push([70 - A * Math.sin(t), y]);
      }
      for (i = 0; i < 16; i++) {
        t = PI / 8 + i * PI / 4;
        if (Math.abs(Math.sin(t)) < 0.5) continue;
        y = y0 + t / (4 * PI) * H; x1 = 70 + A * Math.sin(t); x2 = 70 - A * Math.sin(t);
        rungs.push([x1, y, x2, y]);
      }
      ticks(p, rungs, { stroke: C.orange, width: 3 });
      p.curve(s1, { width: 2.4 }); p.curve(s2, { width: 2.4 });
    });
    sparkle(p, 20, 22, 5); sparkle(p, 120, 90, 5);
  });

  reg(HL, 'pill-capsule', function (p, C) {
    rot(p, -35, 56, 50, function () {
      rrect(p, 14, 36, 84, 28, 14, plate(C));
      fillOnly(p, arcPts(28, 50, 14, 14, 90, 270, 8).concat([[56, 36], [56, 64]]), { fill: C.orange });
      p.line(56, 36, 56, 64);
      p.line(62, 43, 86, 43, { width: 1.2, passes: 1 });
    });
    p.circle(104, 84, 30, plate(C));
    p.line(92, 90, 116, 78, { width: 1.3 });
    p.circle(26, 92, 18, plate(C));
  });

  reg(HL, 'stethoscope', function (p, C) {
    p.circle(36, 12, 8, plate(C)); p.circle(104, 12, 8, plate(C));
    p.curve([[36, 17], [36, 40], [50, 62], [70, 74]], { width: 2 });
    p.curve([[104, 17], [104, 40], [90, 62], [70, 74]], { width: 2 });
    p.dot(70, 74, 7);
    p.curve([[70, 76], [70, 94], [88, 102], [106, 94], [112, 78]], { width: 2 });
    p.circle(112, 60, 30, { fill: C.blue });
    p.circle(112, 60, 14, plate(C));
  });

  reg(HL, 'thermometer', function (p, C) {
    var jy = 84 - 17 * Math.sin(rad(54));
    p.poly([[60, jy], [60, 18]].concat(arcPts(70, 18, 10, 10, 180, 360, 8), [[80, jy]], arcPts(70, 84, 17, 17, -54, 234, 16)), plate(C));
    p.rect(67, 30, 6, 54, { fill: C.red, passes: 0 });
    fillOnly(p, arcPts(70, 84, 11, 11, 0, 360, 16), { fill: C.red });
    p.line(64, 20, 64, 58, { width: 1.1, passes: 1 });
    ticks(p, [[86, 20, 96, 20], [86, 28, 92, 28], [86, 36, 96, 36], [86, 44, 92, 44], [86, 52, 96, 52], [86, 60, 92, 60]], { width: 1.4 });
  });

  reg(HL, 'bandage', function (p, C) {
    rot(p, -38, 70, 55, function () {
      rrect(p, 10, 40, 120, 30, 15, { fill: C.rose });
      beads(p, 24, 50, 40, 50, 2.8, 6); beads(p, 24, 60, 40, 60, 2.8, 6);
    });
    rot(p, 38, 70, 55, function () {
      rrect(p, 10, 40, 120, 30, 15, plate(C));
      beads(p, 24, 50, 40, 50, 2.8, 6); beads(p, 24, 60, 40, 60, 2.8, 6);
      beads(p, 100, 50, 116, 50, 2.8, 6); beads(p, 100, 60, 116, 60, 2.8, 6);
      p.rect(50, 40, 40, 30, plate(C));
      ticks(p, [[56, 48, 84, 48], [56, 55, 84, 55], [56, 62, 84, 62]], { width: 1.1 });
    });
  });

  reg(HL, 'plant-cell', function (p, C) {
    rrect(p, 8, 8, 124, 94, 12, plate(C, { width: 2.2 }));
    rrect(p, 15, 15, 110, 80, 9, { width: 1.2, passes: 1 });
    blob(p, [[62, 36], [86, 30], [106, 42], [104, 66], [84, 78], [62, 72], [54, 54]], plate(C));
    p.circle(34, 40, 22, plate(C)); p.dot(32, 38, 8);
    [[100, 24, -20], [30, 78, 15], [100, 86, 10]].forEach(function (c) {
      rot(p, c[2], c[0], c[1], function () { p.ellipse(c[0], c[1], 22, 12, { fill: C.teal }); });
    });
    ticks(p, [[24, 78, 38, 78], [92, 86, 108, 86]], { width: 1.1 });
  });

  reg(HL, 'leaf', function (p, C) {
    var L = [], R = [], v = [], i, t, cx, cy, nx, ny, w, vv;
    function mid(u) { return [24 + 88 * u, 92 - 76 * u - 10 * Math.sin(PI * u)]; }
    for (i = 0; i <= 14; i++) {
      t = i / 14; cx = mid(t)[0]; cy = mid(t)[1];
      var n2 = mid(Math.min(1, t + 0.02)), n1 = mid(Math.max(0, t - 0.02)), dx = n2[0] - n1[0], dy = n2[1] - n1[1], ln = Math.hypot(dx, dy);
      nx = -dy / ln; ny = dx / ln; w = 27 * Math.pow(Math.sin(PI * t), 0.85);
      L.push([cx + nx * w, cy + ny * w]); R.push([cx - nx * w, cy - ny * w]);
    }
    p.poly(L.concat(R.reverse()), { fill: C.teal });
    p.curve([mid(0), mid(0.25), mid(0.5), mid(0.75), mid(1)], { width: 2 });
    [0.18, 0.34, 0.5, 0.66, 0.8].forEach(function (u) {
      var m = mid(u), m2 = mid(u + 0.07), dx = m2[0] - m[0], dy = m2[1] - m[1], ln = Math.hypot(dx, dy), ux = -dy / ln, uy = dx / ln, ww = 22 * Math.pow(Math.sin(PI * (u + 0.07)), 0.85);
      v.push([m[0], m[1], m2[0] + ux * ww, m2[1] + uy * ww], [m[0], m[1], m2[0] - ux * ww, m2[1] - uy * ww]);
    });
    ticks(p, v, { width: 1.2 });
    p.line(24, 92, 10, 104, { width: 2 });
    p.poly([[118, 78], [124, 88], [118, 96], [112, 88]], plate(C));
  });
})(typeof window !== 'undefined' ? window : this);
