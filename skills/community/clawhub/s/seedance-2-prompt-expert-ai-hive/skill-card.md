## Description:

This skill helps AI video creators, advertising directors, and ecommerce content teams turn Seedance 2.0 creative goals and authorized materials into structured prompts, shot plans, runnable AI-HIVE commands, and acceptance checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External AI video creators, advertising directors, and ecommerce content teams use this skill to convert campaign goals, product facts, channel constraints, and authorized references into Chinese video production blueprints, Seedance 2.0 prompts, AI-HIVE generation commands, task records, and review checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API keys and stores a local credential for later use.

Mitigation: Use a dedicated API key, keep the local configuration file private, rotate the key if exposed, and avoid pasting real credentials into chat logs or shared files.

Risk: The helper can submit paid remote generation jobs after confirmation.

Mitigation: Review prompts, model mode, routing, pricing snapshot, and batch size before execution; run a small sample before larger batches.

Risk: A custom AI-HIVE base URL can redirect requests and credentials to an untrusted endpoint.

Mitigation: Use the default AI-HIVE endpoint unless the alternative endpoint is fully trusted and controlled.

## Reference(s):

- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-2-prompt-expert-ai-hive)
- [Publisher profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured sections and inline bash commands; helper scripts can emit JSON files and task status JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local blueprint files, AI-HIVE media upload identifiers, generation task identifiers, downloaded media paths, and acceptance checklists when the user confirms execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
