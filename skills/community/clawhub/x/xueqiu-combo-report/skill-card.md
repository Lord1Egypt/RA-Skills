## Description:

Xueqiu Combo Report guides agents through collecting Xueqiu combo holdings from a logged-in browser session, merging and patching batches, ranking held stocks, and exporting JSON, Markdown, HTML, and PDF reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ning-kun](https://clawhub.ai/user/ning-kun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to turn Xueqiu self-selected combo holdings batches into ranked portfolio-style reports while documenting collection limits, failures, and manual patches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The collection workflow depends on a logged-in Xueqiu financial browser session.

Mitigation: Use only trusted sessions and trusted input files, keep browser-side fetches scoped to the intended Xueqiu holdings workflow, and review collected data before reporting.

Risk: Generated holdings reports may persist portfolio-style financial data.

Mitigation: Keep generated JSON, Markdown, HTML, and PDF reports out of shared or published repositories unless disclosure is intentional.

Risk: PDF generation currently involves unescaped report data and Chrome sandboxing concerns.

Mitigation: Avoid PDF generation until HTML escaping and Chrome sandboxing issues are fixed; prefer reviewed JSON, Markdown, or HTML outputs in the meantime.

## Reference(s):

- [End-to-end workflow](references/end-to-end.md)
- [Data formats](references/data-format.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, markdown, configuration]

**Output Format:** [Markdown guidance with bash and JavaScript snippets; generated report files may be JSON, Markdown, HTML, and PDF.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report generation depends on trusted input data, a logged-in Xueqiu browser session for collection, and Chrome or Chromium for optional PDF export.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
