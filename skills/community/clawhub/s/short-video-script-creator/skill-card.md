## Description: <br>
Creates short-video scripts from structured product, strategy, tone-reference, competitor, and historical-script inputs, with native PDF and Word input support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsbnb](https://clawhub.ai/user/ahsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, content creators, and agent operators use this skill to assemble reviewed parameters, read source documents, and generate batches of short-video scripts in Markdown that match a requested voice, content structure, and word-count range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a hard-coded API key. <br>
Mitigation: Remove and rotate the embedded key, then require user-supplied credentials or an approved secret store before use. <br>
Risk: The skill can send user document contents to an undisclosed external AI service. <br>
Mitigation: Use only documents approved for external processing, name the provider clearly, and require confirmation before any network transmission. <br>
Risk: The skill stores full prompts locally. <br>
Mitigation: Let users choose or clear the output directory and avoid storing sensitive source material in generated prompt files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahsbnb/short-video-script-creator) <br>
- [Configured external AI service endpoint](https://api2.aigcbest.top/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown scripts and local Markdown prompt/output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate multiple scripts per run and may read PDF, Word, Markdown, and text inputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact package.json declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
