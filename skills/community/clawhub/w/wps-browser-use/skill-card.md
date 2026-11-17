## Description:

Browser Use lets agents navigate websites, interact with indexed page elements, run page JavaScript, take screenshots, and return structured text snapshots when search results are insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihaha123123123123](https://clawhub.ai/user/xixihaha123123123123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and text-only agents use this skill to supplement search with browser navigation, site search, form interaction, and dynamic page inspection. It is intended for tasks where public search summaries are missing, stale, incomplete, or a specific website or logged-in workflow must be inspected with user supervision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can run arbitrary JavaScript in the active page context through execute_script.

Mitigation: Install only for agents trusted to control the browser session, and restrict or remove execute_script when page-script execution is not required.

Risk: Screenshot output can write files to caller-provided paths.

Mitigation: Confine screenshot output to a dedicated workspace directory and review generated files before sharing them.

Risk: Browser automation can operate on sensitive logged-in sites.

Mitigation: Avoid sensitive logged-in sites unless explicitly needed, and keep user supervision for authentication, CAPTCHA, or manual steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixihaha123123123123/skills/wps-browser-use)
- [Publisher profile](https://clawhub.ai/user/xixihaha123123123123)

## Skill Output:

**Output Type(s):** [text, files, code, guidance]

**Output Format:** [Structured plain-text browser snapshots with optional PNG screenshots and saved text overflow files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Page text above 10000 characters and interactive element lists above 100 entries are truncated in the snapshot, with overflow saved to a workspace file when possible.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
