## Description: <br>
Guides an agent to use the Xianchou CLI for Markdown/MDX image insertion, AI image generation, AI video generation, model discovery, task polling, and Xianchou upload workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[starlying](https://clawhub.ai/user/starlying) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and content authors use this skill to configure and run Xianchou CLI commands that generate images or videos, upload local media, and insert generated assets into Markdown or MDX documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown-derived content and reference media may be uploaded to Xianchou's remote AI media service, and returned asset URLs may be public. <br>
Mitigation: Do not pass private images, videos, audio, or sensitive Markdown content unless remote upload and public asset URLs are acceptable. <br>
Risk: Using Markdown image generation with write-back can modify source Markdown or MDX files. <br>
Mitigation: Review generated changes before using or accepting commands that include --write. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/starlying/xianchou) <br>
- [Xianchou Homepage](https://xianchou.com) <br>
- [Xianchou CLI npm Package](https://www.npmjs.com/package/@xianchou/cli) <br>
- [CLI Command Guide](references/cli-command-guide.md) <br>
- [API Generation Guide](references/api-generation-guide.md) <br>
- [Markdown Image Guide](references/markdown-image-guide.md) <br>
- [API Contract Guide](references/api-contract-guide.md) <br>
- [Common Pitfalls](references/common-pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose CLI commands that upload local files, poll remote tasks, download generated assets, or write changes to Markdown/MDX files when explicitly requested.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
