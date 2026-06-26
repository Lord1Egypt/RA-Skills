## Description: <br>
Guides Move-to-TypeScript type mapping for @aptos-labs/ts-sdk, including bigint numeric handling, addresses, TypeTag, functionArguments, and typeArguments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iskysun96](https://clawhub.ai/user/iskysun96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to map Move values and function signatures to TypeScript when working with @aptos-labs/ts-sdk. It helps them choose safe numeric representations, pass address values, and align functionArguments and typeArguments with Move entry and view functions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Community guidance may not reflect current official Aptos SDK behavior for every project. <br>
Mitigation: Verify transaction examples, recipient addresses, amounts, type arguments, and current SDK behavior before using the guidance in real code. <br>
Risk: Incorrect numeric or argument mapping can produce wrong transaction or view payloads. <br>
Mitigation: Review generated code carefully, use bigint for large Move integer values, and confirm functionArguments and typeArguments match the target Move function signature. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iskysun96/ts-sdk-types) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown with TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only reference guidance; no executable behavior or sensitive access requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
