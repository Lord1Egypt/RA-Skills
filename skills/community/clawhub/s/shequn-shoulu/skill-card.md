## Description: <br>
社群收录 guides community owners through structured intake, collects public community details, and prepares submissions for synchronization to an IMA knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingmuhuijianghu](https://clawhub.ai/user/qingmuhuijianghu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Community operators and directory maintainers use this skill to collect structured information from group owners for alumni, business association, enterprise, and interest communities. The skill helps gather public contact channels, format the submission as Markdown, mark it pending review, and submit it to an external IMA knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted community information is uploaded to an external IMA knowledge base and may later appear in related directories. <br>
Mitigation: Use the skill only for information intended for publication, keep submissions marked pending review, and review entries before making them visible. <br>
Risk: The broader workflow may involve publishing tools, platform credentials, or curl-to-bash installation steps beyond basic intake. <br>
Mitigation: Avoid those flows unless the publisher and destination services are separately trusted, and confirm what credentials are requested and where data will be posted. <br>
Risk: The artifact includes an automated upload path to an external service. <br>
Mitigation: Confirm user consent, inspect generated Markdown before upload, and restrict contact details to public channels such as official accounts or video accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingmuhuijianghu/shequn-shoulu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational text and Markdown with Python code and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces community intake prompts, structured submission content, and external knowledge-base upload guidance; submissions are marked pending review.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
