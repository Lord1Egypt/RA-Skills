## Description: <br>
Keyword research and analysis skill for any website. Performs systematic keyword discovery, competitive gap analysis, intent classification, difficulty scoring, and priority ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meikidd](https://clawhub.ai/user/meikidd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, SEO specialists, and content teams use this skill to discover keyword opportunities, compare competitor coverage, classify search intent, and produce a prioritized keyword research report for a target website. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use logged-in SEO tools in the user's browser, including Google Search Console and other account-based services. <br>
Mitigation: Keep browser automation limited to the intended account and tab, and confirm access before extracting or using account-specific site data. <br>
Risk: The skill saves per-site business context locally in domain profile files. <br>
Mitigation: Review or delete saved domain profile files when that information should not be retained, and avoid storing sensitive business details unnecessarily. <br>
Risk: Some workflows can involve paid SEO tools or account tiers. <br>
Mitigation: Confirm the user's available account tier before using paid-tool workflows and use documented free alternatives when paid access is unavailable or undesired. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/meikidd/seo-keyword-research) <br>
- [GSC web UI playbook](references/gsc-operations.md) <br>
- [Keyword optimization methodology](references/methodology.md) <br>
- [Keyword research tools](references/tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with tables, prioritized recommendations, and supporting setup or browser-navigation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local per-domain JSON profile files to retain site context between runs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
