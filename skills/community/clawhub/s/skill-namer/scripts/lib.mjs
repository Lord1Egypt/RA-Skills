// Skill Namer: lib.mjs
// Shared helpers for forge.mjs and links.mjs. Node built-ins only. No network, no checks of availability.
import { domainToASCII } from "node:url";

export const SCRIPTS = ["Latin", "Greek", "Cyrillic", "Armenian", "Hebrew", "Arabic", "Syriac", "Thaana",
  "Devanagari", "Bengali", "Gurmukhi", "Gujarati", "Oriya", "Tamil", "Telugu", "Kannada", "Malayalam",
  "Sinhala", "Thai", "Lao", "Tibetan", "Myanmar", "Georgian", "Hangul", "Ethiopic", "Cherokee", "Khmer",
  "Mongolian", "Hiragana", "Katakana", "Han", "Bopomofo", "Lisu", "Coptic", "Tifinagh", "Nko", "Adlam", "Vai",
  "Canadian_Aboriginal", "Javanese", "Balinese", "Tagalog", "Yi", "Tai_Viet", "Osage", "Ol_Chiki", "Meetei_Mayek",
  "Lepcha", "Limbu", "Buhid", "Hanunoo", "Tagbanwa", "Cham", "Tai_Tham", "Tai_Le", "New_Tai_Lue", "Bamum",
  "Mandaic", "Samaritan", "Glagolitic", "Deseret", "Sundanese", "Batak", "Rejang", "Saurashtra", "Kayah_Li"];
// Scripts few registries accept (historic, ceremonial, or very new); named so two of them never read as one.
export const RARE_SCRIPTS = ["Ahom", "Anatolian_Hieroglyphs", "Avestan", "Bassa_Vah", "Bhaiksuki", "Brahmi",
  "Braille", "Buginese", "Carian", "Caucasian_Albanian", "Chakma", "Chorasmian", "Cuneiform", "Cypriot",
  "Cypro_Minoan", "Dives_Akuru", "Dogra", "Duployan", "Egyptian_Hieroglyphs", "Elbasan", "Elymaic", "Gothic",
  "Grantha", "Gunjala_Gondi", "Hanifi_Rohingya", "Hatran", "Imperial_Aramaic", "Inscriptional_Pahlavi",
  "Inscriptional_Parthian", "Kaithi", "Kawi", "Kharoshthi", "Khitan_Small_Script", "Khojki", "Khudawadi", "Linear_A",
  "Linear_B", "Lycian", "Lydian", "Mahajani", "Makasar", "Manichaean", "Marchen", "Masaram_Gondi", "Medefaidrin",
  "Mende_Kikakui", "Meroitic_Cursive", "Meroitic_Hieroglyphs", "Miao", "Modi", "Mro", "Multani", "Nabataean",
  "Nag_Mundari", "Nandinagari", "Newa", "Nushu", "Nyiakeng_Puachue_Hmong", "Ogham", "Old_Hungarian", "Old_Italic",
  "Old_North_Arabian", "Old_Permic", "Old_Persian", "Old_Sogdian", "Old_South_Arabian", "Old_Turkic", "Old_Uyghur",
  "Osmanya", "Pahawh_Hmong", "Palmyrene", "Pau_Cin_Hau", "Phags_Pa", "Phoenician", "Psalter_Pahlavi", "Runic",
  "Shavian", "Sharada", "Siddham", "SignWriting", "Sogdian", "Sora_Sompeng", "Soyombo", "Syloti_Nagri", "Takri",
  "Tangsa", "Tangut", "Tirhuta", "Toto", "Ugaritic", "Vithkuqi", "Wancho", "Warang_Citi", "Yezidi",
  "Zanabazar_Square", "Garay", "Gurung_Khema", "Kirat_Rai", "Ol_Onal", "Sunuwar", "Todhri", "Tulu_Tigalari"];
const SCRIPT_RE = {};
for (const s of [...SCRIPTS, ...RARE_SCRIPTS]) { try { SCRIPT_RE[s] = new RegExp(`\\p{Script=${s}}`, "u"); } catch { /* older Unicode tables */ } }
const RARE_NOTE = " (most registries will not accept it)";
const NEUTRAL_RE = /\p{Script=Common}|\p{Script=Inherited}/u;

// Sets a language itself writes in; any other mix is stopped, because most registries allow one script per label.
// Japanese writing mixes kana, kanji, and Latin letters; .jp allows that in one label, ENS normalization may not.
export const ALLOWED_MIXES = [["Han", "Hiragana", "Katakana"], ["Han", "Hangul"], ["Han", "Bopomofo"], ["Latin", "Han", "Hiragana", "Katakana"]];
// Scripts with letters that look like Latin letters; a mix with Latin here is the lookalike pattern.
export const LATIN_LOOKALIKE_SCRIPTS = ["Cyrillic", "Greek", "Armenian", "Cherokee", "Lisu", "Coptic", "Canadian_Aboriginal", "Osage", "Tifinagh", "Deseret"];

const cp = (n) => String.fromCodePoint(n);
// Invisible and format characters: Unicode's default-ignorable set, all format characters, plus the classic ranges.
export const HIDDEN_RE = new RegExp(
  "\\p{Default_Ignorable_Code_Point}|\\p{Cf}|[" + cp(0x200B) + "-" + cp(0x200F) + cp(0x202A) + "-" + cp(0x202E) +
  cp(0x2060) + "-" + cp(0x2064) + cp(0xFEFF) + "]", "u");
// The two joiners IDNA allows in some Indic and Arabic-script contexts (CONTEXTJ).
const JOINER_RE = new RegExp("[" + cp(0x200C) + cp(0x200D) + "]", "gu");

// Whitespace and control characters never belong in a name; they also let text pose as script output.
export const CONTROL_RE = /[\s\p{Cc}]/u;

// What a name may contain: letters, combining marks, decimal digits, hyphen.
export const ALLOWED_RE = /^[\p{L}\p{M}\p{Nd}-]+$/u;

export function codePointLabel(ch) {
  return "U+" + ch.codePointAt(0).toString(16).toUpperCase().padStart(4, "0");
}

// Lowercase with the Turkish I handled: toLowerCase turns a dotted capital I into i plus a combining dot,
// which makes a lookalike of the plain word. The combining dot after i is dropped and reported by the caller.
// NFKC first, so compatibility forms (fullwidth, mathematical, modifier letters) become the plain letters a registry stores.
// Turkish and Azerbaijani: when a word carries ş, ğ, ı, or İ, a capital I lowercases to dotless ı, as those languages write it.
const TURKISH_MARK = /[şğıİŞĞ]/u;
export function fold(s) {
  const k = s.normalize("NFKC");
  const lowered = TURKISH_MARK.test(k) ? k.replace(/I/g, "ı").toLowerCase() : k.toLowerCase();
  return lowered.normalize("NFC").replace(new RegExp("i" + cp(0x0307), "gu"), "i");
}

export function hadTurkishCapital(s) {
  const k = s.normalize("NFKC");
  return TURKISH_MARK.test(k) && /I/.test(k);
}

export function hadTurkishDot(s) {
  return /İ/.test(s) || hadTurkishCapital(s);
}

export function revealHidden(s) {
  return [...s].map((ch) => (HIDDEN_RE.test(ch) || CONTROL_RE.test(ch) ? `[${codePointLabel(ch)}]` : ch)).join("");
}

export function hiddenPoints(s) {
  const out = [];
  for (const ch of [...s]) if (HIDDEN_RE.test(ch)) out.push(codePointLabel(ch));
  return [...new Set(out)];
}

// True when the only hidden characters are joiners that IDNA accepts in this label (checked by encoding it).
export function joinersAllowed(s) {
  const others = [...s].filter((ch) => HIDDEN_RE.test(ch) && !JOINER_RE.test(ch) && (JOINER_RE.lastIndex = 0, true));
  JOINER_RE.lastIndex = 0;
  if (others.length) return false;
  if (!JOINER_RE.test(s)) { JOINER_RE.lastIndex = 0; return false; }
  JOINER_RE.lastIndex = 0;
  return domainToASCII(`${s}.com`) !== "";
}

export function disallowedPoints(s) {
  const out = [];
  for (const ch of [...s]) if (!/[\p{L}\p{M}\p{Nd}-]/u.test(ch)) out.push(codePointLabel(ch));
  return [...new Set(out)];
}

export function scriptsOf(s) {
  const found = new Set();
  for (const ch of [...s]) {
    if (NEUTRAL_RE.test(ch)) continue;
    let scriptName = null;
    for (const name in SCRIPT_RE) if (SCRIPT_RE[name].test(ch)) { scriptName = RARE_SCRIPTS.includes(name) ? name + RARE_NOTE : name; break; }
    found.add(scriptName || "a script this file does not list" + RARE_NOTE);
  }
  return [...found];
}

// Arabic tatweel (U+0640) stretches letters and is disallowed in domain labels under IDNA2008; it also makes within-script lookalikes.
export const TATWEEL = cp(0x0640);

// Latin letters outside a to z after folding and accent stripping: real in Icelandic, Polish, Ewe, Fula, and others, and also the
// small capitals and IPA letters used to imitate a to z. A caution, never a stop; the skeleton still finds listed names.
export function latinOutsideAZ(s) {
  const folded = fold(s).normalize("NFD").replace(/\p{M}/gu, "");
  return [...folded].filter((ch) => /\p{Script=Latin}/u.test(ch) && !/[a-z]/.test(ch));
}

export function mixAllowed(sc) {
  return sc.length <= 1 || ALLOWED_MIXES.some((group) => sc.every((x) => group.includes(x)));
}

// Why a mix is stopped: the lookalike pattern, or the one-script-per-label rule most registries apply.
export function mixReason(sc) {
  if (sc.includes("Latin") && sc.some((x) => LATIN_LOOKALIKE_SCRIPTS.includes(x))) return "lookalike pattern";
  return "most registries allow one script per label, and the sets a language writes in are the only mixes passed here";
}

// A small, non-exhaustive list of often-imitated names, the services this skill links to among them.
// Matching rules, applied to the folded name and to its plain-Latin skeleton (lookalike letters, digits, accents,
// compatibility forms folded):
//   exact, for every listed name;
//   a listed name with one or more service words before or after it (applepay, mybinancelogin, appleidverify);
//   an adjacent transposition, for listed names of six letters or more (payapl, gtihub);
//   for listed names of six letters or more that are not also everyday words (COMMON): the name anywhere inside a
//   longer name (thepaypalapp), a substitution that keeps the first two and last two letters (gighub), a substitution
//   between letters that look alike (paypai), or a doubled letter added or removed (gooogle, gogle).
// Plain one-letter differences at the edges (finance, interest, switch) and short or everyday-word brands (venom, karna,
// aina, dal) are left to the agent's cut list, so ordinary words are not stopped as brands.
export const KNOWN_NAMES = ["github", "gitlab", "paypal", "google", "gmail", "apple", "icloud", "microsoft", "amazon",
  "openai", "chatgpt", "anthropic", "claude", "metamask", "coinbase", "binance", "uniswap", "opensea", "ethereum",
  "bitcoin", "solana", "facebook", "instagram", "whatsapp", "tiktok", "youtube", "netflix", "twitter", "discord",
  "telegram", "slack", "stripe", "venmo", "cashapp", "zelle", "chase", "wellsfargo", "citibank", "barclays",
  "unicef", "redcross", "medicare", "medicaid", "irsgov", "clawhub", "openclaw", "moltbook", "godaddy", "namecheap",
  "cloudflare", "porkbun", "dynadot", "hover", "gandi", "squarespace", "huggingface", "bluesky", "unstoppable",
  "namebase", "basenames", "shopify", "spotify", "notion", "vercel", "revolut", "monzo", "nubank", "linear", "figma",
  "canva", "airbnb", "dropbox", "reddit", "linkedin", "pinterest", "snapchat", "wechat", "alipay", "alibaba",
  "samsung", "nvidia", "adobe", "salesforce", "hubspot", "zendesk", "atlassian", "twitch", "roblox", "minecraft",
  "nintendo", "playstation", "tesla", "spacex", "starlink", "klarna", "robinhood", "trezor",
  "farcaster", "warpcast", "arbitrum", "chainlink", "makerdao", "ledger", "phantom", "rainbow", "polygon", "optimism",
  "disney", "nike", "adidas", "visa", "amex", "hsbc", "santander", "paytm", "phonepe", "mpesa", "gcash", "uber", "zoom",
  "icann", "iana", "uspto", "euipo", "wipo", "tmview", "ensdomains", "npmjs", "pypi", "adl", "lens", "aave", "lido", "zora"];
export const COMMON = new Set(["apple", "slack", "stripe", "chase", "hover", "notion", "linear", "ledger", "phantom",
  "rainbow", "polygon", "optimism", "claude", "canva", "gandi", "monzo", "zelle", "uber", "zoom", "visa", "lens",
  "disney", "discord", "twitch", "telegram", "twitter", "reddit", "amazon", "tesla", "adobe", "oracle", "intel",
  "anthropic", "revolut", "solana", "unstoppable"]);
// Words that turn a listed name into a service lookalike (applepay, ledgerlive, chasebank), stopped on every listed name.
export const SERVICE_WORDS = ["pay", "id", "care", "wallet", "live", "bank", "online", "login", "secure", "support", "app",
  "plus", "store", "cash", "card", "help", "verify", "account", "official", "team", "music", "tv", "watch", "credit",
  "debit", "eats", "nano", "page", "portal", "service", "my", "the", "get", "go", "hub", "home", "ai", "labs"];

// Letters of other scripts and IPA that look like Latin letters, and digit-for-letter swaps. Small on purpose.
const LOOKALIKE = {
  "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x", "і": "i",
  "ј": "j", "ѕ": "s", "һ": "h", "ԁ": "d", "ӏ": "l", "ԛ": "q", "ԝ": "w", "ѡ": "w",
  "α": "a", "ο": "o", "ρ": "p", "ν": "v", "τ": "t", "ι": "i", "κ": "k", "χ": "x",
  "υ": "u", "η": "n", "ε": "e", "γ": "y", "ω": "w",
  "ɡ": "g", "ɑ": "a", "ɩ": "l", "ı": "i", "ſ": "s", "ǀ": "l", "ʀ": "r",
  // Latin small capitals, used to imitate a to z.
  "ᴀ": "a", "ʙ": "b", "ᴄ": "c", "ᴅ": "d", "ᴇ": "e", "ꜰ": "f", "ɢ": "g", "ʜ": "h",
  "ɪ": "i", "ᴊ": "j", "ᴋ": "k", "ʟ": "l", "ᴍ": "m", "ɴ": "n", "ᴏ": "o", "ᴘ": "p",
  "ᴛ": "t", "ᴜ": "u", "ᴠ": "v", "ᴡ": "w", "ʏ": "y", "ᴢ": "z", "ꜱ": "s",
  // Armenian, Cherokee, and Lisu letters that look like Latin letters.
  "օ": "o", "ո": "n", "ս": "u", "յ": "j", "լ": "l", "հ": "h", "գ": "q", "ա": "w",
  "Ꭺ": "a", "Ꭱ": "r", "Ꭲ": "t", "Ꭼ": "e", "Ꮃ": "w", "Ꮇ": "m", "Ꮋ": "h", "Ꮓ": "z", "Ꮯ": "c",
  "Ꮪ": "s", "Ꮲ": "p", "Ꮴ": "v", "Ꮶ": "k", "Ꮐ": "g", "Ꭻ": "j", "Ꮮ": "l", "Ꭰ": "d", "Ꮟ": "b",
  "ꓐ": "b", "ꓑ": "p", "ꓓ": "d", "ꓔ": "t", "ꓖ": "g", "ꓗ": "k", "ꓙ": "j", "ꓚ": "c", "ꓟ": "m", "ꓠ": "n", "ꓢ": "s", "ꓣ": "r", "ꓦ": "v",
  // The same Cherokee letters in their small forms, which lowercasing produces.
  "ꭺ": "a", "ꭱ": "r", "ꭲ": "t", "ꭼ": "e", "ꮃ": "w", "ꮇ": "m", "ꮋ": "h", "ꮓ": "z", "ꮯ": "c",
  "ꮪ": "s", "ꮲ": "p", "ꮴ": "v", "ꮶ": "k", "ꮐ": "g", "ꭻ": "j", "ꮮ": "l", "ꭰ": "d", "ꮟ": "b",
  "0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "7": "t", "8": "b",
};

// A plain-Latin skeleton used only to compare with the small list: compatibility forms folded (fullwidth and
// modifier letters become plain letters), lookalike letters mapped, hyphens dropped, rn to m, vv to w.
export function skeleton(s) {
  // NFKC folds compatibility forms; NFD then dropping marks strips accents (pàypal and shopìfy compare as plain).
  const k = fold(s).normalize("NFKC").replace(/-/g, "").normalize("NFD").replace(/\p{M}/gu, "").normalize("NFC");
  return [...k].map((ch) => LOOKALIKE[ch] || ch).join("").replace(/rn/g, "m").replace(/vv/g, "w");
}

// True when a single-script name is written in a script whose letters can look like Latin letters and every letter of
// it is in the small lookalike map (Cyrillic, Greek), or the whole script is one the map does not cover letter by letter
// (Cherokee, Canadian syllabics, Osage, Tifinagh, Deseret), where a caution is owed whatever the word is.
export function wholeScriptLookalike(s) {
  const letters = [...s].filter((ch) => /\p{L}/u.test(ch));
  if (letters.length === 0) return false;
  const sc = scriptsOf(s);
  if (sc.length !== 1 || !LATIN_LOOKALIKE_SCRIPTS.includes(sc[0])) return false;
  if (sc[0] === "Cyrillic" || sc[0] === "Greek" || sc[0] === "Armenian" || sc[0] === "Coptic") return letters.every((ch) => LOOKALIKE[ch]);
  return true;
}

function isTransposition(a, b) {
  if (a.length !== b.length) return false;
  const diff = [];
  for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) diff.push(i);
  return diff.length === 2 && diff[1] === diff[0] + 1 && a[diff[0]] === b[diff[1]] && a[diff[1]] === b[diff[0]];
}

const SIMILAR = [["i", "l", "j", "1"], ["o", "0"], ["e", "c"], ["g", "q"], ["u", "v"], ["n", "m"], ["b", "d"], ["p", "q"], ["t", "f"]];
function lookAlike(x, y) {
  return SIMILAR.some((g) => g.includes(x) && g.includes(y));
}

// Keys that sit next to each other on a QWERTY keyboard: the substitutions a slip of the finger makes.
const ADJACENT = { q: "wa", w: "qeas", e: "wrsd", r: "etdf", t: "ryfg", y: "tugh", u: "yihj", i: "uojk", o: "ipkl", p: "ol",
  a: "qwsz", s: "adwezx", d: "sferxc", f: "dgrtcv", g: "fhtyvb", h: "gjyubn", j: "hkuinm", k: "jliom", l: "kop",
  z: "asx", x: "zsdc", c: "xdfv", v: "cfgb", b: "vghn", n: "bhjm", m: "njk" };
function adjacentKeys(x, y) {
  return Boolean(ADJACENT[x] && ADJACENT[x].includes(y));
}

// One substitution: a letter from outside a to z (a lookalike the small map does not cover), letters that look alike
// anywhere, or an interior slip to a neighboring key (first two and last two letters kept). Any other single interior
// change (goggle, tremor) is an ordinary word and stays with the cut list.
function typoSubstitution(n, brand) {
  if (n.length !== brand.length) return false;
  const diff = [];
  for (let i = 0; i < n.length; i++) if (n[i] !== brand[i]) diff.push(i);
  if (diff.length !== 1) return false;
  const i = diff[0];
  const outsideLatin = !/[a-z]/.test(n[i]);
  return outsideLatin || lookAlike(n[i], brand[i]) || (i >= 2 && i <= n.length - 3 && adjacentKeys(n[i], brand[i]));
}

// A doubled letter added or removed: gooogle, gogle.
function doubledLetterEdit(n, brand) {
  if (Math.abs(n.length - brand.length) !== 1) return false;
  const [longer, shorter] = n.length > brand.length ? [n, brand] : [brand, n];
  for (let i = 0; i < longer.length; i++) {
    if (longer.slice(0, i) + longer.slice(i + 1) === shorter) return longer[i] === longer[i - 1] || longer[i] === longer[i + 1];
  }
  return false;
}

// A listed name wrapped in service words on either side, any number of them: applepay, appleidverify, mybinancelogin.
const SERVICE_ALT = SERVICE_WORDS.join("|");
const WRAPPED = new Map(KNOWN_NAMES.map((b) => [b, new RegExp(`^(?:${SERVICE_ALT})*${b}(?:${SERVICE_ALT})*$`)]));
function wrappedInServiceWords(n, brand) {
  return n !== brand && WRAPPED.get(brand).test(n);
}

// Returns the listed name a candidate is equal to, within one edit of, or built around; otherwise null.
// Built-around applies to every listed name except those that are also everyday words.
export function nearKnownName(name) {
  const forms = new Set([fold(name).replace(/-/g, ""), skeleton(name)]);
  const ascii = domainToASCII(`${name}.com`).replace(/\.com$/, "");
  if (ascii && !ascii.startsWith("xn--")) forms.add(ascii);
  for (const n of forms) {
    for (const brand of KNOWN_NAMES) {
      if (n === brand || wrappedInServiceWords(n, brand)) return brand;
      if (brand.length >= 6 && isTransposition(n, brand)) return brand;
      const strict = brand.length >= 6 && !COMMON.has(brand);
      if (!strict) continue;
      if (n.includes(brand) || typoSubstitution(n, brand) || doubledLetterEdit(n, brand)) return brand;
    }
  }
  return null;
}

export const NOT_DETECTED = "Not detected by any script here: lookalikes of names that are not on the small list, lookalike letters\n  from scripts the small map does not cover, and whether an ending exists today. The cut list and a person decide.";
