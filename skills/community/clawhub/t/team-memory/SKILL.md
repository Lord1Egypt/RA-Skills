---
name: team-memory
description: 私人团队记忆管理系统 v2.4.0。用于记录团队成员观察、维护成员档案和蒸馏摘要、准备 1:1、生成周报/月报/绩效材料，并兼容 v1 的 姓名-档案.md / 姓名-时间轴.md / 姓名-蒸馏.md 旧数据。
license: MIT
compatibility: opencode
version: "2.4.0"
---

# Team Memory v2.4.0

本 skill 帮助管理者维护本地 Markdown 团队记忆。原则：先保护历史数据，再更新结构；新写入使用 v2 结构，旧 v1 文件可继续读取。

本发布包是 lean runtime 包，不携带 `data/`、真实 `skill-config.yaml` 或示例成员数据。用户数据由 `scripts/init.sh` 在本地按需创建；升级 skill 时不要覆盖用户的 `data/` 和 `skill-config.yaml`。

## 数据结构

默认数据目录：`~/.config/opencode/skills/team-memory/data`

```text
data/
├── members/
│   └── member-001/
│       ├── profile.md
│       ├── timeline.md
│       └── distill.md
├── upward/
│   └── expectations.md
├── company/
│   └── strategy.md
├── insights/
├── templates/
└── archive/
```

成员真实姓名、别名、角色、职级和入职日期保存在 `skill-config.yaml`。文件路径优先使用 `member-XXX`，降低隐私和跨平台风险。

## v1 兼容

读取历史数据时同时支持：

- v2：`data/members/member-001/profile.md`
- v1：`data/members/张三-档案.md`
- v2：`data/members/member-001/timeline.md`
- v1：`data/members/张三-时间轴.md`
- v2：`data/members/member-001/distill.md`
- v1：`data/members/张三-蒸馏.md`

如果 v2 和 v1 同时存在：优先读取 v2，把 v1 视为只读历史来源。不要删除、覆盖或重命名 v1 文件，除非用户明确要求。

## 成员匹配

1. 读取 `skill-config.yaml` 的 `members` 和 `shortcuts`。
2. 用输入中的姓名、别名、成员 ID 匹配成员。
3. 如果多个成员命中同一别名，停止并请用户确认，不要猜。
4. 如果没有命中，询问是否创建新成员；创建时使用 `scripts/new-member.sh`。

## 记录观察

当用户说“记录……”“补一条……”“今天张三……”等记录请求：

1. 匹配成员。
2. 写入 `data/members/{member-id}/timeline.md` 的“时间轴（从新到旧）”标题后方。
3. 新记录格式：

```markdown
### YYYY-MM-DD（周X）
#### HH:MM - 一句话标题 [OBS-YYYYMMDD-001]
**事件**: 事实描述
**类别**: 技术能力 / 协作沟通 / 项目交付 / 团队影响 / 成长潜力
**评价**: ⭐⭐⭐⭐⭐ 优秀 / ⭐⭐⭐⭐ 良好 / ⭐⭐⭐ 一般 / ⚠️ 需关注
**标签**: #标签

**观察笔记**:
- 基于事实的观察

**追踪项**:
- [ ] 中 - 需要跟进的事项 (来源: OBS-YYYYMMDD-001)
```

4. 如果输入里有承诺、提醒、下次跟进、1:1，要生成追踪项。
5. 记录后更新同成员 `distill.md`：近期状态、关键事件、追踪项。
6. 对负面记录只写事实和行为，不写人格判断。

## 查询和报告

默认检索顺序：

1. 先读 `distill.md` 快速理解成员状态。
2. 需要证据时读 `timeline.md`。
3. 需要 OKR、职级、发展计划时读 `profile.md`。
4. 团队级问题再读本地存在的 `data/team-memory-overview.md`、`upward/expectations.md`、`company/strategy.md`。

常见输出：

- 1:1 准备：近期亮点、需关注、上次承诺、本次谈话要点、建议提问。
- 周报/月报：团队亮点、风险、追踪项、下周期建议。
- 绩效材料：按维度给评价，并引用具体日期和事件 ID。
- 晋升评估：只使用有记录证据的事件，区分事实、推断和建议。

## 更新和迁移

- 升级前阅读 `references/upgrade.md`。
- v1 到 v2 使用 `scripts/migrate-v1-to-v2.sh`。
- 迁移脚本默认 dry-run；只有 `--apply` 才复制文件。
- 迁移只复制，不删除旧文件。
- 使用说明见 `references/usage.md`。

## 参考文档

- 使用指南、模板、场景和故障排除：`references/usage.md`
- 升级、迁移、兼容和变更摘要：`references/upgrade.md`
