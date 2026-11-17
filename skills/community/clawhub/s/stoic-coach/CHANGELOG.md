# Changelog
## 2.0.3 — 2026-11-17

发布面修正，无功能变更。

- **首屏重写**：显示名补中文 + 首屏加场景句 + tag 从 1.4.0 刷新
- **显示名**：发布时必须带 `--name "斯多葛日常 · Stoic Daily Practice"`（此前未能稳定带中文名）
- **检索面**：tags 刷新到 2.0.3 并补齐语义 tag（`stoic,philosophy,coaching,personal-growth,reflection`）；topics 同步为 `斯多葛,哲学练习,情绪管理,晨间复盘,晚间复盘`

## 2.0.2 — 2026-10-27

- 首屏中文化：description 中文前置并给出使用场景（事情有点乱、想把可控与不可控切开），保留英文触发词以维持英文检索。功能零变化。

## 2.0.1 — 2026-09-17

- Converted daily practice cards from Chinese interface copy into language-neutral prompt meanings.
- Marked the Chinese one-minute example as illustrative rather than a fixed product locale.

## 2.0.0 — 2026-09-17

- Repositioned `stoic-coach` as `Stoic Daily Practice`.
- Added four independent modes: One-Minute Control Check, Morning Preview, Evening Review, and Situation Practice.
- Expanded activation from formal Stoic-framework wording to explicit natural-language practice requests.
- Replaced the mandatory seven-part analysis with low-friction practice cards.
- Removed the requirement to end every response with a clarifying question.
- Added control/influence/outcome separation and one-action completion.
- Added explicit safeguards against emotion suppression, victim-blaming, and passive tolerance of harm.
- Kept the default conversation-only with no silent persistence.
