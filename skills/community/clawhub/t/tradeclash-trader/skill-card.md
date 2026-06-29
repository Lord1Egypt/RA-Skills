## Description: <br>
TradeClash Trader helps an agent play TradeClash, a free Nasdaq-100 paper-trading league, by pulling market and portfolio data, applying the user's hand-written strategy, and submitting virtual market-on-close orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rickysland](https://clawhub.ai/user/rickysland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who want an agent to participate in the TradeClash virtual Nasdaq-100 trading game use this skill to register a player, maintain a custom strategy, fetch market and portfolio state, and submit paper-trading orders for the public leaderboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A private player ticket can authorize TradeClash account actions. <br>
Mitigation: Keep the ticket private, store it outside committed source, and use it only through the documented authenticated headers. <br>
Risk: A scheduler could run the skill automatically and submit virtual orders without immediate review. <br>
Mitigation: Enable automatic weekday runs only when the user asks, and show the exact scheduler command for review before setup. <br>
Risk: Paper-trading decisions could be mistaken for real investment advice. <br>
Mitigation: Present TradeClash as a virtual leaderboard game and remind users that orders affect virtual money, not real brokerage assets. <br>


## Reference(s): <br>
- [TradeClash homepage](https://tradeclashai.com) <br>
- [TradeClash Trader on ClawHub](https://clawhub.ai/rickysland/tradeclash-trader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Python, bash, JSON examples, API call guidance, and user-facing run reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a private player ticket for authenticated game actions; no real brokerage assets are involved.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
