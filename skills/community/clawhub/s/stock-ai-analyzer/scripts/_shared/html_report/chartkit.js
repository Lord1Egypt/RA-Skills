/* shared/html_report chart kit — one copy of the SVG + DOM primitives that
 * every skill's chart hook used to redefine for itself. Injected once by the
 * builder (right after the base UI script, before any ChartHook IIFE), so
 * hook JS can read everything off `window.CK` instead of carrying private
 * copies of svgEl / svgText / tooltip / card / legend / heading-finders,
 * metric cards, or simple horizontal bars.
 *
 * Skill-specific number formatting (price precision, 亿/万亿 unit divisors)
 * stays in each skill's hook because the units genuinely differ; only the
 * truly shared plumbing lives here. */
window.CK = (function () {
  const NS = "http://www.w3.org/2000/svg";

  function svgEl(name, attrs) {
    const el = document.createElementNS(NS, name);
    Object.entries(attrs || {}).forEach(([k, v]) => el.setAttribute(k, v));
    return el;
  }

  function svgText(x, y, text, anchor, color, size) {
    const el = svgEl("text", {
      x, y,
      "text-anchor": anchor || "start",
      fill: color || "var(--ink-4)",
      "font-size": size || 11,
    });
    el.textContent = text;
    return el;
  }

  const fmt = {
    /* YYYYMMDD -> YYYY-MM-DD (identical across every skill) */
    date: (v) => String(v || "").replace(/^(\d{4})(\d{2})(\d{2})$/, "$1-$2-$3"),
    /* general numeric: >=100 -> 1 decimal, else 2 (override with explicit d) */
    num: (v, d) => (Number.isFinite(v) ? v.toFixed(d == null ? (Math.abs(v) >= 100 ? 1 : 2) : d) : "—"),
    /* signed percentage, e.g. +2.04% / -3.07% */
    signedPct: (v) => (Number.isFinite(v) ? `${v > 0 ? "+" : ""}${v.toFixed(2)}%` : "—"),
  };

  function num(value) {
    const n = Number(value);
    return Number.isFinite(n) ? n : null;
  }

  function signedClass(value) {
    const n = Number(value);
    if (!Number.isFinite(n) || n === 0) return "";
    return n > 0 ? "pos" : "neg";
  }

  /* dark floating tooltip; appended to `card`, returns the element */
  function tooltip(card) {
    const tip = document.createElement("div");
    tip.style.cssText =
      "position:absolute;background:rgba(15,23,42,0.92);color:#f1f5f9;padding:8px 12px;border-radius:8px;font-size:12px;line-height:1.5;pointer-events:none;opacity:0;transition:opacity .15s ease;z-index:100;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,0.2);";
    card.style.position = "relative";
    card.appendChild(tip);
    return tip;
  }

  function moveTip(tip, card, e) {
    const r = card.getBoundingClientRect();
    tip.style.left = Math.min(e.clientX - r.left + 12, r.width - tip.offsetWidth - 8) + "px";
    tip.style.top = Math.max(8, e.clientY - r.top - tip.offsetHeight - 12) + "px";
  }

  /* <article class=cls><div.chart-title><div.chart-subtitle> */
  function card(cls, title, subtitle) {
    const c = document.createElement("article");
    c.className = cls;
    if (title) {
      const t = document.createElement("div");
      t.className = "chart-title";
      t.textContent = title;
      c.appendChild(t);
    }
    if (subtitle) {
      const s = document.createElement("div");
      s.className = "chart-subtitle";
      s.textContent = subtitle;
      c.appendChild(s);
    }
    return c;
  }

  /* legend from [[label, color], ...] */
  function legend(items) {
    const l = document.createElement("div");
    l.className = "legend";
    (items || []).forEach(([label, color]) => {
      const span = document.createElement("span");
      span.style.setProperty("--legend-color", color);
      span.textContent = label;
      l.appendChild(span);
    });
    return l;
  }

  function grid(cls) {
    const g = document.createElement("div");
    g.className = cls || "chart-grid";
    return g;
  }

  function metricCard(spec) {
    const c = document.createElement("article");
    c.className = spec.className || "metric-card";

    const title = document.createElement("div");
    title.className = "metric-title";
    title.textContent = spec.title || "";

    const value = document.createElement("div");
    const signCls = signedClass(spec.signValue);
    value.className = `metric-value${signCls ? ` ${signCls}` : ""}`;
    value.textContent = spec.value == null ? "—" : String(spec.value);

    const sub = document.createElement("div");
    sub.className = "metric-sub";
    sub.textContent = spec.subtitle || spec.sub || "";

    c.append(title, value, sub);
    return c;
  }

  function metricGrid(items) {
    const g = document.createElement("div");
    g.className = "metric-grid";
    (items || []).forEach(item => g.appendChild(metricCard(item)));
    return g;
  }

  function horizontalBarCard(spec) {
    const rows = (spec.rows || []).slice(0, spec.maxRows || 12);
    const c = card(spec.className || "chart-card", spec.title, spec.subtitle);
    if (!rows.length) return c;

    const W = spec.width || 520;
    const rowH = spec.rowHeight || 24;
    const top = spec.top == null ? 18 : spec.top;
    const bottom = spec.bottom == null ? 20 : spec.bottom;
    const pad = {
      l: spec.labelWidth || 94,
      r: spec.valueWidth || 58,
      t: top,
      b: bottom,
    };
    const H = top + rows.length * rowH + bottom;
    const svg = svgEl("svg", { viewBox: `0 0 ${W} ${H}`, role: "img" });
    const maxAbs = Math.max(1, ...rows.map(row => Math.abs(num(row.value) || 0)));
    const zeroX = pad.l + (W - pad.l - pad.r) / 2;
    const scale = (W - pad.l - pad.r) / 2 / maxAbs;

    svg.appendChild(svgEl("line", {
      x1: zeroX,
      x2: zeroX,
      y1: pad.t - 8,
      y2: H - pad.b + 4,
      class: "grid-line",
    }));

    rows.forEach((row, i) => {
      const y = pad.t + i * rowH;
      const value = num(row.value) || 0;
      const width = Math.abs(value) * scale;
      const x = value >= 0 ? zeroX : zeroX - width;
      const signCls = value >= 0 ? "pos" : "neg";

      const label = svgText(8, y + 13, row.label || "", "start", "var(--ink-2)", 10);
      label.setAttribute("class", "bar-label");
      svg.appendChild(label);

      svg.appendChild(svgEl("rect", {
        x: x.toFixed(2),
        y: (y + 3).toFixed(2),
        width: Math.max(1, width).toFixed(2),
        height: 12,
        rx: 3,
        class: `bar-fill ${signCls === "pos" ? "bar-pos" : "bar-neg"}`,
      }));

      const valueText = svgText(W - 8, y + 13, fmt.signedPct(value), "end", null, 10);
      valueText.setAttribute("class", `bar-value ${signCls}`);
      svg.appendChild(valueText);

      if (row.meta) {
        const meta = svgText(pad.l - 8, y + 13, row.meta, "end", "var(--ink-4)", 9);
        meta.setAttribute("class", "bar-meta");
        svg.appendChild(meta);
      }
    });

    c.appendChild(svg);
    return c;
  }

  /* first heading (default h2/h3/h4) whose text contains one of `texts` */
  function findHeading(root, texts, sel) {
    const list = Array.from(root.querySelectorAll(sel || "h2, h3, h4"));
    const arr = Array.isArray(texts) ? texts : [texts];
    for (const t of arr) {
      const h = list.find((e) => e.textContent.includes(t));
      if (h) return h;
    }
    return null;
  }

  /* the next .table-wrap after a heading, or null if a heading intervenes */
  function findNextTable(heading) {
    let cur = heading.nextElementSibling;
    while (cur) {
      if (cur.classList && cur.classList.contains("table-wrap")) return cur;
      if (/^H[234]$/.test(cur.tagName || "")) return null;
      cur = cur.nextElementSibling;
    }
    return null;
  }

  function insertAfter(root, texts, node, fallback) {
    const heading = findHeading(root, texts);
    if (heading) {
      heading.after(node);
      return;
    }
    const target = fallback || root.querySelector("h1");
    if (target && target.nextElementSibling) target.nextElementSibling.before(node);
    else root.prepend(node);
  }

  return {
    NS,
    svgEl,
    svgText,
    fmt,
    num,
    signedClass,
    tooltip,
    moveTip,
    card,
    legend,
    grid,
    metricCard,
    metricGrid,
    horizontalBarCard,
    findHeading,
    findNextTable,
    insertAfter,
  };
})();
