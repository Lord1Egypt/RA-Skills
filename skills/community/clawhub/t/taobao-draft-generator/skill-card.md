## Description: <br>
Generates Taobao product listing drafts from manually prepared product data, with human confirmation before draft creation and no automatic publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guowaa223](https://clawhub.ai/user/guowaa223) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce operators use this skill to turn manually prepared Taobao product information into a draft listing JSON file and an Excel final-review sheet for human review before manual publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overstate compliance checks for title originality, forbidden words, material consistency, category, price, and stock. <br>
Mitigation: Treat outputs as draft formatting aids and manually verify all compliance-sensitive fields before publishing. <br>
Risk: Unsafe product IDs can cause files to be read or written outside the intended product folder. <br>
Mitigation: Use simple product IDs without slashes, parent-directory segments, or path traversal characters, and run the skill in a controlled workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guowaa223/taobao-draft-generator) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Usage guide](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, JSON, Spreadsheet] <br>
**Output Format:** [Console text plus generated JSON draft and Excel audit workbook] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a product ID and explicit human confirmation; writes local draft and audit output files.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
