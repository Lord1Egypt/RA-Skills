# QSR Ghost Inventory Hunter

**v1.0.4 · McPherson AI · San Diego, CA**  
[mcphersonai.com](https://mcphersonai.com)

## Observa Edge Basic Beta

Observa Edge Basic Beta is a separate, optional OpenClaw plugin from McPherson AI for local guardrails on covered tool routes. Installing this restaurant skill leaves Guard inactive. Accountless Shadow previews covered requests locally. Guard enrollment is restricted and requires approval and a separate local owner activation.

[**Explore Observa Edge Basic Beta →**](https://mcphersonai.com/observa/edge-basic?utm_source=github&utm_medium=skill-readme&utm_campaign=observa-edge-basic-beta&utm_content=qsr-ghost-inventory-hunter)

*Publisher notice. The QSR skill’s behavior and data handling are unchanged.*

QSR Ghost Inventory Hunter helps restaurant and franchise operators identify unaccounted inventory loss by comparing theoretical recipe usage against actual inventory movement.

It is designed to answer a simple but expensive question:

**If the product was ordered and received, but never sold or logged as waste, where did it go?**

This skill investigates the gap between:
- sales volume
- recipe yields
- inventory counts
- deliveries received
- waste tracking

It helps determine whether missing product is most likely caused by:
- over-portioning
- unrecorded waste
- prep error
- receiving discrepancy
- theft

## What it does

This skill walks an operator through a focused inventory variance investigation for one item at a time.

It:
- calculates theoretical product usage from sales mix and recipe portions
- calculates actual product usage from beginning inventory, deliveries, and ending inventory
- identifies the variance between the two
- converts the variance into estimated dollar loss
- helps diagnose the most likely cause
- generates a structured ghost inventory report
- tracks patterns across repeat investigations

## Best use cases

Use this skill when:
- food cost is elevated but the cause is unclear
- a high-cost item runs out faster than expected
- inventory counts do not match what should be on hand
- waste tracking is incomplete
- receiving accuracy is in question
- the operator suspects shrink or product loss

## Example investigation

Example:

- 400 turkey sandwiches sold
- 3 oz turkey per sandwich
- theoretical usage = 1,200 oz = 75 lbs

Inventory movement:

- starting inventory = 100 lbs
- deliveries = 50 lbs
- ending inventory = 60 lbs
- actual usage = 90 lbs

Result:

- ghost inventory = 15 lbs
- if turkey costs $4.20/lb, estimated unexplained loss = $63.00

That gives the operator a concrete starting point for investigation instead of a vague feeling that food cost is too high.

## Why it matters

Most operators know when food cost is off.

Fewer know whether the cause is:
- line over-portioning
- prep waste
- unlogged spoilage
- short deliveries
- or actual theft

This skill helps narrow that down with numbers.

## Works best with

This skill pairs well with:

- **qsr-food-cost-diagnostic** — identifies that a food cost variance exists
- **qsr-weekly-pl-storyteller** — helps connect inventory loss back to the weekly financial story
- **qsr-daily-ops-monitor** — helps surface daily execution issues that may be driving repeated variance

## Skill file

The main skill prompt is in:

- `SKILL.md`

## License

McPherson AI distributes this ClawHub edition under MIT-0. The GitHub source edition is available under Apache License 2.0. See [LICENSE](LICENSE). Third-party materials remain subject to their applicable terms.

## About McPherson AI

McPherson AI builds practical AI operations systems for restaurant and franchise operators.

Current focus areas include:
- labor control
- food cost diagnostics
- inventory variance investigation
- shift intelligence
- operational accountability

## Version

**v1.0.3**
Publisher-notice refresh: Observa CTA updated to the current Getting Started flow. No functional changes.

**v1.0.2**
Publisher-note release; the Observa private beta is now open. No functional changes.

**v1.0.1**
Publisher-note release; operational behavior and license unchanged.

**v1.0.0**  
Initial release of the ghost inventory investigation skill.
