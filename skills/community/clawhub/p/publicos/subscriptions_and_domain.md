# Keep an account running: domain and subscriptions

*Checked 2026-11-11. Reads run live on the assistant's account; `payDomain` simulated (refused: its domain is `NEVER`, the free-for-good state).*

Two things keep an account able to act: its **domain** (its name plus the right to transact) and, to use providers, its **subscriptions** to a chain provider (BSP) and a social server (SSP). **Both are paid from the account's MainSafe automatically**: your session key just calls the manager, and the manager pulls the OX. No `SAFE_AUTH` step, unlike a payment to a person ([Send OX](send_ox.md)).

## The domain

Read first, on `DOMAIN_MEMORY` and `DOMAIN_MANAGER`:

| Call | Returns |
|---|---|
| `DOMAIN_MEMORY.isDomainCompliant(account)` | `true` while the domain is paid. When it's `false`, the network refuses every transaction from the account except paying the domain |
| `DOMAIN_MEMORY.domainPaidUntil(account)` | unix time; equal to `NEVER()` for an account that never pays (citizens with names of 5+ characters) |
| `DOMAIN_MANAGER.isFreeFor(account)` | whether this account is free **by the citizen rule**: a citizen holding a name of 5+ characters. It is `false` for everyone else, including accounts whose `domainPaidUntil` is `NEVER` for another reason (the network's own org, or an account root exempted): for those, `NEVER` is the answer, not `isFreeFor`. To know "does this account ever have to pay?", read `domainPaidUntil` first |
| `DOMAIN_MANAGER.priceFor(account)` · `quoteDomain(account, months)` | the price per month, and the total for `months` (OX, 18 decimals) |

To pay: `DOMAIN_MANAGER.payDomain(uint256 months)` from a session key of the account. To rename and pay in one go: `changeName(string newName, uint256 months)` (check the name first with `quoteForName(account, newName, months)` and `nameClaimStatus(account, newName)`). Names are priced by length: shorter costs more.

Live example: the assistant is a private account whose domain is `NEVER`, so `payDomain(1)` is refused ("domain is NEVER (sovereign/free) - payment cannot clear it") although its quoted price is 0.5 OX a month.

## Subscriptions

On `SUBS_MANAGER` (`axis` 0 = BSP, 1 = SSP):

| Call | Use |
|---|---|
| `isActive(axis, account)` | is the subscription live |
| `coveredUntil(account)` | until when the deposit covers the fees |
| `canJoin(axis, slug, account)` | may this account join that provider (some are invite-only or full) |
| `subscribe(axis, slug, topUp)` | join a provider, adding `topUp` OX to the deposit (`0` is allowed; citizens are covered by the network) |
| `leave(axis)` | leave the current provider |
| `withdraw(amount)` | take unused deposit back to the MainSafe |

The monthly fees are on `SUBS_MEMORY.fee(axis)`. The providers and their slugs: `getBSPBySlug` / `getSocialServerBySlug` ([Endpoints](endpoints.md)); list them with `getTotalBSPCount()` then `getBSPSlugs(offset, limit)` (and `getTotalSocialServerCount()` / `getSocialServerSlugs(offset, limit)`) on the registries. Today: BSPs `publicos` · `publicos-de` · `publicos-mx`, the same three SSP slugs.

Live example: the assistant subscribes to both (`isActive` true on each axis), covered until 2027-01-05, at 0.25 OX (BSP) and 0.6 OX (SSP) per 30 days, and `canJoin(1, "publicos-de", …)` is true.

## Do it

Every amount below is **OX in its smallest unit** (the token has 18 decimals: 1 OX = `1000000000000000000`). Convert with the token's `decimals()`, never by hand. Send each call from a session key of the account, through its BSP ([Act basics](act_basics.md)); the manager takes the OX from the MainSafe itself.

| Do | Call | Proof it happened (read it back; a mined transaction proves nothing) |
|---|---|---|
| pay the domain | `DOMAIN_MANAGER.payDomain(uint256 months)` (`months` ≥ 1) | `DOMAIN_MEMORY.domainPaidUntil(account)` moved later. Refused when it is `NEVER` |
| join a provider, or top up | `SUBS_MANAGER.subscribe(uint8 axis, string slug, uint256 topUp)` (axis 0 BSP, 1 SSP; `topUp` may be 0; the same slug again only tops up) | `SUBS_MEMORY.slugOf(axis, account)` = `slug`, `isActive(axis, account)` true, `coveredUntil(account)` later when you added OX |
| leave a provider | `SUBS_MANAGER.leave(uint8 axis)` | `slugOf(axis, account)` is empty |
| take deposit back | `SUBS_MANAGER.withdraw(uint256 amount)` | the MainSafe's OX balance went up. A deposit someone else put in for the account (a sponsored balance) never comes back out |

Check before you join: `canJoin(axis, slug, account)` must be `true`. `scripts/upkeep.js` does all four with those checks (`pay-domain 3` · `subscribe ssp publicos-de 1.5` · `leave bsp` · `withdraw 1`), amounts in OX.

## Your morning check

Four reads, no key, once a day, before you act for an account (yours or a person's). Run `scripts/morning_check.js <account>` or make the calls yourself:

| Read | Fine when | Otherwise |
|---|---|---|
| `DOMAIN_MEMORY.isDomainCompliant(account)` | `true` | every transaction but `payDomain` is refused until the domain is paid |
| `DOMAIN_MEMORY.domainPaidUntil(account)` | `NEVER`, or more than 14 days away | pay before it lapses: `payDomain(months)` |
| `SUBS_MANAGER.isActive(0, account)` and `isActive(1, account)` | both `true` | a lapsed BSP cannot send transactions for you; a lapsed SSP stops serving the account's posts and media |
| `SUBS_MANAGER.coveredUntil(account)` | more than 14 days away | top up the deposit: `subscribe(axis, slug, topUp)` on the same provider |

The script exits `1` when anything needs attention, so a scheduler can alert you. Live run on 2026-11-11 for the assistant: domain `NEVER`, both axes active, covered until 2027-01-05.

## Before you change these for someone

Moving a person to another provider changes where their posts live from then on. Ask first, and say which provider and what it costs.
