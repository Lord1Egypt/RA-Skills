## Description: <br>
Smart ClawdBot documentation access with local search index, cached snippets, and on-demand fetch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawdBot operators use this skill to answer ClawdBot documentation questions efficiently by checking local snippets and indexes before fetching uncached documentation pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional remote documentation fetches require SKILLBOSS_API_KEY and send requested documentation URLs to api.heybossai.com. <br>
Mitigation: Use local snippets, the local index, and cached pages first; use a scoped or low-privilege API key where possible and monitor quota or billing. <br>


## Reference(s): <br>
- [ClawdBot Documentation](https://docs.clawd.bot/) <br>
- [ClawdBot Skills Documentation](https://docs.clawd.bot/tools/skills) <br>
- [ClawdBot Multi-Agent Documentation](https://docs.clawd.bot/concepts/multi-agent) <br>
- [ClawdBot Documentation Index](https://docs.clawd.bot/llms.txt) <br>
- [SkillBoss API Hub pilot endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prioritizes cached snippets and local index lookup, then uses optional remote documentation fetches when local evidence is insufficient.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata); artifact frontmatter reports 2.2.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
