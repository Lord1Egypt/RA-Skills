## Description: <br>
Measures compositional structure in AI-generated images with the Visual Thinking Lens framework, detects default-mode bias, and generates targeted re-prompts through configurable operators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rusparrish](https://clawhub.ai/user/rusparrish) <br>

### License/Terms of Use: <br>
Creative Commons Attribution 4.0 International (CC BY 4.0) <br>


## Use Case: <br>
Developers, designers, and image-generation workflows use this skill to diagnose composition in AI-generated images and generate rule-based re-prompt variants when default-mode patterns are detected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Low-confidence or failed image measurements could lead to misleading composition guidance. <br>
Mitigation: Honor the skill's measurement gate: stop on failed measurements and clearly caveat low-confidence results. <br>
Risk: Untrusted operator files could change the generated re-prompt guidance. <br>
Mitigation: Use the bundled or otherwise trusted operators.yaml, and review operator changes before relying on generated prompt variants. <br>
Risk: Python dependencies are installed from pip for local image analysis. <br>
Mitigation: Install and run the skill in an isolated Python environment appropriate for local files you choose to analyze. <br>


## Reference(s): <br>
- [VTL Image Analysis on ClawHub](https://clawhub.ai/rusparrish/vtl-image-analysis) <br>
- [VTL Metric Reference](references/vtl-metrics.md) <br>
- [Visual Thinking Lens Framework](https://github.com/rusparrish/Visual-Thinking-Lens) <br>
- [Russell Parrish](https://artistinfluencer.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with JSON metrics and prompt-variant guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports low-confidence or failed measurements before producing coordinates or re-prompt guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
