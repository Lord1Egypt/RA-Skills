## Description: <br>
Creates vertical three-beat debunk videos with timed English captions using WeryAI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to turn a topic or approved X/Y/Z concept set into a short vertical debunk-video workflow with prompt expansion, confirmation, and WeryAI generation commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid generation can consume WeryAI credits when submit or wait commands are run. <br>
Mitigation: Require explicit approval of the full parameter table and expanded prompt before any paid submit or wait operation. <br>
Risk: Using local image paths may upload local files to WeryAI. <br>
Mitigation: Prefer public HTTPS image URLs and use local image paths only after the user intentionally approves the upload. <br>
Risk: The WERYAI_API_KEY is a sensitive credential. <br>
Mitigation: Keep the key out of source control and use an isolated or short-lived environment for higher-assurance runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/think-x-actually-y-video-gen) <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with parameter tables, inline shell commands, task identifiers, status summaries, and video links when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY and Node.js 18+; generation is paid and network-dependent.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
