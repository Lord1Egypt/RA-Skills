## Description:

Creates AI-narrated film and drama commentary videos through narrator-ai-cli workflows for resource selection, script generation, dubbing, and video composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4myhime](https://clawhub.ai/user/4myhime)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and external creators use this skill to guide end-to-end narrated film or drama commentary video creation. It helps an agent choose materials, narration templates, BGM, and dubbing voices, then generate scripts and compose video outputs through the Narrator AI CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs remote executable code for narrator-ai-cli.

Mitigation: Review the external CLI source and pin installation to a reviewed commit or hashed artifact before use.

Risk: The skill can send media, subtitles, voice data, and generated content to the Narrator AI cloud service.

Mitigation: Use a dedicated environment and scoped API key, and avoid uploading sensitive, private, or copyrighted media unless cloud processing is acceptable.

Risk: The workflows include upload, URL transfer, deletion, account-key, voice clone, and budget-affecting operations.

Mitigation: Require explicit user confirmation before each upload, transfer, deletion, voice clone, account-key action, and budget estimate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/4myhime/skills/test-for-wang)
- [Narrator AI CLI repository](https://github.com/GridLtd-ProductDev/narrator-ai-cli)
- [Pinned narrator-ai-cli source archive](https://github.com/GridLtd-ProductDev/narrator-ai-cli/archive/refs/tags/v1.0.0.zip)
- [Narrator AI API endpoint](https://openapi.jieshuo.cn)
- [Narration resources preview](https://ceex7z9m67.feishu.cn/wiki/WLPnwBysairenFkZDbicZOfKnbc)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON]

**Output Format:** [Markdown guidance with bash and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent workflows may return Narrator AI task IDs, file IDs, generated narration text, audio results, and video download URLs.]

## Skill Version(s):

0.0.2 (source: ClawHub release metadata; artifact frontmatter and plugin.json list 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
