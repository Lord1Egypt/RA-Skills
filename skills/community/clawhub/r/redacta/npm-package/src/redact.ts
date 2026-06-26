/**
 * Redacta — deterministic pattern engine.
 *
 * Pure TypeScript: no DOM, no network, no storage. Replaces fixed-format
 * identifiers and PII with labelled tokens, catches keyword-anchored names
 * (patients, relatives, carers — clinician names preserved), self-checks the
 * output, and reverses the process from a token map.
 */

export type Category = "clinical" | "general" | "safeharbor";

// ---------------------------------------------------------------------------
// Validators
// ---------------------------------------------------------------------------

/** Validate a 10-digit NHS number using the Modulus-11 check digit. */
export function isValidNhs(digits: string): boolean {
  if (!/^\d{10}$/.test(digits)) return false;
  if (digits === digits[0].repeat(10)) return false;
  const weights = [10, 9, 8, 7, 6, 5, 4, 3, 2];
  const total = weights.reduce((sum, w, i) => sum + Number(digits[i]) * w, 0);
  let check = 11 - (total % 11);
  if (check === 11) check = 0;
  if (check === 10) return false;
  return check === Number(digits[9]);
}

const NI_INVALID_PREFIX = new Set(["BG", "GB", "NK", "KN", "TN", "NT", "ZZ"]);
const NI_PREFIX1_BAD = new Set("DFIQUV");
const NI_PREFIX2_BAD = new Set("DFIOQUV");

/** Validate the two-letter prefix of a UK National Insurance number. */
export function isValidNi(prefix: string): boolean {
  const p = prefix.toUpperCase();
  if (p.length !== 2 || NI_INVALID_PREFIX.has(p)) return false;
  return !NI_PREFIX1_BAD.has(p[0]) && !NI_PREFIX2_BAD.has(p[1]);
}

/** Luhn checksum for payment card numbers. */
export function isValidLuhn(digits: string): boolean {
  if (!/^\d{13,19}$/.test(digits)) return false;
  let sum = 0;
  let dbl = false;
  for (let i = digits.length - 1; i >= 0; i--) {
    let d = Number(digits[i]);
    if (dbl) {
      d *= 2;
      if (d > 9) d -= 9;
    }
    sum += d;
    dbl = !dbl;
  }
  return sum % 10 === 0;
}

// ---------------------------------------------------------------------------
// Tokeniser: same value -> same token, distinct values -> new numbers
// ---------------------------------------------------------------------------

class Tokeniser {
  private byKey = new Map<string, string>();
  private counters = new Map<string, number>();
  readonly tokenMap: Record<string, string> = {};

  tokenFor(type: string, original: string, key?: string): string {
    const k = `${type}::${key ?? original}`;
    const existing = this.byKey.get(k);
    if (existing) return existing;
    const n = (this.counters.get(type) ?? 0) + 1;
    this.counters.set(type, n);
    const token = `[${type}_${n}]`;
    this.byKey.set(k, token);
    this.tokenMap[token] = original;
    return token;
  }
}

// ---------------------------------------------------------------------------
// Patterns
// ---------------------------------------------------------------------------

const MONTHS =
  "January|February|March|April|May|June|July|August|September|" +
  "October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept?|Oct|Nov|Dec";

const DATE = [
  String.raw`\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4}`,
  String.raw`\d{4}-\d{2}-\d{2}`,
  String.raw`\d{1,2}(?:st|nd|rd|th)?\s+(?:${MONTHS})\s+\d{4}`,
  String.raw`(?:${MONTHS})\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}`,
]
  .map((s) => `(?:${s})`)
  .join("|");

// A date only counts as a DOB when anchored to a DOB keyword, so clinical and
// appointment dates are left intact.
const DOB_RE = new RegExp(
  String.raw`(\b(?:date\s+of\s+birth|d\.?o\.?b\.?|born(?:\s+on)?)[\s:.]*)((?:${DATE}))`,
  "gi"
);

const NHS_RE = /\b(\d{3}[\s-]?\d{3}[\s-]?\d{4})\b/g;

const NI_RE = /\b([A-Za-z]{2})\s?(\d{2})\s?(\d{2})\s?(\d{2})\s?([A-Da-d])\b/g;

const SSN_FMT_RE = /(?<!\d)(?!000|666|9\d\d)(\d{3})([-\s])(\d{2})\2(\d{4})(?!\d)/g;
const SSN_KW_RE =
  /((?:SSN|Social\s*Security(?:\s*(?:Number|No\.?|#))?)[\s:]*)((?!000|666|9\d\d)\d{9})(?!\d)/gi;

const EMAIL_RE = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;

const MRN_RE =
  /((?:MRN|Hospital\s*(?:No\.?|Number)|Hosp\.?\s*(?:No\.?|Number)|Patient\s*ID|Unit\s*(?:No\.?|Number))[\s:]*)([A-Z0-9-]{4,15})/gi;

const POSTCODE_RE = /\b(GIR\s?0AA|[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2})\b/gi;

const US_STATES =
  "AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|" +
  "MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC";
const ZIP_KW_RE = /((?:ZIP|Zip\s*Code|Postal\s*Code)[\s:]*)(\d{5}(?:-\d{4})?)(?!\d)/gi;
const ZIP_STATE_RE = new RegExp(
  String.raw`((?:,?\s)(?:${US_STATES})\s+)(\d{5}(?:-\d{4})?)(?!\d)`,
  "g"
);

// --- General-PII additions -------------------------------------------------

const URL_RE = /\b(?:https?:\/\/|www\.)[^\s<>"'\])]+/gi;

const IP_RE = /\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b/g;

// Candidate card numbers (13-19 digits, optionally space/dash separated),
// confirmed with the Luhn checksum before redacting.
const CARD_RE = /(?<![\d-])(?:\d[ -]?){12,18}\d(?![\d-])/g;

const IBAN_RE = /\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){2,7}(?:\s?[A-Z0-9]{1,3})?\b/g;

const ACCOUNT_KW_RE =
  /((?:Account|Acct\.?|Member\s*ID|Policy\s*(?:No\.?|Number)|Insurance\s*ID)\s*(?:No\.?|Number|#)?[\s:]*)((?=[A-Z0-9-]*\d)[A-Z0-9-]{5,17})/gi;

const UK_PLATE_RE = /\b[A-Z]{2}\d{2}\s?[A-Z]{3}\b/g;

// --- Names (keyword-anchored) ----------------------------------------------
// Names need contextual judgement, which a client-side deterministic engine
// can't fully do. We catch the high-confidence cases — names introduced by a
// courtesy title, a salutation, or a label — and deliberately PRESERVE names
// carrying a clinical title (Dr, Consultant, Nurse, ...), matching the Redacta
// skill's "don't redact the treating clinician" rule. Names buried in free
// prose are NOT caught; the UI tells users to review.
const NAME = String.raw`[A-Z][a-z]+(?:['’\-][A-Za-z]+)?(?:[ \t]+[A-Z][a-z]+(?:['’\-][A-Za-z]+)?){0,2}`;
// Case-sensitive, anchored version. Used to trim a loosely-captured name down
// to its leading run of properly capitalised words — necessary because the
// label/relative regexes carry the `i` flag (for the keyword), which would
// otherwise let a name match swallow trailing lowercase words ("Sarah is the").
const STRICT_NAME_RE = new RegExp("^" + NAME);

/** Split a loosely-captured name into its real leading name and the remainder. */
function leadingName(s: string): { name: string; rest: string } | null {
  const m = s.match(STRICT_NAME_RE);
  if (!m) return null;
  return { name: m[0], rest: s.slice(m[0].length) };
}
const COURTESY_TITLE = "Mr|Mrs|Ms|Miss|Mx";
const CLINICAL_TITLE =
  "Dr|Doctor|Prof|Professor|Consultant|Nurse|Sister|Matron|Surgeon|Registrar";

// "Mrs Patricia Hartley" → redact title + name together.
const NAME_TITLE_RE = new RegExp(String.raw`\b(?:${COURTESY_TITLE})\.?\s+(${NAME})`, "g");
// "Dear Patricia Hartley" → keep "Dear", redact the name — unless a clinical title follows.
const NAME_SALUTATION_RE = new RegExp(
  String.raw`\b(Dear)\s+(?!(?:${CLINICAL_TITLE})\b)(${NAME})`,
  "g"
);
// "Patient: ...", "Name - ...", "Re: ..." → keep the label, redact the name.
const NAME_LABEL_RE = new RegExp(
  String.raw`\b((?:Patient(?:\s+Name)?|Name|Client|Re)\s*[:\-]\s*)(${NAME})`,
  "gi"
);

// Relatives and carers: a relationship word followed by a name. HIPAA Safe
// Harbor treats relatives' names as identifiers, so "her daughter Sarah" or
// "NOK: John Hartley" should be redacted too.
const RELATION =
  "daughter|son|wife|husband|partner|spouse|mother|father|mum|mom|dad|" +
  "sister|brother|sibling|grandson|granddaughter|grandmother|grandfather|" +
  "grandparent|aunt|uncle|niece|nephew|cousin|carer|caregiver|guardian|" +
  "parent|next\\s+of\\s+kin|nok|relative|widow|widower";
const RELATIVE_NAME_RE = new RegExp(
  String.raw`\b(${RELATION})([:,\-]?[ \t]+)(${NAME})`,
  "gi"
);

// ---------------------------------------------------------------------------
// Redaction passes
// ---------------------------------------------------------------------------

type Pass = (text: string, tok: Tokeniser) => string;

const digitsOf = (s: string) => s.replace(/\D/g, "");

const redactMrn: Pass = (text, tok) =>
  text.replace(MRN_RE, (_m, kw: string, id: string) =>
    kw + tok.tokenFor("MRN", id, id.toUpperCase())
  );

const redactAccount: Pass = (text, tok) =>
  text.replace(ACCOUNT_KW_RE, (_m, kw: string, id: string) =>
    kw + tok.tokenFor("ACCOUNT_NUMBER", id, id.toUpperCase())
  );

const redactDob: Pass = (text, tok) =>
  text.replace(DOB_RE, (_m, kw: string, date: string) =>
    kw + tok.tokenFor("DATE_OF_BIRTH", date)
  );

const redactNhs: Pass = (text, tok) =>
  text.replace(NHS_RE, (m, raw: string) => {
    const d = digitsOf(raw);
    if (d.length === 10 && isValidNhs(d)) return tok.tokenFor("NHS_NUMBER", raw, d);
    return m;
  });

const redactNi: Pass = (text, tok) =>
  text.replace(NI_RE, (m, p1: string, p2: string, p3: string, p4: string, p5: string) => {
    if (!isValidNi(p1)) return m;
    const key = (p1 + p2 + p3 + p4 + p5).toUpperCase();
    return tok.tokenFor("NI_NUMBER", m.trim(), key);
  });

const redactSsn: Pass = (text, tok) => {
  let out = text.replace(SSN_FMT_RE, (m, a: string, _sep: string, b: string, c: string) => {
    if (b === "00" || c === "0000") return m;
    return tok.tokenFor("SSN", m, a + b + c);
  });
  out = out.replace(SSN_KW_RE, (m, kw: string, num: string) => {
    if (num.slice(3, 5) === "00" || num.slice(5, 9) === "0000") return m;
    return kw + tok.tokenFor("SSN", num, num);
  });
  return out;
};

const redactCard: Pass = (text, tok) =>
  text.replace(CARD_RE, (m) => {
    const d = digitsOf(m);
    if (d.length >= 13 && d.length <= 19 && isValidLuhn(d)) {
      return tok.tokenFor("CARD_NUMBER", m.trim(), d);
    }
    return m;
  });

const redactIban: Pass = (text, tok) =>
  text.replace(IBAN_RE, (m) => {
    const clean = m.replace(/\s/g, "");
    if (clean.length >= 15 && clean.length <= 34) {
      return tok.tokenFor("IBAN", m, clean.toUpperCase());
    }
    return m;
  });

const redactUrl: Pass = (text, tok) =>
  text.replace(URL_RE, (m) => tok.tokenFor("URL", m, m.toLowerCase()));

const redactEmail: Pass = (text, tok) =>
  text.replace(EMAIL_RE, (m) => tok.tokenFor("EMAIL", m, m.toLowerCase()));

const redactPhone: Pass = (text, tok) => {
  const mk = (m: string) => tok.tokenFor("PHONE", m.trim(), digitsOf(m));
  let out = text.replace(
    /(?<!\d)\+44[\s-]?(?:\(0\))?[\s-]?\d{2,5}[\s-]?\d{3,4}[\s-]?\d{3,4}(?!\d)/g,
    mk
  );
  out = out.replace(/(?<!\d)\+1[\s\-.]?\(?\d{3}\)?[\s\-.]?\d{3}[\s\-.]?\d{4}(?!\d)/g, mk);
  out = out.replace(/(?<!\d)\(?0\d{2,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}(?!\d)/g, (m) => {
    const len = digitsOf(m).length;
    return len >= 10 && len <= 11 ? mk(m) : m;
  });
  out = out.replace(/(?<!\d)\(?[2-9]\d{2}\)?[\s\-.][2-9]\d{2}[\s\-.]\d{4}(?!\d)/g, mk);
  return out;
};

const redactPostcode: Pass = (text, tok) =>
  text.replace(POSTCODE_RE, (m) => {
    const clean = m.replace(/\s/g, "");
    if (clean.length >= 5 && clean.length <= 7) {
      return tok.tokenFor("POSTCODE", m, clean.toUpperCase());
    }
    return m;
  });

const redactZip: Pass = (text, tok) => {
  let out = text.replace(ZIP_KW_RE, (_m, kw: string, zip: string) =>
    kw + tok.tokenFor("ZIP", zip)
  );
  out = out.replace(ZIP_STATE_RE, (_m, pre: string, zip: string) =>
    pre + tok.tokenFor("ZIP", zip)
  );
  return out;
};

const redactIp: Pass = (text, tok) =>
  text.replace(IP_RE, (m) => tok.tokenFor("IP_ADDRESS", m));

const redactPlate: Pass = (text, tok) =>
  text.replace(UK_PLATE_RE, (m) =>
    tok.tokenFor("VEHICLE_REG", m, m.replace(/\s/g, "").toUpperCase())
  );

const redactRelative: Pass = (text, tok) =>
  text.replace(RELATIVE_NAME_RE, (m, rel: string, sep: string, name: string) => {
    // The `i` flag (for the relationship word) relaxes the name's
    // capitalisation, so trim to the leading capitalised run — this both
    // rejects "daughter and two sons" and stops "Sarah is the" over-capturing.
    const split = leadingName(name);
    if (!split) return m;
    return (
      rel + sep +
      tok.tokenFor("RELATIVE_NAME", split.name, split.name.toLowerCase()) +
      split.rest
    );
  });

const redactName: Pass = (text, tok) => {
  const nameToken = (raw: string) =>
    tok.tokenFor("PATIENT_NAME", raw.trim(), raw.trim().toLowerCase().replace(/\s+/g, " "));
  // Courtesy-titled names first. Store the full match (title + name) as the
  // original so re-identification restores "Mrs Patricia Hartley" verbatim,
  // but key on the name alone so the same person dedupes across contexts.
  let out = text.replace(NAME_TITLE_RE, (m, name: string) =>
    tok.tokenFor("PATIENT_NAME", m.trim(), name.trim().toLowerCase().replace(/\s+/g, " "))
  );
  // Salutations without a courtesy title (clinical titles already excluded).
  out = out.replace(NAME_SALUTATION_RE, (_m, dear: string, name: string) =>
    `${dear} ${nameToken(name)}`
  );
  // Labelled names — preserve the original label + separator. This regex also
  // carries the `i` flag (for the label word), so trim the name the same way.
  out = out.replace(NAME_LABEL_RE, (m, prefix: string, name: string) => {
    const split = leadingName(name);
    if (!split) return m;
    return prefix + nameToken(split.name) + split.rest;
  });
  return out;
};

// --- Safe Harbor extras (HIPAA §164.514(b)(2)) -----------------------------
// Stricter passes layered on top of clinical + general for full Safe Harbor
// de-identification: ALL dates (not just DOB), specific ages, fax numbers,
// certificate/licence numbers, device serials, VINs, and health-plan numbers.
const ANY_DATE_RE = new RegExp("(?:" + DATE + ")", "g");
const AGE_PHRASE_RE = /\b\d{1,3}[\s-]?(?:years?[\s-]?old|y\/?o)\b/gi;
const AGE_LABEL_RE = /\b(aged|age)([:\s]+)(\d{1,3})\b/gi;
const FAX_RE = /\b(fax(?:\s*(?:no\.?|number|#))?[:\s]+)(\+?[\d(][\d().\s-]{6,}\d)/gi;
const LICENSE_RE =
  /\b((?:licen[cs]e|certificate|cert\.?|registration)\s*(?:no\.?|number|#)?[:\s]+)([A-Z0-9][A-Z0-9-]{3,})/gi;
const DEVICE_RE =
  /\b((?:serial|device\s*(?:id|identifier|no\.?|number)|imei)\s*(?:no\.?|number|#)?[:\s]+)([A-Z0-9][A-Z0-9-]{4,})/gi;
const VIN_RE = /\b[A-HJ-NPR-Z0-9]{17}\b/g;
const HEALTH_PLAN_RE =
  /\b((?:health\s*plan|beneficiary|medicare|medicaid)\s*(?:id|no\.?|number|#)?[:\s]+)([A-Z0-9][A-Z0-9-]{4,})/gi;

const redactAllDates: Pass = (text, tok) =>
  text.replace(ANY_DATE_RE, (m) => tok.tokenFor("DATE", m));

const redactAge: Pass = (text, tok) => {
  let out = text.replace(AGE_PHRASE_RE, (m) =>
    tok.tokenFor("AGE", m.trim(), m.replace(/\D/g, ""))
  );
  out = out.replace(AGE_LABEL_RE, (_m, kw: string, sep: string, num: string) =>
    kw + sep + tok.tokenFor("AGE", num)
  );
  return out;
};

const redactFax: Pass = (text, tok) =>
  text.replace(FAX_RE, (_m, kw: string, num: string) =>
    kw + tok.tokenFor("FAX", num.trim(), digitsOf(num))
  );

const redactLicense: Pass = (text, tok) =>
  text.replace(LICENSE_RE, (_m, kw: string, id: string) =>
    kw + tok.tokenFor("LICENSE", id, id.toUpperCase())
  );

const redactDevice: Pass = (text, tok) =>
  text.replace(DEVICE_RE, (_m, kw: string, id: string) =>
    kw + tok.tokenFor("DEVICE_ID", id, id.toUpperCase())
  );

const redactVin: Pass = (text, tok) =>
  text.replace(VIN_RE, (m) => {
    // Require both a digit and a letter, so we don't grab a 17-char all-alpha
    // word or an all-digit run.
    if (!/\d/.test(m) || !/[A-Z]/.test(m)) return m;
    return tok.tokenFor("VIN", m, m.toUpperCase());
  });

const redactHealthPlan: Pass = (text, tok) =>
  text.replace(HEALTH_PLAN_RE, (_m, kw: string, id: string) =>
    kw + tok.tokenFor("HEALTH_PLAN_NUMBER", id, id.toUpperCase())
  );

// Order matters: keyword-anchored and checksum-validated patterns first,
// weaker heuristics last, so high-confidence matches win any overlap.
const CLINICAL_PASSES: Pass[] = [
  redactMrn,
  redactDob,
  redactNhs,
  redactNi,
  redactSsn,
  redactEmail,
  redactPhone,
  redactPostcode,
  redactZip,
  redactRelative,
  redactName,
];

const GENERAL_PASSES: Pass[] = [
  redactAccount,
  redactCard,
  redactIban,
  redactUrl,
  redactEmail,
  redactPhone,
  redactPostcode,
  redactZip,
  redactIp,
  redactPlate,
  redactRelative,
  redactName,
];

// redactFax must run BEFORE the generic phone pass, or a fax number is claimed
// as [PHONE]. It's keyword-anchored ("Fax: ...") so running first is safe.
const SAFE_HARBOR_PRE_PASSES: Pass[] = [redactFax];

// Layered after clinical + general. redactAllDates runs last so keyword DOBs are
// already [DATE_OF_BIRTH] and only the remaining dates (appointments) → [DATE].
const SAFE_HARBOR_EXTRA_PASSES: Pass[] = [
  redactAge,
  redactLicense,
  redactDevice,
  redactVin,
  redactHealthPlan,
  redactAllDates,
];

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

export interface RedactionResult {
  text: string;
  changed: boolean;
}

// Self-check: patterns that should NOT remain in already-redacted text. These
// are intentionally broad — they flag *possible* leftovers for human review,
// not confirmed identifiers. Tokens like [NHS_NUMBER_1] are excluded.
const RESIDUAL_CHECKS: { label: string; re: RegExp }[] = [
  { label: "long number (10+ digits)", re: /(?<![\d-])\d[\d\s-]{8,}\d(?![\d-])/g },
  { label: "email address", re: /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g },
  { label: "UK postcode", re: /\b[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b/gi },
  { label: "URL", re: /\b(?:https?:\/\/|www\.)\S+/gi },
];

export interface ResidualFinding {
  label: string;
  sample: string;
}

/**
 * A Redactor keeps one Tokeniser across many texts, so the same identifier
 * gets the same token on every sticky note on the board.
 */
export class Redactor {
  private tok = new Tokeniser();
  private passes: Pass[];

  constructor(categories: Category[]) {
    // Safe Harbor is the strictest mode and implies clinical + general plus the
    // extra Safe Harbor passes (all dates, ages, fax, licence, device, VIN,
    // health-plan numbers).
    const safeHarbor = categories.includes("safeharbor");
    const seen = new Set<Pass>();
    const passes: Pass[] = [];
    if (safeHarbor) {
      for (const p of SAFE_HARBOR_PRE_PASSES) if (!seen.has(p)) (seen.add(p), passes.push(p));
    }
    if (categories.includes("clinical") || safeHarbor) {
      for (const p of CLINICAL_PASSES) if (!seen.has(p)) (seen.add(p), passes.push(p));
    }
    if (categories.includes("general") || safeHarbor) {
      for (const p of GENERAL_PASSES) if (!seen.has(p)) (seen.add(p), passes.push(p));
    }
    if (safeHarbor) {
      for (const p of SAFE_HARBOR_EXTRA_PASSES) if (!seen.has(p)) (seen.add(p), passes.push(p));
    }
    this.passes = passes;
  }

  redactText(input: string): RedactionResult {
    // Normalise non-breaking spaces so spaced identifiers still match.
    let text = input.replace(/[   ]/g, " ");
    for (const pass of this.passes) text = pass(text, this.tok);
    return { text, changed: text !== input };
  }

  /** {token_type: number_of_distinct_values} */
  get report(): Record<string, number> {
    const report: Record<string, number> = {};
    for (const token of Object.keys(this.tok.tokenMap)) {
      const type = token.slice(1, -1).replace(/_\d+$/, "");
      report[type] = (report[type] ?? 0) + 1;
    }
    return report;
  }

  /** {token: original_value} — for review / re-identification. Handle with care. */
  get tokenMap(): Record<string, string> {
    return { ...this.tok.tokenMap };
  }
}

/**
 * Re-scan already-redacted text for anything that still looks like an
 * identifier, so the UI can warn the user to check manually. Returns one
 * finding per distinct sample (deduplicated, capped). A clean result is not a
 * guarantee — it's a second pair of eyes, not a proof.
 */
/**
 * Re-identification: replace tokens with their original values, using a token
 * map produced by an earlier redaction. The inverse of redaction — for putting
 * real data back into AI output before it returns to the board.
 *
 * Tokens always end in "]", so "[NAME_1]" never matches inside "[NAME_10]";
 * plain string replacement is safe.
 */
export function reinstate(
  text: string,
  tokenMap: Record<string, string>
): RedactionResult {
  let out = text;
  for (const [token, original] of Object.entries(tokenMap)) {
    if (token) out = out.split(token).join(original);
  }
  return { text: out, changed: out !== text };
}

/** Validate that a parsed object is a usable token map ([TOKEN] -> string). */
export function isValidTokenMap(value: unknown): value is Record<string, string> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return false;
  const entries = Object.entries(value as Record<string, unknown>);
  if (entries.length === 0) return false;
  return entries.every(
    ([k, v]) => /^\[[A-Z_]+_\d+\]$/.test(k) && typeof v === "string"
  );
}

export function selfCheck(redactedText: string): ResidualFinding[] {
  const seen = new Set<string>();
  const findings: ResidualFinding[] = [];
  for (const { label, re } of RESIDUAL_CHECKS) {
    for (const match of redactedText.matchAll(re)) {
      const sample = match[0].trim();
      // Ignore our own tokens, e.g. [NHS_NUMBER_1].
      if (/^\[[A-Z_]+_\d+\]$/.test(sample)) continue;
      const key = `${label}:${sample.toLowerCase()}`;
      if (seen.has(key)) continue;
      seen.add(key);
      findings.push({ label, sample });
      if (findings.length >= 20) return findings;
    }
  }
  return findings;
}
