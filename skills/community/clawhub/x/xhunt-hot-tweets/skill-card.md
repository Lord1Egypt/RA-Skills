## Description: <br>
Fetches XHunt X/Twitter trend rankings and returns tweet links, Chinese one-line summaries, and engagement data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DoTheWorkNow](https://clawhub.ai/user/DoTheWorkNow) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to quickly review XHunt hot tweet rankings for global or Chinese-language groups, especially AI topics. It produces links, concise Chinese summaries, engagement metrics, and short observations for trend review or content planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on contacting trends.xhunt.ai, so results can fail or become incomplete if network access is unavailable or the page structure changes. <br>
Mitigation: Use the skill only in environments where access to trends.xhunt.ai is acceptable, and review output for missing fields or the documented fallback and failure notices. <br>
Risk: The skill summarizes public X/Twitter trend content, which may include political or controversial posts when unrestricted mode is used. <br>
Mitigation: Choose the AI-product-only filtering mode when controversial or off-topic trend content is not appropriate for the workflow. <br>


## Reference(s): <br>
- [XHunt Trends](https://trends.xhunt.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/DoTheWorkNow/xhunt-hot-tweets) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown-style text with ranked tweet links, Chinese summaries, engagement metrics, and observations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs Chinese summaries by default and uses NA for missing engagement fields.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata, frontmatter, and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
