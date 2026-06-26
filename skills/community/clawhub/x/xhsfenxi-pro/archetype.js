#!/usr/bin/env node
/**
 * xhsfenxi — archetype.js
 * Purpose: Print the archetype classification prompt for a Xiaohongshu creator.
 *          Helps identify whether an account is Type A (荒诞美学), Type B (共鸣命名),
 *          Type C (现实策略), or a hybrid — based on the three proven archetypes
 *          distilled from real analyses of multiple Xiaohongshu creators.
 * Usage:
 *   node scripts/archetype.js <creator-name>
 *   node scripts/archetype.js <creator-name> --quick
 */

const args = process.argv.slice(2);
const quick = args.includes('--quick');
const name = args.filter(a => !a.startsWith('--'))[0];

if (!name) {
  console.error('Usage: node scripts/archetype.js <creator-name> [--quick]');
  process.exit(1);
}

if (quick) {
  console.log(`
=== xhsfenxi archetype cheatsheet ===

TYPE A — 荒诞美学型 (Absurdist Aesthetics)
  Example: 荒诞美学博主（vlogger型）
  Signals:
  - Unified brand symbol/tag on every post (e.g. "（劲爆）")
  - Absurdist or philosophical topics treated earnestly
  - High-production video; literary title naming
  - Serious × absurd contrast in every piece
  Formula: 荒诞滤镜下的生活哲学

TYPE B — 共鸣命名型 (Resonance & Naming)
  Example: 成长世界观表达博主
  Signals:
  - Posts name vague emotional states or life stages
  - Private experience → universal proposition
  - Titles feel like thoughtful questions or redefinitions
  Formula: 经历 → 命题 → 命名 → 判断 → 共鸣

TYPE C — 现实策略型 (Reality & Strategy)
  Example: 普通女孩上行策略博主
  Signals:
  - Titles contain conflict words ("骗子", "不要脸", "装")
  - Content breaks unspoken workplace/relationship/money rules
  - Self-labels with perceived weakness to pre-empt criticism
  Formula: 困境 → 说破 → 规则 → 策略 → 爽感

MIXED B+C — Most powerful hybrid
  Combines: resonance/naming × reality/strategy
  = "You understand me" + "Now I know what to do"
`);
  process.exit(0);
}

console.log(`
=== xhsfenxi archetype classification: ${name} ===

TASK
Classify the Xiaohongshu account "${name}" into one of these three archetypes
(or a hybrid), based on visible public evidence.

─────────────────────────────────────────────
THREE ARCHETYPES
─────────────────────────────────────────────

TYPE A — 荒诞美学型 (Absurdist Aesthetics)
  Core: Wraps philosophical/serious content in absurdist humor + high visual quality
  Proven example: 荒诞美学vlogger型 (unified brand symbol; grand × mundane contrast; literary naming)
  Key signals to look for:
  - Does every post share a unified recurring symbol or phrase?
  - Do titles contrast a grand/serious setting with a mundane/absurd action?
  - Is the visual/production quality noticeably higher than peers?
  - Are serious topics treated with humor and humor treated earnestly?

TYPE B — 共鸣命名型 (Resonance & Naming)
  Core: Names vague emotions and life stages so users feel "finally, someone said it"
  Proven example: 成长世界观表达型 (youth growth, worldview expression, concept naming)
  Key signals to look for:
  - Do posts give names or definitions to emotional states most people can't articulate?
  - Does the account turn personal stories into universal life propositions?
  - Do titles feel like thoughtful philosophical questions or redefinitions?
  - Is the tone warm, perceptive, aesthetically refined?

TYPE C — 现实策略型 (Reality & Strategy)
  Core: Breaks unspoken real-world rules; provides executable strategies for ordinary people
  Proven example: 普通女孩上行策略型 (antifragile identity; rule-breaking; 普通人上行)
  Key signals to look for:
  - Do titles contain conflict words or counter-intuitive framing?
  - Does the account self-label with a perceived weakness to pre-empt criticism?
  - Does content expose hidden rules in workplace/relationships/money/consumption?
  - Does every piece end with a clear, actionable conclusion or stance?

MIXED HYBRID
  Some accounts combine two archetypes. Most powerful is B+C:
  "I understand your situation (Type B) AND here's what you can actually do (Type C)"

─────────────────────────────────────────────
CLASSIFICATION PROMPT
─────────────────────────────────────────────

Based on publicly visible data for "${name}", answer:

1. Which archetype does this account most closely match? (A / B / C / Mixed)
2. What are 2–3 concrete visible signals that support this classification?
3. If mixed: what percentage is each type, and does one dominate?
4. What is the single sentence that describes this account's core "filter" on the world?
5. Is there a brand symbol or signature phrase? If yes, what is it and how does it function?

Then proceed with the full analysis using this archetype as the lens.
`);
