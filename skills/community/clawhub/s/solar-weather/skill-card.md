## Description: <br>
Monitor solar weather conditions including geomagnetic storms, solar flares, aurora forecasts, and solar wind data using NOAA Space Weather Prediction Center real-time data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[capt-marbles](https://clawhub.ai/user/capt-marbles) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to check current and forecast solar-weather conditions, including geomagnetic storms, solar flares, aurora likelihood, solar wind data, and NOAA SWPC alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script contacts NOAA SWPC public endpoints to produce live results. <br>
Mitigation: Run it only in environments where outbound access to NOAA SWPC is acceptable. <br>
Risk: Solar-weather outputs may be used for operational awareness by radio, aurora, satellite, or power-grid users. <br>
Mitigation: Treat results as situational information and confirm critical decisions against official NOAA SWPC products. <br>


## Reference(s): <br>
- [NOAA Space Weather Prediction Center](https://www.swpc.noaa.gov/) <br>
- [NOAA SWPC Public Data Service](https://services.swpc.noaa.gov) <br>
- [ClawHub Skill Page](https://clawhub.ai/capt-marbles/solar-weather) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON from a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network access to NOAA SWPC public endpoints is required for live results.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
