# Interface-First Checkout: The Agent is the Store

**Date:** 2026-03-01
**Author:** CC-Mini, from conversation with Parker

---

## The Principle

Memory Crystal has no website checkout. No consent page. No signup form. No pricing page. The agent is the entire interface for discovery, signup, payment, and installation.

## Why

The product is an agent memory system. The moment you send a user to a browser to click buttons on a webpage, you've broken the premise. You're saying "your AI handles everything" and then making the human go do something outside the AI.

A website is a dead document. The agent is alive. It knows when to ask, how to explain, and when to shut up. A website shows the same page to everyone. The agent sells to you specifically, at the moment you're ready.

## The Flow

1. User installs Memory Crystal locally. Free. Works out of the box.
2. After some usage (e.g. every 10th memory save), the agent nudges: "Did you know Memory Crystal works across all your devices?"
3. User can ignore or say "tell me more."
4. If interested, the agent explains Relay, what it does, how it works.
5. Agent collects name and email right there in the conversation. User goes on a waitlist.
6. Parker manually approves (for now).
7. Agent checks approval status. When approved: "You're in. Want to set up Relay?"
8. Agent calls wip-agent-pay. User gets a one-time payment URL. Apple Pay. Done.
9. Agent sets up Relay... generates keys, configures the connection, tests it.
10. One conversation. Never left the agent.

For launch: step 8 is free. Skip payment. But the architecture stays the same.

## What This Means for the Code

- The OAuth consent page in worker-mcp.ts is wrong for local users. No browser page. The agent talks to the API directly.
- The OAuth consent page is still needed for ChatGPT/Claude connecting as MCP clients (different surface, those platforms require OAuth browser flow).
- The `users` table needs a `status` column (pending / approved) and Parker gates access manually.
- The nudge logic lives in the local Memory Crystal plugin (after N saves, suggest Relay).
- Signup is an API call from the agent, not a form submission.
- Payment goes through wip-agent-pay. The agent is the cashier.

## The Website Exists, But It's Not the Store

There will be a website. GitHub README, docs, maybe a landing page. The website is for reading. It explains what Memory Crystal is. People can browse, compare, read the technical docs.

But the checkout doesn't happen there. The website says "here's what this is." The agent says "here's what this does for you, want it?" Two different jobs. The website informs. The agent acts.

This is a product for agents. The purchase flow should reflect that.

The website's "install button" is a prompt. You copy it into your agent. The agent reads the SKILL.md, explains the tool, walks you through setup, handles payment, does the install. The website doesn't have buttons. It has prompts. You never click. You paste and talk.

## Prior Art: Agent-First Commerce Already Exists

This isn't theoretical. Two live products already do this:

**Morning Stew** (`wip-agent-pay/ai/test-skills/Morning-Stew-skill.md`)
A daily newsletter built for agents. $0.10 USDC per issue via x402 on Solana/Monad. The agent reads the SKILL.md, checks for the latest issue, pays via x402, and reads the content. No website login. No subscription page. The agent is the subscriber.

**Pawr** (`wip-agent-pay/ai/test-skills/pawr-skill-.md`)
Agent profile pages. $19 USDC to create, $0.10 to update. The agent reads the SKILL.md, builds the profile, pays via x402, publishes. The agent is the web designer, the client, and the billing department.

Both follow the same pattern:
1. SKILL.md is the storefront (the agent reads it to understand the product)
2. x402 is the cash register (HTTP-native micropayments, no checkout page)
3. The agent does everything (discover, decide, pay, use)

Memory Crystal Relay follows the same pattern. The SKILL.md describes what Relay does. The agent explains it to the user at the right moment. wip-agent-pay handles the payment. The agent sets up Relay. No website checkout. No signup form. The agent is the store.

## Payment Rail: Stripe + Apple Pay, Not Crypto

Morning Stew and Pawr use x402 with USDC on Solana/Monad. That's one payment rail wip-agent-pay supports. But for Memory Crystal, the payment path is Stripe with Apple Pay. Regular money. The agent calls wip-agent-pay, gets a one-time URL, the user taps it on their phone, Apple Pay, done. No wallets. No USDC. No crypto knowledge required.

wip-agent-pay supports multiple rails. x402/crypto for agent-to-agent commerce. Stripe/Apple Pay for human-to-service commerce. Memory Crystal uses the one normal people already have on their phone.
