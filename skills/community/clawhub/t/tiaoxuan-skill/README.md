# SkillPick — 挑选Skill

> 一句话：不是搜索、不是排行，是帮你**判断**哪个值得装。
> 版本：v6.5.0 | 更新：2026-05-01

## 跟竞品有什么不同？

| 工具 | 做什么 | 一句话 |
|------|--------|--------|
| find-skills | 搜索查找 | "你要什么？我帮你找到安装方式" |
| skillhub 排行榜 | 跟风装 | "大家装什么？你照着装" |
| **SkillPick** | 判断推荐 | **"哪些最好？我帮你分析推荐"** |

就像「什么值得买」不搜商品也不排销量，它做的是消费决策。

## 双受众

- **人类** → 打开页面看赛道精选，一眼就知道每个赛道该装什么
- **Agent** → 通过 CLI 调用 search / similar / workflow，获取精确推荐结果

## 六大功能

| 功能 | 给谁用 | 干嘛 |
|------|--------|------|
| 🏆 赛道 TOP3 | 人类 | 58个赛道 Top3，双轨评分（热度分+质量分） |
| 🔍 搜索推荐 | Agent | 输入关键词，返回1-3条推荐+理由+结论 |
| 🔄 相似替代 | Agent | 给个 skill 名，返回替代+差异分析 |
| 🧩 工作流组合 | Agent | 8个预定义场景，每个角色推荐最优 skill |
| 📊 Skill 详情 | CLI | 13维雷达图+完整评分 |
| 📈 质量报告 | CLI | 全局质量分布 |

## Agent CLI 接口

```bash
node api.js <命令> [参数]
```

### 六个命令

```bash
node api.js top3              # 全部赛道 TOP3
node api.js top3 "AI Agent"   # 指定赛道
node api.js search PDF        # 搜索推荐
node api.js similar pdf       # 替代选择
node api.js workflow 短视频   # 工作流推荐
node api.js detail docx       # 技能详情（含13维雷达）
node api.js quality           # 全局质量报告
```

## 数据体系

- 29,000+ skill / 58 赛道 / 三源融合（SkillHub + GitHub + 手工）
- **13维Z-score质量评分** + 三层门控（pass/warn/block）+ 安全一票否决
- **双轨评分**：display_score（热度分，人类端） + quality_score（质量分，Agent端）
- Top 3000 精品发布（A+/A级占96%）
- 全量数据预计算，前端零延迟

## 数据管道

```bash
node pipeline/pipeline.js full         # 全量采集+评分（~6分钟）
node pipeline/clean_and_split.js       # 清洗+Top3000拆分（<3秒）
node pipeline/pipeline.js status       # 查看状态
```

## 文件说明

| 文件 | 用途 |
|------|------|
| `index.html` | 前端页面（四大Tab + 13维Modal，单文件无依赖） |
| `skills_data.js` | Top 3000 精华数据（前端 + CLI 共用，~6MB） |
| `api.js` | Agent CLI 接口（6个命令） |
| `scanner.js` | 13维质量扫描引擎 |
| `data/quality_map_slim.json` | Top 3000 质量映射 |
| `data/workflows.json` | 工作流定义 |
| `SKILL.md` | 元数据入口（SkillHub 集成） |

## 版本历史

- **v6.5.0** (2026-05-01): 品牌升级——中文名正式定名「挑选Skill」；全文件版本号统一；发布包重构
- **v6.4.0** (2026-04-27): 双轨评分体系（display_score+quality_score）；TOP3质量保底；C级惩罚加大；赛道分类修复（"其他"6409→2条）；发布包 Top3000 精华
- **v6.2.0** (2026-04-26): 自动化数据管道（SkillHub 30K+GitHub 680→融合→13维评分→构建）；skill总量 954→29,526
- **v6.1.0** (2026-04-19): 纯净版发布——13维Z-score质量评分为核心引擎
- **v6.0.0** (2026-04-17): 安全清理 + 无关文件清除 + 新增 CLI 接口
