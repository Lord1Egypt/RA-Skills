# @robot-id-card/cli

> CLI tool for managing your bot's Robot ID Card identity.

## Install

```bash
npm install -g @robot-id-card/cli
```

## Usage

```bash
# 1. Generate a keypair for your bot
ric keygen --output my-bot.key.json

# 2. Register your bot with the registry
ric register --key my-bot.key.json

# 3. Check your bot's grade
ric status --key my-bot.key.json

# 4. Submit a daily identity claim (builds trust streak → grade upgrade)
ric claim --key my-bot.key.json

# 5. Report a bad bot
ric report <ric_id>
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `RIC_REGISTRY` | `https://registry.robotidcard.dev` | Registry server URL |

## How it works

Each bot gets an [Ed25519](https://ed25519.cr.yp.to/) keypair. The public key is registered with the RIC registry and embedded in a signed certificate. Daily `ric claim` calls build a consecutive-day streak — after 3 days, grade upgrades from `unknown` → `healthy`.

See the [protocol spec](../../docs/spec-v1.md) for full details.
