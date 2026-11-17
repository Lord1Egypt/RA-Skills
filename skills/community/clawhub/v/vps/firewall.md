# Firewalls — Two Layers That Do Not See the Same Packets

Read when a port should be closed and is not, when a rule that looks correct is ignored, before exposing any new service, and when deciding where filtering should live. `firewall_layer` says which layers to configure; the default is both.

**Before opening or closing anything**, read `## Exposure` in `~/Clawic/data/vps/memory.md` (or `exposure.md` if `## Boxes` points there): it records which ports are open on which host, to whom, why, and at which layer — and a rule the user believes exists at a layer where it does not is the single most common finding.

**Contents:** [The Two Layers](#the-two-layers) · [Where a Packet Is Decided](#where-a-packet-is-decided) · [Container Runtimes Walk Around the Host Firewall](#container-runtimes-walk-around-the-host-firewall) · [Default Policy](#default-policy) · [Which Layer for Which Job](#which-layer-for-which-job) · [Binding Beats Filtering](#binding-beats-filtering) · [Egress Filtering](#egress-filtering) · [IPv6 Is a Second Firewall](#ipv6-is-a-second-firewall) · [Private Networks Are Not a Firewall](#private-networks-are-not-a-firewall) · [Verifying From Outside](#verifying-from-outside)

## The Two Layers

| | Provider firewall | Host firewall |
|---|---|---|
| Where it runs | Outside the machine, in the provider's network | On the machine, in the kernel |
| Survives | A broken, overloaded, or misconfigured host | A provider console you cannot reach |
| Sees | Traffic before it reaches the instance | Traffic after it arrives, including from the private network |
| Blind to | Nothing inbound — but it has no idea what is listening | Rules inserted by a container runtime ahead of it |
| Travels with a migration | No — it is provider configuration | Yes, if it is in version control |
| Cost | Free at most providers | Free everywhere |
| Changed by | Console or provider API | A shell session on the box |

Both, by default. If only one is possible, keep the provider layer: it is the one that still works when the machine does not, and it cannot be bypassed by anything running on the box.

## Where a Packet Is Decided

Order for an inbound packet, top to bottom. The first layer that drops it wins, and every layer below is irrelevant:

1. Provider network filter (cloud firewall, security group).
2. Kernel packet filter on the host — including any chain a container runtime inserted, which is typically evaluated **before** the chain a front-end like ufw manages.
3. The service's own bind address: a process bound to `127.0.0.1` is unreachable from outside regardless of any firewall.
4. Application-level controls: allow-lists, authentication.

Debugging follows the same order. Checking the host firewall first is the standard wasted hour, because the provider layer is the one you cannot see from inside the box.

## Container Runtimes Walk Around the Host Firewall

The most reported "my firewall is broken" case, and it is not a bug:

- Publishing a container port makes the runtime write its own rules into the kernel's packet filter, in a chain evaluated ahead of the front-end's chain. The result: a published port is reachable from the internet even though the front-end shows a deny rule for it.
- **This is not fixed by adding another deny rule** in the front-end. It is fixed by one of:
  - **Publish to localhost only** — bind the published port to `127.0.0.1` and put a reverse proxy in front. This is the default answer and it removes the problem instead of filtering it.
  - **Filter at the provider layer**, which sits outside the machine and therefore outside the runtime's reach.
  - **Use the runtime's designated user chain**, which is evaluated before its own rules and is the supported place for administrator policy.
- The symptom that identifies this instantly: the port is closed according to the host firewall's status output, and open according to a scan from another machine.
- Every database, cache, and admin interface running in a container is exposed this way by default the moment someone maps its port for local convenience.

## Default Policy

- **Deny inbound, allow outbound** as the starting point, at both layers.
- **Allow SSH before enabling the policy.** Reversing these two steps is an instant lockout, and it is the reason SKILL.md Rule 1 exists.
- Allow only what is serving traffic: typically SSH from a restricted source, plus 80 and 443 from anywhere.
- Everything else — databases, caches, metrics endpoints, admin panels, message brokers — is reachable over localhost, the private network, or a VPN, never from the public internet.
- Restrict the SSH source where the user's address is stable, and keep the provider console as the fallback for when it is not (`access.md`).
- Rules are configuration: keep them in the provisioning file or configuration management, not typed by hand on each box. Hand-typed rules diverge silently across a fleet.

## Which Layer for Which Job

| Job | Layer | Why |
|---|---|---|
| Public web ports | Both | Cheap, and the provider layer keeps working during a host problem |
| SSH source restriction | Provider | Editable from the console when you are locked out; a host rule that locked you out cannot be edited from outside |
| Blocking a container-published port | Provider, or bind to localhost | The host front-end cannot see it |
| Traffic between your own hosts | Host, on the private interface | Provider firewalls often treat the private network as trusted |
| Emergency: cut all traffic to a compromised box | Provider | Works even if the box is not yours any more (`security.md`) |
| Rate limiting and abusive clients | Application or reverse proxy | Packet filters have no idea what a request is |

## Binding Beats Filtering

A service bound to `127.0.0.1` or to a private address needs no firewall rule and cannot be exposed by a mistaken one. Check the listening sockets of a box, not its rules, to know what is exposed.

Defaults worth knowing because they differ: database servers vary in whether they listen on all interfaces out of the box; several popular data stores historically shipped listening on every interface with no authentication, which is the origin of most public data dumps. Check what is bound on every new box (`provisioning.md` baseline) instead of trusting the image.

## Egress Filtering

- Default allow-outbound is correct for almost everyone. Restricting egress is real security work and real operational cost: package updates, certificate validation, time sync, and every API the application calls each need a hole.
- Where it pays: a box holding sensitive data, where restricting outbound destinations limits what an intruder can exfiltrate to; and compliance regimes that require it.
- Cheaper approximation with most of the benefit: alert on unexpected outbound volume (`operations.md`) rather than blocking it. A compromised box's first act is usually a large outbound transfer or a burst of connections, and that is visible without breaking anything.
- Blocking outbound port 25 on hosts that should not send mail is a small, cheap, well-targeted exception worth making.

## IPv6 Is a Second Firewall

If the box has IPv6 — and it should — then it has a second address space and, in most tools, a **separate rule set**. A deny policy configured only for IPv4 leaves every service reachable over IPv6.

- Verify both families explicitly. Front-ends differ in whether they apply rules to both by default.
- Scan the box's IPv6 address from outside, not just the IPv4.
- The provider layer usually applies to both, which is another argument for it as the floor.

## Private Networks Are Not a Firewall

- A provider private network is shared infrastructure at some providers and isolated per account at others. Establish which before treating it as trusted (`providers.md`, `networking.md`).
- Even when isolated, every machine on it is one compromise away from every other. Services on the private interface still need authentication.
- The correct model: the private network removes the service from the public internet; authentication and host firewall rules do the rest.

## Verifying From Outside

Reading your own rules proves what you intended, not what is true. Verification is a scan from a different machine:

- Scan the public IPv4 and the IPv6 address for the ports you believe are closed.
- Repeat after any container deployment — a new published port is the most common way exposure changes without anyone editing a firewall.
- Repeat after a provider firewall change, because provider rules can be scoped to tags or groups and a machine can silently fall out of a group.
- Anything unexpected goes into `## Exposure` with its reason, or gets closed.

---

**Write it down.** Every open port belongs in `## Exposure` in `~/Clawic/data/vps/memory.md`: host, port, service, what it is open to, why, and the layer the rule lives at (`provider`, `host`, or `both`). Update the row when a rule moves layers; delete it when the port is closed. Past ~15 rows, split to `exposure.md` per the procedure in `memory-template.md`, with one `## <host>` heading per host. If a sweep from outside contradicts what the table says, the scan wins and the table is corrected in the same turn.
