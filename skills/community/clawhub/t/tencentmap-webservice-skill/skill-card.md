## Description: <br>
Guides agents and developers through Tencent Maps WebService API use for geocoding, place search, routing, distance matrix, weather, IP location, coordinate conversion, and administrative region queries over HTTP JSON APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when building or troubleshooting integrations with Tencent Maps WebService APIs. It helps choose the correct endpoint, assemble request parameters, interpret JSON responses and status codes, and apply API key, quota, coordinate, and privacy handling guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tencent Maps API keys or other secrets may be exposed if pasted into chat or committed in examples. <br>
Mitigation: Use environment variables such as TMAP_WEBSERVICE_KEY or a secret manager, redact keys from shared output, and avoid storing credentials in generated code. <br>
Risk: Location queries can include precise addresses, IP addresses, names, phone numbers, or other personal data. <br>
Mitigation: Only send data that is authorized and necessary for the task, minimize precision where possible, and avoid processing third-party personal data without a valid need. <br>
Risk: API guidance can produce incorrect coordinates, routes, or weather results if parameters, coordinate order, or Tencent Maps status codes are misread. <br>
Mitigation: Review generated requests before execution, confirm coordinates use latitude,longitude order and GCJ-02 expectations, and handle nonzero status codes before relying on results. <br>


## Reference(s): <br>
- [Address Service API](references/api-geocoder.md) <br>
- [Search Service API](references/api-search.md) <br>
- [Route Service API](references/api-direction.md) <br>
- [Location and Weather Service API](references/api-location-weather.md) <br>
- [Tools Service API](references/api-tools.md) <br>
- [Tencent Maps WebService API Overview](https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview) <br>
- [Tencent Maps API Key Management](https://lbs.qq.com/dev/console/key/manage) <br>
- [Tencent Maps WebService Status Codes](https://lbs.qq.com/service/webService/webServiceGuide/status) <br>
- [Tencent Maps Quota Guide](https://lbs.qq.com/dev/console/quotaImprove) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown with HTTP examples, JSON snippets, and code or shell commands when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Tencent Maps endpoint paths, request parameters, response interpretation, error handling steps, and API key setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
