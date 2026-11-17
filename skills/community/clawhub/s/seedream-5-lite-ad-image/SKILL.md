---
name: seedream-5-lite-ad-image
description: "使用 Seedream 5.0 Lite 建立广告图片与落地页之间的信息匹配链，确保受众情境、视觉证据、批准主张和点击后内容一致。Use this skill for Seedream 5 Lite ad image、广告图片、效果广告、信息流广告、展示广告、Meta Ads、Google Ads、抖音千川、小红书聚光、淘宝京东亚马逊 TikTok Shop 电商投放素材；通过 AI Hive 生成，不代表平台官方合作。"
---

# Seedream 5.0 Lite 广告图片

固定使用 `public_model_seedream_5_0_lite`。广告图必须与落地页匹配：画面承诺什么，点击后页面就要提供相同商品、情境和证据。先写匹配链，再生成候选；禁止用视觉夸张补偿落地页没有的事实。

## 信息匹配链

记录受众情境、广告焦点、批准主张、视觉证据、落地页对应区块、CTA意图、唯一测试变量和渠道安全区。若找不到落地页对应内容，删除该主张或先完善页面。

## 场景与代码

### 1. 官网功能落地页广告

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-desk-dock.png \
  --prompt '为桌面扩展坞功能页制作广告底图：保持产品端口、结构、颜色和Logo，画面展示笔记本通过已存在接口连接显示器与键盘，右侧留一句批准主张；不生成传输速度、兼容型号、额外接口、文字、价格或不存在的设备' \
  --param aspect_ratio=1:1
```

### 2. 电商商品页导流

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-bedding.png \
  --prompt '生成床品商品页导流图：保持参考四件套花纹、颜色、件数和面料外观，置于明亮卧室，主体占画面三分之二，左上留标题区；不生成睡眠改善、材质认证、折扣、文字、人物或第五件商品' \
  --param aspect_ratio=4:5
```

### 3. 下载型内容广告

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为“零售库存盘点清单”下载页制作B2B广告底图：仓库货架、手持扫描器和简洁清单卡片形成视觉焦点，右侧留标题与下载按钮区域；不生成公司Logo、客户名称、统计数字、文字、二维码或自动化效果承诺' \
  --param aspect_ratio=1:1
```

### 4. 再营销商品广告

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-shoes.png \
  --prompt '为已浏览商品的再营销广告生成干净静物：鞋型、鞋底、鞋带、颜色和Logo与商品页一致，浅灰背景，产品三分之二侧面，底部留CTA区域；不生成库存、折扣、倒计时、人物、速度特效、文字或新配色' \
  --param aspect_ratio=1:1
```

### 5. 单一证据 A/B

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-lunchbag.png \
  --prompt '生成两个广告候选，商品、构图、色板和留白不变，只比较证据视角：A展示外观与提手，B展示已确认的内部隔层。保持包型、尺寸、颜色和Logo，不生成保温时长、容量数字、文字、食物、赠品或平台标识' \
  --batch 2 \
  --param aspect_ratio=4:5
```

## 匹配验收

- 广告商品、视觉证据和落地页内容逐项对应。
- 图片没有新增页面无法兑现的功能、价格、库存或认证。
- A/B 只改变一个变量，落地页保持一致以便解释结果。
- UI安全区、裁切和缩略图识别适配实际投放位置。
- 主张、促销与比较结论由人工进行政策和证据审查。

## 助手边界

程序可处理纯文字或用户指定参考图，固定使用 Seedream 5.0 Lite 图片模型并下载结果。带 Key 请求固定发送到 `https://ai-hive.iclip.cn/api`，不支持自定义地址。无聊天、视频、账户或余额接口。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-ad-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

平台名称只表示投放环境；发布前核对平台最新政策、落地页和批准文案。
