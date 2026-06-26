## Description: <br>
Looks up a mobile phone number's province, city, carrier, and card type through JisuAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer phone-number attribution questions by querying a provided mobile number and summarizing its province, city, carrier, and card type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried phone numbers are sent to JisuAPI under the configured API key. <br>
Mitigation: Use a dedicated JISU_API_KEY, monitor quota or billing, and only query numbers you are authorized and comfortable sharing with the provider. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jisuapi/shouji) <br>
- [JisuAPI website](https://www.jisuapi.com/) <br>
- [JisuAPI mobile phone number attribution documentation](https://www.jisuapi.com/api/shouji/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON result or JSON error object from the command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends queried phone numbers to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
