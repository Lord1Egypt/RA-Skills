# Weight Adjustment by Skill Type

## Adjustment Matrix

| Skill Type | D1 Design | D2 Content | D3 Security | D4 Usability |
|------------|-----------|------------|-------------|--------------|
| Security scanner | 20% | 15% | 45% | 20% |
| CLI wrapper / tool | 25% | 20% | 25% | 30% |
| Writing / creative | 30% | 35% | 10% | 25% |
| Workflow / process | 30% | 25% | 15% | 30% |
| API integration | 20% | 20% | 25% | 35% |
| Pure reference / docs | 15% | 45% | 10% | 30% |
| Default (unclassifiable) | 30% | 25% | 30% | 15% |

## How to Classify

1. Read SKILL.md description and body
2. Identify the **primary purpose** (what the skill mainly does for the user)
3. Match against the type that best describes the primary purpose:

| Primary Purpose | Type |
|----------------|------|
| Scanning, auditing, or vetting code/skills for threats | Security scanner |
| Automating external service operations (Feishu, Notion, Gmail…) | API integration |
| Multi-step process, checklist, or workflow orchestration | Workflow / process |
| Generating text, creative content, or documentation | Writing / creative |
| Wrapping CLI tools for direct command execution | CLI wrapper / tool |
| No scripts/, only references/ and/or assets/ | Pure reference / docs |

Key: classification is based on **purpose**, not file structure. A workflow skill with scripts/ is still "Workflow", not "CLI wrapper". Only classify as CLI wrapper when the primary function is executing individual commands via scripts.

## Mixed Types

Many skills span multiple types. For mixed types:
1. Identify the **primary** type (what the skill mainly does)
2. Use that type's weights
3. If truly 50/50 split, average the two weight sets and round

Example: A skill that is 60% workflow + 40% CLI wrapper → use workflow weights (primary type wins).

## Unclassifiable

If no rule matches clearly, use Default weights (30/25/30/15).
