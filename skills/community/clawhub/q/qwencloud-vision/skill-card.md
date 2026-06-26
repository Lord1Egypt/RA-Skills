## Description: <br>
qwencloud-vision helps agents analyze images and videos with Qwen vision models, including OCR, visual reasoning, multi-image comparison, screenshot understanding, and video comprehension. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route visual analysis tasks to QwenCloud vision models for image and video understanding, OCR extraction, chart and table reading, and visual reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images, videos, OCR documents, and prompts may be processed by a cloud provider. <br>
Mitigation: Avoid submitting secrets, IDs, financial documents, private screenshots, or regulated data unless the user has approval. <br>
Risk: The skill includes update/install and agent-configuration behavior beyond image and video analysis. <br>
Mitigation: Review update-check prompts, npx install commands, and CLAUDE.md or AGENTS.md changes before allowing them. <br>
Risk: The skill requires sensitive API credentials. <br>
Mitigation: Use environment variables or placeholder .env entries and never print API key values in plaintext. <br>


## Reference(s): <br>
- [Qwen Vision API Sources](references/sources.md) <br>
- [Qwen Vision API Supplementary Guide](references/api-guide.md) <br>
- [Qwen Vision Execution Guide](references/execution-guide.md) <br>
- [Qwen Visual Reasoning Guide](references/visual-reasoning.md) <br>
- [Qwen OCR Guide](references/ocr.md) <br>
- [Agent Compatibility Guide](references/agent-compatibility.md) <br>
- [Official QwenCloud Vision API Reference](https://docs.qwencloud.com/developer-guides/multimodal/vision) <br>
- [Official QwenCloud Visual Reasoning Guide](https://docs.qwencloud.com/developer-guides/text-generation/thinking) <br>
- [Official QwenCloud OCR Guide](https://docs.qwencloud.com/developer-guides/multimodal/ocr) <br>
- [QwenCloud Model List](https://www.qwencloud.com/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, Python or curl examples, and JSON responses from QwenCloud vision APIs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write analysis outputs under output/qwencloud-vision when an output path is requested.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
