# 记忆安全规范（追加到 AGENTS.md 的记忆相关章节）

> 🌐 语言 / Language：默认中文，**语言可选**（可按用户语言改写）。
> ⚠️ 本文件是**建议文本**：是否写进 `AGENTS.md` 由用户决定，技能不自动写入。

## 记忆文件位置（既有体系，勿改变）

- **MEMORY.md** = 长期记忆，位于**工作区根目录**（与 AGENTS.md/SOUL.md 平级），**不在 memory/ 下**
- **memory/YYYY-MM-DD.md** = 日常日志（raw），只放日志
- **distill-config.json** = 蒸馏运行参数，工作区根目录（per-agent 独立）

## 记忆安全红线

1. 蒸馏**不删除**任何记忆文件，只提取和整理
2. 敏感信息（token/密码/密钥）默认跳过不落盘，报告提示
3. 归档 ≠ 删除；删除必须用户明确确认
4. 不自动清理（autoClean 保持 false）；蒸馏不触发 /reset（重置由用户自行决定）
5. 不改 openclaw.json；记忆路径一律按 WORKSPACE.md 走
6. 每个 agent **只处理自己的工作区记忆**；跨 agent 整理需用户明确指令
7. MEMORY.md 含个人上下文 → 只在主会话加载，不在群聊/共享会话加载
