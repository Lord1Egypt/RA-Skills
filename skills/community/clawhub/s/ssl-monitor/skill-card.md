## Description: <br>
查询域名 SSL 证书过期时间，并根据剩余天数返回正常、注意或紧急状态。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunny-lobster-api](https://clawhub.ai/user/sunny-lobster-api) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and site owners use this skill to check SSL certificate expiry for one domain or a batch of domains and identify certificates that need renewal soon. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to user-provided domains on port 443, so batch runs can reveal which domains are being checked to the local network path. <br>
Mitigation: Review domain lists before running batch checks and use the skill only for domains the user is permitted to inspect. <br>
Risk: Failed OpenSSL connections or date parsing issues can produce failed or incomplete certificate results. <br>
Mitigation: Treat failed checks as items for manual review and verify urgent renewal decisions against a second trusted source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunny-lobster-api/ssl-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown with shell command snippets; the optional batch script can also emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires openssl and network access to queried domains on port 443; batch checks may return a nonzero exit code for critical or failed domains.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
