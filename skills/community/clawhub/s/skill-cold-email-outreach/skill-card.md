## Description: <br>
Automates B2B cold email outreach by sourcing Apollo leads, verifying addresses with Hunter.io, and uploading verified contacts to an Instantly campaign. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, growth, and revenue operations users can use this skill to turn Apollo lead exports into verified Instantly campaign leads with basic personalization and a three-email outreach sequence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send contact data to third-party services and bulk add leads to an outreach campaign with little built-in review. <br>
Mitigation: Review the CSV, target campaign, and applicable permission to contact leads before running the upload. <br>
Risk: Hunter.io and Instantly API keys are required for normal operation. <br>
Mitigation: Keep API keys out of shared files and logs, use a local config file, and rotate keys if they are exposed. <br>
Risk: Bulk uploads can affect a live outreach campaign. <br>
Mitigation: Test with a small CSV first and add a dry-run or confirmation step before importing larger lead lists. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-cold-email-outreach) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown instructions and Node.js command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes CSV lead data, verifies email status through Hunter.io, and uploads verified leads to Instantly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
