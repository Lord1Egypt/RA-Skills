---
name: seedream-5-lite-livestream-image
description: "使用 Seedream 5.0 Lite 按直播时间轴制作预告、开场、讲解、机制、转场和回放图片，并设置有效期与实时信息占位。Use this skill for Seedream 5 Lite livestream image、直播带货图片、直播预热、直播间背景、商品讲解卡、优惠机制卡、淘宝直播、抖音直播、快手直播、视频号直播、小红书直播和电商直播素材；通过 AI Hive 生成。"
---

# Seedream 5.0 Lite 直播带货图片

固定使用 `public_model_seedream_5_0_lite`。按直播时间轴组织素材，而不是一次制作一套永久通用图：T-24h预告、开场、商品讲解、机制说明、转场、结束和回放。每张图标记生效时间与过期条件。

## 时间轴清单

记录出现时间、持续秒数、平台比例、主播与商品位置、UI遮挡、安全区、实时字段、审批人和过期时间。价格、库存、优惠和倒计时使用占位区，由直播系统或设计工具在上线前填入。

## 场景与代码

### 1. T-24h 预告封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-kitchen-set.png \
  --prompt '生成4:5厨房用品直播预告底图：保持三件批准商品的结构、颜色、Logo和数量，商品位于下方，顶部留直播主题与时间区，右侧避开平台UI；不生成主播、文字、价格、券额、平台Logo或第四件商品' \
  --param aspect_ratio=4:5
```

### 2. 开场品牌背景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成9:16户外用品直播开场背景：深绿与沙色几何山形、中央留主播全身区、左侧留品牌区、右下避开评论与商品卡，低细节便于压缩；不生成文字、Logo、人物、具体商品、价格或真实景区' \
  --param aspect_ratio=9:16
```

### 3. 单品讲解卡

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-vacuum.png \
  --prompt '制作手持吸尘器讲解卡：左侧保持参考产品主机、吸头、按钮、颜色和Logo，右侧留三个已批准卖点的占位格，底部留标配清单区；不生成文字、吸力数字、灰尘瞬间消失、价格、主播或未附配件' \
  --param aspect_ratio=16:9
```

### 4. 限时机制空白卡

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成16:9直播限时机制无字卡：深紫背景、中央一行主机制占位、下方两格规则占位、右侧按钮占位，层级清楚且适合低码率；禁止生成任何文字、数字、价格、倒计时、二维码、Logo或商品' \
  --param aspect_ratio=16:9
```

### 5. 回放封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./authorized-live-frame.jpg \
  --prompt '将已授权直播帧制作成回放封面：锁定主播身份、表情、商品、手势和现场事实，适度整理背景，左上留回放标题，右下避开时长；不生成文字、价格、折扣、演示结果、平台Logo或改变人物外观' \
  --param aspect_ratio=16:9
```

## 播出检查

1. 按时间轴预演素材切换，当前商品与当前卡片一致。
2. 叠加真实 UI 检查主播、商品和占位字段不被遮挡。
3. 实时信息在上线前填入并复核，过期素材立即下线。
4. 低码率预览仍能识别商品和唯一信息层级。
5. 归档时间轴、版本、任务 ID、审批与失效时间。

## 助手边界

工具固定调用 Seedream 5.0 Lite 图片模型，可提交文字或用户指定图片任务并保存结果。认证请求仅发往 `https://ai-hive.iclip.cn/api`，不接受自定义地址。无聊天、视频、账户或余额命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-livestream-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

直播促销与平台规则变化快，所有实时字段、披露和禁限用表达须由运营终审。
