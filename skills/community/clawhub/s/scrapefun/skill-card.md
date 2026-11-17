## Description:

Use this skill when OpenClaw needs to operate a scrapefun server through dedicated OpenClaw-facing APIs, preferring /api/openclaw/* query and download endpoints while limiting generic scrapefun API fallbacks to documented cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoweili97](https://clawhub.ai/user/haoweili97)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage a local scrapefun/OpenClaw server through authenticated operational APIs for library lookup, media state checks, download submission, landed-file confirmation, import finalization, and explicit library scans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broadly scoped OpenClaw access key could allow media download, import, or library-scan state changes beyond the intended workflow.

Mitigation: Use an access key limited to the documented permissions and review requests that require download_submit, import_finalize, or library_scan before execution.

Risk: Running the skill against an untrusted or uncontrolled scrapefun/OpenClaw server could expose credentials or alter an unexpected media library.

Mitigation: Install and use the skill only with a scrapefun/OpenClaw server the operator controls.

Risk: Legacy fallback endpoints can behave differently from the dedicated OpenClaw API surface.

Mitigation: Prefer /api/openclaw/* endpoints and use generic scrapefun APIs only for the documented narrow fallback cases.

## Reference(s):

- [API Reference](references/api.md)
- [ScrapeFun skill page](https://clawhub.ai/haoweili97/skills/scrapefun)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with endpoint, permission, payload, and result or blocker details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Functional responses only; outputs may include authentication method, API endpoint, required permission, payload shape, returned result, and exact blocker.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
