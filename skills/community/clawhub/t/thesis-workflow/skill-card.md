## Description: <br>
A multi-agent workflow for MBA and academic thesis writing that supports dual-version drafting, review, integration, finalization, and Word output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hehe973781230](https://clawhub.ai/user/hehe973781230) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, students, researchers, and writing assistants use this skill to coordinate long-form MBA or academic thesis workflows from proposal planning through drafting, review, integration, and final Word generation. It is most relevant for formal papers that need multi-round review, citation checks, structured formatting, and human approval checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe local parsing and path handling may allow unintended local execution or writes outside the intended workspace. <br>
Mitigation: Review the scripts before installation, replace eval-style parsing with strict JSON parsing, and validate paper or workspace names so generated paths cannot escape the expected workspace. <br>
Risk: Persistent automation and broad trigger behavior may advance thesis workflow steps without enough user review. <br>
Mitigation: Gate automated phase transitions with explicit human approval, review any scheduled jobs before enabling them, and narrow trigger rules to the intended thesis workflow. <br>
Risk: Thesis drafts, company details, email addresses, or other confidential material may be stored locally or sent through LLM/tool calls during the workflow. <br>
Mitigation: Use only approved thesis data, keep company mappings and sensitive inputs out of final outputs, and confirm where local files and model/tool calls are routed before using real confidential material. <br>


## Reference(s): <br>
- [Academic Standards Checklist](references/checklist.md) <br>
- [Loop Design Principles](references/loop-design.md) <br>
- [Chapter Summary Design](references/chapter-summary-design.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/hehe973781230/skills/thesis-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown, JSON state files, review reports, shell commands, and generated Word documents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces staged thesis artifacts, validation reports, and docx output through a human-gated workflow.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
