## Description: <br>
Fetch weekly sale details from Australian supermarkets (Woolworths and Coles). Use when the user wants to check current specials, compare prices, or get sale information from Woolworths or Coles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicowu07](https://clawhub.ai/user/nicowu07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve and compare current Woolworths and Coles specials in Australia. It is most useful for checking advertised grocery deals, prices, and savings, especially around the Melbourne metro area noted in the skill documentation. <br>

### Deployment Geography for Use: <br>
Australia <br>

## Known Risks and Mitigations: <br>
Risk: Installing npm dependencies and running Puppeteer browser automation can execute third-party code and browse external supermarket or aggregator sites. <br>
Mitigation: Review the scripts and dependency manifest before use, run them in a sandbox or container where practical, and avoid heavy scraping that may violate site terms or trigger rate limits. <br>
Risk: Sale data can be incomplete or stale when supermarket sites change selectors, block automation, or third-party aggregators lag behind official catalogues. <br>
Mitigation: Treat returned specials as current-price guidance, verify important prices against the supermarket site or catalogue before purchasing, and update selectors or fallback links when extraction fails. <br>


## Reference(s): <br>
- [Supermarket Sales on ClawHub](https://clawhub.ai/nicowu07/supermarket-sales) <br>
- [Publisher profile](https://clawhub.ai/user/nicowu07) <br>
- [Coles specials](https://www.coles.com.au/on-special) <br>
- [Woolworths catalogue](https://www.catalogueau.com/woolworths/) <br>
- [Woolworths specials aggregator](https://www.catalogueau.com/sales/?stores=Woolworths) <br>
- [Current Specials Woolworths weekly catalogue](https://currentspecials.com.au/woolworths-weekly-catalogue/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown tables, JSON summaries, shell commands, and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on current supermarket websites, third-party aggregator availability, and local Puppeteer execution.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
