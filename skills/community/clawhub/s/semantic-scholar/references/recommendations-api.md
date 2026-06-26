# Recommendations API

## Purpose

Use the Recommendations API when the user already has one or more seed papers and wants related literature.

## Primary Workflow

- Start from trusted seed paper IDs.
- Call the recommendations endpoint for related papers.
- If the user wants richer metadata than the recommendations response provides, follow up with `paper/batch`.
- Keep recommendation-derived results separate from query-derived results so provenance stays explicit.

## When It Beats Search

- The user says "papers similar to this one" or "expand this seed set".
- Keyword search is too brittle or misses nearby work.
- The goal is a related-work neighborhood rather than exhaustive keyword coverage.

## Practical Notes

- Recommendations complement search; they do not replace broad Boolean search for exhaustive reviews.
- Save the input seed IDs with the output records.
- Use recommendations first, then merge with Graph API search results only if the user wants both views.
