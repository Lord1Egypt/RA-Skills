## Description: <br>
Safe Smart Web Fetch helps an agent fetch web pages while routing sensitive, private, local, or non-HTTP URLs through direct fetching and using third-party cleanup services only for ordinary public pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zqh2333](https://clawhub.ai/user/zqh2333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve web content with conservative handling for private URLs, token-bearing links, local hosts, and non-HTTP inputs. It is suited for fetching public pages as cleaned Markdown while avoiding third-party cleanup services for links that may expose sensitive information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ordinary public URLs may be sent to external cleanup services. <br>
Mitigation: Use the skill only for public pages, or modify the workflow to require explicit approval or force direct fetch only. <br>
Risk: Confidential links, private documents, invite or reset URLs, and URLs with identifiers could expose sensitive information if misclassified. <br>
Mitigation: Avoid using the skill for these URLs unless the workflow is modified to require explicit approval or direct fetching only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zqh2333/safe-smart-web-fetch) <br>
- [Publisher profile](https://clawhub.ai/user/zqh2333) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON containing fetched page content, source, third-party-use flag, blocked reason, and errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Jina Reader, markdown.new, or defuddle.md for ordinary public pages; sensitive or private-looking URLs are fetched directly without third-party cleanup.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
