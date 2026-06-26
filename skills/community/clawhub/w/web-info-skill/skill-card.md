## Description: <br>
Extract and display useful information from web pages including title, meta description, headers, and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sangjie123](https://clawhub.ai/user/sangjie123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch public web pages and extract page titles, descriptions, headings, links, image alt text, and approximate word counts for quick inspection or downstream parsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make outbound HTTP(S) requests from the agent environment to user-provided URLs. <br>
Mitigation: Use it only in environments where outbound web requests are acceptable, and provide only URLs the operator intends to fetch. <br>
Risk: The release claims public-only and robots.txt protections that the security review says are not enforced. <br>
Mitigation: Do not rely on those protections unless the skill is updated to enforce them; apply network controls or manual review for sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sangjie123/web-info-skill) <br>
- [OpenClaw homepage](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Plain text summaries or JSON objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes extracted webpage metadata, headings, links, image alt text, and word count when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
