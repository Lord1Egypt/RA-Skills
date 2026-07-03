## Description: <br>
析题 helps agents write heuristic Chinese competitive-programming solution explanations that teach problem-solving reasoning rather than only presenting answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, educators, and competitive-programming learners use this skill to turn problem statements, URLs, or standard solution files into Chinese heuristic explanations. It produces annotated C++ solutions, complexity analysis, preserved samples, common pitfalls, and optional fill-in-the-blank practice when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated explanations or C++ solutions may be incorrect or incomplete for a specific contest problem. <br>
Mitigation: Review the reasoning, test the code against official samples and edge cases, and verify complexity claims before publishing or submitting. <br>
Risk: The skill can request file reads, writes, and edits while preparing or delivering explanations. <br>
Mitigation: Keep file operations inside the intended contest or problem workspace and review any requested write or edit before allowing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fslong520/skills/xiti) <br>
- [Publisher profile](https://clawhub.ai/user/fslong520) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, guidance] <br>
**Output Format:** [Markdown with C++ code blocks, LaTeX math, tables, and Mermaid diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese heuristic explanation style; asks for depth preference after assessing difficulty; optional fill-in-the-blank mode only when requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
