# 🦞 ClawScan: wildidea

> Wild Domain Injection Brainstorming Engine — Throw unrelated things next to each other and let the friction spark ideas.

## Quickstart

```python
# 1. Inject 3 remote channels
domains = load("references/paradigms.md")       # 17 domains, pick 3
seeds = run("scripts/pick_seed.py")             # 2 random Mao quotes
chars = run("scripts/search_char.py")           # 2 random chars → real web domain

# 2. Juxtapose → find nails → find counterparts
for each domain/seed/char domain:
    nail = extract_one_specific_operation_or_constraint(numeral!)
    counterpart = find_one_specific_product_or_feature(numeral!)
    output(nail + " | " + counterpart)

# 3. Gate check
if counterpart_feels_reasonable():     # 🌪️ Comfort
    reroll()
if search_exists(counterpart):          # 🔍 Web verification
    reroll()
```

## The One Rule

> **Zero abstraction between nail and counterpart.**
> No "because", "therefore", "this means", "this shows", "this implies".
> Just raw juxtaposition. Let the user make the connection.

## Input Format

```
nail (concrete operation/event/constraint from remote domain, must include number/time/boundary)
  |
  | ← BLANK. No words here.
  v
counterpart (concrete existing product/tech/feature name from user's domain)
```

## Nail Examples

| Domain | ✅ Concrete Nail | ❌ Abstract |
|--------|-----------------|-------------|
| Deep sea vents | "Tube worms grow 1mm/year, live 300 years" | "Slow growth strategy" |
| Honeybees | "75ms wing flutter = 1km distance" | "Efficient communication" |
| Monasteries | "One lamb skin = 3-4 parchment folios" | "Resource scarcity mindset" |
| Alchemy | "Mars hour → iron work, Venus hour → copper" | "Timing is a craft parameter" |
| Polar expedition | "Shackleton abandoned all gear to save crew" | "Prioritizing human life" |

## Gate: Comfort Check

Ask: "Would this get pushback if posted in an internal product review?"

| If answer | Verdict |
|-----------|---------|
| "Nah, makes sense" | ❌ Too reasonable. Reroll. |
| "WTF but there's something there" | ✅ Pass |

## Gate: Web Verification

Check Tavily/brave search for the counterpart + domain query.

| If search finds | Verdict |
|----------------|---------|
| Product/patent/article describing the same concept | 🚫 Ban. Reroll (max 3x). |
| Weak match or no result | ✅ Pass |

## Output Format

```markdown
| Nail (domain's concrete constraint) | Counterpart (user's concrete thing) | 🌪️/🔍 |
|-------------------------------------|-------------------------------------|--------|
| Honeybees: 75ms flutter = 1km      | App: daily quota of 3 predictions   | ✅/✅  |
| Shackleton: abandoned all gear      | Feature: one-button "reset"          | ✅/✅  |
```

No commentary. No interpretation. No "therefore."

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Full spec (this) |
| `references/paradigms.md` | 17 remote domains with ~7 paradigms each |
| `references/mao-seeds.md` | 50 Mao Zedong quotes for seed channel |
| `references/common-chinese-chars.txt` | ~500 Chinese character pool |
| `scripts/pick_seed.py` | Random seed picker (run `python3 scripts/pick_seed.py`) |
| `scripts/search_char.py` | Random char + Tavily search (run `python3 scripts/search_char.py`) |
| `templates/poster.html` | HTML poster template for visual output |
| `templates/output-example.md` | Sample output format |

## Dependencies

- Python 3
- Tavily API key in `~/.openclaw/.env` as `TAVILY_API_KEY`
- For poster: modern browser

## Origin

Created by [liwenyu2002](https://github.com/liwenyu2002/wildidea) for Hermes Agent. Iterated through 5 major versions (V1: multi-step analysis → V5: pure juxtaposition, zero abstraction).

## When NOT to use

- When user wants predictive/statistical answers (use data science)
- When user wants causal reasoning (use systematic debugging)
- When user just wants to know what already exists (use web search)
- **Use exclusively for: stuck on a creative problem, need to break out of thinking rut**
