---
name: vaudtax
description: Working with .vaudtax files (Swiss canton Vaud tax declarations). Use when the user mentions a .vaudtax file, wants to read/summarize/convert a VD tax declaration, or inspect tax data (income, deductions, assets, attached documents).
---

# VaudTax Skill

## File format

A `.vaudtax` file is a **ZIP archive** containing:

- **One XML file** (named `<filename>.xml`) — the entire tax declaration as structured XML under the namespace `http://www.vd.ch/fiscalite/vaudtax`, root element `<vaudTaxData>`.
  - **Namespace:** `http://www.vd.ch/fiscalite/vaudtax` (proprietary format, no public XSD available)
  - **Structure:** 32+ main sections organizing all tax declaration data
- **Zero or more `doc*` files** — attached supporting documents: PDF, JPEG, or PNG. The format is declared in the XML's `<mimeType>` field.

## Bundled scripts

All scripts live in the `scripts/` subdirectory of this skill and use only Python standard library — no installs needed.

| Script | Purpose |
|---|---|
| `parse_vaudtax.py <file.vaudtax>` | Parse and print a human-readable summary to stdout; `--extract` writes attachments to disk |
| `export_json.py <file.vaudtax> [out.json]` | Export clean JSON (omits UI/navigation state) |
| `compute_code800.py <file.vaudtax>` | Estimate revenu imposable ICC (code 800), IFD, and fortune — outputs values ready to pass to `calculate_taxes.py` |
| `calculate_taxes.py --periode YEAR --commune NAME --revenu-icc N --fortune-icc N --revenu-ifd N` | Query the official Canton Vaud tax calculator via HTTP POST and return authoritative results |

The JSON output conforms to **`vaudtax-export.schema.json`** (JSON Schema 2020-12; file is in the skill root).

`<skill-dir>` below is this skill's base directory, announced when the skill is loaded — use it directly:

```bash
python <skill-dir>/scripts/parse_vaudtax.py /path/to/file.vaudtax
python <skill-dir>/scripts/export_json.py  /path/to/file.vaudtax
```

Only if the base directory is unknown, locate the scripts with `find -L` (the `-L` is required: skill directories are often symlinks, which plain `find` does not descend into):

```bash
find -L ~ -name parse_vaudtax.py -path '*vaudtax*' 2>/dev/null | head -1
```

## Key XML sections

`parse_vaudtax.py` covers all known sections. Read [`references/xml-sections.md`](references/xml-sections.md) only when you need to work with the raw XML: the per-section field tables, which sections are not yet parsed, year-to-year element renames, and a discovery snippet for unexpected `None` fields.

## Summarizing a file

Run `parse_vaudtax.py` and present the output using this structure:

1. **Filing info** — fiscal year, reference, municipality
2. **Taxpayer(s)** — name, birthdate, civil status, profession; CTB2 if joint filer
3. **Income** — employed activity, pension/rentes, self-employment
4. **Deductions** — transport, meals, professional expenses, insurance/3rd pillar, rent, medical, debt interest, education
5. **Assets** — bank accounts, investment portfolios, cash, real estate, vehicles, movable objects
6. **Attached documents** — filename and size for each
7. **Cross-check results** — outcome of proactive PDF verification (see below)

Amounts are in CHF unless a different `devise` is specified.

The summary masks direct identifiers (NAVS13, IBANs, phone, e-mail) by default — keep them masked in your output. Rerun with `--full` only if the user explicitly asks for them.

**Only report what exists.** Do not mention sections that are empty, not initialized, or not applicable to this taxpayer. If `parse_vaudtax.py` reports no unknown sections, say nothing about sections at all.

**A summary is just a summary.** Do not run `compute_code800.py` or `calculate_taxes.py` unless the user explicitly asks for a tax estimate.

### Proactive cross-checks

Even for a basic summary, cross-check the attachment types below against their XML values — discrepancies are high-value findings the user needs before filing.

**Only extract and read the attachment types named below.** Attached PDFs are by far the dominant token cost of a summary; the skill defines no comparison for other attachments (bank statements, insurance invoices, …), so list those from their XML metadata without reading them. Read one only when the user asks to verify it — and for long bank statements, totals are usually on the first and last pages, so read those pages before anything else.

**Read the needed attachments in parallel** (wall-clock time scales with the slowest single document, not the total count).

**Pillar 3a attestations** (label contains "21 EDP", "cotisations", or "pilier 3a"):
1. Extract the attachments (see [Extracting and reading attached files](#extracting-and-reading-attached-files)) and read each extracted file — see [`references/pillar-attestation.md`](references/pillar-attestation.md) for field layout
2. Sum per taxpayer; compare against `formesReconnuesPrevoyanceIndividuelleContribuable1` / `...Contribuable2`
3. Flag any discrepancy: **"⚠ Écart pilier 3a : attestations CHF X, déclaration CHF Y — vérifier avant envoi"**

**Salary certificates** (label contains "Certificat de salaire"):
1. Extract the attachment (see [Extracting and reading attached files](#extracting-and-reading-attached-files)) and read the extracted file — see [`references/salary-certificate.md`](references/salary-certificate.md) for field layout
2. Extract line 11 (salaire net) and line 10.1 (LPP); compare against `salaireNet` and `cotisationOrdinaire` in the XML
3. Flag any mismatch beyond ±1 CHF rounding

Skip the cross-checks only if the user explicitly asks for a quick overview. A quick overview is also the privacy option: no attached PDF is extracted or read, so only the redacted XML summary enters the conversation.

When verifying deductions, see [`references/deductions.md`](references/deductions.md) for official rules and caps.

## Full analysis — always include taux marginal

For any full analysis (running both `compute_code800.py` and `calculate_taxes.py`), **always also compute the taux marginal** with `--marginal-rate`:

```bash
python calculate_taxes.py \
  --periode YEAR --commune "Commune" \
  --revenu-icc N --fortune-icc N --revenu-ifd N \
  --marginal-rate
```

This makes two HTTP calls and returns the marginal rate for ICC, IFD, and the combined total. Include it in the output:

| | Taux marginal |
|---|---|
| ICC (cantonal + communal) | X.XX % |
| IFD (fédéral direct) | X.XX % |
| **Total** | **X.XX %** |

See [`references/tax-computation.md`](references/tax-computation.md) for ICC and IFD formulas.

## Extracting and reading attached files

Extract attachments with `parse_vaudtax.py --extract` — it writes them to a temp directory and prints one path per line:

```bash
python <skill-dir>/scripts/parse_vaudtax.py file.vaudtax --extract doc17700000000000 doc17700000000001
# --extract all extracts everything — avoid it for summaries; extract only the
# attachments you will actually read (see Proactive cross-checks)
```

Then read each printed path using your agent's native file reading capability (PDF and image reading is handled natively — no external tools needed). Read all paths in parallel. Long PDFs (bank statements often exceed 10 pages) may exceed your reader's per-call page limit — read those with an explicit page range instead of retrying blindly. The files persist across tool calls; delete the temp directory once you are done with them.

Use the `<key>` value (not the `<reference>` UUID) to match XML metadata to ZIP entries. Each `<documents>` element has: `<key>`, `<filename>`, `<mimeType>`, `<label>`, `<fileSize>`.

For salary certificate field layout → [`references/salary-certificate.md`](references/salary-certificate.md)
For Form 21 EDP pillar attestation structure → [`references/pillar-attestation.md`](references/pillar-attestation.md)

## Official references

| Resource | URL | Notes |
|---|---|---|
| Instructions générales 2025 | [21001_2025.pdf](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/21001_2025.pdf) | Main guide; URL is year-specific |
| ICC barème revenu 2025 | [barème_revenu_2025.pdf](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/barème_revenu_2025.pdf) | Income tax table at CHF 100 intervals |
| ICC barème fortune 2025 | [barème_fortune_2025.pdf](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/barème_fortune_2025.pdf) | Wealth tax table at CHF 1'000 intervals |
| IFD barème 2025 (form 58c) | [Bareme_IFD_58c-2025.pdf](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/Bareme_IFD_58c-2025.pdf) | Single + married tables |
| Communal coefficients | [Arrêtés d'imposition](https://www.vd.ch/etat-droit-finances/communes/finances-communales/arretes-dimposition-et-tableaux-des-impots-communaux) | Current year XLS for all communes |

Update PDF URLs by replacing the year suffix (e.g. `21001_2024.pdf` for fiscal year 2024).

## Reporting unhandled content

When the file contains sections or fields the skill can't handle, tell the user and suggest opening a GitHub issue.

**Report when:**
- `parse_vaudtax.py` outputs a **"Sections non reconnues"** block
- A section marked "not yet parsed" in [`references/xml-sections.md`](references/xml-sections.md) contains data (`isInitialized` is not `false` and child elements are non-empty)
- A script raises an exception or produces clearly wrong output

**Say:**
> This declaration contains content the vaudtax skill doesn't handle yet: **[describe what's missing]**. The analysis above may be incomplete.
>
> Please open an issue at **https://github.com/fredj/ai-stuff/issues** with: the fiscal year, the section name(s), and a brief description (no personal data needed).

Do **not** silently skip unhandled content.

## Data flows

Working with a declaration sends data to exactly two parties:

1. **The agent's inference API** — everything read during the analysis (parser output, attached PDFs opened for cross-checks) becomes part of the conversation. This is inherent to LLM analysis. To limit it, `parse_vaudtax.py` and `export_json.py` mask direct identifiers (NAVS13, IBANs, phone, e-mail) by default; pass `--full` only when the user explicitly needs them — they are never required for tax analysis.
2. **`calculate_taxes.py` → `https://www.vd.ch/...`** — only when the user asks for a tax estimate. The POST payload contains: fiscal year, normalized commune name, marital-status code, children counts, and the three taxable amounts (revenu ICC, fortune ICC, revenu IFD). No name, NAVS13, IBAN, or birthdate. `--marginal-rate` makes the call twice.

No other bundled script makes network calls.

**Never include declaration content in web searches, GitHub issues, or any MCP/external tool call.** The only permitted network call when working with a declaration is `calculate_taxes.py`.

## Guardrails

**Tax data is sensitive — being wrong is worse than being incomplete.**

**Sources** — Every number must trace back to script output or a direct XML field read. Never supply a value from general knowledge. If a field is absent, say so — absent ≠ zero ≠ "not applicable".

**No mental arithmetic** — Never compute ICC/IFD/fortune tax without running `compute_code800.py` + `calculate_taxes.py`. The only exception is explaining the method conceptually.

**Year-specific rules** — Always read `fiscalPeriod` before applying any deduction cap, barème table, or form field name. The limits in [`references/deductions.md`](references/deductions.md) are 2025 values and differ for other years.

**No guessing** — Never infer what an unhandled section contains, never fabricate totals from partial data, never guess XML field names (use the discovery snippet in [`references/xml-sections.md`](references/xml-sections.md)).

**Estimates vs official figures** — `compute_code800.py` output is an estimate. When a `lastGesdemReference` or official bordereau is available, those figures take precedence.

**Commune rates** — Tax coefficients are commune-specific. Flag any mismatch between the commune in `identification` and the one passed to `calculate_taxes.py`.

**Réforme valeur locative (from 2029)** — Valeur locative suppressed, mortgage interest non-deductible (except primo-acquéreurs Art. 33a LIFD), code 660 disappears for IFD. Do not apply pre-2029 rules to post-2028 projections.

**Network** — The only network call is `calculate_taxes.py` → `https://www.vd.ch/...` — no personal identifiers; see [Data flows](#data-flows) for the exact payload.

**When in doubt:** say what you found, say what you couldn't find, and let the user decide.
