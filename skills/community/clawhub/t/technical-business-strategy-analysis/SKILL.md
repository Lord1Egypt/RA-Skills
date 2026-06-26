---
name: business-strategy-analysis
description: "专业级商业战略分析：从市场规模估算到可执行洞察的完整工作流。支持 TAM/SAM/SOM、竞品矩阵、SWOT+、Porter 五力、商业模式画布等专业框架。"
homepage: https://github.com/vincentlau2046-sudo/business-strategy-analysis
metadata: {"clawdbot":{"emoji":"📊"}}
---

# Business Strategy Analysis

完整的商业战略分析工作流，从市场研究到战略洞察。

## 工作流步骤

### 1. 问题定义与范围界定
- **输入**: 行业/产品关键词、地理范围、时间范围
- **输出**: 分析范围文档 + 关键假设列表
- **工具**: Tavily 搜索 API 获取行业背景

### 2. 市场规模估算 (TAM/SAM/SOM)
- **输入**: 行业关键词、地理范围、时间维度
- **数据源**: Tavily 搜索 + 统计数据库 + 行业报告
- **量化要求**:
  - 所有市场规模数据必须包含具体数值（单位：美元/人民币/用户数等）
  - 提供置信区间（95% CI）或数据可靠性评分（1-5分）
  - 历史数据至少包含过去3年，预测数据至少包含未来5年
  - 市场增长率必须计算复合年增长率（CAGR）并标注标准差
- **输出**: 
  - 市场规模数据表格（含历史数据、预测、置信区间）
  - TAM/SAM/SOM 可视化图表（带误差线）
  - 市场增长率分析（含CAGR和波动性指标）

### 3. 竞品矩阵分析  
- **输入**: 竞品列表、评估维度（价格、功能、市场份额等）
- **数据源**: 公司财报、产品文档、用户评论、新闻报道
- **量化要求**: 
  - 市场份额必须提供具体百分比数值（如：NVIDIA 80%，AMD 15%）
  - 价格对比需提供具体美元数值和相对差异百分比
  - 功能评分采用 1-10 分制，附置信区间（如：8.5±0.3）
  - 对无法量化的维度明确标注为"定性分析"
- **输出**: 
  - 2x2 竞争矩阵图（坐标轴需有具体数值刻度）
  - 详细竞品对比表格（包含量化数据和置信区间）
  - 竞争优势/劣势分析（量化影响程度：高/中/低 + 具体数值支撑）

### 4. SWOT+ 分析
- **输入**: 公司/产品信息、市场环境
- **处理**: 
  - 自动识别 Strengths/Weaknesses/Opportunities/Threats
  - **量化评分**：每个要素按 1-5 分制评分，并提供置信区间（如：3.2±0.5）
  - **定性分析标注**：对无法量化的软性因素明确标注为"定性分析"
  - 生成 TOWS 战略矩阵，包含具体数值支撑
- **输出**: 
  - SWOT 矩阵可视化（含评分和置信区间）
  - 战略建议（SO/WO/ST/WT 策略）带优先级分数（0-100）
  - 优先级排序（基于量化权重计算）

### 5. Porter 五力模型（量化+定性）
- **输入**: 行业信息、供应链数据
- **处理**: 
  - 供应商议价能力分析（量化：供应商集中度CR4/HHI指数、转换成本美元数值）
  - 购买者议价能力分析（量化：客户集中度、价格敏感度弹性系数）
  - 新进入者威胁分析（量化：资本需求金额、规模经济门槛、品牌忠诚度百分比）
  - 替代品威胁分析（量化：替代品价格差异%、性能差距分数、转换成本）
  - 现有竞争者竞争强度分析（量化：行业利润率%、产能利用率%、广告支出占比%）
  - 行业生命周期阶段判断（基于增长率CAGR和市场渗透率%）
  - **定性分析标注**：对无法量化的制度性、文化性因素明确标注为"定性分析"
- **量化要求**：
  - 每个力量按 1-5 分制评分威胁/强度级别，附置信区间
  - 行业吸引力综合评分 = 加权平均（权重基于行业特性自动计算）
  - 所有量化数据必须标注数据来源和时间戳
- **输出**: 
  - 五力雷达图（含具体数值和置信区间）
  - 行业吸引力综合评分（0-100分）及置信区间
  - 关键成功因素识别（按重要性排序 + 量化影响程度）

### 6. 商业模式拆解（量化+定性）
- **输入**: 商业模式描述、收入来源
- **处理**: 
  - Business Model Canvas 九要素分析（每个要素评分1-5分，置信区间80%）
  - 盈利引擎和成本结构分析（量化：毛利率、运营利润率、客户生命周期价值LTV、获客成本CAC等具体数值）
  - 客户获取和留存策略（量化：转化率、留存率、流失率等指标）
- **输出**: 
  - 商业模式画布可视化（含量化评分）
  - 盈利模式优化建议（含预期ROI和实施成本估算）
  - 风险点和改进机会（按风险概率和影响程度量化评估）
  - 对无法量化的战略要素明确标注为"定性分析"

### 7. 洞察报告生成
- **整合**: 所有分析结果 + 执行摘要
- **输出**: 
  - 结构化 Markdown 报告（含数据源引用）
  - 调用 ppt-generator 技能生成乔布斯风极简科技感演示文稿
  - 关键洞察卡片（便于分享）

## 输出文件结构

所有分析结果自动保存到：

```
~/.openclaw/workspace/tech-insight/business-strategy-analysis/{主题}/
├── strategy-report.md      # 完整分析报告（含数据源引用）
├── presentation.html       # 交互式可视化演示文稿
├── data/                   # 原始数据和中间结果
│   ├── market-size.csv     # 市场规模数据
│   ├── competitors.csv     # 竞品数据
│   └── swot-analysis.json  # SWOT 分析数据
└── sources.md              # 数据源和参考文献
```

**示例**：
- OpenRouter 分析 → `tech-insight/business-strategy-analysis/openrouter/`
- Palantir 分析 → `tech-insight/business-strategy-analysis/palantir/`

## 行业专业化模板

系统内置四个行业专业化模板，针对不同行业的关键指标和分析维度进行优化：

### 1. AI Infra 模板
- **适用场景**: AI芯片、云计算基础设施、GPU/TPU硬件、AI平台
- **核心指标**: 
  - 芯片性能（TFLOPS、内存带宽、能效比 TOPS/W）
  - 软件生态（框架支持度、开发者数量、文档质量）
  - 客户案例（头部客户、部署规模、ROI数据）
  - 供应链安全（制造工艺、地缘政治风险）

### 2. SaaS 模板  
- **适用场景**: 软件即服务、B2B软件、订阅制产品
- **核心指标**:
  - ARR/MRR（年度/月度经常性收入）
  - 获客成本（CAC）和客户生命周期价值（LTV）
  - 留存率（净留存率、毛利率留存率）
  - 功能矩阵（竞品功能对比、差异化程度）

### 3. AI Agent 模板
- **适用场景**: AI代理、自动化工作流、智能助手
- **核心指标**:
  - 能力矩阵（多轮对话、工具调用、推理能力评分）
  - 工具集成（支持的API数量、集成复杂度）
  - 多模态支持（文本、图像、语音、视频处理能力）
  - 部署复杂度（硬件要求、运维成本、扩展性）

### 4. 消费品模板
- **适用场景**: 快消品、零售、品牌消费品
- **核心指标**:
  - 品牌价值（Brand Finance评分、社交媒体声量）
  - 渠道分析（线上/线下占比、渠道利润率、覆盖密度）
  - 消费者行为（购买频率、客单价、NPS净推荐值）
  - 供应链（库存周转率、物流成本、供应商集中度）

### 5. AI 软件模板
- **适用场景**: AI开发框架、机器学习平台、AI模型服务、MLOps工具
- **核心指标**:
  - 技术栈完整性（支持的框架数量、API丰富度、SDK覆盖度）
  - 开发者生态（GitHub stars、社区活跃度、文档质量、教程数量）
  - 模型性能（推理延迟、吞吐量、准确率基准、资源利用率）
  - 企业采用度（头部客户数量、生产环境部署案例、合规认证）
  - 商业模式（开源vs闭源、定价策略、企业支持服务）

模板文件位置：`~/.openclaw/workspace/skills/business-strategy-analysis/templates/`

## 使用示例

```
用户: 分析 AI 芯片市场 (自动使用 AI Infra 模板)
用户: 对比 NVIDIA 和 AMD 的竞争格局 (自动使用 AI Infra 模板)  
用户: 生成 Tesla 的 SWOT 分析 (自动使用消费品模板)
用户: 创建我们的 SaaS 商业模式画布 (自动使用 SaaS 模板)
用户: 评估 AI Agent 平台的投资机会 (自动使用 AI Agent 模板)
用户: 分析可口可乐的市场地位 (自动使用消费品模板)
```

## 自动执行流程

当触发分析时，系统会：

1. **创建标准化输出目录（绝对路径）**
   ```bash
   # 设置工作目录
   cd /home/Vincent/.openclaw/workspace/
   
   # 创建输出目录（绝对路径）
   OUTPUT_DIR="/home/Vincent/.openclaw/workspace/tech-insight/business-strategy-analysis/{主题}"
   mkdir -p "$OUTPUT_DIR"
   mkdir -p "$OUTPUT_DIR/data"
   
   # 验证目录创建成功
   if [ ! -d "$OUTPUT_DIR" ]; then
       echo "Error: Failed to create output directory"
       exit 1
   fi
   ```

2. **执行针对性数据提取策略**
   - **市场规模估算**: 优先从 Statista、IBISWorld、政府统计局获取权威数据；使用 Yahoo Finance 获取上市公司财报数据
   - **竞品分析**: 从 Crunchbase 获取公司基本信息；从官方产品文档和 MLPerf 等基准测试获取技术指标；从 SEC EDGAR 获取财务数据
   - **SWOT/Porter 分析**: 综合新闻报道、学术论文、行业报告进行多维度分析
   - **商业模式分析**: 从公司官网、投资者关系页面、S-1 文件获取详细商业模式信息
   
3. **执行完整分析工作流**
   - 并行收集多源数据（Tavily API 域名白名单过滤 + 公开数据库直接访问）
   - 应用专业分析框架
   - 生成量化洞察和可视化

3. **保存结构化输出并生成演示文稿**
   ```bash
   # 保存完整报告
   write ~/.openclaw/workspace/tech-insight/business-strategy-analysis/{主题}/strategy-report.md
   
   # 保存原始数据
   write ~/.openclaw/workspace/tech-insight/business-strategy-analysis/{主题}/data/*.csv
   
   # 记录数据源
   write ~/.openclaw/workspace/tech-insight/business-strategy-analysis/{主题}/sources.md
   
   # 调用 ppt-generator 技能生成乔布斯风演示文稿
   # 基于 strategy-report.md 内容生成 presentation.html
   ```
   
4. **返回结果摘要**
   - 在对话中显示关键洞察（3-5个要点）
   - 提供完整文件路径
   - 演示文稿已通过 ppt-generator 技能生成并保存为 presentation.html
   - 支持后续深入查询

## 数据源配置

### Tavily API 域名白名单配置
为确保数据质量和权威性，已配置以下域名白名单：

**金融/市场数据源**:
- `finance.yahoo.com` (Yahoo Finance)
- `sec.gov` (SEC EDGAR)
- `statista.com` (Statista 公开数据)
- `ibisworld.com` (IBISWorld 行业报告)
- `marketwatch.com` (MarketWatch)

**技术指标数据源**:
- `mlperf.org` (MLPerf 官方基准)
- `arxiv.org` (学术论文预印本)
- `paperswithcode.com` (官方基准和代码)
- `techcrunch.com` (技术新闻和分析)
- `official company websites` (公司官网技术文档)

**公司信息数据源**:
- `crunchbase.com` (Crunchbase 公司数据库)
- `linkedin.com` (LinkedIn 公司页面)
- `official company websites` (公司官网投资者关系页面)
- `bloomberg.com` (Bloomberg 公司信息)
- `reuters.com` (Reuters 公司新闻)

配置命令：
```bash
mkdir -p ~/.config/business-strategy-analysis
echo "tvly-YOUR_API_KEY" > ~/.config/business-strategy-analysis/tavily_key

# 配置域名白名单（用于Tavily搜索的include_domains参数）
cat > ~/.config/business-strategy-analysis/tavily_domains.json << EOF
{
  "financial": ["finance.yahoo.com", "sec.gov", "statista.com", "ibisworld.com", "marketwatch.com"],
  "technical": ["mlperf.org", "arxiv.org", "paperswithcode.com", "techcrunch.com"],
  "company": ["crunchbase.com", "linkedin.com", "bloomberg.com", "reuters.com"]
}
EOF
```

### 针对性数据提取策略

**市场规模估算 (TAM/SAM/SOM)**:
- 优先搜索：Statista, IBISWorld, Yahoo Finance
- 关键词策略："[行业] market size", "[行业] TAM SAM SOM", "[行业] growth rate CAGR"
- 数据验证：交叉验证至少3个独立来源

**竞品矩阵分析**:
- 金融数据：Yahoo Finance, SEC EDGAR (财报数据)
- 技术数据：MLPerf, Papers with Code, 官方技术文档
- 市场份额：Statista, Crunchbase, 行业报告
- 关键词策略："[公司] market share", "[产品] benchmark", "[竞品] comparison"

**SWOT+ 分析**:
- 优势/劣势：公司财报、技术文档、专利数据库
- 机会/威胁：行业报告、新闻分析、政策文件
- 关键词策略："[公司] SWOT", "[行业] trends", "[市场] opportunities threats"

**Porter 五力模型**:
- 供应商议价能力：供应链报告、行业集中度数据
- 购买者议价能力：客户集中度、价格弹性研究
- 新进入者威胁：资本需求、监管门槛、规模经济数据
- 替代品威胁：技术替代分析、价格性能比较
- 竞争强度：行业利润率、产能利用率、广告支出数据

**商业模式拆解**:
- 收入模式：财报收入细分、定价策略文档
- 成本结构：财报成本分析、运营效率指标
- 客户获取：营销支出、CAC计算、渠道分析
- 关键词策略："[公司] business model", "[产品] revenue model", "[服务] pricing strategy"

## 配置选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `output_format` | `both` | `markdown` \| `html` \| `both` |
| `competitor_count` | 5 | 竞品分析数量（3-10）|
| `geographic_scope` | `global` | `local` \| `regional` \| `global` |
| `time_horizon` | `5_years` | `current` \| `3_years` \| `5_years` \| `10_years` |
| `quantification_level` | `strict` | `strict` (强制量化) \| `balanced` (量化+定性) |

## 错误处理和降级策略

- **数据不足**: 
  - 切换到备用数据源
  - 提供基于有限数据的分析 + 置信度评分
  - 建议补充数据收集方法

- **API 限制**: 
  - 自动指数退避重试
  - 使用缓存数据进行部分分析
  - 分批处理大型请求

- **分析失败**: 
  - 返回已完成的部分结果
  - 提供详细的错误日志
  - 建议简化分析范围

- **文件保存失败**: 
  - 重试保存操作
  - 提供临时下载链接
  - 保存到备用位置

## 质量保证

- **数据验证**: 交叉验证多个数据源
- **分析一致性**: 确保各框架结论逻辑一致  
- **引用完整性**: 所有数据点都有明确来源
- **更新机制**: 支持定期重新运行分析以获取最新数据