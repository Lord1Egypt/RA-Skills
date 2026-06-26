## Description: <br>
Work smarter with loop detection, parallel decisions, and file size analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Workflow Tools to find open work loops, decide whether tasks should run serially or in parallel, analyze oversized files, and spawn subworkflows when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delegate work to installed skills, including background subworkflows, which can expand the effective behavior beyond this skill alone. <br>
Mitigation: Review installed companion skills before use, avoid background subworkflows unless the invoked skill and monitoring path are clear, and review generated outputs before acting on them. <br>
Risk: Loop detection and MCE analysis read user-specified files or directories. <br>
Mitigation: Run /wt loops and /wt mce only against intended project paths and use excludes for sensitive or irrelevant directories. <br>
Risk: The security assessment flags insufficient scoping and stop-control detail for delegated subworkflows. <br>
Mitigation: Install only when subworkflow orchestration is needed, monitor spawned work, and keep command inputs narrowly scoped. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leegitw/workflow-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style analysis, recommendations, command examples, and workspace output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write analysis results under output/loops/, output/parallel-decisions/, output/mce-analysis/, and output/subworkflows/.] <br>

## Skill Version(s): <br>
1.5.1 (source: ClawHub release metadata; artifact frontmatter says 1.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
