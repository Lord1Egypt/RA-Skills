## Description: <br>
Generates academic figures from PDF or plain-text papers, including architecture diagrams, flowcharts, motivation figures, results charts, captions, and Mermaid topology descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljk00000](https://clawhub.ai/user/ljk00000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and agents use this skill to extract visualizable structure from academic papers and generate publication-oriented diagrams, result charts, captions, and reusable topology descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The results-chart path can run generated Python code with the user's local permissions. <br>
Mitigation: Review generated Python before execution and run chart generation in a sandboxed environment. <br>
Risk: Paper contents may be sent to configured third-party model or image-generation providers. <br>
Mitigation: Use only trusted papers and providers, and avoid confidential or unpublished manuscripts unless the provider terms permit that use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ljk00000/ynu-papergraphgeneration-openclaw) <br>
- [Artifact README](artifact/readme.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Generated image files with Markdown or plain-text captions, Mermaid topology descriptions, and optional Python/Matplotlib code or shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and image-generation API credentials such as BANANA2_API_URL and BANANA2_API_KEY, with documented fallback environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
