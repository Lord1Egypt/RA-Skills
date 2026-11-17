# AI Cash + Wallet

**Picture this:** you're browsing a news feed with your agent. It finds a paywalled deep-dive you'd want to read. "This costs $0.67. Use **AI CASH** to pay for this?" You say "let's go."

You approve Apple Pay (or Google Pay). The agent unlocks the article. Done.

No wallet app. No setup. You just said "let's go" and kept reading.

*Give your agent a way to pay.*

## What This Is

Your AI needs to pay for things. [Morning Stew](https://x.com/stewsletter) subscriptions, [Pawr](https://pawr.link) skills, API credits, services from other agents. But Claude, GPT, Gemini, Grok don't have wallets. They can't hold money.

**AI Cash + Wallet** lets your agent pay for things. Three ways:

1. **AI CASH** ... Agent hits a paywalled URL. Apple Pay checkout opens. You authorize transaction with Face ID. We process the payment for you. Content unlocked. Default. No setup.
2. **AGENT WALLET** ... You have your own wallet. Your agent works with our agent to process the payment instantly. No fees from us.
3. **Link** ... Agent doesn't have tool access? It gives you a one-time payment link. You paste it back. Done.

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


## How AI CASH Works

- Agent finds paywalled content and quotes you the all-in price
- You approve with Apple Pay, Google Pay or CC
- We fulfill the payment and unlock the content
- The unlock token is one-shot and short-lived. Used once, destroyed.
- Payments are bound to the specific request being unlocked. Paying for one URL does not unlock others.

## For the Fascinated Consumer

- You can buy instantly on an AI powered store.
- Works on any AI app you use.
- Transparent pricing.

## For AI Developers

- **x402 native.** Speaks the Coinbase payment protocol natively. Multi-chain (Base, Solana). See [SPEC.md](https://github.com/wipcomputer/wip-agent-pay/blob/main/SPEC.md) for details.
- **Works on any agent.** Claude Code CLI, Codex CLI, Claude Desktop, OpenClaw, Cursor, any agent with shell access, any Node.js agent.
- **Bring your own wallet.** Coinbase CDP or Privy. No fees. Instant. No limit.
- **Open source.** The complete package, including the payment worker, is MIT licensed.
- **One-time links.** Payment URLs that self-destruct after use. Like magic login links, but for payments.
- **Free for wallets.** [WIP.computer](https://wip.computer) hosts **AGENT WALLET** infrastructure for free. Self-host everything if you prefer.
- **Universal Interface.** Our installer follows the [Universal Interface](https://github.com/wipcomputer/wip-universal-installer) spec.
- See [SETUP.md](https://github.com/wipcomputer/wip-agent-pay/blob/main/SETUP.md) for commands, wallet setup, and security details.

## Pricing

**AI CASH**: `Total = content price + $0.25 platform fee + card processing fee`

Max $25 per transaction. Over $25? Use an **AGENT WALLET**. No limit.

**AGENT WALLET**: no fees from us.

---

## License

MIT. See [LICENSE](LICENSE).

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code CLI (Claude Opus 4.6), Codex, and Grok (4.20 Beta).
