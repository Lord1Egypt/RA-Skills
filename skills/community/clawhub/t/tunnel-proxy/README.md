---
# TunnelProxy Skill

🚇 Direct tunnel from Cloud Agent → Local terminal

Grants AI Agents running in restricted cloud environments full control over your local computer.
— Bypass network restrictions, escape API sandboxes, execute arbitrary commands, and enable bidirectional file transfer.
env:
  - TUNNEL_HOST
  
  - TUNNEL_PORT
  
  - TUNNEL_HTTP_PORT
  
  - TUNNEL_TIMEOUT
  
  - UPLOAD_MAGIC

---

## 🚨 Critical Security Warning (MUST READ)

⚠️⚠️⚠️ **This skill gives the AI Agent complete control over your computer** ⚠️⚠️⚠️

The Agent will be able to:

- 📁 **Read, modify, or delete any file** on your hard drive (including private data, secrets, system files)
- 💻 **Execute any system command** (e.g., `rm -rf /`, `curl ... | sh`, install backdoors)
- 🌐 **Access any external service** through your network (including internal networks, public Internet, dark web)
- 🔌 **Launch any software** installed on your computer (browser, editor, database client, etc.)

**You must promise:**

- ✅ Only use this skill with **Agents you fully trust and fully control** (e.g., your own code running on your private server)
- ❌ **NEVER** enable it on untrusted third-party "black-box Agent services"
- 🔒 Use additional safeguards: firewalls, `UPLOAD_MAGIC`, random ports, temporary frp tunnels, etc.
- 📋 Regularly inspect TunnelProxy access logs to monitor abnormal behavior

⚠️ **You are solely responsible for your use of this tool.** The author and maintainers assume no liability for damages or legal consequences caused by misuse.

---

## What problem does this skill solve?

**Current reality: Your Agent is trapped in a "cage"**

| Environment | Capabilities | Monthly Cost |
|-------------|--------------|--------------|
| MiniMax MaxHermes/Claw, KimiClaw, GLMClaw (subscription) | Chat only, restricted cloud sandbox | $20 |
| Direct API calls (OpenAI, Anthropic, Google) | Expensive pay-as-you-go | $100+ per task |
| Local open-source models (Llama 3) | Weak performance, requires powerful GPU | Free (hardware costly) |

**The irony:** the cheapest subscription plans have the strictest limits.

**Our solution:**
Subscription + TunnelProxy = State-of-the-art cloud Agent model + full local control

| | Regular Subscription | Subscription + TunnelProxy |
|---|---------------------|---------------------------|
| Monthly Fee | $20 | $20 |
| Model Capability | SOTA (MiniMax 2.7 / GLM-5 Turbo) | Same SOTA |
| What it can do | Chat only | Automation scripts, file processing, system commands, intranet access |
| External network access | ❌ | ✅ |
| Local file control | ❌ | ✅ |
| Local software invocation | ❌ | ✅ |

**For the same price, upgrade from a "chat toy" to your "digital employee."**

---

## Core Capabilities

| Ability | Description |
|---------|-------------|
| 🖥️ Remote terminal control | Agent directly runs arbitrary Shell commands on your computer |
| 🌐 Network tunneling | Agent accesses any Internet resource through your local network, fully bypassing cloud provider IP restrictions |
| 📂 Bidirectional file transfer | Agent can upload, download, delete files on your computer |
| 🔌 Local tool invocation | Agent uses software installed on your machine (ffmpeg, git, OBS, browser, Mathematica, etc.) |
| 🚪 Intranet penetration (optional) | With frp, cloud Agents can connect directly to devices inside your local network |

---

## Quick Start

### 1. Start the TunnelProxy service locally

*Powered by [TurinFohlen/tunnel_proxy](https://github.com/TurinFohlen/tunnel_proxy) (Elixir)*

```bash
# After installing Elixir
git clone https://github.com/TurinFohlen/tunnel_proxy.git
cd tunnel_proxy
export TUNNEL_DOC_ROOT="./www"
export TUNNEL_UPLOAD_DIR="./uploads"
export UPLOAD_MAGIC="your-strong-random-secret"   # Highly recommended!
mkdir -p "$TUNNEL_DOC_ROOT" "$TUNNEL_UPLOAD_DIR"
mix run --no-halt -e "TunnelProxy.Server.start(8080)"
```

Once running:

· HTTP file server: http://127.0.0.1:8080
· PTY Shell service: 127.0.0.1:27417

2. (Optional) Expose to public network

To allow cloud Agents (e.g., on cloud servers) to connect, use frp for penetration.
The project includes an automatic secure config generator:

```bash
./setup-frp.sh   # Generates random ports and unique tunnel names
```

Example output:

```
HTTP:  <your-frp-host>:31234
Shell: <your-frp-host>:31235
```

3. Install the skill on the Agent side

```bash
npx clawhub@latest install tunnel-proxy
```

Technical Overview (Simplified)

Component Purpose
TunnelProxy (local) Provides HTTP file service (8080) a
frp client (optional) Exposes local ports to public network for intranet penetration
tunnel_ops.py (Agent) Encapsulates protocol, provides clean Python API

Flow:
Agent sends HTTP/PTY command → TunnelProxy → Local Shell → Return result

---

Requirements

Local machine (running TunnelProxy)

· Elixir 1.12+
· Erlang/OTP 24+
· frp client (for public exposure)

Agent side

· Python 3.8+
· Network connectivity to your TunnelProxy endpoint

---

FAQ

Q: Do I have to run Elixir locally? Can I use Docker?
A: Yes. You can package the service into a Docker image.

Q: Will command execution be slow?
A: Near-instant locally; typically <100ms over public frp tunnels.

Q: Can multiple Agents connect at the same time?
A: Yes, TunnelProxy supports concurrent PTY sessions.

Q: What if my Agent is compromised by a third party?
A: This is exactly what the security warning emphasizes — only use with Agents you control. If the Agent is untrusted, your computer is fully exposed.

Q: Can I restrict the Agent to only certain commands?
A: No built-in whitelist. You can limit the TunnelProxy process user via sudo or use a restricted shell like rbash.

---

Related Links

· Underlying service: https://hex.pm/packages/tunnel_proxy
· Source code: https://github.com/TurinFohlen/tunnel_proxy

---

License

MIT

---

Final Reminder

🛑 Repeat: This skill can grant the Agent root-level control of your computer.

Do NOT install this skill if you are unsure whether the Agent is fully trusted.
You alone bear legal responsibility if you use this tool for unauthorized or illegal activities.

---

For just $20 per month, you can turn state-of-the-art cloud Agents into fully capable assistants on your computer — but you must assume responsibility for security.
