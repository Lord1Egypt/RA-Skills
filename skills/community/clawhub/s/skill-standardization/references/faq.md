# 常见问题（FAQ）

> 本文件收集 skill-standardization v2 使用过程中的常见疑问和解答。
> 按「使用场景 → 技术细节 → 最佳实践」组织。

---

## 目录

1. [基础概念](#基础概念)
2. [create 模式](#create-模式)
3. [update 模式](#update-模式)
4. [refactor 模式](#refactor-模式)
5. [审查与规范](#审查与规范)
6. [渐进式 MD 体系](#渐进式-md-体系)
7. [版本管理](#版本管理)
8. [集成与扩展](#集成与扩展)

---

## 基础概念

### Q1: 什么是 SKILL.md 标准化规范？

**A:** 这是 skill-standardization 的核心规范——一套定义了标准 Skill 文件应如何编写的规则体系（v2+）。主要包含：

- **Frontmatter 规范**：3 个必须字段（name/version/description）+ 7 个可选字段
- **正文结构规范**：三层体系（must_have 必须章节 / whitelist 白名单章节 / nonstandard 非标章节）+ 渐进式索引表
- **审查规则**：R-01~R-26 共 25 条自动检查规则（含安全审计、写作规范、章节顺位、格式合规等）

该规范定义在 `scripts/spec/frontmatter.json`、`scripts/spec/body.json` 和 `scripts/spec/rules.json` 中，可直接查看 `scripts/spec/` 下的 JSON 文件。

### Q2: skill-standardization 可以独立使用吗？

**A:** 可以。skill-standardization 是一个独立审查工具，不依赖任何其他技能：

```
-m scripts.skill_audit audit <skill-dir>
  ├─ R-01~R-26 规则检查
  └─ 输出审查报告
```

它可以直接对任意 skill 目录执行审查，适合在 CI/CD 或手动工作流中调用。

### Q3: 「三级复杂度」是什么意思？

**A:** 标准 Skill 目录结构支持三种复杂度级别：

| 级别 | 内容 | 适用场景 |
|------|------|---------|
| **minimal** | 仅 `SKILL.md` + `_meta.json` | 纯提示型 skill（如 color-toolkit） |
| **standard** | + `scripts/` + `references/` | 有脚本或辅助文档的 skill |
| **full** | + `assets/` + `tests/` | 复杂工具型 skill |

大多数 skill 属于 standard 级别。

---

## create 模式

### Q4: 创建后的 SKILL.md 有很多 TODO，我需要全部填完吗？

**A:** 不需要全部立即填完，但建议至少完成以下必填项：

**必须填写的 TODO：**
1. `description` — frontmatter 中的描述（create 时通过 --desc 可预设）
2. `触发场景` 章节 — 明确何时触发此 skill
3. `核心能力` 表格 — 列出至少 1 个核心功能
4. `快速开始` — 提供最简使用示例

**可以后续补充的：**
- 详细教程 → 拆分到 `references/guide.md`
- 示例集合 → 拆分到 `references/examples.md`
- FAQ → 拆分到 `references/faq.md`

### Q5: create 生成的版本号为什么是 0.1.0？

**A:** 这是有意设计。按照 SemVer 规范：

- `0.x.y` 表示初始开发阶段，API 可能不稳定
- 首次正式发布时应升级到 `1.0.0`
- create 模板的 `0.1.0` 是起点，后续由开发者根据实际更新升级

### Q6: 可以自定义 create 模板吗？

**A:** create 模板位于 `scripts/skill_audit` 中 `cmd_create` 的 fallback 骨架代码。当前模板已对齐 v2.91.0+ 规范：

- 包含 `## 约束` must_have 章节
- 核心能力末尾含 `### 渐进式文件索引` 表格
- references/ 引用通过索引表统一管理

要更新模板：更新 `creator.py` 中 `SKILL_TEMPLATE` 字符串后保存即可。

---

## update 模式

### Q7: update 和 refactor 怎么选？

**A:** 简单判断：

| 场景 | 选择 |
|------|------|
| 已基本标准，想检查是否有遗漏 | `update` |
| 结构混乱、根目录散落文件多 | `refactor` |
| 不确定 | 先 `update` 看报告，再决定 |

update 是**轻量检查**（只读+可选修复），refactor 是**重量改造**（移动文件+重组目录）。

### Q8: update --fix 会更新哪些内容？

**A:** 当前 --fix 自动修复以下项目：

| 修复项 | 动作 |
|--------|------|
| `_meta.json` 缺失 | 创建新的 _meta.json（含默认值） |
| `_meta.json` 缺少字段 | 补充空值（tags 为空数组） |
| 描述/标签同步 | description/tags 从 _meta.json 同步到 SKILL.md frontmatter |
| 渐进式索引表 | 扫描 references/ 自动生成/更新索引表 |
| 约束章节 | 从目标技能脚本采集约束规则 |
| 章节重排 | 按 section_order 重排章节顺序 |

**不会自动更新的：**
- 缺失的 must_have 章节（仅提示）
- 非标章节归类（由 LLM Phase 2 判断后调用 fix_reclassify_section）

### Q9: update 报告中的 ERROR/WARN/PASS 是什么意思？

**A:**

| 类型 | 含义 | 说明 |
|------|------|------|
| **PASS** (✅) | 该项检查完全通过 | — |
| **WARN** (⚠️) | 存在格式/结构不规范条目 | 由 LLM 二次筛归类（真问题或误报） |
| **ERROR** (❌) | 存在严重结构性问题 | 由 LLM 二次筛归类（真问题或误报） |
| **💡** | 改进建议（非规则） | — |

> 审计报告输出仅描述问题本身、发生位置与级别（WARN/ERROR），不附加"必须修复""建议修复"等程度判断。问题分类（真问题/误报）由 LLM 二次筛统一判定。

---

## refactor 模式

### Q10: refactor 会删除我的文件吗？

**A:** 不会！refactor 的核心设计原则是**信息零遗漏**：

- ✅ 仅执行 `move`（移动）操作
- ❌ 绝不执行 `delete`（删除）操作
- ✅ 执行前强制备份（除非显式 `--no-backup`）
- ✅ 移动后验证总字节一致性（允许 1% 容差）

如果验证发现文件总大小差异超过 1%，会输出警告提示可能丢失。

### Q11: 何时使用 --dry-run？

**A:** **几乎每次 refactor 都应先用 --dry-run！**

dry-run 会输出完整的迁移计划但不执行任何实际操作，让你确认：
- 哪些文件会被移动到哪里
- 哪些文件会保留在原位及原因
- 是否有意外情况

确认计划无误后再删除 `--dry-run` 正式执行。

### Q12: refactor 后如何回滚？

**A:** refactor 默认会创建时间戳命名的备份目录：

```bash
# 备份位置示例：
./my-skill_bak_refactor_20260522_190000/

# 回滚方法（用备份覆盖当前目录）：
mv ./my-skill_bak_refactor_20260522_190000 ./my-skill
```

> 如果用了 `--no-backup`，则无法自动回滚！

## 审查与规范

### Q14: R-01~R-26 是 ERROR 级，会阻断工作流吗？

**A:** 不会！自 v2.0 起，所有审查结果均为**纯警告模式**：

- 即使有 ERROR 级问题，`-m scripts.skill_audit` 也始终返回退出码 `0`
- 后续操作是否继续由调用方决定
- 审查报告会明确标注每个问题的严重程度供参考

这个设计的目的是**不阻断工作流**，让用户自行决定何时修复。

### Q15: 如何理解「同义词匹配」？

**A:** 审查规则中的章节检查使用模糊匹配。例如「触发场景」章节的匹配关键词包括：

`触发条件`, `触发场景`, `适用场景`, `触发`

只要 H2 标题包含其中任一关键词即视为通过。这允许一定的命名灵活性，同时保持语义一致性。

完整同义词表见 SKILL.md 中「审查规则」章节的同义关键词表格。

### Q16: 审查规则可以自定义吗？

**A:** 当前版本规则定义在 `spec/rules.json` 中，是静态 JSON 配置。要自定义规则：

1. 更新 `spec/rules.json`
2. 添加/更新规则条目
3. 对应更新 `spec/_index.json` 的模块注册

> 未来版本计划支持外部规则文件加载。

---

## 渐进式 MD 体系

### Q17: references/ 下的文件是必需的吗？

**A:** 不是。渐进式 MD 文件的设计原则是：

> **SKILL.md 必须可独立理解核心功能和使用方法。references/ 下的文件是按需加载的补充材料，缺失不影响基本使用。**

对于 minimal 级别的 skill，可以完全不创建 references/ 目录。
对于 standard/full 级别，建议至少有 `guide.md`。

### Q18: SKILL.md 超过 230 行怎么办？

**A:** audit 检查时会提示超过 230 行需要拆分。按三层体系优先级拆分：

1. **优先拆 whitelist_optional 章节**（反模式/FAQ/配置/示例等）——它们可留在 SKILL.md 也可拆到 references/
2. **always_progressive 章节**（版本日志）——永远在 references/，SKILL.md 只留 → 详见引用
3. **非标章节**——直接拆分到 references/
4. **must_have 章节**（H1/触发条件/核心能力/工作流程/约束）——永远留在 SKILL.md，不拆分

引用语法示例：
```markdown
→ 详见 `references/guide.md` 完整教程
→ `references/examples.md` 包含更多使用示例
```

### Q19: 渐进式文件的命名有规定吗？

**A:** 推荐使用以下标准命名（也是 progressive_md.json 中注册的标准文件）：

| 文件名 | 用途 |
|--------|------|
| `guide.md` | 详细教程 / 使用指南 |
| `examples.md` | 示例集合 / 用例库 |
| `reference.md` | API 参考 / 命令手册 |
| `faq.md` | 常见问题 / 疑难解答 |
| `changelog.md` | 版本更新日志 |
| `architecture.md` | 架构设计 / 模块说明 |

也可以根据 skill 特点增减文件，但建议保持命名一致性以便 AI 加载识别。

---

## 版本管理

### Q20: 版本号出现在哪些地方？需要全部保持一致吗？

**A:** 是的，以下是完整的版本号位置清单：

| # | 位置 | 说明 | 格式 |
|---|------|------|------|
| 1 | `SKILL.md` frontmatter `version:` | 主版本号 | SemVer（如 `2.0.0`） |
| 2 | `_meta.json` `"version"` | 元数据版本 | 与 SKILL.md 一致 |
| 3 | `manifest.json` `"version"`（如有） | 仓库注册版本 | 与上述一致 |
| 4 | 各 `spec/*.json` 的 `"_version"` | 规范文件自身的版本 | 通常跟随主版本 |
| 5 | `python -m scripts.skill_audit` CLI | 工具自身版本标识 | `vX.Y.Z` |
| 6 | `-m scripts.skill_audit` 自述字符串 | 工具自身版本标识 | `vX.Y.Z` |

**位置 1-3 必须严格一致**（三方一致原则）。位置 4-6 跟随主版本号更新即可。

### Q21: 如何正确升级版本号？

**A:** 按照 SemVer 规范：

| 更新类型 | 示例 | 说明 |
|---------|------|------|
| Patch（补丁） | `2.0.0` → `2.0.1` | Bug 修复，无功能变化 |
| Minor（次版） | `2.0.0` → `2.1.0` | 新增向后兼容的功能 |
| Major（主版） | `2.0.0` → `3.0.0` | 不兼容的重大更新 |

升级步骤：
1. 更新 `SKILL.md` frontmatter 中的 version
2. 同步更新 `_meta.json` 中的 version
3. 如有 manifest.json，同步更新
4. 更新 spec/*.json 的 `_version`（如规范本身有变化）
5. 更新各脚本的自述字符串
6. 在 changelog.md 中记录更新内容

---

## 集成与扩展

### Q22: 可以在其他 Python 项目中导入这些脚本吗？

**A:** 可以，但需注意：

- 脚本设计为 CLI 工具（通过 `if __name__ == "__main__"` 入口）
- 函数级别的导入是安全的（如 `load_spec()`、`cmd_update()` 等）
- 所有依赖都是 Python 标准库，无第三方包

导入示例：
```python
import sys
sys.path.append("path/to/skill-standardization/scripts")
from scripts.skill_audit.__init__ import cmd_create, cmd_update, cmd_refactor
```

### Q23: 如何为新 skill 编写 spec JSON？

**A:** 如果要扩展规范体系（例如新增一种检查维度），需要：

1. 在 `scripts/spec/` 下创建 `.json` 文件
2. 在 `spec/_index.json` 的 `modules` 数组中注册

JSON 文件的推荐结构：
```json
{
  "_version": "1.0.0",
  "_description": "简要描述",
  "_depends_on": ["frontmatter"], // 可选的依赖声明
  // ... 具体规范内容
}
```

### Q24: Windows 上路径斜杠有问题吗？

**A:** 脚本内部统一使用 `pathlib.Path` 处理路径，自动适配操作系统：

- Windows: `C:\Users\...` → 内部转为 Path 对象
- Linux/Mac: `/home/...` → 同上
- 输出路径显示时使用正斜杠 `/` 保持跨平台一致

CLI 参数传入的路径（反斜杠）会被 pathlib 自动规范化。

---

## 常见错误处理

### Q25: 审计报 "⛔ 未传入 --confirmed 参数，拒绝执行"

**A:** 这是**语义门禁**在生效——所有 audit/create/update/refactor 操作必须显式传 `--confirmed` 才能执行。

```bash
# ❌ 会被阻断
python -m scripts.skill_audit audit <skill-dir>

# ✅ 正确
python -m scripts.skill_audit audit <skill-dir> --confirmed --mode audit
```

### Q26: 运行 audit --verify 后 exit(1)，但报告里全是误报

**A:** 先检查报告底部是否有 `#ID` 编号的 FAIL 条目。如果有实心 FAIL 项：
- **真问题** → 运行 `--show-fix ID` 获取修复指引
- **误判** → 运行 `--classify ID` 标记为误报，之后审计会自动过滤

如果确实全是已标记的误报，确认 `_reclassify_false_positive()` 是否覆盖了该模式。新发现的误判模式请联系开发者补充。

### Q27: git push 到 GitHub 报 443 超时

**A:** 这不是 skill-standardization 的问题，是网络环境导致的 GitHub 连接失败。常见原因和解决方法：

| 原因 | 解决 |
|------|------|
| 网络代理未配置 | 配置 git 代理：`git config --global http.proxy http://127.0.0.1:7890` |
| DNS 污染 | 使用 `ssh` 协议替代 `https`，或更新 hosts 文件 |
| 防火墙限制 | 尝试切换到 SSH 方式推送，或使用 Gitee 镜像仓库 |

### Q28: "规则 R-XX 执行异常"是什么？

**A:** 这是审计器在运行某条规则时 Python 代码抛出了未预期的异常。终端输出会附带完整的 traceback 信息，常见原因：

| 原因 | 解决 |
|------|------|
| SKILL.md YAML 格式损坏 | 检查 frontmatter 的 `---` 闭合和缩进 |
| 文件编码非 UTF-8 | 确保文件保存为 UTF-8 编码 |
| 脚本内部 bug | 查看 traceback 定位具体哪行代码崩溃 |

traceback 行数多不要慌，关注最后几行（`File "...", line XX`）即可定位问题文件。

### Q29: refactor 步骤卡在修复循环中，一直无法退出

**A:** 修复循环有内置上限——update 最多 10 轮，refactor 最多 20 轮，超限后自动 exit(1) 阻断。

如果循环反复失败：
1. 检查是否在修**不可自动修复的规则**（R-23/R-25 需要 LLM 手动编辑，`--fix` 修不了）
2. 脚本检测到剩余 R-23/R-25 项时，会以 `exit(2)` 退出并保存 `.remaining_llm.json`
3. **LLM 闭环修复流程**：
   - 读取 `.remaining_llm.json`（位于 `.standardization/skill-standardization/data/<skill>/outputs/`）
   - 逐条编辑 SKILL.md（R-23: 文档一致性 / R-25: 写作规范）
   - 重新运行: `python -m scripts.skill_audit refactor <skill-dir> --confirmed --mode refactor`
   - 针对性审计确认后自动继续到全量审计 → 双0 通过
4. 备用：也可以运行 `audit <skill-dir> --show-fix ID` 获取每条 FAIL 的具体修复指引

### Q30: Windows 上文件写入报 "Permission denied"

**A:** safe_io.py 内置了 3 次重试 + `shutil.move` 降级机制。如果仍失败：

```bash
# 检查文件是否被其他程序占用
# 常见原因：文件已在 vscode/记事本/资源管理器中打开
```

关闭占用程序后重新运行即可。safe_io 的重试逻辑（v2.73.8+）会自动处理临时文件锁。

---


