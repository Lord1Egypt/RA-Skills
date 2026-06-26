## Description: <br>
Talos plans a 4-week social media content calendar with platform-specific captions, posting times, content pillars, hashtag guidance, and JSON/Markdown exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media managers, marketers, creators, and small teams use this skill to turn a brand topic into an offline 4-week posting plan for Twitter/X, LinkedIn, Instagram, and Threads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs the Python formatting package rich before running. <br>
Mitigation: Install dependencies in a virtual environment and avoid system-wide package installation when possible. <br>
Risk: The skill writes social_calendar_*.json and social_calendar_*.md exports in the current working directory. <br>
Mitigation: Run it in a dedicated folder and avoid placing sensitive campaign details in shared directories. <br>
Risk: Generated captions, posting times, and hashtags may not match current platform guidance or brand requirements. <br>
Mitigation: Review and edit the generated calendar before importing it into a scheduling tool. <br>


## Reference(s): <br>
- [Talos ClawHub listing](https://clawhub.ai/occupythemilkyway/talos) <br>
- [OccupyTheMilkyWay publisher profile](https://clawhub.ai/user/occupythemilkyway) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash and Python code blocks; generated JSON and Markdown calendar files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRAND_TOPIC; optional PLATFORMS, POSTS_PER_WEEK, CONTENT_PILLARS, and BRAND_TONE tune the generated calendar.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
