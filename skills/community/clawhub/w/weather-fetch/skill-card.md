## Description: <br>
Weather Fetch retrieves current weather data for supported Chinese cities from weathercn.com using Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wndagg](https://clawhub.ai/user/wndagg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents can use this skill to look up current weather conditions for supported cities in China and return temperature, wind, humidity, pressure, visibility, sunrise and sunset times, and air quality details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill launches Chromium with reduced sandboxing to scrape weathercn.com. <br>
Mitigation: Run it in a contained environment and install Playwright/Chromium only from trusted package sources. <br>
Risk: The skill contacts an external weather website and depends on that site's availability and page structure. <br>
Mitigation: Allow outbound access only to the expected weather source and review outputs when the source page changes or fails. <br>
Risk: City coverage is limited to the cities defined in the script unless the mapping is updated. <br>
Mitigation: Confirm the requested city is supported before relying on the result, and update the city mapping through normal review if broader coverage is needed. <br>


## Reference(s): <br>
- [ClawHub Weather Fetch release](https://clawhub.ai/wndagg/weather-fetch) <br>
- [weathercn.com mobile weather source](https://m.weathercn.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [JSON object plus formatted plain text weather report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [City name input; requires network access and Playwright/Chromium at runtime.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
