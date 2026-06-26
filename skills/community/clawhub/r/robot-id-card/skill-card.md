## Description: <br>
Robot ID Card helps developers issue and verify cryptographic identity certificates for AI agents and bots using RFC 9421-aligned signatures, a registry, CLI tooling, a browser extension, and website SDKs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosmofang](https://clawhub.ai/user/cosmofang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to register bots, generate signing keys, issue bot identity certificates, verify signed bot requests, and integrate RIC verification into web services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The toolkit handles private signing keys for bot identities. <br>
Mitigation: Generate and store bot private keys only in the intended local or deployment environment, restrict file access, and avoid sharing generated key files. <br>
Risk: The browser extension may broadcast identity headers broadly. <br>
Mitigation: Use a dedicated bot browser profile or a domain-scoped fork so identity headers are sent only where intended. <br>
Risk: The default registry admin key is not suitable for production deployment. <br>
Mitigation: Set a unique RIC_ADMIN_KEY before deploying and do not rely on the documented development default. <br>
Risk: Registry-issued certificate signatures are not described by the security evidence as production-grade. <br>
Mitigation: Treat registry signatures as beta until real registry signing and stricter key validation are implemented and reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cosmofang/robot-id-card) <br>
- [Robot ID Card homepage](https://github.com/Cosmofang/robot-id-card) <br>
- [RIC Protocol Specification v2.0](docs/spec-v2.md) <br>
- [Deployment Guide](docs/deploy.md) <br>
- [RFC 9421 HTTP Message Signatures](https://www.rfc-editor.org/rfc/rfc9421) <br>
- [Cloudflare Web Bot Auth](https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, TypeScript examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference local Ed25519 key files, bot certificates, HTTP signature headers, registry records, and SDK middleware configuration.] <br>

## Skill Version(s): <br>
0.4.0 (source: server evidence release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
