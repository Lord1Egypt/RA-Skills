## Description: <br>
Short alias for external-site-profile-learning. Use this when investigating, adding, validating, or debugging external website profiles for the 99idea Playwright browser demo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allens0104](https://clawhub.ai/user/allens0104) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to investigate, add, validate, and debug reusable external website profiles for the 99idea Playwright browser demo, including heuristic and Gemini planning flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to browse or test external websites. <br>
Mitigation: Use it only on sites you are authorized to test, and avoid placing special or rate-limited sites in broad regression runs. <br>
Risk: Generated site profiles can encode incorrect selectors or verification assumptions. <br>
Mitigation: Review selected selectors and validation commands, then validate both heuristic and Gemini flows before treating a profile as stable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with selectors, verification details, validation commands, and final status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include failure or site class, exact selectors with rationale, verification mode, planned or executed validation commands, and stable/blocked/special-case status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
