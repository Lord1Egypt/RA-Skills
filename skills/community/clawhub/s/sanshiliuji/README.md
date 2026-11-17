# 三十六计 Strategic Analysis Skill

> 以世界顶级思维框架重构三十六计——博弈论、系统论、认知心理学、孙子兵法、现代竞争战略的深度融合。

## What is this?

A Claude Code skill that transforms the ancient Chinese Thirty-Six Stratagems (三十六计) into a modern multi-dimensional strategic analysis framework. Input any competitive scenario — business, negotiation, military, game theory — and receive a rigorous strategic analysis powered by seven world-class thinking frameworks.

## Features

- **3-Level Auto-Adaptive Depth**: Quick stratagem lookup → Focused tactical application → Full 7-dimension strategic analysis
- **7 Analytical Frameworks**: Game Theory, Systems Thinking, Cognitive Psychology, Sun Tzu Meta-Principles, Modern Competitive Strategy (Porter/Blue Ocean/OODA), 4-Layer Depth Model, 7 Meta-Thinking Paradigms
- **36 Stratagems Full Catalog**: Classical text, mechanisms, framework mappings, modern applications, conditions, and countermeasures for each
- **Bilingual**: Full Chinese and English support, auto-detection
- **Smart Triggering**: Auto-activates on strategic keywords or explicit `/stratagem` invocation

## Installation

### For Claude Code

```bash
# Copy to your project or global skills directory
cp -r stratagem/ ~/.claude/skills/stratagem/
```

### Via ClawHub

```bash
npx clawhub@latest install stratagem
```

## Usage

### Quick Lookup (Level 1)
```
什么是围魏救赵？
Tell me about stratagem 18
```

### Focused Application (Level 2)
```
如何用声东击西做薪资谈判？
How to use "Loot a Burning House" in my market entry?
```

### Full Strategic Analysis (Level 3)
```
我们初创公司被字节和腾讯双重挤压，市场份额从15%降到5%，该怎么办？
Analyze Tesla vs BYD competitive dynamics from a game theory perspective
```

### Explicit Invocation
```
/stratagem [your scenario]
/36计 [your scenario]
```

## File Structure

```
stratagem/
├── SKILL.md                   # Main orchestrator
└── references/
    ├── catalog.md             # Complete 36 stratagems catalog
    ├── framework.md           # 7-dimension analytical framework
    └── depth-routing.md       # Depth classification decision table
```

## Tags

`strategy` `game-theory` `business` `competitive-analysis` `chinese-classics` `sun-tzu` `military-strategy` `negotiation` `systems-thinking` `cognitive-psychology` `decision-making` `leadership`

## License

MIT
