## Description:

Baidu Qianfan Tools integrates Baidu Qianfan platform APIs for search, hotword lookup, text generation, continuation, image generation, OCR, PPT generation, academic search, and related agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yingyangdao](https://clawhub.ai/user/yingyangdao)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent users use this skill to call Baidu Qianfan services from an OpenClaw-compatible environment, including web search summaries, hot topics, chat, generation, OCR, PPT, and academic-search tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts, search terms, document or image URLs, and generated-content requests are sent to Baidu Qianfan services using BAIDU_API_KEY.

Mitigation: Avoid using the skill with secrets, regulated personal data, or confidential internal documents unless that external transfer is approved.

Risk: Dependency reproducibility is weaker because axios is version-ranged and no lockfile is included in the release evidence.

Mitigation: Pin axios and add a lockfile before controlled or high-assurance deployments.

## Reference(s):

- [Baidu Qianfan API Documentation](https://cloud.baidu.com/doc/qianfan-api/s/3m9b5lqft)
- [Baidu Qianfan Console](https://console.bce.baidu.com/qianfan/)
- [ClawHub Skill Page](https://clawhub.ai/yingyangdao/skills/qianfan-tools)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses from command-line scripts, plus setup guidance in Markdown and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY; several Baidu Qianfan APIs require separate activation and may be metered.]

## Skill Version(s):

1.1.0 (source: evidence release, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
