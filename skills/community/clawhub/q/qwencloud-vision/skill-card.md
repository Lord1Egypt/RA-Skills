## Description:

[QwenCloud] Understand images and videos with Qwen vision models for image analysis, OCR, chart and table reading, visual reasoning, multi-image comparison, screenshot understanding, and video comprehension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to analyze images and videos with QwenCloud vision models, including OCR, visual reasoning, document understanding, screenshot analysis, and multi-image comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub security scan flags under-scoped update and endpoint behaviors that can run extra local code or send credentials to an untrusted destination.

Mitigation: Install only from trusted working directories, avoid accepting the unpinned remote update-check install unless approved, and keep API endpoint settings on official QwenCloud hosts.

Risk: The skill uses API credentials and local .env configuration for QwenCloud requests.

Mitigation: Store credentials in trusted user-controlled configuration, use variable references instead of plaintext values, and do not expose .env contents in agent output.

## Reference(s):

- [Qwen Vision API Sources](references/sources.md)
- [Qwen Vision API Supplementary Guide](references/api-guide.md)
- [Qwen-VL-OCR Text Extraction Guide](references/ocr.md)
- [Visual Reasoning Guide](references/visual-reasoning.md)
- [Qwen Vision Execution Guide](references/execution-guide.md)
- [Vision curl Examples](references/curl-examples.md)
- [Vision Prompt Guide](references/prompt-guide.md)
- [Agent Compatibility](references/agent-compatibility.md)
- [QwenCloud Vision API Reference](https://docs.qwencloud.com/developer-guides/multimodal/vision)
- [QwenCloud Visual Reasoning Guide](https://docs.qwencloud.com/developer-guides/text-generation/thinking)
- [QwenCloud OCR Guide](https://docs.qwencloud.com/developer-guides/multimodal/ocr)
- [QwenCloud Model List](https://www.qwencloud.com/models)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python command examples; bundled scripts can emit JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save JSON response files, stream visual reasoning output, and require QwenCloud API key configuration.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
