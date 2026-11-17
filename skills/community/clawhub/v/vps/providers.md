# Providers — What Each One Is Actually Like

Read when `provider` is unset, when the user names a provider you have not given steps for yet, or when a procedure depends on a console path. Plans, prices, and policies change: everything below is the **shape** of each provider, which is stable, plus the specific things that surprise people. Verify any number on their page before quoting it.

**Contents:** [The Five Properties That Differ](#the-five-properties-that-differ) · [Provider Notes](#provider-notes) · [Recovery Paths by Provider](#recovery-paths-by-provider) · [Outbound Mail Policy](#outbound-mail-policy) · [What Never Differs](#what-never-differs)

## The Five Properties That Differ

When the user names a provider, these are the five things to establish before giving any procedure. Everything else transfers.

1. **Recovery path** — what the console is called, whether there is a rescue system, and whether it needs a support ticket. This decides Rule 1 and must be known before any SSH change.
2. **Firewall model** — is there a free cloud firewall applied outside the machine, or is the host firewall the only layer? This decides `firewall.md`.
3. **Traffic model** — included allowance, whether it pools across servers in the account, and the overage rate. This decides most of the bill.
4. **Address policy** — is IPv4 included, charged, or optional; is IPv6 free; can an address be reserved and moved.
5. **Port 25 policy** — blocked by default, unblockable by request, or open. This decides whether mail from the box is possible at all.

## Provider Notes

| Provider | Strong at | Watch out for |
|---|---|---|
| **Hetzner** | Best mainstream price for RAM; very large included traffic; free cloud firewall and private networks; a genuine rescue system | EU and US locations only, and the ARM line is not in every location; outbound mail is restricted until the account is established; identity verification can delay a first signup by a day |
| **DigitalOcean** | The most predictable operations and by far the best documentation; free cloud firewalls and VPC; transfer pools across the account | Transfer allowance is modest and overage is metered per GB; SMTP is blocked and generally stays blocked; managed add-ons are convenient and priced well above the equivalent droplet |
| **Vultr** | Many locations worldwide, hourly billing, fast provisioning; useful for putting a box near one specific city | Quality varies noticeably between locations; SMTP blocked pending a request; check the traffic allowance per plan, it is not uniform |
| **Linode / Akamai** | Global footprint and an unusually good out-of-band console; long track record of stable plan families | SMTP blocked for new accounts pending a support request; support quality changed after the acquisition and is worth re-testing |
| **OVH** | Cheap, European, unusually permissive on outbound mail, DDoS filtering included on most products | Control panel is a maze, provisioning can be slow, and support is inconsistent; product lines overlap confusingly (VPS versus their bare-metal brands) |
| **Scaleway** | European jurisdiction, ARM options, good object storage in the same account | Smaller region set; some resources bill in ways that surprise (flexible addresses, block volumes) — read the invoice in the first month |
| **Contabo** | The most raw specs per euro of anything mainstream | Heavily oversubscribed, IO performance is inconsistent, support is slow, and some plans carry a setup fee. Correct for mirrors, build agents, and experiments; never for anything with a revenue number attached |
| **AWS Lightsail** | A fixed-price VPS inside an AWS account you already control, with a clean upgrade path into a full VPC | Egress beyond the bundle is billed at that cloud's rates, which are an order of magnitude above budget hosts; the simplicity ends the moment you need a real VPC feature |
| **Always-free ARM tiers** | Genuinely free and genuinely useful for a hobby box | Genuinely reclaimable, with capacity errors on creation and idle-instance policies; never for anything you would miss |
| **Anything not listed** | — | Establish the five properties above before giving a single step, and record them in `## Provider Accounts` |

## Recovery Paths by Provider

Every provider offers some version of these three; the names differ, and knowing the name is the difference between six hours down and ten minutes.

| Layer | What it is | Typical names |
|---|---|---|
| Web console | A keyboard and screen attached to the running machine; works when the network stack or sshd is broken, not when the box will not boot | "Console", "Recovery Console", "View Console", a shell-based console on some providers |
| Rescue system | Boots a temporary live OS with your disk *unmounted*; the only way to fix a bad `/etc/fstab`, a full root filesystem, or a broken bootloader | "Rescue mode", "Rescue system", "Recovery ISO" |
| Reinstall / rebuild | Fresh image over the disk. Destroys everything not backed up | "Rebuild", "Reinstall", "Reimage" |

Two rules that survive every provider:

- **Confirm the console works before you need it.** Some providers require an account setting, a password set in advance, or a browser that permits the console's protocol. Discovering this while locked out is the standard version of this failure.
- **Never reinstall before reading the disk in rescue mode.** The rebuild button is next to the rescue button and it is the irreversible one.

## Outbound Mail Policy

Port 25 outbound is blocked by default at most providers, because a rented server that can send mail is a spam engine the moment it is compromised. The pattern:

- **Blocked, unblockable on request** — most European hosts: an account in good standing asks support and receives it, sometimes after a waiting period.
- **Blocked, effectively permanent** — several US-based providers: submission ports for a relay work, direct delivery does not.
- **Open** — a minority, usually with their own abuse enforcement instead.

This is a provider-selection input, not a configuration problem. Full treatment in `email.md`.

## What Never Differs

Do not go looking for a provider-specific answer to these:

- The host firewall, the distribution, systemd, and everything above the hypervisor behave identically everywhere.
- Disk growth is one-way at every provider that offers it.
- Snapshots always live in the account that can delete them (Rule 4).
- Provider-account 2FA is the actual root of trust everywhere (Rule 2).
- A stock image is behind on patches everywhere, on day one.

---

**Write what you establish.** The moment a provider account is used, record it in `## Provider Accounts` in `~/Clawic/data/vps/memory.md` — provider, account or project name, who owns the login, whether 2FA is on, how it is billed, the API-token **pointer** (`keychain:<entry>`, never the token), and the support tier — and add its recurring cost as one row per account in `~/Clawic/data/finances/subscriptions.md`. From the second account, the table splits to `provider-accounts.md` per the procedure in `memory-template.md`. The five properties above, once established for a provider you had not used, belong in the same row's notes so the next session does not re-derive them.
