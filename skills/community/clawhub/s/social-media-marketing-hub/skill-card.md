## Description:

Social Media Marketing Hub analyzes Douyin trend patterns, generates AI-assisted titles and spoken scripts, supports product selection analysis, competitor account analysis, and a local memory system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dadajuanzhenren](https://clawhub.ai/user/dadajuanzhenren)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, social media operators, and agent users use this skill to analyze Douyin keywords or competitor accounts, identify content and product patterns, and generate titles, sales scripts, and actionable marketing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports unsafe and under-disclosed credential behavior for API keys.

Mitigation: Use environment variables for TikHub and DeepSeek credentials, avoid file-based credential storage, and rotate credentials if they were passed through command output or local files.

Risk: The security scan reports command construction and subprocess behavior that should be reviewed before use.

Mitigation: Run only in a restricted workspace with minimal subprocess permissions, review inputs before invoking browser, curl, ffmpeg, whisper, or process-control commands, and avoid shared or sensitive environments until maintainer fixes are available.

Risk: The security scan reports unsafe filename handling and local file-write behavior.

Mitigation: Use non-sensitive keywords and account names, constrain write roots to the skill directory, and inspect generated memory and author report JSON before reuse or sharing.

Risk: The security scan reports a TikHub host mismatch and broad Xvfb process killing.

Mitigation: Confirm allowed network hosts match the runtime API host and avoid browser mode on shared systems until process cleanup behavior is narrowed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dadajuanzhenren/skills/social-media-marketing-hub)
- [dadajuanzhenren Publisher Profile](https://clawhub.ai/user/dadajuanzhenren)
- [TikHub API Access](https://user.tikhub.io/register?ref=teKGFLs1)
- [DeepSeek Platform](https://platform.deepseek.com/)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON files, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown-style analysis, with local JSON memory and report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist keyword memory and author analysis JSON under the skill scripts directory.]

## Skill Version(s):

8.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
