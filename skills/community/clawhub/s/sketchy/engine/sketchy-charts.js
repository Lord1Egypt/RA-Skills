/*!
 * sketchy-charts.js: hand-drawn charts with honest numbers
 * Looks sketchy. The numbers are real.
 * Needs sketchy.js (the pen). MIT License. https://github.com/OthmanAdi/sketchy
 *
 *   <figure class="sk-chart" data-chart='{"type":"bar","title":"Revenue by quarter",
 *           "unit":"€k","data":[["Q1",120],["Q2",140]]}'></figure>
 *
 *   SketchyCharts.render(figure, spec?)  draw one chart; the spec comes from the argument,
 *                                        from data-chart, or from a <script type="application/json">
 *                                        inside the figure
 *   SketchyCharts.renderAll(root?)       draw every .sk-chart and [data-chart] under root
 *   SketchyCharts.drawOn(figure?)        pencil reveal, counts up figures, lands stamps;
 *                                        nothing moves under ?static, ?print or reduced motion
 *
 * Sketchy.mount() renders charts through Sketchy.onMount whether this file loads before or
 * after sketchy.js. Rendering is idempotent and seeded: the same spec at the same width draws
 * the same chart. Layout is computed once without randomness; the four boil variants only
 * change the wobble of the strokes, and every label is drawn once, on top.
 *
 * Honesty lives in this file, not only in the docs: bars and areas start at zero, one axis
 * only, no 3D, pie slices add up to the whole, categories are sorted unless they carry an order
 * of their own, every value is in a hidden table and on data-* attributes of the marks.
 */
(function (global) {
  'use strict';

  var doc = global.document;
  var NS = 'http://www.w3.org/2000/svg';
  var VERSION = '0.1.0';
  var ANGLES = [-41, 38, -62, 60, -28, 26, -52];
  var LAYERS = ['back', 'guides', 'axes', 'marks', 'over', 'notes'];
  var TYPES = {};
  var ALIASES = {
    column: 'bar', columns: 'bar', bars: 'bar', horizontal: 'hbar', 'bar-h': 'hbar', row: 'hbar',
    stack: 'stacked', 'stacked-bar': 'stacked', group: 'grouped', 'grouped-bar': 'grouped',
    lines: 'line', doughnut: 'donut', ring: 'donut', xy: 'scatter', dots: 'scatter',
    slopegraph: 'slope', 'before-after': 'slope', tallies: 'tally', meter: 'gauge', fuel: 'gauge',
    milestones: 'timeline', 'big-number': 'bignumber', number: 'bignumber', kpi: 'bignumber',
    receipt: 'ledger', bill: 'ledger', invoice: 'ledger', slip: 'ledger'
  };

  /* ------------------------------------------------------------------ *
   * Small helpers
   * ------------------------------------------------------------------ */
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function isNum(v) { return typeof v === 'number' && isFinite(v); }
  function toNum(v) {
    if (v == null || v === '' || typeof v === 'boolean') return null;
    if (typeof v === 'number') return isFinite(v) ? v : null;
    var s = String(v).replace(/[\s  ,_]/g, '').replace(/−/g, '-');
    if (!/^[-+]?(\d+\.?\d*|\.\d+)(e[-+]?\d+)?$/i.test(s)) return null;
    var n = parseFloat(s);
    return isFinite(n) ? n : null;
  }
  function max(a) { var m = -Infinity; for (var i = 0; i < a.length; i++) if (a[i] > m) m = a[i]; return m; }
  function min(a) { var m = Infinity; for (var i = 0; i < a.length; i++) if (a[i] < m) m = a[i]; return m; }
  function sum(a) { var s = 0; for (var i = 0; i < a.length; i++) if (isNum(a[i])) s += a[i]; return s; }
  function svgEl(tag, attrs, parent) {
    var e = doc.createElementNS(NS, tag);
    if (attrs) for (var k in attrs) if (attrs[k] != null) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function part(parent, tag, cls) {
    var e = doc.createElement(tag);
    e.className = cls;
    e.setAttribute('data-sk-part', '');
    parent.appendChild(e);
    return e;
  }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function f2(n) { return Math.round(n * 100) / 100; }
  function params() { var S = global.Sketchy; return (S && S.params) || {}; }
  function isStatic() {
    var P = params(), S = global.Sketchy;
    return !!(P['static'] || P.print || (S && S.reducedMotion));
  }

  /* ------------------------------------------------------------------ *
   * Text measurement. Courier Prime is monospaced (0.6 em per glyph);
   * Caveat is measured on a canvas once the font is loaded, estimated before.
   * ------------------------------------------------------------------ */
  var mctx = null;
  function fontsReady() {
    try { return !doc.fonts || (doc.fonts.check('600 16px Caveat') && doc.fonts.check('700 16px "Courier Prime"')); } catch (e) { return true; }
  }
  function textW(str, size, mono, weight) {
    str = String(str == null ? '' : str);
    if (mono) return str.length * size * 0.6;
    if (fontsReady()) {
      mctx = mctx || doc.createElement('canvas').getContext('2d');
      mctx.font = (weight || 600) + ' ' + size + 'px Caveat';
      return mctx.measureText(str).width;
    }
    return str.length * size * 0.46;
  }
  function wrap(str, size, maxW, mono, weight) {
    var out = [];
    String(str == null ? '' : str).split('\n').forEach(function (para) {
      var words = para.split(/\s+/).filter(Boolean), cur = '';
      words.forEach(function (w) {
        var t = cur ? cur + ' ' + w : w;
        if (cur && textW(t, size, mono, weight) > maxW) { out.push(cur); cur = w; } else cur = t;
      });
      if (cur) out.push(cur);
    });
    return out.length ? out : [''];
  }
  function splitTwo(l, size) {
    var words = String(l).split(/\s+/);
    if (words.length < 2) return [String(l)];
    var best = null, bw = Infinity;
    for (var i = 1; i < words.length; i++) {
      var a = words.slice(0, i).join(' '), b = words.slice(i).join(' '), m = Math.max(textW(a, size), textW(b, size));
      if (m < bw) { bw = m; best = [a, b]; }
    }
    return best;
  }

  /* Push labels apart along one axis. items: [{pos, size}], pos is the center. */
  function spread(items, gap, lo, hi) {
    var list = items.slice().sort(function (a, b) { return a.pos - b.pos; });
    for (var it = 0; it < 6; it++) {
      for (var i = 1; i < list.length; i++) {
        var need = list[i - 1].pos + (list[i - 1].size + list[i].size) / 2 + gap;
        if (list[i].pos < need) list[i].pos = need;
      }
      if (list.length && hi != null) { var l = list[list.length - 1], over = l.pos + l.size / 2 - hi; if (over > 0) l.pos -= over; }
      for (var j = list.length - 2; j >= 0; j--) {
        var lim = list[j + 1].pos - (list[j + 1].size + list[j].size) / 2 - gap;
        if (list[j].pos > lim) list[j].pos = lim;
      }
      if (list.length && lo != null) { var fst = list[0], under = lo - (fst.pos - fst.size / 2); if (under > 0) fst.pos += under; }
    }
    return items;
  }
  function overlap(a, b) {
    var w = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x), h = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
    return w > 0 && h > 0 ? w * h : 0;
  }

  /* The pieces of a straight line that stay clear of every label: the hand lifts the
     pencil over the words. Ops run at paint time, when all label boxes are known. */
  function clearRuns(ctx, x1, y1, x2, y2, pad) {
    pad = pad == null ? 3 : pad;
    var len = Math.hypot(x2 - x1, y2 - y1), n = Math.max(2, Math.ceil(len / 2.5)), runs = [], cur = null;
    var lo = { x: Math.min(x1, x2) - pad, y: Math.min(y1, y2) - pad }, hi = { x: Math.max(x1, x2) + pad, y: Math.max(y1, y2) + pad };
    var boxes = ctx.texts.map(function (t) { return t.box; }).filter(function (b) { return !(b.x > hi.x || b.x + b.w < lo.x || b.y > hi.y || b.y + b.h < lo.y); });
    for (var i = 0; i <= n; i++) {
      var t = i / n, x = x1 + (x2 - x1) * t, y = y1 + (y2 - y1) * t;
      var hit = boxes.some(function (b) { return x > b.x - pad && x < b.x + b.w + pad && y > b.y - pad && y < b.y + b.h + pad; });
      if (!hit) { if (!cur) cur = [t, t]; else cur[1] = t; } else if (cur) { runs.push(cur); cur = null; }
    }
    if (cur) runs.push(cur);
    return runs.filter(function (r) { return (r[1] - r[0]) * len > 5; })
      .map(function (r) { return [x1 + (x2 - x1) * r[0], y1 + (y2 - y1) * r[0], x1 + (x2 - x1) * r[1], y1 + (y2 - y1) * r[1]]; });
  }
  function gapLine(p, ctx, x1, y1, x2, y2, o) {
    clearRuns(ctx, x1, y1, x2, y2, o && o.pad).forEach(function (s) { p.line(s[0], s[1], s[2], s[3], o); });
  }

  /* A line through data points with a little hand wobble between them.
     The curve passes through every data point exactly, so it never invents a peak. */
  function wobblePath(pts, r, amp) {
    if (pts.length < 2) return '';
    var out = [pts[0]];
    for (var i = 1; i < pts.length; i++) {
      var a = pts[i - 1], b = pts[i], dx = b[0] - a[0], dy = b[1] - a[1], len = Math.hypot(dx, dy) || 1;
      var nx = -dy / len, ny = dx / len, k = len > 90 ? 2 : 1;
      for (var j = 1; j <= k; j++) {
        var t = j / (k + 1), o = (r() - 0.5) * amp * Math.min(1, len / 40);
        out.push([a[0] + dx * t + nx * o, a[1] + dy * t + ny * o]);
      }
      out.push(b);
    }
    return global.Sketchy.geometry.smooth(out, false);
  }

  /* ------------------------------------------------------------------ *
   * Numbers. Defaults follow the house rules: thousands separators, one
   * decimal under 100, whole numbers from 100, rounded to the hundred above
   * 10,000, "1.42 million" from a million; signs are + and U+2212.
   * ------------------------------------------------------------------ */
  var CURRENCY_UNIT = /^([$£¥₹€]|EUR|USD|GBP|CHF|JPY)$/;
  function decimalsOf(step) {
    for (var d = 0; d < 6; d++) { var k = step * Math.pow(10, d); if (Math.abs(Math.round(k) - k) < 1e-6) return d; }
    return 6;
  }
  function makeFormat(spec, values, unitOverride) {
    var f = spec.format;
    if (typeof f === 'string') f = { locale: f };
    f = f || {};
    var locale = f.locale || spec.locale || (doc.documentElement.getAttribute('lang')) || 'en';
    try { new Intl.NumberFormat(locale); } catch (e) { locale = 'en'; }
    var unit = unitOverride != null ? unitOverride : (spec.unit == null ? '' : String(spec.unit));
    var nums = values.filter(isNum);
    var allInt = nums.every(function (v) { return Math.round(v) === v; });
    var cache = {};
    function nf(o) { var k = JSON.stringify(o); return cache[k] || (cache[k] = new Intl.NumberFormat(locale, o)); }
    var fixed = f.decimals != null ? f.decimals : null;
    var english = /^(en|ja|zh|ko|th|he)/i.test(locale);
    function minus(s) { return s.replace(/^-/, '−').replace(/^−(\D*)0([.,]0*)?$/, '$10$2'); }
    function core(v, dec) {
      if (dec == null) dec = fixed;
      var a = Math.abs(v);
      if (f.currency) {
        var dd = dec != null ? dec : 2;
        return minus(nf({ style: 'currency', currency: f.currency, minimumFractionDigits: dd, maximumFractionDigits: dd }).format(v));
      }
      var s;
      if (dec != null) s = nf({ minimumFractionDigits: dec, maximumFractionDigits: dec }).format(v);
      else if (a >= 1e6 && f.compact !== false) s = nf({ notation: 'compact', compactDisplay: 'long', maximumFractionDigits: 2 }).format(v);
      else if (a > 10000 && f.round !== false) s = nf({ maximumFractionDigits: 0 }).format(Math.round(v / 100) * 100);
      else if (a >= 100 || allInt) s = nf({ maximumFractionDigits: 0 }).format(Math.round(v));
      else if (a > 0 && a < 1) s = nf({ maximumSignificantDigits: 2 }).format(v);
      else s = nf({ minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(v);
      return minus((f.prefix || '') + s + (f.suffix || ''));
    }
    function unitize(s, u) {
      u = u == null ? unit : u;
      if (!u || f.currency) return s;
      if (u === '%') return s + (english ? '%' : ' %');
      if (/^[$£¥₹]$/.test(u) || (u === '€' && english)) return s.charAt(0) === '−' ? '−' + u + s.slice(1) : u + s;
      return s + ' ' + u;
    }
    var fmt = {
      locale: locale, unit: unit, allInt: allInt,
      num: function (v, dec) { return core(v, dec); },
      u: function (v, dec) { return unitize(core(v, dec)); },
      v: function (v, dec) { return fmt.unitOnValues || unit === '%' ? unitize(core(v, dec)) : core(v, dec); },
      signed: function (v, dec, u) {
        var s = core(Math.abs(v), dec);
        var sign = Math.abs(v) < 1e-12 || /^[0.,\s]*$/.test(s.replace(/[^\d.,]/g, '').replace(/[1-9]/g, 'x')) ? '±' : (v > 0 ? '+' : '−');
        if (/^0([.,]0+)?$/.test(s)) sign = '±';
        return sign + unitize(s, u);
      },
      diff: function (v, dec) {
        if (unit === '%') return fmt.signed(v, dec == null ? 1 : dec, '').replace(/$/, ' pts');
        return fmt.signed(v, dec);
      },
      exact: function (v) {
        if (!isNum(v)) return '';
        if (f.currency) return core(v, fixed != null ? fixed : 2);
        return unitize(minus(nf({ maximumFractionDigits: 6 }).format(v)));
      },
      pct: function (ratio, dec) {
        var p = ratio * 100, d = dec != null ? dec : (Math.abs(p) >= 100 ? 0 : 1);
        return unitize(minus(nf({ minimumFractionDigits: d, maximumFractionDigits: d }).format(p)), '%');
      },
      tick: function (nt) {
        var big = Math.max(Math.abs(nt.hi), Math.abs(nt.lo)) >= 10000;
        return function (v) {
          if (f.currency && !big) return core(v, nt.dec);
          var s = big ? nf({ notation: 'compact', compactDisplay: 'short', maximumFractionDigits: 1 }).format(v)
            : nf({ minimumFractionDigits: nt.dec, maximumFractionDigits: nt.dec }).format(v);
          return minus((f.prefix || '') + s + (f.suffix || ''));
        };
      },
      date: function (d, o) {
        try { return new Intl.DateTimeFormat(locale, Object.assign({ timeZone: 'UTC' }, o)).format(d); } catch (e) { return d.toISOString().slice(0, 10); }
      }
    };
    return fmt;
  }

  function niceStep(span, count) {
    var raw = span / Math.max(1, count), mag = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10)), n = raw / mag;
    return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10) * mag;
  }
  /* Nice ticks; without fixed ends, try a few tick counts and keep the axis that wastes the least room. */
  function niceTicks(lo, hi, count, fixedHi, fixedLo) {
    if (!(hi > lo)) hi = lo + (lo === 0 ? 1 : Math.abs(lo) * 0.5);
    if (fixedHi != null || fixedLo != null) return niceOnce(lo, hi, count, fixedHi, fixedLo);
    var best = null;
    for (var c = Math.max(2, count - 1); c <= count + 2; c++) {
      var t = niceOnce(lo, hi, c), n = t.ticks.length;
      if (n < 3 || n > 8) continue;
      var score = ((t.hi - t.lo) - (hi - lo)) / (t.hi - t.lo) + Math.abs(n - (count + 1)) * 0.06;
      if (!best || score < best.score - 1e-9) { best = t; best.score = score; }
    }
    return best || niceOnce(lo, hi, count);
  }
  function niceOnce(lo, hi, count, fixedHi, fixedLo) {
    var step = niceStep((fixedHi != null ? fixedHi : hi) - (fixedLo != null ? fixedLo : lo), count);
    var a = fixedLo != null ? fixedLo : Math.floor(lo / step + 1e-9) * step;
    var b = fixedHi != null ? fixedHi : Math.ceil(hi / step - 1e-9) * step;
    var d = decimalsOf(step), ticks = [];
    for (var v = Math.ceil(a / step - 1e-9) * step; v <= b + step * 1e-6; v += step) ticks.push(+v.toFixed(d));
    return { lo: a, hi: b, step: step, ticks: ticks, dec: d };
  }

  /* ------------------------------------------------------------------ *
   * Spec: reading and normalising
   * ------------------------------------------------------------------ */
  function readSpec(fig) {
    var raw = fig.getAttribute('data-chart');
    if (!raw || raw === 'true') {
      var s = fig.querySelector(':scope > script[type="application/json"]');
      raw = s ? s.textContent : null;
    }
    if (!raw) return null;
    try { return JSON.parse(raw); } catch (e) { return { __error: 'The chart spec is not valid JSON (' + e.message + ').' }; }
  }

  function toRows(data) {
    if (data == null) return [];
    if (!Array.isArray(data) && typeof data === 'object') {
      return Object.keys(data).map(function (k) { return { label: k, values: [].concat(data[k]).map(toNum), raw: data[k] }; });
    }
    return data.map(function (d, i) {
      if (Array.isArray(d)) return { label: d[0], values: d.slice(1).map(toNum), raw: d };
      if (d && typeof d === 'object') {
        var v = d.values != null ? [].concat(d.values) : [d.value != null ? d.value : (d.y != null ? d.y : d.count)];
        return { label: d.label != null ? d.label : (d.name != null ? d.name : d.x), values: v.map(toNum), raw: d };
      }
      return { label: String(i + 1), values: [toNum(d)], raw: d };
    });
  }

  /* -> { labels: [...], series: [{ name, values, role, color }] } */
  function normalizeSeries(sp) {
    var ser = sp.series, given = Array.isArray(sp.x) ? sp.x.slice() : (Array.isArray(sp.labels) ? sp.labels.slice() : null);
    if (Array.isArray(ser) && ser.length && ser[0] && typeof ser[0] === 'object' && !Array.isArray(ser[0])) {
      var labels = given ? given.slice() : [], seen = {};
      labels.forEach(function (l) { seen[String(l)] = 1; });
      ser.forEach(function (s) {
        (s.data || s.values || []).forEach(function (pt, j) {
          var lab = Array.isArray(pt) ? pt[0] : (pt && typeof pt === 'object' ? (pt.label != null ? pt.label : pt.x) : (given ? given[j] : j + 1));
          if (lab != null && !seen[String(lab)]) { seen[String(lab)] = 1; labels.push(lab); }
        });
      });
      var keys = labels.map(String);
      return {
        labels: labels,
        series: ser.map(function (s, si) {
          var vals = keys.map(function () { return null; });
          (s.data || s.values || []).forEach(function (pt, j) {
            var lab, v;
            if (Array.isArray(pt)) { lab = pt[0]; v = pt[1]; }
            else if (pt && typeof pt === 'object') { lab = pt.label != null ? pt.label : pt.x; v = pt.value != null ? pt.value : pt.y; }
            else { lab = given ? given[j] : j + 1; v = pt; }
            var idx = keys.indexOf(String(lab));
            if (idx >= 0) vals[idx] = toNum(v);
          });
          return { name: String(s.name || s.label || ('series ' + (si + 1))), values: vals, role: s.role || s.kind, color: s.color, dashed: s.dashed };
        })
      };
    }
    var rows = toRows(sp.data);
    var nSer = Math.max(1, max(rows.map(function (r) { return r.values.length; }).concat([1])));
    var names = Array.isArray(ser) ? ser.map(String) : [];
    var out = { labels: rows.map(function (r) { return r.label; }), series: [] };
    for (var k = 0; k < nSer; k++) {
      out.series.push({
        name: names[k] || (nSer === 1 ? ((sp.y && sp.y.label) || sp.title || 'value') : 'series ' + (k + 1)),
        values: rows.map(function (r) { return r.values[k] == null ? null : r.values[k]; })
      });
    }
    out.rows = rows;
    return out;
  }

  function collectNumbers(x, out) {
    out = out || [];
    if (isNum(x)) out.push(x);
    else if (Array.isArray(x)) x.forEach(function (v, i) { if (i > 0 || typeof v !== 'string') collectNumbers(v, out); });
    else if (x && typeof x === 'object') Object.keys(x).forEach(function (k) { if (!/^(x|date|label|name|year)$/.test(k)) collectNumbers(x[k], out); });
    return out;
  }

  var ORDERED = /^(q[1-4]\b|h[12]\b|fy|cw|kw|wk|week|woche|day|tag|month|monat|year|jahr|stage|step|phase|sprint|round|wave|lesson|module|unit|chapter|v\d|jan|feb|mar|mär|apr|may|mai|jun|jul|aug|sep|oct|okt|nov|dec|dez|mon|tue|wed|thu|fri|sat|sun|strongly|agree|disagree|neutral|very|somewhat|never|rarely|sometimes|often|always|low|medium|high|none|poor|fair|good|excellent|before|after|start|end|first|second|third|last|now|today|beginner|intermediate|advanced|bronze|silver|gold|platinum|diamond|visit|sign|trial|paid|lead|demo)/i;
  function looksOrdered(labels) {
    return labels.length > 0 && labels.every(function (l) { var s = String(l).trim(); return /\d/.test(s) || ORDERED.test(s); });
  }

  /* ------------------------------------------------------------------ *
   * Styles injected once: the visually hidden table, figure parts, slips.
   * ------------------------------------------------------------------ */
  var styled = false;
  function injectStyle() {
    if (styled || doc.getElementById('sk-charts-style')) { styled = true; return; }
    styled = true;
    var css = [
      '.sk-chart{margin:0;position:relative;display:block;min-width:0;color:var(--sk-graphite)}',
      '.sk-chart-head{display:grid;gap:.06em;margin:0 0 .5em}',
      '.sk-chart-title{font:600 1.32em/1.04 var(--sk-font-hand);color:var(--sk-ink);text-wrap:balance}',
      '.sk-chart-sub{font:500 .94em/1.15 var(--sk-font-hand);color:var(--sk-graphite-soft)}',
      '.sk-chart-delta{font:600 1em/1.3 var(--sk-font-hand);color:var(--sk-graphite);margin-top:.15em}',
      '.sk-chart .sk-num{font-family:var(--sk-font-mono);font-weight:700;font-size:.84em;color:var(--sk-figure);font-variant-numeric:tabular-nums;white-space:nowrap}',
      '.sk-chart .sk-num.is-ref{font-weight:400}',
      '.sk-chart .sk-num.is-good{color:var(--sk-stamp-green)}',
      '.sk-chart .sk-num.is-bad{color:var(--sk-red-ink)}',
      '.sk-chart-body{position:relative}',
      '.sk-chart-svg{display:block;width:100%;height:auto;overflow:visible}',
      '.sk-chart-svg .sk-text-mono{font-variant-numeric:tabular-nums lining-nums}',
      '.sk-chart-hits *{fill:transparent;stroke:none}',
      '.sk-chart-foot{display:flex;flex-wrap:wrap;align-items:flex-start;justify-content:space-between;gap:.3em 1.6em;margin-top:.4em}',
      '.sk-chart-foot:empty{display:none}',
      '.sk-chart-source{margin:0;font:500 .86em/1.3 var(--sk-font-hand);color:var(--sk-graphite-soft)}',
      '.sk-chart-source .sk-sect{margin-right:.3em}',
      '.sk-chart-source .val{font-family:var(--sk-font-mono);font-weight:700;font-size:.97em;color:var(--sk-figure)}',
      '.sk-chart-math{margin-left:auto;font-size:.9em;text-align:right}',
      '.sk-chart-math summary{cursor:pointer;list-style:none;color:var(--sk-graphite-soft);font-family:var(--sk-font-hand);font-weight:600}',
      '.sk-chart-math summary::-webkit-details-marker{display:none}',
      '.sk-chart-math[open] .sk-m-show,.sk-chart-math:not([open]) .sk-m-hide{display:none}',
      '.sk-chart-math p{margin:.1em 0 0;font-family:var(--sk-font-hand);font-weight:600}',
      '.sk-chart-math .val{font-family:var(--sk-font-mono);font-weight:700;color:var(--sk-figure);font-size:.96em}',
      '.sk-chart-error{font:600 1em/1.3 var(--sk-font-hand);color:var(--sk-red-ink);margin:0}',
      '.sk-chart.is-slip .sk-chart-head{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}',
      '.sk-chart.is-slip .sk-chart-body{max-width:580px;margin:0 auto;transform:rotate(-.8deg);filter:drop-shadow(0 10px 12px rgba(var(--sk-shadow),.22))}',
      '.sk-chart-stamp{position:absolute;pointer-events:none;white-space:nowrap;transform:translate(-50%,-50%) rotate(-10deg)}',
      '.sk-chart-stamp.is-slam{animation:sk-chart-slam 360ms var(--sk-ease-slam,cubic-bezier(.3,.6,.3,1.25)) both}',
      '.sk-chart-stamp.is-unearned{border-style:dashed;outline-style:dashed;opacity:.3;filter:none;color:var(--sk-graphite)}',
      '@keyframes sk-chart-slam{0%{opacity:0;transform:translate(-50%,-50%) scale(1.7) rotate(-10deg)}70%{opacity:.9;transform:translate(-50%,-50%) scale(.95) rotate(-10deg)}100%{transform:translate(-50%,-50%) scale(1) rotate(-10deg)}}',
      '.sk-chart.is-drawing .sk-v{display:none!important}',
      '.sk-chart.is-drawing .sk-v0,.sk-chart.is-drawing .sk-v-only{display:inline!important}',
      '.sk-chart .sk-sr,table.sk-sr{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}'
    ].join('\n');
    var st = doc.createElement('style');
    st.id = 'sk-charts-style';
    st.textContent = css;
    (doc.head || doc.documentElement).appendChild(st);
  }

  /* ------------------------------------------------------------------ *
   * The chart context: layout is recorded as ops and texts, then drawn
   * by Sketchy.variants() into four boil variants.
   * ------------------------------------------------------------------ */
  function makeCtx(figure, sp, C, W, fs) {
    var narrow = W < 540;
    var hand = clamp(fs * 0.86, 15, 30);
    if (narrow) hand = Math.max(15, hand * 0.95);
    var mono = clamp(fs * 0.72, 13, 24);
    var S = { hand: hand, mono: mono, tick: Math.max(12, mono * 0.9), small: Math.max(15, hand * 0.88) };
    var ctx = {
      figure: figure, spec: sp, C: C, W: W, H: sp.height ? +sp.height : null, S: S, narrow: narrow,
      lw: clamp(hand / 11, 1.35, 2.5), gap: clamp(hand * 0.2, 3.2, 4.8),
      night: doc.documentElement.getAttribute('data-theme') === 'night',
      ops: [], texts: [], marks: [], occupied: [], anchors: [], counts: [], stamps: [],
      notesRoom: sp.annotate && [].concat(sp.annotate).length ? hand * 0.9 : 0,
      warnings: [], table: null, headline: null, unitOnValues: false
    };
    ctx.warn = function (msg) {
      ctx.warnings.push(msg);
      var seen = figure.__skWarned || (figure.__skWarned = {});
      if (!seen[msg]) { seen[msg] = 1; if (global.console) console.warn('[sketchy-charts] ' + (sp.title || sp.type) + ': ' + msg); }
    };
    ctx.op = function (layer, fn, attrs) { ctx.ops.push({ layer: layer, fn: fn, attrs: attrs }); };
    ctx.occupy = function (b) { ctx.occupied.push(b); };
    ctx.text = function (x, y, str, o) {
      o = o || {};
      str = String(str);
      var size = o.size || (o.mono ? S.mono : S.hand);
      var w = textW(str, size, o.mono, o.weight || (o.mono ? 700 : 600)), box;
      if (o.rotate) {
        var r = Math.abs(o.rotate) * Math.PI / 180, c = Math.cos(r), s = Math.sin(r);
        box = { x: x - w * c, y: y - size * 0.8, w: w * c + size * 0.3, h: w * s + size };
      } else {
        var bx = o.anchor === 'middle' ? x - w / 2 : o.anchor === 'end' ? x - w : x;
        box = { x: bx, y: y - size * (o.mono ? 0.74 : 0.8), w: w, h: size * (o.mono ? 0.94 : 1.02) };
      }
      ctx.texts.push({ x: x, y: y, str: str, box: box, attrs: o.attrs, count: o.count,
        o: { anchor: o.anchor, size: size, color: o.color || (o.mono ? C.figure : C.graphite), weight: o.weight, mono: o.mono, rotate: o.rotate, opacity: o.opacity, cls: o.cls } });
      if (!o.free) ctx.occupied.push(box);
      return box;
    };
    /* Handwriting with the numbers in Courier: "axis starts at 700", "plan 75%".
       Every run of digits (with its sign, separators and unit) switches to the mono face. */
    ctx.textMix = function (x, y, str, o) {
      o = o || {};
      var size = o.size || S.small, ms = size * 0.84, parts = [];
      String(str).split(/([−+\-±]?\d[\d.,  ]*(?:\s?(?:%|pts|€|\$|£|k|h))?)/).forEach(function (s, i) { if (s) parts.push({ t: s, mono: i % 2 === 1 }); });
      var widths = parts.map(function (q) { return textW(q.t, q.mono ? ms : size, q.mono, q.mono ? 700 : 600); });
      var total = sum(widths) + (parts.length - 1) * 1.5, cx = o.anchor === 'end' ? x - total : o.anchor === 'middle' ? x - total / 2 : x;
      var first = null;
      parts.forEach(function (q, i) {
        var b = ctx.text(cx, y, q.t.replace(/^\s+/, ' ').replace(/\s+$/, ' '), { size: q.mono ? ms : size, mono: q.mono, color: q.mono ? (o.figure || o.color || C.figure) : (o.color || C.graphite), weight: q.mono ? 700 : null, free: o.free });
        if (!first) first = b;
        cx += widths[i] + 1.5;
      });
      return { x: first ? first.x : x, y: y - size * 0.8, w: total, h: size };
    };
    ctx.mark = function (kind, geom, data) { ctx.marks.push({ kind: kind, geom: geom, data: data }); };
    ctx.anchor = function (keys, pt) { ctx.anchors.push({ keys: [].concat(keys).map(function (k) { return String(k).toLowerCase(); }), pt: pt }); };
    ctx.color = function (i) { var P = C.pencils; return P[i % P.length]; };
    return ctx;
  }

  function hlIndex(ctx, labels, quiet) {
    var h = ctx.spec.highlight;
    if (h == null || h === false || h === '') return -1;
    if (Array.isArray(h)) { ctx.warn('one focal point per chart: highlight takes one label, the first one was used'); h = h[0]; }
    if (h && typeof h === 'object') h = h.at != null ? h.at : h.label;
    var s = String(h).toLowerCase();
    for (var i = 0; i < labels.length; i++) if (String(labels[i]).toLowerCase() === s) return i;
    if (typeof h === 'number' && Math.round(h) === h && h >= 0 && h < labels.length) return h;
    if (!quiet) ctx.warn('highlight "' + h + '" matches no label');
    return -1;
  }
  function hlLabel(ctx, labels, quiet) { var i = hlIndex(ctx, labels, quiet); return i < 0 ? null : String(labels[i]); }

  function sortRows(ctx, rows, key) {
    var s = ctx.spec.sort;
    if (s == null) s = looksOrdered(rows.map(function (r) { return r.label; })) ? 'none' : 'desc';
    if (s === true) s = 'desc';
    if (s === 'desc' || s === 'descending') return rows.slice().sort(function (a, b) { return key(b) - key(a); });
    if (s === 'asc' || s === 'ascending') return rows.slice().sort(function (a, b) { return key(a) - key(b); });
    if (s === 'label' || s === 'alpha') return rows.slice().sort(function (a, b) { return String(a.label).localeCompare(String(b.label)); });
    return rows;
  }

  function refOf(x, name) {
    if (x == null || x === false) return null;
    if (isNum(x)) return { value: x, label: name };
    if (typeof x === 'object' && isNum(toNum(x.value))) return { value: toNum(x.value), label: x.label || name };
    var n = toNum(x);
    return n == null ? null : { value: n, label: name };
  }
  function refsOf(ctx) {
    var out = [], b = refOf(ctx.spec.benchmark, 'benchmark'), t = refOf(ctx.spec.target, 'target');
    if (b) { b.kind = 'benchmark'; out.push(b); }
    if (t) { t.kind = 'target'; out.push(t); }
    return out;
  }

  /* Bars and areas start at zero. A spec that asks otherwise gets a warning and a zero baseline. */
  function zeroDomain(ctx, vals, what) {
    var sp = ctx.spec, y = sp.y && typeof sp.y === 'object' ? sp.y : {};
    var lo = Math.min(0, min(vals.concat([0]))), hi = Math.max(0, max(vals.concat([0])));
    refsOf(ctx).forEach(function (r) { hi = Math.max(hi, r.value); lo = Math.min(lo, r.value); });
    var askMin = y.min != null ? toNum(y.min) : toNum(sp.min);
    if (askMin != null && askMin > lo) ctx.warn(what + ' start at zero; the axis minimum ' + askMin + ' was ignored');
    var askMax = y.max != null ? toNum(y.max) : toNum(sp.max), fixedHi = null;
    if (askMax != null) {
      if (askMax < hi) ctx.warn('max ' + askMax + ' is below the largest value ' + hi + '; the axis was extended so nothing is cut off');
      else fixedHi = askMax;
    }
    return { lo: lo, hi: fixedHi != null ? fixedHi : hi, fixedHi: fixedHi };
  }
  /* Lines may start above zero (positions, not lengths); the chart then says so. */
  function lineDomain(ctx, vals) {
    var sp = ctx.spec, y = sp.y && typeof sp.y === 'object' ? sp.y : {};
    var lo = min(vals), hi = max(vals);
    refsOf(ctx).forEach(function (r) { hi = Math.max(hi, r.value); lo = Math.min(lo, r.value); });
    var askMin = y.min != null ? toNum(y.min) : toNum(sp.min), askMax = y.max != null ? toNum(y.max) : toNum(sp.max);
    if (y.zero === true || (lo >= 0 && lo <= hi * 0.45)) lo = Math.min(0, lo);
    var fixedLo = null, fixedHi = null;
    if (askMin != null) { if (askMin > lo) ctx.warn('the axis minimum ' + askMin + ' would cut off data; it was lowered'); else { lo = askMin; fixedLo = askMin; } }
    if (askMax != null) { if (askMax < hi) ctx.warn('the axis maximum ' + askMax + ' would cut off data; it was raised'); else { hi = askMax; fixedHi = askMax; } }
    if (hi === lo) { hi = lo + 1; }
    return { lo: lo, hi: hi, fixedHi: fixedHi, fixedLo: fixedLo };
  }

  /* ------------------------------------------------------------------ *
   * Cartesian frame: y ticks, guides, axis, baseline, x labels
   * ------------------------------------------------------------------ */
  function yCaption(ctx) {
    var sp = ctx.spec, y = sp.y && typeof sp.y === 'object' ? sp.y : {};
    var u = y.unit != null ? y.unit : sp.unit;
    var parts = [];
    if (y.label) parts.push(y.label);
    if (u) parts.push(y.label ? '(' + u + ')' : u);
    return parts.join(' ');
  }
  function defaultHeight(ctx) {
    var W = ctx.W;
    return Math.round(clamp(W * (ctx.narrow ? 0.82 : 0.5), 260, 520));
  }
  function xLabelLayout(ctx, labels, slot, band) {
    var size = ctx.S.hand, ws = labels.map(function (l) { return textW(l, size); }), m = max(ws.concat([0]));
    if (m <= slot * 0.92) return { mode: 'flat', h: size * 1.45, every: 1 };
    if (!band) return { mode: 'flat', h: size * 1.45, every: Math.max(2, Math.ceil((m + size) / Math.max(1, slot))) };
    var two = labels.map(function (l) { return splitTwo(l, size); });
    var m2 = max(two.map(function (ls) { return max(ls.map(function (s) { return textW(s, size); })); }));
    if (m2 <= slot * 0.94 && two.every(function (ls) { return ls.length <= 2; })) return { mode: 'two', h: size * 2.45, lines: two, every: 1 };
    var rot = 38;
    return { mode: 'rot', rot: rot, h: m * Math.sin(rot * Math.PI / 180) + size * 1.25, every: 1 };
  }
  function frame(ctx, o) {
    var S = ctx.S, W = ctx.W;
    var cap = o.caption != null ? o.caption : yCaption(ctx);
    var legendH = o.legendH || 0;
    var capRow = cap || o.lo > 0;
    var top = legendH + ctx.notesRoom + (capRow ? S.tick * 2 : S.tick * 0.9) + (o.topRoom || 0);
    var prov = niceTicks(o.lo, o.hi, 5, o.fixedHi, o.fixedLo), tf0 = ctx.fmt.tick(prov);
    var labW = max(prov.ticks.map(function (t) { return textW(tf0(t), S.tick, true); }));
    var x0 = Math.ceil(labW + 18), x1 = W - Math.max(o.right || 0, S.hand * 0.5) - (ctx.refRoom || 0);
    var n = o.xLabels ? o.xLabels.length : 0, inset = o.inset || 0;
    var slot = n ? (x1 - x0 - inset * 2) / Math.max(1, o.band ? n : n - 1) : 0;
    var xl = n ? xLabelLayout(ctx, o.xLabels, slot, o.band) : { h: 0, every: 1 };
    var bottom = xl.h + S.hand * 0.35 + (o.xTitle ? S.hand * 1.4 : 0);
    if (!ctx.H) ctx.H = defaultHeight(ctx);
    var y0 = top, y1 = ctx.H - bottom, minPlot = Math.max(120, S.hand * 6.5);
    if (y1 - y0 < minPlot) { ctx.H = Math.ceil(top + minPlot + bottom); y1 = ctx.H - bottom; }
    var count = clamp(Math.round((y1 - y0) / (S.tick * 3.8)), 3, 6);
    var nt = niceTicks(o.lo, o.hi, count, o.fixedHi, o.fixedLo);
    var fr = {
      x0: x0, x1: x1, y0: y0, y1: y1, lo: nt.lo, hi: nt.hi, ticks: nt.ticks, tf: ctx.fmt.tick(nt), xl: xl, slot: slot, inset: inset,
      caption: cap, capY: legendH + ctx.notesRoom + S.tick * 1.15
    };
    fr.y = function (v) { return fr.y1 - (v - fr.lo) / (fr.hi - fr.lo) * (fr.y1 - fr.y0); };
    fr.zero = fr.lo <= 0 && fr.hi >= 0;
    fr.yBase = fr.zero ? fr.y(0) : y1;
    return fr;
  }
  function drawFrame(ctx, fr) {
    var C = ctx.C, S = ctx.S, lw = ctx.lw;
    fr.ticks.forEach(function (t) {
      var y = fr.y(t);
      var isBase = fr.zero ? Math.abs(t) < 1e-12 : t === fr.lo;
      if (!isBase) ctx.op('guides', function (p) { gapLine(p, ctx, fr.x0 + 4, y, fr.x1, y, { width: 0.9, passes: 1, rough: 0.35, opacity: 0.2 }); });
      ctx.op('axes', function (p) { p.line(fr.x0 - 6, y, fr.x0 - 1, y, { width: 1.1, passes: 1, rough: 0.4, opacity: 0.7 }); });
      ctx.text(fr.x0 - 10, y + S.tick * 0.33, fr.tf(t), { mono: true, size: S.tick, anchor: 'end', color: C['graphite-soft'], weight: 400 });
    });
    ctx.op('axes', function (p) { p.line(fr.x0, fr.y1 + 3, fr.x0, fr.y0 - S.tick * 0.6, { width: lw * 0.9 }); });
    ctx.op('axes', function (p) { p.line(fr.x0 - 3, fr.yBase, fr.x1 + 5, fr.yBase, { width: lw }); });
    var capX = 0;
    if (fr.caption) { var b = ctx.text(0, fr.capY, fr.caption, { size: S.small, color: C['graphite-soft'] }); capX = b.x + b.w + S.hand * 0.6; }
    if (!fr.zero && fr.lo > 0) {
      // the axis does not start at zero: break it and say so
      var yb = fr.y1 - S.hand * 0.55;
      ctx.op('axes', function (p) {
        p.line(fr.x0 - 7, yb + 3, fr.x0 + 7, yb - 3, { width: 1.3, passes: 1, rough: 0.5 });
        p.line(fr.x0 - 7, yb + 8, fr.x0 + 7, yb + 2, { width: 1.3, passes: 1, rough: 0.5 });
      });
      ctx.textMix(capX, fr.capY, 'axis starts at ' + fr.tf(fr.lo), { size: S.small, color: C['red-ink'] });
    }
  }
  function drawXLabels(ctx, fr, labels, xs, hl) {
    var S = ctx.S, xl = fr.xl, y0 = fr.y1 + S.hand * 1.08, C = ctx.C, n = labels.length, k = xl.every || 1;
    // thin long axes: keep the first and the last label, every k-th between them
    var keep = labels.map(function (l, i) { return k === 1 || i === 0 || i === n - 1 || (i % k === 0 && n - 1 - i >= k * 0.75); });
    if (hl) hl.forEach(function (h, i) { if (h) keep[i] = true; });
    labels.forEach(function (l, i) {
      if (!keep[i]) return;
      var col = hl && hl[i] ? C['red-ink'] : C.graphite;
      if (xl.mode === 'rot') ctx.text(xs[i] + S.hand * 0.3, y0 - S.hand * 0.25, l, { anchor: 'end', rotate: -xl.rot, color: col });
      else if (xl.mode === 'two') xl.lines[i].forEach(function (s, k) { ctx.text(xs[i], y0 + k * S.hand * 0.98, s, { anchor: 'middle', color: col }); });
      else ctx.text(xs[i], y0, l, { anchor: 'middle', color: col });
    });
  }

  /* Benchmark (blue, solid: what others did) and target (red, dashed: a plan). */
  function refLines(ctx, fr, horizontal) {
    var C = ctx.C, S = ctx.S;
    refsOf(ctx).forEach(function (r) {
      var isT = r.kind === 'target', col = isT ? C.red : C.blue, dash = isT ? '7 6' : null;
      var word = r.label || r.kind, val = ctx.fmt.u(r.value), size = S.small;
      var tw = textW(word + ' ', size) + textW(val, S.mono * 0.92, true);
      if (horizontal) {
        var y = fr.y(r.value), wc = isT ? C['red-ink'] : C['graphite-soft'], vc = isT ? C['red-ink'] : C.figure;
        ctx.op('over', function (p) { gapLine(p, ctx, fr.x0 + 2, y, fr.x1 + 4, y, { stroke: col, width: ctx.lw * (isT ? 1.05 : 1.2), passes: 1, dash: dash, rough: 0.5, opacity: 0.95 }); });
        // the label goes where it hits no bar and no value: scan along the line, right end first
        var ww = textW(word, size), vw2 = textW(val, S.mono * 0.92, true);
        if (ctx.refRoom) {
          var two = ww + size * 0.25 + vw2 > ctx.refRoom - 8, mx = ctx.W - ctx.refRoom + 8;
          var lh = two ? size * 2.1 : size, by0 = clamp(y - lh / 2, 0, ctx.H - lh);
          ctx.text(mx, by0 + size * 0.8, word, { size: size, color: wc });
          if (two) ctx.text(mx, by0 + size * 1.9, val, { mono: true, size: S.mono * 0.92, color: vc });
          else ctx.text(mx + ww + size * 0.25, by0 + size * 0.8, val, { mono: true, size: S.mono * 0.92, color: vc });
          return;
        }
        var cands = [], steps = 14, span = Math.max(0, fr.x1 - fr.x0 - tw - 8);
        for (var k = 0; k <= steps; k++) {
          var cx = fr.x1 - tw - span * k / steps;
          cands.push({ x: cx, y: y - S.hand * 0.42 - size * 0.8 });
          cands.push({ x: cx, y: y + S.hand * 0.35 });
        }
        // keep clear of the points an annotation will point at
        var targets = [].concat(ctx.spec.annotate || []).map(function (a) { return a && findAnchor(ctx, a.at); }).filter(Boolean);
        var box = bestBox(ctx, tw, size, cands, null, function (b) {
          var c = 0;
          targets.forEach(function (t) { if (t.x > b.x - 16 && t.x < b.x + b.w + 16 && t.y > b.y - 16 && t.y < b.y + b.h + 16) c += 900; });
          return c;
        });
        if (box.hits > 0) ctx.needRefRoom = Math.max(ctx.needRefRoom || 0, Math.max(ww, vw2) + 18);
        var wb = ctx.text(box.x, box.y + size * 0.8, word, { size: size, color: wc });
        ctx.text(wb.x + wb.w + size * 0.25, box.y + size * 0.8, val, { mono: true, size: S.mono * 0.92, color: vc });
      } else {
        var x = fr.x(r.value);
        ctx.op('over', function (p) { gapLine(p, ctx, x, fr.y0 - 4, x, fr.y1 + 2, { stroke: col, width: ctx.lw * (isT ? 1.05 : 1.2), passes: 1, dash: dash, rough: 0.5, opacity: 0.95 }); });
        var ty = fr.y0 - S.hand * 0.55;
        var anchor = x + tw / 2 > ctx.W ? 'end' : (x - tw / 2 < 0 ? 'start' : 'middle');
        var x0 = anchor === 'end' ? x + 4 - tw : anchor === 'start' ? x - 4 : x - tw / 2;
        var wb2 = ctx.text(x0, ty, word, { size: size, color: isT ? C['red-ink'] : C['graphite-soft'] });
        ctx.text(wb2.x + wb2.w + size * 0.25, ty, val, { mono: true, size: S.mono * 0.92, color: isT ? C['red-ink'] : C.figure });
      }
    });
  }

  /* Headline: yours, the reference, and the signed difference. */
  function setHeadline(ctx, label, value) {
    var r = refsOf(ctx);
    if (!r.length || !isNum(value)) return;
    var ref = r[r.length - 1];
    ctx.headline = { label: label, value: value, refLabel: ref.label || ref.kind, refValue: ref.value, kind: ref.kind };
  }

  function bestBox(ctx, w, h, cands, avoid, extra) {
    var best = cands[0], bs = Infinity;
    cands.forEach(function (c, k) {
      var b = { x: c.x, y: c.y, w: w, h: h }, s = k * 3 + (extra ? extra(b) : 0);
      var out = Math.max(0, -b.x) + Math.max(0, b.x + w - ctx.W) + Math.max(0, -b.y) + Math.max(0, b.y + h - ctx.H);
      s += out * 400;
      var pad = { x: b.x - 3, y: b.y - 2, w: w + 6, h: h + 4 };
      ctx.occupied.forEach(function (o) { s += overlap(pad, o); });
      if (avoid) s += overlap(pad, avoid) * 4;
      if (s < bs) { bs = s; best = b; best.hits = s - k * 3; }
    });
    return { x: best.x, y: best.y, w: w, h: h, hits: best.hits || 0 };
  }

  function legend(ctx, items, y) {
    var S = ctx.S, x = 0, row = 0, sw = S.hand * 1.15, sh = S.hand * 0.66, lineH = S.hand * 1.4;
    items.forEach(function (it) {
      var w = sw + 7 + textW(it.name, S.small);
      if (x > 0 && x + w > ctx.W) { x = 0; row++; }
      var yy = y + row * lineH, bx = x;
      ctx.op('marks', function (p) {
        p.rect(bx, yy - sh, sw, sh, { width: 1.1, passes: 1, rough: 0.6, stroke: it.edge });
        shade(p, ctx, { x: bx, y: yy - sh, w: sw, h: sh }, it.color, { angle: it.angle, gap: Math.max(2.6, ctx.gap * 0.8) });
      });
      ctx.text(bx + sw + 7, yy, it.name, { size: S.small });
      x += w + S.hand * 1.1;
    });
    return (row + 1) * lineH + S.hand * 0.2;
  }

  /* Colored pencil on paper: a light wash, then hatching wide enough that
     the strokes read as strokes at chart size (the dense 'body' fill reads
     as a flat tint once a shape is larger than a planet). */
  function shade(p, ctx, shape, col, o) {
    o = o || {};
    var a = o.alpha != null ? o.alpha : 1, wash = (o.wash != null ? o.wash : 0.3) * a;
    var hatch = { fill: col, passes: 0, fillStyle: o.style || 'hatch', gap: o.gap || ctx.gap, angle: o.angle != null ? o.angle : ANGLES[0], fillOpacity: 0.95 * a };
    var washO = { fill: col, passes: 0, fillStyle: 'solid', fillOpacity: wash / 0.85 };
    if (shape.poly) {
      if (wash > 0) p.poly(shape.poly, washO);
      p.poly(shape.poly, hatch);
    } else if (shape.w > 0.6 && shape.h > 0.6) {
      if (wash > 0) p.rect(shape.x, shape.y, shape.w, shape.h, washO);
      p.rect(shape.x, shape.y, shape.w, shape.h, hatch);
    }
  }
  function bar(p, ctx, x, yz, w, yv, edge, col, o) {
    o = o || {};
    p.polyline([[x, yz], [x, yv], [x + w, yv], [x + w, yz]], { stroke: edge, width: ctx.lw, rough: 1.1, dash: o.est ? '6 5' : null, opacity: o.dim ? 0.7 : 0.92 });
    var top = Math.min(yv, yz), h = Math.abs(yz - yv);
    shade(p, ctx, { x: x, y: top, w: w, h: h }, col, { angle: o.angle, alpha: o.est ? 0.45 : (o.dim ? 0.55 : 1) });
  }
  function hbarShape(p, ctx, xz, y, xv, t, edge, col, o) {
    o = o || {};
    p.polyline([[xz, y - t / 2], [xv, y - t / 2], [xv, y + t / 2], [xz, y + t / 2]], { stroke: edge, width: ctx.lw, rough: 1.1, opacity: o.dim ? 0.7 : 0.92 });
    shade(p, ctx, { x: Math.min(xz, xv), y: y - t / 2, w: Math.abs(xv - xz), h: t }, col, { angle: o.angle, alpha: o.dim ? 0.55 : 1 });
  }

  function estIndex(ctx, labels) {
    var e = ctx.spec.forecastFrom != null ? ctx.spec.forecastFrom : ctx.spec.estimateFrom;
    if (e == null) return -1;
    var s = String(e).toLowerCase();
    for (var i = 0; i < labels.length; i++) if (String(labels[i]).toLowerCase() === s) return i;
    if (isNum(e) && e >= 0 && e < labels.length) return e;
    ctx.warn('forecastFrom "' + e + '" matches no label');
    return -1;
  }

  /* ================================================================== *
   * Chart types
   * ================================================================== */

  /* ---------- bar: vertical bars, values on the caps ---------- */
  TYPES.bar = function (ctx) {
    var D = ctx.D, S = ctx.S, C = ctx.C;
    if (D.series.length > 1) return TYPES.grouped(ctx);
    var ser = D.series[0], rows = [];
    D.labels.forEach(function (l, i) {
      var v = ser.values[i];
      if (isNum(v)) rows.push({ label: String(l), value: v, i: i }); else ctx.warn('no value for "' + l + '"; it was left out');
    });
    var hl = hlLabel(ctx, D.labels);
    rows = sortRows(ctx, rows, function (r) { return r.value; });
    var labels = rows.map(function (r) { return r.label; });
    var est = estIndex(ctx, labels);
    var dom = zeroDomain(ctx, rows.map(function (r) { return r.value; }), 'bars');
    var fr = frame(ctx, { lo: dom.lo, hi: dom.hi, fixedHi: dom.fixedHi, xLabels: labels, band: true, topRoom: S.mono * 1.4 });
    drawFrame(ctx, fr);
    var n = rows.length, band = (fr.x1 - fr.x0) / Math.max(1, n), bw = Math.min(band * 0.62, S.hand * 4.4);
    var shown = rows.map(function (r) { return ctx.fmt.v(r.value); });
    var fits = shown.every(function (s) { return textW(s, S.mono, true) <= band * 0.96; });
    var top = rows.reduce(function (a, r, i) { return r.value > rows[a].value ? i : a; }, 0);
    var xs = [];
    rows.forEach(function (r, i) {
      var cx = fr.x0 + band * (i + 0.5), x = cx - bw / 2, yv = fr.y(r.value), yz = fr.yBase;
      var isH = r.label === hl, dim = hl != null && !isH, isEst = est >= 0 && i >= est;
      var col = isH ? C.red : ctx.color(0), edge = isH ? C['red-frame'] : C.graphite;
      xs.push(cx);
      ctx.op('marks', function (p) { bar(p, ctx, x, yz, bw, yv, edge, col, { dim: dim, est: isEst }); });
      var ty = r.value >= 0 ? yv - S.mono * 0.55 : yv + S.mono * 1.2;
      if (fits || isH || i === top || i === n - 1) {
        ctx.text(cx, ty, shown[i], { mono: true, anchor: 'middle', color: isH ? C['red-ink'] : C.figure, weight: isH ? 700 : 400 });
      }
      var hb = { x: x, y: Math.min(yv, yz), w: bw, h: Math.abs(yz - yv) };
      ctx.occupy(hb);
      ctx.mark('rect', hb, { label: r.label, value: r.value, series: ser.name, shown: shown[i] });
      ctx.anchor([r.label, r.i], { x: cx, y: r.value >= 0 ? yv - S.mono * 1.5 : yv + S.mono * 1.6, mark: hb });
    });
    drawXLabels(ctx, fr, labels, xs, rows.map(function (r) { return r.label === hl; }));
    if (est >= 0) ctx.text(xs[est] - bw / 2, fr.y0 - S.tick * 0.2, 'estimate', { size: S.small, color: C['graphite-soft'] });
    refLines(ctx, fr, true);
    var mine = hl != null ? rows.filter(function (r) { return r.label === hl; })[0] : (looksOrdered(labels) ? rows[n - 1] : null);
    if (mine) setHeadline(ctx, mine.label, mine.value);
    ctx.table = { head: [xName(ctx), ser.name], rows: rows.map(function (r) { return [r.label, ctx.fmt.exact(r.value)]; }) };
  };

  function xName(ctx) { var x = ctx.spec.x; return (x && typeof x === 'object' && !Array.isArray(x) && x.label) || ''; }

  /* ---------- hbar: horizontal, sorted, labelled directly ---------- */
  TYPES.hbar = function (ctx) {
    var D = ctx.D, S = ctx.S, C = ctx.C, W = ctx.W;
    if (D.series.length > 1) ctx.warn('hbar draws one series; the first was used (stacked or grouped take more)');
    ctx.fmt.unitOnValues = true;
    var ser = D.series[0], rows = [];
    D.labels.forEach(function (l, i) { var v = ser.values[i]; if (isNum(v)) rows.push({ label: String(l), value: v, i: i }); });
    var hl = hlLabel(ctx, D.labels);
    rows = sortRows(ctx, rows, function (r) { return r.value; });
    var dom = zeroDomain(ctx, rows.map(function (r) { return r.value; }), 'bars');
    var labMax = Math.min(W * (ctx.narrow ? 0.4 : 0.32), max(rows.map(function (r) { return textW(r.label, S.hand); })));
    var lines = rows.map(function (r) { return wrap(r.label, S.hand, labMax).slice(0, 3); });
    labMax = max(lines.map(function (ls) { return max(ls.map(function (s) { return textW(s, S.hand); })); }));
    var shown = rows.map(function (r) { return ctx.fmt.v(r.value); });
    var valW = max(shown.map(function (s) { return textW(s, S.mono, true); }));
    var refs = refsOf(ctx);
    var top = ctx.notesRoom + (refs.length ? S.hand * 1.6 : S.hand * 0.25);
    var x0 = Math.ceil(labMax + 16), x1 = W - valW - 14;
    var X = function (v) { return x0 + (v - dom.lo) / (dom.hi - dom.lo || 1) * (x1 - x0); };
    var fr = { x0: x0, x1: x1, y0: top, x: X };
    var y = top, xz = X(0);
    var rowHs = lines.map(function (ls) { return Math.max(S.hand * 1.95, ls.length * S.hand + S.hand * 0.75); });
    ctx.H = Math.ceil(top + sum(rowHs) + S.hand * 0.3);
    fr.y1 = ctx.H - S.hand * 0.2;
    ctx.op('axes', function (p) { p.line(xz, top - 4, xz, fr.y1, { width: ctx.lw }); });
    rows.forEach(function (r, i) {
      var h = rowHs[i], yc = y + h / 2, t = Math.min(h * 0.56, S.hand * 1.25), xv = X(r.value);
      var isH = r.label === hl, dim = hl != null && !isH;
      var col = isH ? C.red : ctx.color(0), edge = isH ? C['red-frame'] : C.graphite;
      ctx.op('marks', function (p) { hbarShape(p, ctx, xz, yc, xv, t, edge, col, { dim: dim }); });
      lines[i].forEach(function (s, k) {
        ctx.text(x0 - 12, yc + S.hand * 0.32 + (k - (lines[i].length - 1) / 2) * S.hand * 0.98, s, { anchor: 'end', color: isH ? C['red-ink'] : C.graphite });
      });
      var tx = r.value >= 0 ? xv + 9 : xv - 9;
      ctx.text(tx, yc + S.mono * 0.33, shown[i], { mono: true, anchor: r.value >= 0 ? 'start' : 'end', color: isH ? C['red-ink'] : C.figure, weight: isH ? 700 : 400 });
      var hb = { x: Math.min(xz, xv), y: yc - t / 2, w: Math.abs(xv - xz), h: t };
      ctx.occupy(hb);
      ctx.mark('rect', hb, { label: r.label, value: r.value, series: ser.name, shown: shown[i] });
      ctx.anchor([r.label, r.i], { x: xv + textW(shown[i], S.mono, true) + 14, y: yc, mark: hb });
      y += h;
    });
    refLines(ctx, fr, false);
    if (hl != null) setHeadline(ctx, hl, rows.filter(function (r) { return r.label === hl; })[0].value);
    ctx.table = { head: [xName(ctx), ser.name], rows: rows.map(function (r) { return [r.label, ctx.fmt.exact(r.value)]; }) };
  };

  /* ---------- stacked: parts of a whole per category ---------- */
  TYPES.stacked = function (ctx) {
    var D = ctx.D, S = ctx.S, C = ctx.C, W = ctx.W;
    var series = D.series.slice();
    if (series.length > 6) {
      ctx.warn('more than six series; the smallest were folded into "other"');
      var keep = series.slice(0, 5), rest = series.slice(5);
      keep.push({ name: 'other', values: D.labels.map(function (l, j) { return sum(rest.map(function (s) { return s.values[j]; })); }) });
      series = keep;
    }
    var neg = false;
    var rows = D.labels.map(function (l, j) {
      var vals = series.map(function (s) { var v = s.values[j]; if (isNum(v) && v < 0) { neg = true; return 0; } return isNum(v) ? v : 0; });
      return { label: String(l), vals: vals, total: sum(vals), i: j };
    });
    if (neg) ctx.warn('stacked bars cannot show negative parts; negatives were drawn as zero (use grouped bars)');
    var hl = hlLabel(ctx, D.labels);
    rows = sortRows(ctx, rows, function (r) { return r.total; });
    var labels = rows.map(function (r) { return r.label; });
    var dom = zeroDomain(ctx, rows.map(function (r) { return r.total; }), 'bars');
    // direct labels at the right of the last stack; a legend only when they do not fit
    var nameW = max(series.map(function (s) { return textW(s.name, S.small); }));
    var direct = nameW + 22 < W * 0.3;
    var legendH = direct ? 0 : legend(ctx, series.map(function (s, k) { return { name: s.name, color: ctx.color(k), angle: ANGLES[k] }; }), S.small);
    var fr = frame(ctx, { lo: dom.lo, hi: dom.hi, fixedHi: dom.fixedHi, xLabels: labels, band: true, topRoom: S.mono * 1.4, right: direct ? nameW + 22 : 0, legendH: legendH });
    drawFrame(ctx, fr);
    var n = rows.length, band = (fr.x1 - fr.x0) / Math.max(1, n), bw = Math.min(band * 0.62, S.hand * 4.4), xs = [];
    rows.forEach(function (r, i) {
      var cx = fr.x0 + band * (i + 0.5), x = cx - bw / 2, isH = r.label === hl;
      xs.push(cx);
      var acc = 0, segs = [];
      r.vals.forEach(function (v, k) { segs.push({ k: k, v: v, a: acc, b: acc + v }); acc += v; });
      var yTop = fr.y(r.total), yz = fr.yBase;
      ctx.op('marks', function (p) {
        p.polyline([[x, yz], [x, yTop], [x + bw, yTop], [x + bw, yz]], { stroke: isH ? C['red-frame'] : C.graphite, width: ctx.lw, rough: 1.1 });
        segs.forEach(function (sg) {
          var ya = fr.y(sg.a), yb = fr.y(sg.b);
          shade(p, ctx, { x: x, y: yb, w: bw, h: ya - yb }, ctx.color(sg.k), { angle: ANGLES[sg.k] });
          if (sg.k < segs.length - 1 && sg.v > 0) p.line(x, yb, x + bw, yb, { width: ctx.lw * 0.7, passes: 1, rough: 0.6, opacity: 0.8 });
        });
      });
      segs.forEach(function (sg) {
        var ya = fr.y(sg.a), yb = fr.y(sg.b), sh = ctx.fmt.v(sg.v);
        var m = { x: x, y: yb, w: bw, h: ya - yb };
        ctx.mark('rect', m, { label: r.label, value: sg.v, series: series[sg.k].name, shown: sh });
        if (ya - yb >= S.mono * 1.45 && textW(sh, S.mono * 0.86, true) <= bw - 8) {
          ctx.text(cx, (ya + yb) / 2 + S.mono * 0.3, sh, { mono: true, size: S.mono * 0.86, anchor: 'middle', color: C.figure, weight: 400, free: true });
        }
      });
      var tot = ctx.fmt.v(r.total);
      ctx.text(cx, yTop - S.mono * 0.55, tot, { mono: true, anchor: 'middle', color: isH ? C['red-ink'] : C.figure, weight: 700 });
      var hb = { x: x, y: yTop, w: bw, h: yz - yTop };
      ctx.occupy(hb);
      ctx.anchor([r.label, r.i], { x: cx, y: yTop - S.mono * 1.5, mark: hb });
    });
    if (direct && n) {
      var last = rows[n - 1], lx = xs[n - 1] + bw / 2 + 10, acc2 = 0;
      var items = last.vals.map(function (v, k) { var a = acc2; acc2 += v; return { k: k, pos: (fr.y(a) + fr.y(a + v)) / 2, want: (fr.y(a) + fr.y(a + v)) / 2, size: S.small * 1.05 }; });
      spread(items, 1, fr.y0, fr.y1);
      items.forEach(function (it) {
        var bx = lx;
        if (Math.abs(it.pos - it.want) > 3) ctx.op('marks', function (p) { p.line(bx - 7, it.want, bx + 4, it.pos - S.small * 0.3, { width: 0.9, passes: 1, opacity: 0.6, rough: 0.4 }); });
        ctx.text(bx + (Math.abs(it.pos - it.want) > 3 ? 7 : 0), it.pos + S.small * 0.3, series[it.k].name, { size: S.small, color: C.graphite });
      });
    }
    drawXLabels(ctx, fr, labels, xs, rows.map(function (r) { return r.label === hl; }));
    refLines(ctx, fr, true);
    var mine = hl != null ? rows.filter(function (r) { return r.label === hl; })[0] : (looksOrdered(labels) ? rows[n - 1] : null);
    if (mine) setHeadline(ctx, mine.label, mine.total);
    ctx.table = {
      head: [xName(ctx)].concat(series.map(function (s) { return s.name; })).concat(['total']),
      rows: rows.map(function (r) { return [r.label].concat(r.vals.map(ctx.fmt.exact)).concat([ctx.fmt.exact(r.total)]); })
    };
  };

  /* ---------- grouped: side by side per category ---------- */
  TYPES.grouped = function (ctx) {
    var D = ctx.D, S = ctx.S, C = ctx.C;
    var series = D.series.slice(0, 5);
    if (D.series.length > 5) ctx.warn('more than five series side by side do not read; the first five were drawn');
    var rows = D.labels.map(function (l, j) {
      return { label: String(l), vals: series.map(function (s) { return s.values[j]; }), i: j };
    });
    var hl = hlLabel(ctx, D.labels);
    rows = sortRows(ctx, rows, function (r) { return max(r.vals.filter(isNum).concat([0])); });
    var labels = rows.map(function (r) { return r.label; });
    var all = []; rows.forEach(function (r) { r.vals.forEach(function (v) { if (isNum(v)) all.push(v); }); });
    var dom = zeroDomain(ctx, all, 'bars');
    var legendH = legend(ctx, series.map(function (s, k) { return { name: s.name, color: ctx.color(k), angle: ANGLES[k] }; }), S.small);
    var fr = frame(ctx, { lo: dom.lo, hi: dom.hi, fixedHi: dom.fixedHi, xLabels: labels, band: true, topRoom: S.mono * 1.4, legendH: legendH });
    drawFrame(ctx, fr);
    var n = rows.length, k = series.length, band = (fr.x1 - fr.x0) / Math.max(1, n);
    var gw = Math.min(band * 0.8, S.hand * 2.7 * k), bw = (gw - (k - 1) * 3) / k, xs = [];
    var vs = S.mono * (bw < S.mono * 2.6 ? 0.82 : 0.92);
    var fits = rows.every(function (r) { return r.vals.every(function (v) { return !isNum(v) || textW(ctx.fmt.v(v), vs, true) <= bw + 6; }); });
    rows.forEach(function (r, i) {
      var cx = fr.x0 + band * (i + 0.5), gx = cx - gw / 2, isH = r.label === hl;
      xs.push(cx);
      r.vals.forEach(function (v, s) {
        if (!isNum(v)) return;
        var x = gx + s * (bw + 3), yv = fr.y(v), yz = fr.yBase, sh = ctx.fmt.v(v);
        ctx.op('marks', function (p) { bar(p, ctx, x, yz, bw, yv, isH ? C['red-frame'] : C.graphite, ctx.color(s), { angle: ANGLES[s] }); });
        if (fits) ctx.text(x + bw / 2, (v >= 0 ? yv - vs * 0.5 : yv + vs * 1.2), sh, { mono: true, size: vs, anchor: 'middle', color: isH ? C['red-ink'] : C.figure, weight: 400 });
        var hb = { x: x, y: Math.min(yv, yz), w: bw, h: Math.abs(yz - yv) };
        ctx.occupy(hb);
        ctx.mark('rect', hb, { label: r.label, value: v, series: series[s].name, shown: sh });
        ctx.anchor([series[s].name + ':' + r.label], { x: x + bw / 2, y: yv - vs * 1.5, mark: hb });
      });
      var tallest = max(r.vals.filter(isNum).concat([0]));
      ctx.anchor([r.label, r.i], { x: cx, y: fr.y(tallest) - S.mono * 1.5, mark: { x: gx, y: fr.y(tallest), w: gw, h: fr.yBase - fr.y(tallest) } });
    });
    drawXLabels(ctx, fr, labels, xs, rows.map(function (r) { return r.label === hl; }));
    refLines(ctx, fr, true);
    ctx.table = {
      head: [xName(ctx)].concat(series.map(function (s) { return s.name; })),
      rows: rows.map(function (r) { return [r.label].concat(r.vals.map(ctx.fmt.exact)); })
    };
  };

  /* ---------- line and area ---------- */
  var ROLE_PLAN = /plan|forecast|estimate|target|budget|projection|goal|expected/;
  var ROLE_BENCH = /bench|reference|baseline|average|market|peer|industry/;
  var ROLE_OLD = /old|superseded|previous|former|outdated/;
  var ROLE_ACTUAL = /actual|real|computed|result|measured/;
  function seriesStyles(ctx, series, hlS, isArea) {
    var C = ctx.C, roles = series.map(function (s) { return String(s.role || '').toLowerCase(); });
    var hasBench = roles.some(function (r) { return ROLE_BENCH.test(r); });
    var pal = C.pencils.filter(function (c) { return !(hasBench && c === C.blue); });
    var k = 0, single = series.length === 1;
    return series.map(function (s, i) {
      var r = roles[i];
      var st = { w: ctx.lw * 1.2, dash: null, band: true, glow: false, color: null, core: C.graphite, coreOp: 0.72, op: 0.9, label: C.graphite, fill: null };
      if (ROLE_PLAN.test(r) || s.dashed) st.dash = '7 6';
      if (ROLE_OLD.test(r)) { st.color = C.graphite; st.dash = st.dash || '5 6'; st.op = 0.25; st.band = false; st.coreOp = 0.25; st.label = C['graphite-soft']; }
      else if (ROLE_BENCH.test(r)) { st.color = C.blue; st.coreOp = 0.4; }
      else if (ROLE_ACTUAL.test(r) || (single && !r)) {
        if (ctx.night) { st.color = C.gold; st.glow = true; st.band = false; st.w = ctx.lw * 1.3; }
        else if (ROLE_ACTUAL.test(r)) { st.color = C.graphite; st.band = false; st.w = ctx.lw * 1.35; }
        else st.color = pal[k++ % pal.length];
      } else st.color = s.color ? (C[s.color] || s.color) : pal[k++ % pal.length];
      st.fill = isArea ? (st.glow ? C.gold : (st.band || st.color === C.blue ? st.color : ctx.color(i))) : null;
      if (hlS >= 0) {
        if (i === hlS) { st.color = C.red; st.core = C['red-frame']; st.label = C['red-ink']; st.w *= 1.15; st.glow = false; st.band = true; st.fill = isArea ? C.red : null; }
        else { st.op *= 0.5; st.coreOp *= 0.45; st.label = C['graphite-soft']; }
      }
      return st;
    });
  }
  function strokeSeries(p, ctx, pts, st, dash) {
    if (pts.length < 2) return;
    var C = ctx.C;
    if (st.glow) {
      var d = wobblePath(pts, p.random, 0.35);
      p.path(d, { stroke: st.color, width: st.w * 5, opacity: 0.07, passes: 1, dash: dash });
      p.path(d, { stroke: st.color, width: st.w * 2.4, opacity: 0.16, passes: 1, dash: dash });
      p.path(d, { stroke: st.color, width: st.w, opacity: 1, passes: 1, dash: dash });
      p.path(d, { stroke: C.ink, width: st.w * 0.35, opacity: 0.5, passes: 1, dash: dash });
      return;
    }
    if (st.band) p.path(wobblePath(pts, p.random, 0.9), { stroke: st.color, width: st.w * 2.6, opacity: st.op * 0.95, passes: 1, dash: dash });
    p.path(wobblePath(pts, p.random, 0.8), { stroke: st.band ? st.core : st.color, width: st.band ? st.w * 0.7 : st.w, opacity: st.band ? st.coreOp : st.op, passes: 1, dash: dash });
    if (!st.band && !dash) p.path(wobblePath(pts, p.random, 1), { stroke: st.color, width: st.w * 0.6, opacity: st.op * 0.45, passes: 1 });
  }

  function lineChart(ctx, isArea) {
    var D = ctx.D, S = ctx.S, C = ctx.C, W = ctx.W;
    var series = D.series.slice(0, 7);
    if (D.series.length > 7) ctx.warn('more than seven lines do not read; the first seven were drawn (use small multiples)');
    var labels = D.labels.map(String), n = labels.length;
    if (n < 2) ctx.warn('a line needs at least two points');
    var numericX = n > 1 && D.labels.every(function (l) { return isNum(toNum(l)); });
    var xv = numericX ? D.labels.map(toNum) : null;
    var hlS = -1;
    if (ctx.spec.highlight != null) {
      var hs = String(ctx.spec.highlight && ctx.spec.highlight.series != null ? ctx.spec.highlight.series : ctx.spec.highlight).toLowerCase();
      series.forEach(function (s, i) { if (s.name.toLowerCase() === hs) hlS = i; });
    }
    var hlX = hlS < 0 ? hlIndex(ctx, labels) : -1;
    var hlXSeries = 0;
    if (ctx.spec.highlight && typeof ctx.spec.highlight === 'object' && ctx.spec.highlight.series != null) {
      series.forEach(function (s, i) { if (s.name.toLowerCase() === String(ctx.spec.highlight.series).toLowerCase()) hlXSeries = i; });
      hlX = hlIndex(ctx, labels);
      hlS = -1;
    }
    var styles = seriesStyles(ctx, series, hlS, isArea);
    var stacked = isArea && series.length > 1;
    var tops = series.map(function (s) { return s.values.slice(); });
    if (stacked) {
      var neg = false;
      for (var j = 0; j < n; j++) {
        var acc = 0;
        for (var i = 0; i < series.length; i++) {
          var v = series[i].values[j];
          if (isNum(v) && v < 0) { neg = true; v = 0; }
          acc += isNum(v) ? v : 0;
          tops[i][j] = acc;
        }
      }
      if (neg) ctx.warn('stacked areas cannot show negative values; they were drawn as zero');
    }
    var all = [];
    tops.forEach(function (t) { t.forEach(function (v) { if (isNum(v)) all.push(v); }); });
    if (!all.length) { ctx.warn('no numbers to draw'); all = [0, 1]; }
    var dom = isArea ? zeroDomain(ctx, all, 'areas') : lineDomain(ctx, all);
    var multi = series.length > 1;
    var lastIdx = series.map(function (s, i) { for (var j = n - 1; j >= 0; j--) if (isNum(tops[i][j])) return j; return -1; });
    var endTexts = series.map(function (s, i) { var li = lastIdx[i]; return li < 0 ? null : { name: multi ? s.name : '', val: ctx.fmt.v(series[i].values[li]) }; });
    var endW = max(endTexts.map(function (e) { return e ? (e.name ? textW(e.name, S.small) + 6 : 0) + textW(e.val, S.mono, true) : 0; }).concat([0]));
    var useLegend = multi && endW + 18 > W * 0.36;
    var legendH = 0;
    if (useLegend) {
      legendH = legend(ctx, series.map(function (s, i) { return { name: s.name, color: styles[i].fill || styles[i].color, angle: ANGLES[i], edge: styles[i].color }; }), S.small);
      endTexts.forEach(function (e) { if (e) e.name = ''; });
      endW = max(endTexts.map(function (e) { return e ? textW(e.val, S.mono, true) : 0; }).concat([0]));
    }
    var est = estIndex(ctx, labels);
    var fr = frame(ctx, { lo: dom.lo, hi: dom.hi, fixedHi: dom.fixedHi, fixedLo: dom.fixedLo, xLabels: labels, band: false, inset: S.hand * 0.4, right: endW + 18, legendH: legendH, topRoom: S.mono * 1.1 });
    drawFrame(ctx, fr);
    var xmin = numericX ? min(xv) : 0, xmax = numericX ? max(xv) : n - 1;
    var X = function (j) { var t = numericX ? (xv[j] - xmin) / (xmax - xmin || 1) : (n > 1 ? j / (n - 1) : 0.5); return fr.x0 + fr.inset + t * (fr.x1 - fr.x0 - fr.inset * 2); };
    var xs = labels.map(function (l, j) { return X(j); });
    function ptsOf(arr, from, to) {
      var out = [], segs = [];
      for (var j = from; j <= to; j++) {
        if (isNum(arr[j])) out.push([xs[j], fr.y(arr[j])]);
        else if (out.length) { segs.push(out); out = []; }
      }
      if (out.length) segs.push(out);
      return segs;
    }
    // areas: hatched bands from the baseline (or the series below) up to the line
    if (isArea) {
      series.forEach(function (s, i) {
        var st = styles[i], lowArr = i > 0 && stacked ? tops[i - 1] : null;
        var polyFor = function (from, to) {
          var up = [];
          for (var j = from; j <= to; j++) if (isNum(tops[i][j])) up.push([xs[j], fr.y(tops[i][j]), j]);
          if (up.length < 2) return null;
          var poly = up.map(function (q) { return [q[0], q[1]]; });
          for (var b = up.length - 1; b >= 0; b--) poly.push([up[b][0], lowArr ? fr.y(lowArr[up[b][2]] || 0) : fr.yBase]);
          return poly;
        };
        var a = hlS >= 0 && hlS !== i ? 0.5 : 1;
        // estimates are shaded lighter than what happened
        [[0, est >= 0 ? est : n - 1, a], [est, n - 1, a * 0.42]].forEach(function (seg) {
          if (seg[0] < 0) return;
          var poly = polyFor(seg[0], seg[1]);
          if (poly) ctx.op('marks', function (p) { shade(p, ctx, { poly: poly }, st.fill, { angle: ANGLES[i], alpha: seg[2] * (ctx.night ? 0.8 : 1), wash: 0.26 }); });
        });
      });
    }
    series.forEach(function (s, i) {
      var st = styles[i], arr = tops[i];
      var solidTo = est >= 0 ? est : n - 1;
      ptsOf(arr, 0, solidTo).forEach(function (seg) { ctx.op('marks', function (p) { strokeSeries(p, ctx, seg, st, st.dash); }); });
      if (est >= 0) ptsOf(arr, est, n - 1).forEach(function (seg) { ctx.op('marks', function (p) { strokeSeries(p, ctx, seg, st, '7 6'); }); });
      for (var j = 0; j < n; j++) {
        if (!isNum(arr[j])) continue;
        var px = xs[j], py = fr.y(arr[j]), sh = ctx.fmt.v(series[i].values[j]);
        ctx.mark('circle', { cx: px, cy: py, r: Math.max(10, S.hand * 0.55) }, { label: labels[j], value: series[i].values[j], series: s.name, shown: sh });
        ctx.anchor([s.name + ':' + labels[j]].concat(i === (hlS >= 0 ? hlS : 0) ? [labels[j], j] : []), { x: px, y: py - S.mono * 0.8, mark: { x: px - 4, y: py - 4, w: 8, h: 8 } });
        if (n <= 16 && !st.glow) {
          (function (px, py, last) {
            ctx.op('marks', function (p) { p.dot(px, py, last ? S.hand * 0.5 : S.hand * 0.26, { fill: last ? st.color : C.graphite, stroke: C.graphite, width: 0.9, opacity: st.op }); });
          })(px, py, j === lastIdx[i]);
        } else if (j === lastIdx[i]) {
          (function (px, py) { ctx.op('marks', function (p) { p.dot(px, py, S.hand * 0.5, { fill: st.color, stroke: st.glow ? st.color : C.graphite, width: 0.9 }); }); })(px, py);
        }
      }
    });
    // the lines are in the way of notes and reference labels: occupy small boxes along them
    series.forEach(function (s, i) {
      var prev = null;
      for (var j = 0; j < n; j++) {
        if (!isNum(tops[i][j])) { prev = null; continue; }
        var pt = [xs[j], fr.y(tops[i][j])];
        if (prev) {
          var steps = Math.max(1, Math.round(Math.hypot(pt[0] - prev[0], pt[1] - prev[1]) / 9));
          for (var q = 0; q < steps; q++) ctx.occupy({ x: prev[0] + (pt[0] - prev[0]) * q / steps - 3, y: prev[1] + (pt[1] - prev[1]) * q / steps - 3, w: 6, h: 6 });
        }
        prev = pt;
      }
    });
    // end labels: name and last value at the end of each line, pushed apart, with a leader when moved
    var ends = [];
    series.forEach(function (s, i) {
      if (!endTexts[i]) return;
      var j = lastIdx[i], yy = fr.y(tops[i][j]);
      if (stacked) yy = (fr.y(tops[i][j]) + (i > 0 ? fr.y(tops[i - 1][j]) : fr.yBase)) / 2;
      ends.push({ i: i, j: j, want: yy, pos: yy, size: S.hand * 1.02 });
    });
    spread(ends, 1, fr.y0 - S.hand * 0.3, fr.y1 + S.hand * 0.2);
    ends.forEach(function (e) {
      var ex = xs[e.j] + S.hand * 0.55, et = endTexts[e.i], st = styles[e.i], moved = Math.abs(e.pos - e.want) > 4;
      var lx = ex + (moved ? 10 : 0);
      if (moved) ctx.op('notes', function (p) { p.line(ex - 2, e.want, lx - 3, e.pos - S.hand * 0.25, { width: 0.9, passes: 1, opacity: 0.55, rough: 0.4 }); });
      var x = lx;
      if (et.name) { var nb = ctx.text(x, e.pos + S.hand * 0.3, et.name, { size: S.small, color: st.label }); x = nb.x + nb.w + 6; }
      ctx.text(x, e.pos + S.hand * 0.3, et.val, { mono: true, color: hlS === e.i ? C['red-ink'] : C.figure, weight: hlS === e.i || !multi ? 700 : 400 });
    });
    // a single line also says where it started
    if (!multi && n > 2 && isNum(tops[0][0])) {
      var fy = fr.y(tops[0][0]);
      ctx.text(xs[0], fy - S.mono * 0.75, ctx.fmt.v(series[0].values[0]), { mono: true, anchor: 'start', color: C.figure, weight: 400 });
    }
    if (hlX >= 0 && isNum(tops[hlXSeries][hlX])) {
      var hx = xs[hlX], hy = fr.y(tops[hlXSeries][hlX]), r0 = S.hand * 0.95;
      ctx.op('over', function (p) { p.ellipse(hx, hy, r0 * 2, r0 * 1.7, { stroke: C.red, width: ctx.lw * 1.05, passes: 2, rough: 1.2 }); });
      var cands = [{ x: hx - 30, y: hy - r0 - S.mono * 1.6 }, { x: hx - 30, y: hy + r0 + 4 }, { x: hx + r0 + 4, y: hy - S.mono * 0.5 }];
      var vt = ctx.fmt.v(series[hlXSeries].values[hlX]), vw = textW(vt, S.mono, true);
      cands.forEach(function (c) { c.x = c.x === hx - 30 ? hx - vw / 2 : c.x; });
      var vb = bestBox(ctx, vw, S.mono, cands);
      ctx.text(vb.x, vb.y + S.mono * 0.78, vt, { mono: true, color: C['red-ink'], weight: 700 });
      ctx.occupy({ x: hx - r0, y: hy - r0, w: r0 * 2, h: r0 * 2 });
    }
    if (est >= 0) {
      var ex0 = xs[est];
      ctx.op('guides', function (p) { p.line(ex0, fr.y0 - 2, ex0, fr.y1, { width: 0.9, passes: 1, opacity: 0.3, dash: '2 5', rough: 0.3 }); });
      ctx.text(ex0 + 6, fr.y0 + S.small * 0.2, 'forecast', { size: S.small, color: C['graphite-soft'] });
    }
    var xls = labels.map(function () { return false; });
    if (hlX >= 0) xls[hlX] = true;
    drawXLabels(ctx, fr, labels, xs, xls);
    refLines(ctx, fr, true);
    // the headline: yours against the reference, at the last point both have
    var roleOf = function (re) { for (var q = 0; q < series.length; q++) if (re.test(String(series[q].role || '').toLowerCase())) return q; return -1; };
    var mineI = hlS >= 0 ? hlS : roleOf(ROLE_ACTUAL), refI = roleOf(ROLE_PLAN);
    if (refI < 0 || refI === mineI) refI = roleOf(ROLE_BENCH);
    if (mineI >= 0 && refI >= 0 && mineI !== refI && !stacked) {
      for (var jj = n - 1; jj >= 0; jj--) {
        if (isNum(series[mineI].values[jj]) && isNum(series[refI].values[jj])) {
          ctx.headline = { label: labels[jj] + ' ' + series[mineI].name, value: series[mineI].values[jj], refLabel: series[refI].name, refValue: series[refI].values[jj] };
          break;
        }
      }
    } else if (!multi && lastIdx[0] >= 0) setHeadline(ctx, labels[lastIdx[0]], series[0].values[lastIdx[0]]);
    else if (hlS >= 0 && lastIdx[hlS] >= 0) setHeadline(ctx, series[hlS].name, series[hlS].values[lastIdx[hlS]]);
    ctx.table = {
      head: [xName(ctx)].concat(series.map(function (s) { return s.name; })),
      rows: labels.map(function (l, j) { return [l].concat(series.map(function (s) { return ctx.fmt.exact(s.values[j]); })); })
    };
  }
  TYPES.line = function (ctx) { lineChart(ctx, false); };
  TYPES.area = function (ctx) { lineChart(ctx, true); };

  /* ---------- pie and donut: at most five slices, labels on the slices ---------- */
  function arcPts(cx, cy, r, a0, a1) {
    var n = Math.max(2, Math.ceil(Math.abs(a1 - a0) / 0.05)), out = [];
    for (var i = 0; i <= n; i++) { var a = a0 + (a1 - a0) * i / n; out.push([cx + r * Math.sin(a), cy - r * Math.cos(a)]); }
    return out;
  }
  function inWedge(x, y, cx, cy, r0, r1, a0, a1) {
    var dx = x - cx, dy = y - cy, rr = Math.hypot(dx, dy);
    if (rr < r0 || rr > r1) return false;
    var a = Math.atan2(dx, -dy); if (a < 0) a += Math.PI * 2;
    return a >= a0 && a <= a1;
  }
  function pieChart(ctx, donut) {
    var D = ctx.D, S = ctx.S, C = ctx.C, W = ctx.W, sp = ctx.spec;
    if (D.series.length > 1) ctx.warn('a pie shows one series; the first was used');
    ctx.fmt.unitOnValues = true;
    var rows = [];
    D.labels.forEach(function (l, i) { var v = D.series[0].values[i]; if (isNum(v)) rows.push({ label: String(l), value: v, i: i }); });
    if (rows.some(function (r) { return r.value < 0; })) {
      ctx.warn('a pie cannot show negative values; drawn as horizontal bars instead');
      return TYPES.hbar(ctx);
    }
    var total = sum(rows.map(function (r) { return r.value; }));
    var whole = sp.total != null ? toNum(sp.total) : (ctx.fmt.unit === '%' ? 100 : null);
    if (whole != null) {
      if (total > whole * 1.005) {
        ctx.warn('the slices add up to ' + f2(total) + ', more than the whole (' + whole + '); answers that allow several choices belong in a bar chart, drawn as horizontal bars');
        return TYPES.hbar(ctx);
      }
      if (total < whole * 0.995) {
        ctx.warn('the slices add up to ' + f2(total) + ' of ' + whole + '; the rest is drawn as "not accounted for"');
        rows.push({ label: 'not accounted for', value: whole - total, i: -1, rest: true });
        total = whole;
      }
    }
    rows = sortRows(ctx, rows.filter(function (r) { return !r.rest; }), function (r) { return r.value; }).concat(rows.filter(function (r) { return r.rest; }));
    if (rows.filter(function (r) { return !r.rest; }).length > 5) {
      var named = rows.filter(function (r) { return !r.rest; }), keep = named.slice(0, 4), fold = named.slice(4);
      ctx.warn('more than five slices; ' + fold.length + ' small ones were grouped as "other"');
      keep.push({ label: 'other (' + fold.length + ')', value: sum(fold.map(function (r) { return r.value; })), i: -2, other: true, parts: fold });
      rows = keep.concat(rows.filter(function (r) { return r.rest; }));
    }
    var hl = hlLabel(ctx, rows.map(function (r) { return r.label; }));
    if (!ctx.H) ctx.H = Math.round(clamp(W * (ctx.narrow ? 0.95 : 0.52), 280, 470));
    var top = ctx.notesRoom + S.hand * 0.3, H = ctx.H, cy = top + (H - top) / 2, cx = W / 2;
    var rMax = Math.min((H - top) / 2 - S.hand * 0.6, W / 2 - 6);
    var a = 0, slices = rows.map(function (r, k) {
      var sw = total > 0 ? r.value / total * Math.PI * 2 : 0, s = { r: r, a0: a, a1: a + sw, k: k };
      a += sw;
      s.name = r.label;
      s.val = sp.show === 'value' || ctx.fmt.unit === '%' ? ctx.fmt.u(r.value) : ctx.fmt.pct(r.value / total);
      s.col = r.rest ? C['graphite-faint'] : (r.label === hl ? C.red : (r.other ? C['graphite-soft'] : ctx.color(k)));
      return s;
    });
    function fitsInside(s, r0, r1) {
      var mid = (s.a0 + s.a1) / 2, rl = r0 > 0 ? (r0 + r1) / 2 : r1 * 0.6;
      var lx = cx + rl * Math.sin(mid), ly = cy - rl * Math.cos(mid);
      var w = Math.max(textW(s.name, S.small), textW(s.val, S.mono * 0.92, true)) + 6, h = S.small * 2.1;
      var pts = [[lx - w / 2, ly - h / 2], [lx + w / 2, ly - h / 2], [lx - w / 2, ly + h / 2], [lx + w / 2, ly + h / 2]];
      return pts.every(function (q) { return inWedge(q[0], q[1], cx, cy, r0 + 2, r1 - 3, s.a0, s.a1); });
    }
    var rr = rMax, ri = donut ? rr * 0.56 : 0;
    var outside = slices.filter(function (s) { return !fitsInside(s, ri, rr); });
    var listBelow = false;
    if (outside.length) {
      var outW = max(outside.map(function (s) { return textW(s.name + ' ', S.small) + textW(s.val, S.mono * 0.92, true); }));
      var rFit = W / 2 - outW - S.hand * 1.6;
      if (rFit >= rMax * 0.62) {
        rr = Math.min(rMax, rFit); ri = donut ? rr * 0.56 : 0;
        outside = slices.filter(function (s) { return !fitsInside(s, ri, rr); });
      } else listBelow = true;
    }
    if (listBelow) {
      cy = top + rr + S.hand * 0.4;
      ctx.H = Math.ceil(cy + rr + S.hand * 1.5 + outside.length * S.hand * 1.3);
    }
    // fills, spokes, rim
    slices.forEach(function (s) {
      if (s.a1 - s.a0 <= 0) return;
      var poly = donut ? arcPts(cx, cy, rr, s.a0, s.a1).concat(arcPts(cx, cy, ri, s.a1, s.a0)) : [[cx, cy]].concat(arcPts(cx, cy, rr, s.a0, s.a1));
      var alpha = (hl != null && s.r.label !== hl ? 0.6 : 1) * (s.r.other ? 0.55 : 1);
      ctx.op('marks', function (p) { shade(p, ctx, { poly: poly }, s.col, { angle: ANGLES[s.k % ANGLES.length], alpha: alpha, wash: s.r.rest ? 0 : 0.3 }); });
      var mid = (s.a0 + s.a1) / 2;
      ctx.mark('path', { d: 'M' + poly.map(function (q) { return f2(q[0]) + ' ' + f2(q[1]); }).join('L') + 'Z' },
        { label: s.r.label, value: s.r.value, series: D.series[0].name, shown: s.val });
      ctx.anchor([s.r.label, s.r.i], { x: cx + rr * 1.02 * Math.sin(mid), y: cy - rr * 1.02 * Math.cos(mid), mark: { x: cx - rr * 0.3, y: cy - rr * 0.3, w: rr * 0.6, h: rr * 0.6 } });
    });
    ctx.op('marks', function (p) {
      p.circle(cx, cy, rr * 2, { width: ctx.lw, passes: 2, rough: 0.8 });
      if (donut) p.circle(cx, cy, ri * 2, { width: ctx.lw * 0.9, passes: 2, rough: 0.8 });
      if (slices.length > 1) slices.forEach(function (s) {
        if (s.a1 - s.a0 <= 0) return;
        p.line(cx + ri * Math.sin(s.a0), cy - ri * Math.cos(s.a0), cx + rr * Math.sin(s.a0), cy - rr * Math.cos(s.a0), { width: ctx.lw * 0.85, passes: 1, rough: 0.6 });
      });
    });
    var hlCol = function (s) { return s.r.label === hl ? C['red-ink'] : C.graphite; };
    ctx.occupy({ x: cx - rr, y: cy - rr, w: rr * 2, h: rr * 2 });
    slices.forEach(function (s) {
      if (outside.indexOf(s) >= 0) return;
      var mid = (s.a0 + s.a1) / 2, rl = ri > 0 ? (ri + rr) / 2 : rr * 0.6;
      var lx = cx + rl * Math.sin(mid), ly = cy - rl * Math.cos(mid);
      ctx.text(lx, ly - S.small * 0.12, s.name, { anchor: 'middle', size: S.small, color: hlCol(s), free: true });
      ctx.text(lx, ly + S.mono * 0.95, s.val, { anchor: 'middle', mono: true, size: S.mono * 0.92, color: s.r.label === hl ? C['red-ink'] : C.figure, free: true });
    });
    if (outside.length && !listBelow) {
      var sides = { l: [], r: [] };
      outside.forEach(function (s) {
        var mid = (s.a0 + s.a1) / 2, side = Math.sin(mid) >= 0 ? 'r' : 'l';
        sides[side].push({ s: s, mid: mid, want: cy - (rr + 12) * Math.cos(mid), pos: cy - (rr + 12) * Math.cos(mid), size: S.small * 1.1 });
      });
      ['l', 'r'].forEach(function (sd) {
        spread(sides[sd], 2, S.hand * 0.4, ctx.H - S.hand * 0.2);
        sides[sd].forEach(function (it) {
          var ex = cx + rr * Math.sin(it.mid), ey = cy - rr * Math.cos(it.mid);
          var lx = sd === 'r' ? cx + rr + S.hand * 0.9 : cx - rr - S.hand * 0.9;
          ctx.op('notes', function (p) { p.polyline([[ex, ey], [lx + (sd === 'r' ? -6 : 6), it.pos - S.small * 0.3]], { width: 0.9, passes: 1, opacity: 0.6, rough: 0.4 }); });
          var t = it.s.name + ' ', tw = textW(t, S.small);
          if (sd === 'r') { ctx.text(lx, it.pos, t, { size: S.small, color: hlCol(it.s) }); ctx.text(lx + tw, it.pos, it.s.val, { mono: true, size: S.mono * 0.92, color: C.figure }); }
          else { var vw = textW(it.s.val, S.mono * 0.92, true); ctx.text(lx, it.pos, it.s.val, { mono: true, size: S.mono * 0.92, color: C.figure, anchor: 'end' }); ctx.text(lx - vw - 4, it.pos, it.s.name, { size: S.small, color: hlCol(it.s), anchor: 'end' }); }
        });
      });
    } else if (listBelow) {
      var ly0 = cy + rr + S.hand * 1.5, sw = S.hand * 0.9;
      var listW = max(outside.map(function (s) { return sw + 16 + textW(s.name, S.small) + textW(s.val, S.mono * 0.92, true); }));
      var lx0 = Math.max(0, (W - listW) / 2);
      outside.forEach(function (s, q) {
        var yy = ly0 + q * S.hand * 1.3;
        ctx.op('marks', function (p) {
          p.rect(lx0, yy - sw * 0.7, sw, sw * 0.7, { width: 1, passes: 1, rough: 0.5 });
          shade(p, ctx, { x: lx0, y: yy - sw * 0.7, w: sw, h: sw * 0.7 }, s.col, { angle: ANGLES[s.k % ANGLES.length], gap: 2.8, alpha: s.r.other ? 0.55 : 1 });
        });
        var nb = ctx.text(lx0 + sw + 8, yy, s.name, { size: S.small, color: hlCol(s) });
        ctx.text(nb.x + nb.w + 8, yy, s.val, { mono: true, size: S.mono * 0.92, color: C.figure });
      });
    }
    if (donut) {
      var ct = sp.center != null ? String(sp.center) : ctx.fmt.u(total);
      ctx.text(cx, cy + S.mono * 0.3, ct, { anchor: 'middle', mono: true, size: Math.min(S.mono * 1.5, ri * 2 / Math.max(3, ct.length) / 0.62), color: C.figure, weight: 700, free: true });
      ctx.text(cx, cy + S.mono * 0.3 + S.small * 1.15, sp.centerLabel || 'in all', { anchor: 'middle', size: S.small, color: C['graphite-soft'], free: true });
    }
    var other = rows.filter(function (r) { return r.other; })[0];
    if (other) ctx.distortion = 'other: ' + other.parts.map(function (r) { return r.label; }).join(', ');
    ctx.table = {
      head: [xName(ctx), D.series[0].name, 'share'],
      rows: (other ? rows.filter(function (r) { return !r.other; }).concat(other.parts) : rows).map(function (r) { return [r.label, ctx.fmt.exact(r.value), ctx.fmt.pct(r.value / total)]; })
    };
  }
  TYPES.pie = function (ctx) { pieChart(ctx, false); };
  TYPES.donut = function (ctx) { pieChart(ctx, true); };

  /* ---------- scatter, with an optional least-squares trend ---------- */
  TYPES.scatter = function (ctx) {
    var S = ctx.S, C = ctx.C, W = ctx.W, sp = ctx.spec;
    var xc = sp.x && typeof sp.x === 'object' && !Array.isArray(sp.x) ? sp.x : {}, yc = sp.y && typeof sp.y === 'object' ? sp.y : {};
    var pts = [];
    (Array.isArray(sp.data) ? sp.data : []).forEach(function (d, i) {
      var p;
      if (Array.isArray(d)) p = typeof d[0] === 'string' && !isNum(toNum(d[0])) ? { label: d[0], x: toNum(d[1]), y: toNum(d[2]) } : { x: toNum(d[0]), y: toNum(d[1]), label: d[2] };
      else if (d && typeof d === 'object') p = { x: toNum(d.x), y: toNum(d.y), label: d.label || d.name };
      if (p && isNum(p.x) && isNum(p.y)) { p.i = i; pts.push(p); } else ctx.warn('point ' + (i + 1) + ' has no x and y; left out');
    });
    var fx = makeFormat({ format: sp.format, unit: xc.unit || '' }, pts.map(function (p) { return p.x; }));
    var fy = makeFormat({ format: sp.format, unit: yc.unit != null ? yc.unit : (sp.unit || '') }, pts.map(function (p) { return p.y; }));
    ctx.fmt = fy;
    var xsV = pts.map(function (p) { return p.x; }), ysV = pts.map(function (p) { return p.y; });
    var xlo = min(xsV), xhi = max(xsV), ylo = min(ysV), yhi = max(ysV);
    if (xlo >= 0 && xlo <= xhi * 0.35) xlo = 0;
    if (ylo >= 0 && ylo <= yhi * 0.35) ylo = 0;
    var xt = niceTicks(xlo, xhi, ctx.narrow ? 4 : 6), xtf = fx.tick(xt);
    var hlI = hlIndex(ctx, pts.map(function (p) { return p.label != null ? p.label : ''; }));
    var xTitle = [xc.label, xc.unit ? '(' + xc.unit + ')' : ''].filter(Boolean).join(' ');
    var fr = frame(ctx, { lo: ylo, hi: yhi, xLabels: null, right: S.hand * 0.8, xTitle: !!xTitle, caption: yCaption(ctx) });
    fr.y1 -= S.tick * 1.6;
    var nt = niceTicks(ylo, yhi, clamp(Math.round((fr.y1 - fr.y0) / (S.tick * 3.8)), 3, 6));
    fr.lo = nt.lo; fr.hi = nt.hi; fr.ticks = nt.ticks; fr.tf = fy.tick(nt); fr.zero = fr.lo <= 0 && fr.hi >= 0; fr.yBase = fr.y1;
    var X = function (v) { return fr.x0 + 6 + (v - xt.lo) / (xt.hi - xt.lo || 1) * (fr.x1 - fr.x0 - 6); };
    fr.zero = false;
    drawFrame(ctx, fr);
    xt.ticks.forEach(function (t) {
      var x = X(t);
      ctx.op('axes', function (p) { p.line(x, fr.y1 + 1, x, fr.y1 + 6, { width: 1.1, passes: 1, rough: 0.4, opacity: 0.7 }); });
      var s = xtf(t), w = textW(s, S.tick, true), yy = fr.y1 + S.tick * 1.6;
      var b = { x: x - w / 2 - 3, y: yy - S.tick * 0.8, w: w + 6, h: S.tick };
      if (ctx.occupied.some(function (o) { return overlap(b, o) > 0; })) return;
      ctx.text(x, yy, s, { mono: true, size: S.tick, anchor: 'middle', color: C['graphite-soft'], weight: 400 });
    });
    if (xTitle) ctx.text(fr.x1, fr.y1 + S.tick * 1.6 + S.hand * 1.15, xTitle, { anchor: 'end', size: S.small, color: C['graphite-soft'] });
    var d = clamp(S.hand * 0.55, 8, 13);
    if (sp.trend && pts.length > 2) {
      var n = pts.length, mx = sum(xsV) / n, my = sum(ysV) / n, sxx = 0, sxy = 0, syy = 0;
      pts.forEach(function (p) { sxx += (p.x - mx) * (p.x - mx); sxy += (p.x - mx) * (p.y - my); syy += (p.y - my) * (p.y - my); });
      if (sxx > 0) {
        var b = sxy / sxx, a0 = my - b * mx, r2 = syy > 0 ? (sxy * sxy) / (sxx * syy) : 0;
        var xa = min(xsV), xb = max(xsV), ya = a0 + b * xa, yb = a0 + b * xb;
        ctx.op('over', function (p) { p.line(X(xa), fr.y(ya), X(xb), fr.y(yb), { width: ctx.lw, passes: 1, dash: '7 6', rough: 0.5, opacity: 0.8 }); });
        var lbl = 'trend, r² ' + r2.toFixed(2), lw2 = textW(lbl, S.small) + 6;
        var tb = bestBox(ctx, lw2, S.small, [{ x: X(xb) - lw2, y: fr.y(yb) - S.small * 1.9 }, { x: X(xb) - lw2, y: fr.y(yb) + S.small * 0.6 }, { x: X(xa), y: fr.y(ya) + S.small * 0.6 }]);
        ctx.textMix(tb.x, tb.y + S.small * 0.8, lbl, { size: S.small, color: C['graphite-soft'] });
        ctx.trend = { slope: b, intercept: a0, r2: r2 };
      }
    }
    pts.forEach(function (p, k) {
      var px = X(p.x), py = fr.y(p.y), isH = k === hlI;
      ctx.op('marks', function (pen) { pen.dot(px, py, isH ? d * 1.35 : d, { fill: isH ? C.red : C.blue, stroke: isH ? C['red-frame'] : C.graphite, width: 1, fillOpacity: 0.95 }); });
      ctx.occupy({ x: px - d / 2, y: py - d / 2, w: d, h: d });
      ctx.mark('circle', { cx: px, cy: py, r: Math.max(10, d) }, { label: p.label != null ? p.label : '', value: p.y, x: p.x, series: yc.label || 'y', shown: fx.u(p.x) + ', ' + fy.u(p.y) });
      ctx.anchor([p.label != null ? p.label : '#' + k, k], { x: px, y: py - d * 0.6, mark: { x: px - d / 2, y: py - d / 2, w: d, h: d } });
    });
    var labelAll = sp.labels === true || (sp.labels !== false && pts.length <= 12);
    pts.forEach(function (p, k) {
      if (p.label == null || p.label === '') return;
      if (!labelAll && k !== hlI) return;
      var px = X(p.x), py = fr.y(p.y), size = S.small, w = textW(p.label, size);
      var cands = [{ x: px + d * 0.7, y: py - size * 0.55 }, { x: px - d * 0.7 - w, y: py - size * 0.55 }, { x: px - w / 2, y: py - d - size }, { x: px - w / 2, y: py + d * 0.6 }];
      var b = bestBox(ctx, w, size, cands);
      var hit = ctx.occupied.some(function (o) { return overlap({ x: b.x - 1, y: b.y, w: w + 2, h: size }, o) > 4; });
      if (hit && k !== hlI) return;
      ctx.text(b.x, b.y + size * 0.8, p.label, { size: size, color: k === hlI ? C['red-ink'] : C.graphite });
    });
    ctx.table = {
      head: ['', xTitle || 'x', yCaption(ctx) || 'y'],
      rows: pts.map(function (p) { return [p.label != null ? p.label : '', fx.exact(p.x), fy.exact(p.y)]; })
    };
  };

  /* ---------- slope: before and after ---------- */
  TYPES.slope = function (ctx) {
    var D = ctx.D, S = ctx.S, C = ctx.C, W = ctx.W, sp = ctx.spec;
    ctx.fmt.unitOnValues = true;
    var cols = D.series.length >= 2 ? [D.series[0].name, D.series[1].name] : ['before', 'after'];
    if (Array.isArray(sp.columns)) cols = sp.columns.map(String);
    if (D.series.length < 2) { ctx.warn('a slope chart needs two values per row'); }
    var rows = D.labels.map(function (l, j) { return { label: String(l), a: D.series[0].values[j], b: D.series[1] ? D.series[1].values[j] : null, i: j }; })
      .filter(function (r) { return isNum(r.a) && isNum(r.b); });
    var hl = hlLabel(ctx, D.labels);
    var all = []; rows.forEach(function (r) { all.push(r.a, r.b); });
    var lo = min(all), hi = max(all), pad = (hi - lo || 1) * 0.06;
    var nameW = max(rows.map(function (r) { return textW(r.label, S.small); }));
    var valW = max(rows.map(function (r) { return Math.max(textW(ctx.fmt.v(r.a), S.mono, true), textW(ctx.fmt.v(r.b), S.mono, true)); }));
    var namesRight = W >= 620;
    var xl = Math.min(W * 0.42, nameW + valW + S.hand * 1.4), xr = W - (namesRight ? Math.min(W * 0.3, nameW + valW + S.hand * 1.4) : valW + S.hand * 1.1);
    if (!ctx.H) ctx.H = Math.round(clamp(rows.length * S.hand * 2.1 + S.hand * 3, 260, 520));
    var y0 = ctx.notesRoom + S.hand * 2.2, y1 = ctx.H - S.hand * 0.8;
    var Y = function (v) { return y1 - (v - (lo - pad)) / ((hi + pad) - (lo - pad)) * (y1 - y0); };
    ctx.op('axes', function (p) { p.line(xl, y0 - S.hand * 0.4, xl, y1 + 4, { width: ctx.lw * 0.9 }); p.line(xr, y0 - S.hand * 0.4, xr, y1 + 4, { width: ctx.lw * 0.9 }); });
    ctx.text(xl, y0 - S.hand * 0.95, cols[0], { anchor: 'middle', color: C.ink, size: S.hand * 1.05 });
    ctx.text(xr, y0 - S.hand * 0.95, cols[1], { anchor: 'middle', color: C.ink, size: S.hand * 1.05 });
    var left = rows.map(function (r) { return { r: r, want: Y(r.a), pos: Y(r.a), size: S.hand * 1.02 }; });
    var right = rows.map(function (r) { return { r: r, want: Y(r.b), pos: Y(r.b), size: S.hand * 1.02 }; });
    spread(left, 1, y0 - S.hand * 0.2, y1 + S.hand * 0.4);
    spread(right, 1, y0 - S.hand * 0.2, y1 + S.hand * 0.4);
    rows.forEach(function (r, k) {
      var isH = r.label === hl, dim = hl != null && !isH;
      var col = isH ? C.red : (dim ? C['graphite-soft'] : C.graphite), w = isH ? ctx.lw * 1.6 : ctx.lw * (dim ? 0.8 : 1.05);
      var ya = Y(r.a), yb = Y(r.b);
      ctx.op('marks', function (p) {
        p.line(xl, ya, xr, yb, { stroke: col, width: w, passes: isH ? 2 : 1, opacity: dim ? 0.6 : 0.92, rough: 0.6 });
        p.dot(xl, ya, S.hand * 0.42, { fill: isH ? C.red : ctx.color(0), stroke: C.graphite, width: 0.9 });
        p.dot(xr, yb, S.hand * 0.42, { fill: isH ? C.red : ctx.color(0), stroke: C.graphite, width: 0.9 });
      });
      ctx.mark('path', { d: 'M' + f2(xl) + ' ' + f2(ya) + 'L' + f2(xr) + ' ' + f2(yb) }, { label: r.label, value: r.b, before: r.a, series: cols[1], shown: ctx.fmt.v(r.a) + ' to ' + ctx.fmt.v(r.b) });
      ctx.anchor([r.label, r.i], { x: (xl + xr) / 2, y: (ya + yb) / 2 - 6, mark: { x: xl, y: Math.min(ya, yb), w: xr - xl, h: Math.abs(yb - ya) } });
    });
    left.forEach(function (it) {
      var isH = it.r.label === hl, va = ctx.fmt.v(it.r.a), vw = textW(va, S.mono, true);
      if (Math.abs(it.pos - it.want) > 4) ctx.op('notes', function (p) { p.line(xl - 5, it.want, xl - 12, it.pos - S.hand * 0.25, { width: 0.9, passes: 1, opacity: 0.5, rough: 0.3 }); });
      ctx.text(xl - 14, it.pos + S.hand * 0.3, va, { mono: true, anchor: 'end', color: isH ? C['red-ink'] : C.figure, weight: isH ? 700 : 400 });
      ctx.text(xl - 22 - vw, it.pos + S.hand * 0.3, it.r.label, { size: S.small, anchor: 'end', color: isH ? C['red-ink'] : C.graphite });
    });
    right.forEach(function (it) {
      var isH = it.r.label === hl, vb = ctx.fmt.v(it.r.b), vw = textW(vb, S.mono, true);
      if (Math.abs(it.pos - it.want) > 4) ctx.op('notes', function (p) { p.line(xr + 5, it.want, xr + 12, it.pos - S.hand * 0.25, { width: 0.9, passes: 1, opacity: 0.5, rough: 0.3 }); });
      ctx.text(xr + 14, it.pos + S.hand * 0.3, vb, { mono: true, color: isH ? C['red-ink'] : C.figure, weight: isH ? 700 : 400 });
      if (namesRight) ctx.text(xr + 22 + vw, it.pos + S.hand * 0.3, it.r.label, { size: S.small, color: isH ? C['red-ink'] : C.graphite });
    });
    var mine = rows.filter(function (r) { return r.label === hl; })[0];
    if (mine) ctx.headline = { label: mine.label, value: mine.b, refLabel: cols[0], refValue: mine.a, kind: 'before' };
    ctx.table = {
      head: [xName(ctx), cols[0], cols[1], 'change'],
      rows: rows.map(function (r) { return [r.label, ctx.fmt.exact(r.a), ctx.fmt.exact(r.b), ctx.fmt.diff(r.b - r.a)]; })
    };
  };

  /* ---------- waffle: 10 x 10 hatched squares ---------- */
  TYPES.waffle = function (ctx) {
    var D = ctx.D, S = ctx.S, C = ctx.C, W = ctx.W, sp = ctx.spec;
    ctx.fmt.unitOnValues = true;
    var rows = [];
    D.labels.forEach(function (l, i) { var v = D.series[0].values[i]; if (isNum(v) && v >= 0) rows.push({ label: String(l), value: v, i: i }); else if (isNum(v)) ctx.warn('negative value for "' + l + '" left out'); });
    if (sp.sort) rows = sortRows(ctx, rows, function (r) { return r.value; });
    var tot = sum(rows.map(function (r) { return r.value; }));
    var whole = sp.total != null ? toNum(sp.total) : (ctx.fmt.unit === '%' ? 100 : tot);
    if (tot > whole * 1.005) { ctx.warn('the parts add up to ' + f2(tot) + ', more than the whole (' + whole + '); the whole was raised to match'); whole = tot; }
    if (ctx.fmt.unit === '%' && Math.abs(tot - 100) > 0.5 && sp.total == null) ctx.warn('the percentages add up to ' + f2(tot) + ', not 100; the rest is left empty');
    // largest remainder: whole squares that add up exactly
    var exact = rows.map(function (r) { return r.value / whole * 100; });
    var cnt = exact.map(Math.floor), need = Math.round(tot / whole * 100) - sum(cnt);
    exact.map(function (e, i) { return { i: i, rem: e - Math.floor(e) }; }).sort(function (a, b) { return b.rem - a.rem; })
      .slice(0, Math.max(0, need)).forEach(function (o) { cnt[o.i] += 1; });
    var rounded = exact.some(function (e, i) { return Math.abs(e - cnt[i]) > 1e-9; });
    var hl = hlLabel(ctx, rows.map(function (r) { return r.label; }));
    var side = ctx.narrow ? Math.min(W, 340) : Math.min(W * 0.48, 380, (ctx.H || 400) - S.hand);
    var gapc = Math.max(2.5, side * 0.012), cell = (side - gapc * 9) / 10;
    var gx = ctx.narrow ? (W - side) / 2 : 0, gy = ctx.notesRoom + S.hand * 0.2;
    var colOf = function (k) { return rows[k].label === hl ? C.red : ctx.color(k); };
    var owner = [], k = 0;
    cnt.forEach(function (c, ci) { for (var q = 0; q < c; q++) owner[k++] = ci; });
    ctx.op('marks', function (p) {
      for (var s = 0; s < 100; s++) {
        var r = Math.floor(s / 10), c = s % 10, x = gx + c * (cell + gapc), y = gy + r * (cell + gapc), o = owner[s];
        if (o == null) { p.rect(x, y, cell, cell, { width: 0.9, passes: 1, rough: 0.7, opacity: 0.35 }); continue; }
        p.rect(x, y, cell, cell, { width: Math.max(0.9, ctx.lw * 0.6), passes: 1, rough: 0.7, opacity: 0.85, stroke: rows[o].label === hl ? C['red-frame'] : C.graphite });
        shade(p, ctx, { x: x, y: y, w: cell, h: cell }, colOf(o), { angle: ANGLES[o % ANGLES.length], gap: clamp(cell / 7, 2.6, ctx.gap), alpha: hl != null && rows[o].label !== hl ? 0.55 : 1 });
      }
    });
    ctx.occupy({ x: gx, y: gy, w: side, h: side });
    var start = 0;
    rows.forEach(function (r, i) {
      if (cnt[i] > 0) {
        var s0 = start, x = gx + (s0 % 10) * (cell + gapc), y = gy + Math.floor(s0 / 10) * (cell + gapc);
        ctx.anchor([r.label, r.i], { x: x + cell / 2, y: y, mark: { x: x, y: y, w: cell, h: cell } });
      }
      start += cnt[i];
    });
    // the key: swatch, label, value
    var lx = ctx.narrow ? gx : side + S.hand * 1.6, ly = ctx.narrow ? gy + side + S.hand * 1.6 : gy + S.hand * 1.1;
    var lineH = S.hand * 1.55, sw = S.hand * 0.95;
    rows.forEach(function (r, i) {
      var y = ly + i * lineH, isH = r.label === hl;
      ctx.op('marks', function (p) {
        p.rect(lx, y - sw * 0.78, sw, sw * 0.78, { width: 1, passes: 1, rough: 0.5, stroke: isH ? C['red-frame'] : C.graphite });
        shade(p, ctx, { x: lx, y: y - sw * 0.78, w: sw, h: sw * 0.78 }, colOf(i), { angle: ANGLES[i % ANGLES.length], gap: 2.8 });
      });
      var nb = ctx.text(lx + sw + 9, y, r.label, { color: isH ? C['red-ink'] : C.graphite });
      var vs = ctx.fmt.unit === '%' ? ctx.fmt.u(r.value) : ctx.fmt.u(r.value) + ' · ' + ctx.fmt.pct(r.value / whole);
      ctx.text(nb.x + nb.w + 10, y, vs, { mono: true, color: isH ? C['red-ink'] : C.figure, weight: isH ? 700 : 400 });
      ctx.mark('rect', { x: lx, y: y - sw, w: sw + nb.w + 20, h: sw * 1.2 }, { label: r.label, value: r.value, series: D.series[0].name, shown: vs, squares: cnt[i] });
    });
    var note = '1 square = ' + (ctx.fmt.unit === '%' ? ctx.fmt.u(whole / 100) : ctx.fmt.pct(0.01)) + (rounded ? ', rounded to whole squares' : '');
    var ny = ly + rows.length * lineH + S.hand * 0.2;
    ctx.textMix(lx, ny, note, { size: S.small, color: C['graphite-soft'] });
    ctx.H = Math.ceil(Math.max(gy + side, ny + S.hand * 0.6) + 4);
    ctx.table = { head: [xName(ctx), D.series[0].name, 'squares'], rows: rows.map(function (r, i) { return [r.label, ctx.fmt.exact(r.value), String(cnt[i])]; }) };
  };

  /* ---------- tally: five-bar gates for small counts ---------- */
  TYPES.tally = function (ctx) {
    var D = ctx.D, S = ctx.S, C = ctx.C, W = ctx.W, sp = ctx.spec;
    var rows = [];
    D.labels.forEach(function (l, i) { var v = D.series[0].values[i]; if (isNum(v)) rows.push({ label: String(l), value: Math.round(v), i: i }); });
    if (!rows.length && isNum(toNum(sp.value))) rows.push({ label: sp.label || '', value: Math.round(toNum(sp.value)), i: 0 });
    rows.forEach(function (r) {
      if (r.value < 0) { ctx.warn('a tally cannot count below zero ("' + r.label + '")'); r.value = 0; }
      if (r.value > 120) ctx.warn('a tally is for small counts; ' + r.value + ' marks for "' + r.label + '" belong in a bar chart');
    });
    var hl = hlLabel(ctx, rows.map(function (r) { return r.label; }));
    var labW = Math.min(W * 0.3, max(rows.map(function (r) { return textW(r.label, S.hand); }).concat([0])));
    var cntW = max(rows.map(function (r) { return textW(String(r.value), S.mono, true); }).concat([0]));
    var step = clamp(S.hand * 0.36, 6, 11), gateW = step * 3, gateGap = step * 2.1, mh = S.hand * 1.2;
    var x0 = labW ? labW + S.hand * 0.9 : 0, x1 = W - cntW - S.hand * 0.9;
    var perLine = Math.max(1, Math.floor((x1 - x0 + gateGap) / (gateW + gateGap)));
    var widest = max(rows.map(function (r) { return Math.min(perLine, Math.ceil(r.value / 5)); }).concat([1]));
    var countX = Math.min(W - cntW, x0 + widest * (gateW + gateGap) + S.hand * 0.5);
    var y = ctx.notesRoom + S.hand * 0.3;
    rows.forEach(function (r) {
      var gates = Math.ceil(r.value / 5), lines = Math.max(1, Math.ceil(gates / perLine));
      var rowH = lines * (mh + S.hand * 0.55) + S.hand * 0.45, isH = r.label === hl, col = isH ? C.red : C.graphite;
      var yc = y + S.hand * 0.35 + mh / 2;
      ctx.text(0, yc + S.hand * 0.3, r.label, { color: isH ? C['red-ink'] : C.graphite });
      ctx.text(countX, yc + S.mono * 0.33, String(r.value), { mono: true, color: isH ? C['red-ink'] : C.figure, weight: 700 });
      var v = r.value;
      ctx.op('marks', function (p) {
        for (var k = 0; k < v; k++) {
          var g = Math.floor(k / 5), m = k % 5, ln = Math.floor(g / perLine), gi = g % perLine;
          var gx = x0 + gi * (gateW + gateGap), gy = yc + ln * (mh + S.hand * 0.55);
          var tilt = (p.random() - 0.5) * 2.4;
          if (m < 4) p.line(gx + m * step + tilt * 0.4, gy - mh / 2 + p.random() * 1.5, gx + m * step - tilt * 0.4, gy + mh / 2 - p.random() * 1.5, { stroke: col, width: ctx.lw * 1.05, passes: 1, rough: 1.2 });
          else p.line(gx - step * 0.7, gy + mh * 0.32, gx + gateW + step * 0.7, gy - mh * 0.3, { stroke: col, width: ctx.lw * 1.05, passes: 1, rough: 1.2 });
        }
      });
      var hb = { x: x0 - 4, y: y + S.hand * 0.3, w: Math.min(gates, perLine) * (gateW + gateGap), h: lines * (mh + S.hand * 0.55) };
      ctx.occupy(hb);
      ctx.mark('rect', hb, { label: r.label, value: r.value, series: D.series[0].name, shown: String(r.value) });
      ctx.anchor([r.label, r.i], { x: hb.x + hb.w, y: yc - mh / 2, mark: hb });
      y += rowH;
    });
    ctx.H = Math.ceil(y + S.hand * 0.2);
    ctx.table = { head: [xName(ctx), D.series[0].name], rows: rows.map(function (r) { return [r.label, String(r.value)]; }) };
  };

  /* ---------- gauge: the hatched fuel bar with a red mark ---------- */
  TYPES.gauge = function (ctx) {
    var D = ctx.D, S = ctx.S, C = ctx.C, W = ctx.W, sp = ctx.spec;
    ctx.fmt.unitOnValues = true;
    var rows = [];
    D.labels.forEach(function (l, i) {
      var raw = D.rows && D.rows[i] && D.rows[i].raw;
      var mark = raw && typeof raw === 'object' && !Array.isArray(raw) ? toNum(raw.target != null ? raw.target : raw.mark) : (Array.isArray(raw) ? toNum(raw[2]) : null);
      if (isNum(D.series[0].values[i])) rows.push({ label: String(l), value: D.series[0].values[i], mark: mark, i: i });
    });
    if (!rows.length && isNum(toNum(sp.value))) rows.push({ label: sp.label || '', value: toNum(sp.value), mark: null, i: 0 });
    var mx = toNum(sp.max);
    if (mx == null) {
      if (ctx.fmt.unit === '%') mx = 100;
      else { mx = max(rows.map(function (r) { return r.value; })); ctx.warn('a gauge needs max (the full tank); the largest value was used'); }
    }
    var target = refOf(sp.target, 'target'), bench = refOf(sp.benchmark, 'benchmark');
    var labW = Math.min(W * 0.32, max(rows.map(function (r) { return textW(r.label, S.hand); }).concat([0])));
    var vals = rows.map(function (r) { return ctx.fmt.unit === '%' && mx === 100 ? ctx.fmt.u(r.value) : ctx.fmt.num(r.value) + ' of ' + ctx.fmt.u(mx); });
    var valW = max(vals.map(function (v) { return textW(v, S.mono, true); }));
    var stacked = ctx.narrow && labW + valW > W * 0.55;
    var x0 = stacked ? 0 : (labW ? labW + S.hand * 0.9 : 0), x1 = W - (stacked ? 0 : valW + S.hand * 0.8);
    var bh = clamp(S.hand * 0.95, 15, 26), rowH = bh + S.hand * (stacked ? 2.5 : 1.45);
    var y = ctx.notesRoom + S.hand * (target || bench ? 1.5 : 0.4);
    rows.forEach(function (r, i) {
      var v = r.value;
      if (v < 0 || v > mx) { ctx.warn('"' + r.label + '" (' + v + ') lies outside 0 to ' + mx + '; the bar was clamped and the number printed as given'); }
      var frac = clamp(v / mx, 0, 1), isH = r.label === hlLabel(ctx, rows.map(function (q) { return q.label; }), true);
      var by = stacked ? y + S.hand * 1.2 : y, w = x1 - x0;
      if (stacked) ctx.text(0, y + S.hand * 0.75, r.label, { color: C.graphite });
      else ctx.text(x0 - S.hand * 0.6, by + bh / 2 + S.hand * 0.3, r.label, { anchor: 'end', color: C.graphite });
      ctx.text(stacked ? W : x1 + S.hand * 0.6, stacked ? y + S.hand * 0.75 : by + bh / 2 + S.mono * 0.33, vals[i], { mono: true, anchor: stacked ? 'end' : 'start', color: C.figure, weight: 700 });
      ctx.op('marks', function (p) {
        p.rect(x0, by, w, bh, { width: ctx.lw * 0.9, passes: 2, rough: 0.9 });
        if (frac > 0) p.rect(x0 + 2.5, by + 2.5, Math.max(0, (w - 5) * frac), bh - 5, { fill: isH ? C.red : C.graphite, fillStyle: 'hatch', gap: 2.6, angle: -41, passes: 0, fillOpacity: 0.8 });
      });
      var m = r.mark != null ? { value: r.mark, kind: 'target' } : (target ? { value: target.value, kind: 'target' } : null);
      [m, bench ? { value: bench.value, kind: 'benchmark' } : null].forEach(function (mk) {
        if (!mk) return;
        var xm = x0 + clamp(mk.value / mx, 0, 1) * w;
        ctx.op('over', function (p) { p.line(xm, by - 5, xm, by + bh + 5, { stroke: mk.kind === 'target' ? C.red : C.blue, width: 2.2, passes: 1, rough: 0.4 }); });
        if (i === 0) ctx.textMix(xm, by - 9, (mk.kind === 'target' ? (target && target.label) || 'target' : (bench && bench.label) || 'benchmark') + ' ' + ctx.fmt.u(mk.value), { anchor: 'middle', size: S.small, color: mk.kind === 'target' ? C['red-ink'] : C['graphite-soft'] });
      });
      var hb = { x: x0, y: by, w: w, h: bh };
      ctx.occupy(hb);
      ctx.mark('rect', hb, { label: r.label, value: r.value, max: mx, series: D.series[0].name, shown: vals[i] });
      ctx.anchor([r.label, r.i], { x: x0 + frac * w, y: by - 4, mark: hb });
      y += rowH;
    });
    ctx.H = Math.ceil(y - S.hand * 0.4);
    if (rows.length === 1 && (target || bench)) setHeadline(ctx, rows[0].label, rows[0].value);
    ctx.table = { head: [xName(ctx), D.series[0].name, 'max', 'target'], rows: rows.map(function (r) { var m = r.mark != null ? r.mark : (target ? target.value : null); return [r.label, ctx.fmt.exact(r.value), ctx.fmt.exact(mx), m != null ? ctx.fmt.exact(m) : '']; }) };
  };

  /* ---------- timeline: milestones as postmarks on a hand-drawn line ---------- */
  function parseDate(s) {
    if (s instanceof Date) return s;
    var m = /^(\d{4})(?:-(\d{1,2}))?(?:-(\d{1,2}))?/.exec(String(s));
    if (m) return new Date(Date.UTC(+m[1], m[2] ? +m[2] - 1 : 0, m[3] ? +m[3] : 1));
    var d = new Date(s);
    return isNaN(d) ? null : d;
  }
  TYPES.timeline = function (ctx) {
    var S = ctx.S, C = ctx.C, W = ctx.W, sp = ctx.spec, fmt = ctx.fmt;
    var items = [];
    (Array.isArray(sp.data) ? sp.data : []).forEach(function (d, i) {
      var it = Array.isArray(d) ? { date: d[0], label: d[1], note: d[2] } : Object.assign({}, d);
      it.when = parseDate(it.date);
      if (!it.when) { ctx.warn('milestone ' + (i + 1) + ' has no readable date (use YYYY-MM-DD)'); return; }
      it.i = i; items.push(it);
    });
    items.sort(function (a, b) { return a.when - b.when; });
    if (!items.length) { ctx.H = 60; return; }
    var now = sp.now ? parseDate(sp.now) : null;
    var hl = hlIndex(ctx, items.map(function (it) { return it.label; }), true);
    var t0 = items[0].when.getTime(), t1 = items[items.length - 1].when.getTime();
    if (now) { t0 = Math.min(t0, now.getTime()); t1 = Math.max(t1, now.getTime()); }
    if (t1 === t0) t1 = t0 + 864e5;
    var vertical = W < 640 || sp.vertical === true;
    var rad = clamp(S.hand * (vertical ? 1.9 : 2.15), 28, 56);
    var dateOf = function (it) { return fmt.date(it.when, it.date && /^\d{4}-\d{1,2}-\d{1,2}/.test(String(it.date)) ? { day: 'numeric', month: 'short', year: 'numeric' } : { month: 'short', year: 'numeric' }); };
    var stampDate = function (it) { return fmt.date(it.when, /^\d{4}-\d{1,2}-\d{1,2}/.test(String(it.date)) ? { day: 'numeric', month: 'short' } : { month: 'short', year: 'numeric' }).toUpperCase(); };
    var done = function (it) { return it.done != null ? !!it.done : (now ? it.when <= now : true); };
    var stampCol = function (it, k) { return k === hl ? C['red-ink'] : C.graphite; };
    function drawStamp(it, k, cx, cy) {
      var col = stampCol(it, k), past = done(it);
      var center = it.figure != null ? String(it.figure) : String(k + 1);
      // arc text stays inside the ring band (the engine's 0.24 r); below 9 px it is dropped,
      // the date is printed in full beside the stamp anyway
      var ringOK = rad * 0.24 >= 9;
      var top = ringOK && it.place ? String(it.place).toUpperCase() : '';
      var bottom = ringOK ? stampDate(it) : '';
      ctx.op('marks', function (p) {
        var g = global.Sketchy.postmark(p, cx, cy, rad, top, bottom, { color: col, opacity: past ? 0.85 : 0.42 });
        if (!past) Array.prototype.forEach.call(g.querySelectorAll('.sk-path'), function (pth) { pth.setAttribute('stroke-dasharray', '5 4'); pth.removeAttribute('pathLength'); });
      });
      // the center figure fits well inside the inner ring (radius 0.66 r) or is left out
      var cs = Math.min(rad * 0.46, rad * 0.92 / (Math.max(1, center.length) * 0.6));
      if (cs >= 9) ctx.text(cx, cy + cs * 0.34, center, { mono: true, anchor: 'middle', size: cs, color: past || k === hl ? col : C['graphite-soft'], weight: 700, free: true });
      ctx.occupy({ x: cx - rad, y: cy - rad, w: rad * 2, h: rad * 2 });
      ctx.mark('circle', { cx: cx, cy: cy, r: rad }, { label: it.label || '', value: it.when.toISOString().slice(0, 10), series: 'date', shown: dateOf(it) });
      ctx.anchor([it.label || '', it.i], { x: cx + rad * 0.7, y: cy - rad * 0.8, mark: { x: cx - rad, y: cy - rad, w: rad * 2, h: rad * 2 } });
    }
    var labelOf = function (it, k, x, y, anchor, maxW) {
      var col = k === hl ? C['red-ink'] : C.graphite, lines = wrap(it.label || '', S.hand, maxW).slice(0, 3), yy = y;
      lines.forEach(function (l) { ctx.text(x, yy, l, { anchor: anchor, color: col }); yy += S.hand * 0.98; });
      ctx.text(x, yy, dateOf(it), { anchor: anchor, mono: true, size: S.tick, color: C['graphite-soft'], weight: 400 });
      yy += S.tick * 1.25;
      if (it.note) wrap(it.note, S.small, maxW).slice(0, 2).forEach(function (l) { ctx.text(x, yy, l, { anchor: anchor, size: S.small, color: C['graphite-soft'] }); yy += S.small * 1.0; });
      return yy;
    };
    var nowT = now ? now.getTime() : null;
    if (!vertical) {
      var pad = rad + 8, X = function (t) { return pad + (t - t0) / (t1 - t0) * (W - pad * 2); };
      var labW = Math.max(rad * 2.6, Math.min(200, (W - pad * 2) / Math.max(2, Math.ceil(items.length / 2)) - 14));
      var blockH = function (it) { return wrap(it.label || '', S.hand, labW).slice(0, 3).length * S.hand * 0.98 + S.tick * 1.25 + (it.note ? Math.min(2, wrap(it.note, S.small, labW).length) * S.small : 0); };
      var hUp = 0, hDn = 0;
      items.forEach(function (it, k) { if (k % 2 === 0) hUp = Math.max(hUp, blockH(it)); else hDn = Math.max(hDn, blockH(it)); });
      var stem = S.hand * 0.9, top = ctx.notesRoom + S.hand * 0.4;
      var ly = top + hUp + S.hand * 0.6 + rad * 2 + stem;
      ctx.H = Math.ceil(ly + stem + rad * 2 + S.hand * 0.9 + hDn + S.hand * 0.3);
      var up = [], dn = [];
      items.forEach(function (it, k) { var o = { it: it, k: k, want: X(it.when.getTime()), size: Math.max(rad * 2, labW) + 10 }; o.pos = o.want; (k % 2 ? dn : up).push(o); });
      spread(up, 0, 4, W - 4); spread(dn, 0, 4, W - 4);
      var xNow = nowT != null ? X(nowT) : null;
      ctx.op('axes', function (p) {
        if (xNow == null) p.line(6, ly, W - 6, ly, { width: ctx.lw * 1.1 });
        else {
          if (xNow > 8) p.line(6, ly, xNow, ly, { width: ctx.lw * 1.1 });
          if (xNow < W - 8) p.line(xNow, ly, W - 6, ly, { width: ctx.lw, dash: '7 6', opacity: 0.7 });
        }
      });
      up.concat(dn).forEach(function (o) {
        var isUp = up.indexOf(o) >= 0, cy = isUp ? ly - stem - rad : ly + stem + rad;
        ctx.op('marks', function (p) {
          p.line(o.want, ly, o.pos, isUp ? cy + rad : cy - rad, { width: 1, passes: 1, rough: 0.5, opacity: 0.7 });
          p.dot(o.want, ly, S.hand * 0.32, { fill: C.graphite });
        });
        drawStamp(o.it, o.k, o.pos, cy);
        var anchor = 'middle', lx = o.pos;
        if (lx - labW / 2 < 0) { anchor = 'start'; lx = Math.max(0, o.pos - rad); }
        if (lx + labW / 2 > W && anchor === 'middle') { anchor = 'end'; lx = Math.min(W, o.pos + rad); }
        if (isUp) labelOf(o.it, o.k, lx, cy - rad - S.hand * 0.5 - blockH(o.it) + S.hand * 0.75, anchor, labW);
        else labelOf(o.it, o.k, lx, cy + rad + S.hand * 1.05, anchor, labW);
      });
      if (xNow != null) {
        ctx.op('over', function (p) { p.line(xNow, ly - S.hand * 0.6, xNow, ly + S.hand * 0.6, { stroke: C.red, width: 2.4, passes: 1, rough: 0.4 }); });
        var nl = sp.nowLabel || 'today', nw = textW(nl, S.small);
        var nb = bestBox(ctx, nw, S.small, [{ x: xNow - nw / 2, y: ly + S.hand * 0.75 }, { x: xNow - nw / 2, y: ly - S.hand * 0.75 - S.small }, { x: xNow + 6, y: ly + S.hand * 0.75 }, { x: xNow - nw - 6, y: ly + S.hand * 0.75 }, { x: xNow + 6, y: ly - S.hand * 0.75 - S.small }, { x: xNow - nw - 6, y: ly - S.hand * 0.75 - S.small }]);
        ctx.text(nb.x, nb.y + S.small * 0.8, nl, { size: S.small, color: C['red-ink'] });
      }
    } else {
      var lx2 = 10, top2 = ctx.notesRoom + S.hand * 0.6;
      var cx = lx2 + S.hand * 0.9 + rad, tx = cx + rad + S.hand * 0.7, maxW = Math.max(120, W - tx - 4);
      var blocks = items.map(function (it) { return Math.max(rad * 2, wrap(it.label || '', S.hand, maxW).slice(0, 3).length * S.hand * 0.98 + S.tick * 1.25 + (it.note ? Math.min(2, wrap(it.note, S.small, maxW).length) * S.small : 0)); });
      var span = Math.max(sum(blocks) + items.length * S.hand * 0.8, items.length * (rad * 2 + S.hand));
      var Y = function (t) { return top2 + rad + (t - t0) / (t1 - t0) * span; };
      var os = items.map(function (it, k) { var w = Y(it.when.getTime()); return { it: it, k: k, want: w, pos: w, size: blocks[k] + S.hand * 0.6 }; });
      spread(os, 0, top2, null);
      var yEnd = Math.max(Y(t1), os[os.length - 1].pos + blocks[os.length - 1] / 2) + rad * 0.6;
      ctx.H = Math.ceil(yEnd + S.hand * 1.2);
      var yNow = nowT != null ? Y(nowT) : null;
      ctx.op('axes', function (p) {
        if (yNow == null) p.line(lx2, top2, lx2, yEnd, { width: ctx.lw * 1.1 });
        else { p.line(lx2, top2, lx2, yNow, { width: ctx.lw * 1.1 }); p.line(lx2, yNow, lx2, yEnd, { width: ctx.lw, dash: '7 6', opacity: 0.7 }); }
      });
      os.forEach(function (o) {
        var cy = o.pos;
        ctx.op('marks', function (p) { p.line(lx2, o.want, cx - rad, cy, { width: 1, passes: 1, rough: 0.5, opacity: 0.7 }); p.dot(lx2, o.want, S.hand * 0.32, { fill: C.graphite }); });
        drawStamp(o.it, o.k, cx, cy);
        var bh = blocks[o.k];
        labelOf(o.it, o.k, tx, cy - Math.min(bh, rad * 2) / 2 + S.hand * 0.75, 'start', maxW);
      });
      if (yNow != null) {
        ctx.op('over', function (p) { p.line(lx2 - S.hand * 0.5, yNow, lx2 + S.hand * 0.5, yNow, { stroke: C.red, width: 2.4, passes: 1, rough: 0.4 }); });
        var nl2 = sp.nowLabel || 'today', nw2 = textW(nl2, S.small);
        var nb2 = bestBox(ctx, nw2, S.small, [{ x: lx2 + S.hand * 0.7, y: yNow - S.small * 0.5 }, { x: tx, y: yNow - S.small * 0.5 }, { x: lx2 + S.hand * 0.7, y: yNow - S.small * 1.4 }, { x: lx2 + S.hand * 0.7, y: yNow + 2 }, { x: W - nw2, y: yNow - S.small * 0.5 }]);
        ctx.text(nb2.x, nb2.y + S.small * 0.8, nl2, { size: S.small, color: C['red-ink'] });
      }
    }
    ctx.table = { head: ['date', 'milestone', 'note'], rows: items.map(function (it) { return [it.when.toISOString().slice(0, 10), it.label || '', it.note || '']; }) };
  };

  /* ---------- funnel: honest widths, the leakiest step in red ---------- */
  TYPES.funnel = function (ctx) {
    var D = ctx.D, S = ctx.S, C = ctx.C, W = ctx.W;
    ctx.fmt.unitOnValues = true;
    var rows = [];
    D.labels.forEach(function (l, i) { var v = D.series[0].values[i]; if (isNum(v) && v >= 0) rows.push({ label: String(l), value: v, i: i }); });
    rows.forEach(function (r, i) { if (i && r.value > rows[i - 1].value) ctx.warn('"' + r.label + '" is larger than the stage before it; a funnel only narrows'); });
    var top = rows.length ? rows[0].value : 1;
    var labW = Math.min(W * (ctx.narrow ? 0.34 : 0.26), max(rows.map(function (r) { return textW(r.label, S.hand); }).concat([0])));
    var lines = rows.map(function (r) { return wrap(r.label, S.hand, labW).slice(0, 2); });
    var shown = rows.map(function (r) { return ctx.fmt.v(r.value); });
    var valW = max(shown.map(function (s) { return textW(s, S.mono, true); }));
    var x0 = labW + S.hand * 0.9, x1 = W - valW - S.hand * 0.9, cxF = (x0 + x1) / 2, fullW = x1 - x0;
    var bh = clamp(S.hand * 1.55, 24, 46), gapH = S.mono * 2.2, y = ctx.notesRoom + S.hand * 0.3;
    var conv = rows.map(function (r, i) { return i ? (rows[i - 1].value > 0 ? r.value / rows[i - 1].value : 0) : null; });
    var worst = -1;
    conv.forEach(function (c, i) { if (c != null && (worst < 0 || c < conv[worst])) worst = i; });
    var hl = hlLabel(ctx, rows.map(function (r) { return r.label; }), true);
    if (hl != null) worst = rows.map(function (r) { return r.label; }).indexOf(hl);
    var prev = null;
    rows.forEach(function (r, i) {
      var w = Math.max(2, fullW * (r.value / top)), x = cxF - w / 2, isH = i === worst && hl != null, y0 = y;
      lines[i].forEach(function (s, k) { ctx.text(x0 - S.hand * 0.6, y0 + bh / 2 + S.hand * 0.3 + (k - (lines[i].length - 1) / 2) * S.hand * 0.95, s, { anchor: 'end', color: isH ? C['red-ink'] : C.graphite }); });
      var p0 = prev;
      ctx.op('marks', function (p) {
        if (p0) { gapLine(p, ctx, p0.x, p0.y, x, y0, { width: 0.9, passes: 1, opacity: 0.35, rough: 0.5 }); gapLine(p, ctx, p0.x + p0.w, p0.y, x + w, y0, { width: 0.9, passes: 1, opacity: 0.35, rough: 0.5 }); }
        p.rect(x, y0, w, bh, { stroke: isH ? C['red-frame'] : C.graphite, width: ctx.lw, rough: 1.1 });
        shade(p, ctx, { x: x, y: y0, w: w, h: bh }, isH ? C.red : ctx.color(0), { angle: ANGLES[0] });
      });
      var vw = textW(shown[i], S.mono, true);
      if (vw + 12 <= w) ctx.text(cxF, y + bh / 2 + S.mono * 0.33, shown[i], { mono: true, anchor: 'middle', color: C.figure, weight: 700, free: true });
      else ctx.text(x + w + 8, y + bh / 2 + S.mono * 0.33, shown[i], { mono: true, color: C.figure, weight: 700 });
      if (i > 0) {
        var c = conv[i], ct = ctx.fmt.pct(c), isW = i === worst;
        var cy = y - gapH / 2 + S.mono * 0.33, cw = textW(ct, S.mono * 0.92, true);
        ctx.op('notes', function (p) { p.arrow(cxF - cw / 2 - 16, cy - S.mono * 0.85, cxF - cw / 2 - 16, cy + S.mono * 0.2, { width: 1.2, passes: 1, bend: 0.1, head: 5, stroke: isW ? C.red : C.graphite }); });
        ctx.text(cxF - cw / 2 - 4, cy, ct, { mono: true, size: S.mono * 0.92, color: isW ? C['red-ink'] : C['graphite-soft'], weight: isW ? 700 : 400 });
        if (isW && hl == null) ctx.text(cxF + cw / 2 + 8, cy, 'the biggest drop', { size: S.small, color: C['red-ink'] });
        if (isW && hl == null) ctx.anchor(['drop', 'worst'], { x: cxF, y: cy - S.mono, mark: null });
      }
      var hb = { x: x, y: y, w: w, h: bh };
      ctx.occupy(hb);
      ctx.mark('rect', hb, { label: r.label, value: r.value, series: D.series[0].name, shown: shown[i], conversion: conv[i] != null ? f2(conv[i] * 100) : '' });
      ctx.anchor([r.label, r.i], { x: x + w, y: y, mark: hb });
      prev = { x: x, y: y + bh, w: w };
      y += bh + gapH;
    });
    ctx.H = Math.ceil(y - gapH + S.hand * 0.4);
    if (rows.length > 1) ctx.distortion = rows[rows.length - 1].label + ' is ' + ctx.fmt.pct(rows[rows.length - 1].value / top) + ' of ' + rows[0].label;
    ctx.table = { head: [xName(ctx), D.series[0].name, 'from the stage before'], rows: rows.map(function (r, i) { return [r.label, ctx.fmt.exact(r.value), conv[i] != null ? ctx.fmt.pct(conv[i]) : '']; }) };
  };

  /* ---------- bignumber: one figure, a hand-drawn arrow, the delta ---------- */
  TYPES.bignumber = function (ctx) {
    var S = ctx.S, C = ctx.C, W = ctx.W, sp = ctx.spec;
    ctx.fmt.unitOnValues = true;
    var v = toNum(sp.value);
    if (v == null && Array.isArray(sp.data) && sp.data.length) { var rr = toRows(sp.data); v = rr[rr.length - 1].values[0]; }
    if (v == null) { ctx.warn('bignumber needs value'); v = 0; }
    var cmp = refOf(sp.compare, '') || refOf(sp.benchmark, 'benchmark') || refOf(sp.target, 'target');
    if (cmp) cmp.kind = refOf(sp.compare, '') ? 'compare' : (refOf(sp.benchmark) ? 'benchmark' : 'target');
    var big = ctx.fmt.u(v), dec = sp.format && sp.format.decimals != null ? sp.format.decimals : null;
    var size = clamp(W * 0.16, 54, 138);
    var maxW = ctx.narrow ? W * 0.96 : W * 0.6;
    if (textW(big, size, true) > maxW) size = maxW / (big.length * 0.6);
    var top = ctx.notesRoom + size * 0.06, base = top + size * 0.8;
    ctx.text(0, base, big, { mono: true, size: size, color: C.figure, weight: 700, count: { to: v, fmt: function (x) { return ctx.fmt.u(x, dec != null ? dec : decimalsShown(big)); } } });
    var fw = textW(big, size, true);
    var y = base + size * 0.12;
    if (sp.label) { y += size * 0.1 + S.hand * 1.05; ctx.text(0, y, sp.label, { color: C['graphite-soft'] }); }
    var bx = ctx.narrow ? 0 : fw + S.hand * 1.6, by = ctx.narrow ? y + S.hand * 1.3 : top + size * 0.12;
    ctx.anchor(['value', big, 0], { x: fw * 0.85, y: top + size * 0.05, mark: { x: 0, y: top, w: fw, h: size * 0.85 } });
    ctx.mark('rect', { x: 0, y: top, w: fw, h: size * 0.85 }, { label: sp.label || sp.title || 'value', value: v, series: 'value', shown: big });
    var endY = Math.max(y, base);
    if (cmp) {
      var d = v - cmp.value, good = sp.good || sp.better;
      var up = d > 0, flat = Math.abs(d) < 1e-12;
      var isGood = good ? ((good === 'up' || good === 'higher') ? up : !up && !flat) : null;
      var col = flat || isGood == null ? C.graphite : (isGood ? C['stamp-green'] : C['red-frame']), tcol = flat || isGood == null ? C.figure : (isGood ? C['stamp-green'] : C['red-ink']);
      var al = clamp(size * 0.62, 38, 84), ax = bx + al * 0.32, aw = Math.max(1.8, ctx.lw * 1.35);
      ctx.op('notes', function (p) {
        if (flat) p.arrow(ax - al * 0.3, by + al * 0.5, ax + al * 0.5, by + al * 0.5, { stroke: col, width: aw, passes: 2, bend: 0.1, head: al * 0.24 });
        else if (up) p.arrow(ax - al * 0.22, by + al, ax + al * 0.22, by + al * 0.06, { stroke: col, width: aw, passes: 2, bend: -0.3, head: al * 0.24 });
        else p.arrow(ax - al * 0.22, by + al * 0.06, ax + al * 0.22, by + al, { stroke: col, width: aw, passes: 2, bend: 0.3, head: al * 0.24 });
      });
      var tx = bx + al * 0.95, dsz = clamp(size * 0.34, S.mono * 1.15, S.mono * 2.2);
      var dt = ctx.fmt.diff(d);
      ctx.text(tx, by + al * 0.48, dt, { mono: true, size: dsz, color: tcol, weight: 700 });
      var rel = cmp.value !== 0 && ctx.fmt.unit !== '%' ? ' (' + (d >= 0 ? '+' : '−') + ctx.fmt.pct(Math.abs(d / cmp.value)) + ')' : '';
      var cl = cmp.kind === 'compare' ? (cmp.label ? cmp.label + ' was ' : 'was ') + ctx.fmt.u(cmp.value) + rel : (cmp.label || cmp.kind) + ' ' + ctx.fmt.u(cmp.value) + rel;
      ctx.text(tx, by + al * 0.48 + S.hand * 1.15, cl, { size: S.small, color: C['graphite-soft'] });
      endY = Math.max(endY, by + al + S.hand * 0.6);
      ctx.compare = { value: cmp.value, label: cmp.label, delta: d };
    }
    ctx.H = Math.ceil(endY + S.hand * 0.5);
    ctx.table = { head: ['measure', 'value'].concat(cmp ? [cmp.label || 'compared with', 'difference'] : []), rows: [[sp.label || sp.title || 'value', ctx.fmt.exact(v)].concat(cmp ? [ctx.fmt.exact(cmp.value), ctx.fmt.diff(v - cmp.value)] : [])] };
  };
  function decimalsShown(s) { var m = /[.,](\d+)/.exec(String(s).replace(/\s/g, '')); return m ? m[1].length : 0; }

  /* ---------- ledger: a receipt with dotted leaders, a ruled total and stamps ---------- */
  TYPES.ledger = function (ctx) {
    var S = ctx.S, C = ctx.C, W = ctx.W, sp = ctx.spec;
    ctx.figure.classList.add('is-slip');
    var f = sp.format && typeof sp.format === 'object' ? sp.format : {};
    var money = !!f.currency || CURRENCY_UNIT.test(String(sp.unit || ''));
    var items = [];
    (Array.isArray(sp.data) ? sp.data : toRows(sp.data).map(function (r) { return [r.label, r.values[0]]; })).forEach(function (d, i) {
      var it = Array.isArray(d) ? { label: d[0], value: toNum(d[1]), note: d[2] } : Object.assign({}, d, { value: toNum(d.value) });
      if (it.qty != null && it.price != null) {
        var q = toNum(it.qty), pr = toNum(it.price), calc = Math.round(q * pr * 100) / 100;
        if (it.value != null && Math.abs(it.value - calc) > 0.005) ctx.warn('"' + it.label + '": ' + q + ' × ' + pr + ' is ' + calc + ', not ' + it.value + '; the product was used');
        it.value = calc; it.qty = q; it.price = pr;
      }
      if (!isNum(it.value)) { ctx.warn('row ' + (i + 1) + ' has no amount'); return; }
      items.push(it);
    });
    var fm = makeFormat({ format: Object.assign({ decimals: money ? 2 : undefined }, f), unit: sp.unit }, items.map(function (it) { return it.value; }));
    ctx.fmt = fm;
    var subtotal = Math.round(sum(items.map(function (it) { return it.value; })) * 100) / 100;
    var tax = sp.tax != null ? (typeof sp.tax === 'object' ? sp.tax : { rate: toNum(sp.tax) }) : null;
    var taxAmt = tax && isNum(toNum(tax.rate)) ? Math.round(subtotal * toNum(tax.rate) * 100) / 100 : 0;
    var total = Math.round((subtotal + taxAmt) * 100) / 100;
    if (sp.total != null && Math.abs(toNum(sp.total) - total) > 0.005) ctx.warn('the given total ' + sp.total + ' does not match the rows (' + total + '); the computed total is printed');
    var slipW = Math.min(W, 560), sx = (W - slipW) / 2, pad = clamp(S.hand * 1.15, 16, 30), tooth = clamp(S.hand * 0.5, 7, 12);
    var lx = sx + pad, rx = sx + slipW - pad, y = tooth + pad * 0.8, row = 0;
    var rowH = S.hand * 1.5, hl = hlLabel(ctx, items.map(function (it) { return it.label; }), true);
    function r(attrs) { return { 'data-row': attrs }; }
    if (sp.title) { wrap(sp.title, S.hand * 1.35, slipW - pad * 2, false, 700).forEach(function (l) { y += S.hand * 1.3; ctx.text(W / 2, y, l, { anchor: 'middle', size: S.hand * 1.35, color: C.ink, weight: 700, attrs: r(row) }); }); row++; }
    if (sp.subtitle) { y += S.hand * 1.1; ctx.text(W / 2, y, sp.subtitle, { anchor: 'middle', size: S.small, color: C['graphite-soft'], attrs: r(row++) }); }
    if (sp.meta) { y += S.hand * 1.05; ctx.text(W / 2, y, sp.meta, { anchor: 'middle', mono: true, size: S.tick, color: C['graphite-soft'], weight: 400, attrs: r(row++) }); }
    y += S.hand * 0.75;
    var ry0 = y;
    ctx.op('marks', function (p) { p.line(lx, ry0, rx, ry0, { width: 1, passes: 1, opacity: 0.55, rough: 0.5 }); }, r(row));
    y += S.hand * 0.4;
    function leaderRow(label, valueStr, o) {
      o = o || {};
      var rowIdx = row++, size = o.size || S.hand, vsize = o.vsize || S.mono, vw = textW(valueStr, vsize, true);
      var maxL = rx - lx - vw - S.hand * 1.6, ls = wrap(label, size, maxL, false, o.weight);
      ls.forEach(function (l, k) {
        y += k ? size * 1.02 : rowH;
        ctx.text(lx, y, l, { size: size, color: o.color || C.graphite, weight: o.weight, opacity: o.opacity, attrs: r(rowIdx) });
      });
      var lw = textW(ls[ls.length - 1], size, false, o.weight), ly = y - S.mono * 0.12;
      var a = lx + lw + 7, b = rx - vw - 7;
      if (b - a > 8) ctx.op('marks', function (p) { p.line(a, ly, b, ly, { width: 1.5, passes: 1, rough: 0.25, dash: '0.1 5.5', opacity: (o.opacity || 1) * 0.7 }); }, r(rowIdx));
      ctx.text(rx, y, valueStr, { mono: true, anchor: 'end', size: vsize, color: o.vcolor || C.figure, weight: o.vweight || 400, opacity: o.opacity, attrs: r(rowIdx), count: o.count });
      if (o.sub) { y += S.tick * 1.25; ctx.text(lx + S.hand * 0.4, y, o.sub, { mono: true, size: S.tick, color: C['graphite-soft'], weight: 400, attrs: r(rowIdx) }); }
      if (o.mark) ctx.mark('rect', { x: lx, y: y - rowH * 0.8, w: rx - lx, h: rowH }, o.mark);
      return rowIdx;
    }
    items.forEach(function (it) {
      var isH = String(it.label) === hl;
      var sub = it.qty != null ? fm.num(it.qty, Math.round(it.qty) === it.qty ? 0 : 2) + ' × ' + fm.u(it.price) : (it.note || null);
      leaderRow(String(it.label), fm.u(it.value), { sub: sub, color: isH ? C['red-ink'] : null, vcolor: isH ? C['red-ink'] : null, mark: { label: it.label, value: it.value, series: 'amount', shown: fm.u(it.value) } });
      ctx.anchor([it.label], { x: rx - textW(fm.u(it.value), S.mono, true) - 6, y: y - S.mono, mark: { x: lx, y: y - rowH * 0.7, w: rx - lx, h: rowH } });
    });
    y += S.hand * 0.7;
    var ry1 = y;
    ctx.op('marks', function (p) { p.line(lx, ry1, rx, ry1, { width: ctx.lw * 0.9, passes: 2, rough: 0.5 }); }, r(row));
    if (tax) {
      leaderRow(sp.subtotalLabel || 'subtotal', fm.u(subtotal), { size: S.small });
      leaderRow((tax.label || 'tax') + ' ' + fm.pct(toNum(tax.rate), toNum(tax.rate) * 100 % 1 ? 1 : 0), fm.u(taxAmt), { size: S.small });
    }
    y += S.hand * 0.25;
    var totLabel = String(sp.totalLabel || 'In all').toUpperCase();
    var tdec = money ? 2 : decimalsShown(fm.u(total));
    var totalRow = leaderRow(totLabel, fm.u(total), { weight: 700, size: S.hand * 1.12, vsize: S.mono * 1.3, vweight: 700, color: C.ink, mark: { label: totLabel, value: total, series: 'total', shown: fm.u(total) }, count: { to: total, fmt: function (x) { return fm.u(x, tdec); } } });
    var totalY = y;
    ctx.anchor(['total', totLabel.toLowerCase(), 'in all'], { x: rx - textW(fm.u(total), S.mono * 1.3, true) - 6, y: y - S.mono * 1.2, mark: { x: lx, y: y - rowH, w: rx - lx, h: rowH } });
    y += S.hand * 0.45;
    var ry2 = y;
    ctx.op('marks', function (p) { p.line(lx, ry2, rx, ry2, { width: ctx.lw * 0.9, passes: 1, rough: 0.4 }); p.line(lx, ry2 + 3.5, rx, ry2 + 3.5, { width: ctx.lw * 0.9, passes: 1, rough: 0.4 }); }, r(totalRow));
    // stamps get a band of their own under the total, so no figure is ever inked over
    var stamps = [].concat(sp.stamps || (sp.stamp ? [sp.stamp] : [])), stampSize = clamp(S.hand * 1.95, 26, 56);
    if (stamps.length) {
      var bandY = y + stampSize * 1.2;
      stamps.forEach(function (st, k) {
        if (typeof st === 'string') st = { text: st };
        var cxs = stamps.length === 1 ? 0.5 : 0.3 + k * (0.4 / (stamps.length - 1));
        ctx.stamps.push({ text: st.text, earned: st.earned !== false, color: st.color, x: sx + slipW * cxs, y: bandY + (k % 2 ? stampSize * 0.15 : 0), size: stampSize });
      });
      y += stampSize * 2.2;
    }
    var bench = refOf(sp.benchmark, 'budget');
    if (bench) {
      y += S.hand * 0.1;
      // the reference row stays quieter through the soft pencil, not through opacity:
      // at 0.62 its figures fall under 4.5:1 contrast on the slip
      leaderRow(bench.label, fm.u(bench.value), { size: S.small, color: C['graphite-soft'], vcolor: C['graphite-soft'], vweight: 400 });
      var dd = total - bench.value;
      leaderRow('difference', fm.signed(dd), { size: S.small, vcolor: dd > 0 ? C['red-ink'] : C['stamp-green'], vweight: 700 });
      ctx.headline = { label: totLabel.toLowerCase(), value: total, refLabel: bench.label, refValue: bench.value, kind: 'benchmark' };
    }
    if (sp.note) { y += S.hand * 1.4; wrap(sp.note, S.small, slipW - pad * 2).forEach(function (l, k) { ctx.text(W / 2, y + k * S.small * 1.05, l, { anchor: 'middle', size: S.small, color: C['graphite-soft'], attrs: r(row) }); }); y += S.small * 1.05 * (wrap(sp.note, S.small, slipW - pad * 2).length - 1); row++; }
    y += pad * 0.9 + tooth;
    ctx.H = Math.ceil(y + 4);
    var H = ctx.H;
    // the slip: paper with pinked top and bottom edges
    var edge = function (yy, dir) { var pts = [], n = Math.max(6, Math.round(slipW / (tooth * 1.6))); for (var k = 0; k <= n; k++) pts.push([sx + slipW * k / n, yy + (k % 2 ? dir * tooth * 0.55 : 0)]); return pts; };
    var topE = edge(tooth * 0.6, -1), botE = edge(H - tooth * 0.6 - 2, 1);
    var outline = topE.concat(botE.slice().reverse());
    ctx.op('back', function (p) {
      svgEl('path', { d: 'M' + outline.map(function (q) { return f2(q[0]) + ' ' + f2(q[1]); }).join('L') + 'Z', fill: C['paper-light'], 'fill-opacity': 0.95, 'class': 'sk-ch-slip' }, p.root());
      p.polyline(topE, { width: 1, passes: 1, rough: 0.3, opacity: 0.55 });
      p.polyline(botE, { width: 1, passes: 1, rough: 0.3, opacity: 0.55 });
      p.line(sx, tooth * 0.6, sx, H - tooth * 0.6 - 2, { width: 1, passes: 1, rough: 0.5, opacity: 0.5 });
      p.line(sx + slipW, tooth * 0.6, sx + slipW, H - tooth * 0.6 - 2, { width: 1, passes: 1, rough: 0.5, opacity: 0.5 });
    });
    ctx.stamps.forEach(function (st) { st.x /= W; st.y /= H; });
    var rowsOut = items.map(function (it) { return [String(it.label), fm.exact(it.value)]; });
    if (tax) { rowsOut.push([sp.subtotalLabel || 'subtotal', fm.exact(subtotal)]); rowsOut.push([(tax.label || 'tax'), fm.exact(taxAmt)]); }
    rowsOut.push([totLabel, fm.exact(total)]);
    if (bench) { rowsOut.push([bench.label, fm.exact(bench.value)]); rowsOut.push(['difference', fm.signed(total - bench.value)]); }
    ctx.table = { head: ['item', 'amount'], rows: rowsOut };
  };

  /* ================================================================== *
   * Annotations: a red pen note with a curved arrow, placed where it
   * covers the least.
   * ================================================================== */
  function findAnchor(ctx, at) {
    if (at == null) return null;
    var keys = [];
    if (typeof at === 'object' && !Array.isArray(at)) keys.push(String(at.series) + ':' + String(at.at));
    else keys.push(String(at));
    for (var k = 0; k < keys.length; k++) {
      var key = keys[k].toLowerCase();
      for (var i = 0; i < ctx.anchors.length; i++) if (ctx.anchors[i].keys.indexOf(key) >= 0) return ctx.anchors[i].pt;
    }
    return null;
  }
  function placeNotes(ctx) {
    var list = ctx.spec.annotate;
    if (!list) return;
    list = [].concat(list);
    var S = ctx.S, C = ctx.C;
    list.forEach(function (a) {
      if (!a || a.text == null) return;
      var anc = findAnchor(ctx, a.at);
      if (!anc) { ctx.warn('annotation target "' + (a.at && typeof a.at === 'object' ? JSON.stringify(a.at) : a.at) + '" matches nothing'); return; }
      var line = C.red, ink = C['red-ink'];
      if (a.color && a.color !== 'red') { line = C[a.color] || a.color; ink = a.color === 'graphite' ? C.graphite : (C[a.color] || a.color); }
      var size = S.hand * 0.98, lines = wrap(a.text, size, Math.min(ctx.W * 0.42, 260));
      var tw = max(lines.map(function (l) { return textW(l, size); })), th = lines.length * size * 1.05;
      var cands = [];
      [1.4, 2.3, 3.3].forEach(function (k) {
        var dd = S.hand * k;
        [[1, -1], [-1, -1], [1, 0], [-1, 0], [0, -1], [1, 1], [-1, 1], [0, 1]].forEach(function (dir) {
          var cx = anc.x + dir[0] * dd * 1.3, cy = anc.y + dir[1] * dd;
          cands.push({ x: dir[0] > 0 ? cx : dir[0] < 0 ? cx - tw : cx - tw / 2, y: dir[1] < 0 ? cy - th : dir[1] > 0 ? cy : cy - th / 2 });
        });
      });
      // also score the arrow: a straight run from the note to the target that crosses labels costs
      var arrowCost = function (b) {
        var sx = clamp(anc.x, b.x, b.x + tw), sy = clamp(anc.y, b.y, b.y + th), cost = 0;
        for (var k = 1; k < 8; k++) {
          var px = sx + (anc.x - sx) * k / 8, py = sy + (anc.y - sy) * k / 8;
          ctx.occupied.forEach(function (o) { if (o !== anc.mark && px > o.x && px < o.x + o.w && py > o.y && py < o.y + o.h) cost += 60; });
        }
        return cost;
      };
      var box = bestBox(ctx, tw, th, cands, anc.mark, arrowCost);
      var right = box.x + tw / 2 < anc.x;
      lines.forEach(function (l, k) {
        ctx.text(right ? box.x + tw : box.x, box.y + size * 0.82 + k * size * 1.05, l, { size: size, color: ink, anchor: right ? 'end' : 'start' });
      });
      var sx = clamp(anc.x, box.x, box.x + tw), sy = clamp(anc.y, box.y, box.y + th);
      if (sx > box.x && sx < box.x + tw && sy > box.y && sy < box.y + th) return;
      var dx = anc.x - sx, dy = anc.y - sy, dist = Math.hypot(dx, dy);
      if (dist < S.hand * 0.8) return;
      sx += dx / dist * 5; sy += dy / dist * 5;
      var ex = anc.x - dx / dist * 4, ey = anc.y - dy / dist * 4;
      var bend = (dx * dy >= 0 ? -1 : 1) * 0.3;
      ctx.op('notes', function (p) { p.arrow(sx, sy, ex, ey, { stroke: line, width: Math.max(1.3, ctx.lw * 0.9), passes: 1, bend: bend, head: clamp(dist * 0.18, 6, 11) }); });
    });
  }

  /* ================================================================== *
   * Render
   * ================================================================== */
  function normalizeSpec(sp) {
    var o = Object.assign({}, sp);
    var t = String(o.type || 'bar').toLowerCase().trim();
    o.type = ALIASES[t] || t;
    return o;
  }
  function honesty(ctx) {
    var sp = ctx.spec;
    if (sp['3d'] || sp.depth || sp.perspective || sp.threeD) ctx.warn('no 3D: depth distorts every length; drawn flat');
    var dual = sp.y2 || sp.dualAxis || sp.secondaryAxis || (Array.isArray(sp.series) && sp.series.some(function (s) { return s && (s.axis === 'right' || s.axis === 'y2' || s.yAxis === 1); }));
    if (dual) ctx.warn('one axis only: a second axis invents correlations; everything was drawn on one axis (use two charts, or index both series to 100)');
    var needsUnit = /^(bar|hbar|stacked|grouped|line|area|gauge|bignumber|ledger|funnel|slope)$/.test(sp.type);
    var f = sp.format && typeof sp.format === 'object' ? sp.format : {};
    if (needsUnit && sp.unit == null && !(sp.y && sp.y.unit != null) && !f.currency && !f.prefix && !f.suffix) ctx.warn('no unit given; pass "unit": "" if the values are plain counts');
  }
  function buildHead(ctx, head) {
    var sp = ctx.spec;
    if (sp.title) { var t = doc.createElement('span'); t.className = 'sk-chart-title'; t.textContent = sp.title; head.appendChild(t); }
    if (sp.subtitle) { var s = doc.createElement('span'); s.className = 'sk-chart-sub'; s.textContent = sp.subtitle; head.appendChild(s); }
  }
  function headline(ctx, head) {
    var h = ctx.headline;
    if (!h || ctx.spec.headline === false || ctx.spec.type === 'bignumber') return;
    var fm = ctx.fmt, d = h.value - h.refValue;
    var good = ctx.spec.good;
    var cls = good ? ((good === 'up' || good === 'higher') === (d > 0) ? ' is-good' : ' is-bad') : '';
    if (Math.abs(d) < 1e-12) cls = '';
    var el = doc.createElement('span');
    el.className = 'sk-chart-delta';
    el.innerHTML = esc(h.label) + ' <b class="sk-num">' + esc(fm.u(h.value)) + '</b>, ' + esc(h.refLabel) +
      ' <b class="sk-num is-ref">' + esc(fm.u(h.refValue)) + '</b>: <b class="sk-num' + cls + '">' + esc(fm.diff(d)) + '</b>';
    head.appendChild(el);
  }
  function mathHTML(line) {
    var s = esc(line);
    s = s.replace(/(^|[\s(=:≈×·/])([−+\-±]?\d[\d.,  ]*\d?(?:\s?(?:%|pts|€|\$|£|k|m|s|h|km\/s|m\/s|km))?)/g, function (m, pre, num) { return pre + '<span class="val">' + num + '</span>'; });
    s = s.replace(/§\s?(\d+)\s*$/, '<span class="sk-sect">§$1</span>');
    return s;
  }
  /* "math" is the field; "maths" is accepted as well */
  function mathOf(sp) { return sp.math != null ? sp.math : sp.maths; }
  function autoMath(ctx) {
    var sp = ctx.spec;
    if (mathOf(sp) !== true) return null;
    var fm = ctx.fmt, out = [];
    if (sp.type === 'bignumber' && ctx.compare) {
      var c = ctx.compare, v = toNum(sp.value);
      out.push('Δ = ' + fm.u(v) + ' − ' + fm.u(c.value) + ' = ' + fm.diff(c.delta) + ' §1');
      if (c.value !== 0) out.push('(' + fm.num(v) + ' − ' + fm.num(c.value) + ') / ' + fm.num(c.value) + ' = ' + (c.delta >= 0 ? '+' : '−') + fm.pct(Math.abs(c.delta / c.value)) + ' §2');
    } else if (sp.type === 'scatter' && ctx.trend) {
      out.push('y = ' + ctx.trend.intercept.toFixed(2) + ' + ' + ctx.trend.slope.toFixed(3) + ' · x §1');
      out.push('r² = ' + ctx.trend.r2.toFixed(2) + ' §2');
    } else if (ctx.headline) {
      var h = ctx.headline;
      out.push(fm.u(h.value) + ' − ' + fm.u(h.refValue) + ' = ' + fm.diff(h.value - h.refValue) + ' §1');
    }
    return out.length ? out : null;
  }
  function buildFoot(ctx, foot) {
    var sp = ctx.spec;
    var notes = [];
    if (ctx.distortion) notes.push(ctx.distortion);
    if (sp.source || notes.length) {
      var p = doc.createElement('p');
      p.className = 'sk-chart-source';
      p.innerHTML = (sp.source ? '<span class="sk-sect">§</span>' + esc(sp.source) : '') + (notes.length ? (sp.source ? '<br>' : '') + mathHTML(notes.join('; ')) : '');
      foot.appendChild(p);
    }
    var m = mathOf(sp), lines = Array.isArray(m) ? m : (typeof m === 'string' ? [m] : autoMath(ctx));
    if (lines && lines.length) {
      var dd = doc.createElement('details');
      dd.className = 'sk-chart-math sk-maths';
      if (sp.mathOpen !== false && sp.mathsOpen !== false) dd.open = true;
      dd.innerHTML = '<summary><span class="sk-m-hide">Σ hide the math</span><span class="sk-m-show">Σ show the math</span></summary>' +
        lines.map(function (l) { return '<p>' + mathHTML(l) + '</p>'; }).join('');
      foot.appendChild(dd);
    }
  }
  function buildTable(ctx, figure) {
    var t = ctx.table;
    if (!t) return;
    // a table grows to its content whatever its width says, so it sits in a clipped box
    var box = part(figure, 'div', 'sk-sr');
    var tbl = doc.createElement('table');
    tbl.className = 'sk-sr';
    box.appendChild(tbl);
    var cap = doc.createElement('caption');
    cap.textContent = (ctx.spec.title || ctx.spec.type) + (ctx.fmt && ctx.fmt.unit ? ' (' + ctx.fmt.unit + ')' : '');
    tbl.appendChild(cap);
    var thead = doc.createElement('thead'), tr = doc.createElement('tr');
    t.head.forEach(function (h) { var th = doc.createElement('th'); th.scope = 'col'; th.textContent = h; tr.appendChild(th); });
    thead.appendChild(tr); tbl.appendChild(thead);
    var tb = doc.createElement('tbody');
    t.rows.forEach(function (r) {
      var row = doc.createElement('tr');
      r.forEach(function (c, i) { var cell = doc.createElement(i ? 'td' : 'th'); if (!i) cell.scope = 'row'; cell.textContent = c == null ? '' : c; row.appendChild(cell); });
      tb.appendChild(row);
    });
    tbl.appendChild(tb);
  }
  function paint(ctx, body) {
    var S = global.Sketchy, H = Math.ceil(ctx.H || defaultHeight(ctx));
    var svg = svgEl('svg', {
      'class': 'sk-chart-svg', viewBox: '0 0 ' + ctx.W + ' ' + H, width: '100%', role: 'img', focusable: 'false',
      'aria-label': (ctx.spec.title ? ctx.spec.title + '. ' : '') + ctx.spec.type + ' chart; the exact values are in the table that follows.'
    }, body);
    svg.style.aspectRatio = ctx.W + ' / ' + H;
    var texts = ctx.texts, counts = [];
    S.variants(svg, function (p, v) {
      var root = p.root(), lg = {};
      LAYERS.forEach(function (n) { lg[n] = svgEl('g', { 'class': 'sk-ch-' + n }, root); });
      ctx.ops.forEach(function (op) {
        var g = lg[op.layer] || lg.marks;
        if (op.attrs) g = svgEl('g', op.attrs, g);
        p.into(g);
        op.fn(p, v);
      });
      p.into(root);
      if (v === 0) {
        texts.forEach(function (t) {
          var el = p.text(t.x, t.y, t.str, t.o);
          if (!el) return;
          if (t.o.weight == null && t.o.mono) el.style.fontWeight = 700;
          if (t.attrs) for (var k in t.attrs) el.setAttribute(k, t.attrs[k]);
          if (t.count) counts.push({ el: el, to: t.count.to, fmt: t.count.fmt, text: t.str });
        });
      }
    }, { seed: ctx.seed, tokens: ctx.C, width: ctx.lw });
    var hits = svgEl('g', { 'class': 'sk-chart-hits', 'aria-hidden': 'true' }, svg);
    ctx.marks.forEach(function (m) {
      var g = m.geom, e;
      if (m.kind === 'rect') e = svgEl('rect', { x: f2(g.x), y: f2(g.y), width: f2(Math.max(1, g.w)), height: f2(Math.max(1, g.h)) }, hits);
      else if (m.kind === 'circle') e = svgEl('circle', { cx: f2(g.cx), cy: f2(g.cy), r: f2(g.r) }, hits);
      else e = svgEl('path', { d: g.d }, hits);
      e.setAttribute('class', 'sk-mark');
      var d = m.data || {};
      for (var k in d) if (d[k] != null && d[k] !== '') e.setAttribute('data-' + k, d[k]);
      var title = svgEl('title', null, e);
      title.textContent = [d.series && d.series !== 'value' ? d.series : null, d.label].filter(Boolean).join(', ') + (d.shown ? ': ' + d.shown : '');
    });
    ctx.stamps.forEach(function (st) {
      var s = doc.createElement('span');
      s.className = 'sk-stamp sk-chart-stamp' + (st.earned ? '' : ' is-unearned') + (st.color ? ' is-' + st.color : '');
      s.textContent = st.text;
      if (st.size) s.style.fontSize = Math.round(st.size) + 'px';
      s.style.left = (st.x * 100) + '%';
      s.style.top = (st.y * 100) + '%';
      body.appendChild(s);
    });
    ctx.figure.__skCounts = counts;
    return svg;
  }
  function showError(figure, msg) {
    var p = part(figure, 'p', 'sk-chart-error');
    p.textContent = msg;
    if (global.console) console.error('[sketchy-charts] ' + msg);
  }

  function render(figure, spec) {
    var Sk = global.Sketchy;
    if (!figure) return null;
    if (!Sk || !Sk.pen) { if (global.console) console.error('[sketchy-charts] load sketchy.js before drawing charts'); return null; }
    injectStyle();
    if (spec != null) figure.__skSpec = typeof spec === 'string' ? (function () { try { return JSON.parse(spec); } catch (e) { return { __error: 'The chart spec is not valid JSON (' + e.message + ').' }; } })() : spec;
    var raw = figure.__skSpec || readSpec(figure);
    var C = Sk.tokens();
    var theme = doc.documentElement.getAttribute('data-theme') || 'day';
    var body0 = figure.querySelector(':scope > .sk-chart-body');
    var W0 = body0 ? Math.floor(body0.clientWidth) : 0;
    var key = JSON.stringify(raw) + '|' + theme + '|' + (Sk.config && Sk.config.boil) + '|' + fontsReady();
    if (body0 && W0 > 0 && figure.__skKey === key + '|' + W0) return figure;
    Array.prototype.slice.call(figure.children).forEach(function (c) { if (c.hasAttribute('data-sk-part')) figure.removeChild(c); });
    figure.classList.remove('is-slip');
    if (!raw) return null;
    if (raw.__error) { showError(figure, raw.__error); return null; }
    var sp = normalizeSpec(raw);
    if (!TYPES[sp.type]) { showError(figure, 'Unknown chart type "' + sp.type + '". Known: ' + Object.keys(TYPES).join(', ') + '.'); return null; }
    figure.classList.add('sk-chart');
    figure.setAttribute('data-type', sp.type);
    if (sp.type === 'ledger') figure.classList.add('is-slip');
    var head = part(figure, 'figcaption', 'sk-chart-head');
    var body = part(figure, 'div', 'sk-chart-body');
    var foot = part(figure, 'div', 'sk-chart-foot');
    var fs = parseFloat(global.getComputedStyle(figure).fontSize) || 20;
    buildHead({ spec: sp }, head);
    var W = Math.floor(body.clientWidth) || +sp.width || 640;
    var fitH = 0;
    if (sp.fit || figure.hasAttribute('data-fit')) {
      var avail = figure.clientHeight - head.offsetHeight - 40;
      if (avail > 160 && !sp.height) fitH = avail;
    }
    function build(refRoom) {
      var c = makeCtx(figure, sp, C, Math.max(240, W), fs);
      c.seed = String(sp.seed != null ? sp.seed : (sp.title || figure.id || sp.type));
      c.D = normalizeSeries(sp);
      c.fmt = makeFormat(sp, collectNumbers(sp.data).concat(sp.value != null ? [toNum(sp.value)] : []));
      c.refRoom = refRoom || 0;
      if (fitH) c.H = fitH;
      honesty(c);
      TYPES[sp.type](c);
      return c;
    }
    var ctx;
    try {
      ctx = build(0);
      // a reference label with nowhere free along its line: lay out again with a margin for it
      if (ctx.needRefRoom) ctx = build(Math.min(ctx.needRefRoom, ctx.W * 0.3));
      placeNotes(ctx);
    } catch (e) {
      showError(figure, 'This chart could not be drawn: ' + e.message);
      if (global.console) console.error(e);
      return null;
    }
    headline(ctx, head);
    if (!head.firstChild) head.remove();
    buildFoot(ctx, foot);
    if (!foot.firstChild) foot.remove();
    paint(ctx, body);
    buildTable(ctx, figure);
    figure.setAttribute('data-unit', ctx.fmt ? ctx.fmt.unit : '');
    if (ctx.warnings.length) figure.setAttribute('data-sk-warn', ctx.warnings.join(' | ')); else figure.removeAttribute('data-sk-warn');
    figure.__skKey = key + '|' + Math.floor(body.clientWidth || W);
    watch(figure);
    return figure;
  }

  function figuresIn(root) {
    root = root || doc;
    var list = Array.prototype.slice.call(root.querySelectorAll('figure.sk-chart, .sk-chart[data-chart], [data-chart]'));
    if (root.matches && root.matches('figure.sk-chart, [data-chart]')) list.unshift(root);
    return list.filter(function (f, i) { return list.indexOf(f) === i; });
  }
  function renderAll(root) {
    var out = [];
    figuresIn(root).forEach(function (f) {
      try { if (render(f)) out.push(f); } catch (e) { if (global.console) console.error('[sketchy-charts]', e); }
    });
    loadFonts();
    return out;
  }

  /* Re-render on width changes and once the fonts have arrived. */
  var ro = null, fontsAsked = false;
  function watch(figure) {
    if (!global.ResizeObserver) return;
    if (!ro) {
      var pending = new Set(), raf = 0;
      ro = new ResizeObserver(function (entries) {
        entries.forEach(function (e) { pending.add(e.target); });
        if (!raf) raf = global.requestAnimationFrame(function () {
          raf = 0;
          pending.forEach(function (f) { if (f.isConnected && !f.classList.contains('is-drawing')) render(f); });
          pending.clear();
        });
      });
    }
    if (!figure.__skObserved) { figure.__skObserved = true; ro.observe(figure); }
  }
  function loadFonts() {
    if (fontsAsked || !doc.fonts || !doc.fonts.load) return;
    fontsAsked = true;
    if (fontsReady()) return;
    Promise.all([doc.fonts.load('600 16px Caveat'), doc.fonts.load('400 16px "Courier Prime"'), doc.fonts.load('700 16px "Courier Prime"')])
      .then(function () { figuresIn(doc).forEach(function (f) { if (f.__skKey) render(f); }); })
      .catch(function () { /* fonts unavailable: the estimates stand */ });
  }

  /* ================================================================== *
   * Motion: one variant is pinned while the pencil traces, so the boil
   * does not flash between drawn and undrawn copies. Figures count up
   * without moving; stamps land one every 340 ms.
   * ================================================================== */
  function countUp(c, delay, dur) {
    var to = c.to, el = c.el;
    if (!isNum(to)) return;
    var anim;
    try { anim = el.animate([{ '--sk-count': '0' }, { '--sk-count': '1' }], { duration: dur, delay: delay, fill: 'both', easing: 'linear' }); } catch (e) { return; }
    function tick() {
      var t = anim.effect.getComputedTiming().progress;
      if (t == null) t = anim.playState === 'finished' ? 1 : 0;
      var e = 1 - Math.pow(1 - t, 3);
      el.textContent = c.fmt(to * e);
      if (anim.playState !== 'finished') global.requestAnimationFrame(tick); else el.textContent = c.text;
    }
    el.textContent = c.fmt(0);
    global.requestAnimationFrame(tick);
    return anim.finished.then(function () { el.textContent = c.text; }, function () { el.textContent = c.text; });
  }
  function drawOne(fig, opts) {
    var Sk = global.Sketchy;
    var slip = fig.classList.contains('is-slip');
    fig.classList.add('is-drawing');
    var v0 = fig.querySelector('.sk-v0, .sk-v-only');
    var labels = fig.querySelector('.sk-chart-svg > .sk-labels');
    var stamps = Array.prototype.slice.call(fig.querySelectorAll('.sk-chart-stamp'));
    stamps.forEach(function (s) { s.style.opacity = '0'; s.classList.remove('is-slam'); });
    var waits = [];
    var stagger = opts.stagger != null ? opts.stagger : 12, dur = opts.duration || 520, ease = 'cubic-bezier(.35,.1,.25,1)';
    var last = 0;
    // The start state is written with transitions off and flushed before the transition is
    // set; writing both in one style change starts a delayed transition towards the start
    // value, and the release then cancels it, so nothing would move.
    function flush(el) { if (el) void global.getComputedStyle(el).opacity; }
    if (slip) {
      // receipt printer: rows appear one after the other, 95 ms apart after 180 ms
      var rows = {};
      Array.prototype.forEach.call(fig.querySelectorAll('[data-row]'), function (el) {
        if (el.closest('.sk-v') && !el.closest('.sk-v0, .sk-v-only')) return;
        var r = +el.getAttribute('data-row'); (rows[r] = rows[r] || []).push(el);
      });
      var all = [];
      Object.keys(rows).forEach(function (r) { rows[r].forEach(function (el) { el.style.transition = 'none'; el.style.opacity = '0'; all.push([el, 180 + r * 95]); }); last = Math.max(last, 180 + r * 95 + 160); });
      flush(all.length && all[0][0]);
      all.forEach(function (a) { a[0].style.transition = 'opacity 160ms ease-out ' + a[1] + 'ms'; a[0].style.opacity = ''; });
    } else if (v0) {
      var paths = Array.prototype.slice.call(v0.querySelectorAll('.sk-path, .sk-hatch, .sk-wash'));
      var plan = paths.map(function (pth, i) {
        var traced = pth.classList.contains('sk-path') && !pth.getAttribute('stroke-dasharray');
        pth.style.transition = 'none';
        if (traced) { pth.style.strokeDasharray = '1 1'; pth.style.strokeDashoffset = '1'; } else pth.style.opacity = '0';
        var at = (opts.delay || 0) + i * stagger;
        last = Math.max(last, at + dur * 1.9);
        return { el: pth, traced: traced, at: at };
      });
      if (labels) { labels.style.transition = 'none'; labels.style.opacity = '0'; }
      flush(paths[0] || labels);
      plan.forEach(function (q) {
        if (q.traced) { q.el.style.transition = 'stroke-dashoffset ' + dur + 'ms ' + ease + ' ' + q.at + 'ms'; q.el.style.strokeDashoffset = '0'; }
        else { q.el.style.transition = 'opacity ' + Math.round(dur * 1.3) + 'ms ease-out ' + Math.round(q.at + dur * 0.6) + 'ms'; q.el.style.opacity = ''; }
      });
      if (labels) { labels.style.transition = 'opacity 420ms ease-out ' + Math.round(last * 0.35) + 'ms'; labels.style.opacity = ''; }
    }
    (fig.__skCounts || []).forEach(function (c) { var p = countUp(c, slip ? last : Math.round(last * 0.35), 900); if (p) waits.push(p); });
    stamps.forEach(function (s, k) {
      var at = last + 120 + k * 340;
      if (s.classList.contains('is-unearned')) {
        s.style.transition = 'none'; s.style.opacity = '0'; flush(s);
        s.style.transition = 'opacity 300ms ease-out ' + at + 'ms'; s.style.opacity = '';
      } else { s.style.animationDelay = at + 'ms'; s.style.opacity = ''; s.classList.add('is-slam'); }
      last = Math.max(last, at + 360);
    });
    waits.push(new Promise(function (res) { global.setTimeout(res, last + 60); }));
    return Promise.all(waits).then(function () {
      fig.classList.remove('is-drawing');
      Array.prototype.forEach.call(fig.querySelectorAll('.sk-path, .sk-hatch, .sk-wash, [data-row], .sk-labels'), function (el) { el.style.transition = ''; el.style.strokeDasharray = ''; el.style.strokeDashoffset = ''; });
    });
  }
  function drawOn(target, opts) {
    opts = opts || {};
    var figs = target && target.matches && target.matches('.sk-chart') ? [target] : Array.prototype.slice.call((target || doc).querySelectorAll('.sk-chart'));
    if (isStatic() || opts.instant) return Promise.resolve();
    return Promise.all(figs.map(function (f, i) { return drawOne(f, Object.assign({}, opts, { delay: (opts.delay || 0) })); }));
  }

  /* ================================================================== *
   * Registration with the engine: Sketchy.onMount, whichever file loads first
   * ================================================================== */
  var api = {
    version: VERSION,
    render: render, renderAll: renderAll, drawOn: drawOn,
    types: function () { return Object.keys(TYPES); },
    register: function (name, fn) { TYPES[String(name).toLowerCase()] = fn; },
    format: makeFormat
  };
  global.SketchyCharts = api;

  function hook(Sk) {
    if (!Sk || Sk.__skCharts) return;
    Sk.__skCharts = true;
    if (typeof Sk.onMount === 'function') Sk.onMount(function (root) { renderAll(root || doc); });
    else if (typeof Sk.mount === 'function') {
      var orig = Sk.mount;
      Sk.mount = function () { var out = orig.apply(this, arguments); renderAll(arguments[0] || doc); return out; };
      Sk.mount._watching = orig._watching;
    }
    // Sketchy.drawOn(root) also reveals the charts inside root with the chart motion
    // (pinned variant, receipt rows, counting figures, stamps)
    if (typeof Sk.drawOn === 'function' && !Sk.drawOn.__skCharts) {
      var origDraw = Sk.drawOn;
      var wrapped = function (root) {
        var out = origDraw.apply(this, arguments);
        var r = root || doc, figs = r.matches && r.matches('.sk-chart') ? [r] : Array.prototype.slice.call(r.querySelectorAll ? r.querySelectorAll('.sk-chart') : []);
        if (!figs.length) return out;
        return Promise.all([out].concat(figs.map(function (f) { return drawOn(f); }))).then(function () {});
      };
      wrapped.__skCharts = true;
      Sk.drawOn = wrapped;
    }
    // sketchy.js was mounted before this file loaded: draw now
    if (Sk.mount && (Sk.mount._watching || (Sk.mount._orig && Sk.mount._orig._watching))) {
      if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', function () { renderAll(doc); });
      else renderAll(doc);
    }
  }
  if (global.Sketchy) hook(global.Sketchy);
  else {
    try {
      var held;
      Object.defineProperty(global, 'Sketchy', {
        configurable: true, enumerable: true,
        get: function () { return held; },
        set: function (v) {
          held = v;
          Object.defineProperty(global, 'Sketchy', { value: v, writable: true, configurable: true, enumerable: true });
          hook(v);
        }
      });
    } catch (e) {
      doc.addEventListener('DOMContentLoaded', function () { hook(global.Sketchy); });
    }
  }
})(typeof window !== 'undefined' ? window : this);
