## Description: <br>
Smartlib Citation Checker Clawhub helps agents verify whether paper references or AI-generated citations are real, compare them with SmartLib records, and produce HTML citation-check reports with corrections, verification links, and citation analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j-levee](https://clawhub.ai/user/j-levee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, authors, editors, and developers use this skill to check reference lists, paper drafts, BibTeX entries, and AI-generated citations for authenticity and formatting issues before relying on or submitting them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Citation text and an email address may be sent to SmartLib/VIP Smart services. <br>
Mitigation: Use the skill only with citation data and account identifiers that are approved for external processing, especially for unpublished or confidential drafts. <br>
Risk: The skill uses a shared SmartLib quota and account flow. <br>
Mitigation: Confirm which email and quota account are active before running citation checks or payment-related flows. <br>
Risk: Corrected bibliography exports can still require human judgment. <br>
Mitigation: Treat corrected references, fuzzy matches, and not-found results as review material and verify important citations before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j-levee/skills/smartlib-citation-checker) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/j-levee) <br>
- [SmartLib / VIP Smart homepage](https://www.vipslib.com) <br>
- [Artifact README](artifact/README.md) <br>
- [Paper draft sample report](artifact/examples/citation_check_paper_draft_sample.html) <br>
- [AI hallucination sample report](artifact/examples/citation_check_ai_hallucination_sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, HTML, markdown, configuration, guidance] <br>
**Output Format:** [HTML reports with corrected citation text, verification links, tabbed citation formats, statistics, and concise agent guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SmartLib Gateway environment configuration and may request a user email for quota management before citation checks.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release metadata; artifact frontmatter reports 3.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
