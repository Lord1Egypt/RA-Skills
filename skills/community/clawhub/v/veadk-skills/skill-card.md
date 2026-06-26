## Description: <br>
Generates VeADK agent code from user requirements and helps convert LangChain/LangGraph code or Dify workflow DSL into VeADK agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaozheng-fang](https://clawhub.ai/user/yaozheng-fang) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to design VeADK agent structures, refine prompts, generate Python agent code, and convert existing LangChain/LangGraph or Dify workflows into VeADK implementations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated files may be written outside the intended project directory or overwrite existing files. <br>
Mitigation: Review destination paths before allowing the save step and keep writes inside the intended project directory. <br>
Risk: Generated agent code may include behavior that should not be run without review, especially code-execution tools. <br>
Mitigation: Inspect generated VeADK code before running it and apply project security review for any code-execution capability. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yaozheng-fang/veadk-skills) <br>
- [Agent definition guidance](references/common/agent.md) <br>
- [Tool definition guidance](references/common/tools.md) <br>
- [Knowledge base guidance](references/common/knowledgebase.md) <br>
- [LangChain to VeADK conversion rules](references/converter/langchain_rules.md) <br>
- [Dify to VeADK conversion rules](references/converter/dify_rules.md) <br>
- [Agent architecture generation guidance](references/generator/analyze.md) <br>
- [Prompt refinement guidance](references/generator/refine_prompt.md) <br>
- [Code generation guidance](references/generator/coding.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands] <br>
**Output Format:** [Markdown with Python code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save generated VeADK agent files such as agent.py and __init__.py when the save script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
