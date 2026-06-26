# Lint 流程（两层：机械扫描 + LLM 整理）

对齐 Karpathy LLM Wiki 模式：**LLM 才是真正的 lint 者**，脚本只做机械扫描和提醒。

示例里的 `$WIKI_ROOT` 默认是 `~/.openclaw/workspace/wiki`，
`$WIKI_SKILL_DIR` 默认是 `~/.openclaw/workspace/skills/wikisage`。

---

## Layer 1：机械扫描（lint.py · cron 每周一 02:00 UTC）

由 `scripts/lint.py` 执行，产出报告到 `$WIKI_ROOT/.lint-history/YYYY-MM-DD.md`。

### 扫描项（6 项对齐 Karpathy 原版）

| # | 检查项 | 谁做 |
|---|---|---|
| 1 | index.md 一致性（有条目但文件不存在 / 有文件但未记录） | 脚本 ✅ |
| 2 | 孤儿页面（没有被任何页面 [[引用]]） | 脚本 ✅ |
| 3 | 缺失概念页（[[链接]] 但无对应文件） | 脚本 ✅ |
| 4 | 缺失交叉引用（A 提到 B 但没建 [[B]] 链接） | 脚本 ✅ |
| 5 | 过时页面（超过 90 天未更新，按 mtime） | 脚本 ✅ |
| 6 | 矛盾内容 / 被推翻的旧说法 / 数据空白 | **LLM**（Layer 2） |

### 定时调度（跨平台）

**Linux / macOS (cron)：**
```cron
0 2 * * 1 WIKI_ROOT=$HOME/.openclaw/workspace/wiki python3 $HOME/.openclaw/workspace/skills/wikisage/scripts/lint.py >> $HOME/.openclaw/workspace/wiki/.lint-history/cron.log 2>&1
```

**Windows（Task Scheduler）**：详见 `README.md` 的 *Weekly lint schedule* 节（用 `python.exe`，而非 `python3`）。

脚本只写报告、打印到 stdout。**要推通知到邮件/聊天/webhook**，加 `--summary` 参数拿到一行摘要再在 cron/Task Scheduler 里自己 pipe，示例见 README。

脚本本身不推通知，只写报告。想要「本周 Lint：X 孤儿、Y 缺失页…」这种推送：
- 跳到 `--summary` 获取一行摘要
- 在你的 cron/Task Scheduler 里 pipe 到那个工具（邮件、Slack webhook、Discord webhook、`openclaw message`、飞书自定义机器人…）

---

## Layer 2：LLM 整理（用户触发 · Agent 执行）

**执行通道**：Layer 2 所有读写 wiki 文件走 **Obsidian MCP**（详见 SKILL.md 执行通道）。
Layer 1 的 `lint.py` 脚本还是走 Python filesystem 直读，速度快、扫描无副作用。


### 触发条件

用户说以下任一关键词 → 进入 Layer 2：
- "整理 wiki"
- "wiki 健康检查"
- "lint"（不加参数）
- "整理 wiki 矛盾"（只跑第 6 项）

### 执行流程

```
Step 1: 读最新 lint 报告
  → exec: ls $WIKI_ROOT/.lint-history/ | tail -1
  → mcporter call obsidian.read_text_file path=<报告文件>
  → 如果找不到报告（cron 还没跑过）：先手动跑 python3 scripts/lint.py --no-log

Step 2: 逐类处理（按优先级）

  【孤儿页面】——通常是漏了从 index.md 或其他页面建链接
    → 每个孤儿：
        - 读页面看内容
        - 判断归属：应该被谁引用？(index.md 肯定要加)
        - 问用户："建议在 X 页面加 [[孤儿]] 链接，同意吗？"
        - 同意 → 改目标页面 + index.md

  【缺失概念页】——[[链接]] 引用了但没文件
    → 按"被引用次数"排序（高频的先处理）
    → 每个：
        - 看引用它的几个页面说了什么
        - 判断：这概念**有独立价值**吗？
          - 有 → 建议新建页面（问用户是否需要）
          - 没（只是随手引用）→ 建议改成普通文字 + 删除 [[]]
          - 是别的页面的别名 → 建议改成正确的 slug

  【缺失交叉引用】——A 提到 B 但没 [[B]]
    → 每个：问"在 X 页面的 Y 章节加 [[B]] 链接吗？"
    → 同意 → 插入链接

  【过时页面】
    → 每个：
        - 读页面内容
        - 是否过时？（时效性强的才算过时，概念性内容不算）
        - 过时 → 建议：更新 / 标注 / 删除
        - 问用户决策

  【矛盾内容】（Layer 2 独有）
    → 扫所有页面，找同一概念/事实的描述
    → 对比发现矛盾
    → 标注 ⚠️ + 问用户哪个是对的
    → 改页面 + 更新 log

  【数据空白】（Layer 2 独有）
    → 扫 wiki 的主题覆盖，找可能缺的重要主题
    → 建议："要不要让我搜 X 然后补一页？"

Step 3: 每改一组，同步更新（全部走 MCP edit_file / write_file）
  - index.md（页面增删）
  - log.md（追加 ## [日期] lint-fix | 做了什么）

Step 4: 收尾
  - 再跑一次 python3 scripts/lint.py --no-log 验证
  - 汇报：改了 N 条，剩余 M 条未处理（不紧急）
```

### 行为原则（重要）

1. **逐项问，不批量改**——每个改动用户确认，避免改坏知识结构
2. **宁可保守**——不确定就问，不要自作主张
3. **链接规范**：slug 统一用小写连字符（`obsidian`、`aws-security-hub`），避免大小写孤儿
4. **改一批同步 index.md 一批**——防止中途出错留脏状态
5. **永远同步更新 log.md**——log 是 wiki 的时间线

---

## 轻量 lint（ingest 后自动触发）

```bash
python3 $WIKI_SKILL_DIR/scripts/lint.py --quick
```

只查 index.md 一致性，防止 ingest 留脏。ingest 流程最后一步可调用。

---

## 报告归档

```
$WIKI_ROOT/.lint-history/
├── 2026-04-18.md          ← 今天的报告
├── 2026-04-20.md          ← cron 下周一产出
├── 2026-04-27.md
└── cron.log               ← cron 运行日志（stderr 也在这里）
```

如果 wiki 被 Mutagen/git 同步到本地编辑器（Obsidian/VS Code 等），用户在本地也能直接翻历史报告。

---

## 执行频率

- Layer 1（脚本）：**每周一 02:00 UTC** 自动
- Layer 2（LLM）：**用户触发** —— 看到周报通知后决定是否整理
- Ingest 后：**自动 --quick**（轻量 lint 防脏）
