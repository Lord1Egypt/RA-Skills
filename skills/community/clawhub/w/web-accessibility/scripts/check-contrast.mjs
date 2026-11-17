#!/usr/bin/env node
/* WCAG 2 contrast validator — zero dependencies, Node >= 14.
 *
 * Implements the relative-luminance contrast ratio from WCAG 2.2.
 * Thresholds you'll typically assert:
 *   4.5 — normal text            (SC 1.4.3, Level AA)
 *   3.0 — large text             (SC 1.4.3, Level AA)
 *   3.0 — meaningful non-text    (SC 1.4.11, Level AA)
 * Reference: https://www.w3.org/WAI/WCAG2AA-Conformance
 *
 * Usage:
 *   # ad-hoc pairs (repeatable): fg,bg,minimum,label
 *   node check-contrast.mjs --pair "#0f766e,#ffffff,4.5,link on white"
 *
 *   # or a JSON config file:
 *   node check-contrast.mjs contrast-pairs.json
 *
 * Config format (colors map is optional — pairs may use raw hex directly):
 *   {
 *     "colors": { "teal-700": "#0f766e", "white": "#ffffff" },
 *     "pairs": [
 *       ["teal-700", "white", 4.5, "link on white"],
 *       ["#111827", "#14b8a6", 4.5, "primary button text"]
 *     ]
 *   }
 *
 * Exits non-zero if any pair is below its minimum — wire it into your build
 * or CI so a failing color can't ship.
 */

import { readFileSync } from "node:fs";

const HEX = /^#?([0-9a-f]{3}|[0-9a-f]{6})$/i;

const normalizeHex = (raw) => {
  const m = HEX.exec(raw.trim());
  if (!m) return null;
  let h = m[1].toLowerCase();
  if (h.length === 3) h = [...h].map((c) => c + c).join("");
  return `#${h}`;
};

// WCAG 2.x relative luminance (sRGB)
const luminance = (hex) => {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
    .map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};

const contrast = (fgHex, bgHex) => {
  const [hi, lo] = [luminance(fgHex), luminance(bgHex)].sort((a, b) => b - a);
  return (hi + 0.05) / (lo + 0.05);
};

// ---- collect pairs from CLI and/or config ---------------------------------
const args = process.argv.slice(2);
const pairs = []; // { fg, bg, min, label }
let colors = {};

const resolve = (nameOrHex) => {
  const fromMap = colors[nameOrHex];
  const hex = normalizeHex(fromMap ?? nameOrHex);
  if (!hex) {
    console.error(`error: "${nameOrHex}" is neither a defined color name nor a hex value`);
    process.exit(2);
  }
  return hex;
};

const addPair = (fg, bg, min, label) => {
  const minimum = Number(min);
  if (!Number.isFinite(minimum) || minimum <= 0) {
    console.error(`error: invalid minimum "${min}" for pair "${label ?? `${fg}/${bg}`}"`);
    process.exit(2);
  }
  pairs.push({ fg, bg, min: minimum, label: label ?? `${fg} on ${bg}` });
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--pair") {
    const spec = args[++i];
    if (!spec) { console.error("error: --pair needs a value: fg,bg,min,label"); process.exit(2); }
    const [fg, bg, min, ...label] = spec.split(",");
    addPair(fg, bg, min ?? "4.5", label.join(",").trim() || undefined);
  } else if (args[i] === "--help" || args[i] === "-h") {
    console.log("usage: check-contrast.mjs [config.json] [--pair fg,bg,min,label]...");
    process.exit(0);
  } else {
    let config;
    try {
      config = JSON.parse(readFileSync(args[i], "utf8"));
    } catch (e) {
      console.error(`error: cannot read config "${args[i]}": ${e.message}`);
      process.exit(2);
    }
    colors = { ...colors, ...(config.colors ?? {}) };
    for (const p of config.pairs ?? []) addPair(p[0], p[1], p[2] ?? 4.5, p[3]);
  }
}

if (pairs.length === 0) {
  console.error("no pairs given — pass a config file and/or --pair fg,bg,min,label (see --help)");
  process.exit(2);
}

// ---- check -----------------------------------------------------------------
let failed = 0;
for (const { fg, bg, min, label } of pairs) {
  const r = contrast(resolve(fg), resolve(bg));
  const ok = r >= min;
  if (!ok) failed++;
  console.log(`${ok ? "  ok " : "FAIL "} ${r.toFixed(2)}:1 (min ${min}) ${label}`);
}

if (failed) {
  console.error(`\n${failed} pair(s) below the WCAG minimum — fix the colors before shipping.`);
  process.exit(1);
}
console.log(`all ${pairs.length} pairs pass`);
