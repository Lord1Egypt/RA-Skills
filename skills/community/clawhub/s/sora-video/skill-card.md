## Description: <br>
Generate, edit, extend, and manage AI videos using OpenAI's Sora 2 API with marketing-ready prompt templates for product demos, social ads, brand spots, and launch teasers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonathanlindsay](https://clawhub.ai/user/jonathanlindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, edit, extend, poll, download, list, and delete OpenAI Sora video jobs. It is especially oriented toward marketing workflows such as product demos, social ads, brand identity spots, launch teasers, and batch video variants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Sora operations can incur usage-based OpenAI API charges. <br>
Mitigation: Use dry-run mode while preparing prompts, monitor API spending, and run live generation only with an approved customer-provided OPENAI_API_KEY. <br>
Risk: Uploaded prompts or media may contain confidential information. <br>
Mitigation: Avoid uploading confidential media unless allowed by policy and review prompts and reference assets before submission. <br>
Risk: The delete command can remove a video job by ID. <br>
Mitigation: Confirm video IDs before running delete and prefer listing or status checks before destructive operations. <br>
Risk: Installing uv through a shell installer can introduce supply-chain risk. <br>
Mitigation: Install uv through a trusted package manager or review and verify the installer before running it. <br>


## Reference(s): <br>
- [Sora Video ClawHub release](https://clawhub.ai/jonathanlindsay/sora-video) <br>
- [CLI Reference](references/cli.md) <br>
- [Sora Video API quick reference](references/video-api.md) <br>
- [Prompting Guide](references/prompting.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [OpenAI API keys](https://platform.openai.com/api-keys) <br>
- [OpenAI API pricing](https://openai.com/api/pricing/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, CLI arguments, JSON request previews, and generated video asset files from the Sora API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live API calls require a customer-provided OPENAI_API_KEY and may create billable Sora jobs; dry-run mode can preview requests without an API call.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
