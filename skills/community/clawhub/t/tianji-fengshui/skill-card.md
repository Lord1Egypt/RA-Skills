## Description: <br>
玄机子 is a feng shui and traditional Chinese metaphysics assistant for bazi analysis, palm and face reading, feng shui layout review, image analysis, and related learning guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuhong-cray](https://clawhub.ai/user/yuhong-cray) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to obtain traditional feng shui, bazi, palmistry, face-reading, and I Ching style analysis, including image-based palm or layout review through configured third-party model APIs. It also provides command examples, configuration guidance, and reference material for using those analyses in an OpenClaw-style agent environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive palm, face, home-layout, and exact birth information through third-party model APIs. <br>
Mitigation: Use only information the user accepts sending to those services, and avoid private images, home details, or exact birth data unless third-party processing is acceptable. <br>
Risk: The skill relies on API keys and local configuration files. <br>
Mitigation: Use a restricted API key or a dedicated configuration file containing only the credentials needed for this skill. <br>
Risk: Image analysis workflows can create optimized images and reports under /tmp. <br>
Mitigation: Manually delete generated /tmp/tianji_fengshui* files after use, especially on shared machines. <br>
Risk: Traditional metaphysics outputs may be uncertain or misleading if treated as authoritative advice. <br>
Mitigation: Treat analyses as informational or entertainment-oriented guidance and do not use them as the sole basis for important medical, financial, legal, safety, or life decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuhong-cray/tianji-fengshui) <br>
- [Volcengine Doubao API documentation](https://www.volcengine.com/docs/82379) <br>
- [DeepSeek API documentation](https://platform.deepseek.com/api-docs) <br>
- [Baidu API Key Setup Guide](skills/baidu-search/references/apikey-fetch.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands, JSON configuration examples, and generated analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call configured third-party APIs and may write temporary optimized images or text reports under /tmp during image and palm analysis workflows.] <br>

## Skill Version(s): <br>
2.7.0 (source: server release metadata; artifact frontmatter lists 2.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
