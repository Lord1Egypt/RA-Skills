## Description: <br>
小红书文案创作 helps agents research Xiaohongshu viral-note patterns with RedFox trend data and generate ready-to-publish note copy with titles, body text, tags, and source formulas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brand operators, and social-media teams use this skill to analyze Xiaohongshu viral notes for a topic and produce complete platform-style copy. Agents can retrieve trend data, extract title and content patterns, ask for optional writing samples, and return structured publish-ready Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and sends Xiaohongshu search keywords to redfox.hk. <br>
Mitigation: Install only when the user is comfortable using RedFox for Xiaohongshu research, and store REDFOX_API_KEY in the environment rather than in prompts, code, logs, or output files. <br>
Risk: Personal writing samples may contain sensitive or identifying information. <br>
Mitigation: Use non-confidential public drafts as style references and avoid sharing sensitive personal samples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/xhs-copywriter) <br>
- [Xiaohongshu hot article data format](references/xhs_hot_article_format.md) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with structured copywriting sections; the supporting fetch script returns JSON data for agent analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; final copy should include 3-6 recommended titles, complete body text, 5-10 tags, a viral formula summary, and 2-3 reference notes with links and engagement metrics.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
