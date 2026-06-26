## Description: <br>
Checks academic references in AI-generated content by validating citation authenticity, assessing topical relevance, generating corrected BibTeX and APA citations, recommending replacement literature, and optionally matching uploaded PDFs against in-text citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[793943403](https://clawhub.ai/user/793943403) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical writers use this skill to audit generated bibliographies, identify hallucinated or questionable academic references, repair citation formatting, and find credible replacement papers. When a PDF is available, it can guide an agent to compare in-text citations with the reference list and produce a mismatch report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to query external academic services or process uploaded PDF content. <br>
Mitigation: Avoid confidential, unpublished, regulated, or student-identifiable documents unless external lookup and PDF-processing exposure is acceptable. <br>
Risk: Academic metadata lookup results can be incomplete, unavailable, or mismatched to malformed references. <br>
Mitigation: Review final citation decisions against DOI records or publisher pages before using them in submitted work. <br>
Risk: PDF parsing can fail or miss citation markers in complex documents. <br>
Mitigation: Provide a text version or key page ranges when PDF matching is incomplete, and treat the generated report as review guidance. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown tables, citation text, BibTeX entries, APA 7th citations, replacement recommendations, and PDF citation-match reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include verification status, DOI, author, year, abbreviated title, relevance rating, core abstract, action recommendation, and batch-processing notes.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
