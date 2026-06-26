## Description: <br>
Extract multilingual document content and language learning notes from PDFs using multimodal vision with Qwen-VL-Max, converting pages into structured Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MingEnsiie](https://clawhub.ai/user/MingEnsiie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to convert language-learning PDFs, bilingual notes, and complex document layouts into readable Markdown using a vision model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF page images are sent to Alibaba Cloud DashScope/Qwen for analysis. <br>
Mitigation: Use the skill only with documents approved for that provider and avoid sensitive, regulated, or confidential PDFs unless provider use is acceptable. <br>
Risk: API keys may be exposed if passed directly on the command line. <br>
Mitigation: Prefer the DASHSCOPE_API_KEY environment variable and run the skill from an isolated shell or Python environment. <br>
Risk: Installing runtime dependencies changes the local Python environment. <br>
Mitigation: Install pymupdf and dashscope in a dedicated virtual environment before running the parser. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MingEnsiie/universal-pdf-vision-parse) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown file generated from PDF page images, with shell commands and setup guidance for agent use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DashScope API key and processes PDF pages through Qwen-VL-Max; default processing is limited to two pages unless configured otherwise.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
