## Description: <br>
Taopiaopiao helps agents summarize public movie, cinema, showtime, price, rating, and basic film information from Taopiaopiao pages without booking or bulk scraping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike47512](https://clawhub.ai/user/mike47512) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to summarize public Taopiaopiao movie and cinema pages, compare showtimes and price ranges, and prepare lightweight reminders or analysis with source links and collection time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live ticketing pages can contain time-sensitive showtime, region, and price information. <br>
Mitigation: Include the collection time, region, and source link in summaries, and ask the user to verify details before relying on them. <br>
Risk: Automating public ticketing pages can create scraping or platform-compliance concerns. <br>
Mitigation: Keep activity user-directed, apply frequency control, and avoid bulk scraping or interface reverse engineering. <br>
Risk: Ticketing or account pages may request credentials or payment-related actions. <br>
Mitigation: Do not book tickets, place orders, or provide account credentials unless the user separately trusts the browsing session and site. <br>


## Reference(s): <br>
- [Taopiaopiao homepage](https://dianying.taobao.com/) <br>
- [ClawHub skill page](https://clawhub.ai/mike47512/taopiaopiao) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Natural-language text or Markdown summaries with source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries should include the city or region, collection time, and source page when reporting time-sensitive showtime or price information.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
