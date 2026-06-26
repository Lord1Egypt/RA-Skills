---
name: walter-competitor-monitor
version: 1.0.0
description: "亚马逊竞品监控 - 回答"竞品在做什么"的问题。自动发现竞品、分析流量词、挖掘VOC、追踪动态，输出竞品情报报告。"
---

# 亚马逊竞品监控

## 核心问题

**"我的竞品在做什么？"**

## 用户交互

### 输入

```
用户: "监控 CRZ YOGA"
用户: "分析 ASIN B071WV2SRC"
用户: "关注这几个竞品: B071WV2SRC, B08KHQY9DV"
用户: "竞争对手分析"
```

### 输出

```
[竞品监控报告]

Target: CRZ YOGA

├─ 基础情报
│   ASIN: B071WV2SRC
│   月销量: ~3,200 units
│   月收入: ~$92,800
│   价格: $28.99 | 评分: 4.5
│
├─ 流量词 (Top 5)
│   beach shorts women (12%)
│   summer shorts (8%)
│   ...
│
├─ VOC分析
│   赞美: "buttery soft", "fits true to size"
│   痛点: "pills after 3 washes", "waistband rolls"
│
└─ 行动建议
    攻击点: pilling问题 (23%差评)
    策略: 主打"anti-pilling"差异化
```

---

## 分析流程

### Step 1: 解析竞品标识

- ASIN识别 (10位字母数字)
- 品牌名识别
- 批量处理支持

### Step 2: 获取基础情报

- 销量/价格/评分/BSR
- 月收入估算
- 上市时间

### Step 3: 流量词分析

- 核心流量词排名
- 流量词类型 (Search/AC/Sponsored)
- 竞品流量词对比

### Step 4: VOC分析

- 赞美点提取
- 痛点提取
- 差评关键词

### Step 5: 行动建议

- 攻击点识别
- 差异化策略
- 投放建议

---

## 技术实现

```python
class CompetitorMonitor:
    def analyze(self, user_input: str) -> Dict:
        """
        竞品监控完整流程
        """
        # 1. 解析竞品
        targets = self.parse_targets(user_input)
        
        # 2. 获取情报
        intelligence = []
        for target in targets:
            intel = self.get_intel(target)
            intelligence.append(intel)
        
        # 3. 流量词分析
        keywords = self.analyze_keywords(intelligence)
        
        # 4. VOC分析
        voc = self.analyze_voc(intelligence)
        
        # 5. 行动建议
        actions = self.generate_actions(keywords, voc)
        
        return {
            'targets': targets,
            'intelligence': intelligence,
            'keywords': keywords,
            'voc': voc,
            'actions': actions
        }
```

---

## 依赖

- `unified_data_layer_v2.py` - 统一数据层
- `sellersprite_mcp.py` - MCP客户端
- SellerSprite API access

---

## 版本

V1 - 2026-04-13
- 第一版发布
- 场景: 竞品监控
