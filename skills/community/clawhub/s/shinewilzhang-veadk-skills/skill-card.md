## Description: <br>
Generates VeADK agent code from user requirements and converts LangChain, LangGraph, or Dify workflow inputs into VeADK agent implementations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shinewilzhang](https://clawhub.ai/user/shinewilzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to design VeADK agent structures, refine prompts, generate Python agent code, and convert LangChain/LangGraph or Dify workflows into VeADK implementations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated files can accidentally overwrite local files when saved to user-provided paths. <br>
Mitigation: Run the skill in a dedicated project workspace and review exact target paths before using the save helper. <br>
Risk: Generated or converted agent code may be incorrect for the target runtime or use case. <br>
Mitigation: Inspect generated code before execution and test it before deploying or sharing it. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/shinewilzhang/shinewilzhang-veadk-skills) <br>
- [Agent definition methods](references/common/agent.md) <br>
- [Tool definition methods](references/common/tools.md) <br>
- [Knowledge base usage](references/common/knowledgebase.md) <br>
- [LangChain to VeADK conversion rules](references/converter/langchain_rules.md) <br>
- [Dify to VeADK conversion rules](references/converter/dify_rules.md) <br>
- [Agent architecture generation](references/generator/analyze.md) <br>
- [Prompt refinement guidance](references/generator/refine_prompt.md) <br>
- [Code generation guidance](references/generator/coding.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with Python code blocks and save-file shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated VeADK agent files to local paths when the save script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
