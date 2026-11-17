## Description:

对小红书达人笔记做品牌词、必带话题、@官号、调性、链接与广告法/竞品合规的自动化质检，并输出结构化报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wandervine](https://clawhub.ai/user/wandervine)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and content operations reviewers use this skill to check Xiaohongshu KOL/KOC notes for brand wording, required hashtags, official account mentions, tone, link reachability, and advertising-law or competitor-brand compliance before release. It can also guide updates to the skill's wordlist and reference files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Link-fetching helpers can request arbitrary URLs too broadly.

Mitigation: Review before installation, run with sandboxed outbound network access, and add URL allowlisting plus untrusted-content handling before processing arbitrary links.

## Reference(s):

- [Brand name and official accounts reference](references/brand-name-and-official-accounts.md)
- [ClawHub skill page](https://clawhub.ai/wandervine/skills/xhs-content-qc)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Structured Markdown report with optional JSON from link-fetching helpers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses line-based wordlists and may mark checks SKIP or BLOCKED when note content is incomplete.]

## Skill Version(s):

1.0.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
