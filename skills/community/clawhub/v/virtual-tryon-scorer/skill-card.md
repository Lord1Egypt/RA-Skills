## Description:

Scores virtual try-on results by comparing the source person, target garment, and generated output for identity preservation, garment fidelity, body consistency, and background stability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xavierjiezou](https://clawhub.ai/user/xavierjiezou)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate AI-generated virtual try-on images before relying on them for presentation, review, or purchase-decision workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill evaluates uploaded try-on photos that may include identifiable face and body imagery.

Mitigation: Use only with images the user is authorized to analyze and avoid submitting sensitive personal photos unless appropriate for the deployment context.

Risk: Ambiguous image roles or low-quality inputs can make the scoring report unreliable.

Mitigation: Ask users to identify the source person, target garment, and try-on result when unclear, and caveat scores when image quality limits visual assessment.

Risk: The report format is expected to be Chinese unless the user asks for another language.

Mitigation: Tell the agent or user to request a different output language when the deployment requires English or another locale.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown scoring report with per-dimension scores, weighted total score, and concise explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores four dimensions on a 0-100 scale with weights of 40%, 30%, 20%, and 10%.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
