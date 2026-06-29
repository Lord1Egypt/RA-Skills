## Description: <br>
Retrieves the current device's public IP address and geographic information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moxin1044](https://clawhub.ai/user/moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check a device's public IPv4 or IPv6 address, approximate location, ISP, timezone, and selected lookup service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external IP lookup services, which can reveal the device's public IP address and approximate network location. <br>
Mitigation: Run the skill only when that network disclosure is acceptable for the current environment. <br>
Risk: Geolocation, ISP, and timezone results can be unavailable, approximate, or service-dependent. <br>
Mitigation: Treat the output as informational and avoid using it as the sole source for security, compliance, or access-control decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/moxin1044/public-ip) <br>
- [ipify API](https://api.ipify.org) <br>
- [ifconfig.me IP Endpoint](https://ifconfig.me/ip) <br>
- [myip.com API](https://api.myip.com) <br>
- [ip-api JSON Endpoint](http://ip-api.com/json) <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [Plain text status report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access; output may include public IP address, approximate location, ISP, timezone, coordinates, and selected lookup service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
