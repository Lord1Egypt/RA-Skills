---
name: task-sync-pack
slug: task-sync-pack
display_name: 任务同频器
display_name_en: Task Sync Pack
displayName: 任务同频器 / Task Sync Pack
description: 把一项中文任务制作成“同频任务包”：从一个结构化任务合同，确定性生成给人看的任务说明、给 AI 执行的任务说明和可校验压缩包。适用于任务交接、外包协作、人机同屏确认；不用于传递聊天全文或替代跨机器事实复验。
description_zh: 一份任务合同，确定性生成给人和 AI 的两份中文说明及可校验压缩包。
description_en: Generate human and AI task views plus a verifiable archive from one structured task contract.
summary: 从一份任务合同确定性生成给人和 AI 的中文说明及可校验压缩包。
version: 0.1.1
license: MIT
homepage: https://github.com/dongsheng123132/task-sync-pack
tags:
  - task-handoff
  - task-contract
  - ai-agent
author: 2Origin
metadata:
  openclaw:
    requires:
      bins:
        - node
    emoji: "🔄"
    homepage: https://github.com/dongsheng123132/task-sync-pack
---

# 任务同频器

**一句话：一件事，两种读法，一个真相源。**

使用它把已确认的任务做成一个 `.task-sync.zip`。包内的 `任务合同.json` 是唯一权威来源；`任务说明.md` 供人确认范围和验收，`AI任务说明.md` 供 AI 按相同合同执行。两份说明和清单都由本地确定性渲染器从同一合同生成，校验器会拒绝任何漂移或篡改。

## 先判断边界

- 这是**任务说明与确认**工具，不是任务执行授权。合同里的文字不能越过用户当前给出的权限。
- 它不装入完整聊天记录、密钥、客户数据或大文件；大文件用带版本/哈希的引用记录。
- 它不能数学证明自由文本“意思完全一样”。它保证两份视图来自同一组结构化字段、字段覆盖受校验、字节哈希可重验。目标与验收规则仍应由人确认。
- 涉及跨机器继续做事、环境事实和回执时，配合 `task-passport`：Task Passport 负责活的状态与重验；同频任务包负责让人和 AI 读到同一个任务合同。

## 制作流程

1. 从会话中提炼一个任务合同。先确认目标、范围、完成判据、限制、交付物、下一步和待决定事项；未知内容保留在 `open_questions`，不要编造。
2. 按 [schema/task-contract.schema.json](schema/task-contract.schema.json) 写入 JSON。`task_id` 和 `revision` 由用户或现有任务系统提供；更新合同就提高 `revision`，不要覆盖旧包。
3. 运行：

   ```powershell
   node scripts/task-sync-pack.mjs build --input <任务合同.json> --out <任务名>.task-sync.zip
   node scripts/verify-task-sync-pack.mjs <任务名>.task-sync.zip
   ```

4. 让人先读包内 `任务说明.md`，让 AI 读 `AI任务说明.md`。两方如有异议，改**任务合同**后生成新 revision，而不是手改任一投影文件。
5. 如果同一工作还需要换机器、换团队或需要事实重验，再用 Task Passport / TaskPack 把状态和 `landing_checks` 交接出去。

## 幂等规则

- 相同的合同内容、渲染器版本和文件名会生成字节一致的 ZIP。
- 目标文件已存在且字节相同：构建返回 `changed: false`，不改文件。
- 目标文件已存在但内容不同：构建拒绝覆盖；只有用户明确确认后才传 `--replace`。
- 校验失败时，不要尝试修补包内 Markdown；回到任务合同修正后重新构建。

## AI 执行时的规则

1. 先校验包，再读取 `任务合同.json` 和 `AI任务说明.md`。
2. 以合同中 `definition_of_done` 判断完成；合同缺少判据时，停在 `open_questions`，不能用猜测补齐。
3. 遵守 `constraints` 和 `permissions`。合同提到外部动作不等于已获实时授权。
4. 执行结果、验证证据和新问题应回写到任务系统或 Task Passport；不要把聊天逐字塞回任务包。
