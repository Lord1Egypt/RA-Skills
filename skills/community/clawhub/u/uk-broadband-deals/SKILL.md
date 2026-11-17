---
name: uk-broadband-deals
description: Find the broadband deals available at an exact UK address, priced by their true whole-contract cost, or check whether a UK broadband bill or renewal quote is too high. Use for UK broadband deals, prices, switching or "am I overpaying" questions.
homepage: https://www.findbroadbanddeals.com/ai-assistants
---

# UK broadband deals with FindBroadband

Every tool named below comes from FindBroadband's MCP server, `https://www.findbroadbanddeals.com/api/mcp/standard` (Streamable HTTP, no sign-in, no keys). If `search_addresses` is not available, add the server first: `claude mcp add --transport http findbroadband https://www.findbroadbanddeals.com/api/mcp/standard` (Claude Code), or point any other MCP client at the URL.

These are FindBroadband's live UK broadband deals, the same data and figures as findbroadbanddeals.com.

## Steps

1. Broadband availability differs per property. Ask for the postcode and the house number or name together in one question, then call `search_addresses`.
2. When the user's message already names the property, match it from the list and say which address you're checking. Only ask them to pick when the match is unclear.
3. Pass the `uprn` and `display_address` to the other tools and never show the uprn.
4. Deals at the address: `find_broadband_deals`. Is a bill or renewal quote too high: `check_if_overpaying`. The full terms of one deal: `get_deal_details`.

## Reporting rules

- All costs, picks and verdicts are computed by FindBroadband: present them as given and don't re-rank, re-filter or recalculate them. `total_contract_cost` and `effective_monthly_cost` already include intro pricing, later rises and setup fees.
- `precision` says whether results are for one property (`address`) or the whole postcode (`postcode`). Say which.
- Set `include_mobile_broadband` only when the user asks for 4G, 5G or wireless broadband or names a mobile provider, and `include_satellite` only when they ask for satellite or Starlink or no line is fast enough. When you show a satellite deal, say it needs a dish and an upfront cost.
- A switching credit is conditional on owing early-termination fees, never a discount.
- After showing deals, ask one short question about what matters most (budget, speed, contract length, avoiding price rises) and refine with the filters.
- Switching completes on findbroadbanddeals.com; nothing is bought in the chat.

## Use

For a person asking about their own broadband. Commercial use of the server or its data is not allowed: see https://www.findbroadbanddeals.com/terms.
