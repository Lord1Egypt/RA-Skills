## Description: <br>
PSN Assistant helps agents look up PlayStation Store deals, PS Plus games, cross-region prices, game ratings, trophy guides, new releases, PSN service status, and deal reminders from public sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jundongGit](https://clawhub.ai/user/jundongGit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External PlayStation users and shopping-focused agents use this skill to find current discounts, PS Plus catalog information, regional price comparisons, game ratings, trophy guidance, release calendars, PSN status, and optional deal reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prices, discounts, PS Plus availability, release dates, ratings, and PSN status can change after the skill retrieves public web data. <br>
Mitigation: Show source links and remind users to verify current details on the official PlayStation Store or status page before purchasing or acting. <br>
Risk: Cross-region price comparisons may omit account, payment, language, tax, or entitlement constraints. <br>
Mitigation: State that cross-region purchases require a regional account and advise users to confirm language support, payment requirements, and local terms before buying. <br>
Risk: Deal reminders may retain selected game and sale metadata in a local watchlist. <br>
Mitigation: Do not request or store PSN passwords, payment details, or private account data, and remove watchlist entries when reminders are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jundongGit/psn-deals) <br>
- [PlayStation Blog](https://blog.playstation.com/) <br>
- [PSDeals](https://psdeals.net/us-store) <br>
- [PlatPrices](https://platprices.com/) <br>
- [PSN Service Status](https://status.playstation.com/) <br>
- [PSNProfiles Trophy Guides](https://psnprofiles.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown tables and concise text responses with links and optional JSON watchlist entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include time-sensitive price, region, sale-end, rating, and status data from public web pages; deal reminders can use a local watchlist.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
