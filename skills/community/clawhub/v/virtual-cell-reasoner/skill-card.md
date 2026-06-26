## Description: <br>
Consult a virtual cell language model on single-cell tasks, including cell generation, cell understanding, cell perturbation, and biology Q&A using cell token sequences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxuanyuan](https://clawhub.ai/user/wxuanyuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and biology researchers use this skill to query a hosted virtual-cell model for cell token generation, token-based cell feature summaries, perturbation-oriented prompts, and biology questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, cell token sequences, and biology questions are sent to an external API endpoint. <br>
Mitigation: Use only trusted endpoints and avoid submitting confidential clinical data, proprietary research, unpublished biological data, or regulated information unless the endpoint's data handling is acceptable. <br>
Risk: Model responses for biological interpretation may be incomplete or incorrect. <br>
Mitigation: Review outputs before using them for research decisions, downstream analysis, or documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wxuanyuan/virtual-cell-reasoner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with command-line examples and model response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the configured hosted API endpoint, prompt, max token limit, and sampling temperature.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
