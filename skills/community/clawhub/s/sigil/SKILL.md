---
name: sigil
description: "Brand reviews from a public website and an optional product document. Use it for brand review through Sigil's MCP server."
---

# Sigil

Brand reviews from a public website and an optional product document.

## Connect

Add Sigil's MCP server: https://sigilbrandstudio.com/mcp (Streamable HTTP, no sign-in).

## Offers

### Brand review

Sigil's review of a company's current brand from its website and, optionally, one document (a pitch deck, memo or product brief). Use it when someone wants feedback on their brand, positioning, messaging, website or visual identity. It returns a brand score out of 100, a verdict, six scored dimensions, what the brand says against what the business is, positioning, visual identity and voice notes, a one-line brand idea and the changes to make first.

1. Call `start_read`. It returns an id.
2. Call `check_read` with the id until it is ready; it usually takes a few minutes.
3. Give the person the result and its link.
