## Description: <br>
Silver Daily helps agents generate a concise HTML daily briefing on the silver economy by collecting and summarizing news across policy, consumption, finance, technology, healthcare, culture, home care, and employment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnspica](https://clawhub.ai/user/cnspica) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, investors, and eldercare-industry practitioners use this skill to request a daily silver-economy news digest with source links and short summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web search results and source links can be stale, incomplete, or misleading. <br>
Mitigation: Review source links and dates before distributing the generated briefing. <br>
Risk: Pension, healthcare, and finance coverage may be mistaken for personal account support, medical advice, or investment advice. <br>
Mitigation: Use the briefing as general public information and confirm decisions with qualified or official sources. <br>
Risk: The skill saves an HTML report to local storage. <br>
Mitigation: Provide an explicit output path when location or retention matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cnspica/silver-daily) <br>
- [Content Framework](references/content_framework.md) <br>
- [HTML Template](references/html_template.md) <br>
- [Output Format](references/output_format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [HTML report file plus concise text or Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves reports locally using the requested or default output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version and artifact/clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
