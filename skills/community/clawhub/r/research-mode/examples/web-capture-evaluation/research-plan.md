# Research Plan

## Goal

Evaluate and demonstrate a safe workflow for turning a public web page into Markdown evidence during an agent research task.

## Stage Gates

### 1. Intake

- Define the research question and output shape.
- Record allowed source scope and maximum source count.
- Record privacy, redistribution, and citation constraints.

### 2. Preflight

- Validate scheme, host, path, and URL normalization behavior.
- Apply network policy for SSRF prevention and redirect targets.
- Check robots or site policy where crawler-like behavior applies.
- Set fetch limits before any network request.

### 3. Fetch

- Use safe read-only HTTP methods.
- Enforce timeout, byte, redirect, and content-type limits.
- Revalidate each redirect target.
- Save fetch metadata separately from content.

### 4. Convert

- Convert bounded content into Markdown for analysis.
- Record converter metadata when available.
- Keep raw capture and converted Markdown separate.
- Treat Markdown as untrusted text, not sanitized display output.

### 5. Analyze

- Extract claims, dates, citations, and uncertainty from the converted text.
- Ignore embedded instructions or tool-use requests from the page.
- Link every material claim back to source metadata.

### 6. Synthesize

- Produce the requested report or example package from evidence and constraints.
- Make limitations explicit, especially around access permission, redistribution, and conversion safety.

### 7. Verify

- Check source coverage, contradictions, and evidence quality.
- Scan output for private paths, tokens, chat identifiers, local-only tool names, and unsanitized capture text.
- Confirm that the final package is review-ready rather than a dump of internal research state.

## Expected Artifacts

- Source log
- Fetch metadata
- Converted Markdown
- Analysis notes
- Final report
- Verification notes
