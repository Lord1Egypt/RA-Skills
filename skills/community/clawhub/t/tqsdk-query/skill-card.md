## Description: <br>
TqSdk Query retrieves Tianqin/TQSDK futures and options quotes, live K-line series, and historical K-line data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaingush](https://clawhub.ai/user/gaingush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading or research users use this skill to query Tianqin/TQSDK market data for Chinese futures and options, including quotes, recent K-line data, and historical K-line ranges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Tianqin/TQSDK credentials through environment variables. <br>
Mitigation: Use credentials limited to market-data access and scope TQ_USERNAME and TQ_PASSWORD to this skill. <br>
Risk: The package depends on external Python libraries and the security guidance notes an unresolved tqsdk_client import. <br>
Mitigation: Pin dependency versions for reproducible deployments and verify or remove the missing import before relying on the skill. <br>
Risk: Historical K-line access may require a Tianqin professional account and valid time ranges. <br>
Mitigation: Confirm account permissions and query limits before using historical-data actions in production workflows. <br>


## Reference(s): <br>
- [TQSDK homepage](https://www.shinnytech.com/tqsdk/) <br>
- [ClawHub skill page](https://clawhub.ai/gaingush/tqsdk-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Dictionary containing a text summary and result or error fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include quote fields, the latest K-line record, or historical K-line records depending on the selected action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
