## Description: <br>
Extracts clean text from public web pages with r.jina.ai so an agent can summarize or analyze the core content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuxNd](https://clawhub.ai/user/kukuxNd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and general agent users use this skill to extract readable text from public articles, news pages, and blog posts before summarization or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private URLs, authenticated pages, token-bearing query strings, or sensitive page content could be shared with r.jina.ai and temporarily stored in local output files. <br>
Mitigation: Use the skill for public pages by default; avoid intranet, authenticated, private, or tokenized URLs unless that sharing and local storage are acceptable. <br>


## Reference(s): <br>
- [Web Extractor on ClawHub](https://clawhub.ai/kukuxNd/web-extractor) <br>
- [r.jina.ai extraction endpoint](https://r.jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and extracted text saved as local Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public page content through r.jina.ai and writes extracted content to /tmp/ by default; output paths can be customized.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
