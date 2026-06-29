# skill-sub 常见问题

> 本文档是 SKILL.md 的渐进式补充，收录常见问题与使用技巧。
> 反模式详见 `references/antipatterns.md`。

---

## FAQ

### Q1：调用链和脚本有什么区别？

调用链是**声明式**的——描述"做什么"和"谁来做"，由 AI 按 action 执行。脚本是**命令式**的——精确指令序列，机器直接运行。

| | 调用链 | 脚本 |
|---|--------|------|
| 执行者 | AI | 解释器 |
| 容错 | 分级重试 + 询问 | 严格终止 |
| 适用 | 跨 Skill 编排 | 单一工具链 |

### Q2：如何判断一个任务该不该创建调用链？

三个条件同时满足：
1. 涉及 ≥2 个 Skill
2. 有复用价值（不会只用一次）
3. 步骤间的依赖关系可固化

缺一则不适合。

### Q3：调用链失败后怎么恢复？

1. 查看失败步骤的 `on_exhaust` 配置
2. 非里程碑 + `on_exhaust: ask` → AI 会询问你
3. 非里程碑 + `on_exhaust: skip` → 已自动跳过
4. 里程碑失败 → 链已中止，需修复后重新执行整条链
5. 用 `chain_executor.py plan` 重新生成执行计划

### Q4：配置里的"记忆参考"开启后有什么用？

创建调用链时，AI 会额外读取 MEMORY.md 和近期日志，用于：
- 个性化步骤描述（匹配你的命名习惯）
- 推荐常用或相关的 Skill（基于历史使用模式）

不开也不影响功能，只是步骤描述更通用。

### Q5：为什么我的调用链执行时每一步都要问我？

两个常见原因：
1. 所有步骤配置了 `on_exhaust: ask` — 改为 `skip` 或 `abort` 减少交互
2. 第1层 action 描述不够精确 — 执行时 AI 无法确定怎么做，只能问

解决：创建链时确保每个 action 包含具体的动词+对象+产出。

### Q6：skill-sub 的数据存在哪？更新会丢吗？

数据存储在 `~/.workbuddy/skills/.standardization/skill-sub/`（可通过 `SKILL_SUB_HOME` 环境变量更新）：
- `chains/` — 调用链 JSON 文件
- `config.json` — 用户配置

更新 skill-sub 本身（覆盖 SKILL.md + scripts/）**不会影响**数据目录。但注意这个路径不符合铁律4（产出物应在 `skills/.standardization/` 下），后续版本会迁移。

---

## 使用技巧

1. **命名调用链要有规律** — 用「动词+对象」格式（如"发布技能"、"审查代码"），方便 `list` 时快速定位
2. **action 写得越具体，执行越顺畅** — 好：「运行 `sensitive_scan.py scan <skill-name>` 检查敏感信息」；差：「检查安全」
3. **非里程碑步骤优先 `on_exhaust: skip`** — 减少人工介入，除非该步骤的产出被后续步骤强依赖
4. **`tags` 不要随便填** — 它是自动推荐的匹配依据，填 `["通用"]` 等于没填。用领域关键词：`["发布","安全","数据分析"]`
5. **定期清理不用的调用链** — `chain_manager.py list` 检查，`delete --force` 清理。链不是越多越好
6. **里程碑只在"失败不可接受"的步骤用** — 如安全审计、部署上线。中间步骤失败通常可跳过或询问

---

## 常见错误场景

### E1：创建链时报"连续缺口应合并为一个粘连点"

**原因**：两个 `type: "adhesion"` 步骤相邻。粘连点是 skill 之间的连接器，禁止连续。

**解决**：合并为一个 adhesion，用 hybrid 方案覆盖全部缺口。

```json
// 错误：两个连续粘连点
{"index":2,"type":"adhesion","step_name":"审核"},
{"index":3,"type":"adhesion","step_name":"转换"}  // 禁止

// 正确：合并为一个 hybrid 粘连点
{"index":2,"type":"adhesion","step_name":"审核+转换",
 "adhesion":{"reason":"需要人工审核和数据格式转换",
  "solutions":[{"mode":"hybrid","llm_steps":"人工审核",
                "tool_steps":"脚本转换格式"}]}}
```

### E2：创建链时报"引用的 skill 不存在"

**原因**：`skill_name` 对应的 skill 未安装或名称写错。

**解决**：用 `python scripts/skill_extractor.py scan` 查看已安装 skill 列表。

### E3：执行时报"步骤失败"

| 原因 | 现象 | 解决 |
|------|------|------|
| action 描述模糊 | AI 反复确认 | 用具体动词+对象+产出重写 action |
| 依赖的 skill 报错 | skill 本身执行失败 | 单独运行该 skill 确认 |
| 里程碑步骤失败 | 整条链中止 | 修复后重新执行 |
| 重试耗尽 | 超过 max_retries | 检查错误类型后修正重试 |

### E4：校验器阻断保存

| 阻断信息 | 原因 | 解决 |
|---------|------|------|
| 缺少必填字段 skill_name | skill 步骤没有指定 skill | 补充 skill_name |
| 无效类型 'xxx' | type 不在 skill/loop/branch/adhesion 中 | 修正 type 字段 |
| 检测到依赖闭环 | depends_on 形成循环 | 打破循环依赖 |
| 索引重复 | 两个步骤相同 index | 使用 --fix 自动修复 |
