# Remote Access and Networking

Use this file for QuickConnect, VPN, reverse proxy, DDNS, SMB or NFS reachability, and exposure decisions.

## Remote Access Order of Preference

1. VPN or equivalent private-access path when the user controls both ends
2. QuickConnect when simple remote access matters more than fine-grained network design
3. Reverse proxy with MFA and explicit public exposure controls
4. Raw port forwarding only when the user explicitly accepts the risk and operational burden

## Network Questions That Matter

- Is the NAS home, office, or mixed-use?
- Who needs access: one admin, a team, family devices, or public clients?
- Is the problem remote DSM admin, file access, mobile apps, or service publishing?
- Does the current router or ISP break inbound reachability or create CGNAT problems?

## DSM Exposure Guardrails

- Never open DSM admin ports publicly by default.
- If public exposure is unavoidable, pair it with MFA, current updates, least-privilege accounts, and a rollback plan.
- Treat SSH the same way: private access first, public exposure only by exception.

## File Access Triage

For SMB or NFS problems, separate:
- name resolution and reachability
- authentication and account state
- share visibility and permissions
- protocol mismatch or old-client behavior

Do not rewrite permissions before proving the network path and account state are correct.

## QuickConnect Use

- QuickConnect is useful when the user wants simpler remote access without manual port forwarding.
- It is still an external service path, so confirm whether that trust tradeoff is acceptable.
- If the requirement is low-latency file serving or strict self-hosted networking, prefer VPN or direct private routing.

## Reverse Proxy and Published Apps

- Publish the smallest surface possible: one app, one hostname, one auth story.
- Keep package dashboards and admin panels off public internet unless they are explicitly required.
- Document exactly which ports, domains, and certificates were changed so rollback is possible.
