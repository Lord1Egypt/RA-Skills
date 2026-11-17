# Networking — Addresses, Private Links, and Reverse DNS

Read when planning addresses, connecting two servers, setting reverse DNS, or when connectivity behaves differently over IPv6 than IPv4. Filtering is in `firewall.md`; mail-specific address concerns are in `email.md`.

**Before assigning or changing an address**, read `## Hosts` in `~/Clawic/data/vps/memory.md` for the private address plan and PTR records already in use, and `~/Clawic/data/domains/domains.md` for anything pointing at the host.

**Contents:** [IPv4 Is Now a Line Item](#ipv4-is-now-a-line-item) · [IPv6](#ipv6) · [Floating and Reserved Addresses](#floating-and-reserved-addresses) · [Reverse DNS](#reverse-dns) · [Private Networking](#private-networking) · [Mesh VPN Between Servers](#mesh-vpn-between-servers) · [Address Reputation](#address-reputation) · [MTU and the Mysterious Hang](#mtu-and-the-mysterious-hang) · [Bandwidth and Traffic Shaping](#bandwidth-and-traffic-shaping)

## IPv4 Is Now a Line Item

- Nearly every provider charges separately for a dedicated IPv4 address, attached or not, since address scarcity started being priced in 2024. The amount is small per address and stops being small across a fleet and a year.
- **An address on a destroyed server keeps billing if it was reserved.** Releasing reserved addresses is a step on the teardown list (`migration.md`).
- Sharing one address across several sites is normal: a reverse proxy with name-based virtual hosts serves many domains from one address (`hosting.md`).
- Some providers offer IPv6-only plans at a discount. They work for a service behind a proxy or CDN that speaks IPv4 to clients, and they do not work for anything that must be reached directly by IPv4-only users — which, for a public website, is still a meaningful share of the internet.

## IPv6

- Free almost everywhere, and providers hand out a large block per instance rather than a single address.
- **Enable it**, and then treat it as a second attack surface: a separate rule set in most firewall front-ends, and a service bound to all interfaces is reachable over it even when the IPv4 rules are perfect (`firewall.md`).
- Publish AAAA records only for services you have actually tested over IPv6. A published AAAA that leads nowhere makes the site unreachable for clients that prefer IPv6, and it presents as an intermittent, user-specific outage.
- Test both families explicitly after any network change. "Works for me" over one family is half a test.

## Floating and Reserved Addresses

- A floating address is one you own within the provider and can point at any of your instances. Reassignment takes seconds and requires no DNS change and no TTL wait.
- **This is the fastest failover primitive available on a VPS**, and the cheapest blue-green mechanism: build the replacement, verify it, move the address.
- Reassignment usually needs the address configured inside the receiving instance too — a step people forget, producing a machine that owns an address it does not answer on.
- It is scoped to one provider and usually one location: it does not help with a cross-provider migration, which is a DNS operation (`migration.md`).
- Reserved but unattached addresses bill. Release them when the project ends.

## Reverse DNS

- The PTR record maps address → name and is set **at the provider**, not at your DNS host. This surprises people every time, because every other record is at the registrar or DNS provider.
- **Mail requires it**: receivers check that the PTR exists and that it matches the name the server presents, and a mismatch alone is enough for rejection (`email.md`).
- Set it to a name that actually resolves back to the same address. A PTR pointing to a name with no forward record is worse than none for a mail server's reputation.
- For anything that is not mail, PTR is cosmetic — useful in logs and traceroutes, not required.
- IPv6 needs its own PTR for the specific address the server sends from, and mail servers check it.

## Private Networking

- Traffic between your machines over a provider private network stays off the public internet, is usually not metered against the traffic allowance, and has lower latency.
- **Scoped to one location.** Machines in different regions cannot share it — that is what a VPN is for.
- **Isolation varies by provider**: at some, the private network is per-account and isolated; at others, historically, it was a shared segment where any customer in the location could reach it. Establish which before treating it as trusted, and record it in `## Provider Accounts`.
- **Never treat it as authentication.** Services on private interfaces still need passwords, and the host firewall should still restrict which machines may connect (`firewall.md`).
- Plan the address range before the second box: a small private range with a documented layout, recorded in `## Hosts`, beats renumbering three servers later.
- The private interface must be configured inside the instance as well as attached in the console; an attached-but-unconfigured network is a common "the servers cannot see each other" case.

## Mesh VPN Between Servers

When machines span providers or regions, an encrypted overlay is the correct answer:

- A modern point-to-point tunnel is cheap in CPU and simple in configuration, and gives every host a stable address regardless of provider.
- **It removes the need for a public SSH port entirely**: administration over the overlay, nothing exposed. This is the strongest single reduction in attack surface available (`security.md`), and it introduces a dependency whose failure locks you out — so the provider console stays as the floor (Rule 1).
- Key material is per-host and belongs in the user's secret store, never in `~/Clawic/data/`. Public keys are not secrets and can be recorded.
- Route only what needs routing. A full-tunnel default on a server sends its package updates and its outbound traffic through another machine, which is rarely intended and always confusing later.
- Managed mesh services trade a monthly fee and an external dependency for identity-based access and painless key rotation. Correct above a handful of machines or humans.

## Address Reputation

- **Addresses are recycled.** A new server can arrive with an address that a previous tenant used for spam, scanning, or something that got it blocklisted.
- Check reputation before committing an address to anything user-visible: blocklist lookups for mail, and a quick check that the address is not category-blocked by corporate filters if the service is aimed at business users.
- Most providers will replace a bad address on request; some will not. It is easier to ask on day one than after DNS has propagated.
- Certain address ranges from budget providers are treated with blanket suspicion by some networks. That is a provider-selection input for a user-facing service (`choosing.md`).

## MTU and the Mysterious Hang

The classic symptom pair: small requests work, large ones hang forever; SSH connects and then freezes when output scrolls.

- Cause: an oversized packet cannot be fragmented and the path's notification is being dropped, usually across a tunnel, an overlay network, or a provider link with a reduced maximum size.
- It looks like an application bug and it is not. The tell is that size, not endpoint, decides whether it works.
- Fix at the interface or the tunnel, by reducing the maximum size to what the path supports, or by allowing the notification traffic that would have negotiated it.
- Suspect it immediately after introducing a VPN or an overlay network, which is when it almost always appears.

## Bandwidth and Traffic Shaping

- The allowance is usually **outbound only**, sometimes pooled across the account, and sometimes per instance. Which one it is changes the fleet's economics (`costs.md`).
- Inter-server traffic over the private network usually does not count. Over public addresses in the same location, it usually does — an easy and expensive mistake when configuring replication or backups between two of your own machines.
- Overage is billed on the total for the period, not on a peak. A single misconfigured backup job that egresses nightly to another region is the standard cause of a surprising bill.
- Cap what you can: rate-limit large downloads, put static assets behind a CDN, and keep backups going to storage in the same location where the transfer is free.

---

**Write it down.** Private addresses, PTR records, and private-network membership go in `## Hosts` in `~/Clawic/data/vps/memory.md`, keyed by the same `Name` as `~/Clawic/data/servers/servers.md`. A domain newly pointed at a host — or a TTL lowered for a cutover — goes to `~/Clawic/data/domains/domains.md` with the host **name** as its target, never a bare address. Whether a provider's private network is isolated or shared goes in the provider's row in `## Provider Accounts`, because the answer shapes every future design on that provider. VPN public keys may be recorded; private keys are pointers only.
