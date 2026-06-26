# 小红书内容创作助手 v4.5

## 技能简介

**定位：** 小红书博主全能运营助手，集成 AI 生图 + 草稿发布全流程

**核心功能：**
- 🎨 AI 生图（**智能路由**：模型优先，豆包备选）
- ✍️ 小红书爆款文案创作
- 📤 草稿箱自动发布
- 📢 确认后立即发布
- 📱 **未登录时自动点出二维码登录**

**适用人群：** 小红书博主、微商、内容创作者

**跨平台：** ✅ 支持 Windows / macOS / Linux

---

## 功能一：AI 生图（智能路由）

### 核心策略

生图前系统自动判断，按以下优先级执行：

```
当前模型能生图 + 额度够 → 模型生图（MiniMax API）
        ↓ 失败
    降级 → 豆包全自动化生图（无需用户引导）
```

**智能路由脚本：** `scripts/generate_image_smart.js`

```bash
node scripts/generate_image_smart.js --prompt "可爱的橘猫" --n 4
```

---

### 方式1：MiniMax 模型生图（优先）

**条件：** config.json 配置了有效的 MiniMax API Key

**优势：** 精确可控、额度内免费（每日50次）、程序化调用

**无需安装 Python！** 已改为纯 Node.js 实现，不依赖任何 Python 库。

**前置安装：**
- Playwright：OpenClaw 自带，无需安装
- MiniMax API Key：访问 https://platform.minimaxi.com/ 注册获取

**配置 API Key：**
```bash
cp scripts/config.json.example scripts/config.json
# 编辑 config.json，填入你的 MiniMax API Key
```

**参数说明：**
- `--prompt/-p`：图片描述（英文效果更好）
- `--aspect_ratio/-r`：图片比例（3:4、1:1、16:9，默认3:4）
- `--n`：生成数量（1-9张）

---

### 方式2：豆包全自动化生图（降级备选）

**触发条件：** MiniMax API Key 未配置 / Python 不可用 / API 调用失败

**自动化流程（无需任何用户引导）：**
```
1. 自动打开豆包浏览器
2. 自动定位输入框
3. 自动填写并发送生图prompt
4. 自动轮询检测图片生成（最多等90秒）
5. 自动提取图片URL
6. 自动下载保存到 generated_images/
7. 返回文件路径，继续后续流程
```

**整个过程无需人工介入！**

---

## 功能二：草稿自动发布

### 前置条件

1. **OpenClaw 浏览器正在运行**
   - 确保 OpenClaw 应用已启动
   - 浏览器状态为"Running"

2. **登录小红书创作平台**
   - 打开 https://creator.xiaohongshu.com
   - ✅ **未登录时脚本会自动点出二维码**，你用小红书 App 扫码即可
   - 不需要提前手动登录

3. **Playwright（OpenClaw 自带）**
   OpenClaw 自带 playwright-core，无需额外安装

---

### 快速发布流程

```bash
cd skills/xhs-content-studio
node scripts/upload_auto.js \
  --title "养猫必知的5件事 🐱" \
  --content-file "正文.txt" \
  --images "img_123_1.jpeg,img_123_2.jpeg,img_123_3.jpeg"
```

**长文本建议用 `--content-file` 从文件读取**，避免命令行编码问题。

---

### 草稿保存后：是否发布？

草稿保存成功后，会主动询问你是否要发布：

```
✅ 草稿保存成功！
📌 是否需要我现在帮你发布？
   回复"发布"即发布
   回复"否"则保留草稿，稍后手动发布
```

---

## 功能三：爆款文案创作

### 标题公式

| 类型 | 公式 | 示例 |
|------|------|------|
| 提问式 | XX真的吗？ | 养猫真的会变穷吗？ |
| 震惊式 | 没想到XX这么XX | 没想到猫咪这么记仇！ |
| 数字式 | N个XX技巧 | 5个让猫更亲人的技巧 |
| 挑战式 | 你知道XX吗？ | 你知道猫咪的17个秘密吗？ |
| 吐槽式 | XX使我快乐/崩溃 | 当妈后才知道的15件事 |
| 反问式 | XX有那么难吗？ | 养猫有那么难吗？ |

### 正文结构

```
开头（50字）：痛点/共鸣/悬念

正文（300-400字）：
- 3-5个要点
- 每个要点配 emoji
- 简短精炼

结尾（50字）：互动引导 + 话题标签
```

### 话题标签规则

- 数量：3-10 个
- 格式：以 # 开头
- 放置：正文章节末尾
- 示例：`#养猫 #猫咪日常 #铲屎官日记`

---

## 平台限制清单

| 项目 | 限制 |
|------|------|
| 标题 | ≤20 字 |
| 正文 | ≤1000 字 |
| 配图 | 1-18 张 |
| 图片大小 | ≤32MB/张 |
| 图片格式 | png/jpg/jpeg/webp |

**最佳实践：**
- 标题：15-18 字
- 正文：300-500 字
- 配图：4-9 张

---

## 质量检查清单

发布前必须验证：
- [ ] 标题字数 ≤20
- [ ] 正文字数 ≤1000
- [ ] 配图数量 1-18 张
- [ ] 话题标签 3-10 个
- [ ] 内容预览确认
- [ ] 点击"暂存离开"前再次确认

---

## 文件结构

```
xhs-content-studio/
├── SKILL.md                      # 本文件
├── README.md                     # 入门指南
├── scripts/
│   ├── generate_image_smart.js   # 智能生图脚本（主入口，v2.0）
│   ├── generate_image.py          # MiniMax 直调脚本（备选）
│   ├── upload_auto.js            # 自动化发布脚本（v4.4 跨平台）
│   ├── config.json.example       # 配置文件模板
│   ├── install.bat               # 一键安装依赖（Windows）
│   └── install.sh                 # 一键安装依赖（macOS/Linux）
├── references/
│   ├── hashtags.md               # 话题标签库
│   ├── title-formulas.md         # 标题公式大全
│   └── content-templates.md      # 内容模板
└── generated_images/             # 生成的图片目录（自动创建）
```

---

## 故障排查

### Q: 提示"MiniMax API Key 未配置"
**解决：** 复制 config.json.example 为 config.json，填入 API Key；或使用豆包方案

### Q: MiniMax 生图失败
**解决：** 智能路由自动降级到豆包，按指引操作即可

### Q: 图片上传失败，只有 1 张成功
**解决：** 使用 upload_auto.js，或分批上传

### Q: browser.upload() 超时
**解决：** 重启 OpenClaw 浏览器后重试

### Q: Playwright 连接失败
**解决：** 确保 OpenClaw 浏览器正在运行，CDP 端口 18800 可用

### Q: 草稿保存失败
**解决：** 检查"暂存离开"按钮是否可见，可能需要等待页面加载完成

---

## 快速入门

**第一步：配置（如使用 MiniMax 生图）**
```bash
cp scripts/config.json.example scripts/config.json
# 编辑 config.json，填入你的 MiniMax API Key
```

**第二步：生图（智能路由，自动选择最优方案）**
```bash
node scripts/generate_image_smart.js -p "可爱的橘猫" -n 4
```

**第三步：发布草稿**
```bash
node scripts/upload_auto.js \
  --title "标题" \
  --content-file "正文.txt" \
  --images "img_xxx_1.jpeg,img_xxx_2.jpeg"
```

---

*最后更新：2026-03-30 v4.5*
