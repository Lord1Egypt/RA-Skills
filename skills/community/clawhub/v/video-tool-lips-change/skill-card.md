## Description: <br>
Lip-sync an existing HTTPS video to a separate audio URL via WeryAI (video-lips-change). Use when the user wants lip sync to new audio, not text-to-video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run WeryAI lips-change jobs that sync an existing public HTTPS video to a separate public HTTPS audio URL. It is intended for URL-based lip-sync workflows, not local file uploads, text-to-video generation, or face replacement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends user-provided video and audio URLs to WeryAI for processing. <br>
Mitigation: Use only public HTTPS media URLs the user is comfortable sharing with WeryAI, avoid signed or credential-bearing URLs when possible, and run in a trusted environment. <br>
Risk: Paid WeryAI runs may be submitted when the agent executes submit or wait. <br>
Mitigation: Use dry-run first and require explicit user confirmation of both URLs before starting a paid job. <br>
Risk: The WERYAI_API_KEY credential is required at runtime. <br>
Mitigation: Provide WERYAI_API_KEY only through the runtime environment and do not write it into files or prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/video-tool-lips-change) <br>
- [WeryAI llms.txt](https://docs.weryai.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON, markdown] <br>
**Output Format:** [Markdown guidance with shell commands, JSON request payloads, and final result links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, public HTTPS media URLs, and user confirmation before paid submit or wait runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
