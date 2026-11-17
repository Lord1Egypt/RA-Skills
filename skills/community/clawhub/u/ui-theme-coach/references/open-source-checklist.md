# 开源前检查清单（Agent Skills 标准 · Markdown skill 通用版）

> **用途**：skill 发布/开源前自查。本次服务 8/20 开源的 openclaw-ui-theme-coach / feedback-loop-xiaoliu，以后新 skill 复用。
> **依据**：agentskills.io「Agent Skills 标准」（对照 Prime Agent `packages/coding-agent/docs/skills.md` 实现提炼，2026-08-16）。
> **用法**：发布前逐项跑一遍。**FAIL 必改**（缺 description 是唯一「不加载」级硬失败）；WARN 尽量改。文末附自动化检查脚本，可直接跑出 PASS/FAIL 表。
> **范围**：只覆盖通用 Markdown skill。Python-backed skills 不适用（见 §三，仅一行注记）。

## 一、硬性必查（FAIL = 不合规）

### 1. name（7 条规则，全过才算 PASS）

| # | 规则 | 反例 |
|---|------|------|
| 1 | 1-64 字符 | 空、超长 |
| 2 | 只允许小写 a-z、0-9、连字符 `-` | 大写 / 下划线 / 空格 / 中文 |
| 3 | 无前导连字符 | `-pdf` |
| 4 | 无尾随连字符 | `pdf-` |
| 5 | 无连续连字符 | `pdf--processing` |
| 6 | **必须匹配父目录名** | 目录 `my-skill/` → name 必须是 `my-skill` |
| 7 | 合法示例：`pdf-processing` / `data-analysis` / `code-review` | `PDF-Processing` |

### 2. description（必填，≤1024 字符）

- **缺失 = 按标准直接不加载**——全部规则里唯一的硬失败项；其余违规（name 不匹配/超长/非法字符/描述超长）都是「警告但仍加载」，开源品质要求清零警告。
- 内容要求：**做什么 + 何时用**，具体到能据此决定「什么任务该加载这个 skill」。
- **Good**：
  ```yaml
  description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents.
  ```
- **Poor**（空泛 → agent 不知道何时加载）：
  ```yaml
  description: Helps with PDFs.
  ```
- OpenClaw 习惯：触发词直接写进 description（如「触发词：主题、换皮、皮肤」），匹配更准。

### 3. frontmatter 格式

- 必须在 SKILL.md **最顶部**，`---` 包裹，YAML 可解析（name 值纯小写连字符可不加引号，加引号也不违规）。
- 标准可选字段：`license` / `compatibility` / `metadata` / `allowed-tools` / `disable-model-invocation`。
- 未知字段按标准忽略（无害）：OpenClaw 侧自带的 `version`/`emoji`/`categories`/`tags` 属此类，不影响标准合规；ClawHub 发布以其自身校验为准（`clawhub skill publish --dry-run`）。

### 4. 结构

- skill 目录顶层必须有 `SKILL.md`；其余自由（惯例：`scripts/` + `references/` + `assets/`）。
- SKILL.md 内引用一律用相对路径（`references/xxx.md`、`scripts/xxx.sh`）。

## 二、Progressive disclosure（设计原则，非必查项）

- 只有 name + description **常驻**系统上下文，正文按任务匹配才加载 → description 就是 skill 的「门面」，值得反复打磨。
- 正文越长越该拆：流程骨架留 SKILL.md，详细文档进 `references/`，脚本进 `scripts/`。单文件小 skill（<10K）全在正文也可接受。

## 三、Python-backed skills —— 不适用注记

> `pyproject.toml` + `src/<import_name>/__init__.py` + IPython 内核内 `await skill_name(...)` callable 是 Prime Agent 的 IPython 特有机制，**OpenClaw 不吃这套**。开源到 OpenClaw 生态保持纯 Markdown + scripts/ 即可，本清单不覆盖该机制。

## 四、实测记录（2026-08-16 跑，两 skill 三份 SKILL.md）

| 检查项 | theme-coach | feedback-loop（本地） | feedback-loop（开源副本） |
|---|---|---|---|
| SKILL.md 在目录顶层 | ✅ | ✅ | ✅ |
| frontmatter 存在且 YAML 可解析 | ✅ | ✅ | ✅ |
| name 1-64 字符 | ✅（23） | ✅（21） | ✅（13） |
| name 仅小写/数字/连字符 | ✅ | ✅ | ✅ |
| name 无前导/尾随/连续连字符 | ✅ | ✅ | ✅ |
| **name 匹配父目录名** | ✅ | ✅ | ❌ `feedback-loop` vs 父目录 `open-source` |
| description 必填 | ✅（133 字符） | ✅（167 字符） | ✅（167 字符） |
| description ≤1024 | ✅ | ✅ | ✅ |
| description Good 标准（做什么+何时用） | ✅ | ✅ | ✅ |
| 缺 description 不加载风险 | 无 | 无 | 无 |

附查：开源副本去个人化 ✅（个人词零命中，示例已泛化为「用户/某案例」）。

## 五、不符合项修复建议

1. **❌ P0（发布前必改）feedback-loop 开源副本 name 不匹配父目录**。本地使用不受影响（本地版 name 正确）。修复：打包时把 `open-source/SKILL.md` 提升到新仓库根，**目录/仓库名必须叫 `feedback-loop`**（把 name 改成 `open-source` 不推荐，会丢语义）。防再犯一行检查：`[ "$(basename "$(dirname SKILL.md)")" = "<name>" ]`。
2. **🟡 WARN（可选）feedback-loop 正文 107 行全在 SKILL.md**：按 §二 可把「效果实测/示例」挪 `references/examples.md`；8K 小 skill 不拆也合规，按开源后反馈决定。
3. **🟡 WARN（可选）description 标点混用**（中文逗号 + 半角括号 + 英文逗号混排）：不影响加载，发布前顺手统一。

## 六、自动化检查脚本（复用）

```bash
python3 - << 'EOF'
import re
try:
    import yaml
except ImportError:
    print("WARN: 缺 pyyaml（pip install pyyaml）"); raise SystemExit(1)
# 每个 skill 三要素：(标签, SKILL.md 路径, 期望的父目录名)
CASES = [
    ("theme-coach",            "SKILL.md", "openclaw-ui-theme-coach"),
    ("feedback-loop-local",    "SKILL.md", "feedback-loop-xiaoliu"),
    ("feedback-loop-open",     "SKILL.md", "feedback-loop"),   # 打包后目录名
]
for label, path, dirname in CASES:
    print("=" * 50); print(f"## {label}")
    text = open(path, encoding="utf-8").read()
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        print("  FAIL: 无 frontmatter"); continue
    data = yaml.safe_load(m.group(1))
    name, desc = data.get("name"), data.get("description")
    fails = []
    if not name:                      fails.append("name 缺失")
    if name and len(name) > 64:       fails.append(f"name 超 64（{len(name)}）")
    if name and not re.fullmatch(r'[a-z0-9-]+', name): fails.append("name 含非法字符")
    if name and (name[0] == '-' or name[-1] == '-'): fails.append("name 前导/尾随连字符")
    if name and '--' in name:         fails.append("name 连续连字符")
    if name != dirname:               fails.append(f"name({name!r}) != 父目录({dirname!r})")
    if desc is None:                  fails.append("description 缺失【不加载级硬失败】")
    if desc and len(desc) > 1024:     fails.append(f"description 超 1024（{len(desc)}）")
    print(f"  name={name!r}  desc_len={len(desc or '')}")
    print("  -> ALL-PASS ✅" if not fails else "  -> FAIL ❌\n     " + "\n     ".join(fails))
EOF
```

> 输出逐项标 PASS/FAIL 并说明具体违规。注意第三行的期望目录名是**打包后**的目录名（开源副本发布时目录要叫 `feedback-loop`，见 §五 P0）。

> 用法：cd 到 skill 目录后跑（或把 path 换成绝对路径）。原理 = 本清单 §一 的四段：frontmatter 解析 → name 五规则 + 目录名匹配 → description 长度 → 缺 description 硬失败。跑完对照 §四 的表格看有没有回退。
