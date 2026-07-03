# Example Prompts

Use these as trigger examples for Tunly Artifact Share.

- Publish this Codex-generated acceptance report as a private Tunly artifact and verify the version link.
- Turn this Claude HTML artifact into a durable share link with account-only access.
- Create a review page for this architecture plan, publish it through Tunly, and confirm unauthenticated users cannot read it.
- Publish this dashboard as a public Tunly artifact and give me latest plus immutable version URLs.
- Bundle these logs and screenshots as evidence, redact sensitive text first, then publish privately.
- Update the latest review link but preserve the previous version for audit.
- I do not have a Tunly account yet; guide me through registration before publishing.

## Expected Final Answer

```text
Published: https://...
Version: https://...
Access: private, unauthorized fetch returned 404/403
Verified: latest fetch, version fetch, sentinel title, no local-server dependency
Unverified: none
```
