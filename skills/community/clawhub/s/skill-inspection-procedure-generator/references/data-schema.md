# 检验规程数据结构规范

## 目录

- [概览](#概览)
- [完整 JSON 结构](#完整-json-结构)
- [字段说明](#字段说明)
- [校验规则](#校验规则)
- [完整示例](#完整示例)

## 概览

本文档定义了产品检验规程生成脚本 `generate_doc.py` 所需的 JSON 数据结构。智能体从用户提供的控制计划、测试报告、产品图纸等资料中提取信息后，需按此格式组织为 JSON 文件，供脚本读取并生成 Word 文档。

## 完整 JSON 结构

```json
{
  "product_info": {
    "product_name": "产品名称（必填）",
    "product_model": "产品型号",
    "product_category": "产品类别（如：外购件、自制件）",
    "specification": "规格描述",
    "material": "材质",
    "drawing_number": "图纸编号"
  },
  "document_info": {
    "company_name": "公司名称",
    "company_address": "公司地址",
    "doc_number": "文件编号",
    "version": "版本号（默认 A/0）",
    "effective_date": "生效日期（YYYY-MM-DD）"
  },
  "purpose": "目的段落文本（可选，为空时自动生成）",
  "scope": {
    "description": "适用范围描述",
    "product_types": ["子类型1", "子类型2"]
  },
  "inspection_criteria": {
    "documents": ["依据文件1（优先级最高）", "依据文件2"],
    "standards": ["引用标准1", "引用标准2"]
  },
  "sampling": {
    "standard": "抽样标准名称",
    "level": "检验水平",
    "aql": {
      "CRI": 0,
      "MAJ": 0.65,
      "MIN": 1.5
    },
    "plan_description": "抽样方案说明",
    "plan": [
      {
        "batch_range": "2 - 25",
        "sample_code": "C",
        "sample_size": 5,
        "ac_cri": 0,
        "ac_maj": 0,
        "ac_min": 1,
        "re_cri": 1,
        "re_maj": 1,
        "re_min": 2
      }
    ]
  },
  "incoming_check": {
    "description": "来料确认总体说明",
    "items": ["检查项1", "检查项2"]
  },
  "environment": {
    "temperature": "温度要求（如：23±2℃）",
    "humidity": "湿度要求（如：50±5%RH）",
    "equipment": ["设备1", "设备2"]
  },
  "inspection_items": [
    {
      "seq": "1",
      "name": "检验项目名称",
      "defect_level": "CRI/MAJ/MIN",
      "method": "检验方法/工具",
      "standard": "合格标准/要求"
    }
  ],
  "acceptance_criteria": "合格判定标准（字符串或字符串数组）",
  "nonconformance_handling": {
    "标识与隔离": "描述",
    "记录与报告": "描述",
    "处置方式": ["方式1", "方式2"],
    "纠正措施": "描述"
  },
  "records": ["记录名称1", "记录名称2"],
  "signatures": {
    "compiled_by": "编制人姓名",
    "reviewed_by": "审核人姓名",
    "approved_by": "批准人姓名"
  }
}
```

## 字段说明

### product_info（产品信息）-- 必填

| 字段 | 必填 | 说明 | 缺失处理 |
|------|------|------|----------|
| product_name | 是 | 产品名称 | 标注"待确认" |
| product_model | 否 | 产品型号/规格 | 标注"待确认" |
| product_category | 否 | 产品类别（外购件/自制件/委外加工件等） | 省略类别前缀 |
| specification | 否 | 详细规格描述 | 不显示 |
| material | 否 | 材质信息 | 不显示 |
| drawing_number | 否 | 关联图纸编号 | 不显示 |

### document_info（文件信息）

| 字段 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| company_name | 否 | 公司名称 | "待确认" |
| company_address | 否 | 公司地址 | "待确认" |
| doc_number | 否 | 文件编号 | "待确认" |
| version | 否 | 版本号 | "A/0" |
| effective_date | 否 | 生效日期 | "待确认" |

### inspection_items（检验项目）-- 必填

每个检验项目包含以下字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| seq | 是 | 序号（支持层级如 1, 2.1, 2.2） |
| name | 是 | 检验项目名称 |
| defect_level | 是 | 缺陷等级：CRI（关键）/ MAJ（重要）/ MIN（次要）/ 组合如 MAJ/MIN |
| method | 否 | 检验方法或使用的工具/设备 |
| standard | 否 | 合格标准或具体要求描述 |

### sampling.plan（抽样计划表）

每行数据包含：

| 字段 | 说明 |
|------|------|
| batch_range | 批次数量范围（如 "2 - 25"） |
| sample_code | 样本量字码（如 "C", "D", "E"） |
| sample_size | 抽样数量 |
| ac_cri / ac_maj / ac_min | 合格判定数（CRI/MAJ/MIN） |
| re_cri / re_maj / re_min | 不合格判定数（CRI/MAJ/MIN） |

### nonconformance_handling（不合格品处置）

支持两种格式：
1. 字符串：直接作为段落文本
2. 对象：键为处置类别名（加粗显示），值为描述文本或列表

## 校验规则

### 必填字段校验

生成文档前必须检查以下字段：

1. `product_info.product_name` -- 缺失则标注"待确认"
2. `inspection_items` -- 不能为空数组，至少包含1个检验项目

### 数据一致性校验

1. `inspection_items` 中每个项目的 `defect_level` 必须为 CRI/MAJ/MIN 或其组合
2. `inspection_items` 中序号 `seq` 应保持逻辑层级关系（如 1, 2, 2.1, 2.2, 3）
3. `sampling.aql` 中的 CRI 值应为 0

### 缺失数据处理原则

- 用户未提供的非必填字段：使用默认值或省略
- 用户未提供的必填字段：标注"待确认"，并在文档末尾汇总所有待确认项
- 智能体不得自行编造任何技术参数、公差值、检验标准

## 完整示例

以下为一个电机槽绝缘的检验规程数据示例：

```json
{
  "product_info": {
    "product_name": "槽绝缘",
    "product_model": "DMD-F-120",
    "product_category": "外购件",
    "specification": "厚度0.20mm，耐温等级B级(130℃)",
    "material": "DMD（聚酯薄膜-聚酯纤维非织布-聚酯薄膜三层复合材料）",
    "drawing_number": "DWG-SL-001"
  },
  "document_info": {
    "company_name": "大连誉信科技有限公司",
    "company_address": "大连市金州区站前街道金湾路287号-1号1层",
    "doc_number": "QM-IQC-0023",
    "version": "A/0",
    "effective_date": "2025-01-15"
  },
  "purpose": "为确保外协定制的电机定子绝缘件（槽绝缘）在尺寸、材质、电气及机械性能上完全符合我公司提供的技术图纸与标准要求，防止不合格品流入产线，保障电机产品的质量与可靠性，特制定本检验规范。",
  "scope": {
    "description": "本规范适用于根据我公司图纸和技术要求定制生产的电机定子槽绝缘件。",
    "product_types": [
      "槽绝缘（Slot Liner）：插入定子槽内的绝缘材料"
    ]
  },
  "inspection_criteria": {
    "documents": [
      "本检验规范",
      "经双方签字确认的技术协议",
      "我公司提供的最终版产品图纸（含尺寸、公差、形状等）",
      "材质标准要求（DMD-F-120，厚度0.20mm，耐温等级B级）"
    ],
    "standards": [
      "GB/T 5591.2（电气绝缘用柔软复合材料）",
      "IEC 60626",
      "GB/T 13542（电气绝缘用薄膜）"
    ]
  },
  "sampling": {
    "standard": "GB/T 2828.1-2012《计数抽样检验程序》",
    "level": "一般检验水平 II",
    "aql": {"CRI": 0, "MAJ": 0.65, "MIN": 1.5},
    "plan_description": "一次正常抽样方案。根据每批交货数量（以"张"或"卷"计）查询抽样计划表确定样本量。",
    "plan": [
      {"batch_range": "2 - 25", "sample_code": "C", "sample_size": 5, "ac_cri": 0, "ac_maj": 0, "ac_min": 1, "re_cri": 1, "re_maj": 1, "re_min": 2},
      {"batch_range": "26 - 150", "sample_code": "D", "sample_size": 8, "ac_cri": 0, "ac_maj": 1, "ac_min": 1, "re_cri": 1, "re_maj": 2, "re_min": 2},
      {"batch_range": "151 - 500", "sample_code": "E", "sample_size": 13, "ac_cri": 0, "ac_maj": 1, "ac_min": 2, "re_cri": 1, "re_maj": 2, "re_min": 3}
    ]
  },
  "incoming_check": {
    "items": [
      "核对送货单、采购订单信息（供应商、物料代码、品名、规格、数量）是否一致",
      "检查包装是否完好，有无破损、受潮、挤压变形",
      "外包装标识（生产批号、材质、规格、日期）是否清晰"
    ]
  },
  "environment": {
    "temperature": "（23±2）℃",
    "humidity": "（50±5）%RH",
    "equipment": ["游标卡尺", "千分尺", "台式测厚仪", "耐压测试仪", "绝缘电阻测试仪", "电子天平", "钢卷尺"]
  },
  "inspection_items": [
    {"seq": "1", "name": "外观质量", "defect_level": "MAJ/MIN", "method": "目视（在标准光源箱下）", "standard": "表面光滑平整，无针孔、气泡、污渍、杂质、裂纹、机械损伤。边缘切割整齐，无毛刺。颜色与纹理均匀一致，与封样件无异。"},
    {"seq": "2", "name": "尺寸检测", "defect_level": "", "method": "", "standard": ""},
    {"seq": "2.1", "name": "外形尺寸（长/宽）", "defect_level": "MAJ", "method": "钢卷尺/游标卡尺", "standard": "符合图纸公差要求（±1.0mm）"},
    {"seq": "2.2", "name": "厚度", "defect_level": "CRI", "method": "台式测厚仪", "standard": "多点测量（至少5点/m²），平均值和单点值均需符合图纸公差（±0.02mm）"},
    {"seq": "3", "name": "材质确认", "defect_level": "CRI", "method": "", "standard": ""},
    {"seq": "3.1", "name": "材质证明", "defect_level": "CRI", "method": "查验随货文件", "standard": "必须提供原材料生产厂的材质证明书（COC），型号DMD-F-120、耐温等级B-130℃与要求一致"},
    {"seq": "4", "name": "电气性能", "defect_level": "CRI", "method": "（每批或定期抽样送Lab检测）", "standard": ""},
    {"seq": "4.1", "name": "耐电压强度", "defect_level": "CRI", "method": "耐压测试仪", "standard": "≥10kV/mm，测试1min无击穿、无闪络"}
  ],
  "acceptance_criteria": [
    "批合格判定：抽样样本中，所有关键项（CRI）的不合格数为0，且重要项和次要项的不合格数均小于或等于规定的合格判定数（Ac），则判定该批次为合格。",
    "单项判定：任何关键项（CRI）出现一个不合格，即判定该批次不合格。"
  ],
  "nonconformance_handling": {
    "标识与隔离": "立即对不合格品及其同批产品粘贴红色"不合格"标签，并移至不合格品区隔离",
    "记录与报告": "详细填写《进货检验报告》，记录不合格项、比例，并附照片证据",
    "处置方式": [
      "退货/拒收：关键项不合格或主要缺陷严重的批次，整批退货",
      "挑选/返工：仅适用于轻微外观缺陷，需供应商派人处理",
      "特采/让步接收：原则上不适用，极特殊情况需最高级别评审批准"
    ],
    "纠正措施": "向供应商发出《SCAR》，要求分析根本原因并制定改进措施"
  },
  "records": ["进货检验报告", "材料检验报告（实验室）", "不合格品评审单", "供应商纠正措施报告（SCAR）"],
  "signatures": {
    "compiled_by": "待确认",
    "reviewed_by": "待确认",
    "approved_by": "待确认"
  }
}
```
