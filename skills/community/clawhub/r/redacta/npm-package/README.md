# @pharmatools/redacta

Pseudonymise patient identifiers and PII in text — and restore them. A
dependency-free TypeScript engine you can embed in any Node or browser pipeline.

```bash
npm install @pharmatools/redacta
```

```ts
import { Redactor, reinstate, selfCheck } from "@pharmatools/redacta";

const redactor = new Redactor(["clinical", "general"]);
const { text } = redactor.redactText(
  "Dear Mrs Patricia Hartley, NHS Number: 943 476 5919"
);
// text -> "Dear [PATIENT_NAME_1], NHS Number: [NHS_NUMBER_1]"

// same Redactor keeps a token map across many strings (consistent tokens)
const original = reinstate(text, redactor.tokenMap).text;
// original -> "Dear Mrs Patricia Hartley, NHS Number: 943 476 5919"

// second-pass safety check on already-redacted text
const leftovers = selfCheck(text); // ResidualFinding[]
```

## What it detects

Deterministic, checksum-validated patterns — NHS numbers (Modulus-11), UK
National Insurance numbers, dates of birth (keyword-anchored; appointment dates
preserved), UK postcodes, US SSN/ZIP, hospital/MRN numbers, emails, phones —
plus general PII (URLs, IPs, Luhn-validated payment cards, IBANs, account
numbers, UK vehicle regs) and keyword-anchored patient / relative / carer names
(clinician names preserved by design). Names in free prose are not caught.

Same value → same token across a `Redactor` instance; the `tokenMap` reverses
the redaction. No DOM, no network, no storage.

### Safe Harbor mode

`new Redactor(["safeharbor"])` applies a stricter, US-focused pass aligned with
the HIPAA Safe Harbor method (§164.514). It implies `clinical` + `general` and
adds: **all** dates (not just DOB — appointment dates included), specific ages,
fax numbers, certificate/licence numbers, device serial numbers, VINs, and
health-plan/beneficiary numbers.

```ts
const r = new Redactor(["safeharbor"]);
r.redactText("73-year-old, appointment 15 March 2026, fax 0113 496 1234").text;
// "[AGE_1], appointment [DATE_1], fax [FAX_1]"
```

Note: this over-redacts slightly versus the letter of the standard (it removes
all specific ages and full dates rather than only ages 90+ and date elements
beyond the year) — deliberately, on the safe side. Biometric and photographic
identifiers are out of scope for a text engine. Not legal advice; review output.

## API

- `new Redactor(categories: ("clinical" | "general")[])` — `.redactText(s)`,
  `.report`, `.tokenMap`
- `reinstate(text, tokenMap)` → `{ text, changed }`
- `selfCheck(text)` → `ResidualFinding[]`
- `isValidNhs`, `isValidNi`, `isValidLuhn`, `isValidTokenMap`

This is the same engine that powers the
[Redacta for Miro app](https://www.pharmatools.ai/redacta) and the
[`redacta-mcp` server](https://www.npmjs.com/package/redacta-mcp). For an
agent-skill build with LLM reasoning over free-text names, see the
[Redacta skill](https://clawhub.ai/nickjlamb/redacta).

## Limits

Deterministic + keyword-anchored detection only — not a guarantee, not a
substitute for formal data-protection processes. Review the output, and treat the
token map as the key that reverses the redaction.

## License

MIT-0. Built by [PharmaTools.AI](https://www.pharmatools.ai/redacta).
