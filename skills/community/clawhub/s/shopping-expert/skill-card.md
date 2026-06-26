## Description: <br>
Find and compare products online (Google Shopping) and locally (stores near you). Auto-selects best products based on price, ratings, availability, and preferences. Generates shopping list with buy links and store locations. Use when asked to shop for products, find best deals, compare prices, or locate items locally. Supports budget constraints (low/medium/high or "$X"), preference filtering (brand, features, color), and dual-mode search (online + local stores). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[udiedrichsen](https://clawhub.ai/user/udiedrichsen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search for products online, locate nearby stores, compare price, ratings, availability, shipping or distance, and produce a ranked shopping list. It supports budget, country, local-search location, preferences, and text or JSON output controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping queries, preferences, country codes, and local-search locations may be sent to SerpAPI or Google Places. <br>
Mitigation: Use only approved API keys and avoid local or hybrid searches when location disclosure is not acceptable. <br>
Risk: Prices, availability, and local inventory may be stale or incomplete. <br>
Mitigation: Verify final price, availability, shipping, and store stock with the seller before purchase. <br>
Risk: The ranking algorithm may over-weight incomplete third-party result metadata such as ratings, reviews, shipping, or distance. <br>
Mitigation: Treat rankings as decision support and compare important products or stores manually before acting. <br>


## Reference(s): <br>
- [Shopping Expert on ClawHub](https://clawhub.ai/udiedrichsen/shopping-expert) <br>
- [Publisher profile: udiedrichsen](https://clawhub.ai/user/udiedrichsen) <br>
- [Skill homepage](https://github.com/clawdbot/clawdbot) <br>
- [SerpAPI search endpoint](https://serpapi.com/search) <br>
- [Google Places API endpoint](https://places.googleapis.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown shopping table by default, or structured JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs ranked products or stores with prices or distance, ratings, availability, source links, warnings, and search metadata.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
