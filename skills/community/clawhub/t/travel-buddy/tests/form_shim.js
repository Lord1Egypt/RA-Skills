// A DOM small enough to run the intake form's own JavaScript, built FROM the form's HTML.
//
// The form is where every answer the traveller types lands -- fifty-odd fields, several
// conditional branches, and a build() that both validates and assembles the intake JSON the whole
// pipeline reads. Nothing tested it. Both defects fixed on 2026-08-30 went in without one, and
// both were the same shape: a field that was collected but not required, so it came back null and
// the question got asked in chat instead. A null that reaches the assistant is indistinguishable
// from an answer of "nothing", which is why this needs execution rather than a reader.
//
// Elements are derived from the markup rather than declared here, so a field renamed in the HTML
// and not in the JS shows up as a null element instead of a stub that quietly answers "".
"use strict";
const fs = require("fs");

// `config` is what the local server injects as window.TRAVEL_BUDDY_TRIP_INTAKE -- the display
// language among it -- so a test can load the same page the way an English traveller gets it.
// `options.fetch` replaces the network, so a test can see what a submission actually sends.
module.exports = function load(htmlPath, config = {}, options = {}) {
  const html = fs.readFileSync(htmlPath, "utf8");
  // Only JavaScript is executed; the zh/en dictionary is a JSON <script> the page reads by id.
  const scripts = [...html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)];
  const js = scripts.filter((m) => !/type="application\/json"/.test(m[1])).map((m) => m[2]).join("\n");
  const ids = [...new Set([...html.matchAll(/id="([^"]+)"/g)].map((m) => m[1]))];
  const opts = {};
  for (const m of html.matchAll(/<select id="([^"]+)"([\s\S]*?)<\/select>/g)) {
    opts[m[1]] = [...m[2].matchAll(/<option\b([^>]*)>([^<]*)</g)]
      .map((o) => { const v = o[1].match(/\bvalue="([^"]*)"/); return v ? v[1] : o[2]; });
  }

  const el = (id) => ({
    id, value: "", hidden: false, textContent: "", innerHTML: "", checked: false, disabled: false,
    style: {}, dataset: {}, classList: { add() {}, remove() {}, toggle() {}, contains: () => false },
    options: opts[id] ? opts[id].map((v) => ({ value: v, text: v })) : null,
    listeners: {},
    addEventListener(type, fn) { (this.listeners[type] = this.listeners[type] || []).push(fn); },
    removeEventListener() {}, focus() {}, scrollIntoView() {},
    setAttribute() {}, getAttribute: () => null, removeAttribute() {}, appendChild() {},
    querySelectorAll: () => [], querySelector: () => null, closest: () => null,
    insertAdjacentHTML() {}, reset() {}, checkValidity: () => true, remove() {},
    append() {}, prepend() {}, replaceChildren() {}, add() {}, item: () => null,
  });

  const store = {};
  ids.forEach((i) => { store[i] = el(i); });
  for (const m of scripts) {
    const id = (m[1].match(/\bid="([^"]+)"/) || [])[1];
    if (id && store[id]) store[id].textContent = m[2];
  }
  // A real <select> assigned a value it does not offer ends up with NO value -- it does not keep
  // the string. The stub used to keep it, which is how the example button could set a scope the
  // page had stopped offering while every test still passed. Selects whose markup declares their
  // options behave the real way; the ones the script builds at runtime (budget-range, the two
  // ranking lists) cannot be known from the markup and keep whatever they are given.
  for (const [id, values] of Object.entries(opts)) {
    if (!store[id] || !values.filter(Boolean).length) continue;
    let current = values.includes("") ? "" : values[0];
    Object.defineProperty(store[id], "value", {
      get: () => current,
      set: (next) => { current = values.includes(String(next)) ? String(next) : ""; },
      enumerable: true,
    });
  }

  // Checkbox and radio groups, built from the markup, so `checked("natural")` returns what the
  // page would return. Without these the transport-mode check refuses every submission and the
  // baseline never passes -- which is a test that proves nothing, not a test that found a bug.
  const groups = {};
  for (const m of html.matchAll(/<input([^>]*)>/g)) {
    const tag = m[1];
    const name = (tag.match(/name="([^"]+)"/) || [])[1];
    const value = (tag.match(/value="([^"]*)"/) || [])[1];
    if (!name || value === undefined) continue;
    const node = { name, value, checked: false, type: /type="radio"/.test(tag) ? "radio" : "checkbox",
                   addEventListener() {} };
    (groups[name] = groups[name] || []).push(node);
  }

  const g = {
    document: {
      getElementById: (i) => store[i] || null,
      querySelectorAll: (sel) => {
        const out = [];
        if (/input\[type="checkbox"\]/.test(String(sel))) {
          for (const nodes of Object.values(groups)) out.push(...nodes.filter((n) => n.type === "checkbox"));
        }
        for (const m of String(sel).matchAll(/input\[name="([^"]+)"\](:checked)?/g)) {
          const nodes = groups[m[1]] || [];
          out.push(...(m[2] ? nodes.filter((n) => n.checked) : nodes));
        }
        return out;
      },
      querySelector: (sel) => {
        const m = String(sel).match(/^input\[name="([^"]+)"\]\[value="([^"]+)"\]$/);
        return m ? (groups[m[1]] || []).find((n) => n.value === m[2]) || null : null;
      },
      createElement: () => el("created"), body: el("body"),
      documentElement: el("html"), addEventListener() {},
    },
    window: { TRAVEL_BUDDY_TRIP_INTAKE: config, addEventListener() {}, setTimeout, clearTimeout,
              location: { search: "", href: "http://127.0.0.1/" } },
    localStorage: { getItem: () => null, setItem() {}, removeItem() {} },
    fetch: options.fetch || (async () => ({ ok: true, json: async () => ({}), text: async () => "" })),
    navigator: { language: "zh-CN" },
    location: { search: "", href: "http://127.0.0.1/" },
    alert() {},
    Option: function (t, v) { return { text: t, value: v === undefined ? t : v }; },
    CustomEvent: function (n, d) { return { type: n, detail: d && d.detail }; },
    Event: function (n) { return { type: n }; },
    crypto: { randomUUID: () => "test-uuid", getRandomValues: (a) => a },
  };
  // Injected as function parameters rather than assigned onto `global`. Modern Node makes some
  // of these (navigator) getter-only, and a test that mutates the real global environment can
  // leak into whatever runs next; a parameter list cannot.
  // The whole form lives inside one `(() => { ... })();`, so build() is not reachable from
  // outside it -- which is correct for the page and useless for a test. A probe call is injected
  // just before that IIFE closes. If the anchor is ever not found the load FAILS rather than
  // returning a null build: a test that silently stops exercising the form is worse than no test,
  // because the suite still goes green.
  const anchor = "})();";
  const at = js.lastIndexOf(anchor);
  if (at < 0) {
    throw new Error("form_shim: could not find the form's closing IIFE; the probe was not "
      + "injected, so nothing would have been tested. Update the anchor.");
  }
  const probed = `${js.slice(0, at)}\n__probe({ build, text, $, updateConditionalPanels, `
    + `applyLanguage: typeof applyLanguage === "function" ? applyLanguage : null });\n`
    + js.slice(at);

  let captured = null;
  g.__probe = (api) => { captured = api; };
  const names = Object.keys(g);
  let topLevelError = null;
  try {
    new Function(...names, probed)(...names.map((n) => g[n]));
  } catch (err) {
    topLevelError = err.message;
  }
  const build = captured && captured.build;

  // A select is set only to a value it really offers. A test that types an option the page does
  // not have passes while the real form refuses -- the failure mode this whole file exists to
  // stop, one level up.
  const set = (id, value) => {
    if (!store[id]) throw new Error(`no such field: ${id}`);
    // A select whose only markup option is the empty placeholder is populated at runtime
    // (budget-range is built from the chosen currency), so its values are not knowable from the
    // HTML and validating against them would reject every real value.
    const declared = (opts[id] || []).filter(Boolean);
    if (declared.length && value !== "" && !declared.includes(value)) {
      throw new Error(`${id} has no option ${JSON.stringify(value)}; it offers ${declared.join(", ")}`);
    }
    store[id].value = value;
  };
    const tick = (name, ...values) => {
    const nodes = groups[name] || [];
    if (!nodes.length) throw new Error(`no such input group: ${name}`);
    for (const n of nodes) n.checked = values.includes(n.value);
    const hit = values.filter((v) => !nodes.some((n) => n.value === v));
    if (hit.length) throw new Error(`no such value in ${name}: ${hit.join(", ")}`);
  };
  // Runs the page's own listeners for `type` on element `id`, the way a click would.
  const fire = (id, type) => {
    if (!store[id]) throw new Error(`no such element: ${id}`);
    const handlers = store[id].listeners[type] || [];
    if (!handlers.length) throw new Error(`${id} has no ${type} listener`);
    for (const handler of handlers) handler({ type, preventDefault() {}, target: store[id] });
  };
  return { store, opts, ids, groups, tick, build, topLevelError, set, fire, api: captured,
           get: (id) => (store[id] ? store[id].value : null) };
};
