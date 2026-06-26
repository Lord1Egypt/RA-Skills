# Input Handling

## Goal

Convert user inputs into a validated list of papers with accessible full PDFs.

## Accepted Inputs

- Paper titles
- Paper URLs
- Uploaded PDF files

## Workflow

### 1. Parse the input set

Identify each paper candidate and classify it as:
- title-only
- URL
- local PDF

### 2. Resolve each paper to a full PDF

#### If the input is a title

1. Search the web for the canonical paper source.
2. Prefer sources in this order:
   - arXiv
   - OpenReview
   - ACL Anthology / conference proceedings
   - publisher or author project page
3. Find a PDF URL and verify that it is the target paper.
4. Download or fetch the PDF text for analysis.

#### If the input is a URL

1. Inspect whether the URL is already a PDF.
2. If not, identify the paper landing page and locate the PDF link.
3. Verify title, venue, and year when possible.
4. Retrieve the PDF full text.

#### If the input is a local PDF

1. Extract title and basic metadata from the file.
2. Read the full text.
3. If metadata is weak or missing, use the extracted title to search for a canonical source and citation.

### 3. Validate evidence sufficiency

A paper is eligible for comparison only if:
- the PDF full text is available, and
- enough text can be extracted to identify method, setting, and results sections.

If extraction returns only metadata, abstract, or a fragmentary preview, treat the paper as blocked.

### 4. Build a paper record

After PDF retrieval, create one normalized record per paper using `comparison-schema.md`.

## Failure Policy

Stop and report blockers if any target paper lacks accessible PDF full text.
Do not proceed with cross-paper analysis based only on abstracts, snippets, or search summaries.

## Search Notes

Use web search to discover canonical sources, but use the PDF full text as the primary evidence source.
Search is for retrieval; PDF is for analysis.
