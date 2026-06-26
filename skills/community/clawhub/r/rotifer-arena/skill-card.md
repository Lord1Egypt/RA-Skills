## Description: <br>
One-click Gene comparison and evaluation for Rotifer Protocol that can import from ClawHub Skills, local files, or new scenarios, then compile, match opponents, run Arena battles, and generate structured Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoba-dev](https://clawhub.ai/user/xiaoba-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare Rotifer Genes, imported Skills, or custom implementations with Arena scoring, rankings, and reproducible evaluation reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes Rotifer CLI or MCP workflows and may submit, import, or evaluate local Skills and Genes. <br>
Mitigation: Confirm the exact local paths or ClawHub slugs being evaluated before execution, and avoid sensitive code unless the user understands what the Rotifer tooling submits or imports. <br>
Risk: Rotifer CLI and MCP packages are external tools executed through npx. <br>
Mitigation: Treat the Rotifer packages as external code, review the package source or provenance as needed, and run them only in intended Rotifer Gene or Arena workflows. <br>
Risk: Cross-fidelity comparisons can reflect scoring-model differences rather than direct capability differences. <br>
Mitigation: Include the skill's cross-fidelity disclaimer in reports and prefer same-fidelity opponents when comparing Wrapped, Hybrid, or Native Genes. <br>


## Reference(s): <br>
- [Rotifer Protocol](https://rotifer.dev) <br>
- [Rotifer Documentation](https://rotifer.dev/docs) <br>
- [Rotifer Protocol Specification](https://github.com/rotifer-protocol/rotifer-spec) <br>
- [Rotifer Playground](https://github.com/rotifer-protocol/rotifer-playground) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaoba-dev/rotifer-arena) <br>
- [Publisher Profile](https://clawhub.ai/user/xiaoba-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with tables, fixed-width ranking visualizations, and bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write saved reports to arena-reports/ after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
