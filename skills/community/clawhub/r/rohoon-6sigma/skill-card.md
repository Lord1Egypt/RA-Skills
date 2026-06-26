## Description: <br>
Rohoon Six Sigma provides Six Sigma and Lean quality management support for DMAIC/DMADV workflows, SPC control charts, process capability indices, MSA analysis, DOE, FMEA, 5S, VSM, automotive quality management, process optimization, and supplier assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamhyzhu](https://clawhub.ai/user/williamhyzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Quality engineers, manufacturing engineers, supplier quality teams, and agents supporting them use this skill to calculate SPC, process capability, MSA, and DOE results, then produce PDF, Excel, JSON, Markdown, and command-line report outputs for quality reviews and continuous-improvement work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Python scripts can execute report-generation logic and write files in the agent environment. <br>
Mitigation: Install and run the skill in an environment approved for local script execution, and review generated artifacts before sharing them externally. <br>
Risk: Dependency drift could change numerical, plotting, or document-generation behavior. <br>
Mitigation: Pin or lock Python dependencies before production use and rerun representative SPC, MSA, DOE, PDF, and Excel checks after dependency updates. <br>
Risk: Batch PDF processing may open or process files from a folder that contains untrusted PDFs. <br>
Mitigation: Run batch PDF workflows only on trusted inputs, or remove or disable the automatic open step before processing untrusted folders. <br>
Risk: Quality calculations and report conclusions depend on correct input data, specification limits, distribution assumptions, and study design. <br>
Mitigation: Have a qualified quality or process engineer review inputs, assumptions, and conclusions before using results for audits, supplier decisions, or production controls. <br>


## Reference(s): <br>
- [Rohoon Six Sigma on ClawHub](https://clawhub.ai/williamhyzhu/rohoon-6sigma) <br>
- [Control Charts Reference](references/control-charts.md) <br>
- [Process Capability Indices](references/capability-indices.md) <br>
- [MSA Reference Guide](references/msa-reference.md) <br>
- [Design of Experiments Guide](references/doe-guide.md) <br>
- [Lean Six Sigma Tools Reference](references/lean-six-sigma-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON-capable script output, and generated PDF or Excel report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Python report-generation scripts may write local PDF, Excel, chart, or JSON artifacts.] <br>

## Skill Version(s): <br>
1.8.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
