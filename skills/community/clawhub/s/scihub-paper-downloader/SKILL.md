---
name: scihub-paper-downloader
description: "Get a PDF link from Sci-Hub for a DOI."
---

# Sci-Hub Paper Downloader

Given a DOI, use the bundled Python script to resolve a direct PDF URL through the current Sci-Hub and Sci-Net flow.

Treat the script output as follows:

- If it returns a URL, use that as the final PDF link.
- If it returns `NOT_FOUND` and a second line starts with `OA_LINK `, treat that value as the OA entry link shown on the Sci-Hub page. It may be a publisher page, repository page, or another non-PDF landing page rather than a final PDF URL.
- If it returns `NOT_FOUND` with no second line, report that Sci-Hub does not currently have the paper.
- If it returns `MIRROR_ERROR`, report that Sci-Hub could not be resolved reliably and the result is inconclusive.
- If it returns `INVALID_INPUT`, ask for a valid DOI.
