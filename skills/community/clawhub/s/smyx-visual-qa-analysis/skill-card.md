## Description: <br>
Conducts open-ended visual question answering over image content using computer vision and large language models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask natural-language questions about image content, receive structured VQA answers, and retrieve cloud-hosted history or report links for prior analyses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads user-provided images, videos, and questions to the publisher's cloud service. <br>
Mitigation: Use it only for media that is approved for third-party cloud processing, and avoid private, regulated, or sensitive content unless retention and publisher controls have been reviewed. <br>
Risk: The skill creates or reuses an internal cloud-linked user identity and stores tokens locally. <br>
Mitigation: Run it in a workspace where local token storage is acceptable, restrict workspace access, and clear local state when the identity should not persist. <br>
Risk: History and report-link features can expose prior cloud analyses beyond the current image question. <br>
Mitigation: Review history output before sharing it and ensure that generated report links are appropriate for the audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-visual-qa-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API interface documentation](artifact/references/api_doc.md) <br>
- [Analysis API error reference](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-formatted analysis text, with optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include cloud report links and history tables when history lookup is requested.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata; artifact frontmatter says 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
