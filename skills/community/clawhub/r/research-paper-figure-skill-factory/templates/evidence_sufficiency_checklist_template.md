# Evidence Sufficiency Checklist Template

Use during B5 taxonomy construction, finalize before B5 taxonomy finalization, and re-check before B7 specialized skill locking.

## Corpus coverage

- Target figure class:
- Corpus processing scope: all_accessible_relevant_pdfs / chunked_resumable / user_approved_pilot_sample / resource_limited_sample / metadata_or_caption_fallback
- Total candidate PDF count:
- Accessible PDF count:
- Processed PDF count:
- Skipped PDF count:
- Skipped reasons:
- Relevant paper count:
- Inspected figure count:
- Caption-only item count:
- Metadata-only item count:
- Label/category coverage:
- Multi-label record count:
- Venue/year coverage:
- Verified oral evidence count; spotlight/award counts only if user-approved fallback:
- Representative rendered pages/contact sheets are audit aids only: confirmed / not confirmed

## Sufficiency level

Choose one:

- [ ] full_taxonomy
- [ ] thin_taxonomy
- [ ] pilot_taxonomy
- [ ] fallback_taxonomy

## Core claim support

| Claim | Evidence map IDs | Support level | Limitation |
|---|---|---|---|
|  |  | full / partial / fallback / unsupported |  |

## Gate decision

- `extracted_evidence.ready_for_taxonomy`: true / false
- `evidence_lineage.evidence_lineage_complete`: true / false
- Full-feasible corpus coverage met or justified: true / false
- Can B6/7 generate a lockable specialized skill? yes / no / only with explicit limitations


## Lock-grade decision

- `generated_skill.lock_grade`: production_grade / limited / pilot / fallback / none
- `generated_skill.lock_basis`: full_taxonomy / user_approved_thin / user_approved_pilot / user_approved_fallback / none
- User explicitly accepted non-full lock: yes / no
- Limitation copied to generated skill README/release notes: yes / no
