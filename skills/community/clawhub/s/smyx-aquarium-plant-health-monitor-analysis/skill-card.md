## Description: <br>
AI-powered aquatic plant health monitoring analyzes aquarium images or videos to detect leaf color and morphology issues, assess health, and provide care-direction suggestions for smart fish tanks, aquascaping tanks, and aquarium shops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External aquarium keepers, aquascaping operators, aquarium shops, and agents assisting them use this skill to analyze aquarium plant images or videos, receive structured plant-health assessments, and retrieve cloud-hosted history reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aquarium images, videos, report history, and account metadata are processed by the Life Emergence cloud service. <br>
Mitigation: Use the skill only with media and report history that users are comfortable sending to that cloud service, and avoid submitting sensitive personal, household, or location-identifying content. <br>
Risk: The skill silently creates or reuses a local identity and stores authentication tokens in a local SQLite database. <br>
Mitigation: Run it in a controlled agent environment, restrict local file access, and clear local identity or token storage when the workspace should not retain account state. <br>
Risk: The security scan verdict is suspicious because users have limited control over local identity, token storage, and attached account metadata. <br>
Mitigation: Review the account-linking behavior before deployment, use test or least-privilege accounts where possible, and disclose cloud processing expectations to affected users. <br>
Risk: Visual plant-health assessments may be uncertain and do not provide precise water-parameter adjustment instructions. <br>
Mitigation: Treat results as care-direction guidance and confirm important aquarium decisions with water testing or a qualified aquarium specialist. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/smyx-sunjinhui/skills/smyx-aquarium-plant-health-monitor-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/smyx-sunjinhui) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured JSON-style report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include analysis status, health findings, care-direction suggestions, report links, cloud history tables, and optional saved output files.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
