## Description: <br>
Queries weather for a specified city and returns temperature, weather description, and humidity in Celsius or Fahrenheit. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[qkainan](https://clawhub.ai/user/qkainan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent developers can use this skill to answer user weather questions for a named city and requested temperature unit. Because the security evidence identifies the output as simulated, it is suitable as a mock weather-query example unless connected to a real weather data source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises current weather while returning random simulated weather data. <br>
Mitigation: Treat results as mock data, clearly label them as simulated, or connect the skill to a real weather data source before using it for weather-dependent decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qkainan/testmaibao) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON string with city, temperature, description, humidity, and status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Temperature unit may be Celsius or Fahrenheit; weather values are simulated in the provided artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
