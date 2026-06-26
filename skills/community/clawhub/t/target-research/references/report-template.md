# HTML 报告模板 + 质量检查清单

## 报告模板

**设计原则：**
- 内容优先，排版简洁，信息密度高
- 不用卡片、KPI网格、评分条等装饰性组件
- 以段落论述为主，表格用于结构化数据，列表仅用于枚举
- 每个章节内容必须充实详细，有分析、有论证、有数据支撑
- 一页多信息，而非一页一个概念

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{靶点名称}（{基因符号}）靶点深度调研报告</title>
<style>
:root {
  --bg: #ffffff;
  --text: #1a1a1a;
  --muted: #666666;
  --accent: #1a56db;
  --accent2: #7c3aed;
  --red: #dc2626;
  --orange: #d97706;
  --green: #059669;
  --border: #e5e7eb;
  --highlight-bg: #fef3c7;
  --tag-green-bg: #d1fae5; --tag-green-fg: #065f46;
  --tag-red-bg: #fee2e2; --tag-red-fg: #991b1b;
  --tag-orange-bg: #fef3c7; --tag-orange-fg: #92400e;
  --tag-blue-bg: #dbeafe; --tag-blue-fg: #1e40af;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: "Noto Sans SC", "Source Han Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
  background: var(--bg);
  color: var(--text);
  font-size: 14px;
  line-height: 1.8;
  max-width: 820px;
  margin: 0 auto;
  padding: 40px 32px;
}

/* 封面 */
.cover {
  border-bottom: 3px solid var(--accent);
  padding-bottom: 20px;
  margin-bottom: 32px;
}
.cover h1 {
  font-size: 2em;
  color: var(--text);
  margin-bottom: 4px;
  font-weight: 700;
}
.cover .subtitle {
  font-size: 1em;
  color: var(--muted);
  margin-bottom: 16px;
}
.cover .summary-row {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  font-size: 0.95em;
  color: var(--muted);
}
.cover .summary-row strong {
  color: var(--text);
}

/* 标题 */
h2 {
  font-size: 1.4em;
  color: var(--accent);
  margin: 36px 0 12px;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--border);
  font-weight: 700;
}
h3 {
  font-size: 1.1em;
  color: var(--text);
  margin: 20px 0 8px;
  font-weight: 600;
}

/* 段落 */
p {
  margin: 8px 0;
  text-align: justify;
}

/* 表格 */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
  font-size: 0.9em;
}
th {
  background: #f3f4f6;
  color: var(--text);
  padding: 8px 12px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid var(--border);
  white-space: nowrap;
}
td {
  padding: 6px 12px;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
}

/* 标签 */
.tag {
  display: inline-block;
  padding: 1px 8px;
  border-radius: 3px;
  font-size: 0.85em;
  font-weight: 600;
}
.tag-green { background: var(--tag-green-bg); color: var(--tag-green-fg); }
.tag-red { background: var(--tag-red-bg); color: var(--tag-red-fg); }
.tag-orange { background: var(--tag-orange-bg); color: var(--tag-orange-fg); }
.tag-blue { background: var(--tag-blue-bg); color: var(--tag-blue-fg); }

/* 列表 */
ul, ol {
  padding-left: 20px;
  margin: 8px 0;
}
li {
  margin: 3px 0;
}

/* 强调 */
.highlight {
  background: var(--highlight-bg);
  padding: 1px 6px;
  border-radius: 2px;
}
.warning { color: var(--orange); font-weight: 600; }
.danger { color: var(--red); font-weight: 600; }
.success { color: var(--green); font-weight: 600; }

/* SWOT（简洁2×2表格，不用网格卡片） */
.swot-table {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
}
.swot-table th, .swot-table td {
  border: 1px solid var(--border);
  padding: 10px 14px;
  vertical-align: top;
  font-size: 0.9em;
}
.swot-table th {
  width: 50%;
  font-weight: 600;
  text-align: center;
}
.swot-table td ul { margin: 4px 0; }

/* 引用块 */
blockquote {
  border-left: 3px solid var(--accent);
  padding: 8px 16px;
  margin: 12px 0;
  background: #f9fafb;
  font-size: 0.95em;
  color: var(--muted);
}

/* 页脚 */
.footer {
  text-align: center;
  color: var(--muted);
  font-size: 0.8em;
  margin-top: 40px;
  padding-top: 16px;
  border-top: 1px solid var(--border);
}

/* 打印优化 */
@media print {
  body { padding: 20px; max-width: none; }
  h2 { page-break-before: auto; }
}
</style>
</head>
<body>

<!-- 封面 -->
<div class="cover">
  <h1>{靶点名称}（{基因符号}）</h1>
  <div class="subtitle">小分子新药靶点深度调研报告 | {UniProt ID} | {蛋白类型}</div>
  <div class="summary-row">
    <span>靶点价值：<strong>{N}/10</strong></span>
    <span>专利拥挤度：<strong>{N}/10</strong></span>
    <span>小分子起点：<strong>{✅/❌}</strong></span>
    <span>晶体结构：<strong>{✅/❌}</strong></span>
    <span>报告日期：<strong>{YYYY-MM-DD}</strong></span>
  </div>
</div>

<!-- 各章节按 <h2> 标题依次展开 -->
<!-- 每个章节必须以段落论述为主，辅以表格和列表 -->
<!-- 不要使用卡片、KPI网格等装饰性组件 -->
<!-- 内容要充实详细，每个观点都要有数据或文献支撑 -->

<!-- 第一章：靶点概述与生物学基础 -->
<!-- 第二章：成药性评估 -->
<!-- 第三章：适应症格局 -->
<!-- 第四章：竞争格局深度分析 -->
<!-- 第五章：专利态势分析 -->
<!-- 第六章：同源靶点与选择性 -->
<!-- 第七章：安全性评估 -->
<!-- 第八章：前沿动态与机会 -->
<!-- 第九章：高引文献推荐 -->
<!-- 第十章：综合评估与策略建议 -->

</body>
</html>
```

## 内容要求（必须遵守）

### 核心原则：内容充实 > 排版美观

1. **每个章节必须有充实的段落论述**，不能只有表格和列表。每个关键观点都要展开分析，解释"为什么"，引用具体数据或文献。
2. **段落长度**：每个核心论点至少2-3句话的展开论述，不能一句话带过。
3. **数据必须具体**：不能只说"有PDB结构"，要写出具体PDB ID、分辨率、配体名称；不能只说"有临床药物"，要写出药物名、公司、阶段、机制。
4. **分析要有深度**：不能只罗列事实，要分析意义、影响、趋势。例如"PRDM1突变在DLBCL中频繁出现"后面要跟"这意味着恢复PRDM1功能可能是DLBCL的分化治疗策略"。
5. **表格用于结构化数据**（如药物列表、PDB列表、同源物列表），段落用于分析和论述。
6. **不用**：卡片(.card)、KPI网格(.kpi-grid)、评分条(.score-bar)等装饰性组件。
7. **SWOT用2×2表格**，不用四色网格卡片。
8. **封面简洁**：一行标题+一行副标题+一行关键指标，不要大号居中装饰。

### 每章最低内容量

| 章节 | 最低段落论述量 | 必含内容 |
|------|--------------|---------|
| 一、靶点概述 | ≥8段 | 身份卡表格、核心功能（每项2-3句展开）、通路文字描述（含上下游）、组织表达、疾病关联证据链 |
| 二、成药性评估 | ≥8段 | CRO assay详细分析、结构可靶向性论述、PDB结构评价、成药性评分理由、小分子策略对比分析 |
| 三、适应症格局 | ≥6段 | 每个核心适应症需2-3段论述（疾病背景+干预逻辑+证据+市场）、拓展适应症分析、罕见病机会 |
| 四、竞争格局 | ≥8段 | 全局态势分析、每个药物2-3段详析（含特征点评）、每个公司1-2段画像、差异化策略四维分析 |
| 五、专利态势 | ≥4段 | 专利全景、核心专利拆解、FTO评估、拥挤度评分依据 |
| 六、同源选择性 | ≥4段 | 家族图谱表格、选择性挑战论述、脱靶风险分析 |
| 七、安全性评估 | ≥6段 | On-target分系统论述、Off-target分析、KO表型、临床AE、安全策略 |
| 八、前沿动态 | ≥4段 | 2024-2025进展、耐药机制、新技术方向、机会窗口 |
| 九、高引文献 | 表格+论述 | 5-10篇文献表格、主题分布分析、阅读优先级建议 |
| 十、综合评估 | ≥6段 | 评分各维度论述、SWOT表格、立项建议+理由、里程碑建议 |

## 质量检查清单

报告生成后逐项核验：

### 数据完整性
- [ ] 靶点基础信息（UniProt ID、分子量、定位）已填写
- [ ] 结构信息（PDB数量、共晶情况）已填写，PDB ID具体到编号
- [ ] CRO Assay 可及性评估已完成（生化/细胞 assay 类型、丰富度评级）
- [ ] 成药性评分已给出并解释理由
- [ ] 至少3个适应症已列出并附证据等级
- [ ] 竞争格局中每个药物有"特征点评"
- [ ] 竞争格局中每个公司有"竞争力评价"
- [ ] 差异化策略方向已分析（机制、适应症、分子设计、临床策略四维）
- [ ] 差异化策略推荐矩阵已给出
- [ ] 专利拥挤度评分（1-10）已给出
- [ ] On-target 和 Off-target 毒性已分开讨论
- [ ] 每项安全性风险已标注等级
- [ ] 高引文献 5-10 篇已列出，含标题、期刊、引用数、推荐理由
- [ ] 高引文献覆盖至少3个主题维度

### 内容充实度（新增重点！）
- [ ] 每个章节有充实的段落论述，不是只有表格/列表
- [ ] 关键观点都有"为什么"的分析，不是只陈述结论
- [ ] 数据具体（PDB ID、药物名、公司名、临床阶段），不是模糊描述
- [ ] 分析有深度，有趋势判断和策略含义
- [ ] 不使用卡片、KPI网格、评分条等装饰性组件
- [ ] SWOT用2×2表格而非四色网格
- [ ] 封面简洁，非大号居中装饰

### 分析质量
- [ ] "是否有小分子起点"有明确回答及理由
- [ ] "是否有晶体结构"有明确回答
- [ ] 通路关系已描述
- [ ] 同源靶点选择性挑战已分析
- [ ] CRO Assay 对项目启动的影响已评估
- [ ] SWOT 四象限完整
- [ ] 靶点价值评分各维度分数已列出
- [ ] 立项建议（推荐/有条件推荐/不推荐）已给出
- [ ] 差异化策略有明确优先级推荐
- [ ] 高引文献阅读优先级建议已给出

### 格式规范
- [ ] HTML 文件可正常打开，无渲染错误
- [ ] 白底深色文字，专业文档风格
- [ ] 无乱码或编码问题
- [ ] 打印友好

### 摘要输出
- [ ] 结构化摘要已按 SKILL.md Step 6 模板输出
- [ ] 靶点价值评分、专利拥挤度、小分子起点、晶体结构、Assay丰富度5项关键指标已包含
- [ ] 差异化策略推荐已包含
- [ ] 高引文献 Top 3 已包含