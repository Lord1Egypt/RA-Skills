---
name: 项目Solution自动分类工具**
version:1.0
description:根据项目属性（如Competency、名称、描述、EP、公司类型等），从预定义的解决方案列表中为其标注最合适的Solution标签。
---

**一、用户输入格式 (Input Schema)**
请以**CSV格式**或**包含以下字段的JSON数组**提供项目清单。**字段名必须严格一致**。

| 字段名 (英文) | 字段名 (中文) | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `Engagement_Code` | 项目代码 | 是 | 项目唯一标识 |
| `Engagement_Name` | 项目名称 | 是 | 主要分类依据之一 |
| `Service_Description` | 服务描述 | 是 | 主要分类依据之一 |
| `EP_Local_Competency` | EP本地能力领域 | 是 | 决定候选Solution范围的关键字段 |
| `Company_Type` | 公司类型 | 是 | 用于`Internal Audit Support for SOE Overseas Entities`的校验 |
| `Engagement_Partner` | 项目合伙人 | 是 | 用于People & Organization类Solution的校验 |
| `Eng_Global_Service_Descr` | 项目全球服务描述 | 是 | 用于Finance.类别下Solution的直接匹配 |

---

**二、处理逻辑与步骤 (Step-by-step Logic)**

**步骤 0： 数据准备与校验**
1.  **检查必填字段**：确保每条记录都包含 `EP_Local_Competency` 字段。如果缺失，标记为“**错误：EP Local Competency缺失**”。
2.  **读取Competency-Solution映射**：加载"assets"文件下“Competency的Solution清单”，构建内部查找表。

**步骤 1： 确定候选Solution范围**
1.  根据项目的 `EP_Local_Competency` 值，从“Competency的Solution清单”中查找其对应的**所有**Solution列表。这是**主要搜索范围**。
2.  **特殊情况处理**：
    *   如果 `EP_Local_Competency` 不在清单中，将候选范围设为**所有Competency的Solution全集**。
    *   如果找到的候选Solution列表为空，也将候选范围设为**全集**。

**步骤 2： 匹配与分类 (核心逻辑)**
此步骤按**优先级**执行，一旦匹配成功即停止，并进入步骤3的校验。

*   **优先级 2.1: Finance. 类别的直接匹配 (最高优先级)**
    *   **触发条件**：`EP_Local_Competency` 为 **`Finance.`**。
    *   **操作**：**完全忽略**项目名称和描述。**仅**根据 `Eng_Global_Service_Descr` 的值，与以下列表进行**精确匹配**，并赋予对应的Solution。
        *   `FI-Bus. Planning, Reporting & Analytics` -> `Business Planning Reporting & Analytics`
        *   `FI-Finance Technology Services` -> `Finance Technology Services`
        *   `FI-Global Business Services` -> `Global Business Services`
        *   `FI-Finance Transform Strategy and Vision` -> `Finance Transform Strategy and Vision`
        *   `FI-MS Global Business Managed Services` -> `Global Business Managed Services`
        *   `FI-Finance Data Transformation` -> `Finance Data Transformation`
        *   `SCO-Intelligent Operations` -> `SCO-Intelligent Operations`
    *   **结果**：如果匹配成功，直接得到Solution，进入步骤3。如果未匹配，则进入下一优先级。

*   **优先级 2.2: 基于项目名称和描述的通用匹配**
    *   **触发条件**：所有非Finance.项目，或Finance.项目在2.1中未匹配成功。
    *   **操作**：在**步骤1确定的候选Solution范围内**，逐一将每个Solution的**关键词/特征描述**与项目的 `Engagement_Name` 和 `Service_Description` 进行比对。
    *   **匹配规则**：
        1.  **精确关键词匹配**：如果项目名称/描述中包含Solution定义中的**核心关键词**（如“PN21”对应`Internal Audit`，“MLPS”对应`Risk and Compliance Assessment`），则优先匹配。
        2.  **语义理解匹配**：分析项目描述的核心活动（如“流程梳理”、“系统开发”、“战略规划”），与Solution定义的核心（如“设计”、“实施”、“规划”）进行匹配。
        3.  **单一匹配原则**：一个项目**通常只分配一个最匹配的Solution**。如果出现多个高度匹配的候选，选择定义更精确、更具体的那一个。
    *   **结果**：如果找到匹配，得到Solution，进入步骤3。如果**在候选范围内未找到**任何合适匹配，则将搜索范围**扩大到所有Competency的Solution全集**，重复此匹配过程。

*   **备用逻辑**：如果在全集中仍无法匹配，则将Solution标记为“**未分类-需人工复核**”。

**步骤 3： 特殊Solution的附加校验**
对步骤2得到的Solution进行最终核查，如果不满足条件，则**降级**或**标记错误**。

*   **校验规则 3.1: `Internal Audit Support for SOE Overseas Entities`**
    *   **条件**：`Company_Type` 字段的值必须是 **`State-Owned Enterprise (SOE)`** 或 **`Specialized Enterprise (SE/央企)`**。
    *   **处理**：如果条件满足，保留该Solution。**如果不满足**，则将此Solution**降级**为更通用的 `Internal Audit` 或 `Risk and Compliance Assessment`（需根据项目内容二次判断）。

*   **校验规则 3.2: `Talent Transformation` 与 `Change Management` (People & Organization)**
    *   **条件**：`Engagement_Partner` 字段的值必须是 **`Jeff TK Tang`**, **`Kannie Kong`**, **`Kevin L Zhang`**, **`Danielle Xie`**, **`Mary Chua`** 中的一个。
    *   **处理**：如果条件满足，保留该Solution。**如果不满足**，则将此Solution标记为“**错误：EP不匹配**”，并建议重新评估或选择其他Solution（如`Group Governance and Control`, `Digital Transformation Planning`等）。

---

**三、输出格式 (Output Schema)**
处理完成后，将返回一个包含**新增列**的表格。

| 新增字段名 | 说明 |
| :--- | :--- |
| `Matched_Solution` | 最终匹配的Solution名称。 |
| `Match_Confidence` | 匹配置信度，如“高（直接匹配）”、“中（语义匹配）”、“低（范围外匹配）”、“需校验”。 |
| `Validation_Status` | 特殊Solution的校验结果，如“通过”、“降级为[其他Solution]”、“失败：原因”。 |
| `Processing_Notes` | 处理过程的简要说明，如“在[Competency]范围内匹配”、“因EP不匹配，标记错误”。 |

---

**四、示例 (Example)**

**输入 (CSV片段):**
```csv
Engagement_Code,Engagement_Name,Service_Description,EP_Local_Competency,Company_Type,Engagement_Partner,Eng_Global_Service_Descr
EC001,PN21内部控制审阅,为港股IPO提供内控审阅,Regulatory Compliance,Private,John Doe,
EC002,海外子公司风险评估,对某央企海外子公司进行风险评估,Regulatory Compliance,State-Owned Enterprise (SOE),Jane Smith,
EC003,组织变革与领导力工作坊,推动数字化转型下的组织变革,Transformation Consulting,Private,Jeff TK Tang,
EC004,财务分析平台实施,实施SAP BPC系统,Finance.,Private,Mike Brown,FI-Bus. Planning, Reporting & Analytics
```

**输出 (处理结果):**
| Engagement_Code | Matched_Solution | Match_Confidence | Validation_Status | Processing_Notes |
| :--- | :--- | :--- | :--- | :--- |
| EC001 | Internal Audit | 高（直接匹配） | 通过 | 在Regulatory Compliance范围内，根据关键词“PN21”匹配。 |
| EC002 | Internal Audit Support for SOE Overseas Entities | 中（语义匹配） | 通过 | 在Regulatory Compliance范围内匹配，且公司类型为SOE，校验通过。 |
| EC003 | Change Management (People & Organization) | 高（语义匹配） | 通过 | 在Transformation Consulting范围内匹配，且EP为Jeff TK Tang，校验通过。 |
| EC004 | Business Planning Reporting & Analytics | 高（直接匹配） | 通过 | Finance.类别，根据Eng Global Service Descr直接匹配。 |

