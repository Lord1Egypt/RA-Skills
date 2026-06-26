## Description: <br>
Fetches current weather from Open-Meteo API and automatically captures a live webcam image from Meteoblue or Windy for the requested location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex1389](https://clawhub.ai/user/alex1389) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer weather requests with current Open-Meteo conditions and a live webcam image for the requested location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill visits external weather and webcam sites and may accept webcam-site cookies in a named browser session. <br>
Mitigation: Use only trusted destination URLs for the requested location and clear or isolate the named browser session when cookie persistence is not desired. <br>
Risk: The skill may overwrite /home/user/.openclaw/workspace/webcam.jpg when returning an image. <br>
Mitigation: Confirm that overwriting this path is acceptable or preserve the existing file before running the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alex1389/weather-webcam-v2) <br>
- [Publisher profile](https://clawhub.ai/user/alex1389) <br>
- [Open-Meteo geocoding API](https://geocoding-api.open-meteo.com/v1/search) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast) <br>
- [Meteoblue webcam example: Roses](https://www.meteoblue.com/en/weather/webcams/roses_spain_3111348) <br>
- [Meteoblue webcam example: Premia de Mar](https://www.meteoblue.com/en/weather/webcams/vilassar-de-mar_spain_3105522) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, guidance] <br>
**Output Format:** [Markdown-style weather caption with an attached JPEG image file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save the webcam image to /home/user/.openclaw/workspace/webcam.jpg.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
