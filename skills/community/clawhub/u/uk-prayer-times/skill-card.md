## Description: <br>
Get instant, accurate Islamic prayer times for any UK location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clinicode](https://clawhub.ai/user/clinicode) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to check daily Islamic prayer times for UK cities, towns, boroughs, or auto-detected locations. <br>

### Deployment Geography for Use: <br>
United Kingdom <br>

## Known Risks and Mitigations: <br>
Risk: Location-related requests may be processed by external services. <br>
Mitigation: Provide a city manually instead of using auto-detect mode when reducing location privacy exposure is important. <br>
Risk: Prayer times depend on external API availability and returned location data. <br>
Mitigation: Review the displayed location and date before relying on the returned prayer times. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clinicode/uk-prayer-times) <br>
- [Aladhan prayer timings API](https://api.aladhan.com/v1/timings) <br>
- [ipapi location API](https://ipapi.co/json/) <br>
- [OpenStreetMap Nominatim search API](https://nominatim.openstreetmap.org/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text prayer-time results with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Shows location, date, and Fajr, Sunrise, Dhuhr, Asr, Maghrib, and Isha times in 12-hour format.] <br>

## Skill Version(s): <br>
1.4.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
