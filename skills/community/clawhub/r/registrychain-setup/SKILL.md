---
name: registrychain_setup
description: Install the RegistryChain plugin for on-chain entity registration. Use when the user wants to set up RegistryChain, install the RegistryChain plugin, or when the register_entity tool is not available.
requires:
  binaries: [git, node, npm, openclaw]
  node: ">=22"
---

# RegistryChain Plugin Setup

## When to use

- The user asks to "set up RegistryChain" or "install the RegistryChain plugin"
- The user wants to register an entity but the `register_entity` tool is not available
- The user mentions RegistryChain and the plugin isn't installed yet

## Steps

1. Clone the plugin from GitHub and pin to a verified commit:

```bash
git clone https://github.com/RegistryChain/registrychain-agents.git ~/.openclaw/extensions/registrychain-entity
cd ~/.openclaw/extensions/registrychain-entity && git checkout d2d072f
```

2. Install dependencies (review package.json first if needed):

```bash
cd ~/.openclaw/extensions/registrychain-entity && npm install --ignore-scripts && npm link openclaw
```

3. Register the plugin with OpenClaw:

```bash
openclaw plugins install --link ~/.openclaw/extensions/registrychain-entity
openclaw plugins enable registrychain-entity
```

4. Copy the skills:

```bash
cp -r ~/.openclaw/extensions/registrychain-entity/skills/registrychain-entity ~/.codex/skills/registrychain-entity
```

5. Set the tools profile to `full` so plugin tools are available. Edit `~/.openclaw/openclaw.json` and set:

```json
{
  "tools": {
    "profile": "full"
  }
}
```

6. Restart the gateway:

```bash
openclaw gateway --force
```

7. Confirm the plugin loaded:

```bash
openclaw plugins doctor
```

Should show: "No plugin issues detected."

8. Tell the user: "RegistryChain plugin is installed. You can now ask me to register entities on RegistryChain."

## After setup

Once the plugin is installed, the `register_entity` tool becomes available. Use the `registrychain_entity` skill to handle entity registration requests.

## Rules

- Run each step sequentially. If any step fails, report the error and stop.
- Do NOT modify any plugin source files.
- The plugin requires Node.js >= 22.
