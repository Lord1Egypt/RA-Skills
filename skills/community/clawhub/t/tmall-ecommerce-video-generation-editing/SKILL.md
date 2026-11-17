---
name: tmall-ecommerce-video-generation-editing
description: "为天猫旗舰店生成与编辑商品页视频、品牌故事、新品首发、详情演示、大促会场和会员内容。Use this skill for 天猫电商视频、旗舰店商品视频、详情页演示、品牌TVC、新品发布、超级品牌日、618双11素材、会员营销和天猫广告；支持 Seedance 多模式及 AI Hive 自动交付。"
---

# 天猫电商视频生成与编辑

把旗舰店品牌表达和商品购买证据组织成不同版本：商品页需要清楚演示，首页需要品牌节奏，新品首发需要核心创新，大促素材需要为批准机制留出空间。不能用一条 TVC 覆盖所有触点。

## 品牌与商品母版

收集品牌视觉、Logo 规则、商品与包装、真实卖点、批准台词、模特授权、活动主题、会员用途和禁止表达。活动价格、权益、机制和复杂中文在审核后的后期流程中加入。

## 场景与代码

### 1. 天猫商品页演示

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt '天猫旗舰店商品页视频，保持商品、包装、Logo、颜色和配件准确；先完整展示，再演示一个正确使用动作和一个材质细节，结尾回到品牌级商品全景，静音也能理解，不生成价格、功效、认证或活动信息'
```

### 2. 新品首发短片

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '天猫新品首发短片：从品牌生活场景切入，逐步揭示商品外观、一个已批准创新点和真实使用结果，节奏高级克制，结尾预留新品名称与上市信息区域；不生成首发价、销量、奖项或未提供技术'
```

### 3. 品牌首页 Hero 视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/brand-motion.mp4 \
  --image /path/to/product.png \
  --prompt '参考视频只用于品牌运动语言、转场柔度和节奏，使用准确商品生成原创天猫首页Hero；宽幅构图、无声可读、标题留白清楚，不复制参考产品、模特、台词、音乐或Campaign概念'
```

### 4. 大促会场底片

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/brand-master.mp4 \
  --prompt '将品牌母片重制为天猫大促会场底片：保留商品、模特与品牌事实，强化商品组合和节奏，在开场、机制与CTA位置留出干净区域；不生成双11标识、到手价、折扣、赠品、倒计时或销量'
```

### 5. 会员复购内容

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/product-use.mp4 \
  --prompt '从现有使用视频自然延长，增加主商品与补充装的正确关系、一次复购使用场景和系列全景；保持商品、人物与品牌连续，不生成会员身份、权益、优惠或使用周期数字'
```

## 旗舰店验收

- 商品页、首页、首发、大促和会员版各自承担不同任务。
- 品牌、商品、模特和包装在版本间一致。
- 卖点有真实动作或细节支持。
- 活动机制、价格、权益和复杂文字由人工审核添加。
- 不生成销量、奖项、认证、功效或平台标识。
- 发布前按天猫当前商品、活动和广告规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name tmall-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

使用 Seedance 2.5 的生成、参考、编辑与延长模式；按需传入素材、参数、路由、输出目录和仅提交选项。
