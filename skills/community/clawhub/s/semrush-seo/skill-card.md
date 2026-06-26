## Description: <br>
Semrush SEO integration with API key authentication. Analyze backlinks, keyword rankings, competitor domains, traffic metrics, and SEO data across organic and paid search channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, SEO practitioners, and developers use this skill to query Semrush analytics through ClawLink for keyword research, backlink review, competitor analysis, traffic metrics, and account unit checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting a Semrush API key through ClawLink. <br>
Mitigation: Install only when comfortable using ClawLink for credential handling, and avoid pasting API keys into chat. <br>
Risk: Semrush requests can consume paid API units, especially large batches. <br>
Mitigation: Check the account API unit balance before large runs and limit batch size to the needed scope. <br>
Risk: CSV-like Semrush responses can be misread if parsed as JSON or split without respecting delimiters. <br>
Mitigation: Parse responses with delimiter-aware logic and cast numeric fields before analysis. <br>


## Reference(s): <br>
- [ClawHub Semrush skill](https://clawhub.ai/hith3sh/semrush-seo) <br>
- [Semrush API Documentation](https://developers.semrush.com/api/) <br>
- [Semrush Domain Analytics](https://www.semrush.com/domain-analytics/) <br>
- [Semrush Keyword Research](https://www.semrush.com/keyword-research/) <br>
- [Semrush Backlink Analytics](https://www.semrush.com/backlinks/) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and CSV-like Semrush response handling notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Semrush tool responses are described as CSV-like strings that may need delimiter-aware parsing.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
