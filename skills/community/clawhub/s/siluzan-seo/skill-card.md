## Description: <br>
Siluzan SEO helps agents generate schema-valid structured JSON packages for industrial B2B SEO landing pages, blog articles, and backlink articles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sigedev01-bit](https://clawhub.ai/user/sigedev01-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and SEO operators use this skill to route industrial B2B SEO requests into the correct schema-backed workflow and produce JSON packages for CMS or website ingestion. It also guides optional DOCX or PDF exports when a human-readable review copy is requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can make broad global changes to the local agent environment. <br>
Mitigation: Review the install scripts before running them, prefer manual npm installation from a registry you trust, avoid one-line curl or iex installers, and use a scoped init target instead of --global --force when possible. <br>
Risk: Generated SEO content may include testimonials or review-like claims that are not supported by source material. <br>
Mitigation: Require source-backed customer evidence for testimonials and remove reviews, customer names, certifications, or order claims unless they are verified in the provided knowledge base. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/sigedev01-bit/skills/siluzan-seo) <br>
- [Setup guide](references/setup.md) <br>
- [Export guide](references/export.md) <br>
- [Traffic page output schema](seo-traffic-page/schemas/output.json) <br>
- [Blog article output schema](blog/schemas/output.json) <br>
- [Backlink article output schema](backlink-article/schemas/output.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Schema-valid JSON with plain-text content fields, plus optional shell commands for installation and DOCX or PDF export.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs target the bundled schemas for traffic pages, blog SEO packages, and backlink SEO packages; blog and backlink outputs may include Chinese summary or audit fields where required by the schema.] <br>

## Skill Version(s): <br>
1.1.30 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
