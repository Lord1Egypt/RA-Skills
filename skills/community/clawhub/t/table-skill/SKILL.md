---
name: table-skill
description: "端到端表格数据引擎：提供工业级表格预处理（拆分、清洗、表头合并、描述生成），并支持在受控前提下进行深度探索性分析、可视化与报告生成。"
metadata:
  {
    "openclaw": {
      "emoji": "📊",
      "requires": {
        "bins": ["python"],
        "env": ["OPENAI_API_KEY"]
      },
      "primaryEnv": "OPENAI_API_KEY"
    }
  }
---

# 📊 工业级表格预处理与深度分析技能 (Table Preprocess & EDA)

本技能集专注于脏数据的早期治理，覆盖表格拆分、清洗、表头结构化、描述生成，以及在**明确授权且风险可控**前提下的 EDA、可视化与现代化报告编译。所有脚本已适配 OpenClaw 环境，Agent 可在 workspace 根目录直接调用。

## 🎯 Purpose & Capability

本技能实际包含并支持以下能力：

1. **split_table**：按空行或区域拆分 Excel/CSV 中的多个表格  
2. **clean_table**：移除空白行列、清理字符、规整表结构  
3. **merge_header**：借助 LLM 检测并合并多行表头  
4. **describe_table**：生成表格描述、统计信息与样本摘要  
5. **eda_and_visualization**：由 Agent 动态编写 Python 代码，对已清洗表格做 QA/EDA/可视化/假设生成/报告输出

> 说明：本技能名称与描述已与实际脚本能力保持一致，核心聚焦于 `split / clean / merge / describe`，并在此基础上支持受控的深度分析与可视化。

---

## 🔐 环境变量与凭证说明

### 必需环境变量
- `OPENAI_API_KEY`  
  仅在使用 **LLM 相关功能** 时需要，例如：
  - `merge_header`（表头合并）
  - `describe_table` 的摘要能力
  - 某些 EDA/报告生成阶段中的 LLM 辅助分析

### 可选环境变量
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`

上述两个变量**不是必需项**。若未设置，代码将使用默认的 API Base URL 和模型配置。因此，本技能注册信息仅将 `OPENAI_API_KEY` 声明为必需凭证。

> ⚠️ 重要风险提示  
> 提供 `OPENAI_API_KEY` 后，技能在执行相关 LLM 功能时，可能将**部分表格内容、表头、样本行或 schema 信息**发送到配置的远端 LLM 接口。这是实现智能表头合并、摘要和部分分析能力所必需的，但对**敏感数据**具有显著风险。

---

## 🛡️ 数据安全与使用边界

本技能可读取 workspace 中的 CSV/XLSX 文件，并在 EDA 阶段动态生成并执行 Python 代码。为降低误用与数据泄露风险，Agent 在使用本技能时必须遵循以下约束：

### 1. 最小必要原则
仅处理完成当前任务所必需的文件、工作表、列和行。  
除非用户明确要求，不应批量扫描、遍历或分析无关表格。

### 2. LLM 发送最小化
凡涉及 LLM 的步骤（如 `merge_header`、`describe_table` 摘要、LLM 辅助 EDA），只允许发送完成任务所需的**最小必要信息**，优先级如下：
- 优先发送：表头、字段名、数据类型、统计摘要、schema
- 次选发送：少量脱敏后的样本行
- 避免发送：整表原文、大批量明细记录、敏感标识符列

### 3. 敏感数据默认不外发
若表格中包含或疑似包含以下内容，Agent 应默认**避免调用会向远端 LLM 发送数据的功能**，除非用户明确授权并知悉风险：
- 身份证号、护照号、工号、学号
- 银行卡号、支付信息、账单明细
- 手机号、邮箱、住址、精确地理位置
- 医疗、健康、保险、法律、财务等高敏感信息
- API Key、密码、Token、密钥、内部凭证
- 客户名单、员工名册、合同数据、未公开经营数据

### 4. 优先本地处理
遇到敏感或保密表格时，优先采用：
- 本地脚本清洗
- 本地统计与可视化
- 禁用摘要能力（如 `--no-abstract`）
- 禁用或跳过 `merge_header`
- 使用规则/启发式方法替代 LLM 推断

### 5. 动态代码执行边界
EDA 阶段允许 Agent 动态生成 Python 代码，但代码仅应用于：
- 数据质量检查
- 统计分析
- 特征探索
- 可视化与报告生成

不得将其扩展为与任务无关的目录遍历、凭证搜集、网络外传或其他越权行为。

### 6. 输出去敏
在生成图表、摘要、Web 报告或导出文件时，应避免直接暴露敏感字段原值。必要时应：
- 屏蔽标识列
- 截断文本
- 只展示聚合统计
- 使用匿名化/脱敏样本

---

## 📦 环境安装说明

本技能包含动态数据处理与绘图能力。执行前请完成依赖安装：
`pip install -r requirements.txt`

## 🧰 技能列表 (Atomic Skills)

### split_table - 表格拆分
将 Excel/CSV 文件按空行拆分为多个独立表格。
* **命令行 (Agent 首选)**:
  ```bash
  python skills/table-skill-1.0.3/script/split_table_skill.py input.xlsx ./output
  ```
* **使用方式 (Python API)**:
  ```python
  import sys
  sys.path.append("skills/table-skill-1.0.3")
  from script.split_table_skill import SplitTableSkill
  
  skill = SplitTableSkill()
  result = await skill.run("input.xlsx", "./output")
  # 返回: {"split_files": ["output/table1.csv", ...], "table_count": 2, "success": true}
  ```

---

### clean_table - 表格清洗
清洗表格数据，移除空白行列，处理复杂表头。
* **参数**:
  * `--no-merge-header`: 禁用多行表头合并（默认开启）
  * `--remove-chars`: 需要移除的字符列表（默认 `,%`）
* **命令行 (Agent 首选)**:
  ```bash
  python skills/table-skill-1.0.3/script/clean_table_skill.py input.csv ./output
  python skills/table-skill-1.0.3/script/clean_table_skill.py input.csv ./output --no-merge-header
  python skills/table-skill-1.0.3/script/clean_table_skill.py input.csv ./output --remove-chars ",%"
  ```
* **使用方式 (Python API)**:
  ```python
  import sys
  sys.path.append("skills/table-skill-1.0.3")
  from script.clean_table_skill import CleanTableSkill
  
  skill = CleanTableSkill(is_merge_header=True, remove_chars=[',', '%'])
  result = await skill.run("input.csv", "./output")
  # 返回: {"output_file": "output/input_cleaned.csv", "success": true, "row_count": 100, "col_count": 10}
  ```

---

### merge_header - 表头合并
使用 LLM 智能检测并合并多行表头（**依赖 OPENAI 环境变量**）。
* **命令行 (Agent 首选)**:
  ```bash
  python skills/table-skill-1.0.3/script/merge_header_skill.py input.csv ./output
  ```
* **使用方式 (Python API)**:
  ```python
  import sys
  sys.path.append("skills/table-skill-1.0.3")
  from script.merge_header_skill import MergeHeaderSkill
  
  skill = MergeHeaderSkill()
  result = await skill.run("input.csv", "./output")
  # 返回: {"output_file": "output/input_merged.csv", "success": true, "header_rows_detected": 3}
  ```

---

### describe_table - 表格描述生成
生成表格的详细描述信息，包括统计和样本数据。
* **参数**:
  * `--no-abstract`: 禁用 LLM 摘要生成（默认启用）
* **命令行 (Agent 首选)**:
  ```bash
  # 默认启用 LLM 摘要
  python skills/table-skill-1.0.3/script/describe_table_skill.py input.csv ./output
  
  # 禁用 LLM 摘要生成
  python skills/table-skill-1.0.3/script/describe_table_skill.py input.csv ./output --no-abstract
  ```
* **使用方式 (Python API)**:
  ```python
  import sys
  sys.path.append("skills/table-skill-1.0.3")
  from script.describe_table_skill import DescribeTableSkill
  
  skill = DescribeTableSkill(is_abstract=False)
  result = await skill.run("input.csv", "./output")
  # 返回: {"description": {...}, "output_file": "output/input_description.json", "success": true}
  ```

---

### 🌟 eda_and_visualization - 深度数据探索与可视化

在预处理完成后，Agent 应读取 `*_description.json` 了解数据结构，并根据数据特征**生成分析说明**（如选择要绘制的图表类型、要计算的统计指标），然后利用常见 Python 数据分析库（pandas, matplotlib, seaborn）**生成静态图表和 HTML 报告**。所有分析代码应遵循本技能提供的模板和规范，不得执行与数据分析无关的操作。

* **核心任务**: 数据质量校验 (QA)、特征相关性挖掘 (EDA)、业务假设生成 ($H_0$/$H_1$)、现代化 Web 报告编译。
* **详细约束**: Agent 必须严格查阅并遵循 👉 [深度探索与可视化规范](./script/docs/05_eda_mining_skill.md)。

---

## 🔄 完整流程示例

```python
import sys
import asyncio
sys.path.append("skills/table-skill-1.0.3")
from script.split_table_skill import SplitTableSkill
from script.clean_table_skill import CleanTableSkill
from script.merge_header_skill import MergeHeaderSkill
from script.describe_table_skill import DescribeTableSkill

async def main():
    # 1. 拆分
    split_result = await SplitTableSkill().run("data.xlsx", "./output")

    # 2. 遍历处理
    for file in split_result["split_files"]:
        # 清洗 (为 LLM 表头合并做准备，保留原表头)
        clean_result = await CleanTableSkill(is_merge_header=False, remove_chars=[',']).run(file, "./output")
        
        # 表头合并 (依赖 OPENAI 环境变量)
        merged_result = await MergeHeaderSkill().run(clean_result["output_file"], "./output")
        
        # 3. 描述
        desc_result = await DescribeTableSkill(is_abstract=False).run(merged_result["output_file"], "./output")
        
    # 4. 深度探索与可视化 (EDA & Mining)
    # 注意：此处由 Agent 跳出循环后接管，读取上述生成的某一个或全部 JSON 进行深度分析。
    # Agent 将根据 05_eda_mining_skill.md 的规范，自动编写代码生成图表与 Web 报告。

# 执行主函数
asyncio.run(main())
```

---

## 📤 返回格式

所有技能返回统一格式:

**✅ 成功时**:
```json
{
  "success": true,
  "output_file": "output/processed.csv"
}
```

**❌ 失败时**:
```json
{
  "success": false,
  "error": "错误信息"
}
```

---

## 📚 详细文档

- [表格拆分详解](./script/docs/01_split_table_skill.md)
- [表格清洗详解](./script/docs/02_clean_table_skill.md)
- [描述生成详解](./script/docs/03_describe_table_skill.md)
- [表头合并详解](./script/docs/04_merge_header_skill.md)
- [深度探索与可视化规范 (EDA & Mining)](./script/docs/05_eda_mining_skill.md)