## Description: <br>
Buy and resell on Vinted with listing systems, price discipline, shipping workflows, and trust-first handling for offers, bundles, and disputes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to structure Vinted buying, casual selling, and Pro resale workflows, including sourcing decisions, listing quality, pricing discipline, shipping proof, bundles, offers, and dispute handling. It is intended to provide action plans and guardrails while requiring user confirmation before marketplace actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local notes under ~/vinted/ may contain closet, pricing, shipping, and incident details. <br>
Mitigation: Ask for permission before enabling persistence and store only durable marketplace context the user approves. <br>
Risk: Marketplace buying, selling, shipping, and dispute workflows can affect money, account standing, or buyer-seller trust. <br>
Mitigation: Keep payments, labels, and disputes inside Vinted rules and require explicit confirmation before irreversible marketplace actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/vinted) <br>
- [Skill Homepage](https://clawic.com/skills/vinted) <br>
- [Vinted Marketplace](https://www.vinted.com) <br>
- [Vinted Pro Portal](https://pro-portal.svc.vinted.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists, decision templates, and local note templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local notes under ~/vinted/ and should require explicit user confirmation before marketplace actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
