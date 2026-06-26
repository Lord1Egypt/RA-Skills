# Literature Corpus Plan Template

## Target skill

- Target figure class:
- Target specialized skill slug:

## Default v1.0.0 corpus scope

- Year window: `last_2_conference_years`
- Resolved years at execution time:
- Field scope: `computer_science_top_conferences`
- Presentation filter: `oral_required`
- Oral evidence required: `true`
- Fallback policy: `user_approval_required`

## Venue set

- ML / AI:
- CV:
- NLP:
- Data mining / IR / Web:
- Optional systems / HCI, only if relevant:

## Queries

- Query 1:
- Query 2:
- Query 3:

## Inclusion rules

- Recent two-year conference window.
- Computer-science top-conference venue.
- Official oral status verified.
- Open-access or user-authorized PDF/metadata source.
- Relevant to the target figure class.
- If local PDFs or a paper index already exist, enumerate the full relevant candidate set before selecting extraction scope.
- Default processing scope: `all_accessible_relevant_pdfs`.

## Exclusion rules

- No official oral-status evidence.
- Non-CS or non-top-conference venue unless user-approved fallback.
- Paywalled or unauthorized full text.
- Duplicate, poster-only, workshop-only, or unrelated papers unless user-approved fallback.

## Coverage plan

- Total candidate PDFs:
- Accessible PDFs:
- Planned processed PDFs:
- Planned skipped PDFs:
- Skipped reasons:
- Processing mode: full-feasible / chunked-resumable / user-approved pilot / resource-limited sample / metadata-or-caption fallback
- Can support production-grade lock: yes / no / only after more extraction
- Multi-label classification required: yes / no

## Evidence sources to preserve

- Official program / schedule URL:
- Official oral paper list URL:
- OpenReview decision URL:
- Proceedings / CVF / ACL Anthology URL:
- User-provided official source:
