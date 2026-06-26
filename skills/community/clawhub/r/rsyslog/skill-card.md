## Description: <br>
RSyslog advanced system logging reference. RainerScript configuration, input/output modules (imtcp/imfile/omfwd/omelasticsearch), templates with property replacer, content-based filtering, TLS-encrypted remote logging, queue performance tuning, and debug troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, system administrators, and operations engineers use this skill as a command-driven rsyslog reference for configuration syntax, modules, templates, filtering, remote logging, performance tuning, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copying remote logging examples without review can expose syslog listener ports or send logs to unintended forwarding destinations. <br>
Mitigation: Review exposed ports, firewall rules, forwarding destinations, and queue behavior before applying examples in production. <br>
Risk: TLS logging examples may need stronger authentication settings for production environments. <br>
Mitigation: Confirm certificate paths, CA trust, key handling, and TLS authentication mode before enabling encrypted remote logging. <br>
Risk: Forwarded or retained logs may contain sensitive data. <br>
Mitigation: Review retention paths, log destinations, and data handling requirements before forwarding or storing logs. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/rsyslog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reference text with inline bash and rsyslog configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command-selected reference sections for intro, config, modules, templates, filtering, remote logging, performance, and troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
