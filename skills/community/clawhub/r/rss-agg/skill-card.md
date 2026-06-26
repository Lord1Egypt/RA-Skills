## Description: <br>
Parse, aggregate and process RSS/Atom feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to collect RSS or Atom feed items, filter them by keyword or date, and produce digests for monitoring, newsletters, or blog update workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched feed content is untrusted and may affect generated HTML or newsletter content. <br>
Mitigation: Use trusted feed URLs, review generated output before distribution, and avoid relying on generated digests for sensitive decisions. <br>
Risk: The release evidence notes that HTTPS certificate verification is weakened when feeds are fetched. <br>
Mitigation: Prefer trusted networks and update the fetch behavior to use normal TLS verification before using the script with untrusted feeds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/rss-agg) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command examples; generated feed outputs may be JSON, HTML, or Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Aggregated items include title, link, description, publication date, and feed source when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
