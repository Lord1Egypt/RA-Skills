## Description:

QA Architecture Auditor performs static, zero-trust codebase analysis and generates QA and testing strategy reports covering risk assessment, security surface mapping, methodology-specific test plans, tooling recommendations, and compliance controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shifulegend](https://clawhub.ai/user/shifulegend)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA architects, security auditors, and engineering teams use this skill to build an independent testing strategy for a local or authorized remote code repository. It is suited for planning from-scratch QA coverage, security review focus areas, compliance control checks, and tooling recommendations before implementation or system transition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted repository content can influence generated report HTML.

Mitigation: Analyze only trusted repositories, prefer Markdown output, or sanitize generated HTML before opening it in a browser.

Risk: Repository analysis may read outside the selected folder.

Mitigation: Run the skill in a sandbox or container with read-only access limited to the intended target repository.

Risk: The implementation may not match advertised remote git, security-scan, or max-depth behavior.

Mitigation: Validate or fix those behaviors before relying on them for security-sensitive review.

Risk: HTML output also creates an extra sibling Markdown file.

Mitigation: Account for the additional Markdown artifact when choosing output paths and reviewing generated files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shifulegend/skills/qa-architecture-auditor)
- [Testing Methodologies Reference](references/methodologies.md)
- [Risk Assessment and Vulnerability Patterns](references/risk-assessment.md)
- [Tooling Recommendations Matrix](references/tooling-matrix.md)
- [Compliance Frameworks Reference](references/compliance-frameworks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance, files]

**Output Format:** [HTML or Markdown report files with risk tables, testing matrices, control checklists, recommendations, and example test cases.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When HTML output is selected, the artifact behavior also writes a sibling Markdown report file.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
