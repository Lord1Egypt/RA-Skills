## Description: <br>
Performs AI analysis on input video clips/image content and generates a smooth, natural scene description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to send clear images, videos, local files, or media URLs to a cloud visual analysis service for scene summaries, object and behavior recognition, OCR-style text extraction, structured reports, report links, and historical report lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images, videos, URLs, and identity-linked request data are sent to configured Life Emergence cloud services for analysis. <br>
Mitigation: Use the skill only with media that may be processed by that service, and avoid private or sensitive media unless the data flow is acceptable. <br>
Risk: The skill may create or reuse a local identity and persist backend tokens in a workspace SQLite database. <br>
Mitigation: Review local workspace data handling before installation, restrict workspace access, and remove stored local identity or token data when it is no longer needed. <br>
Risk: Historical report listing depends on cloud API results tied to the resolved identity. <br>
Mitigation: Confirm the active identity context before requesting history, and treat returned report links as identity-associated data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-visual-summary-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Analysis API Error Codes](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON-like structured text, with optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured analysis content, report export links, and historical report lists returned from the configured cloud API.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
