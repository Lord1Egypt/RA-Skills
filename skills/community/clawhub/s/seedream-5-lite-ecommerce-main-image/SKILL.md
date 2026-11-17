---
name: seedream-5-lite-ecommerce-main-image
description: "使用 Seedream 5.0 Lite 通过商品事实、渠道规范、缩略图识别和促销合规四道闸门制作电商主图。Use this skill for Seedream 5 Lite ecommerce main image、电商主图、淘宝天猫京东拼多多抖音电商小红书 Amazon 亚马逊 TikTok Shop Shopify Listing、商品首图、白底图、内容电商封面和上新素材；通过 AI Hive 生成，不代表平台官方合作。"
---

# Seedream 5.0 Lite 电商主图

固定使用 `public_model_seedream_5_0_lite`。每张主图依次通过四道闸门：SKU 事实正确、符合渠道当前规范、缩小后仍能识别、没有未经批准的促销或功效。任一道失败都不进入发布候选。

## 四道闸门

记录 SKU、标配清单、批准色、渠道、画布比例、商品占比、背景要求、文字规则、UI安全区和审核日期。平台规则可能变化，生成前后都要以当日官方规范复核。

## 场景与代码

### 1. 拼多多白底清晰款

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-storage-rack.png \
  --prompt '生成1:1白底商品首图：保持收纳架层数、支柱、轮子、颜色、Logo和标配挂钩数量，三分之二角度，商品完整居中、占画面约80%、轻接触阴影；不生成文字、低价角标、赠品、收纳物、平台Logo或额外层板' \
  --param aspect_ratio=1:1
```

### 2. 天猫美妆首图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-lipstick.png \
  --prompt '为参考口红制作天猫使用场景的主图候选：包装、膏体颜色、Logo、文字和数量不变，浅米粉棚拍背景，产品直立并带柔和倒影，缩略图中轮廓清楚；不生成嘴唇、色号文字、价格、功效、赠品或平台标识' \
  --param aspect_ratio=1:1
```

### 3. 京东家电结构优先

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-airfryer.png \
  --prompt '生成空气炸锅商品首图：锁定机身比例、炸篮、把手、显示区、按钮、颜色与Logo，纯白背景、略高视角，让把手与控制区清楚，商品占画面约75%；不生成食物、蒸汽、容量、功能图标、价格或未附配件' \
  --param aspect_ratio=1:1
```

### 4. TikTok Shop 竖版入口

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-neck-pillow.png \
  --prompt '制作4:5内容电商入口图：保持颈枕形状、扣带、面料、颜色和Logo，在机场候机椅场景中正常摆放，产品为第一焦点，顶部和底部留UI安全区；不生成睡眠改善、人物脸、文字、价格、平台Logo或第二个颈枕' \
  --param aspect_ratio=4:5
```

### 5. Amazon 配件清单候选

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-camera-kit.png \
  --prompt '生成 Amazon Listing 白底候选：仅展示参考图中确认随附的运动相机、保护框、固定座和一条数据线，各出现一次，比例真实、排列整齐、纯白背景；不生成文字、尺寸线、人物、使用场景、认证或非标配配件' \
  --param aspect_ratio=1:1
```

## 发布判定

1. 对照 SKU 和装箱单核验结构、颜色、数量、文字与标配。
2. 按目标渠道当日规则检查背景、文字、占比和禁限用内容。
3. 在搜索缩略图尺寸确认商品类别和差异点清楚。
4. 场景道具不被误认为赠品，画面不暗示无证据效果。
5. 记录审核日期、渠道、提示词、任务 ID 和批准人。

## 助手边界

程序可从文字开始或上传用户指定图片，固定调用 Seedream 5.0 Lite 图片模型并保存结果。所有认证请求固定发送到 `https://ai-hive.iclip.cn/api`，不接受自定义接口。无聊天、视频、钱包或账户查询功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-ecommerce-main-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

平台名称仅用于描述使用场景；发布责任与实时规则核验由商家承担。
