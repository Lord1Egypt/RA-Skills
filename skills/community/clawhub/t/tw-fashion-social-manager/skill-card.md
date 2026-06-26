## Description: <br>
Helps Taiwan fashion brands plan social posts, Meta/IG/FB/TikTok ad copy, hashtag mixes, posting schedules, funnel strategy, and performance diagnostics from embedded ad-performance benchmarks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shangweilin7](https://clawhub.ai/user/shangweilin7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, founders, and social-media operators use this skill to create localized Taiwan fashion marketing content, select platforms and hashtags, plan posting calendars, design Meta ad funnels, and diagnose campaign performance. <br>

### Deployment Geography for Use: <br>
Global, with guidance tailored to Taiwan fashion brands and audiences. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require broad, persistent Meta and Threads credentials for account analytics. <br>
Mitigation: Use a dedicated least-privilege Meta system user or token, avoid full-control or admin scopes unless necessary, keep credentials out of source control, restrict .env permissions, and rotate or revoke tokens after use. <br>
Risk: The local helper script can fetch live account analytics and save reports on the user's machine. <br>
Mitigation: Run the helper only when live analytics are intended, review the configured output path before execution, and inspect generated reports before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shangweilin7/tw-fashion-social-manager) <br>
- [README.md](README.md) <br>
- [2026 Taiwan Fashion Brand Meta Ads Data](references/meta-ads-data.md) <br>
- [Brand Context](references/brand-context.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with campaign copy, tables, checklists, and optional bash commands; the helper script can write an XLSX insights report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Meta and Threads API credentials when the local helper script is explicitly run.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
