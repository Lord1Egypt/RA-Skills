# A 股股票分析 Skill 集合

这是一个 OpenClaw Skill 集合仓库（Monorepo），包含多个 A 股股票分析相关的技能。

## 📦 包含的 Skills

| Skill 目录 | 描述 | ClawHub Slug | 状态 |
|-----------|------|-------------|------|
| **[cn-stock-volume](cn-stock-volume/)** | 获取 A 股四市（沪市/深市/创业板/北交所）成交金额、增缩量及比例 | `cn-stock-volume` | ✅ 已发布 |
| **[stock-theme-events](stock-theme-events/)** | 股票题材事件分析，自动聚合同花顺/东方财富题材 | `stock-theme-events` | 📝 待发布 |
| **[stock-top-gainers](stock-top-gainers/)** | 获取 A 股近 10 日涨幅排名前 20 股票 | `stock-top-gainers` | 📝 待发布 |
| **[ths-stock-themes](ths-stock-themes/)** | 获取同花顺个股题材/概念板块和人气排名 | `ths-stock-themes` | 📝 待发布 |

## 🚀 快速安装

```bash
# 安装单个 skill
npx clawhub@latest install cn-stock-volume
npx clawhub@latest install stock-theme-events
npx clawhub@latest install stock-top-gainers
npx clawhub@latest install ths-stock-themes
```

## 📁 目录结构

```
cn-stock-volume/              # 仓库根目录
├── README.md                 # 本文件（集合说明）
├── cn-stock-volume/          # 成交金额分析 skill
│   ├── SKILL.md
│   ├── package.json
│   ├── _meta.json
│   └── scripts/
│       └── fetch_volume.py
├── stock-theme-events/       # 题材事件分析 skill
│   ├── SKILL.md
│   ├── scripts/
│   └── config/
├── stock-top-gainers/        # 涨幅排名 skill
│   ├── SKILL.md
│   └── scripts/
└── ths-stock-themes/         # 同花顺题材 skill
    ├── SKILL.md
    ├── scripts/
    └── references/
```

## 🛠️ 发布更新

使用 `skill-publish-tool` 发布单个 skill 的更新：

```bash
# 安装发布工具
npx clawhub@latest install skill-publish-tool

# 发布 skill 更新（monorepo 模式）
python3 ~/.jvs/.openclaw/workspace/skills/skill-publish-tool/scripts/publish_skill.py \
  ~/.jvs/.openclaw/workspace/skills/cn-stock-volume/cn-stock-volume \
  --slug cn-stock-volume \
  --changelog "修复 XX 问题" \
  --bump patch \
  --collection-root ~/.jvs/.openclaw/workspace/skills/cn-stock-volume
```

## 📊 使用示例

### 1. 查询昨日成交数据

```bash
cd cn-stock-volume
python3 scripts/fetch_volume.py 2026-03-20
```

### 2. 获取近 10 日涨幅排名

```bash
cd stock-top-gainers
python3 scripts/fetch_gainers.py
```

### 3. 查询个股题材

```bash
cd ths-stock-themes
python3 scripts/fetch_themes.py --stock 000001
```

### 4. 分析题材事件

```bash
cd stock-theme-events
python3 scripts/cluster_themes.py
```

## 📝 更新日志

### v1.0.0 (2026-03-21)
- 创建 skill 集合仓库（Monorepo 结构）
- 整合 4 个股票分析 skill
- 统一目录结构，便于管理和发布

## 🔗 相关链接

- **GitHub**: https://github.com/shinelp100/cn-stock-volume
- **ClawHub**: https://clawhub.ai
- **skill-publish-tool**: https://clawhub.ai/k976nx1d2sxx6a13t1ncfatc1s83bbdr/skill-publish-tool

## 📄 许可证

MIT License

## 更新日志

### v1.0.4 (2026-03-22)
- Monorepo 结构重构，独立发布版本
