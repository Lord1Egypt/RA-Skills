<h1 align="center">Product Sense Coach</h1>

<p align="center">
  <strong>A thinking partner for product managers — turn raw intuition into clear product vision</strong>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#what-it-does">What It Does</a> •
  <a href="#see-it-in-action">See It in Action</a> •
  <a href="#philosophy">Philosophy</a> •
  <a href="#install">Install</a>
</p>

<p align="center">
  English | <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="https://github.com/viliawang-pm/product-sense-coach/stargazers"><img src="https://img.shields.io/github/stars/viliawang-pm/product-sense-coach?style=social" alt="Stars"></a>
  <a href="https://github.com/viliawang-pm/product-sense-coach/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="License"></a>
  <a href="#"><img src="https://img.shields.io/badge/Agent%20Skills-compatible-green" alt="Agent Skills Compatible"></a>
</p>

---

## The Problem

You have a product idea. It feels right in your gut. But when you try to explain it:

- **Investors** ask "what's the market size?" and you freeze
- **Engineers** ask "what exactly should I build?" and you ramble
- **Friends** nod politely but clearly don't get it

**The idea is good. The articulation is the problem.**

Most AI tools will immediately judge your idea or generate a business plan you didn't ask for. This skill does neither. Instead, it helps you **think out loud** — surfacing the real insight hidden in your intuition.

---

## What It Does

When you share a product idea, the skill walks you through **five natural conversations**:

| Conversation | Core Question | What You Get |
|:------------|:-------------|:------------|
| **The Origin Story** | "What did you observe that others missed?" | A clear articulation of your core insight |
| **The Opportunity Space** | "How big could this be?" | A feel for the scale and shape of the market |
| **The First 100 Users** | "Who shows up on Day 1?" | A tangible growth path starting from real people you know |
| **The Movie Scene** | "Walk me through a user's Friday night" | Vivid, second-by-second usage scenarios |
| **The Landscape** | "Who else has tried, and what can we learn?" | Competitive intelligence framed as learning |

The output is a **Clarity Map** — not a judgment of whether your idea is good or bad, but a clear picture of what you already understand and where to dig deeper.

---

## See It in Action

<details>
<summary><strong>💬 Example: "I want to build a nightclub discovery mini-program"</strong></summary>

**You say:**
> I want to build a WeChat mini-program that shows nightclub events on a map, filterable by music genre. Help me think this through.

**The skill responds:**
> I love that you're combining location and music taste — those are two deeply personal things that most apps treat as generic. What made you think of this? Was there a specific night where you wished this existed?

**You reveal:**
> Last Saturday I wanted to hear techno but ended up at a club playing hip-hop. My friend said "you should have checked their Instagram" but honestly who has time to check 20 club Instagrams every weekend?

**Together you arrive at:**
> I noticed that people who care about music genre — not just "going out" — have no reliable way to find tonight's vibe without checking multiple fragmented sources (Instagram stories, WeChat groups, word of mouth). There's an opportunity to become the single source of truth for "what's playing where tonight."

**The skill continues:**
> Let's make this concrete. Pick one person — give them a name — and walk me through their Friday night from 9pm to midnight. Where does your product appear in that story?

**You describe:**
> Okay, let's call her Mia. She's 26, works in advertising, loves house music. It's Friday 9pm, she just finished dinner with coworkers. Someone says "should we go somewhere?" Mia opens the mini-program, filters for "House" and "Techno", sees three clubs with events tonight, taps one to see the DJ lineup and a 10-second vibe video. She screenshots it, sends to the group chat. Decision made in 90 seconds.

**The skill reflects:**
> That's powerful — the "screenshot to group chat" moment is your viral loop. The product's job is to make Mia look like the friend who always knows where to go. What's the minimum you'd need to build to test if this 90-second flow actually works?

---

**Clarity Map (excerpt):**

| Dimension | Clarity | Current Understanding |
|:----------|:-------:|:---------------------|
| The Problem | ⬤⬤⬤⬤○ | Clear personal pain point; need to validate with 10+ strangers |
| The Path to Users | ⬤⬤⬤○○ | Know the persona; need to identify specific WeChat groups to seed |
| The Experience | ⬤⬤⬤⬤⬤ | Vivid scenario with clear "screenshot moment" |

**Fastest Way to Learn More:**
> This Friday, stand outside 3 different clubs at 11pm. Ask 10 people in line: "How did you decide to come here tonight?" Write down their exact words.

</details>

<details>
<summary><strong>💬 Example: "I want to build an app where neighbors share homemade food"</strong></summary>

**You say:**
> I want to build an app where neighbors can share homemade food.

**The skill responds:**
> I love that you're thinking about food and community together — those are two deeply human things. What made you think of this? Was there a specific moment where you wished this existed?

**You reveal:**
> Last Sunday I made way too much curry and my neighbor mentioned she hates cooking for one person.

**Together you arrive at:**
> I noticed that single people living alone often cook too much or don't cook at all, while their neighbors are in the exact same situation. There's an opportunity to turn apartment buildings into informal dinner communities.

**The skill then guides you through:**
- Market sizing (how many single-person households in your city?)
- Growth paths (which buildings have the highest density of young professionals?)
- Usage scenarios (what does "ordering from your neighbor" actually look like at 7pm on a Tuesday?)
- Competitive landscape (why haven't food delivery apps solved this?)

</details>

---

## Philosophy

Inspired by the product thinking of **Zhang Xiaolong** (creator of WeChat), this skill emphasizes:

| Principle | What It Means |
|:----------|:-------------|
| **Human nature first** | Great products satisfy emotional needs, not just functional ones. Ask "how does the user *feel*?" before "what does the product *do*?" |
| **Simplicity as discipline** | Find the "one-action moment" — the single interaction that captures the entire product's value |
| **Trust the user** | Design simple rules and let behavior emerge. The "screenshot to group chat" moment wasn't designed — it was discovered |

> "产品经理应该像上帝一样，了解人性，建立简单的规则，然后让用户在规则中自行演化。"

---

## Quick Start

**30 seconds to get started:**

```bash
# Clone and install
git clone https://github.com/viliawang-pm/product-sense-coach.git
cp -r product-sense-coach ~/.codebuddy/skills/

# Or for project-level install
cp -r product-sense-coach .codebuddy/skills/
```

Then in any AI conversation:

> "Use the product-sense-coach skill. I want to build [your idea]. Help me think this through."

---

## Install

### Option 1: Global Install (Recommended)

Works across all your projects:

```bash
git clone https://github.com/viliawang-pm/product-sense-coach.git
cp -r product-sense-coach ~/.codebuddy/skills/
```

### Option 2: Project-Level Install

Keep it scoped to one project:

```bash
git clone https://github.com/viliawang-pm/product-sense-coach.git
cp -r product-sense-coach .codebuddy/skills/
```

### Option 3: Claude Desktop / Cursor

Copy `SKILL.md` to wherever your AI tool looks for custom instructions or system prompts.

---

## Who Is This For?

- **Solo founders** who need a thought partner at 2am
- **PMs at companies** who want to pressure-test ideas before the roadmap meeting
- **Side project builders** who have 10 ideas and need to pick the right one
- **Anyone** who's ever said "I have this idea but I can't quite explain it"

---

## FAQ

<details>
<summary><strong>How is this different from asking ChatGPT about my idea?</strong></summary>

ChatGPT will give you a generic SWOT analysis or immediately suggest features. This skill is designed to **ask better questions** — helping you articulate what you already intuitively know, rather than replacing your thinking with generated content.

</details>

<details>
<summary><strong>Will this tell me if my idea is good or bad?</strong></summary>

No. The skill produces a **Clarity Map**, not a verdict. It shows you where your thinking is sharp and where it needs more real-world input. A "good" idea with unclear execution is worse than a "small" idea with crystal clarity.

</details>

<details>
<summary><strong>Can I use this with Claude / GPT-4 / other models?</strong></summary>

Yes. The `SKILL.md` file contains the full system prompt. You can paste it into any AI tool that accepts custom instructions.

</details>

---

## Contributing

Found this useful? Here's how to help:

- ⭐ **Star this repo** — it helps others discover it
- 🐛 **Open an issue** if a conversation flow doesn't work well
- 💡 **Submit a PR** with improvements to the prompts
- 📣 **Share your Clarity Map** — tweet it with #ProductSenseCoach

---

## License

MIT — use it, fork it, make it better.

---

<p align="center">
  <strong>Built for PMs who think in intuition but need to speak in clarity.</strong>
</p>

<p align="center">
  <a href="https://github.com/viliawang-pm/product-sense-coach/stargazers">⭐ Star if this helped you think clearer</a>
</p>
