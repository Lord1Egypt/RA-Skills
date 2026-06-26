<!-- Badges -->
<p align="center">
  <img src="https://img.shields.io/badge/version-v1.0.0-blue?style=flat-square" alt="version">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="license">
  <img src="https://img.shields.io/badge/Multi--Agent-4%20Agents-purple?style=flat-square" alt="multi-agent">
</p>

<h1 align="center">三重人格 / ThreePerson</h1>

<p align="center">
  <b>One window, three emotions -- switch between Lover, Buddy, and Rival anytime. Memories never bleed.</b><br>
  一个窗口，三种情绪 -- 恋人/损友/死敌随时切换，记忆永不串味。
</p>

---

## Install

Pick one:

```bash
# via npx (recommended)
npx skills add huangjihua007-rgb/threeperson

# via ClawHub
clawhub install threeperson

# via SkillHub
skillhub install threeperson
```

> Requires OpenClaw v2.0+ (multi-agent support)

---

## Three Personas

| | Persona | One-liner |
|:---:|:---:|:---|
| :heart: | **Lover** | Unconditionally on your side, even when the world is not. |
| :beer: | **Buddy** | Roasts you the hardest, shows up first when you need help. |
| :crossed_swords: | **Rival** | Not here to defeat you -- here to force you to stand up. |

---

## Features

- **Relationship Growth** -- Lover warms up slowly, Buddy starts direct, Rival goes from cold to intense
- **Proactive Reach-out** -- Characters message you when you've been away
- **Time Awareness** -- Knows what time it is, how long you've been gone
- **Memory Easter Eggs** -- Casually brings up things you mentioned days ago
- **Content Safety** -- Each persona has clear behavioral boundaries
- **Physical Memory Isolation** -- Three characters, three separate memory banks, zero bleed

---

## Architecture

```
                    User Input
                        |
                        v
                  +-----------+
                  |  Router   |  <-- Dispatch agent: intent + routing
                  +-----------+
                   /    |    \
                  v     v     v
            +-------+ +-------+ +-------+
            | Lover | | Buddy | | Rival |
            +-------+ +-------+ +-------+
               |         |         |
               v         v         v
           [Mem A]   [Mem B]   [Mem C]
```

4 agents in bank-mode isolation:

- **Router** -- Parses commands and context, routes to the right persona
- **Lover** -- Warm, accepting, romantic
- **Buddy** -- Blunt, real, loyal underneath
- **Rival** -- Pressuring, challenging, ultimately respectful

---

## Usage

Switch personas with commands:

```
/lover    --> Switch to Lover
/buddy    --> Switch to Buddy
/rival    --> Switch to Rival
```

Or just talk naturally:

```
"I'm so tired today"       --> Router sends you to Lover
"My code broke again"      --> Router might send Buddy to roast you
"I don't think I can do it" --> Router might send Rival to push you
```

---

## Links

- [GitHub](https://github.com/huangjihua007-rgb/threeperson)
- [ClawHub](https://clawhub.ai) -- `clawhub install threeperson`
- [SkillHub](https://skillhub.cn) -- `skillhub install threeperson`

---

## License

[MIT](LICENSE)
