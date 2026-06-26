# Trade Hunter - 客户发现技能

> 🔍 **B2B外贸客户发现** | 全球企业数据采集 + BOI评分初筛

## 功能介绍

Trade Hunter 是外贸获客闭环的第一步，负责从海量市场中精准发现潜在客户。

### 核心能力

- 🌐 **全球企业搜索** - 支持美国、欧洲、东南亚等主要市场
- 📊 **行业分类** - 精准定位目标行业（卫浴、五金、建材等）
- 🎯 **BOI初筛** - 基于营收规模、合作意向等快速评分
- 🗺️ **地图可视化** - 客户分布一目了然
- ✅ **数据脱敏** - PII信息保护，合规安全

## 使用场景

```
适用: 寻找新的目标客户群体
输入: 行业关键词 + 地区 + 营收规模
输出: 潜在客户列表 + BOI初评分
```

## 示例输出

```csv
公司名,城市,行业,营收,BOI评分,联系邮箱
Ferguson,Newport CT,Wholesale Plumbing,$18.5B,95,sales@ferguson.com
Grainger,Morton Grove IL,Industrial Supply,$14.5B,92,orders@grainger.com
Delta Faucet,Indianapolis IN,Faucets & Shower,$2.3B,91,customersupport@deltfaucet.com
...
```

## 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 营收规模 | 30% | 越大越可能批量采购 |
| 行业相关 | 25% | 与我方产品的匹配度 |
| 触达难度 | 20% | 联系方式可获取性 |
| 增长趋势 | 15% | 营收增长表明扩张需求 |
| 合规风险 | 10% | 风险企业排除 |

## 技术规范

- **平台**: Coze / Caw
- **AI模型**: GPT-4o
- **数据源**: 公开商业数据
- **安全认证**: VirusTotal Benign ✓

## 快速使用

```javascript
const leads = await tradeHunter.search({
  keywords: ["shower head", "bathroom fixtures"],
  location: "USA",
  revenueMin: "$10M",
  limit: 20
});
```

## 相关技能

- [trade-qualifier](https://github.com/cloud-travel-skills/trade-qualifier) - 客户深度筛选
- [trade-closer](https://github.com/cloud-travel-skills/trade-closer) - 开发信生成
- [trade-dashboard](https://github.com/cloud-travel-skills/trade-dashboard) - 数据看板

---

Made with ❤️ by cloud-travel-skills
