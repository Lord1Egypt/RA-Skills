# Agent Wallet

**Picture this:** your agent finds a paid API it needs. No checkout. No approval popup. It signs the payment from your wallet and gets the response. One round trip. Done.

No Stripe. No Apple Pay. No human in the loop. Your agent has its own money.

*Give your agent sovereignty.*

## What This Is

Your AI needs to pay for things. [Morning Stew](https://x.com/stewsletter) subscriptions, [Pawr](https://pawr.link) skills, API credits, services from other agents. Most payment tools require human approval every time.

**Agent Wallet** is the bring-your-own-wallet mode. You fund a wallet with USDC. Your agent settles payments directly on-chain via the [x402 protocol](https://github.com/coinbase/x402). No middleman. No fees from us. No limit.

## Install

Open your AI coding tool and say:

```
Read the SPEC.md and SKILL.md at github.com/wipcomputer/wip-agent-pay.
Then explain to me:
1. What is this tool?
2. What does it do?
3. What would it change or fix in our current system?

Then ask me:
- Do you have more questions?
- Do you want to install it?
- Do you want to use it to pay for something right now?
```

Your agent will read the repo, explain everything, and walk you through setup interactively.

## How AGENT WALLET Works

- Your agent hits a 402 gate
- It reads the payment requirements (price, chain, address)
- Signs the transaction from your wallet
- Replays the request with proof of payment
- Content unlocked. One round trip.

## For AI Developers

- **x402 native.** Speaks the Coinbase payment protocol natively. Multi-chain (Base, Solana). See [SPEC.md](https://github.com/wipcomputer/wip-agent-pay/blob/main/SPEC.md) for details.
- **Works on any agent.** Claude Code CLI, Codex CLI, Claude Desktop, OpenClaw, Cursor, any agent with shell access, any Node.js agent.
- **Bring your own wallet.** Coinbase CDP or Privy. No fees. Instant. No limit.
- **Open source.** The complete package, including the payment worker, is MIT licensed.
- **One-time links.** Payment URLs that self-destruct after use. Like magic login links, but for payments.
- **Free infrastructure.** [WIP.computer](https://wip.computer) hosts **AGENT WALLET** infrastructure for free. Self-host everything if you prefer.
- **Universal Interface.** Our installer follows the [Universal Interface](https://github.com/wipcomputer/wip-universal-installer) spec.
- See [SETUP.md](https://github.com/wipcomputer/wip-agent-pay/blob/main/SETUP.md) for commands, wallet setup, and security details.

## Wallet Options

### Coinbase CDP

Self-custody wallet via [Coinbase Developer Platform](https://portal.cdp.coinbase.com).

```bash
agent-pay pay <url> --wallet=cdp
```

### Privy

Server-side embedded wallet via [Privy](https://docs.privy.io).

```bash
agent-pay pay <url> --wallet=privy
```

## Pricing

No fees from us. You pay gas and any facilitator costs on-chain. That's it.

No transaction limit.

## AI Cash

Don't want to manage a wallet? Use [AI Cash](https://github.com/wipcomputer/wip-agent-pay/blob/main/CASH.md). Apple Pay / Google Pay. No setup. Max $25 per transaction.

**AI Cash is consent. Agent Wallet is sovereignty.**

---

## License

MIT. See [LICENSE](LICENSE).

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code CLI (Claude Opus 4.6), Codex, and Grok (4.20 Beta).
