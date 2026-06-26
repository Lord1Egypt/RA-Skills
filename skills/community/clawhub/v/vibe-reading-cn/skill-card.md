## Description: <br>
Openclaw helps an agent process EPUB or TXT books into chapter-aware Simplified Chinese summaries and a static interactive HTML reader. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drbillwang](https://clawhub.ai/user/drbillwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers, knowledge workers, and developers use this skill with an OpenClaw-compatible agent to clean EPUB or TXT books, split them into chapters, and generate high-fidelity chapter summaries in Simplified Chinese. It also produces a static interactive HTML reader for navigating the generated summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install Python packages while preprocessing EPUB files. <br>
Mitigation: Run it in a project folder or virtual environment and review package installation before execution. <br>
Risk: The generated HTML reader may fetch marked.js from a CDN when opened. <br>
Mitigation: Use it only where CDN loading is acceptable, or replace the CDN dependency with a locally reviewed copy before sharing. <br>
Risk: Embedding API keys or AI service calls in generated HTML would expose secrets. <br>
Mitigation: Keep the HTML static and ask the OpenClaw agent for follow-up questions instead of adding keys or external AI calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drbillwang/vibe-reading-cn) <br>
- [Homepage](https://github.com/drbillwang/vibe-reading-skill-CN) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown summaries, JSON chapter plans, plain text chapter files, and static HTML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML may fetch marked.js from a CDN; EPUB preprocessing may require installing ebooklib and beautifulsoup4.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
