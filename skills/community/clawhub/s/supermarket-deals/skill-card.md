## Description: <br>
Searches German supermarket flyers for product deals via Marktguru and ranks results by best price per litre (EUR/L). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benmillerat](https://clawhub.ai/user/benmillerat) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to search current German supermarket flyers by product, postal code, and store, then rank deals by price per litre for summaries or scheduled notifications. <br>

### Deployment Geography for Use: <br>
Germany <br>

## Known Risks and Mitigations: <br>
Risk: Product searches and German postal codes are sent to Marktguru to retrieve supermarket flyer results. <br>
Mitigation: Use only searches and postal codes that are acceptable to share with Marktguru, and review third-party data handling requirements before deployment. <br>
Risk: Marktguru keys and user preferences are cached locally under ~/.supermarket-deals. <br>
Mitigation: Remove ~/.supermarket-deals when the skill is no longer used and apply normal local file permission controls for shared systems. <br>
Risk: The skill requires local npm setup and build steps. <br>
Mitigation: Run npm setup as a non-administrator user and follow the security guidance to avoid elevated installation privileges. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/benmillerat/supermarket-deals) <br>
- [Marktguru](https://www.marktguru.de) <br>
- [Marktguru offer search endpoint](https://api.marktguru.de/api/v1/offers/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text tables or structured JSON from a CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include product descriptions, stores, size, price, EUR/L ranking, validity dates, and direct Marktguru offer URLs.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
