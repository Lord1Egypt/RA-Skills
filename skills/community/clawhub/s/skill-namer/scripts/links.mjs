#!/usr/bin/env node
// Skill Namer: links.mjs
// Prints search links for a shortlist: ICANN Lookup before registrars for ICANN domains, the name systems for
// .eth and the rest, trademark offices, and the surfaces that aren't domains. Node built-ins only.
// This script never touches the network, never submits anything, and never reports availability. Only a person
// clicking a link, or a named live tool, can report that. It is a link printer, not a check.
//
// Usage:
//   node scripts/links.mjs --names workcrew,payrail --tlds eth,ai,com,dao
//   node scripts/links.mjs --names workcrew --providers all --surfaces all
//   node scripts/links.mjs --names 仲間 --tlds com,jp
//   node scripts/links.mjs --names workcrew --json
import { parseArgs } from "node:util";
import { domainToASCII } from "node:url";

let lib;
try {
  lib = await import("./lib.mjs");
} catch {
  console.log("scripts/lib.mjs is missing beside this file. No links were printed; use the links in references/availability.md by hand.");
  process.exit(1);
}
const { CONTROL_RE, HIDDEN_RE, ALLOWED_RE, fold, hadTurkishDot, hadTurkishCapital, revealHidden, hiddenPoints, joinersAllowed, disallowedPoints,
  scriptsOf, mixAllowed, mixReason, nearKnownName, wholeScriptLookalike, latinOutsideAZ, TATWEEL, skeleton, NOT_DETECTED } = lib;
const JOINERS_RE = new RegExp("[" + String.fromCodePoint(0x200C) + String.fromCodePoint(0x200D) + "]", "gu");

const USAGE = `links.mjs: search links for a shortlist. Touches no network, submits nothing, reports no availability.
  --names workcrew,payrail   the shortlist only; five or fewer is kinder to everyone
  --tlds eth,ai,com,dao      endings to print links for (eth, base, dao, sol, hns, and any ICANN ending)
  --providers top | all      the first three registrars (default), or all listed
  --surfaces all             or a list: clawhub,github,npm,pypi,bsky,hf,fediverse,appstores
  --json                     print one JSON object instead of text; agents should parse this, never the text
  --help                     this text
When the person has said they are under the age of majority, do not run this: candidates only; every registration, wallet, trademark-office, and account-creation link stays unprinted.
Exit code 2 means at least one name or ending was stopped and got no links.`;

const wantsJson = process.argv.some((a) => a === "--json" || a.startsWith("--json="));
function fail(message, code = 1) {
  if (wantsJson) console.log(JSON.stringify({ script: "links.mjs", error: message }, null, 2));
  else console.log(message);
  process.exit(code);
}

let values;
try {
  ({ values } = parseArgs({
    options: {
      names: { type: "string" },
      tlds: { type: "string", default: "eth,ai,com,dao" },
      providers: { type: "string", default: "top" },
      surfaces: { type: "string", default: "" },
      json: { type: "boolean", default: false },
      help: { type: "boolean", default: false },
    },
  }));
} catch (err) {
  fail(err.message + "\n" + USAGE);
}
if (values.help) {
  console.log(USAGE);
  process.exit(0);
}
if (!values.names) fail(USAGE);
if (!["top", "all"].includes(values.providers)) fail("--providers takes top or all.");

const rawNames = values.names.split(",").map((n) => n.trim()).filter(Boolean);
if (!rawNames.length) fail("--names needs at least one name.");
const names = [...new Set(rawNames.map(fold))];
const turkish = rawNames.some((n) => hadTurkishDot(n) || hadTurkishCapital(n));

// Endings are screened like names: one or two labels of letters (co.uk is one ending), 2 to 63 characters each, nothing
// hidden, one script, not a lookalike of a Latin ending, not a listed name. A lookalike ending could otherwise pose as
// this script's output or carry a lookalike.
const rawTlds = values.tlds.split(",").map((t) => t.trim()).filter(Boolean);
if (!rawTlds.length) fail("--tlds needs at least one ending, or leave it off for the default.");
const tlds = [];
const stoppedEndings = [];
let stopped = 0;
function endingReason(t) {
  if (!/^\p{L}[\p{L}\p{M}]{0,62}(\.\p{L}[\p{L}\p{M}]{1,62})?$/u.test(t) || HIDDEN_RE.test(t)) return "not letters only (one or two labels, 2 to 63 letters), or carries hidden characters";
  if (t.length === 1 && !NAME_SYSTEMS[t]) return "a one-letter ending this file does not know";
  for (const label of t.split(".")) {
    const known = KNOWN_GTLDS.has(label) || Boolean(CC[label]) || Boolean(NAME_SYSTEMS[label]);
    const sc = scriptsOf(label);
    if (sc.length !== 1) return "mixes scripts; an ending is written in one script";
    if (!known && wholeScriptLookalike(label)) return "every letter has a Latin lookalike; a lookalike ending";
    if (!known && nearKnownName(label)) return "a well-known name, or a lookalike of one, used as an ending";
  }
  return null;
}
function screenEndings() {
  for (const raw of rawTlds) {
    const t = fold(raw).replace(/^\./, "");
    const why = endingReason(t);
    if (why) {
      stoppedEndings.push({ ending: raw, reason: why });
      stopped += 1;
      continue;
    }
    if (!tlds.includes(t)) tlds.push(t);
  }
}
const enc = encodeURIComponent;

// Everything below is as understood at the time of this version's authorship (October 2026).
// Deep links are best effort; the base link is always printed beside them.
const ICANN_LOOKUP = { name: "ICANN Lookup (RDAP registration data, neutral, sells nothing)", base: "https://lookup.icann.org/", deep: (d) => `https://lookup.icann.org/en/lookup?name=${enc(d)}` };
const ICANN_LOOKUP_NOTE = "      covers endings under ICANN contract and country codes that publish RDAP; no record means no information unless the ending is covered, and even then a hint, not availability";

const NAME_SYSTEMS = {
  eth: { label: (n) => `${n}.eth`, name: "ENS", base: "https://app.ens.domains/", deep: (n) => `https://app.ens.domains/${enc(n)}.eth`, note: "must survive ENS normalization (ENSIP-15): https://docs.ens.domains/resolution/names. ENS itself allows some emoji; this skill's preset is letters only" },
  base: { label: (n) => `${n}.base.eth`, name: "Basenames (subnames under base.eth, managed by Base)", base: "https://base.org/names", deep: null, note: "" },
  dao: { label: (n) => `${n}.dao`, name: "Unstoppable Domains", base: "https://unstoppabledomains.com/search", deep: (n) => `https://unstoppabledomains.com/search?searchTerm=${enc(n)}`, note: "" },
  crypto: { label: (n) => `${n}.crypto`, name: "Unstoppable Domains", base: "https://unstoppabledomains.com/search", deep: (n) => `https://unstoppabledomains.com/search?searchTerm=${enc(n)}`, note: "" },
  nft: { label: (n) => `${n}.nft`, name: "Unstoppable Domains", base: "https://unstoppabledomains.com/search", deep: (n) => `https://unstoppabledomains.com/search?searchTerm=${enc(n)}`, note: "" },
  wallet: { label: (n) => `${n}.wallet`, name: "Unstoppable Domains", base: "https://unstoppabledomains.com/search", deep: (n) => `https://unstoppabledomains.com/search?searchTerm=${enc(n)}`, note: "" },
  blockchain: { label: (n) => `${n}.blockchain`, name: "Unstoppable Domains", base: "https://unstoppabledomains.com/search", deep: (n) => `https://unstoppabledomains.com/search?searchTerm=${enc(n)}`, note: "" },
  x: { label: (n) => `${n}.x`, name: "Unstoppable Domains", base: "https://unstoppabledomains.com/search", deep: (n) => `https://unstoppabledomains.com/search?searchTerm=${enc(n)}`, note: "" },
  unstoppable: { label: (n) => `${n}.unstoppable`, name: "Unstoppable Domains", base: "https://unstoppabledomains.com/search", deep: (n) => `https://unstoppabledomains.com/search?searchTerm=${enc(n)}`, note: "" },
  sol: { label: (n) => `${n}.sol`, name: "Solana Name Service (formerly Bonfida)", base: "https://www.sns.id/", deep: null, note: "" },
  hns: { label: (n) => `${n} (Handshake)`, name: "Namebase (Handshake marketplace; ownership changed in early 2026)", base: "https://namebase.io/", deep: null, note: "Handshake names resolve only with special browsers or plugins" },
};

const ICANN = [
  { name: "GoDaddy", base: "https://www.godaddy.com/domainsearch/find", deep: (d) => `https://www.godaddy.com/domainsearch/find?domainToCheck=${enc(d)}` },
  { name: "Namecheap", base: "https://www.namecheap.com/domains/registration/", deep: (d) => `https://www.namecheap.com/domains/registration/results/?domain=${enc(d)}` },
  { name: "Cloudflare Registrar", base: "https://www.cloudflare.com/products/registrar/", deep: null },
  { name: "Porkbun", base: "https://porkbun.com/", deep: (d) => `https://porkbun.com/checkout/search?q=${enc(d)}` },
  { name: "Dynadot", base: "https://www.dynadot.com/domain/search", deep: (d) => `https://www.dynadot.com/domain/search?domain=${enc(d)}` },
  { name: "Hover", base: "https://www.hover.com/domains", deep: null },
  { name: "Gandi", base: "https://www.gandi.net/en/domain", deep: null },
  { name: "Squarespace Domains", base: "https://domains.squarespace.com/", deep: null },
];

const TRADEMARK = [
  { name: "USPTO (US)", base: "https://tmsearch.uspto.gov/" },
  { name: "EUIPO (EU)", base: "https://euipo.europa.eu/eSearch/" },
  { name: "WIPO Global Brand Database (Madrid records plus many national collections)", base: "https://branddb.wipo.int/" },
  { name: "TMview (free search across the EU and many national offices)", base: "https://www.tmdn.org/tmview/" },
];

// Country-code endings this file knows, and the place each code belongs to. Who runs the registry is a separate
// question. Presence notes only where known; many other endings have them too. Source of truth:
// https://www.iana.org/domains/root/db
const CC = {
  ai: "Anguilla", io: "the British Indian Ocean Territory (the Chagos Islands)", tv: "Tuvalu", co: "Colombia", me: "Montenegro",
  ly: "Libya", fm: "the Federated States of Micronesia", gg: "Guernsey", sh: "Saint Helena, Ascension and Tristan da Cunha",
  to: "Tonga", ws: "Samoa", nu: "Niue", cc: "the Cocos (Keeling) Islands", tk: "Tokelau", is: "Iceland",
  it: "Italy (limited to EU or EEA citizens or residents, plus a few others)", am: "Armenia", im: "the Isle of Man",
  st: "São Tomé and Príncipe", so: "Somalia", vc: "Saint Vincent and the Grenadines", la: "Laos", ms: "Montserrat",
  ac: "Ascension Island", ag: "Antigua and Barbuda", at: "Austria", be: "Belgium", es: "Spain", in: "India",
  no: "Norway (a Norwegian organization number or national ID is required)", pm: "Saint Pierre and Miquelon", re: "Réunion",
  tm: "Turkmenistan", tc: "the Turks and Caicos Islands", mx: "Mexico",
  de: "Germany (an address for service in Germany is required for holders abroad)", jp: "Japan (general-use names require a Japanese address)",
  us: "the United States (a US presence, the Nexus requirement; privacy services not allowed)", uk: "the United Kingdom",
  ca: "Canada (Canadian presence required)", au: "Australia (Australian presence required)",
  eu: "the European Union (residence or establishment in the EU or EEA, or EU citizenship, required)",
  kr: "South Korea", tr: "Türkiye", ir: "Iran", ru: "Russia", gr: "Greece", cn: "China (real-name verification required)",
  sa: "Saudi Arabia", ae: "the United Arab Emirates", eg: "Egypt", pk: "Pakistan", bd: "Bangladesh",
  br: "Brazil (a Brazilian CPF or CNPJ is required)", ng: "Nigeria", ke: "Kenya", id: "Indonesia", vn: "Vietnam", th: "Thailand",
  il: "Israel", ua: "Ukraine", tw: "Taiwan", hk: "Hong Kong", sg: "Singapore (a Singapore address is required)", my: "Malaysia",
  ph: "the Philippines", za: "South Africa", ar: "Argentina", cl: "Chile", pe: "Peru", fr: "France (EU, EEA, or Swiss presence required)",
  nl: "the Netherlands", se: "Sweden", pl: "Poland", cz: "Czechia", fi: "Finland", dk: "Denmark", pt: "Portugal", ch: "Switzerland",
  ie: "Ireland (a real connection to Ireland is required)", nz: "New Zealand", et: "Ethiopia", gh: "Ghana", tz: "Tanzania",
  lk: "Sri Lanka", np: "Nepal", kh: "Cambodia", mm: "Myanmar", mn: "Mongolia", ge: "Georgia",
};

// Generic endings this file knows; any other ending gets a note that the file cannot confirm it exists.
const KNOWN_GTLDS = new Set(["com", "net", "org", "info", "biz", "app", "dev", "xyz", "tech", "online", "site", "store", "shop",
  "art", "design", "studio", "cloud", "live", "page", "link", "network", "systems", "tools", "world", "zone", "space", "digital",
  "agency", "works", "games", "social", "community", "foundation", "ngo", "coop", "edu", "gov", "mil", "int", "pro", "name",
  "mobi", "tel", "travel", "jobs", "museum", "aero", "cat", "asia", "eco", "earth", "health", "science", "academy", "school",
  "news", "media", "blog", "wiki", "email", "chat", "team", "club", "fund", "money", "finance", "capital", "exchange", "market"]);

const SURFACES = {
  clawhub: { name: "ClawHub skill slug", ascii: true, link: () => "https://clawhub.ai", note: 'search there, or run: clawhub search "NAME"; slug rules are ClawHub\'s' },
  github: { name: "GitHub", ascii: true, link: (n) => `https://github.com/${enc(n)}`, note: "a page that doesn't exist suggests unused; reserved and retired names exist" },
  npm: { name: "npm", ascii: true, link: (n) => `https://www.npmjs.com/package/${enc(n)}`, note: "npm declines names too close to existing packages" },
  pypi: { name: "PyPI", ascii: true, link: (n) => `https://pypi.org/project/${enc(n)}/`, note: "case, hyphens, underscores, and dots count as the same name" },
  bsky: { name: "Bluesky handle", ascii: true, link: (n) => `https://bsky.app/profile/${enc(n)}.bsky.social`, note: "a domain you hold can be the handle instead" },
  hf: { name: "Hugging Face", ascii: true, link: (n) => `https://huggingface.co/${enc(n)}`, note: "" },
  fediverse: { name: "Fediverse handles", ascii: false, link: () => "per instance, no single page", note: "the same name can be someone else on another instance" },
  appstores: { name: "App stores", ascii: false, link: () => "Apple App Store Connect and Google Play Console", note: "Apple requires a name unique across the App Store; Google Play does not" },
};

// Returns { lines, stop }. stop means no links are printed for this name.
function screen(n) {
  if (CONTROL_RE.test(n)) return { lines: [`  Stopped: ${JSON.stringify(n)} contains whitespace or control characters. One name per entry, nothing that could pose as this script's output.`], stop: true };
  if (HIDDEN_RE.test(n) && !joinersAllowed(n)) return { lines: [`  Stopped: hidden characters present (${hiddenPoints(n).join(", ")}). No links until they are removed.`], stop: true };
  const core = n.replace(JOINERS_RE, "");
  if (!ALLOWED_RE.test(core)) return { lines: [`  Stopped: contains characters outside letters, marks, digits, and hyphen (${disallowedPoints(core).join(", ")}). No links.${/\p{Extended_Pictographic}/u.test(core) ? " (ENS itself allows some emoji; this skill's preset is letters only.)" : " If this was a full domain, give the name and put the ending in --tlds."}`], stop: true };
  if (n.startsWith("-") || n.endsWith("-")) return { lines: ["  Stopped: a label cannot begin or end with a hyphen. No links."], stop: true };
  if (n.includes(TATWEEL)) return { lines: ["  Stopped: contains the Arabic tatweel (U+0640), a stretching mark that is not allowed in a domain label and can imitate another word. No links."], stop: true };
  if (n.startsWith("xn--")) return { lines: ["  Stopped: this looks like an encoded (punycode) label; give the name as people would write it. No links."], stop: true };
  const asciiLen = domainToASCII(`${n}.com`).replace(/\.com$/, "").length;
  if (n.length > 63 || asciiLen > 63 || asciiLen === 0) return { lines: ["  Stopped: longer than a domain label allows (63 characters after encoding), or not encodable. No links."], stop: true };
  const near = nearKnownName(n);
  if (near) return { lines: [`  Stopped: within one edit of, or built around, "${near}", a well-known name. The list is small; the cut list governs. No links.`], stop: true };
  const sc = scriptsOf(n);
  if (sc.length === 0) return { lines: ["  Stopped: no letters. No links."], stop: true };
  if (!mixAllowed(sc)) return { lines: [`  Stopped: mixed scripts (${sc.join(" + ")}): ${mixReason(sc)}. Letters involved: ${[...n].filter((c) => /\p{L}/u.test(c)).map((c) => `${c} ${lib.codePointLabel(c)}`).slice(0, 12).join(", ")}. No links.`], stop: true };
  const lines = [];
  if (sc.length === 1) lines.push(`  Scripts: ${sc[0]} (single script)`);
  else lines.push(`  Scripts: ${sc.join(" + ")}; a language that writes this way decides`);
  if (wholeScriptLookalike(n)) lines.push(`  Caution: this is written in ${sc[0]}, a script with letters that look like Latin letters${sc[0] === "Cyrillic" || sc[0] === "Greek" || sc[0] === "Armenian" || sc[0] === "Coptic" ? ", and every letter here has one" : ""}. If this is a real word in your language, carry on; if it was built to resemble a Latin name, it is a lookalike and the cut list removes it. Links follow either way.`);
  if (joinersAllowed(n)) lines.push("  Note: contains a joiner (U+200C or U+200D) that IDNA allows in this context; the registry decides.");
  const outside = latinOutsideAZ(n);
  if (outside.length) lines.push(`  Caution: Latin letters outside a to z (${[...new Set(outside)].join(", ")}). Real in Icelandic, Polish, Ewe, Fula, and other languages; also the letters used to imitate a to z. If these are letters of your language, carry on; if they were chosen to look like plain letters, it is a lookalike and the cut list removes it.`);
  return { lines, stop: false };
}

function punyLine(n, t) {
  if (/^[a-z0-9-]+$/.test(n)) return null;
  const ascii = domainToASCII(`${n}.${t}`);
  if (!ascii) return `  Punycode for ${n}.${t}: not a valid domain label under IDNA processing`;
  return `  Punycode for ${n}.${t} (IDNA processing, which differs from ENS normalization): ${ascii}`;
}

screenEndings();
const icann = values.providers === "top" ? ICANN.slice(0, 3) : ICANN;
const surfaceKeys = values.surfaces.trim().toLowerCase() === "all" ? Object.keys(SURFACES)
  : values.surfaces.split(",").map((s) => s.trim().toLowerCase()).filter(Boolean);
for (const k of surfaceKeys) if (!SURFACES[k]) fail(`Unknown surface: ${k}. Surfaces: ${Object.keys(SURFACES).join(", ")}`);

const HEADER = [
  "Searching a name exposes intent. Check at the registrar you would actually use,",
  "check the shortlist only, register promptly once decided, and never post the list first.",
  "Registrar links below are a menu; open the one you would use, not all of them.",
  "Links are as understood at the time of this version's authorship (October 2026); deep links are best effort,",
  "base links always beside them. This file cannot confirm that an ending exists today; the IANA root zone database",
  "can (https://www.iana.org/domains/root/db). .eth, .base.eth, .dao, .sol, and Handshake names live in their own systems.",
];
if (turkish) HEADER.push("Note: Turkish letters were folded the Turkish way: a dotted capital I became i and, where ş, ğ, or ı are present, a plain capital I became dotless ı; no name below carries a combining dot that looks like the plain word.");

const PUBLIC = [
  "registrant data in the registration record unless redacted or covered by a privacy service (rules differ by ending)",
  "creation and expiry dates and the registrar, even when redacted",
  "every hostname on a publicly trusted HTTPS certificate, in certificate transparency logs, permanently (a wildcard hides the names under it)",
  "for .eth, .sol, and similar, the wallet that holds the name and all its transactions",
];
const EXPIRY = "Names expire; services register them the moment they drop. Auto-renew, transfer lock, strong sign-in, and a contact email that stays alive.";
const TRADEMARK_NOTE = "always unchecked ⚠️ until you look; not legal clearance; register searches miss unregistered rights; market-specific registries exist beyond these four";

// Build the report first; render second. The JSON form is the one agents should read.
const report = {
  script: "links.mjs",
  performed: "printed links only; no network request, no check, no availability reported",
  as_understood: "October 2026",
  header: HEADER,
  stopped_endings: stoppedEndings,
  names: [],
  public_on_registration: PUBLIC,
  expiry: EXPIRY,
  not_detected: NOT_DETECTED.replace(/\n\s*/g, " "),
  status: "unchecked ⚠️ for every name, until a person clicks or a named live tool reports",
  stopped: 0,
};

for (const n of names) {
  const entry = { name: n, shown_as: revealHidden(n), stopped: false, notes: [], endings: [], surfaces: [], trademark: null };
  const g = screen(n);
  entry.notes = g.lines.map((l) => l.trim());
  if (g.stop) { entry.stopped = true; stopped += 1; report.names.push(entry); continue; }
  const isAscii = /^[a-z0-9-]+$/.test(n);
  for (const t of tlds) {
    if (NAME_SYSTEMS[t]) {
      const s = NAME_SYSTEMS[t];
      entry.endings.push({ kind: "name-system", ending: t, label: s.label(n), system: s.name, url: s.deep ? s.deep(n) : s.base, base: s.base, notes: s.note ? [s.note] : [] });
      continue;
    }
    const d = `${n}.${t}`;
    const e = { kind: "icann", ending: t, label: d, notes: [], lookup: null, registrars: [] };
    const py = punyLine(n, t);
    if (py) e.punycode = py.trim().replace(/^Punycode for [^:]+: /, "");
    const top = t.includes(".") ? t.split(".").pop() : t;
    if (top.length > 2 && !KNOWN_GTLDS.has(top)) e.notes.push(`This file cannot confirm that .${top} exists or who runs it; the IANA root zone database can.`);
    if (top.length === 2) {
      e.notes.push(CC[top] ? `Country-code ending: the code belongs to ${CC[top]}.` : "Country-code ending not in this file's table; whether it is assigned, and to whom, is in the IANA root zone database.");
      if (top === "io") e.notes.push(".io's long-term status has been under discussion since the 2024-2025 UK-Mauritius agreement on the Chagos Islands.");
      e.notes.push("Who runs the registry and where the money goes are separate questions; rules, prices, and presence requirements are the registry's.");
    }
    e.lookup = { provider: ICANN_LOOKUP.name, url: ICANN_LOOKUP.deep(d), base: ICANN_LOOKUP.base, note: ICANN_LOOKUP_NOTE.trim() };
    for (const p of icann) e.registrars.push({ provider: p.name, url: p.deep ? p.deep(d) : p.base, base: p.base, deep: Boolean(p.deep) });
    entry.endings.push(e);
  }
  for (const k of surfaceKeys) {
    const s = SURFACES[k];
    if (s.ascii && !isAscii) { entry.surfaces.push({ surface: s.name, note: "needs the ASCII slug, not this display name; run again with the slug" }); continue; }
    entry.surfaces.push({ surface: s.name, url_or_where: s.link(n), note: s.note ? s.note.replace("NAME", n) : undefined });
  }
  entry.trademark = { note: TRADEMARK_NOTE, offices: TRADEMARK.map((o) => ({ office: o.name, url: o.base })) };
  report.names.push(entry);
}
report.stopped = stopped;

if (values.json) {
  console.log(JSON.stringify(report, null, 2));
  process.exit(stopped ? 2 : 0);
}

for (const l of HEADER) console.log(l);
console.log("");
for (const se of stoppedEndings) console.log(`Stopped ending: ${JSON.stringify(se.ending)}: ${se.reason}. No links for it.`);
if (stoppedEndings.length) console.log("");
for (const entry of report.names) {
  console.log(`== ${entry.shown_as}`);
  for (const l of entry.notes) console.log("  " + l);
  if (entry.stopped) { console.log(""); continue; }
  for (const e of entry.endings) {
    console.log(`  ${e.label}`);
    if (e.system) {
      console.log(`    ${e.system}: ${e.url === e.base ? `${e.base}  (search there)` : `${e.url}  (base: ${e.base})`}`);
      for (const note of e.notes) console.log(`    ${note}`);
      continue;
    }
    if (e.punycode) console.log(`  Punycode for ${e.label} (IDNA processing, which differs from ENS normalization): ${e.punycode}`);
    for (const note of e.notes) console.log(`    ${note}`);
    console.log(`    ${e.lookup.provider}: ${e.lookup.url}  (base: ${e.lookup.base})`);
    console.log(ICANN_LOOKUP_NOTE);
    for (const r of e.registrars) console.log(`    ${r.provider}: ${r.deep ? `${r.url}  (base: ${r.base})` : `${r.base}  (search there)`}`);
  }
  if (entry.surfaces.length) {
    console.log("  Surfaces that aren't domains (a page that doesn't exist suggests unused; it is not a clearance):");
    for (const s of entry.surfaces) console.log(`    ${s.surface}: ${s.url_or_where || s.note}${s.url_or_where && s.note ? `  (${s.note})` : ""}`);
  }
  console.log(`  Trademark pre-check (${TRADEMARK_NOTE}):`);
  for (const o of entry.trademark.offices) console.log(`    ${o.office}: ${o.url}`);
  console.log("");
}

console.log("What becomes public when you register (as understood October 2026):");
for (const l of PUBLIC) console.log(`  ${l};`);
console.log("Tell the person first. " + EXPIRY);
console.log("");
console.log(NOT_DETECTED);
console.log("Status for every name above: unchecked ⚠️, until a person clicks or a named live tool reports.");
console.log("This script printed links. It performed no check, made no request, and guarantees nothing.");
if (stopped) {
  console.log(`${stopped} name(s) or ending(s) stopped. No links were printed for them.`);
  process.exit(2);
}
