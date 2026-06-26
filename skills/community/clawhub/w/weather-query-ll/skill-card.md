## Description: <br>
A weather lookup skill that extracts a city and requested time from the user, fetches weather information from the web, and returns a concise forecast-style summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gyifei](https://clawhub.ai/user/Gyifei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer weather questions for a specified city and time. It is intended for everyday weather lookup responses that include temperature, conditions, humidity, wind, and a short practical tip. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: City and requested time may be sent to an external weather website during lookup. <br>
Mitigation: Use a trusted weather source and avoid sending sensitive location details when ordinary city-level weather is sufficient. <br>
Risk: Weather responses can be inaccurate, stale, or vary by source. <br>
Mitigation: Check the source, timestamp, and city before acting on weather-sensitive plans. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Gyifei/weather-query-ll) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Gyifei) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Plain text or Markdown weather summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include city, requested time, Celsius temperature, weather condition, humidity, wind, and a short weather tip; prompts for a city when missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
