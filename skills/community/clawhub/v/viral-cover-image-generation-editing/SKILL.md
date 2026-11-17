---
name: viral-cover-image-generation-editing
description: "使用 Nano Banana Pro 设计和编辑信息流封面，通过单一焦点、可兑现的信息缺口、短标题安全区和缩略图测试提高点击意愿，而不制造标题党。Use this skill for 爆款封面图片生成与编辑、viral cover、短视频封面、社媒封面、文章头图、播客封面、课程封面、小红书抖音快手视频号 B站 Instagram YouTube 内容封面；通过 AI Hive 生成，爆款不构成效果保证。"
---

# 爆款封面图片生成与编辑

固定使用 `public_model_nano_banana_pro`。封面只负责让目标用户理解“这条内容与我有关，而且点开后能得到什么”。建立可兑现的信息缺口：画面提出一个具体问题或结果线索，正文必须真正回答；不要用夸张表情、伪造数字和无关冲突骗取点击。

## 封面卡

记录目标读者、内容主题、点开后能获得的价值、唯一焦点、标题占位、不可剧透信息、不得暗示内容和缩略图尺寸。先生成无字底图，再用批准标题排版；只有极短文字允许在模型内尝试并逐字检查。

## 场景与代码

### 1. 知识短视频封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为“为什么会议越开越长”知识短视频生成4:5封面底图：中央是一张被不断拉长的会议桌，人物只用简化剪影，右上留八字以内标题区，蓝灰背景与一个橙色焦点；不生成文字、公司Logo、具体时长、愤怒表情或虚假结论' \
  --batch 3 \
  --param aspect_ratio=4:5
```

### 2. 小红书教程封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-desk-before.jpg \
  --prompt '基于授权桌面照片制作“桌面整理步骤”封面：保持真实桌面与物品，不伪造前后对比；用三个清晰区域提示分类、收纳、留白的内容结构，顶部留标题区，画面自然明亮，不生成文字、平台Logo、效率数字或不存在的收纳用品' \
  --param aspect_ratio=3:4
```

### 3. 播客单集封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为“独立开发者如何定价”播客单集生成方形封面底图：一台笔记本与三张不同高度的价格卡片构成焦点，深蓝与浅黄配色，左侧留单集标题区；不生成货币数字、真实公司、主播人像、文字或收益承诺' \
  --param aspect_ratio=1:1
```

### 4. B站测评封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-keyboard-a.png ./approved-keyboard-b.png \
  --prompt '为两款已授权键盘的真实对比视频制作16:9封面：左右各一款，外观、键位、Logo和颜色不变，中间留对比标题区，用光线区分而非胜负符号；不生成评分、价格、夸张爆炸、人物脸、文字或未测试结论' \
  --param aspect_ratio=16:9
```

### 5. 公众号文章同步封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为“社区小店如何做会员日”文章生成横版封面底图：店主整理会员卡片与商品陈列，场景真实克制，左侧留主标题和一句副标题区域，缩略图中人物与卡片关系仍清楚；不生成文字、销量数字、品牌、顾客脸或成功保证' \
  --param aspect_ratio=16:9
```

## 缩略图测试

- 将候选缩小到实际列表尺寸，三秒内能说出主题和焦点。
- 信息缺口与正文内容一致，不剧透全部，也不承诺正文没有的结果。
- A/B 只改变焦点、标题区或情绪中的一个变量。
- 人物、商品、数字和对比结论来自授权且可验证资料。
- 记录封面版本、标题版本、发布时间和真实表现，用数据迭代而非宣称必爆。

## 助手边界

脚本可从文字开始或上传用户指定图片，固定调用 Nano Banana Pro 图片模型并保存结果。认证请求仅发送到 `https://ai-hive.iclip.cn/api`，不接受自定义地址。无聊天、视频、账户或余额命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name viral-cover-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

“爆款”是创意目标而非保证；平台名称仅用于描述发布环境。
