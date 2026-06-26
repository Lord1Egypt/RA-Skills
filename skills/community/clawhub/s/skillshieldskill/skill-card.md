## Description: <br>
AI Agent Skill Security Scanner - Detect malicious skills, verify signatures, analyze permissions, and provide trust ratings for the agent ecosystem. Protects against credential stealers, data exfiltration, and unauthorized access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uexo](https://clawhub.ai/user/uexo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to scan agent skills for suspicious patterns, permission needs, and trust-rating signals before installation or deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes Moltbook posting code and a bundled token that should be treated as exposed. <br>
Mitigation: Do not run upload_to_moltbook.py unless intentional posting is required; rotate or revoke any exposed token before use. <br>
Risk: The advertised signature verification feature is not implemented. <br>
Mitigation: Do not rely on signature verification results for trust decisions until real cryptographic verification is added and reviewed. <br>
Risk: The scanner reports security findings but can produce false positives or miss behaviors outside its static rules. <br>
Mitigation: Review scan findings manually and combine them with source review before installing or deploying scanned skills. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/uexo/skillshieldskill) <br>
- [Publisher Profile](https://clawhub.ai/user/uexo) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON scan reports, with Markdown documentation and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes trust ratings, warnings, permission summaries, recommendations, and file hash summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
