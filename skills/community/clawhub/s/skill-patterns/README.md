# Agent Skill Design Pattern Templates

Based on Google ADK and ecosystem best practices, providing 5 reusable skill design patterns.

## 🎯 Use Cases

- Need structured templates when creating new Agent Skills
- Optimize existing skill design and quality
- Standardize skill development within teams
- Learn best practices for Agent Skill design

## 📦 Included Patterns

| Pattern | Purpose | Typical Scenarios |
|-----|------|---------|
| [Tool Wrapper](./references/tool-wrapper-pattern.md) | Inject domain expertise | Framework conventions, team agreements, API usage guides |
| [Generator](./references/generator-pattern.md) | Generate structured content | Technical reports, documentation, scaffolding, Commit Messages |
| [Reviewer](./references/reviewer-pattern.md) | Review/audit/score | Code Review, security audits, quality checks |
| [Inversion](./references/inversion-pattern.md) | Interview first, then execute | Project planning with unclear requirements, complex system design |
| [Pipeline](./references/pipeline-pattern.md) | Multi-step sequential execution | Document generation, code migration, data transformation |

## 🚀 Quick Start

### 1. Activate the Skill

Mention these keywords in conversation to activate:
- create skill
- skill template
- skill design
- agent pattern
- skill pattern
- skill structure

### 2. Choose a Pattern

The skill will recommend the most suitable design pattern based on your needs, or combine multiple patterns.

### 3. Create Following Templates

Follow the structure and flow of the recommended pattern to create your skill.

## 📁 Directory Structure

```
skill-patterns/
├── SKILL.md                          # Skill entry point
├── README.md                         # Usage guide
└── references/
    ├── tool-wrapper-pattern.md       # Pattern 1: Tool Wrapper
    ├── generator-pattern.md          # Pattern 2: Generator
    ├── reviewer-pattern.md           # Pattern 3: Reviewer
    ├── inversion-pattern.md          # Pattern 4: Inversion
    ├── pipeline-pattern.md           # Pattern 5: Pipeline
    └── creation-checklist.md         # Creation checklist
```

## 💡 Pattern Combination Examples

- **Generator + Reviewer**: Auto quality check after generating reports
- **Inversion + Generator**: Interview requirements first, then generate solution
- **Pipeline + Reviewer**: Review quality after each step
- **Tool Wrapper + Pipeline**: Load different conventions for each step

## 📊 Decision Tree

```
Is user request clear?
├─ Yes → Need specific domain knowledge?
│   ├─ Yes → Tool Wrapper
│   └─ No → Need fixed output format?
│       ├─ Yes → Generator
│       └─ No → Is it a review task?
│           ├─ Yes → Reviewer
│           └─ No → Single-step execution (no pattern needed)
└─ No → Need multi-turn requirement gathering?
    ├─ Yes → Inversion
    └─ No → Have mandatory multi-step sequence?
        ├─ Yes → Pipeline
        └─ No → Inversion (clarify first)
```

## 📖 Source

Design patterns based on: Google Cloud Tech - "5 Agent Skill design patterns every ADK developer should know"

## 📝 Version

- v1.1.0 - English release with 5 core patterns + creation checklist

## 🤝 Contributing

Welcome to submit new pattern variations and improvement suggestions!
