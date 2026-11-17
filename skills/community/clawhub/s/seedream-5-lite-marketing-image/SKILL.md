---
name: seedream-5-lite-marketing-image
description: "使用 Seedream 5.0 Lite 生成品牌 Campaign KV、广告创意、社交媒体、活动 Banner、邮件和落地页营销图片，并扩展多渠道版本。Use this skill for Seedream 5营销图片、广告图、品牌KV、信息流素材、社媒视觉、海报、Banner、Campaign、A/B测试和多尺寸适配；通过 AI Hive 生成和编辑。"
---

# Seedream 5.0 Lite 营销图片

从“一个受众、一个主张、一个行动”构建营销视觉，再扩展渠道版本。固定调用 `public_model_seedream_5_0_lite`。模型负责视觉和留白，批准文案、价格、活动机制与法律信息在后期排版。

## Campaign 简报

确认目标受众、传播阶段、单一主张、可证明证据、商品与品牌资产、情绪、渠道、版位、CTA 和禁止表达。A/B 版本应改变受众洞察或证据方式，而不是只换颜色。

## 场景与代码

### 1. Campaign 主 KV

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '品牌Campaign主KV，面向城市创作者，主张是“专注让创作更轻松”，准确商品位于右侧，真实工作场景与清晰光线，左侧大标题和证据留白，现代克制，不生成文案、价格、Logo和奖项' \
  --image /path/to/product.png \
  --image /path/to/brand-style.png
```

### 2. 三种创意假设

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为同一商品生成3个营销方向：具体痛点场景、使用动作证明、材质价值特写。商品与品牌系统一致，每版改变沟通理由和构图，为标题与CTA留白，不只换滤镜，不生成效果承诺' \
  --image /path/to/product.png \
  --batch 3
```

### 3. 社交渠道套版

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '将批准KV重新设计为方形Feed、竖版Story和横版Banner，保持商品、人物、品牌色和主张一致；每版根据裁切与界面安全区重新排布标题和CTA留白，不生成平台UI和旧文字' \
  --image /path/to/approved-kv.jpg \
  --batch 3
```

### 4. 活动视觉底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '季节活动视觉底图，准确商品组合与品牌色，建立有节奏的庆祝氛围，分别保留活动标题、机制和CTA区域；不生成活动Logo、折扣、价格、赠品、倒计时或销量' \
  --image /path/to/products.png
```

### 5. 邮件与落地页头图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '宽幅邮件/落地页Hero，商品与一个真实使用场景形成视觉焦点，左侧保留标题、证据与按钮区域，移动端裁切仍保留主体，加载感简洁，不生成文本、评分、价格或浏览器UI' \
  --image /path/to/product.png
```

## 营销验收

- 一个版本只服务一个受众主张与行动。
- A/B 方向改变洞察或证据，不制造伪变体。
- 商品、人物与品牌资产准确一致。
- 渠道版位经过重新构图，安全区和裁切合理。
- 文案、价格、活动机制和法律信息人工排版。
- 为每版记录受众、假设、渠道与用途。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-marketing-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持参考图、批量、实时模型参数、路由、输出目录与仅提交模式。
