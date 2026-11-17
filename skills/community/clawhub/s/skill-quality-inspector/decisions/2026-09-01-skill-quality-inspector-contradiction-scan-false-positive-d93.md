# D93 — contradiction_scan.py 误报修复（命令实跑发现）

**日期**: 2026-09-01
**仓库**: skill-quality-inspector（Level A/100，维持 A）
**类别**: (C) 增量迭代 — 周级升阶抽查的「命令实跑」发现真实缺陷
**触发**: 自动化维护轮转指针指向本仓库；按 D86 升级口径对 3 个脚本做命令实跑，发现 `contradiction_scan.py --repo .` 在**自家仓库**上 `fail=28 warn=19`。

## 根因

扫描器对自身仓库内容产生大量误报（误报同属 bug，见本仓库核心原则 #6）：

1. **`term_drift` 同义术语映射错误**
   `TERM_MAP` 把正确术语当成"漂移"：
   - `"路由表" → "能力索引"`：`路由表` 是 superpower 根 SKILL.md 路由表的**标准叫法**，非笔误；
   - `"playbook" → "参考手册"`：`playbook` 是方法论文档的英文标准词，非笔误。
   二者均被错误标红。

2. **`broken_link` 用裸路径正则 `REF_RE` 匹配示例/说明性路径**
   `REF_RE = (?:references|scripts|assets)/[A-Za-z0-9_./-]+` 匹配正文中**任何** `references/...`、`scripts/...`、`assets/...` 片段，包括方法论文档里的示例与说明（如 `抓 \`references/...\``、`\`scripts/x.py\``、`references/scripts 存在但…`）。这些不是真实链接，却被当作断链 → 大量 phantom broken_link。

3. **`numeric_mismatch` 在全部 .md 里逐项比对数字**
   `references/`、`skills/`、`decisions/` 等文档中的**示例数字 / 历史规划数字**（如"声称 6 个references""声称 3 个子技能"）被当成对仓库结构的"声称数" → 9 条误报。

4. **`iter_md` 把 `tests/` 合成自检样本算作仓库内容**（且 `continue` 未阻止 os.walk 下钻，导致 `tests/` 子树仍被扫）。

## 修复（`scripts/contradiction_scan.py` + `references/contradiction-detection.md`）

| 项 | 改动 |
|----|------|
| `TERM_MAP` | 删除 `路由表→能力索引`、`playbook→参考手册` 两条错误同义映射；仅保留真正的写法错误（`A级/Lv A → Level A` 等） |
| `broken_link` | 去掉 `REF_RE`，**只校验真正的 Markdown 链接 `[文本](references|scripts|assets/...)`**；文档示例/说明路径不再误判 |
| `numeric_mismatch` | 只在 `README.md` 与根 `SKILL.md` 里校验结构数（这才是仓库显式声明数的位置），不再扫 `references/`、`skills/`、`decisions/` 的示例数字 |
| `iter_md` | 仅在被扫描根目录**直属**的 `tests/` 处从 `dirs` 裁剪（阻止下钻）；显式 `--repo tests/sample_bad` 仍可正常扫描，保证自检样本持续有效 |
| `contradiction-detection.md` 二-2 | 同步修正"断链"描述，声明现仅校验 Markdown 链接 |

## 验证（命令实跑）

- 自身 `--repo .`：`fail=28 → 0`，`warn=2`（仅剩 2 处文档**教学示例**中出现的 "A 级" 例句，属 WARN 级良性噪声，不影响门禁 rc=0；保留以保教学清晰度）。
- `tests/sample_good` → rc=0；`tests/sample_bad` → rc=1（仍命中真实断链 + 数字对账，自检样本有效）；`tests/sample_org` 经 `redundancy_scan` → rc=1（跨仓库重名检测有效）。
- `quality_audit.py --repo .` → 12 pass / 0 fail。
- 双门禁：`audit_architecture --repo skill-quality-inspector --strict` A/100 退出 0；`audit_readme_gates --repo skill-quality-inspector --strict` error=0/warning=0 退出 0；全组织 `--strict` 退出 0（A=24 B=11 平均 93）。

## 结论

Level 维持 A（结构/脚本/资产要素未变，仅修正脚本误报逻辑）。本次为内容/逻辑正确性修复，组织审计平均分不变（93）。

## 遗留（保守留待人工）

- 2 处 `term_drift` WARN 为文档教学例句中的 "A 级"；若要彻底清零可改写例句，但会削弱"术语漂移"概念的教学直观性，故保留并标注。
- 是否将「命令实跑 + 误报普查」固化为 maintenance.md 的 W6/W7 标准动作（D86 已提，待人工）。
