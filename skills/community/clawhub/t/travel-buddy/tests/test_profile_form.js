// The profile form's own JavaScript, executed — the one form nothing tested.
//
// This is the FIRST screen a new traveller ever sees, it is the only one whose answers are kept
// between trips, and until now the suite had nothing that ran a line of it. The trip form got a
// shim and two test files; this one was skipped because it looked simpler. It was not simpler,
// it was less examined.
//
// What running it found, all three the same shape — a value the traveller typed that reached the
// profile meaning nothing:
//
//   * `exclusion_strength` was free text with a pass-through. Downstream is an exact comparison
//     (`serve_trip_intake.never_recommend_places` keeps entries where the field `== "never_recommend"`),
//     so a traveller who wrote 「绝对不去」 — the strongest thing they can say — produced an
//     exclusion that matched nothing, filtered nothing, and reported nothing. The form asked them
//     to type a machine enum and then silently discarded every other answer.
//   * `revisit_interest` the same, against `== "no"`.
//   * `priority` went through bare `Number()`, so 「高」 became NaN became `null` in the JSON, and
//     999 was stored as a rank that sorts above every real one.
//
// So the assertions below come in pairs on purpose: what a person actually writes must be
// UNDERSTOOD, and what cannot be understood must be REFUSED by name — never stored as a value
// that quietly does nothing. The second half is the half that was missing.
//
// Run:  node tests/test_profile_form.js
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const FORM = path.join(ROOT, "assets", "traveler-profile-intake.html");

const html = fs.readFileSync(FORM, "utf8");
// Only JavaScript runs; the zh/en dictionary is a JSON <script> the page reads by id.
const scripts = [...html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)];
const js = scripts.filter((m) => !/type="application\/json"/.test(m[1])).map((m) => m[2]).join("\n");
const ids = [...new Set([...html.matchAll(/id="([^"]+)"/g)].map((m) => m[1]))];

// One instance of the page per call, so the same answers can be given to the Chinese page and the
// English one. `config` is what serve_profile_intake.py injects as TRAVEL_BUDDY_PROFILE_INTAKE.
function loadForm(config = {}, options = {}) {
  const el = (id) => ({
    id, value: "", checked: false, hidden: false, textContent: "", innerHTML: "",
    style: {}, dataset: {}, classList: { add() {}, remove() {}, toggle() {}, contains: () => false },
    listeners: {},
    addEventListener(type, fn) { (this.listeners[type] = this.listeners[type] || []).push(fn); },
    focus() {}, setAttribute() {}, getAttribute: () => null,
    querySelectorAll: () => [], querySelector: () => null, closest: () => null,
    reset() {}, checkValidity: () => true,
  });
  const store = {};
  ids.forEach((i) => { store[i] = el(i); });
  for (const m of scripts) {
    const id = (m[1].match(/\bid="([^"]+)"/) || [])[1];
    if (id && store[id]) store[id].textContent = m[2];
  }
  // Checkbox groups from the markup, so checked("natural") and the example button's
  // querySelector('input[name=..][value=..]') see what the page would.
  const groups = {};
  for (const m of html.matchAll(/<input([^>]*)>/g)) {
    const name = (m[1].match(/name="([^"]+)"/) || [])[1];
    const value = (m[1].match(/value="([^"]*)"/) || [])[1];
    if (name && value !== undefined) (groups[name] = groups[name] || []).push({ name, value, checked: false });
  }
  const g = {
    document: {
      getElementById: (i) => store[i] || null,
      querySelector: (sel) => {
        const m = String(sel).match(/^input\[name="([^"]+)"\]\[value="([^"]+)"\]$/);
        return m ? (groups[m[1]] || []).find((n) => n.value === m[2]) || null : null;
      },
      querySelectorAll: (sel) => {
        const out = [];
        for (const m of String(sel).matchAll(/input\[name="([^"]+)"\](:checked)?/g)) {
          const nodes = groups[m[1]] || [];
          out.push(...(m[2] ? nodes.filter((n) => n.checked) : nodes));
        }
        return out;
      },
      addEventListener() {}, createElement: () => el("x"), body: el("body"), documentElement: el("html"),
    },
    window: { TRAVEL_BUDDY_PROFILE_INTAKE: config, addEventListener() {}, location: { href: "" },
              setTimeout, clearTimeout },
    fetch: options.fetch || (async () => ({ ok: true, json: async () => ({}) })),
    console, JSON, Date, Number, String, Array, Object, Math, parseInt, parseFloat, isNaN, Error, RegExp,
  };

  // The probe is injected before the form's IIFE closes. If the anchor ever moves, this THROWS
  // rather than leaving `buildProfile` undefined — a test that stops exercising the form while the
  // suite stays green is worse than no test, which is the lesson the trip-form shim already carries.
  const anchor = "})();";
  const at = js.lastIndexOf(anchor);
  if (at < 0) {
    throw new Error("test_profile_form: could not find the form's closing IIFE; the probe was not "
      + "injected, so nothing would have been tested. Update the anchor.");
  }
  let api = null;
  g.__probe = (found) => { api = found; };
  const names = Object.keys(g);
  new Function(...names, js.slice(0, at)
    + "\n__probe({ buildProfile, applyLanguage: typeof applyLanguage === \"function\" ? applyLanguage : null });\n"
    + js.slice(at))(...names.map((n) => g[n]));
  if (!api || typeof api.buildProfile !== "function") {
    throw new Error("test_profile_form: buildProfile was never captured; nothing was tested.");
  }
  const fire = (id, type) => {
    const handlers = (store[id] && store[id].listeners[type]) || [];
    if (!handlers.length) throw new Error(`${id} has no ${type} listener`);
    handlers.forEach((handler) => handler({ type, preventDefault() {} }));
  };
  const tick = (name, ...values) => (groups[name] || []).forEach((n) => { n.checked = values.includes(n.value); });
  return { store, groups, api, fire, tick };
}

const base = loadForm({});
const store = base.store;
const captured = base.api;

const failures = [];
const check = (label, condition, detail) => {
  if (!condition) failures.push(`${label}\n    ${detail}`);
};

const LISTS = { visited: "visited_places", wishlist: "wish_list", excluded: "excluded_places" };
function firstRow(field, value) {
  Object.keys(LISTS).forEach((i) => { store[i].value = ""; });
  store["profile-id"].value = "test-profile";
  store.consent.checked = true;
  store[field].value = value;
  return captured.buildProfile().travel_history[LISTS[field]][0];
}
function refused(field, value) {
  try { firstRow(field, value); return null; } catch (err) { return err.message; }
}

// 1. The gate on the form at all: a profile cannot be built without a name and consent. Consent
//    is not a formality here — it is the thing that makes writing the file legitimate.
const buildWith = (name, consented) => {
  Object.keys(LISTS).forEach((i) => { store[i].value = ""; });
  store["profile-id"].value = name;
  store.consent.checked = consented;
  try { captured.buildProfile(); return null; } catch (err) { return err.message; }
};
check("a profile with no name is refused", buildWith("", true) !== null,
      "the name is how the traveller picks this profile later");
check("a profile without consent is refused", buildWith("test-profile", false) !== null,
      "the consent box is what makes saving the file legitimate");
check("a named, consented profile builds", buildWith("test-profile", true) === null,
      "the happy path must work, or every case below is testing a refusal that always fires");

// 2. What a person actually writes must be understood. Each of these is a plausible answer from
//    somebody who read the label and wrote their own words, which is what labels are for.
for (const [written, expected] of [
  ["绝对不去", "never_recommend"],
  ["永不推荐", "never_recommend"],
  ["永远不去", "never_recommend"],
  ["暂时避开", "avoid_for_now"],
  ["这次不去", "avoid_for_now"],
  ["never_recommend", "never_recommend"],   // the old machine spelling still works
  ["avoid_for_now", "avoid_for_now"],
  ["NEVER", "never_recommend"],             // case-insensitive
]) {
  const row = firstRow("excluded", `某地 | 国家 | 理由 | ${written}`);
  check(`an exclusion written as "${written}" means ${expected}`,
        row.exclusion_strength === expected,
        `got ${row.exclusion_strength} — downstream compares this string exactly, so anything `
        + `else filters nothing`);
}

// An omitted strength defaults to the SAFE side. Getting this backwards would turn a blank into
// a place the skill happily recommends.
const blank = firstRow("excluded", "某地 | 国家 | 理由");
check("an exclusion with no strength defaults to never_recommend",
      blank.exclusion_strength === "never_recommend", JSON.stringify(blank));

for (const [written, expected] of [
  ["想", "yes"], ["不想", "no"], ["不再去", "no"], ["说不好", "maybe"],
  ["yes", "yes"], ["no", "no"], ["maybe", "maybe"],
]) {
  const row = firstRow("visited", `东京 | 城市 | 2024-04 | ${written} | note`);
  check(`a revisit answer of "${written}" means ${expected}`,
        row.revisit_interest === expected, `got ${row.revisit_interest}`);
}
const noRevisit = firstRow("visited", "东京 | 城市 | 2024-04");
check("an omitted revisit answer is unknown, not a silent no",
      noRevisit.revisit_interest === "unknown", JSON.stringify(noRevisit));

for (const [written, expected] of [["城市", "city_or_region"], ["国家", "country"],
                                   ["区域", "city_or_region"], ["country", "country"],
                                   ["city", "city_or_region"]]) {
  const row = firstRow("wishlist", `冰岛 | ${written} | 5 | why`);
  check(`a scope of "${written}" means ${expected}`, row.scope === expected, `got ${row.scope}`);
}

// 3. What cannot be understood must be REFUSED, by name, with the row number — never stored.
//    This is the half that did not exist: every one of these used to be accepted silently.
for (const [label, field, value, mustMention] of [
  ["a strength nobody can parse", "excluded", "某地 | 国家 | 理由 | 随便啦", "随便啦"],
  // "never recommend" used to be here as a typo of the enum; it is plain English for this column
  // and the English page teaches it, so it is now understood. This is a word nobody can map.
  ["an English word nobody can parse", "excluded", "某地 | 国家 | 理由 | sometimes", "sometimes"],
  ["a revisit answer nobody can parse", "visited", "东京 | 城市 | 2024-04 | 大概吧 | n", "大概吧"],
  ["a scope nobody can parse", "wishlist", "冰岛 | 星球 | 5 | why", "星球"],
  ["a priority written as a word", "wishlist", "冰岛 | 国家 | 高 | why", "高"],
  ["a priority above the stated range", "wishlist", "冰岛 | 国家 | 999 | why", "999"],
  ["a fractional priority", "wishlist", "冰岛 | 国家 | 3.7 | why", "3.7"],
  ["a negative priority", "wishlist", "冰岛 | 国家 | -2 | why", "-2"],
]) {
  const message = refused(field, value);
  check(`${label} is refused`, message !== null,
        "silently stored instead — the traveller's answer would mean nothing downstream");
  if (message) {
    check(`the refusal for ${label} quotes what was written`, message.includes(mustMention),
          `message was: ${message}`);
    check(`the refusal for ${label} names the row`, /第\s*\d+\s*行/.test(message),
          `a traveller with eight lines needs to know which one: ${message}`);
  }
}

// The row number must be the real one, or it sends the traveller to the wrong line.
const third = refused("excluded", "甲 | 国家 | 理由 | 永不推荐\n乙 | 国家 | 理由 | 暂时避开\n丙 | 国家 | 理由 | 看心情");
check("the refusal names the line the mistake is actually on",
      third !== null && third.includes("第 3 行"), `got: ${third}`);

// 4. Legitimate values must still pass, or the fix has made the form unusable. A rank of 1 and a
//    rank of 5 are both boundaries, and an empty one is a traveller who did not want to rank it.
for (const [label, value, expected] of [["1", "1", 1], ["5", "5", 5], ["empty", "", null]]) {
  const row = firstRow("wishlist", `冰岛 | 国家 | ${value} | why`);
  check(`a priority of ${label} is accepted`, row.priority === expected,
        `got ${JSON.stringify(row.priority)}`);
}

// 5. And the example button has to type what the form now documents. It is the one filled-in form
//    most people will ever see, so an example the form itself would refuse teaches the wrong
//    grammar — and this is exactly what happened: it still said `avoid_for_now` after the label
//    stopped mentioning it. The button is pressed, in both languages, and the page it leaves
//    behind must build; reading its literals out of the HTML stopped working once the example
//    came from the dictionary, and a check that finds nothing to check passes.
const CJK = /[　-〿㐀-鿿＀-￯]/;
for (const lang of ["zh", "en"]) {
  const f = loadForm({ language: lang });
  let built = null;
  try { f.fire("fill-example", "click"); built = f.api.buildProfile(); } catch (err) { built = err.message; }
  check(`${lang}: the example the button fills in is one this form accepts`, typeof built === "object",
        `the form refuses its own example: ${built}`);
  if (lang === "en") {
    const typed = ["nationality", "residence-country", "languages", "home-city", "home-country", "map-apps",
                   "booking-platforms", "services-to-avoid", "booking-access-notes", "service-notes",
                   "visited", "wishlist", "excluded", "cabin", "dietary", "accessibility", "avoid-list"];
    const chinese = typed.filter((id) => CJK.test(f.store[id].value));
    check("en: the example's typed answers are in English", !chinese.length, chinese.join(", "));
  }
}

// 6. One page, two languages, ONE profile. The same answers given to the Chinese page and to the
//    English one -- each list column written in the words that page's hint teaches -- must build
//    the same profile: it is read later by code that knows nothing about the page's language.
function fullProfile(lang) {
  const f = loadForm({ language: lang });
  const answers = {
    "profile-id": "same-traveller", "response-language": "English", "nationality": "China",
    "residence-country": "Netherlands", "residence-status": "member_state_residence_permit",
    "languages": "English, Chinese", "language-comfort": "可用翻译工具", "home-city": "Leiden",
    "home-country": "Netherlands", "airports": "AMS, RTM", "currency": "EUR", "map-apps": "Google Maps",
    "booking-platforms": "Booking.com", "google-access": "available", "direction": "balance",
    "pace": "适中", "lodging": "舒适中档", "location-priority": "景点步行范围", "self-drive": "可接受自驾",
    "cabin": "economy", "dietary": "vegetarian", "avoid-list": "red-eye flights",
  };
  for (const [id, value] of Object.entries(answers)) f.store[id].value = value;
  f.store.consent.checked = true;
  const lists = lang === "en"
    ? { visited: "Tokyo | city | 2024-04 | yes | food\nKyoto | city | 2019 | not sure | busy",
        wishlist: "Iceland | country | 5 | aurora",
        excluded: "Somewhere | country | crowds | avoid for now\nElsewhere | region | too hot | never" }
    : { visited: "Tokyo | 城市 | 2024-04 | 想 | food\nKyoto | 城市 | 2019 | 不确定 | busy",
        wishlist: "Iceland | 国家 | 5 | aurora",
        excluded: "Somewhere | 国家 | crowds | 暂时避开\nElsewhere | 区域 | too hot | 永不推荐" };
  for (const [id, value] of Object.entries(lists)) f.store[id].value = value;
  f.tick("natural", "雪景/极光");
  f.tick("cultural", "当地美食", "街区漫步");
  try { return { ok: true, profile: f.api.buildProfile() }; } catch (err) { return { ok: false, message: err.message }; }
}
{
  const zh = fullProfile("zh");
  const en = fullProfile("en");
  check("the Chinese page builds the full answer set", zh.ok, zh.message);
  check("the English page builds the full answer set", en.ok, en.message);
  if (zh.ok && en.ok) {
    check("both languages build the identical profile", JSON.stringify(zh.profile) === JSON.stringify(en.profile),
          `zh=${JSON.stringify(zh.profile.travel_history)}\n    en=${JSON.stringify(en.profile.travel_history)}`);
  }
}

// 7. Consent is required on the English page too. It is the sentence the traveller agrees to; a
//    translation that lost the requirement would save a profile nobody agreed to.
{
  const f = loadForm({ language: "en" });
  f.store["profile-id"].value = "someone";
  f.store.consent.checked = false;
  let message = null;
  try { f.api.buildProfile(); } catch (err) { message = err.message; }
  check("en: a profile without consent is refused", message !== null, "it was built without consent");
  if (message) check("en: that refusal is in English", !CJK.test(message), message);
}

// 8. Every refusal names the line, quotes what was written, reads in the page's language -- and
//    every word it suggests is one the form then accepts, so following the advice cannot fail.
const COLUMN = { excluded: 3, visited: 3, wishlist: 1 };
for (const lang of ["zh", "en"]) {
  const f = loadForm({ language: lang });
  const attempt = (field, value) => {
    for (const id of ["visited", "wishlist", "excluded"]) f.store[id].value = "";
    f.store["profile-id"].value = "someone";
    f.store.consent.checked = true;
    f.store[field].value = value;
    try { f.api.buildProfile(); return null; } catch (err) { return err.message; }
  };
  for (const [field, row, bad] of [["excluded", "X | country | r | whatever", "whatever"],
                                   ["visited", "T | city | 2024 | perhaps not", "perhaps not"],
                                   ["wishlist", "I | planet | 5 | w", "planet"],
                                   ["wishlist", "I | country | high | w", "high"]]) {
    const message = attempt(field, row);
    check(`${lang}: "${bad}" in ${field} is refused`, message !== null, "accepted");
    if (!message) continue;
    check(`${lang}: the refusal quotes "${bad}"`, message.includes(bad), message);
    check(`${lang}: the refusal names the line`, lang === "en" ? /Line 1\b/.test(message) : /第\s*1\s*行/.test(message), message);
    check(`${lang}: the refusal for "${bad}" is in the page's language`,
          lang === "en" ? !CJK.test(message.replace(bad, "")) : CJK.test(message), message);
    const advice = message.match(lang === "en" ? /You can write: (.*)\.\s*$/ : /可以写：(.*)。\s*$/);
    if (!advice) continue;
    const words = advice[1].split(lang === "en" ? ", " : "、");
    for (const word of words) {
      const parts = row.split(" | ");
      parts[COLUMN[field]] = word;
      check(`${lang}: the suggested "${word}" is accepted in ${field}`, attempt(field, parts.join(" | ")) === null,
            `the form suggests a word it then refuses: ${attempt(field, parts.join(" | "))}`);
    }
  }
}

// 9. The English words the English page teaches are understood (the tables are shared, so the
//    Chinese page accepts them too).
for (const [field, written, key, expected] of [
  ["excluded", "某地 | 国家 | 理由 | never", "exclusion_strength", "never_recommend"],
  ["excluded", "某地 | 国家 | 理由 | never recommend", "exclusion_strength", "never_recommend"],
  ["excluded", "某地 | 国家 | 理由 | avoid for now", "exclusion_strength", "avoid_for_now"],
  ["excluded", "某地 | 国家 | 理由 | Avoid  For Now", "exclusion_strength", "avoid_for_now"],
  ["visited", "东京 | city | 2024-04 | not sure | x", "revisit_interest", "unknown"],
  ["visited", "东京 | region | 2024-04 | maybe | x", "revisit_interest", "maybe"],
]) {
  let got;
  try { got = firstRow(field, written)[key]; } catch (err) { got = `refused: ${err.message.trim()}`; }
  check(`"${written.split(" | ")[3]}" in ${field} means ${expected}`, got === expected, `got ${got}`);
}

// 10. The switch works after load, both ways.
{
  const f = loadForm({ language: "zh" });
  check("the profile page exposes its language switch", !!f.api.applyLanguage);
  if (f.api.applyLanguage) {
    f.store["profile-id"].value = "";
    f.api.applyLanguage("en");
    let message = null;
    try { f.api.buildProfile(); } catch (err) { message = err.message; }
    check("after switching to English, a refusal is in English", message !== null && !CJK.test(message), message);
    f.api.applyLanguage("zh");
    try { f.api.buildProfile(); message = null; } catch (err) { message = err.message; }
    check("and after switching back, Chinese again", message !== null && CJK.test(message), message);
  }
}

// 11. A submission says which language its page was in when it was sent, after a switch too, so
//     the server answers a refusal in the language on screen.
async function languageHeaderCases() {
  for (const [lang, switchTo, expected] of [["zh", null, "zh"], ["en", null, "en"], ["zh", "en", "en"]]) {
    const sent = [];
    const f = loadForm({ language: lang, submit_url: "/submit?token=t" },
                       { fetch: async (url, init) => { sent.push(init); return { ok: true, json: async () => ({}) }; } });
    f.store["profile-id"].value = "someone";
    f.store.consent.checked = true;
    if (switchTo && f.api.applyLanguage) f.api.applyLanguage(switchTo);
    for (const handler of f.store["profile-form"].listeners.submit || []) {
      await handler({ type: "submit", preventDefault() {} });
    }
    const header = sent.length ? (sent[0].headers || {})["X-Travel-Buddy-Language"] : undefined;
    check(`a ${lang} profile page${switchTo ? ` switched to ${switchTo}` : ""} submits with language ${expected}`,
          header === expected, `sent: ${JSON.stringify(sent.map((init) => init.headers))}`);
  }
}

languageHeaderCases().then(() => {
  if (failures.length) {
    console.error(`PROFILE FORM FAILED (${failures.length}):`);
    failures.forEach((f) => console.error(`--- ${f}\n`));
    process.exit(1);
  }
  console.log("all profile-form cases passed");
});
