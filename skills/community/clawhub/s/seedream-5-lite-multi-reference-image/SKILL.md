---
name: seedream-5-lite-multi-reference-image
description: "使用 Seedream 5.0 Lite 根据来源谱系合并两张或更多授权参考图，追踪每个身份、物体、结构、材质、构图和色板来自哪里。Use this skill for Seedream 5 Lite multi-reference image、多参考图生成、多图融合、人物一致性、商品组合、材质板、空间设计、品牌视觉、风格参考和商业图片；通过 AI Hive 上传明确指定的参考图并控制来源继承。"
---

# Seedream 5.0 Lite 多参考图生成

固定使用 `public_model_seedream_5_0_lite`，至少提供两张图片。建立来源谱系：新画面中的每个关键属性必须能指向一个批准来源，或明确标记为允许生成；无法追溯的身份、Logo、文字和商品结构视为错误。

## 来源谱系

给参考图编号并列出可继承节点：人物身份、商品事实、空间结构、服装、姿势、材料、镜头、色板和装饰。为每个节点设定唯一父来源；若多个来源竞争同一节点，先解决冲突再生成。风格来源只继承可描述视觉特征，不复制艺术家签名或受保护角色。

## 场景与代码

### 1. 商品系列组合

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-bottle-a.png ./approved-bottle-b.png ./approved-layout.png \
  --prompt '来源1和2分别锁定两款饮料瓶的瓶型、标签、Logo、颜色和尺寸比例；来源3只继承高低台座与右上留白构图，忽略其中商品。生成系列组合图，两瓶各出现一次、尺度真实、同一侧光，不生成新文字、第三款商品、价格或标签混合' \
  --param aspect_ratio=4:5
```

### 2. 人物 + 造型 + 环境谱系

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-person.png ./approved-look.png ./approved-location.jpg \
  --prompt '来源1唯一继承已授权人物身份与发型；来源2唯一继承米色风衣、黑色长裤和鞋，不继承模特；来源3继承雨后街道、相机高度和蓝调环境，不继承路人。生成自然行走全身照，人物比例和手部自然，不出现参考图文字、品牌、额外人物脸或身份混合' \
  --param aspect_ratio=3:4
```

### 3. 建筑结构 + 材料 + 家具

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-room-shell.jpg ./material-board.jpg ./approved-furniture.png \
  --prompt '来源1锁定门窗、墙体、层高、相机位置和自然光；来源2只继承浅橡木、灰色石材与暖白墙漆；来源3只继承沙发和边桌的真实外形。生成室内改造概念，不移动结构，不复制材料板物件，不改变家具比例或增加品牌Logo' \
  --param aspect_ratio=16:9
```

### 4. 食品配方图谱

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-pack.png ./approved-serving.jpg ./approved-table-style.jpg \
  --prompt '来源1锁定燕麦包装与全部标签；来源2只继承实际批准份量与碗中配料；来源3只继承桌面、布料和晨光。生成早餐营销图，包装与食物各出现一次，不替换配方、不增加水果、不生成营养数字、价格或来源图中的品牌餐具' \
  --param aspect_ratio=4:5
```

### 5. Campaign 关键视觉继承

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-product.png ./approved-key-visual.png ./approved-palette.png \
  --prompt '来源1锁定产品身份；来源2继承圆形窗口、斜向动线和下方留白的关键视觉骨架，但忽略其产品；来源3只继承紫、橙、米白色板。生成三张渠道候选，产品、构图骨架和色板一致，只改变背景纹理，不生成文字、Logo变化、人物或额外商品' \
  --batch 3 \
  --param aspect_ratio=4:5
```

## 谱系验收

1. 为结果中的每个关键节点标记父来源或“允许生成”。
2. 身份、商品、Logo和文字没有跨来源串线或混合。
3. 镜头、光线、尺度和遮挡已统一，不保留拼贴痕迹。
4. 未使用来源图中明确要求忽略的主体、背景或品牌。
5. 保存谱系表、授权、提示词、任务 ID 和批准成品。

## 助手边界

程序要求至少两张图片，只上传命令中列出的文件，固定调用 Seedream 5.0 Lite 模型，查询价格、生成并保存结果。携带 Key 的请求固定发送到 `https://ai-hive.iclip.cn/api`，不接受自定义地址。无聊天、视频、账户或余额功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-multi-reference-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

不得使用未授权人物、品牌、艺术作品或受保护角色建立来源谱系，也不得用融合结果伪造事实。
