## Description:

Generates VeADK agent code from user requirements and helps convert LangChain, LangGraph, and Dify workflows into VeADK agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaozheng-fang](https://clawhub.ai/user/yaozheng-fang)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to design VeADK agent architectures, refine prompts, generate VeADK Python code, and convert existing LangChain, LangGraph, or Dify workflow implementations into VeADK agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled save script can create or overwrite arbitrary writable files without path or overwrite safeguards.

Mitigation: Use the skill only in a disposable or dedicated output directory, and require confirmation or a patch or diff review before generated files are saved or overwritten.

Risk: Generated VeADK agent code may not match the intended behavior or deployment constraints without review.

Mitigation: Review generated agent structure, prompts, tools, and file changes before deployment, then test the generated agent in a controlled workspace.

## Reference(s):

- [VeADK Agent Definition](references/common/agent.md)
- [VeADK Tools Definition](references/common/tools.md)
- [VeADK Knowledge Base](references/common/knowledgebase.md)
- [LangChain to VeADK Conversion Rules](references/converter/langchain_rules.md)
- [Dify to VeADK Conversion Rules](references/converter/dify_rules.md)
- [Agent Architecture Generation](references/generator/analyze.md)
- [Prompt Refinement](references/generator/refine_prompt.md)
- [Code Generation](references/generator/coding.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Files, Configuration instructions]

**Output Format:** [Markdown guidance with Python code and shell command snippets; generated deliverables are VeADK Python source files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated agent.py and __init__.py files when the bundled save script is invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
