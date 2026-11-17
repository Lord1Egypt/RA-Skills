# Outbound Mail From a Rented Server

Read when mail sent by an application on the server is rejected, silently dropped, or lands in spam, and before designing anything that sends email from a VPS. The short version: **do not deliver mail directly from a VPS unless mail is the product.**

**Before debugging DNS**, read `## Hosts` in `~/Clawic/data/vps/memory.md` for the host's PTR, and `~/Clawic/data/domains/domains.md` for the sending domain's registrar and DNS host.

**Contents:** [The Default Answer Is a Relay](#the-default-answer-is-a-relay) · [Port 25 Is Blocked](#port-25-is-blocked) · [The Four Things Receivers Check](#the-four-things-receivers-check) · [Address Reputation](#address-reputation) · [Diagnosing a Rejection](#diagnosing-a-rejection) · [If You Really Must Run a Mail Server](#if-you-really-must-run-a-mail-server) · [Receiving Mail](#receiving-mail) · [Compromise Blast Radius](#compromise-blast-radius)

## The Default Answer Is a Relay

For transactional mail — password resets, receipts, notifications — send through a mail service over an authenticated submission port. The application makes one connection to a provider that already has warm addresses, signing keys, feedback loops, and a deliverability team.

Why this is not laziness:

- **Deliverability is a reputation asset built over months.** A new address has no history, and no-history is treated as suspicious by every large receiver.
- **The failure mode is silent.** Mail that is accepted and then filtered produces no bounce and no error. You discover it when a user says they never got the reset link, weeks later.
- **The alternative costs ongoing attention**: monitoring blocklists, rotating keys, reading feedback loops, handling bounces. That is a job, and it is not the job you rented the server for.
- Small volumes are free or nearly free at every mail service. The cost of doing it yourself is measured in support tickets from people who never received an email.

Self-hosting mail is legitimate when mail *is* the product, when the volume makes per-message pricing dominant, or when a policy forbids the data leaving your infrastructure. All three are real. None of them describe a web application sending password resets.

## Port 25 Is Blocked

- Most providers block outbound port 25 by default, because a rented server that can deliver mail is a spam engine the moment it is compromised.
- Some unblock on request for an established account; some effectively never do (`providers.md`).
- **Submission ports for authenticated relaying are not blocked.** This is why the relay path works without asking anyone for anything.
- A blocked port 25 presents as connection timeouts to every receiver, which looks like a DNS or firewall problem on your side and is neither. Test whether an outbound connection to a known mail exchanger on 25 succeeds at all before debugging anything else.

## The Four Things Receivers Check

If mail leaves the server directly, all four must pass. Three are DNS records on the sending domain; one is set at the provider.

| Check | Where it lives | Failure looks like |
|---|---|---|
| **PTR / reverse DNS** matching the name the server announces | At the **provider**, not the DNS host (`networking.md`) | Immediate rejection at connection time, often with an explicit reason |
| **SPF** authorising this address to send for the domain | TXT record at the DNS host | Rejection or spam folder, depending on the receiver's strictness |
| **DKIM** signature with the public key published | TXT record at the DNS host, key on the server | Failed authentication, heavily penalised by large receivers |
| **DMARC** policy telling receivers what to do when the first two disagree | TXT record at the DNS host | Without it, receivers apply their own judgement; with a strict policy and a broken setup, they reject everything |

The forward-confirmed rule that catches people: the PTR name must resolve back to the same address, and the server must announce that same name. Any inconsistency in that triangle is grounds for rejection on its own.

Record design detail belongs to the `dns` skill; the VPS-side facts are that PTR is set at the provider and that the DKIM private key is a secret which lives on the server and never in `~/Clawic/data/`.

## Address Reputation

- Addresses are recycled. A fresh server can arrive with an address already on blocklists from a previous tenant (`networking.md`).
- **Check before you build**: query the major blocklists for the address on day one. If it is listed, ask the provider for a different address — that request is easy at creation and awkward after DNS has propagated.
- Whole ranges from some budget providers are treated with suspicion regardless of your behaviour. That is an argument about provider selection, not a configuration you can fix (`choosing.md`).
- Delisting is possible and slow, and it fails if the listing cause is still active.
- Reputation is per-address and builds with consistent, low-complaint volume. Sending a burst from a cold address is the fastest way to get listed.

## Diagnosing a Rejection

In order, because each step eliminates the ones below:

1. **Does the connection even open?** If outbound 25 times out to every receiver, the port is blocked — stop here and switch to a relay.
2. **Read the rejection text.** Mail servers explain themselves better than almost any other protocol: the response names the failing check and often links to the policy.
3. **PTR triangle.** Announced name, PTR, and forward record all consistent.
4. **Authentication records.** Verify SPF, DKIM, and DMARC evaluate as they should — send a message to a service that reports the results, rather than reading your own records.
5. **Blocklists**, for the address and the sending domain.
6. **Content and volume.** Sudden volume from a cold address, or a message that looks like bulk mail with no unsubscribe path, is filtered regardless of perfect authentication.
7. **Silent filtering** is what remains when all six pass and users still do not receive mail. This is the point at which a relay stops being optional.

## If You Really Must Run a Mail Server

- Use a maintained all-in-one distribution rather than assembling the components. Hand-assembled mail stacks are how open relays happen, and an open relay leads to an abuse notice within days (`security.md`).
- Get port 25 unblocked before building anything, not after.
- Warm the address: start with low volume to engaged recipients and increase gradually. There is no shortcut.
- Configure feedback loops and handle bounces automatically. Continuing to send to addresses that bounce is the fastest route to a blocklist.
- Budget for real maintenance: certificate renewals, blocklist monitoring, software updates on an internet-facing service that processes untrusted input, and backups of the mail store.
- Keep the mail server on its own box. Its compromise profile and its reputation requirements do not belong on the machine serving your application.

## Receiving Mail

- Receiving is a smaller problem than sending, and still requires an always-on server, MX records, spam filtering, and a place to store mail with backups.
- **Do not run a mailbox for a domain you cannot afford to lose access to.** A hosted mailbox provider handles the storage, the filtering, and the availability for a small monthly amount.
- A forwarding-only setup is the middle ground: a small service accepts mail for the domain and forwards to a personal mailbox, with no storage to lose. Note that plain forwarding breaks SPF for the forwarded message, which is what the receiving side's rewriting mechanisms exist to work around.

## Compromise Blast Radius

- A compromised box that can send mail becomes a spam source within hours, and the provider notices before you do (`security.md`).
- If the box does not need to send mail, block outbound 25 at the host firewall. It is a one-line rule with a large payoff.
- Application credentials for the relay grant the ability to send **as your domain**. Treat them as production secrets: pointer only in any documentation, scoped to sending, rotated after any incident.
- Keep the relay's sending limit set to something close to real volume. A cap is the difference between an embarrassing hour and a burned domain reputation.

---

**Write it down.** The host's PTR and whether outbound 25 is open go in `## Hosts` in `~/Clawic/data/vps/memory.md`; the port-25 policy of the provider goes in its row in `## Provider Accounts`, because it is a provider property that will decide the next server's design too. The sending domain's registrar and DNS host go in `~/Clawic/data/domains/domains.md`. When a deliverability problem is finally solved, write `~/Clawic/data/vps/artifacts/runbook-mail-<domain>.md` — which relay, which records, which checks were failing, and how it was verified — with the relay credential as a pointer, never a value, and add its `## Boxes` line in the same turn.
