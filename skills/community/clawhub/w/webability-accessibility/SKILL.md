---
name: webability-accessibility
description: Scan pages and HTML for WCAG 2.2, ADA and Section 508 accessibility issues with the WebAbility MCP server, get framework-aware fixes, and verify each fix with a re-scan.
version: 1.0.0
homepage: https://www.webability.io
metadata:
  openclaw:
    emoji: "♿"
    homepage: https://www.webability.io/mcp
    requires:
      bins:
        - curl
    envVars:
      - name: WEBABILITY_API_KEY
        required: false
        description: Optional. Unlocks visual_audit, start_audit and get_audit. Create a free account at https://www.webability.io.
---

# WebAbility accessibility MCP

Use this skill when the user asks to check a web page, component or HTML snippet for accessibility problems (WCAG 2.2, ADA, Section 508, EAA, AODA), to fix them, or to prove a fix worked.

WebAbility is an accessibility platform: https://www.webability.io. Setup docs: https://www.webability.io/mcp. Source (MIT): https://github.com/snayyar00/webability-mcp.

## Setup

1. Add the hosted MCP server to your agent. No install, no key needed for scan and check tools:

   ```json
   { "mcpServers": { "webability": { "url": "https://mcp.webability.io/mcp" } } }
   ```

   Transport is Streamable HTTP.

2. Optional local option (stdio): `npx -y @webability/mcp` or `docker run -i --rm webabilityio/mcp:latest`.

3. Optional: sign up free at https://www.webability.io, create an API key, and set `WEBABILITY_API_KEY`. This unlocks the account tools `visual_audit`, `start_audit` and `get_audit`.

## Workflow

1. `scan_page` for a live URL, or `scan_html` for raw HTML or a component. Treat `incomplete` results as questions, not as errors to auto-fix.
2. `detect_framework`, then `generate_ai_fix` to get ready-to-paste fixes for that framework (Tailwind, MUI, Bootstrap, Next.js, WordPress).
3. Apply the fix in the code.
4. `verify_fix` with the URL and the selector. Report the result as verified only when it returns verified: true. If you changed the class or id, re-run `scan_page`.
5. Use `diff_scan` to compare before and after, and `flow_scan` for multi-page journeys such as checkout.

## Other tools

- `check_color_contrast`: check a foreground and background pair against WCAG.
- `check_aria`: check ARIA usage.
- `get_rules`: list the rules and the WCAG criteria they map to.
- `find_source` (local npx or Docker only): map a CSS selector to the source file that holds it.
- `visual_audit`: vision-based audit for issues DOM scanners miss (needs account).
- `start_audit`, `get_audit`: full audit with a downloadable report and Excel workbook (needs account).

## Rules for the agent

- Report only what the tools return. Do not claim a page is "compliant". An automated scan does not prove full WCAG conformance.
- Do not auto-apply contrast or `incomplete` fixes without the user reviewing them.
- Send only URLs and HTML the user asked you to scan.

More: https://www.webability.io/mcp
