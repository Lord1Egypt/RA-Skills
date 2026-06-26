## Description: <br>
Fetches public XHunt X/Twitter hot-tweet rankings and returns Chinese summaries with tweet links and engagement data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DoTheWorkNow](https://clawhub.ai/user/DoTheWorkNow) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect recent XHunt tweet rankings by region, time window, and tag, then receive shareable Chinese summaries with source links and interaction metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts trends.xhunt.ai and depends on public page availability and structure. <br>
Mitigation: Run it only in environments where outbound access to XHunt is acceptable, and treat degraded or failed fetch notices as limits on result completeness. <br>
Risk: Broad hot-tweet requests can include political or controversial content when filtering mode is all. <br>
Mitigation: Use the ai-product-only mode when users need AI product, model, or tool updates without unrelated political or entertainment content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/DoTheWorkNow/xhunt-hot-tweets-skill) <br>
- [XHunt trends](https://trends.xhunt.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style text containing ranked tweet URLs, one-line Chinese summaries, engagement statistics, and brief observations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses group, hours, tag, limit, and filtering mode parameters; missing fields are reported as NA rather than fabricated.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence; artifact frontmatter and changelog list 2.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
