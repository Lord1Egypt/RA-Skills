# TADA/Throo Ride Skill — Usage Guide

> This document is for the agent to consult when a user asks **what this skill is, how to get started, or why the skill is structured the way it is**. It is *not* a command reference — see `wallet.md`, `ride.md`, `tip.md`, and `chat.md` for command-level details. When answering a user, paraphrase from this document rather than pasting it back verbatim.

## Overview

### What this skill does

This skill lets you interact with **TADA/Throo** (TADA: [tada.global](https://tada.global); Throo: [ridethroo.ai](https://ridethroo.ai)), a ride-hailing service, through natural conversation with the agent. It covers most of the ride lifecycle:

- Searching available rides between two places
- Requesting and cancelling a ride
- Paying for the ride — with your registered card (as a TADA/Throo member) or in USDC via the [x402](https://www.x402.org) HTTP payment standard (with a crypto wallet)
- Chatting with the assigned driver in real time
- Tipping after the ride
- *(Coming soon)* Reviewing past rides

### Where it works

The underlying app itself operates in a number of cities — **TADA** in New York, Denver, Singapore, Bangkok, Ho Chi Minh, Hanoi, Phnom Penh, Siem Reap, Sihanoukville, Kampot, and Hong Kong, and **Throo** currently in New York only.

**This skill enables a subset of those cities: New York (NYC), Singapore (SIN), Hong Kong (HKG), and — in Cambodia — Phnom Penh (PNH), Siem Reap (REP), Sihanoukville (SHV), and Kampot (KPK).** A city that is not on this list is not supported here; the skill does not fall back to a nearby city or region. Support for additional cities is rolling out over time.

### Who's behind it

TADA/Throo is operated by the TADA team — see [tada.global](https://tada.global) (Throo: [ridethroo.ai](https://ridethroo.ai)) for the official site. This skill is the official integration that lets agents (Claude Code, OpenClaw, …) interact with TADA/Throo on the user's behalf. Bug reports and feedback should go through the repository this skill ships from.

### What you need to get started

Always needed, regardless of how you pay:

- **Node.js 22.22.0 or newer** on a host that supports skills (Claude Code, OpenClaw, …)

Then it depends on which payment mode you choose:

- **TADA/Throo member (card payment)** — a TADA/Throo account with a registered payment card, signed in through the TADA/Throo app. **No wallet, crypto, collateral, gas token, or USDC is required on this path.**
- **Crypto wallet (USDC payment)** — a built-in **Privy** wallet or your **MetaMask** wallet, a small amount of **USDC** or **MVL token** to deposit as collateral, a small amount of the deposit chain's **native gas token** for the deposit transaction fee, and separate USDC for ride fares (collateral and fares are different things — see below).

You do not need any other crypto knowledge to use the skill — the agent walks you through every step.

### What you are authorising

Worth reading once before your first ride, because it is easy to skip past.

This skill lets an agent **spend your money**. It can request a ride that charges your saved card, pay a fare from your wallet, tip a driver, and move USDC between chains. Those are the things it is for, but they are real transactions.

**How often the agent asks you first is decided by your agent host, not by this skill.** The skill's instructions ask for confirmation before paying steps, and an agent that is configured to act autonomously can still be allowed to skip them — for example, requesting a ride between saved locations and settling the fare without prompting you each time. If you want a hard gate, set it at the host level: most hosts can require approval per command. Do not rely on the skill to enforce it.

Two more things it does on your machine:

- It keeps **saved places** in a local database so repeat rides are quick, and caches ride state there too. That is a record of where you go. Deleting the state directory removes the local copy (see the uninstall answer in the FAQ), but it is not the only copy: your **ride history lives on TADA/Throo's servers** the same as it would if you booked from their app, and **saving a place sends that place to them too**. What data goes where is spelled out in the FAQ.
- If you choose built-in Privy, it stores encrypted **wallet key material** under the state directory. Treat that directory the way you would treat a password manager's data. MetaMask keeps its keys outside the skill; the member path creates no wallet keys.

---

## First ride walkthrough

This section explains *what happens at each step* and *why the order matters*. For the actual commands, see the per-feature references.

### 1. Choose how you'll pay
First choose a payment mode. This choice drives ride **pricing** and which backend serves you — member and crypto are priced differently — so it is made explicitly before any wallet is created or connected:

- **TADA/Throo member (card)** — pay with a card registered in the TADA/Throo app.
- **Crypto wallet (USDC)** — pay from your wallet in USDC.

You can also decide later; that leaves the account unconfigured until you choose a path before booking. Searching for a ride, requesting it, and chatting with the driver are similar on both paths; sign-in, readiness checks, command arguments, and payment differ.

### Member path — card payment

**M1. Sign in with the TADA/Throo app.** There is no password: the agent starts a device-flow login, shows an approval link (and a QR code), you approve in the TADA/Throo app, and the app displays a 4-digit code you hand back to the agent. **No wallet, SIWE, collateral, or USDC on this path** — your account and payment card already live in the app.

**M2. Search, request, ride.** Tell the agent where you're going; it resolves the places, shows available cars and fares, and books the one you pick. When the ride completes, the fare is charged to your registered card.

### Crypto path — wallet payment

**C1. Choose and set up a wallet.** Pick the built-in **Privy** wallet (recommended) or connect **MetaMask**. The agent waits for your provider choice and any required approval; it never provisions one merely because the skill was installed.

**C2. Sign in with your wallet (SIWE).** The first time the agent talks to TADA's backend it proves you control the wallet with a **Sign-In With Ethereum (SIWE)** message — a short text the wallet signs once, which the backend exchanges for a session. No password and no email/SMS code; the wallet itself is your identity.

**C3. Verify your phone number.** Accounts on this path are tied to a verified phone number, mostly so drivers can contact riders if needed. The agent triggers an SMS OTP and asks you to type the code back. This only happens once per phone number.

**C4. Deposit collateral into TADA's deposit contract.** Before you are eligible to request rides on this path, you stake collateral — **USDC or MVL token** — into TADA's on-chain deposit contract. This is a one-time on-chain transfer. **It is *not* a prepaid balance that ride fares are deducted from.** Your collateral stays on-chain and can be withdrawn later when you no longer need access. This step requires the collateral itself plus a small amount of the chain's native gas token to pay the deposit transaction fee. Note: whichever token you deposit, your collateral is credited and returned as the **MVL token** — a USDC deposit is converted to an MVL credit, and a withdrawal returns MVL, not USDC.

**C5. Search, request, ride.** The agent resolves both places into TADA "places" via autocomplete + an interactive map session, then queries available cars: how long the wait is, which classes are available, and what each one costs, and books the one you pick. (Origin and destination must currently be inside a city this skill supports — NYC, SIN, PNH, REP, SHV, KPK, or HKG.)

**C6. Pay for the ride with x402 (USDC).** Ride payment is **completely separate from collateral**. After the ride completes, the agent settles the fare using **x402**, an HTTP-native payment protocol where the server tells the client exactly how much to pay and the client pays inline as part of the same request. The fare is paid out of your wallet's USDC balance — it does **not** draw from the deposit contract. Your collateral stays put.

### After the ride (both paths)
While the ride is active, you can chat with the driver in real time. After it ends you can send a tip, charged the same way your fare was — to your card as a member, or in USDC on the crypto path. Past-ride review is currently in development.

---

## How wallets work in this skill

Understanding this is optional for casual use, but useful if you want to know exactly where keys live.

### Privy embedded wallets
The skill uses [Privy](https://privy.io), an embedded-wallet provider that splits a wallet's signing capability across multiple parties so no single place holds a complete private key.

- **The skill never stores a raw private key on disk.** Anywhere.
- Instead, the skill holds a local **quorum key** — a credential that authorises the skill to ask Privy to co-sign on your behalf. The quorum key alone cannot sign anything; signing requires both the local quorum key *and* Privy's side together.
- The quorum key lives in `~/.amb/keys` (or the `AMB_RIDE_STATE_DIR` equivalent) and is bound to your local agent installation.
- **If you delete the keys directory, this machine loses the ability to ask Privy to sign for that wallet.** The wallet still exists on Privy's side, but you would need to recover access through Privy's normal flow rather than from this skill alone. Treat the keys directory like an SSH key folder — back it up if you care about the wallet.

---

## FAQ

### About

**What is TADA/Throo?**
TADA/Throo is a ride-hailing service — see [tada.global](https://tada.global) (TADA) or [ridethroo.ai](https://ridethroo.ai) (Throo). The skill is a connector that lets an agent book and pay for TADA/Throo rides on your behalf.

**Where can I use TADA/Throo through this skill?**
The underlying app operates in multiple cities — **TADA** in New York, Denver, Singapore, Bangkok, Ho Chi Minh, Hanoi, Phnom Penh, Siem Reap, Sihanoukville, Kampot, and Hong Kong, and **Throo** in New York only — but **this agent skill currently enables New York (NYC), Singapore (SIN), Phnom Penh (PNH), Siem Reap (REP), Sihanoukville (SHV), Kampot (KPK), and Hong Kong (HKG)** (regions `NY`, `SG`, `KH`, `HK`). Anywhere else is rejected rather than redirected. More cities will be added over time.

**Is this skill official?**
Yes — it is the official integration shipped by the TADA team.

**Where do I report bugs or send feedback?**
Through the repository this skill ships from. Issues filed there are seen by the maintainers.

### Getting started

**I'm new — what's the first thing I should do?**
Tell the agent something like *"install tada-ride"*, then *"I want to book a ride"*. The agent runs the install script and first asks how you want to pay. If you pick the **TADA/Throo member** path it signs you in without creating a wallet; if you pick **crypto**, it asks whether to use Privy or MetaMask before walking through SIWE login, phone verification, and the initial collateral deposit. After that, you can ask for a ride directly.

**Do I really need crypto to use this?**
Only on the crypto-wallet path. If you sign in as a **TADA/Throo member**, you pay with a card registered in the app and need **no** USDC, collateral, or gas token. On the **crypto** path, both the deposit step (eligibility) and ride payment are on-chain, so you need:
- a small amount of **USDC** or **MVL token** to deposit as collateral,
- a small amount of the deposit chain's **native gas token** to pay the deposit transaction fee, and
- some **USDC** for actually paying ride fares afterwards.

Either way, you do not need any crypto knowledge beyond approving the steps the agent walks you through.

**Can I use my own wallet instead of the built-in one?**
Yes. On the crypto path, choose **MetaMask** to connect an external wallet controlled through the MetaMask Agent Wallet CLI; the skill never receives its private key. Or choose the built-in Privy wallet. TADA/Throo members need neither.

### How it works — concepts

**Why USDC for ride payment?**
On the **crypto** path, USDC is a USD-pegged stablecoin available across the chains TADA/Throo supports. That keeps the price you see stable from quote to settlement, and lets the same payment flow work in every supported region without per-currency conversion. (TADA/Throo members pay by card instead and never touch USDC.)

**Why do I have to deposit anything up front? Isn't paying per ride enough?**
This applies to the **crypto** path only — TADA/Throo members pay by card and deposit nothing. On the crypto path the deposit is a **separate, one-time eligibility step** — not a prepaid fare balance. TADA/Throo requires crypto-wallet users to stake some collateral (USDC or MVL token) into its on-chain deposit contract before they can request rides. Per-ride fares are paid separately at the end of each ride out of your wallet's USDC balance, and **do not** draw from the deposit. Your collateral stays in the deposit contract and can be withdrawn whenever you want.

**Can I deposit something other than USDC as collateral?**
Yes — both USDC and the MVL token are accepted. Run `amb deposit-tokens <network>` to see the current list of depositable tokens and their on-chain addresses. MVL is credited 1:1, so the amount you send is exactly the amount required; USDC is converted at the backend's quoted rate.

**If I deposit USDC, do I get USDC back when I withdraw?**
No. Collateral is held as an **MVL credit** regardless of the token you deposit — a USDC deposit is converted to MVL at deposit time (at the backend's quoted rate), and `deposit-withdraw` returns that balance as the **MVL token**, not USDC.

**What is x402?**
[x402](https://www.x402.org) is an HTTP-native payment standard: the server returns a special response telling the client exactly how much to pay, and the client pays inline as part of the same request flow. As a user, you do not need to know x402 exists — the skill speaks it on your behalf, and it applies only to **ride-fare payment**, not to the collateral deposit.

**What is Privy and why does the skill use it?**
[Privy](https://privy.io) is an embedded-wallet provider that splits signing across multiple parties so no single place holds a complete private key. The skill stores only a local **quorum key** — see *How wallets work in this skill* above for the full picture.

**Why does the agent ask me to sign a "SIWE" message at login?**
SIWE = Sign-In With Ethereum. It is a way to prove ownership of a wallet to a backend without using a password. The signed message has no on-chain effect, costs no gas, and only authenticates your session.

### Privacy & security

**Where is my private key stored?**
There is no single "your private key" — Privy uses a split-signing model. The skill stores a local **quorum key** that lets it co-sign with Privy. See *How wallets work in this skill*.

**What is `AMB_RIDE_PASSPHRASE`?**
A passphrase the install script generates and stores in your local agent config. The skill uses it to encrypt the local database and any sensitive material kept on disk. **If you lose it, you lose access to that local state** — you will need to re-run wallet setup. Treat it like a password.

**What data leaves my machine and where does it go?**
What the skill contacts, and why:

- **TADA/Throo servers** — place search, ride search/request/status/cancel, payment, chat messages, tipping, member sign-in (phone OTP), and telemetry relay. Pickup and drop-off coordinates go here as part of any search or ride. **Your ride history lives on these servers**, not only on this machine — `ride-history` fetches it back from them.
- **Privy** — only when you choose the built-in wallet. Provisioning it, and every signature it produces, goes through Privy's API. This machine holds an encrypted key that lets it ask Privy to sign; Privy holds the other half.
- **MetaMask Agent Wallet CLI** — only when you choose MetaMask. It controls the external wallet and handles approval/signing outside this skill; the skill does not receive its key.
- **Google** — only when you hand the agent a Google Maps link to save as a place. Resolving that link into a real place means asking Google about it.
  Saving a place also sends it to TADA/Throo: `place-save` posts the name, coordinates, and Google identifier to their gateway, signed in as you. So if you save your home, your home address is associated with your account there — the saved-place *list* is local, but the places themselves are not a secret you keep from TADA/Throo.
- **Public blockchain RPC endpoints** (`eth.drpc.org`, `mainnet.base.org`) — crypto path only, for reading balances and broadcasting transactions. They see your wallet address and the transactions you send, both of which are public on-chain regardless.
- **Circle** (`iris-api.circle.com`) — only when you bridge USDC between chains, to fetch the attestation that completes the transfer.
- **Your own agent host** — on OpenClaw, ride updates are relayed to the agent so it can tell you what is happening. If you have connected a channel such as Telegram, ride status, driver messages, and any links in them are delivered there. Nothing about a ride reaches a channel you have not connected yourself.

Block explorer links (Etherscan and friends) are shown to you as links; the skill does not call them.

Telemetry sent to `amb-telemetry-service` is limited to allowlisted journey and activation milestones, outcome, environment, and coarse cohort fields. It excludes phone numbers, raw wallet addresses, coordinates, member display names, email addresses, and message contents.

Telemetry uses namespaced account IDs (`member:<member_uuid>` or `wallet:<sha256-prefix>`) within the selected environment. Before authentication it uses the local installation ID. The installation ID remains an event property so activation and device-level analysis are still possible. Raw wallet addresses, member display names, phone numbers, and email addresses are not sent. Journey, request, and ride IDs are opaque join keys for the dashboard and contain no coordinates or message content.

Commands batch events through the generated `amb-telemetry-service` API client and wait up to 2 seconds for `202 Accepted`. Relay timeout or analytics failure never changes a Ride command result.

The CLI does not call PostHog or another analytics vendor directly; the TADA-operated telemetry service owns downstream delivery.

**How do I uninstall and remove all my data?**
Remove the skill directory, then delete the Ambient state root — by default `~/.amb` (or the path set with `AMB_RIDE_STATE_DIR`).

This removes data stored by Ambient on this machine. It does not delete telemetry already accepted by the TADA-operated telemetry service.

⚠️ **Important:** the keys directory holds your **quorum key for the embedded Privy wallet**. Deleting it means this machine can no longer ask Privy to sign for that wallet. The wallet still exists on Privy's side, but you would need to go through Privy's recovery flow to use it again. If you want to keep the wallet usable, back up the keys directory before deleting.

### Other

**Does the agent ask me to confirm every booking and payment?**
Not necessarily — see [What you are authorising](#what-you-are-authorising) above, which covers this in full. Short version: the skill's instructions ask before paying steps, but an agent configured to act autonomously can be allowed to skip them, and only your agent host can make the gate binding.

**Why can't I find rides where I am?**
Most likely the city is not yet supported by **this skill** — currently NYC, SIN, PNH, REP, SHV, KPK, and HKG are wired up, and an unsupported city is rejected rather than served from a nearby one. Other possibilities: no driver is currently within range, or your origin/destination did not resolve to a valid TADA place. Try a more specific address or a nearby landmark.

---

## Where to go next

- **`wallet.md`** — wallet management, signing, SIWE, phone verification, balance, deposit / withdrawal
- **`ride.md`** — place search, ride search/request/status/cancel/payment, history, error codes, supported city codes
- **`tip.md`** — tip configuration and payment flow
- **`chat.md`** — driver chat, real-time daemon, image sending
