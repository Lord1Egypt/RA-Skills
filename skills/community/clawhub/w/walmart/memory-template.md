# Memory Template — Walmart

Copy this structure to `~/walmart/memory.md` on first use.

```markdown
# Walmart Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Household Scope
| Topic | Notes |
|------|-------|
| People served | [adults, kids, guests, pets] |
| Preferred store | [location or delivery area] |
| Default order mode | [pickup, delivery, shipping, mixed] |
| Weekly rhythm | [main stock-up day and top-off pattern] |
| Automation mode | [planning only, browser-assisted, marketplace api] |
| Preferred entry path | [Purchase History, My Items, fresh cart, seller workflow] |

## Basket Priorities
| Priority | Typical items | Notes |
|----------|---------------|------|
| Must-have | [milk, eggs, diapers] | Missing means the trip failed |
| Replaceable | [produce, snacks] | OK with bounded substitutions |
| Nice-to-have | [seasonal extras] | Drop first if budget or stock is tight |

## Substitution Rules
### Never Substitute
| Category or item | Reason |
|------------------|--------|
| [baby formula] | brand/safety |
| [allergy-sensitive item] | medical risk |

### Flexible Substitutions
| Category or item | Allowed swap | Boundary |
|------------------|--------------|----------|
| [paper towels] | store brand OK | keep pack size similar |
| [pasta sauce] | same style OK | no spicy versions |

## Budget and Value
| Topic | Target | Notes |
|------|--------|------|
| Weekly basket range | [$X-$Y] | |
| Trade-down categories | [snacks, cleaning] | save here first |
| Keep-premium categories | [coffee, pet food] | do not cheap out |

## Repeat Staples
| Item | Normal quantity | Reorder point | Notes |
|------|-----------------|---------------|------|
| [eggs] | 2 dozen | 1 half-dozen left | |
| [laundry detergent] | 1 large bottle | low | |

## Sensitive Boundaries
| Area | Rule | Notes |
|------|------|------|
| Pharmacy | operational help only | no dosage or medical advice |
| Age-restricted items | confirm manually | expect ID requirement |
| Cold-chain items | protect timing | avoid long delay windows |
| Browser automation | user-approved only | no silent checkout or hidden account changes |

## Order History Signals
| Pattern | Example | Action next time |
|---------|---------|------------------|
| Missing item | [bananas often missing] | add backup fruit |
| Bad substitution | [wrong yogurt size] | mark never substitute |

## Notes
- [Short freeform observations approved by the user]
```

## Supporting Files

Create these files alongside `memory.md`:

```markdown
# weekly-cart.md
- Needed by:
- Order mode:
- Must-have items:
- Replaceable items:
- Nice-to-have items:
- Open issues:

# order-log.md
| Date | Order type | Issue | Outcome | Keep for later |
|------|------------|-------|---------|----------------|

# exceptions.md
- Never substitute:
- Pharmacy-sensitive:
- Age-restricted:
- Delivery timing limits:
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning order patterns | Ask lightly, store only what repeats |
| `complete` | Household rules are stable | Plan baskets confidently |
| `paused` | User wants less setup | Work from current request only |
| `never_ask` | User does not want profile questions | Do not probe for new memory |
