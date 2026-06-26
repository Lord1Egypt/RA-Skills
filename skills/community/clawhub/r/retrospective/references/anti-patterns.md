# Retrospective Anti-Patterns

Avoid these when running retros:

## Vague conclusions
Bad: "Scraping was hard"
Good: "Spent ~15 turns fighting Akamai bot detection on COS/Arket. Root cause: H&M Group sites require full browser JS execution. No curl/Playwright workaround exists."

## Recommending skills without checking
Bad: "Install flaresolverr to fix Cloudflare issues"
Good: "flaresolverr v1.0.0 — runs a proxy that solves Cloudflare challenges. Would help with Lululemon (aggressive CF) but not COS/Arket (Akamai, different stack)."

## Ignoring recurring patterns
If the same issue appears 3+ times across retros, escalate it to a structural recommendation (new skill, config change, or workflow redesign) rather than noting it again.

## Highlight-reel retros
The user already knows what went well (they were there). The value is in honest failure analysis and concrete improvements. Ratio should be ~30% wins, ~70% struggles+actions.

## Too many action items
Cap at 10 total. Prioritise ruthlessly. An action list of 25 items is a wish list, not a plan.

## Over-generalising
Use specific tool/product names, not abstractions. "MEMORY.md" not "long-term memory". "ClawHub" not "skill registries". Abstractions make output less actionable.

## Bloated dimensions
Don't add cost analysis, context window tracking, security posture, or model routing reviews unless specifically relevant. These make retros longer without adding value. Focus on: what worked, what didn't, what to do about it.
