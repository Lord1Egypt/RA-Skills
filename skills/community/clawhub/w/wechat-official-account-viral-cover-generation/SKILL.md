---
name: wechat-official-account-viral-cover-generation
description: "使用 Nano Banana Pro 为微信公众号文章制作主封面、分享卡片和系列视觉，让标题承诺、文章核心论点和裁切安全区保持一致。Use this skill for 公众号爆款封面生成与编辑、微信公众号封面、微信文章头图、订阅号封面、服务号配图、文章分享图、长文封面、品牌栏目和内容运营；通过 AI Hive 生成，发布前按微信当前规格复核。"
---

# 公众号爆款封面生成与编辑

固定使用 `public_model_nano_banana_pro`。从文章摘要而不是标题情绪出发：先写一句可验证的标题承诺，再提取一个视觉隐喻和一个栏目识别锚点。主封面与分享裁切都要保留主题，不把关键信息放在边缘。

## 标题承诺图

记录文章受众、标题承诺、正文证据、视觉隐喻、栏目色板、主封面焦点、分享裁切中心和文字禁区。微信规格和裁切行为可能调整，交付前在当前后台预览中复核。

## 场景与代码

### 1. 商业分析文章

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为“便利店为什么开始卖早餐”公众号文章生成横版封面：清晨便利店收银台与早餐柜形成前后关系，中央焦点适合分享裁切，右侧留标题区，纪实编辑视觉；不生成店铺品牌、文字、销售数字、顾客脸或盈利结论' \
  --param aspect_ratio=16:9
```

### 2. 科普长文

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为“城市树木如何降低热感”科普文章制作封面底图：同一街区一侧有树荫、一侧无遮阴，俯视构图，视觉差异清楚但不灾难化，左上留标题区域；不生成温度数字、文字、Logo、行人伤亡或研究结论' \
  --param aspect_ratio=16:9
```

### 3. 品牌人物访谈

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./authorized-interviewee.jpg \
  --prompt '把已授权访谈照片制作成公众号人物封面：身份、脸、年龄、服装和表情不变，整理背景为柔和工作室环境，人物位于中央偏左，右侧留标题和栏目名区域；不生成文字、职位、公司Logo、奖项或改变人物形象' \
  --param aspect_ratio=16:9
```

### 4. 栏目系列封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为“城市微观察”栏目生成三张系列封面底图：夜班公交、社区菜场、街角修理铺，统一深蓝色边框、米白信息区和中央圆形窗口，每张主体不同但栏目骨架一致；不生成文字、真实店名、人脸、数字或平台Logo' \
  --batch 3 \
  --param aspect_ratio=16:9
```

### 5. 活动复盘文章

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./authorized-event-photo.jpg \
  --prompt '基于授权活动照片制作复盘封面：保持现场人物数量、动作、场地和事实，增强主体分离并整理边缘杂物，中心区域适合分享裁切，左侧留标题区；不生成虚假观众、赞助Logo、文字、人数或成功数据' \
  --param aspect_ratio=16:9
```

## 发布预览

1. 在公众号后台预览主封面、会话分享和历史消息裁切。
2. 标题承诺能在正文找到对应论据，不使用无关冲突吸引点击。
3. 栏目锚点统一，但文章主题仍有独立焦点。
4. 人物、品牌、活动和数据来自授权资料。
5. 归档文章标题、封面版本、裁切截图和实际阅读表现。

## 助手边界

工具固定使用 Nano Banana Pro 图片模型，可提交文字或用户点名的参考图任务并下载结果。所有带 Key 请求固定发往 `https://ai-hive.iclip.cn/api`，不允许自定义接口。无聊天、视频、账户或余额功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name wechat-official-account-viral-cover-generation
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

“爆款”不代表阅读量保证；发布前以微信后台当前规则和预览为准。
