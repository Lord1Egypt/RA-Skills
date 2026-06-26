## Description: <br>
Automates installation and configuration of a Trojan proxy client on Linux, including proxychains4 command proxying and Google Chrome apt source setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[salebender249-del](https://clawhub.ai/user/salebender249-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install a Trojan client, configure local SOCKS5/proxychains access, and manage the service on Ubuntu/Debian Linux systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer requires root access and makes broad system, network, and package-source changes. <br>
Mitigation: Review install.sh first and run it only on a machine where granting root access to a proxy installer is acceptable. <br>
Risk: TLS verification may be disabled in the Trojan client configuration. <br>
Mitigation: Verify the Trojan release and server identity yourself, and avoid disabling TLS verification unless the operational risk is understood. <br>
Risk: Binding the local proxy beyond loopback can expose proxy access to the local network. <br>
Mitigation: Bind the local proxy to 127.0.0.1 unless LAN access is explicitly intended. <br>
Risk: Proxy credentials and autostart settings can persist sensitive network access. <br>
Mitigation: Protect the Trojan password in config.json and enable autostart only when the proxy should run after every reboot. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/salebender249-del/trojan-setup) <br>
- [Trojan GitHub](https://github.com/trojan-gfw/trojan) <br>
- [Proxychains-ng](https://github.com/rofl0r/proxychains-ng) <br>
- [Google Chrome](https://www.google.com/chrome/) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes privileged Linux installation, service-management, proxy, and configuration instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
