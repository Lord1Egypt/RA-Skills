## Description: <br>
智能摘要 summarizes long text, supported local documents, and web pages, and extracts core keywords with configurable summary length. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to summarize pasted text, supported local files, or web pages, and to extract keywords for faster review of content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local files selected by the user, so sensitive documents may be summarized or included in output. <br>
Mitigation: Only provide files intended for processing, and review generated summaries before sharing them. <br>
Risk: The skill can fetch URLs supplied by the user, including private, tokenized, localhost, intranet, or cloud metadata URLs. <br>
Mitigation: Avoid confidential or privileged URLs unless the user specifically intends the agent to process that content. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Plain text, Markdown, or JSON summaries and keyword lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summary length can be short, medium, or long; optional metadata may include source and word count.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
