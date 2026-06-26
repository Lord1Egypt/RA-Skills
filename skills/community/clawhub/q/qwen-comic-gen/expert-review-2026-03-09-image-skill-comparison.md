# 图像生成技能横评报告

**生成时间：** 2026-03-09 07:32
**对比技能：** Nano Banana Pro vs Generate Image

---

## 📊 快速对比总览

| 维度 | Nano Banana Pro | Generate Image |
|------|-----------------|----------------|
| **来源** | github/awesome-copilot | davila7/claude-code-templates |
| **安装数** | 7,000+ | 405 |
| **API 提供商** | OpenRouter (Gemini 3 Pro) | OpenRouter (多模型) |
| **核心模型** | google/gemini-3-pro-image-preview | 多模型可选 |
| **分辨率** | 1K/2K/4K | 取决于模型 |
| **图像编辑** | ✅ 支持 | ✅ 支持 |
| **多图合成** | ✅ 支持 (最多 3 张) | ❌ 单图 |
| **系统提示定制** | ✅ 支持 | ❌ 不支持 |
| **默认工作流** | draft→iterate→final | 直接生成 |
| **费用** | OpenRouter 按量计费 | OpenRouter 按量计费 |
| **推荐指数** | ⭐⭐⭐⭐⭐ (5/5) | ⭐⭐⭐⭐ (4/5) |

---

## 🎯 目标效果对比

### Nano Banana Pro

**核心目标：** 专业级图像生成与编辑，支持快速迭代

**效果特点：**
- ✅ **三阶段工作流**：1K 草稿 → 迭代 → 4K 最终（节省时间和 API 费用）
- ✅ **多图合成**：支持最多 3 张输入图像合成（人脸合成、场景融合等）
- ✅ **系统提示定制**：可通过 assets/SYSTEM_TEMPLATE 定制生成行为
- ✅ **分辨率控制**：1K/2K/4K 精确控制
- ✅ **编辑模式**：保留原图风格，精准修改

**适用场景：**
- 专业图像设计工作流
- 需要多次迭代的设计任务
- 多图合成需求（人脸融合、场景组合）
- 对分辨率有明确要求的项目

### Generate Image

**核心目标：** 通用图像生成，简单易用

**效果特点：**
- ✅ **多模型支持**：Gemini 3 Pro / FLUX.2 Pro / FLUX.2 Flex
- ✅ **模型选择灵活**：根据质量/速度/成本选择
- ✅ **科学示意图区分**：明确区分通用图像和科学示意图
- ✅ **.env 自动检测**：自动查找项目目录的 API 密钥
- ✅ **简单工作流**：直接生成，适合快速任务

**适用场景：**
- 快速生成单张图像
- 需要多模型选择的场景
- 科学/技术文档配图
- 成本敏感的任务（可用 FLUX.2 Flex）

---

## ⚙️ 实现逻辑对比

### Nano Banana Pro

**技术架构：**
```
用户请求 → 解析参数 → 调用 OpenRouter API → 保存 PNG → 输出 MEDIA:
```

**核心脚本：** `scripts/generate_image.py`

**关键特性：**
1. **三阶段工作流**
   - Draft (1K): 快速反馈循环
   - Iterate: 小步调整 prompt，保持输入图像不变
   - Final (4K): prompt 锁定后生成高清版本

2. **多图合成逻辑**
   - 支持 `--input-image` 参数重复使用（最多 3 次）
   - 自动处理多图融合

3. **系统提示定制**
   - 读取 `assets/SYSTEM_TEMPLATE`
   - 无需修改代码即可定制行为

4. **文件名自动生成**
   - 格式：`yyyy-mm-dd-hh-mm-ss-描述.png`
   - 自动根据 prompt 生成描述性文件名

**依赖：**
- `uv` (Python 包管理器)
- OpenRouter API 密钥
- Python 3.x

### Generate Image

**技术架构：**
```
用户请求 → 检查.env → 选择模型 → 调用 OpenRouter API → 保存 PNG → 输出
```

**核心脚本：** `scripts/generate_image.py`

**关键特性：**
1. **多模型支持**
   - 默认：`google/gemini-3-pro-image-preview`
   - 备选：`black-forest-labs/flux.2-pro` (快速高质量)
   - 经济：`black-forest-labs/flux.2-flex` (仅生成)

2. **.env 自动检测**
   - 自动查找项目目录/父目录的 `.env` 文件
   - 清晰的错误提示

3. **模型选择逻辑**
   - 质量优先：Gemini 3 Pro / FLUX.2 Pro
   - 成本优先：FLUX.2 Flex
   - 编辑需求：必须用 Gemini 3 Pro 或 FLUX.2 Pro

4. **科学示意图区分**
   - 明确推荐使用 `scientific-schematics` 技能处理技术图表

**依赖：**
- Python 3.x
- OpenRouter API 密钥
- `.env` 文件（可选但推荐）

---

## 💰 费用和代价对比

### 共同点

**API 提供商：** OpenRouter (openrouter.ai)

**计费模式：** 按量计费（按图像生成次数 + 分辨率）

**API 密钥：** 需要 OpenRouter API 密钥（免费获取，按使用付费）

### Nano Banana Pro

**费用结构：**
- **1K 分辨率**：基准价格（约 $0.01-0.03/张）
- **2K 分辨率**：约 2-3x 基准价格
- **4K 分辨率**：约 4-6x 基准价格

**成本优化策略：**
- ✅ 三阶段工作流：先用 1K 草稿迭代，避免直接生成 4K 浪费
- ✅ 系统提示定制：减少试错成本
- ✅ 多图合成：一次 API 调用合成多图，比分别生成便宜

**隐性成本：**
- 需要学习三阶段工作流
- 需要理解系统提示定制

**推荐用户：** 专业用户、高频使用者、对质量有要求的用户

### Generate Image

**费用结构：**
- **Gemini 3 Pro**：高质量，价格较高（约 $0.03-0.05/张）
- **FLUX.2 Pro**：高质量，价格中等（约 $0.02-0.04/张）
- **FLUX.2 Flex**：低质量，价格低廉（约 $0.005-0.01/张）

**成本优化策略：**
- ✅ 多模型选择：根据任务选择合适模型
- ✅ 经济模式：FLUX.2 Flex 适合快速测试
- ✅ .env 自动检测：减少配置错误导致的浪费

**隐性成本：**
- 需要了解不同模型的特点
- 需要自己管理 API 密钥

**推荐用户：** 初学者、成本敏感用户、需要灵活性的用户

---

## 🔍 深度对比分析

### 1. 工作流设计

| 维度 | Nano Banana Pro | Generate Image |
|------|-----------------|----------------|
| **设计理念** | 专业迭代 | 简单直接 |
| **学习曲线** | 中等（需要理解三阶段） | 低（直接使用） |
| **适用频率** | 高频专业使用 | 低中频使用 |
| **浪费风险** | 低（草稿迭代避免浪费） | 中（直接生成可能不满意） |

**结论：** Nano Banana Pro 的工作流更适合专业用户，Generate Image 更适合快速任务。

### 2. 灵活性

| 维度 | Nano Banana Pro | Generate Image |
|------|-----------------|----------------|
| **模型选择** | 单一（Gemini 3 Pro） | 多模型（3 种可选） |
| **分辨率控制** | 精确（1K/2K/4K） | 取决于模型 |
| **系统定制** | ✅ 支持 | ❌ 不支持 |
| **多图合成** | ✅ 支持 | ❌ 不支持 |

**结论：** Nano Banana Pro 在深度上更强，Generate Image 在广度上更强。

### 3. 用户体验

| 维度 | Nano Banana Pro | Generate Image |
|------|-----------------|----------------|
| **安装难度** | 中等（需要 uv） | 中等（需要 Python） |
| **配置难度** | 中等（API 密钥） | 简单（.env 自动检测） |
| **使用难度** | 中等（需要理解工作流） | 简单（直接使用） |
| **错误提示** | 清晰 | 清晰 |

**结论：** Generate Image 对新手更友好，Nano Banana Pro 需要一定学习成本。

### 4. 社区活跃度

| 维度 | Nano Banana Pro | Generate Image |
|------|-----------------|----------------|
| **安装数** | 7,000+ | 405 |
| **更新时间** | 2026-03-08 | 未知 |
| **来源可信度** | github/awesome-copilot (官方) | davila7/claude-code-templates (个人) |
| **文档质量** | 详细 | 详细 |

**结论：** Nano Banana Pro 社区更活跃，更新更频繁。

---

## 🏆 最终推荐

### 推荐 Nano Banana Pro，如果：

- ✅ 你是**专业用户**，需要高质量图像
- ✅ 你需要**多次迭代**设计
- ✅ 你需要**多图合成**功能
- ✅ 你愿意学习**三阶段工作流**
- ✅ 你对**分辨率有明确要求**
- ✅ 你希望**定制系统提示**

### 推荐 Generate Image，如果：

- ✅ 你是**初学者**，想要简单易用
- ✅ 你**成本敏感**，需要经济模型
- ✅ 你需要**多模型选择**
- ✅ 你只做**简单生成任务**
- ✅ 你希望**.env 自动检测**
- ✅ 你不需要多图合成

---

## 💡 我的推荐

**综合推荐：Nano Banana Pro ⭐⭐⭐⭐⭐ (5/5)**

**理由：**
1. **安装数 7,000+** - 社区验证，质量可靠
2. **三阶段工作流** - 专业设计，节省长期成本
3. **多图合成** - 独特功能，其他技能没有
4. **系统提示定制** - 高度可定制
5. **github/awesome-copilot 出品** - 官方背书

**但需要注意：**
- 需要学习三阶段工作流
- 需要理解分辨率选择
- 初始配置稍复杂

**备选：Generate Image ⭐⭐⭐⭐ (4/5)**

适合初学者和成本敏感用户。

---

## 📋 安装建议

### 安装 Nano Banana Pro（推荐）

```bash
# 安装技能
npx skills add github/awesome-copilot@nano-banana-pro-openrouter -g -y

# 设置 API 密钥（PowerShell）
$env:OPENROUTER_API_KEY = "sk-or-你的密钥"

# 测试生成
uv run ~/.agents/skills/nano-banana-pro/scripts/generate_image.py --prompt "A beautiful sunset" --filename test.png --resolution 1K
```

### 安装 Generate Image（备选）

```bash
# 安装技能
npx skills add davila7/claude-code-templates@generate-image -g -y

# 创建.env 文件
echo "OPENROUTER_API_KEY=sk-or-你的密钥" > .env

# 测试生成
python scripts/generate_image.py "A beautiful sunset"
```

---

## 🎯 总结

| 维度 | 胜出者 |
|------|--------|
| **功能丰富度** | 🏆 Nano Banana Pro |
| **易用性** | 🏆 Generate Image |
| **成本优化** | 🏆 Generate Image (多模型) |
| **专业工作流** | 🏆 Nano Banana Pro |
| **社区活跃度** | 🏆 Nano Banana Pro |
| **多图合成** | 🏆 Nano Banana Pro (独家) |

**最终推荐：Nano Banana Pro** - 功能更强大，社区更活跃，专业工作流设计更优秀。

---

_报告生成时间：2026-03-09 07:32_
_数据来源：skills.sh + ClawHub_
