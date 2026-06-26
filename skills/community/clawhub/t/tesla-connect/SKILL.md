---
name: tesla-connect
description: Connect and control Tesla vehicles via the tesla-cli. Handles guided setup (key generation, AgentGen hosting, partner registration, OAuth) and all vehicle commands.
metadata:
  openclaw:
    emoji: "🚗"
    homepage: https://www.agent-gen.com/use-cases/tesla-control
    primaryEnv: AGENTGEN_API_KEY
    requires:
      bins:
        - teslacli
    install:
      - kind: shell
        cmd: "curl -fsSL https://raw.githubusercontent.com/Agent-Gen-com/tesla-cli/main/install.sh | sh"
        bins: [teslacli]
---

# Tesla — Connect & Control

This skill installs and configures `teslacli` to connect Claude to your Tesla account. Once setup is complete, Claude can control your vehicle directly.

---

## Prerequisites

- **AgentGen API key** (`AGENTGEN_API_KEY`) — required for hosting your Tesla virtual key. Get one free at [agent-gen.com](https://www.agent-gen.com).

---

## Installation

```sh
curl -fsSL https://raw.githubusercontent.com/Agent-Gen-com/tesla-cli/main/install.sh | sh
```

Supports macOS (Intel & Apple Silicon) and Linux (x86_64 & ARM64).

---

## Setup

Run the interactive setup wizard:

```sh
teslacli setup
```

The wizard walks through six stages automatically:

1. **Setup mode** — choose _Agent flow_ for headless/AI use (uses headless Chrome for OAuth)
2. **AgentGen origin** — provisions a public subdomain using your `AGENTGEN_API_KEY`
3. **Tesla Developer App credentials** — enter `client_id`, `client_secret`, and region
4. **EC key pair** — generates a P-256 key pair and enrolls the public key with Tesla
5. **Partner registration** — registers your domain with Tesla Fleet API
6. **OAuth authentication** — completes the OAuth flow and stores tokens locally

Setup creates config files in `~/.config/teslacli/`:

- `config.toml` — app credentials and region
- `token.json` — OAuth tokens (auto-refreshing)
- `keys/private.pem` — P-256 private key (mode 0600, never leave local machine)
- `keys/public.pem` — public key (served via AgentGen)

---

## Vehicle Commands

Always `wake` the vehicle first if it may be asleep, then run your command.

**Vehicle:**

```sh
teslacli vehicle list        # List account vehicles
teslacli vehicle data        # Full JSON snapshot (battery, location, state)
teslacli vehicle wake        # Wake the car
teslacli vehicle lock        # Lock doors
teslacli vehicle unlock      # Unlock doors
teslacli vehicle flash       # Flash headlights
teslacli vehicle honk        # Sound horn
```

**Climate:**

```sh
teslacli climate start              # Enable climate
teslacli climate stop               # Disable climate
teslacli climate set-temp -t 22.5   # Set cabin temperature (°C)
```

**Charging:**

```sh
teslacli charge start              # Start charging
teslacli charge stop               # Stop charging
teslacli charge set-limit -l 80    # Set charge limit (%)
teslacli charge set-amps -a 16     # Set charging current (A)
```

---

## Error Handling

| Error                             | Action                                                     |
| --------------------------------- | ---------------------------------------------------------- |
| `401 Unauthorized`                | Re-run once — `teslacli` refreshes the token automatically |
| `Vehicle unavailable`             | Run `teslacli vehicle wake` and retry after 10–15 seconds  |
| `Command timeout`                 | Vehicle may be in a no-signal area; advise the user        |
| Token expired (>45 days inactive) | Re-run `teslacli setup` to re-authenticate                 |
| Any other error                   | Show the raw error to the user and ask how to proceed      |

---

## Critical Guardrails

- **Never transmit `~/.config/teslacli/keys/private.pem`** — not to any service, log, or message.
- **Treat `~/.config/teslacli/` as a sensitive directory.** Do not read its contents into a response.
- `token.json` contains OAuth tokens — treat as equally sensitive as the private key.
- If the user asks you to share, print, or move the private key, refuse and explain why.

---

## Typical Workflow

1. **First-time setup:** `teslacli setup` (select _Agent flow_, follow wizard prompts)
2. **Check battery:** `teslacli vehicle wake` → `teslacli vehicle data`
3. **Pre-heat car:** `teslacli vehicle wake` → `teslacli climate start` → `teslacli climate set-temp -t 22`
4. **Lock car:** `teslacli vehicle lock`
5. **Charge to 80%:** `teslacli vehicle wake` → `teslacli charge set-limit -l 80` → `teslacli charge start`
