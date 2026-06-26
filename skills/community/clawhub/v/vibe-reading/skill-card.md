## Description: <br>
Intelligent book reading and analysis skill that processes EPUB or TXT book files, splits them into chapters, produces deep chapter summaries, and generates an interactive static HTML reader. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drbillwang](https://clawhub.ai/user/drbillwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers, researchers, and developers use this skill to turn user-provided EPUB or TXT books into cleaned text, chapter files, high-fidelity Markdown summaries, and a static reader for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-provided book files and writes cleaned text, chapter files, summaries, and a reader locally. <br>
Mitigation: Use it only with documents you are comfortable storing in generated local files, and review outputs before sharing them. <br>
Risk: The skill depends on unpinned Python packages for EPUB extraction. <br>
Mitigation: Install and run it in a controlled environment where Python package resolution can be reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/drbillwang/vibe-reading) <br>
- [Project homepage](https://github.com/drbillwang/vibe-reading-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Local text, Markdown, JSON, and static HTML files, with generated Python code and shell commands when EPUB extraction is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes cleaned text under input/, chapter files under chapters/, summaries under summaries/, and a static html/interactive_reader.html without embedded API keys or AI service calls.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
