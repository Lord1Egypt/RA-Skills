---
name: ssai-dailymoments
description: 松鼠Ai自习室·每日朋友圈运营助手。触发方式：用户说"朋友圈"时自动调用，自动生成5条不同朋友圈文案+手绘风格插画，图片以文件形式发送。支持定时推送（每日08:00/11:00/12:30/15:30/19:30），也可随时手动触发。
version: 1.3.0
trigger: 手动触发（用户发送"朋友圈"或"发朋友圈"）+ 定时任务（Cron）
---

# ssai-dailymoments（松鼠Ai自习室·每日朋友圈运营Skill）

## 一、Skill基础信息

- **Skill ID / 英文名**：ssai-dailymoments
- **中文名**：松鼠Ai自习室·每日朋友圈运营助手
- **版本**：1.3.0
- **适用平台**：OpenClaw、Clawhub
- **触发类型**：手动触发 + 定时任务（Cron）
- **核心定位**：面向中小学生家长，生成温和真诚、不鸡血、不硬广、无专业术语的朋友圈内容，搭配温馨诗意插画

## 二、触发方式

### 手动触发（用户主动）
- **触发词**：用户发送"朋友圈"或"发朋友圈"
- **执行内容**：一次性生成5条文案 + 5张对应插画
- **防重复**：每次触发前读取 `~/.openclaw/skills/ssai-dailymoments/history.json`，确保5条内容与历史所有内容完全不重复

### 定时触发（Cron）
- 08:00 → 第1条（教育观念）
- 11:00 → 第2条（拒绝内卷）
- 12:30 → 第3条（学习痛点）
- 15:30 → 第4条（温和招生）
- 19:30 → 第5条（生活感悟）

## 三、内容要求

### ⚠️ 核心防重复机制（版本1.3.0重点更新）

**原则：每天的5条内容必须全部唯一，历史永不重复**

- 维护 `history.json`，**记录所有历史内容**（不设3天限制）
- 每次生成前：读取完整历史，比对确保新5条与历史所有内容完全不重复
- 比对维度：文案主题方向、文案关键词、核心观点——三者均不能与历史完全雷同
- 图片：每次使用不同的seed，确保画面元素与历史图片有明显差异
- **如果某方向与历史雷同，自动跳过该方向，替换为新方向**
- **如果所有方向都与历史重复，生成全新的创意方向（家庭关系、专注力、时间管理、阅读兴趣等）**

### 语言风格
- 温和真诚、接地气、不鸡血、不广告
- 不说专业术语（MCM、打地基、AI系统、知识图谱、督学师等）
- 每条80～160字，结尾带简约温暖表情（🌿、🌟、📖、📍、☕️）

### 5条方向池（每次随机选择5个方向，避免固定排期）

**核心方向池：**
1. 教育观念 — 成长节奏、花期、耐心陪伴
2. 拒绝内卷·培养自信 — 不比分数比进步
3. 学习痛点真相 — 基础漏洞、概念吃透
4. 温和招生 — 提供解决方案不推销
5. 生活感悟 — 温暖治愈、亲子日常
6. 学习习惯 — 错题整理、作业节奏
7. 考试心态 — 平常心、减少焦虑传染
8. 亲子沟通 — 愿意说实话比成绩重要
9. 亲子关系 — 叛逆期、退一步留条路
10. 周末生活 — 大自然是黏合剂
11. 家长会 — 状态、相处、参与度
12. 电子产品 — 成就感比没收手机管用
13. 自我设限 — 觉得自己不行比真的不行更难破
14. 学习方法 — 授人以鱼不如授人以渔
15. 小目标 — 每日小成就积累自信心

**扩展方向池（核心方向与历史重复时启用）：**
16. 专注力培养 — 一次只做一件事
17. 时间管理 — 番茄钟、四象限
18. 阅读兴趣 — 故事比作文书有趣
19. 考试复盘 — 失分点比得分点重要
20. 睡眠与学习 — 睡不好学不好
21. 主动学习 — 问问题比回答问题重要
22. 试错心态 — 错题是最好老师
23. 家长情绪 — 焦虑会传染给孩子
24. 学习环境 — 安静桌面、集中注意力
25. 目标拆分 — 大目标拆成小步骤

## 四、图片生成规则

### ⚠️ 重要：必须使用 Python 脚本调用 MiniMax API
**内置 `image_generate` 工具使用的不是用户提供的 API Key**，必须通过 Python 脚本调用 MiniMax 原生 API。

### API配置（用户需自行填写）
- **API Key**：`请填入你的 MiniMax API Key`
- **接口地址**：https://api.minimaxi.com/v1/image_generation
- **模型**：image-01
- **宽高比**：3:4（竖版，适配朋友圈）
- **response_format**：base64（避免URL失效问题）
- **n**：1（每条文案单独生成1张图）

> ⚠️ 若使用其他生图服务（如 Midjourney、Stable Diffusion 等），请替换接口地址、模型名和请求体格式，并确保 API Key 有效。

### Python 脚本生成流程
```
1. 使用 python3 调用 requests 库
2. 构造请求头：Authorization: Bearer <API_KEY>
3. 请求体：model, prompt, aspect_ratio, response_format, n, seed
4. 解析返回的 base64 数据
5. 保存为 .jpg 文件到 workspace 目录
6. 图片以文件路径形式返回给用户
```

### 风格要求
- 手绘插画风格，线条柔和
- 配色温暖舒适（莫兰迪或马卡龙色系）
- 画面元素贴近教育场景（书桌、灯光、亲子互动等）
- 避免过于商业化或写实的图片
- **图片比例**：竖版 3:4（750x1000px）
- **禁止元素**：文字、水印、边框、贴纸、花字、条漫格式

### 构图要求
- 竖版 3:4（750x1000 或等比）
- 主体元素居中偏下
- 背景为浅米色宣纸纹理
- 单图仅包含1-2个核心简约元素（小树、云朵、书本、笑脸、热饮、窗台等）
- 无文字、无水印、无边框

### 输出规则
- **图片以文件形式发送**，直接展示在对话中
- 不输出网络链接、不输出本地路径、不返回URL、不Base64
- 可直接长按保存、转发、发朋友圈

## 五、输出格式

输出仅包含：
- 文案（纯文本）+ 对应图片文件
- 无标题、无解释、无多余内容

## 六、容错机制

- 触发重试：失败后30分钟内自动重试
- 文案重生成：不符合要求则自动重新生成
- 图片重试：失败自动重试2次，仍失败则发送文案并提示"图片生成中"
- 历史保留：所有历史记录永久保留，不覆盖

## 七、MiniMax API 请求示例（Python）

```python
import requests
import base64

api_key = "请填入你的 API Key"
url = "https://api.minimaxi.com/v1/image_generation"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

data = {
    "model": "image-01",
    "prompt": "watercolor style, a cute girl reading a book in a park, warm colors, simple, no text, light cream paper texture, vertical 3:4 ratio",
    "aspect_ratio": "3:4",
    "response_format": "base64",
    "n": 1,
    "seed": 1001
}

resp = requests.post(url, headers=headers, json=data, timeout=30)
result = resp.json()

if result["base_resp"]["status_code"] == 0:
    img_base64 = result["data"]["image_base64"][0]
    img_bytes = base64.b64decode(img_base64)
    with open("output.jpg", "wb") as f:
        f.write(img_bytes)
    print("Image saved!")
else:
    print(f"Error: {result}")
```

## 八、Prompt 模板（核心方向池）

**风格统一前缀（每个Prompt必须以此开头，不得删除或修改）：**
> `Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio`

1. **教育观念**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A little girl sitting on a park bench reading a book, her parents watching her warmly, warm sunset light, small trees in distance, cozy and loving atmosphere`
2. **培养自信**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A little boy proudly holding a perfect score test paper, smiling big, eyes shining, cozy children room background with bookshelf and plants, warm colors, cute and lively`
3. **学习习惯**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A little boy doing homework at a desk, a cup of hot chocolate on the corner, warm night lamp light through window, cozy and warm scene, cream and brown tones, simple rounded lines`
4. **温和招生**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A cozy children study corner with a small desk, a desk lamp, a small potted plant and some children books, warm yellow light, warm orange white and light green tones, simple and warm design`
5. **生活感悟**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A small wooden table by the window with a cup of hot cocoa, a small succulent plant beside it, soft warm light from window, simple and cozy, warm cream and light brown tones, rounded brushstrokes, warm healing atmosphere`
6. **考试心态**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A calm parent and child taking a deep breath together before an exam, holding hands gently, warm exam hall background with soft light, reassuring and peaceful atmosphere, soft warm colors, simple rounded shapes`
7. **亲子关系**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A teenage child sitting at table looking at parent, a gentle conversation happening, warm home kitchen background, soft sunlight, caring atmosphere, soft blue and cream tones, simple rounded shapes`
8. **周末生活**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A family walking in a sunny park on weekend, child holding parent's hands, green grass and soft clouds, warm golden sunlight, relaxed and happy, soft green and warm yellow tones, simple rounded shapes, healing nature atmosphere`
9. **家长会**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A warm parent attending a school meeting with teacher, friendly conversation, school hallway with children's artwork on walls, soft warm light, caring atmosphere, cream and soft blue tones, simple rounded shapes`
10. **电子产品**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A child looking at a tablet with interest and excitement, colorful learning apps on screen, cozy bedroom with soft light, learning through play atmosphere, warm orange and cream tones, simple rounded shapes`
11. **自我设限**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A child breaking through a paper wall with a smile, reaching towards bright sunlight on the other side, metaphorical and inspiring, warm golden light, soft warm colors, simple and hopeful, rounded shapes`
12. **学习方法**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A parent and child studying together at a wooden desk, parent pointing gently at a book, child nodding with understanding, warm evening lamp light, cozy home study atmosphere, soft cream and warm brown tones, simple rounded shapes`
13. **小目标**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A happy child holding a small gold star sticker on chest, proud smile, small completed task list on desk, celebration moment, warm sunny room, soft yellow and cream tones, simple rounded shapes`
14. **亲子沟通**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A parent sitting beside a child, listening attentively with gentle eye contact, warm living room background, soft afternoon light, caring and trusting atmosphere, warm earth tones, simple rounded shapes`
15. **学习环境**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A child's tidy study desk by the window, warm desk lamp on, a small succulent plant, some open books and a pen holder, soft evening light, clean and cozy, cream and light brown tones, simple rounded shapes`
16. **专注力培养**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A child focusing on drawing at a desk, completely absorbed, a cup of tea steaming quietly beside, soft window light, peaceful and focused atmosphere, warm cream and brown tones, simple rounded shapes`
17. **阅读兴趣**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A child lying on a cozy rug reading a picture book, laughing out loud, a small bookshelf nearby with colorful spines, warm afternoon sunlight, relaxed and joyful atmosphere, soft warm colors, simple rounded shapes`
18. **错题整理**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A child happily sorting colorful sticky notes on a study board, a parent helping nearby with a smile, warm study room background, cozy and encouraging atmosphere, warm earth tones, simple rounded shapes`
19. **睡眠与学习**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A cozy child bedroom at night, a child stretching and yawning before going to bed, soft moonlight through curtains, a small star night light on the nightstand, peaceful sleepy atmosphere, soft blue and warm cream tones, simple rounded shapes`
20. **家长情绪**：`Hand-drawn illustration, soft brushstrokes, warm and cozy mood, warm comfortable colors like macaroni and muted tones, education scene with desk lamp, books, parent-child interaction, no text no watermark, vertical 3:4 ratio. A calm parent taking a deep breath with a warm cup of tea in hands, soft window light, peaceful corner of living room, cozy and healing atmosphere, warm cream and light brown tones, simple rounded shapes`

## 九、执行流程

1. **读取历史**：读取 `~/.openclaw/skills/ssai-dailymoments/history.json`
2. **比对方向**：从方向池中选择5个与历史完全不重复的方向
3. **生成文案**：为每个方向生成80-160字文案，确保观点新鲜
4. **生成图片**：用不同seed生成5张水彩插画
5. **发送**：依次发送5条文案+图片
6. **存档**：将本次5条内容追加写入 history.json

---

## ⚠️ 安装备注（必看）

**文本模型建议使用 MiniMax m2.7。**

**生图模型必须配置！** 安装前请确认：
- 已拥有生图 API（MiniMax image-01 或其他兼容服务）
- 在 OpenClaw 后台填入有效的 API Key
- 若没有生图模型，Skill 无法生成图片，请先配置后再启用

配置路径：OpenClaw 后台 → Skill设置 → 图片生成规则 → 填入 API Key
