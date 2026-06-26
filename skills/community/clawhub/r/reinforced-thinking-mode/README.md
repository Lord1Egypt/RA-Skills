# Reinforced Thinking Mode - Publish Description

## Skill Name
**Reinforced Thinking Mode**

## One-line Description
Enforce multi-round independent deep thinking to generate high-quality, comprehensive solutions with strict constraints preventing lazy thinking and hallucination.

## Detailed Description

Reinforced Thinking Mode is a disciplined approach to complex problem-solving that ensures AI agents conduct thorough, independent, and high-quality thinking across multiple rounds.

### The Problem It Solves

Standard multi-round thinking often suffers from:
- **Lazy thinking**: Agents leave TODOs and "improve later" markers
- **Context pollution**: Carrying too much context from previous rounds limits creativity
- **Internal hallucination**: Pretending to complete 10 rounds while actually just summarizing
- **Iterative dependency**: Relying on "next round" to fix current round's shortcomings

### The Solution

This skill enforces strict constraints to ensure:
1. **True Independence**: Each round reads only `problem.md` and the previous round's solution
2. **Final Delivery Quality**: Every round must be complete with no TODOs or "improve later"
3. **No Hallucination**: File I/O forces fresh thinking, preventing internal shortcuts
4. **Internal Self-Review**: Self-check without recording to avoid affecting next round

## Key Features

- ✅ **Mindset Shift**: "Every round is the final round" mentality
- ✅ **Strict File Constraints**: Only read necessary files each round
- ✅ **Forbidden Keywords**: Automatic prevention of lazy patterns (TODO, next round, etc.)
- ✅ **Independence Declaration**: Each solution declares its independence
- ✅ **No Review Files**: Internal self-check only, keeping next round truly independent
- ✅ **Flexible Output**: No fixed templates, adapt to specific problem needs

## Use Cases

- Complex system architecture design
- Multi-dimensional decision making
- Innovative solution exploration
- Comprehensive risk assessment
- Strategic planning with multiple alternatives

## How to Use

1. Create a working directory
2. Define your problem in `problem.md`
3. Run the skill with desired number of rounds (default: 5, recommended: 10)
4. Each round generates an independent `round_{n}.md` solution
5. Final report integrates all solutions

### Example

```bash
# Start reinforced thinking
reinforced_thinking --problem "Design a scalable microservices architecture" --rounds 10

# Output structure
reinforced-thinking/
├── problem.md
├── round_1.md      # Independent solution 1
├── round_2.md      # Independent solution 2
├── ...
├── round_10.md     # Independent solution 10
└── final_report.md # Integrated recommendations
```

## Why This Works

The key insight: **Writing files prevents internal hallucination**. When AI must read files each round, it cannot rely on internal memory or pretend to have done deep thinking. Each round starts fresh, ensuring true independent analysis.

## Language Support

- English (Primary)
- Chinese (Available as `skill_cn.md`)

## Tags

`thinking`, `problem-solving`, `multi-round`, `independent-thinking`, `quality-assurance`, `constraints`, `architecture`, `decision-making`

## Author

[Your Name/Organization]

## License

MIT
