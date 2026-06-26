<p align="center">
  <img src="https://img.shields.io/badge/version-v1.0.0-blue?style=flat-square" alt="version">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="license">
  <img src="https://img.shields.io/badge/lang-Chinese-red?style=flat-square" alt="chinese">
  <img src="https://img.shields.io/badge/rules-40%2B-orange?style=flat-square" alt="rules">
</p>

<h1 align="center">亲笔写的</h1>

<p align="center">
  <b>让领导看不出是AI写的。</b><br>
  Detect and fix AI-generated Chinese text. Platform-aware rewriting.
</p>

---

## Install

```bash
# via npx (recommended)
npx skills add huangjihua007-rgb/qinbixiede

# via ClawHub
clawhub install qinbixiede

# via SkillHub
skillhub install qinbixiede
```

---

## What It Does

1. **Diagnose** -- Scan your Chinese text for AI patterns (40+ rules, severity-graded)
2. **Rewrite** -- Transform it into platform-specific human style
3. **Explain** -- Tell you exactly what was wrong and what changed

---

## Supported Platforms

| Platform | Style | Command |
|----------|-------|---------|
| WeChat Articles | Hook + story + emotion | `/qinbi gongzhonghao` |
| Zhihu | Opinion + evidence + depth | `/qinbi zhihu` |
| Xiaohongshu | Diary + details + casual | `/qinbi xiaohongshu` |
| Work Reports | Conclusion-first + data | `/qinbi huibao` |
| WeChat Moments | Short + warm + incomplete | `/qinbi pengyouquan` |
| General | Just remove AI patterns | `/qinbi tongyong` |

---

## Example

**Before (AI-generated):**

> 在当今数字化转型的大背景下，AI正在深刻改变着各行各业。我们不仅需要积极拥抱变革，更要深入思考如何保持核心竞争力。综上所述，未来可期。

**Diagnosis:**

```
[fatal] "在当今...大背景下" -- template opening
[fatal] "不仅...更要..." -- forced parallelism
[fatal] "综上所述...未来可期" -- cliche ending
[fatal] zero personal details, zero specific examples

AI score: HEAVY
```

**After (WeChat Article style):**

> 上周五改PPT改到第三版的时候，旁边实习生说了句："学姐，这个ChatGPT 30秒就能做。"
>
> 五年经验，干不过一个prompt？
>
> 后来我真试了。5分钟搞定了我改一下午的东西。但说个反直觉的事——用了半年AI之后，我反而加薪了。

---

## Why Not humanizer-zh?

| | humanizer-zh | 亲笔写的 |
|---|---|---|
| Rules | Translated from English Wikipedia | Built natively for Chinese |
| Chinese patterns | Detects "-ing endings" (irrelevant) | Detects 体制词/排比/成语/总分总 |
| Platform styles | None | 5 platform-specific rewrites |
| Updates | v1.0.0, never updated | Active development |
| Examples | None | Real before/after samples |

---

## Detection Categories

| Category | Rules | Examples |
|----------|:-----:|---------|
| Vocabulary | 12 | 赋能/闭环/深耕/综上所述/未来可期 |
| Sentence patterns | 14 | 排比三连/对偶/万能开头/机械过渡 |
| Emotion | 10 | 零立场/假共情/过度正能量 |
| Structure | 8 | 工整病/总分总/段落均匀 |
| Punctuation | 5 | 分号癖/省略号缺失 |

---

## Links

- [ClawHub](https://clawhub.ai/skills/qinbixiede)
- [SkillHub](https://skillhub.cn)
- [GitHub](https://github.com/huangjihua007-rgb/qinbixiede)

---

## License

MIT
