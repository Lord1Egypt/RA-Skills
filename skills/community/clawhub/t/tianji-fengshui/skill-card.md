## Description:

天机·玄机子 is a Chinese-language feng shui and fortune-analysis assistant for BaZi, feng shui layout, palm reading, face reading, image analysis, book recommendations, and learning guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuhong-cray](https://clawhub.ai/user/yuhong-cray)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill for culturally framed feng shui, BaZi, palm, face, and image-layout analysis, plus command-line image analysis workflows that call configured third-party model APIs. Outputs should be treated as entertainment or cultural reference, not as medical, financial, or life-decision advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User images and prompts may be sent to third-party model API endpoints for processing.

Mitigation: Use the skill only with images and personal details you are willing to share with those services, and avoid private, identifying, or sensitive images unless third-party processing is acceptable.

Risk: Optimized images and analysis reports may remain in predictable temporary directories.

Mitigation: Manually delete /tmp/tianji_fengshui, /tmp/tianji_fengshui_public, and /tmp/tianji_fengshui_reports after use, especially on shared systems.

Risk: The security checker may expose credential prefixes in terminal output.

Mitigation: Run security checks only in private terminals and use limited-scope API keys that can be rotated after testing.

Risk: Fortune, health, personality, and relationship interpretations may be mistaken for professional advice.

Mitigation: Treat outputs as entertainment or cultural reference and do not rely on them as medical, financial, legal, or major life-decision guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuhong-cray/skills/tianji-fengshui)
- [Volcengine Doubao Vision API documentation](https://www.volcengine.com/docs/82379)
- [DeepSeek API documentation](https://platform.deepseek.com/api-docs)
- [OpenClaw skills documentation](https://docs.openclaw.ai/skills)
- [Baidu AI Search API key setup](skills/baidu-search/references/apikey-fetch.md)
- [Feng shui, BaZi, and palmistry knowledge base](knowledge/fengshui_bazi_palm_books.md)
- [Analysis templates](knowledge/analysis_templates.md)
- [Quick reference guide](knowledge/quick_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language prose analysis reports, Markdown guidance, JSON-like result objects, and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image workflows may create optimized images and text reports in temporary directories before returning analysis text.]

## Skill Version(s):

2.7.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
