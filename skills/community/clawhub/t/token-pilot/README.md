# token-pilot

> 版本：v3.6.0 | 最后更新：2026-04-20

---

## 🚀 安装后 2 步完成所有设置

### 第 1 步：安装 + 一键初始化

```bash
clawhub install token-pilot
bash ~/.openclaw/skills/token-pilot/scripts/init.sh
```

`init.sh` 先扫描所有 Agent，列出当前行数、注入类型及潜在重叠，**等待你在终端输入 `y` 确认后**才写入 token 优化核心规则（9条，36行）。自动化场景可加 `--yes` 跳过确认。

**也可在对话中触发**：下次对话提及"token"、"优化"、"消耗"等关键词时，Agent 会检测 `.initialized` 标记，若不存在则向你说明注入计划，**等待你同意后**再执行。

---

### 第 2 步：跑一次诊断（5 分钟，只需一次）

```bash
node ~/.openclaw/skills/token-pilot/scripts/audit.js --all
```

只读不改文件，输出中文建议列表。不确定怎么操作，直接说"帮我跑 token-pilot 诊断"，Agent 处理。

---

### 第 3 步（可选）：加周度 Cron 自动巡检

在 `openclaw.json` 的 `cron` 字段中加入：

```json
{
  "kind": "agentTurn",
  "schedule": "0 9 * * 1",
  "message": "运行 token-pilot 周度诊断：帮我检查 token 使用情况，扫描 cron 和 agent 配置有无优化空间，给出摘要建议。",
  "lightContext": true,
  "model": "Qwen/Qwen3-8B"
}
```

不确定怎么改，说"帮我把 token-pilot 周度 cron 加进 openclaw.json"，Agent 来做。每周一早 9 点自动跑，轻量模型，不占主会话 token。

---

## ✅ 覆盖范围：所有 Agent，两层机制并行

### 第一层：核心规则常驻（AGENTS.md 注入，始终生效）

`init.sh` 将以下 9 条规则写入所有 Agent 的 `AGENTS.md`，**每次会话无条件加载，无需触发词**：

| 规则 | 效果 |
|------|------|
| R1：先读前30行，确认再全读 | 避免大文件盲读浪费 |
| R4：不重复读同一文件 | 去除冗余 read 调用 |
| R5：合并无依赖的工具调用 | 减少轮次 |
| R6：小改用 edit，不用 write 全覆盖 | 减少上下文写入 |
| R8：Prompt Cache 保护 | 固定内容稳定，动态内容后置，节省 75% input token |
| R9：机器接收方压缩输出格式 | Cron/Agent 消息不输出装饰性 markdown |
| R10：动态内容分级限制 | 按类型设上限，总比例 <30%，防 cache 失效 |
| 浏览器替代优先级 | API→web_fetch→browser→RPA，选最低消耗路径 |
| 长上下文管理 | 轮数多时主动提示 /compact 或带记忆开新会话 |

注入体积：36行，对 bootstrap token 影响极小。

### 第二层：完整规则按需加载（skill_get，触发词激活）

用户提及 token、优化、消耗、cost 等关键词时，Agent 加载完整 SKILL.md，额外激活：

| 规则 | 效果 | 为何不常驻 |
|------|------|----------|
| R2：工具输出超长时只保留摘要 | 减少工具结果堆积 | 极少数场景用户需要完整原始输出 |
| R3：简单问题短答 | 减少 output token | 用户有时明确需要详细解释 |
| R7：按角色重量裁剪工具使用范围 | 轻角色不开重工具 | 依赖 SOUL.md 分析，按需运行更准确 |

---

## 🔒 落实保障：三层机制

| 层次 | 内容 | 生效方式 |
|------|------|---------|
| **核心规则常驻层** R1/R4-R6/R8-R10 | 注入 AGENTS.md，始终在线 | ✅ 安装后自动，无需触发 |
| **完整规则按需层** R2/R3/R7 + 主动降耗策略 | skill_get 加载 SKILL.md | ✅ 关键词触发后自动 |
| **定期诊断层** audit + optimize 脚本 | 手动或 cron 自动运行 | ⚠️ 首次手动跑一次，之后 cron 自动 |

---

## 🔍 来自 Claude Code 源码分析的优化

以下优化来自对 Claude Code 官方源码的实际读取分析，每条标注来源文件，有工程数据背书。

| # | 优化点 | 来源 | 你需要做的 |
|---|--------|------|-----------|
| 1 | system prompt 禁止动态内容 | `main.tsx` | AGENTS.md/SOUL.md 不加时间戳；进行中事项移出放日记文件 |
| 2 | AGENTS.md 只放稳定内容 | `claudemd.ts` | 任务状态放 memory 日记，项目上下文放 context.md |
| 3 | 动态内容分级上限 | `context.ts` | exec 输出≤2000字符；工具返回≤5000；知识文件≤10KB；总比例<30% |
| 4 | MEMORY.md 改索引结构 | `memdir.ts` | 每行写指针 `- [标题](topics/file.md) — 摘要`，详情放 topic 文件 |
| 5 | feedback 同时记成功经验 | `memoryTypes.ts` | 用户说"对就这样"也要记，不只记纠正 |
| 6 | Cron/subagent 失败最多重试 3 次 | `autoCompact.ts` | 失败就停+告警，禁止无限重试 |
| 7 | Compaction 缓冲设 8000 token | `autoCompact.ts` | `softThresholdTokens: 8000`；压缩后 `/status` 确认在 10K-40K |
| 8 | 通知类 Agent 关掉 cache | `modelCost.ts` | 每次内容不同的 Agent 设 `cacheRetention: "none"` |
| 9 | Subagent 卡死主动 kill | `tokenBudget.ts` | 连续多轮无进展就 kill，不傻等 |

> **工程数据**：第6条——1,279 个 session 发生 50+ 次连续失败，每天浪费约25万次 API 调用。第8条：cache write $3.75/Mtok，比普通 input $3/Mtok 贵 25%，内容不重复开 cache = 纯亏损。

---

## 主动降耗策略（直接告诉 Agent 触发）

| 策略 | 触发方式 |
|------|---------|
| **主记忆重整** — MEMORY.md 积累了临时内容导致冷启动虚高 | "帮我重整记忆索引" |
| **换模型** — 当前任务不需要顶级模型 | "这个任务用便宜点的模型做" |
| **排查异常消耗** — 感觉 token 偏高 | "帮我排查 token 异常消耗" |
| **封装 Skill** — 同一流程重复执行 2 次以上 | Agent 主动提醒，或说"把这个封装成 Skill" |

**浏览器替代优先级**（从低消耗到高消耗）：
① 内部系统 API（联系负责人获取，无截图/DOM）
② web_fetch（公开页面内容抓取）
③ openclaw profile 调用模式（需登录的网站）
④ browser（前三者不可行时）
⑤ RPA 工具（影刀等，固定重复流程，彻底不占 Agent token）

---

## 经实测的 openclaw.json 配置

> ⚠️ 所有字段放在 `agents.defaults` 下，**不是顶层**。写到顶层会导致启动失败。
> 💡 不确定怎么加，说"帮我把 xxx 配置加进 openclaw.json"，Agent 来做。

### 长会话压缩稳定性

```json
"agents": {
  "defaults": {
    "compaction": {
      "mode": "safeguard",
      "memoryFlush": { "enabled": true, "softThresholdTokens": 8000 }
    }
  }
}
```

### Bootstrap 文件大小限制

```json
"agents": {
  "defaults": {
    "bootstrapMaxChars": 12000,
    "bootstrapTotalMaxChars": 20000
  }
}
```

### Heartbeat（维持 prompt cache 不过期）

```json
"agents": {
  "defaults": {
    "heartbeat": { "every": "55m", "activeHours": { "start": "08:00", "end": "23:00" } }
  }
}
```

> 55m 略小于 Anthropic cache TTL（1h），保持缓存活跃，避免重新 cache write 的额外费用。

### 图片 token 控制（可选）

```json
"agents": {
  "defaults": { "imageMaxDimensionPx": 800 }
}
```

### per-agent cache 策略（可选）

```json
"agents": {
  "list": [
    { "id": "main", "params": { "cacheRetention": "long" } },
    { "id": "alerts", "params": { "cacheRetention": "none" } }
  ]
}
```

### 工具白名单（每 Agent 省 4000-8000 tok）

| 角色类型 | 建议白名单 | 可去掉 |
|---|---|---|
| 情报/搜索类 | web_search/web_fetch/read/write/edit/exec/memory_*/message | browser/canvas/tts/feishu_bitable/sessions_spawn |
| 数据分析类 | read/write/edit/exec/web_search/feishu_bitable/memory_*/message | browser/canvas/tts/feishu_wiki |
| 产品管理类 | read/write/edit/exec/web_search/feishu_doc/feishu_bitable/feishu_wiki/memory_*/message | browser/canvas/tts |
| 交付/开发类 | read/write/edit/exec/web_search/web_fetch/browser/sessions_spawn/memory_*/message | canvas/tts/feishu_bitable |

---

## 实时诊断命令

```bash
/status              # 当前 session token 用量 + 预估费用
/usage tokens        # 每条回复后显示 token 用量
/context list        # context 分解（各文件/工具/skill 各占多少）
/context detail      # 详细分解
/compact             # 手动触发 session 压缩
```

---

## AGENTS.md 体积参考

安装本技能 + security-hardening-safey 后，每只 Agent 的 AGENTS.md 约包含：

| 来源 | 行数 |
|------|------|
| security-hardening-safey 注入（安全规则） | 112 行 |
| token-pilot 注入（优化核心规则） | 36 行 |
| Agent 自身原有内容 | 视 Agent 而定 |
| **建议 Agent 自身内容控制在** | **≤ 150 行** |

子 Agent 总 AGENTS.md 建议 ≤ 300 行，主 workspace AGENTS.md 允许更大。保留：启动规则、记忆规则。删除：context-mode 使用说明（系统自动注入）、群聊规则、无关示例代码。

---

## Skill 描述精简建议

OpenClaw 每次对话注入全部已安装 Skill 的 metadata：
- description 控制在 **50 字以内**，只说"什么场景用"
- 不用的 skill 及时卸载：`openclaw skills uninstall <skill-name>`
- 用 `/context detail` 查看 skill list 实际占用 token

---

## 技能协同

| 技能 | 协同方式 |
|---|---|
| `smart-agent-memory` / `memos-local` | memory_search 优先，避免重读文件；解决后立即记录，防止重复调查 |
| `coding-lead` | 大上下文写磁盘 context 文件，ACP prompt 只放最小头部 |
| `qmd` | 检索代替读文件，只在确认需要时再 read |
| `security-hardening-safey` | 两个技能同时注入 AGENTS.md，规则互不干扰，各自独立块标记 |

---

## 卸载

**第一步：移除所有 Agent 的注入规则**

```bash
bash ~/.openclaw/skills/token-pilot/scripts/uninstall.sh
```

脚本移除所有 AGENTS.md 中的 TOKEN-PILOT 规则块，并清除 `.initialized` 标记。幂等安全可重复运行。

**第二步：删除技能目录（可选）**

```bash
rm -rf ~/.openclaw/skills/token-pilot
```

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能主文件（完整行为规则 + 插件协同 + 配置） |
| `references/TOKEN-PILOT-CORE.md` | 注入 Agent 的精简版（9条规则，36行，常驻 AGENTS.md） |
| `references/workspace-patterns.md` | 工作区文件组织最佳实践 |
| `references/cron-optimization.md` | Cron 模型路由指南 |
| `scripts/init.sh` | 核心规则注入脚本（写入所有 Agent 的 AGENTS.md） |
| `scripts/uninstall.sh` | 卸载脚本（从所有 Agent 的 AGENTS.md 移除注入规则） |
| `scripts/audit.js` | 审计脚本（只读，输出建议） |
| `scripts/optimize.js` | 优化建议脚本（含 --apply 自动修复工作区） |
| `scripts/catalog.js` | 技能目录索引生成 |

---

## 更新日志

| 版本 | 日期 | 变更 |
|---|---|---|
| v3.6.0 | 2026-04-20 | 新增"长上下文管理"规则（主动提示 /compact 或带记忆开新会话）；纠正规则数量（7→9条，补录浏览器替代优先级）；注入体积 33→36行 |
| v3.5.0 | 2026-04-20 | 新增 uninstall.sh 卸载脚本；init.sh 自动创建 .initialized 标记；init.sh 增加预览+确认机制；修复 SKILL.md 规则数量描述；修复 cron 示例硬编码 Windows 路径 |
| v3.4.0 | 2026-04-20 | 新增核心规则常驻机制（AGENTS.md 注入，33行，始终生效）；新增 init.sh 和 TOKEN-PILOT-CORE.md；新增主动降耗策略（记忆重整/换模型/浏览器替代层级/异常排查/Skill封装）；README 全面重写，厘清两层生效机制 |
| v2.5.0 | 2026-04-02 | 第二轮源码分析：新增5条（autocompact熔断/compaction 13K缓冲/压缩后10K-40K区间/cache write贵25%/subagent边际递减）；softThresholdTokens从4000调整为8000 |
| v2.4.0 | 2026-04-02 | README 全面重写：覆盖所有 agent 说明 + 落实三层机制 + 源码分析独立章节 |
| v2.3.0 | 2026-04-02 | SKILL.md 新增记忆系统三条规范（MEMORY.md索引结构/记忆四分类/feedback记成功） |
| v2.2.0 | 2026-04-02 | 新增首次加载主动提示 + 周度 Heartbeat cron |
| v2.1.0 | 2026-04-02 | 新增 R10 动态内容分级限制；R8 补充 AGENTS.md 拆分建议 |
| v2.0.0 | 2026-03-31 | imageMaxDimensionPx；per-agent cacheRetention；Skill描述精简；诊断命令 |
