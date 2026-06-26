## Description: <br>
Search Google and get structured JSON results (web, news, images, maps). Use for any query requiring current web information or recent news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scavio-ai](https://clawhub.ai/user/scavio-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Google web, news, image, map, or lens searches through Scavio and return current, structured results with citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires SCAVIO_API_KEY, so use of the skill depends on a sensitive credential. <br>
Mitigation: Provide the key through the environment, avoid pasting it into prompts or outputs, and rotate it if it is exposed. <br>
Risk: The skill performs live web searches and may return incomplete, stale, or misleading external results. <br>
Mitigation: Use only returned URLs and snippets, cite sources when summarizing, and review results before relying on them for consequential decisions. <br>


## Reference(s): <br>
- [Scavio documentation](https://scavio.dev/docs) <br>
- [Scavio Google on ClawHub](https://clawhub.ai/scavio-ai/scavio-google) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown summaries and structured JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCAVIO_API_KEY. The skill documents a 90 second timeout and 1 request per second throttle.] <br>

## Skill Version(s): <br>
2.0.3 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
