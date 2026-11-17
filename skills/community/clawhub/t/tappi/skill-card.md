## Description:

tappi provides lightweight Chrome DevTools Protocol browser control for AI agents, with token-efficient commands for opening pages, clicking elements, filling forms, uploading files, extracting page content, and reusing signed-in Chrome or Chromium sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaihazher](https://clawhub.ai/user/shaihazher)

### License/Terms of Use:


## Use Case:

Developers and agent operators use tappi to let an agent drive a local Chrome or Chromium browser through compact CLI commands for browsing, form interaction, page extraction, file upload, screenshots, and canvas-style keyboard input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents receive broad control over a signed-in browser session.

Mitigation: Install only when that level of browser control is acceptable, and require explicit user confirmation before use on authenticated sites, payment or OAuth flows, captchas, or destructive actions.

Risk: Sensitive commands can run raw JavaScript, upload files, paste from local files, or click page coordinates.

Mitigation: Treat eval, upload, paste-from-file, and click-xy as privileged operations; confirm the target page, action, and local file path before execution.

Risk: The packaged ws dependency may need review before sensitive deployment.

Mitigation: Review or update the ws dependency before relying on the skill in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaihazher/skills/tappi)
- [ws 8.19.0 package artifact](https://registry.npmjs.org/ws/-/ws-8.19.0.tgz)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; browser command responses are compact plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns indexed browser elements and concise page output; artifact documentation states text extraction is capped at 8KB and HTML extraction at 10KB.]

## Skill Version(s):

3.5.0 (source: server release metadata; artifact _meta.json reports 3.2.0 and scripts/package.json reports 1.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
