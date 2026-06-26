# 📝 公众号文章自动创作技能

**OpenClaw Skill - 从选题到发布全流程自动化**

---

## 🚀 快速开始

### 前置依赖

```bash
# 确保依赖技能已安装：
clawhub install baidu-search
clawhub install wanx-image-generator    # 通义万相，配图生成（必需）
clawhub install wechat-toolkit          # 公众号发布（必需）
```

### 配置 API Key

**通义万相配图需要阿里云百炼 API Key**：

```bash
# 推荐：统一配置文件
vim ~/.openclaw/.env

# 添加配置
DASHSCOPE_API_KEY="sk-xxx"
```

**获取 API Key**：https://bailian.console.aliyun.com/?tab=globalset#/efm/api_key

### 使用方式

**直接对话触发：**

```
帮我写一篇关于"AI 自动化工作流"的文章，发布到公众号
```

OpenClaw 会自动执行完整流程：
1. 生成框架
2. 搜索素材
3. 撰写文章
4. 生成配图（通义万相）
5. 发布到公众号

---

## 📋 完整流程

### 步骤 1: 生成框架

```bash
node scripts/generate-framework.js "文章主题"
```

**功能：**
- 自动诊断主题类型（教程/产品/通用）
- 生成结构化框架
- 输出：`examples/framework.md`

**耗时：** <1 秒

---

### 步骤 2: 搜索素材

```bash
node scripts/search.js "关键词"
```

**功能：**
- 调用百度搜索
- 获取实时信息
- 输出：JSON 格式搜索结果

**耗时：** 约 30 秒

---

### 步骤 3: 撰写文章

**OpenClaw AI 直接撰写，不需要额外 API！**

**要求：**
- 根据框架展开
- 结合搜索结果
- 约 3000 字
- Markdown 格式
- 包含 frontmatter（title + cover）

**耗时：** 约 30-60 秒

---

### 步骤 4: 生成配图 ⭐

**调用 wanx-image-generator（通义万相）生成图片：**

#### 封面图

```bash
cd ../wanx-image-generator
uv run scripts/generate.py \
  --prompt "技术文章封面图，AI 自动化主题，简约科技感，蓝紫色调，不要文字" \
  --output examples/images/cover.png \
  --model wan2.6-t2i \
  --size "1280*1280" \
  --no-watermark
```

#### 正文配图（5 张）

```bash
# 配图 1：引言 - 现代化办公室
uv run scripts/generate.py \
  --prompt "现代化办公室，职场人士用电脑，屏幕显示 AI 界面" \
  --output examples/images/img1.png \
  --model wan2.6-t2i --size "1280*1280" --no-watermark

# 配图 2：概念图 - AI 架构
uv run scripts/generate.py \
  --prompt "AI 概念架构图，神经网络 + 流程图，融合效果" \
  --output examples/images/img2.png \
  --model wan2.6-t2i --size "1280*1280" --no-watermark

# 配图 3：趋势图 - 上升曲线
uv run scripts/generate.py \
  --prompt "趋势分析图，上升曲线展示增长，科技感网格背景" \
  --output examples/images/img3.png \
  --model wan2.6-t2i --size "1280*1280" --no-watermark

# 配图 4：流程图 - 三步
uv run scripts/generate.py \
  --prompt "三步流程图，三个圆形节点，蓝紫渐变" \
  --output examples/images/img4.png \
  --model wan2.6-t2i --size "1280*1280" --no-watermark

# 配图 5：实战场景 - 多显示器
uv run scripts/generate.py \
  --prompt "多显示器工作站，3 个屏幕显示代码和仪表盘" \
  --output examples/images/img5.png \
  --model wan2.6-t2i --size "1280*1280" --no-watermark
```

**性能数据：**
- ✅ 稳定性：100%（5/5 成功）
- ✅ 速度：平均 6.5 秒/张
- ✅ 质量：1280×1280 高清
- ✅ 总耗时：约 33 秒（5 张）

---

### 步骤 5: 发布到公众号

```bash
node scripts/publish.js examples/article.md
```

**功能：**
- 检查 frontmatter
- 检查图片路径
- 调用 wechat-toolkit 发布
- 返回草稿箱链接

**耗时：** 5-10 秒

---

## 🔧 脚本说明

| 脚本 | 用途 | 输入 | 输出 |
|------|------|------|------|
| `generate-framework.js` | 生成框架 | 文章主题 | `examples/framework.md` |
| `search.js` | 百度搜索 | 关键词 | JSON 搜索结果 |
| `publish.js` | 公众号发布 | `article.md` | 草稿箱链接 |

---

## ⚙️ 配置说明

### 通义万相配图

**配置方式（3 种，任选其一）：**

**方式 1: 统一配置文件**（推荐）
```bash
# 编辑 ~/.openclaw/.env
DASHSCOPE_API_KEY="sk-xxx"
```

**方式 2: Skill 目录 .env 文件**
```bash
# 编辑 ~/.openclaw/workspace/skills/wanx-image-generator/.env
DASHSCOPE_API_KEY="sk-xxx"
```

**方式 3: 环境变量**（临时测试）
```bash
export DASHSCOPE_API_KEY="sk-xxx"
```

**获取 API Key：**
https://bailian.console.aliyun.com/?tab=globalset#/efm/api_key

**配置优先级**：命令行参数 > 环境变量 > ~/.openclaw/.env > Skill 目录/.env

**模型选择：**
- `wan2.6-t2i` ⭐ - 最新版，同步调用，推荐
- `wan2.5-t2i-preview` - 支持自由尺寸
- `wan2.2-t2i-flash` - 速度更快

**尺寸选择：**
- `1280*1280` - 方形，通用
- `1696*960` - 16:9 横版
- `960*1696` - 9:16 竖版

### 百度搜索

自动读取 OpenClaw 配置中的 `baidu-search` API Key。

### 公众号发布

在 `~/.openclaw/workspace/TOOLS.md` 中配置：

```bash
export WECHAT_APP_ID=你的 APP_ID
export WECHAT_APP_SECRET=你的 APP_SECRET
```

**IP 白名单：**
```bash
curl ifconfig.me
# 添加到公众号后台 → 设置 → IP 白名单
```

---

## 📁 文件结构

```
wechat-mp-auto-publisher/
├── SKILL.md                          # 技能指令
├── README.md                         # 使用说明
├── scripts/
│   ├── generate-framework.js         # 生成框架
│   ├── search.js                     # 百度搜索
│   └── publish.js                    # 公众号发布
├── examples/
│   ├── framework.md                  # 生成的框架
│   ├── article.md                    # 生成的文章
│   └── images/                       # 配图目录
└── templates/
    └── article-template.md           # 文章模板
```

---

## 🎯 使用场景

### 场景 1: 技术教程

```
写一篇"React 性能优化指南"的技术教程
```

### 场景 2: 产品介绍

```
写一篇 OpenClaw 功能介绍的文章
```

### 场景 3: 实战案例

```
写一篇 AI 自动化工作流的实战案例
```

---

## ⚠️ 注意事项

1. **图片路径必须绝对路径** - wechat-toolkit 要求
2. **发布前检查 IP 白名单** - 确保在公众号后台配置
3. **每步用户确认** - 可随时停止或调整
4. **失败降级方案** - 提供手动操作指引
5. **配图生成失败** - 检查 API Key，重试即可

---

## 🐛 故障排查

### 问题 1: 框架生成失败

**解决：** 检查主题是否有效，使用通用模板

### 问题 2: 搜索失败

**解决：** 检查 BAIDU_API_KEY 配置，或手动补充资料

### 问题 3: 生图失败

**解决：**
```bash
# 检查 API Key 配置（统一配置文件）
cat ~/.openclaw/.env

# 或检查 Skill 目录配置
cat ~/.openclaw/workspace/skills/wanx-image-generator/.env

# 测试生成
cd ~/.openclaw/workspace/skills/wanx-image-generator
uv run scripts/generate.py --prompt "测试" --output test.png --model wan2.6-t2i
```

### 问题 4: 发布失败

**解决：**
```bash
# 检查配置
echo $WECHAT_APP_ID
echo $WECHAT_APP_SECRET

# 检查 IP 白名单
curl ifconfig.me

# 手动发布
cat "article.md" | WECHAT_APP_ID=xxx WECHAT_APP_SECRET=xxx wenyan publish -t lapis -h solarized-light
```

---

## 📊 性能数据

| 环节 | 耗时 | 成功率 |
|------|------|--------|
| 框架生成 | <1 秒 | 100% |
| 百度搜索 | 30 秒 | 100% |
| 文章撰写 | 30-60 秒 | 100% |
| 配图生成（5 张） | 33 秒 | 100% |
| 公众号发布 | 5-10 秒 | 100% |
| **总计** | **约 2 分钟** | **100%** |

**配图工具**：wanx-image-generator（通义万相 wan2.6-t2i）
- 稳定性：100%
- 速度：6.5 秒/张
- 质量：1280×1280 高清

---

## 📝 更新日志

### v3.2.0 (2026-03-12) - 文档更新

- ✅ 更新 API Key 配置说明（支持 ~/.openclaw/.env 统一配置）
- ✅ 移除 nano-banana-pro 引用
- ✅ 更新故障排查指南
- ✅ 更新性能数据

### v3.1.0 (2026-03-12) - 通义万相配图

- ✅ 配图工具从 nano-banana-pro 改为 wanx-image-generator
- ✅ 稳定性提升至 100%
- ✅ 速度提升至 6.5 秒/张
- ✅ 更新 SKILL.md 和 README.md

### v3.0.0 (2026-03-12) - OpenClaw Skill 重构

- ✅ 改为真正的 OpenClaw Skill
- ✅ AI 由 OpenClaw 自动调用
- ✅ 简化脚本，只负责具体操作

### v2.1.0 (2026-03-12) - 智能选题框架

- ✅ 自动诊断主题类型
- ✅ 百度搜索增强

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**Discord**: https://discord.com/invite/clawd

---

*Created with ❤️ by OpenClaw Community*
