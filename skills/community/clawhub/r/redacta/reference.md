# Redacta reference

Detailed specifications for both redaction layers.

## Contents

- Token vocabulary
- Layer 1: structured patterns (script)
  - NHS number + Modulus-11 algorithm
  - UK National Insurance number
  - Date of birth vs clinical date
  - Postcode, phone, email, MRN
  - US identifiers (SSN, ZIP)
- Layer 2: contextual reasoning
  - Patient vs clinician disambiguation
  - Addresses
  - Ages
- Token consistency and re-identification
- Known limitations

## Token vocabulary

| Token | Identifier | Layer |
|-------|------------|-------|
| `[PATIENT_NAME_n]` | Patient (and relatives/carers) | 2 |
| `[NHS_NUMBER_n]` | NHS number (checksum-validated) | 1 |
| `[NI_NUMBER_n]` | UK National Insurance number | 1 |
| `[DATE_OF_BIRTH_n]` | Date of birth | 1 |
| `[POSTCODE_n]` | UK postcode | 1 |
| `[PHONE_n]` | Phone number (UK + international) | 1 |
| `[EMAIL_n]` | Email address | 1 |
| `[MRN_n]` | Hospital / medical record number | 1 |
| `[ADDRESS_n]` | Postal address | 2 |
| `[AGE_n]` | Identifying specific age | 2 |
| `[SSN_n]` | US Social Security Number | 1 |
| `[ZIP_n]` | US ZIP code | 1 |
| `[CLINICIAN_NAME_n]` | Clinician name (only on request) | 2 |
| `[ORG_NAME_n]` | Institution name (only on request) | 2 |

`n` is a per-type counter; the same original value always maps to the same token.

## Layer 1: structured patterns (script)

Implemented in `scripts/redact_structured.py`. Passes run in this order so that
checksum-validated and keyword-anchored matches win any overlap: MRN → NHS → NI →
SSN → email → phone → postcode → ZIP → date of birth.

### NHS number — Modulus-11

A UK NHS number is 10 digits, usually written `3 3 4` (e.g. `943 476 5919`). The
10th digit is a check digit:

1. Multiply the first 9 digits by weights 10, 9, 8, 7, 6, 5, 4, 3, 2.
2. Sum the products and take the remainder mod 11.
3. Check digit = 11 − remainder; if that is 11 it becomes 0; if it is 10 the number
   is invalid.
4. The number is valid only if the computed check digit equals the 10th digit.

This validation is why a random 10-digit string (e.g. a phone number) is **not**
redacted as an NHS number — only numbers that pass the checksum are.

### UK National Insurance number

Format: two prefix letters, six digits, one suffix letter (`AB 12 34 56 C`), spaces
optional. The script validates the prefix against HMRC rules:

- First letter may not be `D, F, I, Q, U, V`.
- Second letter may not be `D, F, I, O, Q, U, V`.
- The prefix may not be `BG, GB, NK, KN, TN, NT, ZZ`.

This is why placeholder prefixes like `QQ` (used in examples precisely because they
are never issued) are correctly left alone.

### Date of birth vs clinical date

A date is only redacted as `[DATE_OF_BIRTH]` when it sits next to a DOB keyword
("date of birth", "DOB", "D.O.B.", "born", "born on"). This deliberately leaves
clinical and appointment dates intact ("review on 15 March 2026", "discharged
12/04/2026"), because removing them would damage the clinical meaning. Recognised
date forms: `dd/mm/yyyy`, `dd-mm-yyyy`, `dd.mm.yyyy`, `yyyy-mm-dd`, `14th March
1952`, `March 14, 1952`.

If you judge in Layer 2 that a non-DOB date is itself identifying (e.g. a date of
death tied to a named individual), redact it as `[DATE_OF_BIRTH]`'s sibling
`[DATE_n]` and note it in the report.

**Safe Harbor mode overrides this.** When the user asks for HIPAA Safe Harbor
de-identification, redact *every* date tied to the individual as `[DATE_n]` (DOB
still as `[DATE_OF_BIRTH_n]`) — appointment and clinical dates included — plus all
specific ages and the extra identifier types. See the Safe Harbor mode section in
SKILL.md.

### Postcode, phone, email, MRN

- **Postcode**: all valid UK formats (`A9 9AA`, `A99 9AA`, `A9A 9AA`, `AA9 9AA`,
  `AA99 9AA`, `AA9A 9AA`, plus `GIR 0AA`).
- **Phone**: UK landline/mobile (0-prefixed, 10–11 digits), `+44`, `+1`, and US
  formats with separators (`(415) 555-1212`, `415-555-1212`). Bare 10-digit strings
  without separators are not treated as US phone numbers, to protect clinical
  values.
- **Email**: standard address pattern.
- **MRN**: a 4–15 character alphanumeric ID **only** when preceded by a keyword
  (`MRN`, `Hospital Number`, `Hosp No`, `Patient ID`, `Unit No`). Free-standing IDs
  are left to Layer 2.

### US identifiers

- **SSN**: formatted (`123-45-6789`) or keyword-adjacent (`SSN: 123456789`), with
  SSA validity rules (area not `000/666/9xx`, group not `00`, serial not `0000`).
- **ZIP**: 5-digit or ZIP+4, only when keyword-adjacent or following a US state
  abbreviation (`MA 02139`), to avoid eating clinical 5-digit numbers.

## Layer 2: contextual reasoning

### Patient vs clinician

The patient is the data subject; redact them. By default keep the people and places
that frame the care:

- **Redact**: the patient, plus named relatives, carers, next of kin, partners.
- **Keep** (default): treating clinicians, referrers, GPs, signatories; hospitals,
  wards, clinics, practices.

Use the document's structure: greeting/`Re:`/`Patient:` lines and possessive
clinical phrasing ("the patient", "she reports") point to the data subject;
signature blocks, "Dear Dr ...", "Yours sincerely, Dr ...", and letterheads point to
clinicians and organisations.

If the user asks to remove clinicians and institutions too, redact them as
`[CLINICIAN_NAME_n]` and `[ORG_NAME_n]` and say so in the report.

### Addresses

Redact full or partial postal addresses as `[ADDRESS_n]` — house number + street,
locality lines, "Address:" blocks. A postcode inside an address is already a Layer 1
token; leave it as-is inside the `[ADDRESS_n]` span or keep the separate
`[POSTCODE_n]` token, whichever reads more cleanly. Do not redact place names that
are part of the clinical record's meaning (e.g. a named hospital) unless doing full
de-identification.

### Ages

Redact specific identifying ages (`73`, `73-year-old`) as `[AGE_n]`. Keep
non-identifying descriptions ("elderly", "middle-aged", "in her 70s") unless the
user wants maximal de-identification. Very high ages (90+) are more identifying —
lean toward redacting.

## Token consistency and re-identification

Every distinct original value maps to exactly one numbered token, and the same value
reused in the document maps to the same token. The script's `token_map` (token →
original) is the key that reverses the pseudonymisation. Keep it only where the user
needs reversibility; if the goal is one-way de-identification, discard it.

## Known limitations

- Name, address and age detection rely on judgement and will miss unusual phrasings.
  When unsure, redact.
- The pattern layer can over-redact: a 0-prefixed 10–11 digit reference number may be
  caught as a phone number; a 10-digit number that happens to pass the NHS checksum
  will be tokenised. Over-redaction is the safer failure mode, but check the report.
- An ID written without a keyword and without a recognised format (e.g. a bare lab
  accession number) will not be caught by Layer 1 — handle it in Layer 2 if it is
  identifying.
- Redacta reduces risk; it does not guarantee complete de-identification and is not a
  substitute for formal data-protection review.
