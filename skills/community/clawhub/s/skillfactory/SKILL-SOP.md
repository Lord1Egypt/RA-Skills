# Skill 快速创建 SOP

> 这是 Claw 和用户协作制造 skill 的标准操作程序。
> 每次创建新 skill 时，直接按阶段执行。
>
> **版本**：v1.0  
> **维护人**：Claw（AI）  
> **最后更新**：2026-04-18

---

## 工作目录结构

```
D:/WorkBuddy/
├── skill-factory/           # ← 你现在在这里
│   ├── SKILL-SOP.md         # 本文件：标准操作程序
│   ├── inbox/               # 用户丢想法的地方（任何形式：URL/关键词/草稿）
│   └── wip/                 # Work-in-progress：每个 skill 一个子目录
│       └── <skill-name>/
│           ├── BRIEF.md     # 需求简报（Phase 0 产出）
│           ├── raw/         # 收集的原始资料（web_fetch 抓取结果、PDF等）
│           └── draft/       # 蒸馏草稿
│
├── harness/                 # 已完成的 skill repo（独立发行）
├── <skill-name>/            # 其他已完成的 skill repo
│   ├── SKILL.md
│   ├── README.md
│   └── references/
│
└── .workspace-index.md      # 所有 skill 状态总览（Claw 自我管理用）
```

---

## 四阶段工作流

### Phase 0：快速摄入（≤5分钟）

**触发方式**：用户随时丢来想法，格式不限：
- 一句话：`做一个 X 的 skill`
- URL：`https://...`
- 关键词：`X + Y + Z`

**Claw 的工作**：
1. 在 `inbox/` 记录原始想法（防止丢失）
2. **立刻**提出 3 个快速确认问题（不超过 3 个）：
   - 目标用户/场景是什么？
   - 有没有参考资料来源？（如果没有，Claw 自行搜索）
   - 发行形式：仅本地用 / 发布 GitHub / 分享给他人？
3. 生成 `wip/<skill-name>/BRIEF.md`（标准格式，见下）

**BRIEF.md 模板**：
```markdown
# BRIEF: <skill-name>

**状态**: Phase 0 - 需求确认
**创建时间**: YYYY-MM-DD

## 用户原始想法
（原话或摘要）

## 确认结果
- 目标场景：
- 参考来源：
- 发行形式：local / github / distribute
- 特殊要求：

## 初步规划
- 知识核心：
- 预计文件结构：
- 参考优先级：
```

---

### Phase 1：资料收集（自动执行）

**Claw 的工作**：
1. 对每个来源执行 `web_fetch`，结果存入 `wip/<skill-name>/raw/`
2. 如无来源，使用 `web_search` 找 2-3 个高质量来源
3. 记录来源 URL、获取时间、可信度评估

**原则**：
- 宁可多收不漏，Phase 2 再筛
- 必须包含至少 1 个一手来源（官方文档/原文博客）
- 原始内容不做处理，直接保存

---

### Phase 2：蒸馏（核心工作）

**Claw 的工作**：
1. 读取 `raw/` 中所有资料
2. 按 skill-creator 规范提取：
   - **SKILL.md**：触发词 + 核心流程（≤200行）
   - **references/**：详细知识（按主题拆分）
   - **scripts/**（如需）：可复用脚本
3. **原文二次核对**（LRN-001 教训）：蒸馏完成后，再 `web_fetch` 原文对比，检查遗漏

**质量检查清单**：
- [ ] 触发词够宽，覆盖所有可能的用户问法
- [ ] SKILL.md 有清晰的"何时用"说明
- [ ] references/ 包含足够的背景知识
- [ ] 不在 SKILL.md 里塞太多细节（≤200行）
- [ ] 至少做了一次原文二次核对

---

### Phase 3：封装发行

**Claw 的工作**：
1. 在 `D:/WorkBuddy/<skill-name>/` 创建独立 repo
2. 最小化文件结构：
   ```
   <skill-name>/
   ├── SKILL.md
   ├── README.md       # 包含卖点、用法、安装方式
   ├── .gitignore
   └── references/
   ```
3. `git init` + 初始 commit
4. 同步到 `~/.workbuddy/skills/<skill-name>/`（本地立即可用）
5. 更新 `.workspace-index.md` 状态

**发行版本规范**：
- `v1.0.0`：初始可用版本
- `v1.x.0`：新增来源或内容补充
- `v2.0.0`：结构重构或方向调整

---

## 用户传达想法的最快方式

直接说：
> `新 skill：[名字或主题]，[1-2句说明]，[来源URL（可选）]`

示例：
- `新 skill：arxiv-reader，帮我快速读论文，https://arxiv.org/...`
- `新 skill：prompt-engineering，整合 Anthropic 和 OpenAI 的提示词最佳实践`
- `新 skill：git-workflow，规范我的 git commit 和 PR 流程`

Claw 接到后，进入 Phase 0，直接开始，不需要更多信息就能启动。

---

## 当前 Skill 状态总览

详见 `.workspace-index.md`

---

## 已沉淀的经验（来自 .learnings）

| ID | 教训 | 应对方式 |
|----|------|---------|
| LRN-001 | 蒸馏后未原文核对，遗漏关键内容 | Phase 2 强制二次核对步骤 |
| LRN-002 | skill 应在独立 repo 迭代，成熟再同步 | Phase 3 标准流程 |
| LRN-003 | 过度工程化，偏离用户真实需求 | Phase 0 3问确认，先问再建 |
| LRN-004 | research 资料与 skill 文档混在一起 | raw/ 和 references/ 分离 |
