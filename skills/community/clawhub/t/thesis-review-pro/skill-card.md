## Description:

Thesis Review Pro helps agents review master's, doctoral, pre-review, and blind-review theses with a structured framework and generate Word-format review comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Academic reviewers and graduate-program staff use this skill to extract thesis details from PDFs, assess originality, methodology, experiments, writing quality, compare public literature, and generate structured Chinese review opinions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential or blind-review theses may expose author, school, academic-profile, or project details during PDF extraction and output generation.

Mitigation: For blind review or confidential theses, remove identifying pages first and request anonymized filenames and outputs.

Risk: Web search for literature comparison may disclose sensitive thesis topics or method keywords outside the local review workflow.

Mitigation: Use generalized search terms or skip external search when reviewing confidential or embargoed thesis material.

Risk: Generated review opinions can be incomplete, inaccurate, or overly decisive for academic evaluation.

Mitigation: Have a qualified reviewer verify factual claims, literature comparisons, scoring, and final recommendations before sharing or using them in an academic decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/thesis-review-pro)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Structured Chinese thesis review text with optional Word .docx output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PDF-derived thesis metadata, public-literature comparison notes, revision suggestions, reviewer questions, and batch comparison reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
