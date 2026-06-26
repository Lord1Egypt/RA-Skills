# 🎨 xiaohongshu-cover-gen

> AI Agent Skill：为小红书帖子生成高质量封面图和内容图卡

**经 5 轮实战验证、6 次翻车迭代沉淀的配图方法论。** 不是"调 API 生成图片"——是一套从审美调研、创意构思、prompt 编写到生成交付的完整工作流。

---

## ✨ 特性

- 🎯 **6 阶段标准流程**：调研 → 分析 → 确认 → prompt → 生成 → 检查
- 🧠 **14 条实战翻车经验**（Gotchas）：按严重程度分级，避免重复踩坑
- 🖌️ **核心审美原则**：从用户情绪出发设计封面，而非技术概念
- 🤖 **Lovart 完整操作手册**：agent-browser 自动化 Phase 0-5 全流程
- ✅ **8 项 prompt 自检 checklist**：发送前最后一道质量关卡
- 📊 **审美积累体系**：定期浏览 + 分类归档，持续提升审美水平
- 🐍 **Python 图卡生成器**：PIL 批量生成纯文字卡，Design Token 可配置

---

## 📁 目录结构

```
xiaohongshu-cover-gen/
├── SKILL.md                          # ⭐ 核心 Skill 文件（加载此文件）
├── README.md                         # 项目说明
├── .gitignore
│
├── references/                       # 参考文档
│   ├── lovart-operation.md           # Lovart 平台完整操作手册
│   ├── prompt-checklist.md           # Prompt 发送前 8 项自检
│   ├── research-platforms.md         # 调研平台操作指南
│   └── aesthetic-guide.md            # 审美积累文档模板 & 指南
│
├── scripts/                          # 辅助脚本
│   ├── gen_text_cards.py             # Python 图卡生成器
│   ├── check_jwt.sh                  # Lovart JWT 过期检查
│   └── download_image.sh             # Lovart 图片下载（绕过 SSL）
│
└── templates/                        # 模板文件
    ├── design-tokens.md              # Design Token 模板 + 3 种配色示例
    └── iteration-log.md              # 迭代日志模板
```

---

## 🚀 Quick Start

### 1. 作为 Agent Skill 使用

将 `SKILL.md` 加载到你的 AI Agent（如 CodeBuddy、Cursor、Claude 等），Agent 会自动按照 Skill 中定义的流程工作。

**触发词**：`小红书配图`、`封面生成`、`图卡设计`、`XHS cover`、`social media image`

### 2. 首次使用前准备

#### Lovart 账号（生成封面图）

1. 注册 [Lovart](https://lovart.ai) 账号
2. 在浏览器 DevTools 中导出 3 个关键 cookies：`usertoken`、`useruuid`、`webid`
3. 保存为 `.lovart_cookies.json`（格式见 `references/lovart-operation.md`）

#### Python 环境（生成文字图卡）

```bash
pip install Pillow
```

### 3. 工作流概览

```
收到帖子内容
    ↓
阶段 0：精准调研（10min）— Dribbble + 小红书 + 品牌官网
    ↓
阶段 1：帖子分析 → 配图方案
    ↓
阶段 2：方案确认 + 素材需求前置
    ↓
阶段 3：写 prompt（过 8 项自检）
    ↓
阶段 4：Lovart 生成 / Python 图卡
    ↓
阶段 5：整合检查
```

---

## 🛠️ 前置依赖

| 依赖 | 用途 | 必需？ |
|------|------|--------|
| [Lovart](https://lovart.ai) 账号 | AI 生图 | ✅ 封面图必需 |
| `agent-browser` | 浏览器自动化 | ✅ Lovart 操作必需 |
| Node.js | JWT 检查 + 图片下载 | ✅ |
| Python 3 + Pillow | 文字图卡生成 | 可选（纯文字卡时用） |

---

## 📖 核心理念

### 封面只有 0.5 秒的生存时间

小红书信息流中，用户拇指飞速滑动。封面的职责不是"完整传达信息"，而是**在 0.5 秒内制造好奇心和点击欲**。

### 从用户情绪出发，不是从技术概念出发

> 这是 5 轮迭代最核心的认知沉淀。

❌ 错误：帖子讲 AI 论文 → 画一个大脑（最直线的联想 = 最缺乏创意的路径）

✅ 正确：帖子讲"马斯克点赞的 AI 论文" → 画一个 3D Clay 马斯克竖大拇指

### 审美 > 工具

配图能力的核心不是工具操作，而是审美和生态理解。工具可以学会，审美才是壁垒。

---

## ⚠️ 已知限制

- Lovart 不支持 headless 浏览器 OAuth 登录，必须手动提供 cookies
- Lovart JWT 有效期约 7 天，需定期更新
- `agent-browser` 命令长度限制 ≤ 1024 字节，长 prompt 需分段输入
- `agent-browser wait` 超过 30s 会触发 idle timeout，需分段等待
- Lovart 连续操作可能触发 hCaptcha，建议每次会话只生 1-2 张
- `a.lovart.ai` SSL 证书与 curl/Python 不兼容，图片下载必须用 Node.js

---

## 📝 License

MIT

---

## 🙏 致谢

- [Lovart](https://lovart.ai) — AI 设计生成工具
- [Dribbble](https://dribbble.com) — 设计灵感来源
- [Pillow (PIL)](https://pillow.readthedocs.io) — Python 图像处理
- 5 轮实战中踩过的所有坑 🕳️
