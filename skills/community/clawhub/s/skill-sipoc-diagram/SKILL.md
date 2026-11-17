---
name: SIPOC技能工具
slug: sipoc-diagram
displayName: SIPOC技能工具
description: 生成标准SIPOC流程图（供应商-输入-流程-输出-客户）；当用户需要绘制过程流程图、梳理业务输入输出、建立跨部门流程映射或准备流程文档时使用
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# SIPOC 流程图绘制工具

## 任务目标

- **使用场景**: 创建标准的SIPOC（Supplier-Input-Process-Output-Customer）流程图
- **核心能力**: 辅助用户梳理业务/流程的五大核心要素，生成可视化流程图
- **触发条件**: 用户请求"绘制SIPOC"、"创建流程图"、"梳理输入输出"、"建立供应商-客户关系"

## 前置准备

- Python 环境需安装 playwright: `pip install playwright && playwright install chromium`
- 或使用在线绘图方式，由智能体协助完成结构梳理

## SIPOC 模型概述

SIPOC 是六西格玛和流程管理中的核心工具，由以下五部分组成：

| 要素 | 说明 | 示例 |
|------|------|------|
| **Supplier（供应商）** | 提供输入的任何外部或内部供应方 | 原材料供应商、数据提供方、上游部门 |
| **Input（输入）** | 供应商提供的资源、信息或材料 | 原材料、半成品、数据、需求 |
| **Process（流程）** | 核心业务活动或处理步骤 | 加工生产、订单处理、软件开发 |
| **Output（输出）** | 流程产生的结果或产品 | 产品、服务、报告、决策 |
| **Customer（客户）** | 接收输出的个人或组织 | 终端用户、内部客户、下游部门 |

## 操作步骤

### 第一阶段：信息收集

智能体通过交互式对话收集SIPOC各要素信息：

1. **确定流程边界**
   - 明确流程的起点和终点
   - 确定流程名称和编号
   - 询问流程负责人

2. **收集供应商信息**
   - 询问谁是输入的提供者
   - 区分内部供应商和外部供应商
   - 记录每个供应商提供的具体输入

3. **梳理输入项**
   - 列出所有关键输入
   - 标注输入的类型（原材料/信息/资源）
   - 说明输入的规格或要求

4. **描述核心流程**
   - 确定流程的主要步骤
   - 标注关键控制点
   - 说明流程的输入输出关系

5. **识别输出项**
   - 列出所有输出
   - 区分主要输出和副产物
   - 定义输出的质量标准

6. **确定客户**
   - 明确谁使用输出
   - 区分内部客户和外部客户
   - 了解客户的期望和需求

### 第二阶段：数据整理

将收集的信息整理为JSON格式：

```json
{
  "process_name": "订单处理流程",
  "process_id": "P001",
  "supplier": [
    {"name": "客户", "provides": ["订单需求"]},
    {"name": "库存系统", "provides": ["库存数据"]}
  ],
  "input": [
    {"name": "客户订单", "description": "客户提交的采购订单"},
    {"name": "库存信息", "description": "实时库存数据"}
  ],
  "process": [
    {"step": "订单接收", "description": "接收并验证客户订单"},
    {"step": "库存确认", "description": "检查库存可用性"},
    {"step": "订单处理", "description": "完成订单配货和定价"},
    {"step": "发货执行", "description": "安排物流发货"}
  ],
  "output": [
    {"name": "已处理订单", "description": "完成支付的订单记录"},
    {"name": "发货通知", "description": "物流发货通知"}
  ],
  "customer": [
    {"name": "客户", "receives": ["已处理订单"]},
    {"name": "物流部门", "receives": ["发货通知"]}
  ]
}
```

### 第三阶段：生成可视化

调用脚本生成标准SIPOC图形：

```bash
python scripts/generate_sipoc.py --data "<JSON数据>" --output "sipoc_diagram.html"
```

生成的HTML包含：
- 标准SIPOC五行结构
- 完整的要素卡片
- 连接箭头和流程指示
- 可打印的版式设计

### 第四阶段：导出交付

#### 导出为PNG

```bash
python scripts/export_sipoc.py --input "sipoc_diagram.html" --format "png" --output "sipoc_diagram.png"
```

#### 导出为PDF

```bash
python scripts/export_sipoc.py --input "sipoc_diagram.html" --format "pdf" --output "sipoc_diagram.pdf"
```

## 使用示例

### 示例1：订单处理流程

- **场景/输入**: 用户需要为订单处理部门建立标准流程图
- **预期产出**: 包含供应商、输入、流程步骤、输出、客户的完整SIPOC图
- **关键要点**: 
  - 流程从接收订单到发货完成
  - 供应商包括客户和内部系统
  - 客户包括下游物流和终端用户

### 示例2：软件开发交付

- **场景/输入**: 项目经理需要梳理开发到交付的全流程
- **预期产出**: 展示从需求到交付的端到端流程图
- **关键要点**:
  - 供应商：需求方、架构团队
  - 输入：需求文档、设计规范
  - 流程：设计、开发、测试、部署
  - 输出：软件产品、文档
  - 客户：终端用户、运维团队

### 示例3：面试流程优化

- **场景/输入**: HR需要梳理招聘面试全流程
- **预期产出**: 可视化招聘流程的SIPOC图
- **关键要点**:
  - 供应商：招聘网站、内部推荐
  - 输入：候选人简历、职位需求
  - 流程：筛选、面试、评估、录用
  - 输出：录用通知、入职安排
  - 客户：用人部门、新员工

## 资源索引

- 脚本: 见 [scripts/generate_sipoc.py](scripts/generate_sipoc.py)（用途：生成标准SIPOC HTML可视化文件）
- 脚本: 见 [scripts/export_sipoc.py](scripts/export_sipoc.py)（用途：导出SIPOC图为PNG或PDF格式）
- 参考: 见 [references/sipoc-guide.md](references/sipoc-guide.md)（何时读取：需要SIPOC详细定义、填写规范或模板参考时）
- 资产: 见 [assets/sipoc-template.css](assets/sipoc-template.css)（直接用于：SIPOC图形样式模板）

## 注意事项

- SIPOC图的粒度应适中，每个流程步骤约5-7个核心步骤
- 输入输出应与流程步骤有明确的因果关系
- 供应商和客户应区分内部和外部
- 生成的图形可直接打印或嵌入文档
- 如需自定义样式，可修改 assets/sipoc-template.css

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 10/10 | 有清晰工作流程; 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **48/50** | 通过 |
