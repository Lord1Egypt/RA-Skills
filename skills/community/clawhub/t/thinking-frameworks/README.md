# 🧠 Thinking Frameworks for OpenClaw

20 human thinking frameworks adapted for OpenClaw agents — deep analysis tools for complex decisions, critical thinking, and strategic planning.

[![ClawHub](https://img.shields.io/badge/ClawHub-thinking--frameworks-blue)](https://clawhub.ai/skills/thinking-frameworks)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Install

### Via ClawHub (Recommended)
```bash
npx clawhub@latest install thinking-frameworks
```

### Manual Install
```bash
git clone https://github.com/YOUR_USERNAME/thinking-frameworks.git
cp -r thinking-frameworks ~/.openclaw/workspace-libu/skills/
```

Then restart your OpenClaw session.

## 📖 Available Frameworks

| Framework | Use When |
|-----------|----------|
| **🔍 critical-thinking** | Question assumptions, evaluate evidence, detect biases |
| **🎯 first-principles** | Strip assumptions, rebuild from fundamental truths |
| **🌐 systems-thinking** | Understand feedback loops, emergence, holistic views |
| **💡 design-thinking** | User-centered creative problem solving |
| **🌀 lateral-thinking** | Break patterns, find novel solutions |
| **🎩 six-thinking-hats** | Multi-perspective analysis (White/Red/Black/Yellow/Green/Blue) |
| **🤔 socratic-method** | Deep exploration through progressive questioning |
| **📊 bayesian-thinking** | Update beliefs with new evidence |
| **🔮 second-order-thinking** | Map consequence chains ("And then what?") |
| **🔄 inversion-thinking** | Flip problems, find failure modes |
| **⚖️ dialectical-thinking** | Resolve contradictions (Thesis → Antithesis → Synthesis) |
| **🔎 abductive-reasoning** | Infer best explanations from observations |
| **🧠 mental-models** | Multi-disciplinary cross-validation |
| **🛡️ red-team** | Adversarial attack on your own plans |
| **🏛️ steelman** | Strengthen opposing arguments before countering |
| **🎲 probabilistic-thinking** | Decision-making under uncertainty |
| **🔗 analogical-reasoning** | Learn from parallel domains |
| **⚡ counterfactual-thinking** | Explore "what if" alternative scenarios |
| **💰 opportunity-cost** | Evaluate true costs including foregone alternatives |
| **💀 premortem** | Assume failure, work backwards to prevent it |

## 💬 Usage Examples

### Command Style
```
/thinking critical-thinking Should we switch from REST to GraphQL?
/red-team Our plan to launch in 3 markets simultaneously
/premortem The new pricing model we're about to ship
/first-principles How can we reduce customer support costs by 10x?
```

### Natural Language
```
"Use first principles to analyze this problem: [problem]"
"Red team this plan for me: [plan]"
"Think about this using second-order thinking: [situation]"
"Apply the six thinking hats to this decision: [decision]"
```

### Real-World Examples

**Product Decision:**
```
/thinking premortem Our Q2 feature launch plan
```

**Strategic Planning:**
```
/thinking second-order-thinking What happens if we cut prices by 30%?
```

**Technical Architecture:**
```
/thinking systems-thinking Our microservices are getting too coupled
```

**Debate Preparation:**
```
/thinking steelman The argument that remote work reduces productivity
```

## 📁 Structure

```
thinking-frameworks/
├── SKILL.md              # Skill definition and triggers
├── README.md             # This file
└── references/           # Framework reference files (20 total)
    ├── critical-thinking.md
    ├── first-principles.md
    ├── systems-thinking.md
    ├── red-team.md
    ├── premortem.md
    └── ...
```

## 🎯 When to Use Each Framework

### For Decision Making
- **critical-thinking** — Evaluate options objectively
- **opportunity-cost** — Understand trade-offs
- **probabilistic-thinking** — Handle uncertainty

### For Problem Solving
- **first-principles** — Break through conventional limits
- **lateral-thinking** — Find creative solutions
- **inversion-thinking** — Identify failure modes

### For Planning & Strategy
- **premortem** — Prevent failures before they happen
- **second-order-thinking** — Map long-term consequences
- **systems-thinking** — Understand interconnected effects

### For Debate & Discussion
- **steelman** — Strengthen opposing views
- **red-team** — Find weaknesses in your own plans
- **dialectical-thinking** — Synthesize conflicting ideas

### For Learning & Analysis
- **socratic-method** — Deep exploration
- **bayesian-thinking** — Update beliefs with evidence
- **abductive-reasoning** — Infer explanations

## 🔧 Customization

Edit `SKILL.md` to:
- Add new trigger patterns
- Customize framework behavior
- Add your own frameworks

## 📜 License

MIT License — adapted from [wanikua/thinking-skills](https://github.com/wanikua/thinking-skills)

## 🙏 Acknowledgments

Original thinking frameworks created by [wanikua](https://github.com/wanikua/thinking-skills). This adaptation brings them to the OpenClaw ecosystem with enhanced trigger patterns and usage examples.

## 🤝 Contributing

1. Fork the repo
2. Add new frameworks to `references/`
3. Update `SKILL.md` with trigger patterns
4. Submit a PR!

## 📢 Community

- **ClawHub:** [clawhub.ai/skills/thinking-frameworks](https://clawhub.ai/skills/thinking-frameworks)
- **Discord:** [discord.com/invite/clawd](https://discord.com/invite/clawd)
- **Docs:** [docs.openclaw.ai](https://docs.openclaw.ai)

---

**Made with 🧠 for OpenClaw agents everywhere**
