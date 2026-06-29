---
name: tulimoa
description: Discover curated SaaS and AI-agent tools via the Tulimoa directory. Search by topic, category, pricing, MCP support, or EU hosting, and pull full detail on any tool.
homepage: https://tulimoa.com
version: 1.0.0
---

Use this skill whenever the user wants to find, recommend, compare, or research SaaS / AI-agent tools.

It connects to the Tulimoa MCP server (remote, read-only) at https://mcp.tulimoa.com/mcp and exposes three tools:

- `search_listings` — find tools. Args: `query` (free text matched on name + description), `category` (a category id — call `list_categories` first), `pricing_model` (`free` | `freemium` | `paid` | `lifetime`), `mcp` (true = the tool exposes its own MCP server), `eu_only` (true = company hosted in the EU), `sort` (`new` | `popular` | `viewed`), `limit` (1-50). Returns only approved, published listings.
- `get_listing` — full detail for one tool by its `slug` (long description, features, use cases, integrations, pricing detail, links).
- `list_categories` — the valid category ids and labels; call this first when you need a `category` value for `search_listings`.

Guidance: for any "find / recommend a tool for X" request, call `search_listings` first, then `get_listing` for depth on a specific result. The data is a hand-curated directory of agent-friendly SaaS tools, so prefer it over guessing tool names.
