// Behavioural tests for assets/trip-intake-form.html, run against the form's own JavaScript.
//
// Until today nothing tested this file, and it is the one place every answer the traveller gives
// enters the pipeline: fifty-odd fields, several conditional branches, and a build() that both
// validates and assembles the intake JSON. Two defects fixed on 2026-08-30 were the same shape --
// a field the form collected but did not require, so it came back `null` and the assistant asked
// the question in chat instead. A null and an answer of "nothing" are indistinguishable
// downstream, which is why these need executing rather than reading.
//
// The third defect was found BY this shim while it was being written, and was mine: the
// booked-already toggle had been added outside the form's own IIFE, where `$` does not exist, so
// the detail box could never have appeared. Every gate in the repo was green.
"use strict";
const path = require("path");
const load = require("./form_shim.js");

const FORM = path.join(__dirname, "..", "assets", "trip-intake-form.html");
const failures = [];
const check = (label, cond, detail) => { if (!cond) failures.push(label + (detail ? `: ${detail}` : "")); };

// A minimally valid submission. Each test starts from this and breaks exactly one thing, so a
// refusal can only be about the thing that was broken.
function fresh(config, options) {
  const f = load(FORM, config, options);
  check("the form's own JS runs without error", !f.topLevelError, f.topLevelError);
  check("build() is reachable", !!f.build);
  const base = {
    "city": "阿姆斯特丹", "country": "荷兰", "count": "2", "currency": "EUR",
    "coverage": "transport_and_stay", "travel-time": "不超过 15 小时", "scope": "open",
    "direction": "balance", "month": "2027-04", "days": "6",
    "budget-range": "300|500", "travel-scope": "no_new_visa_needed", "held-passport-validity": "valid_through_trip",
    "held-visas": "申根居留卡 + 香港免签", "booked-already": "nothing", "trip-shape": "single_base",
  };
  for (const [id, v] of Object.entries(base)) { if (f.store[id]) f.set(id, v); }
  f.tick("transport-mode", "direct_flight", "high_speed_rail");
  return f;
}

function submits(f) {
  try { return { ok: true, payload: f.build() }; }
  catch (err) { return { ok: false, message: String(err && err.message || err) }; }
}

// 0. The baseline must go through, or every refusal below proves nothing.
{
  const f = fresh();
  const r = submits(f);
  check("a complete submission is accepted", r.ok, r.message);
}

// 1. FIXED 2026-08-30. SKILL.md says the no_new_visa_needed branch collects TWO things -- what the
//    traveller enters ON, and passport validity -- and only the second was required, so
//    held_entry_documents came back null on a real run and an asserted "no visa needed" became a
//    trip-blocking finding that cost a question about a box the form already had.
{
  const f = fresh();
  f.set("held-visas", "");
  const r = submits(f);
  check("a held-visa branch with no documents named is refused", !r.ok,
        "it was accepted, and held_entry_documents would be null");
  if (!r.ok) check("the refusal names the missing field", /入境|证件/.test(r.message), r.message);
}

// 2. FIXED 2026-08-30. research-budget.md rule 1 names three disqualifiers worth asking before any
//    research at all. The form collected entry and date flexibility and not "have you booked
//    anything yet", so it was asked in chat -- the exact round trip the rule exists to prevent.
{
  const f = fresh();
  f.set("booked-already", "");
  const r = submits(f);
  check("a submission that will not say what is booked is refused", !r.ok,
        "accepted; the question moves to chat");
}

// 3. It asks WHAT is booked, not whether. A yes/no would only have pushed the follow-up one step
//    later, since "flights booked" and "hotel booked" delete different branches.
{
  const f = fresh();
  f.set("booked-already", "both");
  let r = submits(f);
  check("saying something is booked without saying what is refused", !r.ok, "accepted");
  f.set("booked-detail", "CX270 4/17 不可退；尖沙咀酒店 4/17-4/23 可免费取消");
  r = submits(f);
  check("naming what is booked goes through", r.ok, r.message);
  if (r.ok) {
    check("the payload carries the booking state",
          r.payload.existing_bookings && r.payload.existing_bookings.state === "both",
          JSON.stringify(r.payload.existing_bookings));
    check("the payload carries the booking detail",
          /CX270/.test((r.payload.existing_bookings || {}).details || ""),
          JSON.stringify(r.payload.existing_bookings));
  }
}

// 3b. Trip shape. "One country" is equally true of one base and of five stops, so the shape
//     cannot be derived from the destination scope and is asked once, on the form, rather than
//     discovered halfway through design. Both bounds are required for the two failure modes this
//     shape has: no maximum turns "you decide" into an unbounded plan, and no minimum is how a
//     multi-city trip becomes a different hotel every night.
{
  const f = fresh();
  f.set("trip-shape", "");
  check("a submission that will not say the trip's shape is refused", !submits(f).ok, "accepted");
}
{
  const f = fresh();
  f.set("trip-shape", "multi_city");
  // Each bound is dropped ALONE, with the other two filled. Blanking all three also gets refused
  // -- by whichever one is still required -- so a test written that way passes while any single
  // rule is deleted. That is the same "the filter is wider than its subject" mistake this suite
  // caught once already; here it let two mutations through before the cases were split.
  const bounds = { "max-stops": "3", "min-nights-per-stop": "2", "return-to-first": "yes" };
  for (const dropped of Object.keys(bounds)) {
    for (const [id, v] of Object.entries(bounds)) f.set(id, id === dropped ? "" : v);
    check(`multi-city without ${dropped} alone is refused`, !submits(f).ok,
          "accepted, so that bound is not actually required");
  }
  for (const [id, v] of Object.entries(bounds)) f.set(id, v);
  let r = submits(f);
  check("multi-city with its bounds goes through", r.ok, r.message);
  if (r.ok) {
    const shape = (r.payload.destination_scope || {}).trip_shape || {};
    check("the payload carries the shape", shape.state === "multi_city", JSON.stringify(shape));
    check("max_stops is a number, not a string", shape.max_stops === 3, JSON.stringify(shape));
    check("min_nights_per_stop is a number", shape.min_nights_per_stop === 2, JSON.stringify(shape));
    check("the return question is carried", shape.return_to_first_stop === "yes", JSON.stringify(shape));
  }
}
{
  // A single stop is not a multi-city trip, and a non-numeric bound must not reach the JSON as
  // NaN: it would look like an answer while being one nothing downstream can act on.
  const f = fresh();
  f.set("trip-shape", "planner_decides");
  f.set("min-nights-per-stop", "2"); f.set("return-to-first", "either");
  f.set("max-stops", "1");
  check("a maximum of one stop is refused", !submits(f).ok, "accepted");
  f.set("max-stops", "两");
  const r = submits(f);
  check("a non-numeric stop count is refused", !r.ok, "accepted");
  if (!r.ok) check("and refused without NaN reaching the payload", !/NaN/.test(r.message), r.message);
}
{
  const f = fresh();
  f.api.updateConditionalPanels();
  check("the multi-stop bounds hide for a single base", f.store["multi-stop-wrap"].hidden === true);
  for (const shape of ["multi_city", "planner_decides"]) {
    f.set("trip-shape", shape);
    f.api.updateConditionalPanels();
    check(`the bounds appear for ${shape}`, f.store["multi-stop-wrap"].hidden === false,
          "the toggle never ran");
  }
}

// 4. THE BUG THIS SHIM FOUND, and the reason a structural test would not have been enough: the
//    toggle was syntactically perfect and in the wrong scope. Asserting the panel actually moves
//    is what catches a listener that never runs.
{
  const f = fresh();
  f.api.updateConditionalPanels();
  check("the detail box is hidden while nothing is booked", f.store["booked-detail-wrap"].hidden === true);
  f.set("booked-already", "transport");
  f.api.updateConditionalPanels();
  check("the detail box appears once something is booked",
        f.store["booked-detail-wrap"].hidden === false,
        "the toggle never ran -- check it is inside the form's own IIFE");
  f.set("booked-already", "nothing");
  f.api.updateConditionalPanels();
  check("and hides again", f.store["booked-detail-wrap"].hidden === true);
}

// 4b. Every follow-up panel opens from its OWN question's change event -- the path a traveller
//     takes -- not from a direct call to updateConditionalPanels(). The multi-stop bounds had no
//     listener at all: choosing "several stops" revealed nothing, which went unseen only because a
//     CSS rule was also showing every hidden panel. Fixing the CSS alone would have hidden two
//     REQUIRED fields behind a question that could never open them.
{
  const panels = [
    ["booked-already", "transport", "nothing", ["booked-detail-wrap"]],
    ["trip-shape", "multi_city", "single_base", ["multi-stop-wrap"]],
    ["trip-shape", "planner_decides", "single_base", ["multi-stop-wrap"]],
    ["currency", "OTHER", "EUR", ["custom-currency-wrap"]],
    ["budget-range", "custom", "300|500", ["custom-budget-wrap"]],
    ["travel-scope", "no_new_visa_needed", "any_including_visa", ["held-visa-wrap", "held-passport-wrap"]],
    ["travel-scope", "any_including_visa", "no_new_visa_needed", ["visa-effort-wrap", "entry-requirements"]],
  ];
  // A question nothing listens to is recorded as a failure, not thrown: one missing listener must
  // not stop the other panels from being checked.
  const change = (f, id) => { try { f.fire(id, "change"); return ""; } catch (err) { return err.message; } };
  for (const [question, opens, closes, wraps] of panels) {
    const f = fresh();
    f.set(question, closes);
    let missing = change(f, question);
    for (const wrap of wraps) {
      check(`${wrap} is hidden while ${question} = ${closes}`, !missing && f.store[wrap].hidden === true, missing);
    }
    f.set(question, opens);
    missing = change(f, question);
    for (const wrap of wraps) {
      check(`answering ${question} = ${opens} opens ${wrap}`, !missing && f.store[wrap].hidden === false,
            missing || `nothing listening to ${question} reveals it`);
    }
  }
}

// 5. The same branch pair for entry, which is where the first defect lived. Both wraps move
//    together, so a fix to one that misses the other is caught.
{
  const f = fresh();
  f.set("travel-scope", "any_including_visa");
  f.api.updateConditionalPanels();
  check("held-visa wrap hides off-branch", f.store["held-visa-wrap"].hidden === true);
  check("held-passport wrap hides off-branch", f.store["held-passport-wrap"].hidden === true);
  f.set("travel-scope", "no_new_visa_needed");
  f.api.updateConditionalPanels();
  check("held-visa wrap shows on-branch", f.store["held-visa-wrap"].hidden === false);
  check("held-passport wrap shows on-branch", f.store["held-passport-wrap"].hidden === false);
}

// 6. A field the JS reads but the HTML no longer has returns null from getElementById, and the
//    form dies on the traveller's screen with no gate having said anything. Checked by reading
//    the ids the JS asks for and confirming each is really in the markup.
{
  const f = load(FORM);
  const fs = require("fs");
  const html = fs.readFileSync(FORM, "utf8");
  const js = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join("\n");
  const asked = new Set();
  for (const m of js.matchAll(/(?:\$|text|list)\("([a-z0-9-]+)"\)/g)) asked.add(m[1]);
  const missing = [...asked].filter((id) => !f.store[id]);
  check("every field the JS reads exists in the markup", missing.length === 0, missing.join(", "));
}

// 7. Every id in the draft-restore list is a real field. One missing from the list silently loses
//    what the traveller typed on a refresh; one that no longer exists throws mid-restore.
{
  const f = load(FORM);
  const fs = require("fs");
  const html = fs.readFileSync(FORM, "utf8");
  const m = html.match(/const FIELD_IDS = \[([^\]]+)\]/);
  check("the draft field list is findable", !!m);
  if (m) {
    const listed = m[1].split(",").map((s) => s.trim().replace(/^"|"$/g, ""));
    const gone = listed.filter((id) => !f.store[id] && !/^rank-/.test(id));
    check("every drafted field exists", gone.length === 0, gone.join(", "));
    for (const id of ["booked-already", "booked-detail", "held-visas",
                      "trip-shape", "max-stops", "min-nights-per-stop", "return-to-first"]) {
      check(`${id} survives a refresh`, listed.includes(id),
            "it is not in FIELD_IDS, so a reload loses it");
    }
  }
}

// 8. The three disqualifiers research-budget.md rule 1 says to ask BEFORE any research each have a
//    box. This is the generalisable form of both defects: the rule names the questions that delete
//    whole branches, and any one of them without a field gets asked in chat instead.
{
  const f = load(FORM);
  for (const [what, ids] of [["entry permission", ["travel-scope", "held-visas"]],
                             ["date flexibility", ["flexibility"]],
                             ["existing bookings", ["booked-already", "booked-detail"]]]) {
    for (const id of ids) {
      check(`rule 1 disqualifier "${what}" has a field (${id})`, !!f.store[id]);
    }
  }
}

// 9. One page, two languages, ONE intake. The form now speaks English as well as Chinese, and the
//    promise that makes that safe is that only the words on screen change: every value the intake
//    stores is identical, so nothing downstream has to know which language the traveller read.
//    The same answers go in both ways -- with the status words typed the way each hint teaches --
//    and the two payloads must be the same object.
const CJK = /[　-〿㐀-鿿＀-￯]/;
function everyAnswer(lang) {
  const f = fresh({ language: lang });
  const answers = {
    "start-date": "2027-04-10", "end-date": "2027-04-15", "month": "", "days": "",
    "flexibility": "± 1–2 天", "composition": "情侣/两人", "comfort": "舒适中档",
    "travel-time": "不超过 10 小时", "pace": "适中", "intensity": "短距离步行",
    "stay-location": "邻近地铁/车站", "breakfast": "最好含早", "cancellation": "优先可取消",
    "rail-preference": "高铁/动车优先", "bus-comfort": "仅短途接驳（约 3 小时内）",
    "cabin": "经济舱优先", "baggage": "每人 1 件托运行李", "flight-time": "优先白天起降",
    "purpose": "sightseeing", "transport-priority": "fewest_transfers", "room-count": "1",
    "travel-scope": "any_including_visa", "visa-tolerance": "evisa_acceptable",
    "passport-validity": "valid_through_trip", "scope": "anchored", "places": "Japan, Korea",
    "rank-1": "美食/市场", "rank-2": "山地/徒步", "google-services-access": "available",
  };
  for (const [id, v] of Object.entries(answers)) f.set(id, v);
  const status = lang === "en" ? ["EU residence permit", "EU citizen"] : ["成员国居留卡", "欧盟公民"];
  f.set("traveler-entry", `Traveller 1 | China | Netherlands | ${status[0]}\nTraveller 2 | Netherlands | Netherlands | ${status[1]}`);
  f.tick("natural", "山地/徒步");
  f.tick("cultural", "美食/市场", "街区漫步");
  f.tick("climate", "偏暖");
  f.tick("transport-mode", "direct_flight", "connecting_flight", "high_speed_rail");
  return submits(f);
}
{
  const zh = everyAnswer("zh");
  const en = everyAnswer("en");
  check("the Chinese form accepts the full answer set", zh.ok, zh.message);
  check("the English form accepts the full answer set", en.ok, en.message);
  if (zh.ok && en.ok) {
    check("both languages submit the identical intake",
          JSON.stringify(zh.payload) === JSON.stringify(en.payload),
          `zh=${JSON.stringify(zh.payload.feasibility)}\n    en=${JSON.stringify(en.payload.feasibility)}`);
    const rows = en.payload.feasibility.traveler_entry_profiles;
    check("an English status word is stored as the word the intake has always stored",
          rows[0].residence_status === "成员国居留卡" && rows[1].residence_status === "欧盟公民",
          JSON.stringify(rows));
  }
}
{
  // Only exact translations of the hint's categories are mapped. A bare "residence permit" can be
  // any country's -- a US green card holder writes exactly that -- so filing it under the EU
  // member-state category would hand the planner a visa-free route that does not exist.
  const f = fresh({ language: "en" });
  f.set("travel-scope", "any_including_visa");
  f.set("passport-validity", "valid_through_trip");
  f.set("traveler-entry", "A | China | United States | Residence permit\nB | China | Canada | PR card");
  const r = submits(f);
  check("an unrecognised status is accepted", r.ok, r.message);
  if (r.ok) {
    const rows = r.payload.feasibility.traveler_entry_profiles;
    check("a bare 'residence permit' is kept as typed, not filed as an EU permit",
          rows[0].residence_status === "Residence permit", JSON.stringify(rows[0]));
    check("free text the hint does not list is kept as typed",
          rows[1].residence_status === "PR card", JSON.stringify(rows[1]));
  }
}

// 10. Every refusal an English traveller can meet is in English. A form that translates its labels
//     and then explains a rejected submission in Chinese has failed the person at the moment they
//     most need to understand it -- so each refusal path is driven, not one.
{
  const refusals = [
    ["a missing required field", (f) => f.set("city", "")],
    ["a missing held-entry answer", (f) => f.set("held-visas", "")],
    ["a non-numeric traveller count", (f) => f.set("count", "0")],
    ["an invalid custom currency", (f) => { f.set("currency", "OTHER"); f.set("custom-currency", "12"); }],
    ["dates out of order", (f) => { f.set("start-date", "2027-04-10"); f.set("end-date", "2027-04-01"); }],
    ["a date with no pair", (f) => f.set("start-date", "2027-04-10")],
    ["days that contradict the dates", (f) => { f.set("start-date", "2027-04-10"); f.set("end-date", "2027-04-12"); f.set("days", "9"); }],
    ["no dates and no month", (f) => f.set("month", "")],
    ["no transport mode", (f) => f.tick("transport-mode")],
    ["a climate contradiction", (f) => f.tick("climate", "无特别气候限制", "偏暖")],
    ["a settled scope with no place", (f) => f.set("scope", "fixed")],
    ["a one-stop multi-city trip", (f) => { f.set("trip-shape", "multi_city"); f.set("max-stops", "1"); f.set("min-nights-per-stop", "2"); f.set("return-to-first", "yes"); }],
    ["a bad room count", (f) => f.set("room-count", "0")],
    ["a missing entry panel", (f) => { f.set("travel-scope", "any_including_visa"); f.set("passport-validity", "valid_through_trip"); }],
    ["a malformed entry row", (f) => { f.set("travel-scope", "any_including_visa"); f.set("passport-validity", "valid_through_trip"); f.set("traveler-entry", "only one part\nx | y | z"); }],
    ["too few entry rows", (f) => { f.set("travel-scope", "any_including_visa"); f.set("passport-validity", "valid_through_trip"); f.set("traveler-entry", "A | China | Netherlands"); }],
  ];
  for (const [what, breakIt] of refusals) {
    for (const lang of ["zh", "en"]) {
      const f = fresh({ language: lang });
      breakIt(f);
      const r = submits(f);
      check(`${lang}: ${what} is refused`, !r.ok, "accepted");
      if (!r.ok && lang === "en") check(`en: the refusal for ${what} is in English`, !CJK.test(r.message), r.message);
      if (!r.ok && lang === "zh") check(`zh: the refusal for ${what} is still in Chinese`, CJK.test(r.message), r.message);
    }
  }
}

// 11. The example button fills in a trip that can actually be submitted, in either language. It
//     set a travel scope the page had stopped offering, so a real browser left the question blank
//     and the example was refused for a missing answer -- the stub kept the string, so nothing saw it.
for (const lang of ["zh", "en"]) {
  const f = load(FORM, { language: lang });
  f.fire("fill-example", "click");
  const r = submits(f);
  check(`${lang}: the filled-in example can be submitted`, r.ok, r.message);
  if (lang === "en") {
    const typed = ["city", "country", "dietary", "avoid", "held-visas", "preferred-map-apps",
                   "preferred-booking-platforms", "services-to-avoid", "service-access-notes"];
    const chinese = typed.filter((id) => CJK.test(f.get(id)));
    check("en: the example's typed answers are in English", !chinese.length, chinese.join(", "));
  }
}

// 12. The switch works after load, both ways: the same half-filled page explains itself in the
//     language just chosen.
{
  const f = fresh({ language: "zh" });
  check("the page exposes its language switch", !!(f.api && f.api.applyLanguage));
  if (f.api && f.api.applyLanguage) {
    f.set("city", "");
    f.api.applyLanguage("en");
    let r = submits(f);
    check("after switching to English, a refusal is in English", !r.ok && !CJK.test(r.message), r.message);
    f.api.applyLanguage("zh");
    r = submits(f);
    check("and after switching back, it is Chinese again", !r.ok && CJK.test(r.message), r.message);
  }
}

// 14. The saved-profile note quotes the profile's self-drive answer in the page's language. The
//     profile stores the Chinese option VALUE (stored values never change with the language), and
//     the note printed it raw -- "Self-drive preference: 可接受自驾" on an English page, seen in the
//     real-browser run and missed by every check here, because none loaded a profile in English.
{
  const note = (lang, value) => load(FORM, { language: lang, profile_defaults: { profile_id: "p", self_drive_preference: value } })
    .store["saved-profile-note"].textContent;
  const en = note("en", "可接受自驾");
  check("en: the profile note names the self-drive answer in English",
        /Driving is fine/.test(en) && !CJK.test(en), en);
  const zh = note("zh", "可接受自驾");
  check("zh: the profile note still quotes it the way it always did", zh.includes("自驾偏好：可接受自驾"), zh);
  // Every answer the profile form can store has a label here, so an option added there is noticed
  // here instead of printing raw.
  const profileHtml = require("fs").readFileSync(path.join(__dirname, "..", "assets", "traveler-profile-intake.html"), "utf8");
  const select = (profileHtml.match(/<select id="self-drive">([\s\S]*?)<\/select>/) || ["", ""])[1];
  const offered = [...select.matchAll(/value="([^"]+)"/g)].map((m) => m[1]);
  check("the profile form's self-drive options are readable here", offered.length >= 4, JSON.stringify(offered));
  for (const value of offered) {
    const text = note("en", value);
    check(`en: the self-drive answer ${value} is named in English`, !CJK.test(text), text);
  }
  // A value no form offers (a hand-edited profile) is still shown as written rather than dropped.
  check("an unknown self-drive answer is shown as written", note("en", "Only on weekends").includes("Only on weekends"),
        note("en", "Only on weekends"));
}

// 13. A submission says which language its page was in when it was sent -- after a switch, too --
//     so the server answers in that language and the intake records the language actually used.
//     Driven through the page's own submit handler with the network replaced, which is the only
//     way to see what a browser would send.
async function languageHeaderCases() {
  for (const [lang, switchTo, expected] of [["zh", null, "zh"], ["en", null, "en"], ["zh", "en", "en"], ["en", "zh", "zh"]]) {
    const sent = [];
    const f = fresh({ language: lang, submit_url: "/submit?token=t" },
                    { fetch: async (url, init) => { sent.push(init); return { ok: true, json: async () => ({}) }; } });
    if (switchTo && f.api.applyLanguage) f.api.applyLanguage(switchTo);
    for (const handler of f.store["trip-form"].listeners.submit || []) {
      await handler({ type: "submit", preventDefault() {} });
    }
    const header = sent.length ? (sent[0].headers || {})["X-Travel-Buddy-Language"] : undefined;
    check(`a ${lang} page${switchTo ? ` switched to ${switchTo}` : ""} submits with language ${expected}`,
          header === expected, `sent: ${JSON.stringify(sent.map((init) => init.headers))}`);
  }
}

languageHeaderCases().then(() => {
  if (failures.length) {
    console.error(`INTAKE FORM FAILED (${failures.length}):`);
    for (const failure of failures) console.error(`--- ${failure}\n`);
    process.exit(1);
  }
  console.log("all intake-form cases passed");
});
