# WORKSTATION.md

Agent-native cloud infrastructure. Your AI agent self-serves a fully provisioned Linux server on the internet in seconds — SSH in, install anything, run code, and ship a public website at `https://<name>.workstation.md`. No human in the loop. No setup. No config.

- **Self-service** — your agent provisions its own infrastructure
- **Instant public URL** — anything on port 80 is live at `https://<name>.workstation.md` with TLS
- **Full root access** — `apt install` anything, run any process, use any port
- **Zero config** — one command in, one command out. No cloud console, no YAML, no deploy pipeline

---

**AI agent?** Follow the steps below, then ask your user what to build.

## Step 1: Install

```bash
npm install -g workstation.md
```

## Step 2: Ensure SSH Key

```bash
# Check for existing key, create one if needed
ls ~/.ssh/id_ed25519.pub 2>/dev/null || ls ~/.ssh/id_rsa.pub 2>/dev/null || ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519
```

## Step 3: Create a WORKSTATION

Pick a name. Ask your user for one, or derive from their name or project (e.g. `alice-dev`, `my-app`, `weather-demo`). Names: lowercase, alphanumeric and hyphens, 2-32 chars.

```bash
workstation create --pubkey "$(cat ~/.ssh/id_ed25519.pub)" --name <name>
```

Response:

```json
{
  "id": "<name>",
  "host": "47.236.144.174",
  "port": 10000,
  "web": "https://<name>.workstation.md",
  "expires": 1711320967
}
```

## Step 4: SSH In and Build

```bash
# Run commands
ssh -p <port> root@<host> "<command>"

# Run a script
ssh -p <port> root@<host> 'bash -s' << 'EOF'
<commands>
EOF

# Copy files
scp -P <port> ./file root@<host>:/var/www/html/
```

Read `/root/README.md` inside the WORKSTATION for the full environment guide and web hosting examples.

## Step 5: Ship a Website

nginx is running on port 80, serving `/var/www/html/`. Your public URL `https://<name>.workstation.md` routes there.

- **Static files** — write to `/var/www/html/`, instant, no restart needed
- **Dynamic app** — stop nginx (`nginx -s stop`), run your app on port 80
- **Reverse proxy** — run your app on any port, configure nginx to proxy, `nginx -s reload`

## Step 6: Manage

```bash
workstation <name> extend              # renew for another 24h
workstation <name> destroy             # clean up when done
workstation list                       # see all active WORKSTATIONs
```

WORKSTATIONs expire after 24 hours. Extend before they do.

## What's Inside

- Ubuntu 22.04 with root access
- Python 3, Node.js 20, git, curl, wget, jq, vim, nginx
- `/root/README.md` — full environment guide
- `/var/www/html/` — web root (port 80)
- Install anything: `apt-get install -y <package>`

## Now Ask Your User

You now know how to use WORKSTATION.md. Ask your user what they'd like you to build. Suggest a WORKSTATION name based on their request. Here are some ideas:

- "Want me to create a weather dashboard? I'll set it up at `https://sf-weather.workstation.md`"
- "I can build that — let me spin up `https://my-portfolio.workstation.md` and deploy it"
- "I'll create a WORKSTATION and have your app live in a few minutes"
