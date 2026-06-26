## Description: <br>
Score and evaluate virtual try-on results by analyzing identity preservation, garment fidelity, body consistency, and background stability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xavierjiezou](https://clawhub.ai/user/xavierjiezou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and evaluators use this skill to assess AI-generated virtual try-on images, compare source person, garment, and result images, and receive calibrated scoring with concise quality feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes uploaded person images, which may include sensitive personal information. <br>
Mitigation: Use only images the user intends to have evaluated and avoid sensitive personal images unless analysis is explicitly desired. <br>
Risk: Broad outfit-change or garment-swap requests may trigger the skill when image roles or user intent are ambiguous. <br>
Mitigation: Ask the user to confirm the source person, target garment, and try-on result before scoring ambiguous inputs. <br>
Risk: The prescribed report format is fixed in Chinese and may not match every user's preferred language or reporting format. <br>
Mitigation: Offer a translated or reformatted summary when the user needs the evaluation in another language or layout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xavierjiezou/virtual-tryon-scorer) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown report with structured scoring sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a fixed Chinese-language scoring report with four 0-100 dimension scores and a weighted total.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
