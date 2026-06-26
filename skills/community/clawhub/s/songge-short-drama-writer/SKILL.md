---
name: songge-short-drama-writer
description: 专业AI短剧/漫剧剧本创作助手，支持男频/女频爆款短剧、AI漫剧剧本撰写，包含2025最新行业爆款规律、标准结构模板、爆款爽点设计和多平台JSON一键导出。当用户需要写短剧剧本、短剧大纲、剧情设计、AI漫剧脚本、漫画分镜剧本，或提到viflow.app导入时自动触发。包含完整的60-120集黄金结构模板、100+爆款钩子、男女频爆款要素，以及独家多平台分镜JSON导出功能（支持ViFlow等主流平台）。
license: MIT-0
---

# AI 短剧脚本创作大师

专业 AI 短剧/漫剧剧本创作助手，支持男频/女频爆款短剧、AI 漫剧剧本创作。包含 2025 最新行业爆款规律、标准结构模板、爆款爽点设计、多平台分镜 JSON 导出。

当用户需要创作短剧剧本、短剧大纲、剧情设计、AI 漫剧脚本、漫画分镜剧本，或提到 ViFlow / viflow.app 导入时，自动触发本技能。

---

## 核心功能

- 📖 基于 2025 年抖音算法和行业数据
- 🎭 男频/女频爆款要素全拆解（含漫剧专属套路）
- 🎬 真人短剧 + AI 漫剧双模板
- 📤 **多平台分镜 JSON 导出**（ViFlow v1.2 兼容）
- 📐 **分镜结构化输出**（角色库 + 场景库 + 分镜格）
- 🪝 100+ 爆款钩子模板
- 📊 4 阶段黄金结构（60-120 集）

---

## 创作流程（按顺序执行）

### Step 1：定大类
确认是**短剧**还是**漫剧**，这是所有后续选择的基础。

### Step 2：定风格标签
在选定的大类下，结合市场需求和目标用户，选择对应的风格子类标签：

**短剧风格标签（子集）：**
- 男频：战神/逆袭/霸总/系统/都市/古风/悬疑/甜宠/虐恋/职场
- 女频：霸总/甜宠/虐恋/穿越/重生/复仇/闪婚/闪离/青梅竹马/姐弟恋

**漫剧风格标签（子集）：**
- 国漫古风 / 国漫现代 / 日漫画风 / 韩漫风格 / 写实3D / Q版可爱
- （漫剧必须在视觉风格大类下选择具体画风）

### Step 3：基础设定
建立基础设定库：
- **角色库**：所有角色（含 imagePrompt 用于AI生成一致性）
- **道具库**：关键道具（含 imagePrompt）
- **场景库**：所有场景（含 time_period / imagePrompt）

### Step 4：形成 Outline 大纲
按4阶段黄金结构形成章节概述，建议选择集数分段结构进行试写（60/90/120集等）。

### Step 5：分幕创作
按4阶段黄金结构分幕推进创作。

### Step 6：拆解分镜格
每集 8-12 格，每格含时长+运镜+对话+videoPrompt。

### Step 7：导出 ViFlow JSON
按 ViFlow v1.2 Schema 格式导出 JSON 文件，导入 ViFlow.app 分镜工程使用。

---

## 参考文档索引（按需读取）

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| `references/market-rules.md` | 抖音算法、男女频爆款要素、2025数据 | Step 1-2 确认类型风格阶段 |
| `references/structure-templates.md` | 60-120集黄金结构、真人/漫剧分镜模板 | Step 4 大纲设计阶段 |
| `references/writing-skills.md` | 爽点公式、钩子设计、标题封面、避坑指南 | Step 5 创作阶段 |
| `references/manga-guide.md` | AI漫剧画风体系、套路库、人物一致性规范 | 漫剧创作必读 |
| `references/production-process.md` | 对标→创作→运营工业化流程 | 批量生产阶段 |
| `examples/hook-templates.md` | 100+爆款钩子模板（开篇3秒/每集结尾） | Step 6 钩子设计阶段 |
| `examples/case-studies.md` | 4个头部爆款深度拆解 | 学习参考 |
| `examples/demo-script.md` | 完整真人短剧示例剧本（第1集） | 格式参考 |
| `examples/manga_example_ep1.md` | 完整AI漫剧示例剧本（含角色库+分镜） | 漫剧格式参考 |
| `examples/nanpin_example.md` | 男频题材完整示例 | 男频参考 |
| `examples/nvpin_example.md` | 女频题材完整示例 | 女频参考 |

---

## ViFlow JSON 导出说明

剧本创作完成后，同步导出 ViFlow v1.2 格式 JSON，导入 ViFlow.app 分镜工程使用。

### 核心 Schema（完整规范见 `assets/output/viflow_schema.json`）

```json
{
  "version": "1.2",
  "exportMeta": {
    "exportedAt": "<ISO时间>",
    "exportedProjectName": "<剧目标题>",
    "sourceApp": "viflow2026",
    "sourceVersion": "1.2"
  },
  "project": {
    "name": "<剧目标题>",
    "description": "<一句话简介>",
    "current_step": "storyboard",
    "idea_content": "<200-500字故事大纲>",
    "outline_content": "<四幕结构章节概述>",
    "visualStyle": "<画风声明：国漫古风/日漫画风/韩漫/写实3D等>"
  },
  "scriptParts": [
    { "title": "Part 1 - 钩子期", "content": "...", "order": 0, "emotion": "紧张", "estimatedDuration": 90, "shotSuggestion": 5 }
  ],
  "characters": [
    {
      "id": "char-uuid-1", "name": "<姓名>", "type": "real",
      "description": "<详细描述（供AI生成一致形象）>",
      "imagePrompt": "<AI绘图Prompt（英文）>",
      "positioning": "居中|左侧|右侧", "tags": ["主角"], "isReference": true
    }
  ],
  "props": [
    { "id": "prop-uuid-1", "name": "<道具名>", "category": "prop", "description": "...", "imagePrompt": "...", "isReference": true }
  ],
  "scenes": [
    {
      "id": "scene-uuid-1", "name": "<场景名>", "type": "interior|exterior",
      "description": "<场景描述>", "imagePrompt": "<AI绘图Prompt>",
      "time_period": "日|夜|晨|暮"
    }
  ],
  "shots": [
    {
      "id": "shot-uuid-1", "partId": "<关联part的ID>",
      "sceneDescription": "<可给AI视频生成的完整画面描述>",
      "dialogue": "<对话，不超过30字>",
      "cameraMovement": "static|dolly_in|dolly_out|pan_left|pan_right|tilt_up|tilt_down|tracking",
      "duration": 5, "videoPrompt": "<AI视频生成Prompt（英文）>",
      "status": "draft", "shotNumber": 1
    }
  ]
}
```

> 📌 **所有生成剧本必须同步导出 JSON**，否则输出不完整。
> 导出后可在 ViFlow.app 中导入使用。

---

## AI 漫剧创作补充规范

漫剧创作除上述流程外，还需额外执行：

1. **画风声明**：在剧本开头注明 visualStyle + 色调基调 + 主角固定特征
2. **人物一致性**：每集人物外观描述必须与角色库一致，避免 AI 生成飘移
3. **固定特征模板**：
   ```
   角色名固定特征：
   - 年龄/性别
   - 标志性发型/服装
   - 特殊标记（伤疤/配饰）
   - 常用表情/动作
   ```
4. **漫剧套路参考**：见 `references/manga-guide.md`

---

## 快速参考（内嵌）

**爆款核心数据：**
- 短剧+AI漫剧整体市场：**750亿+**
- AI漫剧生产成本：仅为真人短剧的 **15%**
- 爆款集数区间：**60-120集**，单集 **1-3分钟**
- 女频占爆款市场：**80%** 份额
- 前3秒留存率权重：**40%**（必须有强冲突）
- 完播率标准：真人 ≥40%，AI漫剧 ≥45%

**cameraMovement 速查：**
`static`（固定）| `dolly_in`（推进）| `dolly_out`（拉远）| `pan_left/right`（摇镜）| `tilt_up/down`（俯仰）| `tracking`（跟拍）

**visualStyle 速查：**
`国漫古风` | `国漫现代` | `日漫画风` | `韩漫风格` | `写实3D` | `Q版可爱`

---

*MIT-0 License*
