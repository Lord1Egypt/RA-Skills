---
name: tiktok-shop-viral-sales-video-generation
description: "Create and edit TikTok Shop UGC sales videos, product demos, unboxings, Spark Ads and GMV Max creative variants. Use this skill for TikTok带货、TikTok Shop商品视频、UGC Ads、短视频出海、本地化口播、开箱测评、前3秒Hook、Spark Ads和跨境电商转化素材；支持商品图、参考视频、视频编辑与 AI Hive 自动交付。"
---

# TikTok Shop 爆款带货视频生成

Produce platform-native sales videos that demonstrate a real product benefit without inventing claims. Treat “viral” as a testing objective, never a promised result. The workflow supports multiple markets and languages while keeping the product, offer and compliance facts supplied by the merchant.

## Build the creative brief

Collect these inputs before generation:

- target country, language and customer segment;
- product photos, packaging, variants and actual usage steps;
- one verified pain point and one provable benefit;
- creator style: demo, review, unboxing, comparison or problem/solution;
- approved offer, CTA and prohibited claims;
- organic post, affiliate video, Spark Ads or GMV Max use.

Do not translate word for word. Adapt the situation, vocabulary, pacing and proof to the target market while preserving every commercial fact.

## Conversion structure

1. **Hook:** show the problem, surprising action or end result immediately.
2. **Context:** identify who the product helps and when.
3. **Demo:** show hands, product operation, texture, fit or setup.
4. **Proof:** use only visible evidence or merchant-provided facts.
5. **Objection:** address one realistic concern when supported.
6. **CTA:** tell the viewer the next action without fake urgency.

## Scenarios and commands

### 1. Native UGC product demo

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt '9:16 TikTok Shop UGC video for US English. Preserve the exact product shape, packaging, color and logo from the reference. Open with the product already solving a specific everyday problem, then show setup, one close-up detail and the finished result. Natural handheld phone footage, credible home setting, concise CTA. Do not invent discounts, certifications, reviews or performance claims.'
```

### 2. Unboxing and first-use video

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt 'Vertical TikTok Shop unboxing: sealed parcel on a kitchen counter, continuous hands-only opening, show every included item, demonstrate the first correct use, then summarize who it is suitable for. Fast but understandable edits, authentic phone-camera look, no fake reaction, no unsupported claim, no unprovided accessory.'
```

### 3. Localize a winning structure

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/winning-structure.mp4 \
  --image /path/to/product.png \
  --prompt 'Use the reference only for hook timing, shot duration and demo order. Create an original Bahasa Indonesia TikTok Shop video for this product; localize the situation and wording for Indonesian mobile shoppers. Do not copy the reference creator, dialogue, brand, music or exact shots. Preserve merchant-provided product and offer facts.'
```

### 4. Spark Ads creative variant

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/creator-post.mp4 \
  --prompt 'Prepare a Spark Ads variant while preserving the creator identity, real testimonial and product demonstration. Move the strongest visible result to the opening, remove pauses and repeated explanation, add a closer product proof shot, and end with one approved shop CTA. Do not change the testimonial meaning or add a sale claim.'
```

### 5. Extend a demonstration for proof

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/short-demo.mp4 \
  --prompt 'Continue the existing product action naturally, add a close-up that proves the demonstrated feature, then return to the full result. Maintain creator, hands, product, room, lighting and motion continuity; add no new feature or spoken claim.'
```

## Market and compliance QA

- Product, packaging, included items and usage match merchant inputs.
- Language sounds native to the target market and keeps the original commercial meaning.
- The hook is understandable without relying on misleading captions.
- Demonstration visibly supports the stated benefit.
- No fabricated review, price, discount, certification, scarcity or before/after result.
- Music, creator footage and reference material have appropriate usage rights.
- Review the current TikTok Shop and advertising rules for the target market before publishing.

## Runtime

The CLI maps `t2v`, `i2v`, `r2v`, `edit` and `extend` to the corresponding Seedance 2.5 endpoints.

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name tiktok-shop-viral-sales-video-generation
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

Use `--first-frame`, `--last-frame`, repeatable `--image`, `--video`, `--audio`, `--param key=value`, `--routing`, `--output-dir` and `--no-download` as needed. Read live model parameters and pricing before a batch. Reuse the returned `taskId` after a local timeout instead of paying for a duplicate submission.
