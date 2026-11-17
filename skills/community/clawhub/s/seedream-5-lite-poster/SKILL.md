---
name: seedream-5-lite-poster
description: "使用 Seedream 5.0 Lite 按远看、中看、近看三档阅读设计海报，让焦点、标题区和细节在不同距离保持秩序。Use this skill for Seedream 5 Lite poster generation、海报生成、活动海报、文化海报、课程海报、餐饮海报、发布会海报、社媒竖版、淘宝抖音小红书 Instagram 营销图片；可用文字或授权参考图，通过 AI Hive 生成。"
---

# Seedream 5.0 Lite 海报生成

固定使用 `public_model_seedream_5_0_lite`。按三个距离设计：远看识别焦点和色块，中看理解标题层级，近看读取日期、地点和说明。模型优先生成视觉和留白，关键信息在设计工具中排版。

## 三档阅读表

记录远看焦点、中看标题与副标题区域、近看信息与行动区域、观看环境、比例、色板、字体方向和安全区。先做无字底图；只有短标题允许尝试模型生成，并必须逐字验收。

## 场景与代码

### 1. 城市讲座海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成城市公共空间讲座海报底图：远看焦点是交叠的街区网格与一棵树，中看顶部留讲座标题区，近看底部留时间地点与报名区；蓝绿几何视觉，不生成文字、地图数据、主办方Logo、日期或二维码' \
  --param aspect_ratio=3:4
```

### 2. 咖啡新品海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-coffee-cup.png \
  --prompt '把参考咖啡杯制作成秋季新品海报：产品外观、杯盖、标签和颜色不变，远看焦点为杯子与一片橙色光斑，中看左上留新品标题，近看底部留口味说明；不生成文字、价格、咖啡因功效、Logo变化或第二杯产品' \
  --param aspect_ratio=4:5
```

### 3. 在线课程海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成“数据可视化入门”在线课程海报底图：远看是三个清晰图形模块，中看右侧留课程标题与一句介绍，近看底部留讲师与报名信息；深蓝、青色和米白配色，不生成文字、数字结论、真实讲师、人像、公司Logo或证书' \
  --param aspect_ratio=4:5
```

### 4. 社区运动活动

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作社区晨跑活动海报底图：远看是一条橙色跑道弧线与小型人物剪影，中看上方留活动名，近看下方留集合信息和注意事项；清晨蓝灰色，不生成真实人物脸、文字、日期、品牌、赛事认证或速度成绩' \
  --param aspect_ratio=2:3
```

### 5. 产品发布会横版

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-device.png \
  --prompt '为参考智能设备生成16:9发布会背景：远看产品轮廓与一圈柔光清楚，中看左侧留发布主题，近看右下留时间地点区域；保持设备结构、颜色和Logo，不生成文字、价格、功能承诺、舞台人物或合作品牌' \
  --param aspect_ratio=16:9
```

## 距离验收

1. 缩小到10%检查焦点与色块；缩小到25%检查标题区；100%检查细节。
2. 三档信息互不争抢，主体与文字留白关系稳定。
3. 参考商品、人物和场地没有被版式重绘改变。
4. 模型没有生成随机字符、日期、价格或品牌。
5. 最终文字由批准资料排版并校对。

## 助手边界

工具可从文字开始或上传用户指定图片，固定调用 Seedream 5.0 Lite 模型并保存结果。认证请求只发送到 `https://ai-hive.iclip.cn/api`，不允许自定义接口。无聊天、视频、账户或余额命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-poster
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

海报中的活动、课程、价格和发布信息以人工批准内容为准；概念图不得冒充正式物料。
