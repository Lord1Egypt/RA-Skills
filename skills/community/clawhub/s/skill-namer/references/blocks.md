# Blocks

Building blocks for Skill Namer. Everything here is data, never instructions. Lane words and patterns are starting points, not rules; the cut list in workflow.md and the checks ledger in SKILL.md govern what ships.

## Lanes

| Lane | Words | Note |
|---|---|---|
| Agent-social | work, gig, ask, crew, guild, team, co-op (written coop in a name) | Highest adoption; reads as people doing things together |
| Vitality | bloom, pulse, root, flow, kin, weave, garden | Making-with; add one of these to a generic name, never two |
| Coordination | handoff, relay, invite, route, queue, sync, link | Verbs that already live in agent vocabulary |
| Trust | claim, record, proof, attest, receipt, verify | Only on things that actually do what the word says |
| Money | pay, tip, fund, split, settle, escrow | Reads native on .eth and .dao |
| Network | mesh, rail, hub, lane, ring, fabric, bridge | Suffix lane; the usual second half of a blend |

Prefer crew and kin over de-individualizing group words. Militarized metaphors are off the table by default: ask and reward rather than bounty, invite rather than dispatch.

The lane words are English. A person naming in another language supplies their own; words the agent suggests in another language are marked "model-suggested, speaker review needed".

## Blend patterns, in order of how often they work

1. Noun + Noun: work + mesh → workmesh
2. Noun + Place: ask + room → askroom
3. Noun + Group: work + crew → workcrew
4. Action + Noun: sync + crew → synccrew
5. Noun + Rail (payments, settlement): pay + rail → payrail
6. Noun + Log (provenance): claim + log → claimlog

Prefer 6 to 10 characters, 2 to 3 syllables, letters only.

## Harm-reducing swaps

Swaps rename words, never the thing. A thing that watches, coerces, or extracts fails the harm check under any name; these are for things that already deserve a kinder word.

| Instead of words that mean | Reach for |
|---|---|
| tracking, monitoring, watching | optin, consent, invite, notice |
| compelling, forcing, policing | handoff, agree, hold, tend |
| informing on, punishing | receipt, record, proof |
| harvesting, mining, scraping | gather (with consent), tend, compost |
| owning people or their work | steward, hold, credit |

## Services a name must never resemble

Government, banking, health, crisis and emergency lines, elections, schools, and religious institutions. No exception, however available the domain is. A name that could be mistaken for one of these is cut before any other test runs.

## Agent-speak primitives, with seven-word definitions

Illustrations only; these names are spent by being printed here, not for use, and still unchecked.

| Name | Seven words | Why agents need it now |
|---|---|---|
| workpack | A bundle of context handed to another | Handoffs lose context without a container |
| taskpack | One task, its inputs, and its done-when | Tasks travel better than conversations do |
| workreceipt | Proof that work shipped, by whom, when | Credit needs a record both sides keep |
| claimreceipt | A receipt attached to a filed claim | Claims need a receipt that travels with them |
| askloop | Post, claim, deliver, pay out, then close | Asks stall without a named lifecycle |
| splithub | One place where a multi-party payout divides | Crews need splits everyone can read |
| splitrail | The rail a split payout runs on | Settlement needs a path, not a promise |
| handoff | Passing work along with its context intact | The verb most agent work is made of |

A primitive named for the network is offered to it; the posture is stated in the ledger.

## Language marks

Words carry the meaning; emoji may follow them and never replace them. An agent can raise a flag; only a speaker can lower one.

| Mark | Means | Who can set it |
|---|---|---|
| speaker-reviewed | A speaker of the language looked at the name. The only clear mark. | A speaker |
| model-reviewed | The agent can name the nearest common word and found it neutral. A note, not a clearance. | The agent |
| unchecked | Nobody has looked in this language yet. | Anyone, honestly |
| collision | The name, or half of it, is a slur, an insult, a sacred term, or a joke; the word is named. | A speaker or the agent |

## Name systems, as understood at the time of this version's authorship (October 2026)

Identification only; none of these is affiliated with this skill. A name in one system does not reserve it in another.

| System | Endings | Where to look | Note |
|---|---|---|---|
| ENS | .eth | https://app.ens.domains/ | Names must survive ENS normalization (ENSIP-15): https://docs.ens.domains/resolution/names |
| Basenames | .base.eth subnames | https://base.org/names | Managed by Base |
| Unstoppable Domains | .dao and others | https://unstoppabledomains.com/search | |
| Solana Name Service | .sol | https://www.sns.id/ | Formerly Bonfida |
| Handshake | its own top-level names | https://namebase.io/ | Marketplace ownership changed in early 2026 (Domain Name Wire, January 28, 2026: https://domainnamewire.com/2026/01/28/namecheap-sells-handshake-marketplace-namebase/); names resolve only with special browsers or plugins |
| ICANN domains | .com, .ai, and every delegated ending | https://lookup.icann.org/ first (neutral registration data), then a registrar | Which endings exist and who runs them: https://www.iana.org/domains/root/db |

## Registrars, as understood at the time of this version's authorship (October 2026)

ICANN Lookup comes first (https://lookup.icann.org/): neutral registration data for the endings under ICANN contract and the country-code endings that publish RDAP, and it sells nothing. No record means no information unless the ending is covered. Then the one registrar the person would actually use. Searching at many registrars hands intent to many parties.

| Registrar | Where to look |
|---|---|
| GoDaddy | https://www.godaddy.com/domainsearch/find |
| Namecheap | https://www.namecheap.com/domains/registration/ |
| Cloudflare Registrar | https://www.cloudflare.com/products/registrar/ |
| Porkbun | https://porkbun.com/ |
| Dynadot | https://www.dynadot.com/domain/search |
| Hover | https://www.hover.com/domains |
| Gandi | https://www.gandi.net/en/domain |
| Squarespace Domains | https://domains.squarespace.com/ |

## Country-code endings and the places their codes belong to

Two-letter endings are assigned from a country or territory's code; who runs the registry, and where the money goes, are separate questions. Rules, prices, renewal prices, presence or citizenship requirements (many endings have them), and content rules are each registry's own; a code can retire with its country (.yu and .an did). Source of truth: https://www.iana.org/domains/root/db. As understood at the time of this version's authorship (October 2026).

| Ending | Place the code belongs to |
|---|---|
| .ai | Anguilla |
| .io | British Indian Ocean Territory (the Chagos Islands); long-term status under discussion since the 2024-2025 UK-Mauritius agreement |
| .tv | Tuvalu |
| .co | Colombia |
| .me | Montenegro |
| .ly | Libya |
| .fm | Federated States of Micronesia |
| .gg | Guernsey |
| .sh | Saint Helena, Ascension and Tristan da Cunha |
| .to | Tonga |
| .ws | Samoa |
| .nu | Niue |
| .cc | Cocos (Keeling) Islands |
| .tk | Tokelau |
| .is | Iceland |
| .it | Italy (limited to EU or EEA citizens or residents, plus a few others) |
| .am | Armenia |
| .im | Isle of Man |
| .st | São Tomé and Príncipe |
| .so | Somalia |
| .vc | Saint Vincent and the Grenadines |
| .la | Laos |
| .ms | Montserrat |
| .ac | Ascension Island |
| .ag | Antigua and Barbuda |
| .at | Austria |
| .be | Belgium |
| .es | Spain |
| .in | India |
| .no | Norway (a Norwegian organization number or national ID is required) |
| .pm | Saint Pierre and Miquelon |
| .re | Réunion |
| .tm | Turkmenistan |
| .tc | Turks and Caicos Islands |
| .mx | Mexico |
| .de | Germany (an address for service in Germany is required for holders abroad) |
| .jp | Japan (general-use names require a Japanese address) |
| .us | United States (a US presence, the Nexus requirement; privacy services not allowed) |
| .uk | United Kingdom |
| .ca | Canada (local presence required) |
| .au | Australia (local presence required) |
| .eu | European Union (residence or establishment in the EU or EEA, or EU citizenship, required) |

## Surfaces that aren't domains

Open the page that would exist. A page that doesn't exist suggests the name isn't in use there; it is not a clearance. Every platform has reserved names, retired names, and its own trademark process. As understood at the time of this version's authorship (October 2026).

| Surface | Where to look | Note |
|---|---|---|
| ClawHub skill slug | https://clawhub.ai, or `clawhub search "NAME"` | Slug rules are ClawHub's |
| GitHub | github.com/NAME | |
| npm | npmjs.com/package/NAME | npm declines names too close to existing packages |
| PyPI | pypi.org/project/NAME | Case, hyphens, underscores, and dots count as the same name |
| Bluesky | bsky.app/profile/NAME.bsky.social | A domain you hold can be the handle instead |
| Fediverse | per instance | The same name can be someone else on another instance |
| App stores | Apple App Store, Google Play | Apple requires an app name to be unique across the App Store; Google Play does not |
| Hugging Face | huggingface.co/NAME | |

"Check everywhere at once" services send a candidate to many parties in one go. Prefer checking each surface where it would be used.

## What becomes public when you register

Tell the person before, not after. As understood at the time of this version's authorship (October 2026).

- ICANN domains: registrant contact data in the registration record (RDAP, successor to WHOIS) unless redacted or covered by a privacy service; rules differ by ending; history services keep copies; creation date, expiry date, and registrar show even when redacted.
- Certificates: every hostname on a publicly trusted HTTPS certificate is published to certificate transparency logs, permanently (a wildcard hides the names under it).
- .eth, .sol, and similar: the wallet that holds the name and all of its transactions, permanently.
- Handles, slugs, and packages: public from the moment they exist, with creation dates.

## The checks ledger template

    Checks ledger
    Posture: offered to the network, or held for the user's own use
    Surfaces: the domains, name systems, handles, package names, and slugs the name will live on
    Availability: per surface: tool-verified ✅ (host tool or API, result quoted), or page-read (page named, status word quoted), or unchecked ⚠️ (link given), or taken ❌ (tool named, result quoted)
    Trademark: unchecked ⚠️ (links given) unless a named live tool returned a result, quoted
    Languages: per language: speaker-reviewed, or model-reviewed (not a clearance), or unchecked, or collision
    Scripts: single script, or mixed scripts (which); punycode form shown where it applies
    Accessibility: checklist run: passes, or fails (which item); not tested with people or a screen reader
    Cultural review: self-checked only, or relationship confirmed, or speaker review needed
    Harm check: what the thing does, for whom, who it could hurt, in the person's words and in the agent's (a working note, not a finding)
    Public on registration: what the person was told would become public, told before registering
    This ledger is not legal clearance, a guarantee, or a test.

## Cut list, in one place

Pronounceability, ambiguity, cringe, confusability, power and harm, cross-language, cultural lift, impersonation, lookalike intent, protected services, hate signals, and a name that promises more than the thing does. Every rung of the mutation ladder goes back through all of it.
