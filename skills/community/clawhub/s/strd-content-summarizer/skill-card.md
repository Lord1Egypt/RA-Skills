## Description: <br>
Fetch any URL and produce a structured content summary with extractive summarization, AI enhancement prompts, and structured output templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content teams use this skill to turn URLs or raw text into structured markdown summaries, extractive key sentences, tweet hooks, key takeaways, and prompts for optional LLM refinement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-provided URLs and stores extracted text in local markdown files. <br>
Mitigation: Use it for public or shareable content, set OUTPUT_DIR appropriately for sensitive work, and clean up generated files when they are no longer needed. <br>
Risk: Generated AI enhancement prompts may contain copied source text that a user could paste into an external AI service. <br>
Mitigation: Review extracted text before sending prompts to any external service and avoid including private or confidential material. <br>
Risk: Extractive summaries and templates may omit nuance or preserve misleading source phrasing. <br>
Mitigation: Review key sentences and generated templates against the source before publishing or using them for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kryzl19/strd-content-summarizer) <br>
- [Publisher profile](https://clawhub.ai/user/kryzl19) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown summaries and terminal output with generated local markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [URL summaries are saved under the configured OUTPUT_DIR, defaulting to /tmp/summaries; URL extraction limits article text to 15,000 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
