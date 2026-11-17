---
name: security-writeup-bad-effects
description: >
  Add a plain per-section "Bad effect:" statement to each section of a
  defensive security or incident-analysis write-up, naming the concrete harm
  and the failure mode. Use when reviewing or finishing a security/analysis
  article (e.g. a malware dissection) or when the user asks what the bad effect
  of a section is or wants each section annotated.
---

# Security Write-up — Per-Section Bad Effects

Security write-ups tend to describe a finding in neutral, structural terms ("the file is wired into the build", "the token counts are suspicious"). A reader can finish a section without registering what it actually costs them. Add one **Bad effect** statement per substantive section: the concrete harm a reader would suffer, and the failure mode that lets it land.

## Inputs

- `target` — path to the article in `ai-thoughts/docs/` (optional). If omitted, apply to the security article currently being worked on.

## Outputs

- The article with one `**Bad effect:**` paragraph per substantive section.

## Procedure

1. Read the article and list its sections in order (red flags, dynamic analysis, capability, evidence, response, cleanup, and so on).
2. For each section, identify the harm it implies and the assumption it destroys. Ask: "if a reader under-reacts to this section, what do they lose?" and "which comfortable assumption does this section refute?"
3. Write one short paragraph led by `**Bad effect:**`, naming (a) the concrete harm and (b) the failure mode or the trust check it defeats. Keep the article's voice and add no new facts.
4. For analyst-methodology sections (sandboxing, evidence handling), use `**Bad effect (methodology alert):**` — the harm is to the investigator (partial containment, residual exposure), not to the victim.
5. For caveat / evidence sections, spell out the double edge: "not proven" is not "not malicious"; symmetrically, do not over-claim a demonstrated theft.
6. Place the statement at the end of the section's prose, after its claim and before the next heading.
7. Run `python scripts/unwrap_md.py --check`; regenerate the READMEs only if the article's `articles.yaml` description changed.

## Constraints

- **One per section.** A single paragraph that summarizes the section's harm — not one per bullet.
- **Concrete, not generic.** Name the harm ("runs as you with `process.env` + `fs` + `child_process` reach"), not "this is dangerous".
- **No new facts.** Everything must follow from the section's own content.
- **Plain and calm.** State the effect; don't sensationalize.
- **Defensive framing only.** For a malware write-up the "bad effect" is what the payload does to the victim — never operational or attacker-enabling detail.

## Verification

- Every substantive section carries exactly one Bad-effect statement.
- Each names a specific harm and a failure mode, not a vague warning.
- Methodology sections use the `(methodology alert)` variant.
- Reading only the Bad-effect paragraphs, top to bottom, tells the article's risk story.

## Error Handling

- **User says no**: skip; leave the article as-is.
- **Article already annotated**: verify one-per-section; remove duplicates rather than adding more.
- **Not a security/analysis article**: do not apply to essays, translations, READMEs, or `articles.yaml`.
