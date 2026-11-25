// Every theme pack must have a light and a dark version, never force a mode,
// and keep text at WCAG AA contrast. Run with: node --test tests/theme-packs.test.mjs
// It reads PACKS out of src/lib/theme-packs.ts without a TypeScript build.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const src = readFileSync(new URL("../src/lib/theme-packs.ts", import.meta.url), "utf8");
const body = src.slice(src.indexOf("export const PACKS"));
const arr = body.slice(body.indexOf("["), body.indexOf("\n];") + 2);
// The array is a plain literal: evaluate it as JS.
const PACKS = Function(`return ${arr}`)();

const lum = (hex) => {
  const n = parseInt(hex.slice(1), 16);
  const c = [n >> 16, (n >> 8) & 255, n & 255].map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
};
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };

test("there is at least one pack and ids are unique", () => {
  assert.ok(PACKS.length > 0);
  assert.equal(new Set(PACKS.map((p) => p.id)).size, PACKS.length);
});

for (const p of PACKS) {
  test(`${p.id}: has light and dark, and no forced mode`, () => {
    assert.ok(p.tokens?.light, `${p.id} is missing light`);
    assert.ok(p.tokens?.dark, `${p.id} is missing dark`);
    assert.equal(p.mode, undefined, `${p.id} must not force a mode`);
    assert.ok(p.preview, `${p.id} needs a preview`);
  });
  for (const mode of ["light", "dark"]) {
    test(`${p.id} (${mode}): AA contrast`, () => {
      const t = p.tokens[mode];
      for (const [fg, bg] of [["text", "bg"], ["text", "surface"], ["muted", "bg"], ["onAccent", "accent"]]) {
        assert.ok(ratio(t[fg], t[bg]) >= 4.5, `${fg} on ${bg} is ${ratio(t[fg], t[bg]).toFixed(2)}:1`);
      }
    });
  }
}
