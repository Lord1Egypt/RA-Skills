# 中医食疗辨证论治系统（tcm-dietary）

基于"理、法、方、药（食）"完整理论框架的 AI 中医食疗技能。通过 HTTP API 调用 VPS 后端服务。

## 🚀 接入方式

- **API Base URL**: `https://api.tcmplate.com`
- **认证**: `Authorization: Bearer <api_key>`
- **免费额度**: 10 次/日（按 IP）
- **付费订阅**: $5/月 PayPal（不限次数）
- **订阅页面**: https://api.tcmplate.com/subscribe

## 核心能力

- **辨证分析**：症状 → 八纲辨证 + 五脏辨证 + 气血辨证 + 六经辨证 + 病因辨证 → 证型结论
- **知识检索**：28 本中医古籍结构化知识库
- **食疗方案**：个性化食谱生成、菜品中医改良
- **食材查询**：3,372 种食材的性味归经功效
- **茶饮保健**：997 首保健茶饮配方
- **导引功法**：154 式导引功法推荐

## 快速开始

```python
import tcm_dietary
tcm_dietary.set_api_key("tcm_your_api_key_here")

from tcm_dietary.core.syndrome import diagnose
from tcm_dietary.core.knowledge import search

# 辨证
result = diagnose(["头晕", "乏力", "失眠"])
print(result["syndrome"]["pattern"])
print(result["recommended_foods"])

# 知识检索
results = search("ingredients", ["生姜"])
```

```bash
# curl 调用
curl -X POST https://api.tcmplate.com/api/diagnose \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"symptoms":["失眠","心悸","健忘"]}'
```

## 目录结构

```
tcm-dietary/
├── core/              # HTTP API 客户端（syndrome / knowledge / recipe / tea / daoyin）
├── SKILL.md           # 市场版文档（含定价 + API 示例）
├── SKILL_FULL.md      # 完整版文档（Agent 深度使用）
└── CHANGELOG.md
```

## 知识库（托管在 VPS）

| 库 | 条目 | 来源 |
|----|------|------|
| tcm-theory.json | 460 | 辨证录、症因脉治等 28 本经典 |
| ingredients.json | 3,372 | 中药学 + 食养食疗 + 全球食材 |
| dishes.json | 8,673 | 药膳方 + 食疗菜谱 |
| chronic-diseases.json | 619 | 内科/妇科/儿科病证标准 |
| symptoms.json | 4,283 | 症状 → 证型映射 |
| cosmetic_formulas.json | 15 | 中医美容方剂 |
| daoyin_module.json | 154 | 导引功法 |
| 茶饮保健 | 997 | 16 功效分类 |
| 古代房中秘方 | 102 | 传统房中养生 |

## 许可

MIT-0 (MIT No Attribution)。可自由使用、修改和重新分发。
API 调用受免费/付费额度限制，见订阅页面。
