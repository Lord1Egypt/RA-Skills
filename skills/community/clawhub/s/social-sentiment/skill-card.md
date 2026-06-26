## Description: <br>
Social Sentiment guides agents through collecting and analyzing public posts from Twitter, Reddit, and Instagram to monitor brand and product sentiment, reputation themes, and potential PR issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atyachin](https://clawhub.ai/user/atyachin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External brand, marketing, product, and market-research teams use this skill to query social platforms, export large post datasets, classify sentiment, identify themes, and summarize high-engagement complaints or praise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Xpoz authorization and the mcporter npm binary introduce account-access and package-trust exposure. <br>
Mitigation: Authorize only the intended Xpoz account, install mcporter from a trusted registry source, and keep access scoped through the xpoz-setup workflow. <br>
Risk: Exported social posts may contain personal or sensitive data. <br>
Mitigation: Keep searches narrow, store CSV exports in protected locations, and delete or aggregate raw exports when they are no longer needed. <br>
Risk: Keyword-based sentiment scoring can misclassify context, sarcasm, or domain-specific language. <br>
Mitigation: Review representative samples and customize positive and negative keyword lists before relying on reports for decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/atyachin/social-sentiment) <br>
- [Xpoz](https://xpoz.ai) <br>
- [Publisher Profile](https://clawhub.ai/user/atyachin) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, markdown, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses mcporter, Xpoz account authorization, network access to mcp.xpoz.ai, and optional CSV exports for pandas analysis.] <br>

## Skill Version(s): <br>
1.4.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
