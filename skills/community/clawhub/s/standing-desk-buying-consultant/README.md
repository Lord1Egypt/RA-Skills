# Standing Desk Buying Consultant

> Turns any AI agent into an expert standing desk buying consultant.

## What it does

Guides first-time and upgrading standing desk buyers through a structured consultation to identify exactly which specs they need for their height, equipment load, workspace, and region — without relying on biased sales advice. Calculates the user's required height range and weight capacity from their inputs, then delivers a prioritised spec list and up to 5 matched product suggestions.

## How it works

1. Agent asks targeted, research-backed questions grouped by theme: user height, equipment load, workspace dimensions, lifting mechanism, stability needs, usage pattern, surface preferences, and regional standards
2. Calculates required minimum and maximum desk height from the user's stated height using ergonomic elbow-height approximations
3. Estimates total desktop load from the user's equipment list and applies a 20–30% safety margin to determine minimum weight capacity
4. Flags common buyer mistakes proactively (e.g., height range too short for tall users, undersized weight capacity, manual crank for frequent adjusters, wide desktop on narrow frame)
5. Delivers a structured spec recommendation: non-negotiable → recommended → optional, plus a Spec Summary Card
6. Suggests up to 5 real desks matching the user's confirmed specs — only after the full spec list is complete

## Requirements

- No external APIs or environment variables required
- No runtime dependencies
- Works with any AI agent that supports SKILL.md (OpenClaw, ClawHub, etc.)
- Pure instruction-based — agent reasoning does the work

## Specs covered

| Dimension              | What the skill determines                                                              |
| ---------------------- | -------------------------------------------------------------------------------------- |
| Height range           | Min height (seated elbow) and max height (standing elbow), calculated from user height |
| Weight capacity        | Estimated load from equipment list + 20–30% safety margin                              |
| Motor type             | Electric dual / Electric single / Manual crank                                         |
| Column stages          | 2-stage vs 3-stage (stability at height)                                               |
| Crossbar / rear beam   | Stability vs legroom trade-off                                                         |
| Desktop width          | Based on monitor count and setup                                                       |
| Desktop depth          | Based on monitor distance preference                                                   |
| Memory presets         | Required count based on users sharing the desk                                         |
| Anti-collision         | Safety relevance based on environment                                                  |
| Regional certification | UL / CE / BIFMA / RCM based on country and setting                                     |
| Surface material       | Laminate / bamboo / solid wood and edge profile                                        |

## Installation

Add via ClawHub or reference the SKILL.md directly in your agent configuration.

## License

MIT

## Homepage

https://github.com/arbazex/personal-tech-buying-consultants/tree/master/standing-desk-buying-consultant
