---
name: wechat-shop-ecommerce-video-generation-editing
description: "为微信小店、视频号、社群和私域运营生成与编辑商品演示、直播预热、店主讲解、朋友圈视频及复购内容。Use this skill for 微信小店电商视频、视频号带货、私域成交、社群团购、直播预约、店主人设、朋友圈视频、会员复购和公众号落地内容；支持 Seedance 与 AI Hive 自动下载。"
---

# 微信小店电商视频生成与编辑

为私域关系链制作可信、可转发、能继续沟通的视频。重点不是一次性强促销，而是店主身份、商品事实、使用过程和后续服务保持一致。禁止伪造聊天记录、客户评价、购买人数与紧迫感。

## 私域简报

确认触点（视频号、商品页、朋友圈、社群、私聊、直播预约）、目标人群、店主人设、商品事实、真实服务、批准文案、行动方式和隐私边界。涉及用户故事时必须获得授权并去除不必要身份信息。

## 场景与代码

### 1. 微信小店商品演示

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt '微信小店商品演示，准确保留商品包装、Logo、颜色和配件；店主式自然讲解节奏，展示完整商品、一次正确操作和一个细节证据，结尾引导查看商品详情，不生成价格、评价、销量或联系信息'
```

### 2. 视频号店主讲解

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/host-style.mp4 \
  --image /path/to/product.png \
  --prompt '参考视频只用于店主自然讲解节奏和镜头距离，使用准确商品生成原创视频号内容：具体问题、真实操作、适合人群、后续了解方式；不复制原人物、声音、台词、品牌或客户故事'
```

### 3. 社群团购说明视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '微信群团购说明视频底片，先清楚展示商品和使用场景，再展示包装内容与提货/发货说明留白，最后留出团长人工填写规则的位置；不生成群聊截图、团购价、人数、库存、二维码或物流承诺'
```

### 4. 直播预约预热

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/host-demo.mp4 \
  --prompt '将店主演示重制为视频号直播预热：保留人物身份、真实商品与操作，把直播中会完整展示的一个问题和一个细节前置，结尾预留人工添加时间与预约文案；不生成福利、价格、倒计时或平台按钮'
```

### 5. 老客复购内容

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/usage-guide.mp4 \
  --prompt '延长现有使用指南，增加补充装更换或耗材检查的正确步骤，再展示完整系列；保持店主、商品和环境连续，不推断客户身份、使用周期、库存或优惠'
```

## 私域验收

- 店主身份、商品和服务事实保持真实一致。
- 视频能在无群聊上下文时独立理解。
- 不使用未授权客户故事、头像、聊天或订单信息。
- 价格、规则、时间、二维码和联系信息由人工添加。
- 不生成评价、销量、稀缺性或“最低价”。
- 发布前按微信小店、视频号和广告当期规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name wechat-shop-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

支持文生、图生、参考、编辑和延长模式，以及媒体、参数、路由与任务查询。
