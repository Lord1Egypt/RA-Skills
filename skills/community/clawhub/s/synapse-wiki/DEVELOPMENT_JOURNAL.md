# Synapse Wiki 开发日记

## 项目起源

Synapse Wiki 项目始于 2026-04-08，目标是将 Karpathy LLM Wiki 模式封装为 OpenClaw Skill，实现持久化知识库构建，让知识随时间复利积累，越用越聪明。

---

## 开发阶段

### Phase 1: ANKE Refactor
- 重构现有 ai-kb 目录结构
- 提取通用脚本（ingest.py, query.py, lint_wiki.py, scaffold.py）

### Phase 2: synapse-wiki 创建
- 创建独立的 synapse-wiki skill
- 实现 init/ingest/query/lint 命令
- 基线测试 4/4 通过

### Phase 3: 配置化与发布准备 (v1.0.0)
- 创建 config.template.json
- 创建 install.sh 安装脚本
- 创建 CHANGELOG.md 和 RELEASE.md
- SKILL.md 描述优化，突出"越用越聪明"

---

## 关键决策

### 1. 目录结构统一
```
synapse-wiki/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── RELEASE.md
├── .skillhub.json
├── install.sh
├── config.template.json
├── commands/
├── scripts/
└── tests/
```

### 2. 配置化路径
- 使用 config.json 而非硬编码
- 支持用户自定义配置

---

## 测试报告

| 技能 | 测试项 | 结果 |
|------|--------|------|
| synapse-wiki | init, ingest, lint, query | **4/4 通过** |
| synapse-code | init_syntax, infer, status | **3/3 通过** |

---

## 经验教训

### 有效做法
- 基线测试作为发布门禁
- install.sh 支持 --dry-run 和 --uninstall
- 文档先行（CHANGELOG/RELEASE 格式规范）

### 踩过的坑
1. **目录结构不一致** — synapse-wiki 最初没有 README.md 和 .skillhub.json
2. **rsync 优于 cp** — 支持 --exclude 排除 node_modules

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0.0 | 2026-04-08 | 初始公开发布版本 |
| v2.0.0 | 2026-04-10 | Brain/Hands 架构升级 + code 互操作 |

---

## 未来规划

### v2.0.1
- PDF/图片摄取支持
- 增量索引加速
- Wiki 全文搜索

### v2.0.2
- synapse-design — 设计创作 Skill
- synapse-analytics — 数据分析 Skill
- Brain Skill Marketplace
- 跨项目知识图谱
