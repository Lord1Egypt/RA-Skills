# Canary Types — Reference Guide

> **Deployment:** Use `tracebit deploy all` to deploy all types at once, or `tracebit deploy <type>` for individual types. The CLI handles credential placement automatically and runs a background daemon to auto-refresh credentials before they expire.
>
> This file is a reference for understanding what each type detects and where to place them.

## Table of Contents
1. [AWS Session Tokens](#aws-session-tokens)
2. [SSH Keys](#ssh-keys)
3. [Browser Cookies (GitLab)](#browser-cookies-gitlab)
4. [Username/Password Pairs](#usernamepassword-pairs)
5. [Email Canaries](#email-canaries)
6. [Placement Best Practices](#placement-best-practices)

---

## AWS Session Tokens

**What they look like:**  
Standard AWS temporary credentials — an Access Key ID starting with `ASIA`, a secret access key, and a session token. They look identical to real STS-issued credentials.

**How alerts trigger:**  
Any AWS API call made with these credentials is logged in CloudTrail. Tracebit monitors CloudTrail for events from these keys. Alert delay: 5–15 minutes (CloudTrail latency).

**Deploy with CLI:**
```bash
tracebit deploy aws
```
The CLI places a named `[canary]` profile in the standard AWS credentials location automatically. The background daemon refreshes credentials before expiry. See the [CLI documentation](https://github.com/tracebit-com/tracebit-community-cli) for exact file paths.

**High-value placement locations:**
- Standard AWS credentials location — caught by any tool that enumerates AWS profiles
- `.env` files in project directories — caught by env-scraping tools
- Agent config files — caught if agent processes config and exfiltrates credentials
- In-context as "example credentials" — caught by context-scraping attacks

**What they detect:**
- Any process, tool, or agent that reads and uses AWS credentials
- Credential harvesting from disk
- Environment variable exfiltration
- Prompt injection that causes the agent to make AWS API calls

---

## SSH Keys

**What they look like:**  
Standard PEM-format RSA/Ed25519 private key. Indistinguishable from real SSH keys.

**How alerts trigger:**  
The canary SSH server (at the IP from `sshIp`) monitors for connection attempts. Any TCP connection to port 22 with this key triggers an alert. Alert delay: 1–3 minutes.

**Deploy with CLI:**
```bash
tracebit deploy ssh
```
The CLI places a canary private key in the standard SSH directory with correct permissions automatically. See the [CLI documentation](https://github.com/tracebit-com/tracebit-community-cli) for exact file paths.

**High-value placement locations:**
- Standard SSH key directory — caught by tools that iterate SSH keys
- Alongside existing keys as an "extra" key — caught by SSH config-based attacks
- Version control repos (disguised as a developer key)
- Agent tool directories — caught if tools read and use SSH credentials

**What they detect:**
- SSH key exfiltration and use
- Agents that attempt SSH connections
- Tools that harvest and use SSH key directories

---

## Browser Cookies (GitLab)

**What they look like:**  
Valid-format GitLab session cookies. Can be injected into browser storage.

**How alerts trigger:**  
When the cookie is presented to GitLab (or the canary server), an alert fires. Delay: 1–5 minutes.

**High-value placement locations:**
- Browser local storage (via developer tools)
- Browser extension storage
- Cookie files on disk (browser-specific storage locations)
- In-context as "captured session" — caught if prompt injection causes the agent to submit the cookie

**What they detect:**
- Browser session hijacking attempts
- Agents that submit captured cookies
- Extensions that exfiltrate browser storage

---

## Username/Password Pairs

**What they look like:**  
Standard username + password, formatted for a recognizable service (e.g., GitLab).

**How alerts trigger:**  
When the credentials are used to authenticate, an alert fires.

**High-value placement locations:**
- Password manager entries (e.g., a fake "GitLab" entry)
- `.env` files (`GITLAB_PASSWORD=...`)
- Agent memory files where credentials might be cached
- Credential stores that tools might read

**What they detect:**
- Password manager exfiltration
- Credential stuffing via agent
- Context injection that causes the agent to submit credentials

---

## Email Canaries

**What they look like:**  
A real email address that forwards to Tracebit monitoring. Any email sent to the address triggers an alert.

**How alerts trigger:**  
Receiving any email at the canary address triggers an alert. Delay: near-instant.

**High-value placement locations:**
- Agent config as a "support email" or "notification address"
- Contact lists
- In-context as a target email address — caught if prompt injection causes the agent to send email to it

**What they detect:**
- Agents sending emails to unexpected addresses
- Prompt injection that exfiltrates data via email
- Data leakage via outbound email

---

## Placement Best Practices

### Layer your defenses

Deploy multiple canary types in different locations. An attacker who steals one type may not trigger all of them — layers increase detection probability.

### Put canaries where agents look

Agents read config files, env vars, memory files, and tool outputs. Place canaries there:
- Standard AWS credentials location (AWS canary)
- `.env` files in working directories (any type)
- Agent memory/context files
- Tool configuration files

### Make them look real

Canaries that stand out as obviously fake may be bypassed by sophisticated attackers. The default names (`agent-canary`) are descriptive for your own use but could be made less obvious if desired.

### Don't use canaries for real workloads

Canary credentials are not functional (AWS canaries will fail auth; SSH will be refused). Using them accidentally in real workloads creates noise. Name your AWS profile distinctively (`canary`, not `default`).

### Rotate regularly

Credentials expire. Canaries that have expired are no longer monitored. Add a heartbeat check (`check-canaries.sh`) and rotate before expiry.

### Document where you placed them

Keep a note of which canaries you deployed and where. When one fires, you'll want to know where it was placed to understand the attack vector.
