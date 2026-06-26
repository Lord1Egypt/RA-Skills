## Description: <br>
Displays a live time dashboard with a summer solstice countdown, Beijing sunrise and sunset times, and current date and time information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to create a live seasonal time widget that counts down to the 2026 summer solstice and shows Beijing sunrise, sunset, and current time details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated widget contacts third-party public data APIs from the browser. <br>
Mitigation: Use it only in environments where those disclosed external requests are acceptable, or review and replace the endpoints before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/summer) <br>
- [U.S. Naval Observatory Seasons API](https://aa.usno.navy.mil/api/seasons?year=2026) <br>
- [Sunrise-Sunset API for Beijing](https://api.sunrise-sunset.org/json?lat=39.9075&lng=116.3972&formatted=0&date=today) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Guidance] <br>
**Output Format:** [HTML file with CSS and JavaScript] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated widget fetches disclosed public solstice and sunrise/sunset data at runtime.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
