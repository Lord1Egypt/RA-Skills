# Team Memory 使用指南

Team Memory v2.4.0 是一个本地 Markdown 团队记忆系统，用于记录成员观察、维护档案、准备 1:1、生成周报/月报和绩效材料。

发布包不包含 `data/` 和真实 `skill-config.yaml`。首次使用请运行 `scripts/init.sh`，它只会在缺失时创建目录和默认文件，不覆盖已有数据。

## 推荐结构

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

## 快速开始

1. 初始化目录：

```bash
bash scripts/init.sh
```

2. 编辑 `skill-config.yaml`：

- 每个成员必须有唯一 `id`，例如 `member-001`
- `name` 可以是真名
- `alias` 和 `shortcuts` 必须唯一
- `schema-version: "2.0"` 表示数据结构版本，不等同于产品版本

3. 创建新成员：

```bash
bash scripts/new-member.sh member-010 "张三" "后端开发工程师" "2026-05-21"
```

脚本会创建 `profile.md`、`timeline.md`、`distill.md`，并提示你手动更新 `skill-config.yaml`。

## 日常记录

对 Codex/OpenCode 说：

```text
记录：张三今天主动修复了生产问题，并写了复盘文档
```

写入规则：

- 匹配 `skill-config.yaml` 中的姓名、别名或成员 ID
- 新记录写入 `data/members/{member-id}/timeline.md`
- 新记录添加在“时间轴（从新到旧）”标题下方
- 如果包含承诺、提醒、下次跟进、1:1，要生成追踪项
- 记录后更新 `distill.md` 的近期状态、关键事件和追踪项

## 记录模板

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

## 1:1 模板

```markdown
### YYYY-MM-DD（周X）
#### HH:MM - 1:1沟通 [DLG-YYYYMMDD-001]
**事件**: 和{姓名}1:1  
**类别**: 协作沟通 / 成长潜力  
**评价**: ⭐⭐⭐⭐ 良好  
**标签**: #对话 #1on1

**对方反馈**:
- 

**我说了**:
- 

**我的承诺**:
- [ ] {待办} (来源: DLG-YYYYMMDD-001)

**事后反思**:
- 有效：
- 下次改进：
```

## 查询和报告

默认检索顺序：

1. 先读 `distill.md` 快速理解成员状态
2. 需要证据时读 `timeline.md`
3. 需要 OKR、职级、发展计划时读 `profile.md`
4. 团队级问题再读 `team-memory-overview.md`、`upward/expectations.md`、`company/strategy.md`

常见请求：

```text
准备明天和张三的 1:1
生成本周团队观察报告
生成张三本季度绩效材料，需要引用具体证据
对比张三和李四的晋升资格
```

输出要求：

- 1:1 准备：近期亮点、需关注、上次承诺、本次谈话要点、建议提问
- 周报/月报：团队亮点、风险、追踪项、下周期建议
- 绩效材料：按维度评价，并引用日期和事件 ID
- 晋升评估：只使用有记录证据的事件，区分事实、推断和建议

## 双层架构

- 蒸馏层：`distill.md`，用于快速理解成员状态
- 原始层：`timeline.md`，用于追溯完整事实和证据
- 档案层：`profile.md`，用于 OKR、角色、职级和发展计划

准备 1:1 时，先读蒸馏层，再按需追溯原始层。生成绩效材料时，必须从时间轴引用具体日期和事件 ID。

## 隐私建议

- 文件路径优先使用 `member-XXX`
- 真实姓名放在 `skill-config.yaml` 和正文必要位置
- 不要把 `data/` 上传到公共仓库
- 网盘同步前检查加密和共享权限
- 离职成员优先归档到 `data/archive/`

## 故障排除

### 记录无法匹配成员

检查 `skill-config.yaml`：

- `members[].name` 是否与输入姓名一致
- `members[].alias` 是否唯一
- `shortcuts` 是否指向真实存在的 `member-XXX`

### 生成报告缺少数据

常见原因：

- `distill.md` 没有及时更新
- `timeline.md` 记录太少或事件描述过短
- 旧 v1 文件还没有迁移，且查询时没有读取 v1 兼容路径

### 文件名或压缩包乱码

v2 的默认路径使用英文和 `member-XXX`。发布包内部路径必须使用 `/`，不要使用 Windows 反斜杠。

### 搜索历史记录

```bash
rg "张三|member-001|OBS-2024" data/members
```

如果没有安装 `rg`：

```bash
grep -R "张三" data/members
```
