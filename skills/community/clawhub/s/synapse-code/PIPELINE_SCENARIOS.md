# Synapse Code Pipeline 场景扩展设计

## 场景分类

当前 Pipeline 设计过于聚焦**纯开发场景**，需要扩展到更多用户场景。

### 场景分类矩阵

| 场景类型 | 典型任务 | 需求特点 | 流程特点 |
|---------|---------|---------|---------|
| **代码开发** | 实现登录功能、修复 bug | 明确的功能需求 | 需要测试、验收 |
| **文案写作** | 公众号文章、营销文案 | 风格要求、字数限制 | 需要多轮修改 |
| **设计创作** | UI 设计、logo 设计 | 审美要求、品牌规范 | 需要视觉输出 |
| **数据分析** | 销售报表、用户分析 | 数据源、分析维度 | 需要可视化 |
| **翻译本地化** | 文档翻译、字幕翻译 | 专业术语、语境 | 需要校对 |
| **学习研究** | 文献调研、竞品分析 | 信息来源、分析框架 | 需要结构化输出 |

---

## 各场景 Pipeline 设计

### 场景 A：文案写作 Pipeline

```
用户 → 你（文案主编）
         ↓
    ┌────┼────┬────────┐
    ↓    ↓    ↓        ↓
  选题   大纲  初稿     润色
  策划   策划  写作     编辑
    ↓    ↓    ↓        ↓
    └────┴────┴────────┘
              ↓
         成品交付
```

**Agent 角色**：
- **主编**（Orchestrator）— 统筹整体方向
- **选题策划** — 分析受众、确定角度
- **大纲策划** — 搭建文章结构
- **写作者** — 撰写初稿
- **编辑** — 润色、校对、优化

**适用任务**：
- "写一篇公众号文章，介绍 AI 编程技巧"
- "写个产品发布新闻稿"
- "写一封给投资人的邮件"

---

### 场景 B：设计创作 Pipeline

```
用户 → 你（设计总监）
         ↓
    ┌────┼────┬────────┐
    ↓    ↓    ↓        ↓
  需求   竞品  草图     终稿
  分析   调研  设计     输出
    ↓    ↓    ↓        ↓
    └────┴────┴────────┘
              ↓
         成品交付
```

**Agent 角色**：
- **设计总监**（Orchestrator）— 把握整体风格
- **需求分析师** — 理解使用场景、目标用户
- **竞品分析师** — 调研同类设计
- **设计师** — 输出设计方案
- **审核员** — 检查品牌规范、可访问性

**适用任务**：
- "设计一个 logo，要简约现代"
- " redesign 这个 landing page"
- "做个信息图表，展示销售数据"

---

### 场景 C：数据分析 Pipeline

```
用户 → 你（分析总监）
         ↓
    ┌────┼────┬────────┐
    ↓    ↓    ↓        ↓
  数据   清洗  分析     报告
  收集   整理  建模     可视化
    ↓    ↓    ↓        ↓
    └────┴────┴────────┘
              ↓
         成品交付
```

**Agent 角色**：
- **分析总监**（Orchestrator）— 确定分析框架
- **数据工程师** — 收集、清洗数据
- **数据分析师** — 统计分析、建模
- **可视化专家** — 制作图表、dashboard
- **报告撰写** — 撰写分析报告

**适用任务**：
- "分析上季度的销售数据"
- "做个用户行为分析报告"
- "对比我们和竞品的市场份额"

---

### 场景 D：翻译本地化 Pipeline

```
用户 → 你（翻译总监）
         ↓
    ┌────┼────┬────────┐
    ↓    ↓    ↓        ↓
  术语   翻译  校对     本地化
  整理   初稿  润色     适配
    ↓    ↓    ↓        ↓
    └────┴────┴────────┘
              ↓
         成品交付
```

**Agent 角色**：
- **翻译总监**（Orchestrator）— 把控整体质量
- **术语专家** — 整理专业术语表
- **翻译员** — 初稿翻译
- **校对员** — 检查准确性、流畅度
- **本地化专家** — 适配目标语言文化

**适用任务**：
- "翻译这个技术文档到英文"
- "把这篇论文翻译成中文"
- "本地化这个 App 的 UI 文案"

---

### 场景 E：学习研究 Pipeline

```
用户 → 你（研究主管）
         ↓
    ┌────┼────┬────────┐
    ↓    ↓    ↓        ↓
  文献   阅读  提炼     报告
  搜集   整理  总结     综合
    ↓    ↓    ↓        ↓
    └────┴────┴────────┘
              ↓
         成品交付
```

**Agent 角色**：
- **研究主管**（Orchestrator）— 确定研究框架
- **文献搜集员** — 查找相关资料
- **阅读分析师** — 阅读理解、提取要点
- **知识整理师** — 结构化整理
- **报告撰写** — 综合研究报告

**适用任务**：
- "调研一下 RAG 技术的最新进展"
- "分析一下 AI 编程助手的市场格局"
- "学习一下 Karpathy 的 LLM Wiki 模式"

---

## 统一场景识别

### 场景自动检测

```python
def detect_scenario(user_input: str) -> str:
    """根据用户输入自动识别场景"""
    
    # 代码开发关键词
    if any(kw in user_input for kw in ["代码", "开发", "实现", "功能", "bug", "接口", "API"]):
        return "development"
    
    # 文案写作关键词
    if any(kw in user_input for kw in ["文章", "文案", "写", "公众号", "邮件", "稿"]):
        return "writing"
    
    # 设计创作关键词
    if any(kw in user_input for kw in ["设计", "logo", "UI", "图", "视觉", "排版"]):
        return "design"
    
    # 数据分析关键词
    if any(kw in user_input for kw in ["数据", "分析", "报表", "图表", "可视化"]):
        return "analytics"
    
    # 翻译关键词
    if any(kw in user_input for kw in ["翻译", "译成", "本地化", "英文版"]):
        return "translation"
    
    # 学习研究关键词
    if any(kw in user_input for kw in ["调研", "研究", "学习", "了解", "分析", "进展"]):
        return "research"
    
    # 默认使用开发场景
    return "development"
```

---

## 场景配置示例

### config.json 配置

```json
{
  "synapse": {
    "pipeline": {
      "default_scenario": "auto",
      "scenarios": {
        "development": {
          "name": "代码开发",
          "agents": ["req-analyst", "architect", "developer", "qa-engineer"],
          "default_mode": "lite"
        },
        "writing": {
          "name": "文案写作",
          "agents": ["topic-planner", "outline-planner", "writer", "editor"],
          "default_mode": "lite"
        },
        "design": {
          "name": "设计创作",
          "agents": ["requirement-analyst", "researcher", "designer", "reviewer"],
          "default_mode": "lite"
        },
        "analytics": {
          "name": "数据分析",
          "agents": ["data-engineer", "analyst", "visualization-expert", "report-writer"],
          "default_mode": "lite"
        },
        "translation": {
          "name": "翻译本地化",
          "agents": ["terminology-expert", "translator", "proofreader", "localization-expert"],
          "default_mode": "lite"
        },
        "research": {
          "name": "学习研究",
          "agents": ["researcher", "analyst", "synthesizer", "report-writer"],
          "default_mode": "lite"
        }
      }
    }
  }
}
```

---

## 用户交互设计

### 场景提示

```
用户：/synapse-code run my-project "写一篇公众号文章，介绍 AI 编程技巧"

Synapse: 📝 检测到**文案写作场景**
       使用轻量模式（4 阶段）
       
       [1/4] 选题策划：分析受众...
       [2/4] 大纲策划：搭建结构...
       [3/4] 文案写作：撰写初稿...
       [4/4] 编辑润色：优化文案...
       
       ✅ 完成！公众号文章已撰写
       
       📊 执行报告:
       - 标题：AI 编程技巧入门
       - 字数：2500 字
       - 风格：技术科普
```

### 场景手动指定

```
用户：/synapse-code run my-project "分析一下 Q3 销售数据" --scenario analytics

Synapse: 📊 数据分析场景
       使用轻量模式（4 阶段）
       
       [1/4] 数据收集：获取 Q3 数据...
       [2/4] 数据清洗：整理格式...
       [3/4] 数据分析：统计分析...
       [4/4] 可视化：制作图表...
       
       ✅ 完成！销售分析报告已生成
```

---

## 跨场景协作

某些任务需要多个场景协作：

### 示例：产品发布

```
用户："产品发布，需要：
      1. 写发布新闻稿
      2. 设计宣传海报
      3. 开发 landing page
      4. 分析预热数据"

Synapse: 🎯 检测到**复合型任务**
       启动多场景协作模式
       
       📦 场景 A (文案): 新闻稿撰写中...
       📦 场景 B (设计): 海报设计中...
       📦 场景 C (开发): Landing Page 开发中...
       📦 场景 D (分析): 数据监测中...
       
       ✅ 全部完成！共交付 4 项成果
```

---

## 下一步行动

1. **创建各场景 Agent 模板**
   - writing/: 选题策划、大纲策划、写作者、编辑
   - design/: 需求分析、竞品分析、设计师、审核员
   - analytics/: 数据工程师、分析师、可视化专家、报告撰写
   - translation/: 术语专家、翻译员、校对员、本地化专家
   - research/: 研究员、分析师、知识整理师、报告撰写

2. **更新 orchestrator.md**
   - 添加场景识别逻辑
   - 添加各场景执行流程

3. **更新 UI/UX**
   - 场景选择器
   - 场景进度展示
   - 场景专属输出格式
