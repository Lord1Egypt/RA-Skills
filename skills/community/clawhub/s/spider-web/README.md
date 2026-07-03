# 🕷️ Spider Web — WorkBuddy Skill Trigger Network

> 蜘蛛网智能技能路由系统。将所有 WorkBuddy 技能的触发词编织成一张网，用户查询命中任一节点，自动路由到目标技能。

## 核心能力

- **自动索引**: 扫描全部已安装技能，提取触发词，构建反向索引数据库
- **智能匹配**: 4 层匹配算法（精确子串 → 技能名 → 中文 Bigram+Jaccard+LCS → 模糊）
- **串/并联**: 支持 AND（串联多触发词同时命中）和 OR（并联任意命中）模式
- **IDF 加权**: 领域专属触发词得分高于通用词，避免"分析""数据"等高频词误判
- **Web 面板**: 交互式 Dashboard，实时匹配测试 + 触发词分布可视化

## 快速开始

```bash
# 1. 安装到 WorkBuddy
# 将本目录放到 ~/.workbuddy/skills/spider-web/

# 2. 索引触发词（首次或新增技能后）
python scripts/index_triggers.py

# 3. 匹配查询
python scripts/match_engine.py "帮我看看这盆花怎么养"
# → flower-care (score: 20.5)

# 4. 返回技能名（供程序调用）
python scripts/match_engine.py "内存占用高" --skill
# → aioom

# 5. 启动 Web 管理面板
python scripts/server.py --port 8766
```

## 网络规模

| 指标 | 数值 |
|------|------|
| 已索引技能 | 54 |
| 触发词总数 | 465 |
| 唯一触发词 | 453 |
| 重叠触发词 | 11 |
| 网络密度 | 2.4% |
| 匹配准确率 | 100% (15/15) |

## 匹配引擎架构

```
用户输入 → 4层匹配 → IDF特异性加权 → 分数聚合 → 最佳技能
   │
   ├─ L1: 精确子串匹配 (fast)
   ├─ L2: 技能名称直接匹配 (fast)
   ├─ L3: 中文Bigram+Jaccard+LCS (smart)
   └─ L4: 英文模糊匹配 difflib (fallback)
```

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 交互式管理面板 |
| GET | `/api/health` | 健康检查 |
| GET | `/api/data` | 完整数据库 |
| GET | `/api/stats` | 统计摘要 |
| POST | `/api/match` | 查询匹配 `{"query":"...", "mode":"auto"}` |
| POST | `/api/reindex` | 重新索引 |

## 为技能添加触发词

在技能的 `SKILL.md` 的 `description` 中添加：

```yaml
description: >
  技能描述文本。
  触发词：关键词1, 关键词2, 关键词3。
```

支持中英文标记：`触发词：` / `Trigger:` / `Triggers:`

## License

MIT
