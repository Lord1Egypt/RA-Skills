## Description: <br>
Analyzes one to five reference articles and rewrites source material in a similar style, producing three versions with adjustable style intensity and support for iterative refinement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to analyze sample writing style and transform draft material into platform-ready article variants while preserving the source material's core points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reference articles and draft material are sent to the configured LLM provider. <br>
Mitigation: Use only content that the provider terms allow, avoid private or regulated material unless approved, and review the configured API_BASE before running. <br>
Risk: The skill can produce text that closely imitates a person's writing style, which may create impersonation or authorship-misrepresentation risk. <br>
Mitigation: Use the output transparently, avoid presenting generated text as written by the referenced author, and review outputs before publication. <br>
Risk: API credentials are required for the external LLM call. <br>
Mitigation: Use a dedicated API key with appropriate access limits and rotate it if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antonia-sz/style-cloner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown containing a style analysis summary, three rewritten article versions, and usage guidance; the CLI can also write the Markdown result to a file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs vary by reference articles, source material, intensity, target length, target platform, and configured LLM provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
