## Description:

Helps agents research TikTok video examples through Qinghu data APIs and turn high-performing samples, video details, and comments into reusable shooting scripts and content templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agents use this skill to find validated TikTok video samples, analyze hooks, structure, selling points, and comment themes, then produce practical shooting scripts and content templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Qinghu API tokens and request details may be exposed to the external Qinghu service.

Mitigation: Use a scoped Qinghu token, prefer environment variables or approved secret handling, and review requests before authorizing calls.

Risk: Qinghu API calls may consume credits.

Mitigation: Confirm the planned tool calls with the user before the first call, limit calls to the task, and report actual Qinghu credit consumption from the response envelope.

Risk: Copied TikTok assets or overly close reuse of another creator's video may create infringement or platform-enforcement risk.

Mitigation: Use the skill output as structural guidance, then create original footage, wording, and creative execution.

Risk: API wrapper responses can make failed or incomplete calls look successful if only the HTTP status or top-level error flag is checked.

Mitigation: Validate the protocol layer, result error flag, and parsed inner JSON success fields before relying on returned data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-tiktok-video-clone)
- [ClawHub publisher profile](https://clawhub.ai/user/autoagc)
- [Qinghu MCP API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API keys dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with structured sample lists, breakdown tables, shooting scripts, JSON-RPC examples, and optional exported spreadsheet files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user authorization and a Qinghu API token before external API calls; calls may consume Qinghu credits and send request details to Qinghu.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
