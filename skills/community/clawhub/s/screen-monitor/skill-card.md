## Description:

Dual-mode screen sharing and analysis. Model-agnostic (Gemini/Claude/Qwen3-VL).

This skill is ready for commercial/non-commercial use.

## Publisher:

[emasoudy](https://clawhub.ai/user/emasoudy)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to share a browser or desktop view with a vision-capable agent for screen analysis, UI debugging, and visual checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screen frames can expose sensitive information if used on untrusted networks or sensitive displays.

Mitigation: Use only on trusted networks and non-sensitive screens unless local-only binding, authentication, upload limits, and protected session cleanup are added.

Risk: Capture cadence, retention, and OS screenshot fallback behavior may be unclear to users.

Mitigation: Clearly disclose capture cadence and retention, confirm or remove OS screenshot fallback, and clean up per-session frame files.

## Reference(s):

- [Screen Monitor ClawHub Page](https://clawhub.ai/emasoudy/skills/screen-monitor)
- [backend-endpoint.js](references/backend-endpoint.js)
- [env-check.sh](references/env-check.sh)
- [get-share-url.sh](references/get-share-url.sh)
- [screen-analyze.sh](references/screen-analyze.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command snippets and text analysis prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a vision-capable model and user-initiated screen sharing.]

## Skill Version(s):

1.0.1 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
