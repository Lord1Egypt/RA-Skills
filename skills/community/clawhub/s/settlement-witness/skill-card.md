## Description: <br>
Verify structured agent task outputs with signed receipts and optional TrustScore attribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nutstrut](https://clawhub.ai/user/nutstrut) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use SettlementWitness to verify structured agent task results against an expected spec, receive deterministic verdicts, and retain signed receipts for audit, settlement, or reputation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Structured verification data is sent to a remote verifier service. <br>
Mitigation: Submit only minimized task, spec, and output data, and exclude secrets, private user data, proprietary outputs, and account or session details. <br>
Risk: The verifier endpoint's retention policy or operational controls may not match a user's requirements. <br>
Mitigation: Review and trust the configured endpoint and its retention policy before using the skill in settlement, audit, or reputation workflows. <br>
Risk: A signed receipt can be mistaken for payment enforcement or long-term storage. <br>
Mitigation: Use the receipt as verification evidence only; keep payment, storage, and enforcement decisions in separate reviewed systems. <br>


## Reference(s): <br>
- [SettlementWitness on ClawHub](https://clawhub.ai/nutstrut/settlement-witness) <br>
- [Default verifier endpoint](https://defaultverifier.com/settlement-witness) <br>
- [SAR public keys](https://defaultverifier.com/.well-known/sar-keys.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, JSON, API calls] <br>
**Output Format:** [Markdown guidance with JSON-like request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deterministic PASS, FAIL, or INDETERMINATE verdicts with signed receipt fields and optional TrustScore attribution.] <br>

## Skill Version(s): <br>
0.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
