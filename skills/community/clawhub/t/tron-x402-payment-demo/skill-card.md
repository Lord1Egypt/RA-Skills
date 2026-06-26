## Description: <br>
Demonstrates the x402 payment protocol on the TRON network by fetching a protected image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzc1206](https://clawhub.ai/user/wzc1206) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can use this skill to exercise an x402 payment flow on TRON and retrieve a protected image resource. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a TRON private key to perform a payment without clear confirmation or spending limits. <br>
Mitigation: Use only a throwaway or minimally funded TRON wallet and require visible confirmation of amount, network, recipient, and signing details before allowing any payment. <br>
Risk: The payment flow depends on the x402_payment_tron dependency and a remote protected endpoint. <br>
Mitigation: Verify the x402_payment_tron dependency and destination endpoint before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzc1206/tron-x402-payment-demo) <br>
- [Protected x402 demo endpoint](http://x402-tron-demo.sunagent.ai/protected) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or agent response text describing the payment result and displaying the fetched image when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TRON_PRIVATE_KEY when configured and deletes the local temporary file after display.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
