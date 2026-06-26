## Description: <br>
执行基因组间 SYRI 共线性分析，包含染色体处理、minimap2 比对、结构变异检测及 plotsr 可视化流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjw065](https://clawhub.ai/user/wangjw065) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Genomics researchers and bioinformatics practitioners use this skill to run a SYRI-based collinearity and structural-variation workflow between genome assemblies, from chromosome preparation through visualization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Large genome alignments can consume substantial disk space and compute resources. <br>
Mitigation: Confirm available storage before alignment, choose a thread count appropriate for the machine, and run the workflow in an isolated conda or virtual environment. <br>
Risk: Bioinformatics package installation can introduce supply-chain or version drift risk. <br>
Mitigation: Verify minimap2, SYRI, plotsr, and Biopython packages before use and prefer trusted package channels or pinned versions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjw065/syri-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes workflow steps, installation commands, troubleshooting notes, and expected SYRI output file descriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
