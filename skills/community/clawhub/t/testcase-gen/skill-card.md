## Description: <br>
Generates comprehensive test cases from MySQL/Redis data. Invoke when user wants to create test cases for an API endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hcyyy0120](https://clawhub.ai/user/hcyyy0120) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to analyze API endpoint code, read selected MySQL and Redis data, and generate broad JSON test-case coverage for normal, boundary, error, extreme, business-rule, and validation scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads selected service configuration, MySQL tables, and Redis keys, which can expose sensitive application or customer data. <br>
Mitigation: Use staging or sanitized data sources, read-only credentials, narrow table and key patterns, and low row limits. <br>
Risk: Generated test cases may include SQL setup and teardown or cached data assumptions that are unsafe to run unchanged. <br>
Mitigation: Review generated JSON and SQL before sharing it or running tests. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON test-case files with Markdown guidance, SQL setup and teardown snippets, and shell commands for data extraction] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces test_cases_{timestamp}.json for review before downstream JUnit test generation.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
