## Description: <br>
Estimate exterior cleaning services for Rolling Suds from a U.S. residential property address using public property information, attached exterior photos, map/listing context, and a fixed pricing rubric for power washing and window cleaning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mwdearing](https://clawhub.ai/user/mwdearing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Rolling Suds salespeople use this skill to turn residential addresses, photos, and public property details into practical exterior-cleaning estimate ranges before entering final pricing into Workiz. <br>

### Deployment Geography for Use: <br>
St. Louis, Missouri metro area within a 50-mile service radius <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process customer lead numbers, home addresses, exterior photos, and public property details. <br>
Mitigation: Handle inputs as customer information and share them only with approved agents, tools, and workflows. <br>
Risk: Public property data, listing photos, map imagery, and user-provided photos may be incomplete or conflicting. <br>
Mitigation: State assumptions clearly, ask for photos or measurements when confidence is low, and use conservative ranges. <br>
Risk: The estimate could be mistaken for final pricing. <br>
Mitigation: Keep the estimate-only disclaimer and require salesperson review before entering final pricing into Workiz. <br>


## Reference(s): <br>
- [Pricing Rules](references/pricing-rules.md) <br>
- [Version History](references/version-history.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mwdearing/residential-property-rolling-suds-estimator) <br>
- [Publisher Profile](https://clawhub.ai/user/mwdearing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown estimate with property summary, service line items, estimate range, follow-up notes, and disclaimer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a lead number before estimating and treats all pricing as estimate-only pending salesperson review.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
