---
name: seedream-5-lite-character-consistency
description: "使用 Seedream 5.0 Lite 建立角色连续性圣经和镜头变更单，在多场景、表情、动作、服装和渠道版本中保持身份与品牌边界。Use this skill for Seedream 5 Lite character consistency、角色一致性、人物一致性、品牌 IP、吉祥物、虚拟人、绘本角色、漫画人物、短剧分镜、表情包、社媒系列和商业角色图片；通过 AI Hive 使用授权角色参考图生成。"
---

# Seedream 5.0 Lite 角色一致性图片

固定使用 `public_model_seedream_5_0_lite`，必须提供角色参考图。先建立角色连续性圣经，再为每张图写镜头变更单；角色圣经定义不可变身份，变更单只允许本镜头需要的动作、表情、服装或环境变化。

## 连续性圣经

记录脸型与五官比例、年龄表现、肤色、发型、体型、轮廓、主色、基础服装、标志物、比例表、允许表情、允许动作、换装规则、禁用场景和授权范围。品牌吉祥物还需记录线条、材质、色值和Logo使用方式。

## 场景与代码

### 1. 人物三视角基准

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-character-front.png \
  --prompt '基于已授权角色生成正面、左三分之二侧面和右侧面三张基准图：脸型、五官比例、肤色、年龄、发型、体型、白衬衫与蓝夹克完全一致，中性灰背景、同一焦距和光线；不改变身份、不添加配饰、文字或第二个人物' \
  --batch 3 \
  --param aspect_ratio=3:4
```

### 2. 表情范围表

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-character-sheet.png \
  --prompt '生成角色批准表情范围：平静、轻微微笑、专注、温和惊讶四种，每张保持脸部骨骼、眼睛形状、鼻子、发型、年龄、服装和镜头一致，表情幅度自然；不生成夸张变形、哭泣、愤怒、文字或额外角色' \
  --batch 4
```

### 3. 场景变更单

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-character-full.png \
  --prompt '镜头变更单：角色从摄影棚移到清晨书店，允许动作变为右手取书、表情轻微专注，基础服装与标志手表不变；身份、脸、发型、身高比例和主色锁定，不生成书店Logo、文字、敏感内容或其他清晰人物' \
  --param aspect_ratio=4:5
```

### 4. 品牌吉祥物动作组

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-mascot.png \
  --prompt '为品牌吉祥物生成挥手、指向左侧、抱礼盒三种动作：轮廓、头身比、眼睛、主蓝色、黄色围巾、线条粗细和材质完全一致，纯色背景；不改变Logo位置、不增加手指、不生成文字、节日标识或第二角色' \
  --batch 3 \
  --param aspect_ratio=1:1
```

### 5. 连续分镜镜头

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-character-full.png \
  --prompt '生成三格连续分镜：同一角色进入咖啡店、坐下打开笔记本、抬头看向窗外。三格保持身份、发型、夹克、手表、身材、色板和时间连续，动作衔接自然；不改变座位方向、不添加品牌文字、角色复制或突然换装' \
  --batch 3 \
  --param aspect_ratio=16:9
```

## 连续性验收

1. 与角色圣经逐项核对身份、轮廓、颜色、服装和标志物。
2. 变更只发生在镜头变更单允许的项目。
3. 批量图的镜头、时间、左右方向和道具状态连续。
4. 手、五官、年龄和身体比例没有逐帧漂移。
5. 保存角色圣经、变更单、参考图、任务 ID 和批准镜头。

## 助手边界

工具必须接收角色参考图，只上传命令中指定文件，固定调用 Seedream 5.0 Lite 图片模型并保存结果。认证请求仅发往 `https://ai-hive.iclip.cn/api`，不支持自定义地址。无聊天、视频、账户或余额命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-character-consistency
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

真实人物必须有明确授权；不得将角色用于未经批准的敏感、误导、代言或侵权情境。
