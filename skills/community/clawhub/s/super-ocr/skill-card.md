## Description: <br>
Production-grade OCR with intelligent engine selection. Tesseract (lightweight, fast) and PaddleOCR (high accuracy, Chinese-optimized). Use when extracting text from images, processing Chinese documents, needing confidence scores, or working with mixed Chinese/English content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NimaChu](https://clawhub.ai/user/NimaChu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use Super OCR to extract text from images and document batches, especially when content may include Chinese, English, or mixed-language text. The skill helps select between available OCR engines and returns extracted text with confidence and processing metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup may install or download large OCR and image-processing dependencies. <br>
Mitigation: Install in a virtual environment, pin dependency versions, and scan dependencies before use. <br>
Risk: OCR inputs may contain sensitive information or come from untrusted sources. <br>
Mitigation: Run OCR in a sandboxed local environment and avoid processing sensitive images outside approved handling controls. <br>
Risk: Image preprocessing may briefly write derived image files locally. <br>
Mitigation: Use a controlled workspace for processing and clean temporary or output directories after completion. <br>


## Reference(s): <br>
- [API Reference for Super OCR](references/api-reference.md) <br>
- [Engine Comparison](references/engine-comparison.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/NimaChu/super-ocr) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/NimaChu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text, structured text, JSON, and CLI diagnostics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include confidence scores, engine choice, processing time, line counts, and batch output files when requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
