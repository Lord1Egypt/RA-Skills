## Description: <br>
Scan reagent barcodes or IDs, log expiration dates, and generate multi-level alerts before reagent expiry to support laboratory inventory management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Laboratory staff and inventory managers use this skill to log reagent IDs, expiration dates, locations, and quantities, then check for expired or soon-to-expire reagents. It supports inventory review and reorder planning, not safety assessment, controlled substance tracking, disposal guidance, or chain-of-custody inventory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local reagent inventory details may include lab-sensitive operational data. <br>
Mitigation: Confirm local storage is acceptable for the lab before running the skill, and record only the reagent IDs, dates, locations, and quantities needed for expiry tracking. <br>
Risk: Expiry alerts and reorder recommendations could be mistaken for regulated inventory, hazardous disposal, safety assessment, or chain-of-custody guidance. <br>
Mitigation: Use the skill only for expiry tracking, and route controlled substances, hazardous materials, disposal decisions, and formal compliance inventory to approved lab systems and personnel. <br>
Risk: Incorrect or fabricated expiry dates can lead to poor inventory decisions. <br>
Mitigation: Verify reagent IDs and expiration dates against labels or inventory records, and leave missing dates unresolved rather than guessing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/reagent-expiry-alert) <br>
- [Skill definition](SKILL.md) <br>
- [Polish changelog](POLISH_CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with command examples and structured reagent alert reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local JSON reagent inventory file when the packaged script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
