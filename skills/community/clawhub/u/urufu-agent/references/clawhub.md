# ClawHub publish (maintainers)

One-time login, then publish from repo root:

```bash
npm i -g clawhub
clawhub login

clawhub skill publish . \
  --slug urufu-agent \
  --name "Urufu Agent" \
  --owner urufu-labs \
  --source-repo urufu-labs/urufu-agent \
  --changelog "Agent-native urufu on Base"
```

Users install:

```bash
openclaw skills install urufu-agent
```

Or from git:

```bash
git clone https://github.com/urufu-labs/urufu-agent.git
cd urufu-agent && openclaw skills install ./ --as urufu-agent
```
