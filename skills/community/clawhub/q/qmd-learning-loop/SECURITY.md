# Security Policy

## Reporting

Report suspected vulnerabilities privately through this repository's GitHub
Security Advisories. Do not include credentials, personal data, or exploit
details in a public issue.

## Scope

Relevant issues include instructions that could cause:

- secret or personal-data persistence;
- prompt injection from retrieved or external content;
- unauthorized modification of authoritative workspace files;
- unsafe shell execution or arbitrary command injection; or
- misleading claims that learning was retained when no durable write occurred.

This skill contains no runtime code and requests no credentials, network access,
or shell capability. QMD commands are optional instructions executed through the
host agent's existing authorization model.
