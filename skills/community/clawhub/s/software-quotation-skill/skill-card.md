## Description:

Helps agents clarify software project requirements, break work into modules and role-based effort estimates, and produce polished HTML quotation documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horisony](https://clawhub.ai/user/horisony)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert software project requirements into structured scope questions, effort breakdowns, milestone plans, pricing tables, and client-ready quotation material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated quotation HTML loads unverified third-party PDF-export scripts that could access sensitive pricing or contract content in the browser.

Mitigation: Use the skill only with data appropriate for third-party browser libraries, or revise generated HTML to bundle libraries locally or add verified SRI and a restrictive CSP before handling confidential material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horisony/skills/software-quotation-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/horisony)
- [html2canvas 1.4.1 on cdnjs](https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js)
- [jsPDF 2.5.1 on cdnjs](https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Conversational guidance plus single-file HTML quotation documents with embedded CSS and JavaScript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include role-by-role effort matrices, pricing summaries, milestones, payment terms, and PDF export controls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
