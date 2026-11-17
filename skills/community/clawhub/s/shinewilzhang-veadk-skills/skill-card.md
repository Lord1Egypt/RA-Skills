## Description:

Helps developers generate VeADK agent code from requirements or convert LangChain, LangGraph, and Dify workflows into VeADK agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinewilzhang](https://clawhub.ai/user/shinewilzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design VeADK agent structure, refine agent prompts, generate Python agent code, and convert LangChain, LangGraph, or Dify workflow inputs into VeADK implementations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled save script can create or overwrite writable local files based on its path argument.

Mitigation: Use a dedicated workspace, review generated paths before running the save script, and avoid allowing user-provided names or conversion inputs to determine file paths without validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shinewilzhang/skills/shinewilzhang-veadk-skills)
- [Agent definition reference](references/common/agent.md)
- [Tool definition reference](references/common/tools.md)
- [Knowledge base reference](references/common/knowledgebase.md)
- [Agent architecture generation reference](references/generator/analyze.md)
- [Prompt refinement reference](references/generator/refine_prompt.md)
- [Code generation reference](references/generator/coding.md)
- [LangChain conversion rules](references/converter/langchain_rules.md)
- [Dify conversion rules](references/converter/dify_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local file paths and file contents for VeADK agent packages.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
