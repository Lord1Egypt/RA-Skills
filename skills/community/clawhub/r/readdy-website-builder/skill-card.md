## Description: <br>
Provides CLI-based website creation, modification, preview, publishing, deletion, and project management through the Readdy.ai platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankready2025](https://clawhub.ai/user/frankready2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to create, modify, preview, publish, list, update, and delete Readdy.ai website projects from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Website prompts and project context may be sent to Readdy.ai. <br>
Mitigation: Use the skill only when external processing by Readdy.ai is intended, and avoid including secrets or sensitive business data in prompts. <br>
Risk: Broad website requests may trigger this skill even when the user expects a local or different website-building workflow. <br>
Mitigation: Confirm that Readdy.ai is the intended destination before using the skill for generic create, modify, or publish requests. <br>
Risk: Ambiguous modification requests may proceed without enough clarification. <br>
Mitigation: Ask clarifying questions for unclear project IDs, target pages, publish versions, or requested changes before running Readdy.ai commands. <br>
Risk: The skill requires a sensitive Readdy API key. <br>
Mitigation: Configure the API key only on trusted systems and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [Readdy API Reference](references/API.md) <br>
- [Readdy.ai Homepage](https://readdy.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/frankready2025/readdy-website-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Readdy.ai project links or status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require long-running Readdy.ai operations and a configured API key.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
