---
name: supplier-evaluation
description: 当用户需要评估供应商资质、查询供应商评分、比较多个供应商或获取供应商推荐时触发
version: 1.0.0
tools_required:
  - supplier_database
  - rating_calculator
  - compliance_checker
---

# 供应商评估技能 (Supplier Evaluation)

## 触发条件

以下场景自动触发供应商评估技能：
- 用户点击供应商详情页
- 用户要求"比较这几家供应商"
- 用户询问"这家工厂靠谱吗"
- 采购决策前的供应商筛选
- 新供应商准入审核

## 执行步骤

### Step 1: 供应商信息采集
```
1. 从供应商数据库获取基本信息
   - 企业名称、统一社会信用代码
   - 经营地址、生产规模
   - 主营类目、历史年限
   - 出口资质、认证证书

2. 获取绩效数据
   - 历史订单完成率
   - 客户投诉率
   - 交期准时率
   - 质量合格率
```

### Step 2: 四维评分计算

| 维度 | 权重 | 评分因子 | 数据来源 |
|------|------|----------|----------|
| 价格竞争力 | 25% | 报价折扣率、价格响应速度 | 询价记录 |
| 质量稳定性 | 30% | 来料合格率、客验通过率 | QC报告 |
| 交期准时率 | 30% | 订单按期交付率、延期频率 | 订单系统 |
| 服务响应 | 15% | 询盘响应时间、问题解决率 | 沟通记录 |

### Step 3: 综合评分汇总
```
综合评分 = Σ(维度评分 × 权重)

评分等级:
- 4.5-5.0: ⭐⭐⭐⭐⭐ 优质供应商
- 4.0-4.4: ⭐⭐⭐⭐ 良好供应商
- 3.5-3.9: ⭐⭐⭐ 一般供应商
- 3.0-3.4: ⭐⭐ 需谨慎合作
- <3.0: ⭐ 不推荐
```

### Step 4: 风险识别
```
1. 检查黑名单记录
2. 验证资质证书有效性
3. 分析投诉历史
4. 评估产能饱和度
5. 识别关联风险(同一法人多家公司)
```

### Step 5: 报告生成
```
输出结构化评估报告，包含:
- 基础信息卡片
- 四维雷达图数据
- 综合评分与等级
- 风险提示
- 合作建议
```

## 输出格式

### 评估报告响应
```json
{
  "success": true,
  "skill": "supplier-evaluation",
  "data": {
    "supplier_info": {
      "id": "SUP2024YIWU001",
      "name": "义乌市优品生活家居有限公司",
      "location": "义乌市苏溪镇",
      "established": 2015,
      "main_categories": ["收纳用品", "厨房小工具"],
      "factory_size": "3000㎡",
      "employee_count": 85,
      "export_ratio": "60%"
    },
    "certifications": [
      {"type": "ISO9001", "valid_until": "2026-03-15", "status": "valid"},
      {"type": "BSCI", "valid_until": "2025-08-20", "status": "valid"}
    ],
    "evaluation": {
      "overall_score": 4.3,
      "grade": "A",
      "dimensions": {
        "price_competitiveness": {
          "score": 4.2,
          "weight": 0.25,
          "details": "报价响应快，经常有批量折扣"
        },
        "quality_stability": {
          "score": 4.5,
          "weight": 0.30,
          "details": "来料合格率达98%，客验通过率95%"
        },
        "delivery_reliability": {
          "score": 4.1,
          "weight": 0.30,
          "details": "准时交付率92%，偶有延期但会提前沟通"
        },
        "service_response": {
          "score": 4.4,
          "weight": 0.15,
          "details": "平均响应时间2小时，问题解决及时"
        }
      },
      "review_summary": {
        "total_reviews": 156,
        "avg_rating": 4.3,
        "recent_30d_rating": 4.5,
        "positive_rate": "89%"
      }
    },
    "risk_assessment": {
      "risk_level": "low",
      "blacklist": false,
      "capacity_status": "available",
      "warnings": []
    },
    "recommendation": {
      "suitable_for": ["跨境电商", "亚马逊卖家", "线下批发"],
      "moq_recommendation": "50-500件",
      "cooperation_tips": [
        "建议签订正式采购合同",
        "首批建议100件试单",
        "大货前要求样品确认"
      ]
    }
  },
  "confidence": 0.92
}
```

### 供应商对比响应
```json
{
  "success": true,
  "skill": "supplier-evaluation",
  "data": {
    "comparison_type": "multi_supplier",
    "suppliers": [
      {"id": "SUP001", "name": "供应商A", "score": 4.5},
      {"id": "SUP002", "name": "供应商B", "score": 4.2},
      {"id": "SUP003", "name": "供应商C", "score": 3.8}
    ],
    "comparison_matrix": {
      "headers": ["维度", "供应商A", "供应商B", "供应商C"],
      "rows": [
        ["价格竞争力", "4.5", "4.0", "4.3"],
        ["质量稳定性", "4.6", "4.3", "3.9"],
        ["交期准时率", "4.3", "4.4", "3.5"],
        ["服务响应", "4.4", "4.0", "4.1"]
      ]
    },
    "winner": {
      "overall": "供应商A",
      "best_price": "供应商C",
      "best_quality": "供应商A",
      "fastest_delivery": "供应商B"
    }
  }
}
```

## 异常处理

### 异常1: 供应商数据不足
```
判断: 订单数<5 或 评分样本<10
处理:
  1. 标注"数据不足，评分仅供参考"
  2. 提供其他评估维度(实地验厂、样品测试)
  3. 建议先小批量试单
```

### 异常2: 供应商在黑名单
```
判断: blacklisted == true
处理:
  1. 明确提示"该供应商存在风险记录"
  2. 展示具体风险原因
  3. 建议更换供应商
  4. 阻止继续下单操作
```

### 异常3: 资质证书过期
```
判断: 关键认证valid_until < today
处理:
  1. 标注证书状态为"已过期"
  2. 联系供应商更新
  3. 在报告中单独提示
```

## 示例

### 示例1: 新供应商准入评估
```
用户: "帮我评估一下这家工厂: 义乌市宏图塑料制品厂"
系统:
  1. 查询供应商基础信息
  2. 计算四维评分
  3. 识别潜在风险
  4. 输出评估报告和合作建议
```

### 示例2: 供应商对比选择
```
用户: "我想要找收纳箱的供应商，你帮我对比一下这3家: A公司、B公司、C公司"
系统:
  1. 批量获取三家公司评估数据
  2. 生成对比矩阵
  3. 输出各维度最优建议
  4. 给出综合推荐
```

### 示例3: 批量供应商筛选
```
用户: "给我推荐10家做圣诞用品的供应商，要评分4.0以上的"
系统:
  1. 按类目和评分筛选
  2. 返回满足条件的供应商列表
  3. 按评分排序
  4. 提供快速联系入口
```
