# Customer Segmentation — 客户分层

自动客户标签 + 生命周期管理 + 价值分析。基于 OKKI CRM 数据，5 级客户分层（VIP/活跃/普通/休眠/流失），自动评分+标签同步。

## 模块

| 脚本 | 大小 | 功能 |
|------|------|------|
| `customer-data-collector.js` | — | OKKI API 增量采集客户数据 |
| `scoring-engine.js` | — | 加权评分 + 自动分层（5 级） |
| `tag-sync.js` | 16KB | OKKI 标签同步（⚠️ 安全机制齐全） |
| `strategy-output.js` | 13KB | 策略建议输出 + 升级机会识别 |

## 配置

- `config/segmentation-rules.json` — 5 级分层规则 + 评分权重 + 阈值

## 使用

```bash
cd /Users/wilson/.openclaw/workspace/skills/customer-segmentation

# 1. 采集客户数据
node scripts/customer-data-collector.js

# 2. 评分 + 分层
node scripts/scoring-engine.js
node scripts/scoring-engine.js --sample  # 使用示例数据

# 3. 查看策略建议
node scripts/strategy-output.js
node scripts/strategy-output.js --format summary

# 4. 同步标签到 OKKI（默认 dry-run！）
node scripts/tag-sync.js                  # dry-run 预览
node scripts/tag-sync.js --confirm        # 实际写入
node scripts/tag-sync.js --confirm --limit 5  # 分批写入前 5 个
```

## 分层标准

| 等级 | 标签 | 说明 |
|------|------|------|
| VIP | SEG:VIP | 高价值客户 |
| 活跃 | SEG:活跃 | 定期下单 |
| 普通 | SEG:普通 | 偶尔互动 |
| 休眠 | SEG:休眠 | 长期无互动 |
| 流失 | SEG:流失 | 已流失 |

## ⚠️ Tag-Sync 安全机制

**重要：** tag-sync.js 会写入 OKKI CRM 标签，内置多重安全保护：

1. **默认 dry-run** — 不加 `--confirm` 不会写入
2. **SEG: 前缀白名单** — 只操作 `SEG:` 前缀标签，不影响其他标签
3. **GET 先合并** — 写入前先获取现有标签，合并后再写入（避免覆盖）
4. **写入前备份** — 自动备份当前标签状态
5. **配额预估** — >80% 配额自动中止
6. **500ms 间隔** — API 调用限速
7. **--limit 分批** — 支持分批验证

## 依赖

- `OKKI CRM` — 客户数据 + 标签写入

## 数据存储

- `data/customer-scores.json` — 评分结果
- `data/strategy-recommendations.json` — 策略建议
- `data/metrics-export.json` — 看板指标
