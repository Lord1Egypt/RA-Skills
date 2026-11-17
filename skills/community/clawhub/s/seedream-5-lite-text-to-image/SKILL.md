---
name: seedream-5-lite-text-to-image
description: "使用 Seedream 5.0 Lite 从纯文字建立视觉实验卡，快速比较构图、叙事、媒介、色板和渠道比例，再收敛为可交付图片。Use this skill for Seedream 5 Lite text-to-image、文生图、文字生成图片、AI绘画、编辑插画、概念设计、教育图解、建筑氛围、海报底图、社媒创意、广告提案和 AIGC 图片；通过 AI Hive 生成，不读取参考图。"
---

# Seedream 5.0 Lite 文生图

固定使用 `public_model_seedream_5_0_lite`，不接受参考图片。把每次生成当作一个视觉实验：只测试一个明确假设，并定义什么结果算成功。探索轮比较方向，收敛轮锁定主体与构图，交付轮再处理比例和留白。

## 视觉实验卡

写明用途、受众、核心信息、主体与动作、环境、镜头、媒介、色板、留白、比例、必须出现、禁止出现、此次唯一变量和选择标准。不要把“高级、震撼、有氛围”当作可验证目标。

## 场景与代码

### 1. 编辑文章概念插画

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为“远程工作如何重塑小城市”文章生成横版编辑插画：一条铁路连接城市公寓与小镇共享办公空间，人物在两端使用电脑协作；克制的纸张拼贴风格，蓝灰与暖橙色，右侧留标题区，不生成文字、公司Logo、地图边界或统计数字' \
  --param aspect_ratio=16:9
```

### 2. 虚构包装方向探索

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为虚构燕麦饮品牌探索三种包装静物方向：A天然纸感，B清爽几何，C温暖早餐叙事。每版都是同一无品牌白色利乐包轮廓，只比较图形语言、色板和道具，不生成品牌名、文字、营养数据、认证或真实公司标识' \
  --batch 3 \
  --param aspect_ratio=4:5
```

### 3. 教育步骤底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作“雨水如何进入地下”教育图解底图：从左到右展示降雨、植被截留、土壤渗透、地下蓄水四个清晰阶段，儿童科普扁平插画，阶段之间留箭头与标签空位；不生成文字、数字、第五阶段、城市污染或灾害画面' \
  --param aspect_ratio=16:9
```

### 4. 建筑氛围概念

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成海边社区图书馆的早期氛围概念：低矮体量围合避风庭院，木格栅、浅色石材、可见海平线，阴天柔光，行人仅用于尺度；这是概念视觉而非建成照片，不生成项目名、建筑师、结构图、施工细节或真实地标' \
  --param aspect_ratio=16:9
```

### 5. 社媒系列试验

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为“每天十分钟整理”生成三张4:5社媒底图：桌面、衣柜、手机相册三个主题，统一米白背景、蓝色网格和单一黄色焦点物；每张顶部留短标题区，不生成文字、品牌、人物脸、前后对比承诺或平台Logo' \
  --batch 3 \
  --param aspect_ratio=4:5
```

## 实验记录

1. 每轮只改变实验卡中的一个变量，避免无法解释选择原因。
2. 核对主体、动作、数量、空间关系和信息层级。
3. 检查相机、透视、光线、材质和媒介形成同一视觉逻辑。
4. 留白与比例适配真实渠道，生成图不自行添加事实或品牌。
5. 保存实验卡、提示词、任务 ID、淘汰原因和批准方向。

## 助手边界

助手只查询固定 Seedream 5.0 Lite 图片模型与当次路由价格，提交纯文字图片任务、轮询并下载结果；文生图命令不读取或上传本地文件。所有携带 Key 的请求固定发往 `https://ai-hive.iclip.cn/api`，不接受自定义地址。无聊天、视频、账户或余额命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-text-to-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

概念商品、建筑和新闻类画面应清楚标注为 AI 生成或概念，不冒充真实事实。
