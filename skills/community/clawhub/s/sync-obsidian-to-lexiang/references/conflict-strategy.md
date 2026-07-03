# 冲突策略说明

## 冲突场景

当增量同步时，Obsidian 中的 .md 文件发生了变更（content_hash 变化），
同时乐享知识库中对应的文档也可能被其他人编辑过。
此时需要决定以哪一方的内容为准。

## 策略一：lexiang_wins（乐享优先，默认）

**行为**：当乐享侧文档在上次同步后有独立更新时，忽略 Obsidian 的变更。

**判断逻辑**：
1. 从 manifest 获取该文档的 `last_sync_at`
2. 调用 `entry_describe_entry` 获取乐享侧的 `edited_at`
3. 比较：
   - `edited_at > last_sync_at` → 乐享有独立更新 → **跳过**，保留乐享版本
   - `edited_at <= last_sync_at` → 乐享无独立更新 → **覆盖**，用 Obsidian 内容更新

**适用场景**：
- 乐享知识库是团队协作环境，多人可能在乐享侧编辑
- 需要保护乐享侧的编辑成果不被 Obsidian 的本地修改覆盖
- 适合"Obsidian 做初稿，乐享做协作"的工作模式

## 策略二：obsidian_wins（源端优先）

**行为**：Obsidian 的变更始终覆盖乐享侧内容，不检查乐享侧更新。

**判断逻辑**：
1. 检测到 content_hash 变化 → 直接覆盖更新
2. 不调用 `entry_describe_entry`，不比较时间

**适用场景**：
- Obsidian 是唯一的内容编辑入口
- 乐享仅用于展示和分享，不在乐享侧编辑
- 需要保证乐享内容与 Obsidian 严格一致

## 配置方式

在 config.json 中设置：
```json
{
  "conflict_strategy": "lexiang_wins"
}
```

或通过命令行参数覆盖：
```bash
python3 sync.py --mode incremental --conflict-strategy obsidian_wins
```

## 冲突处理流程图

```
Obsidian 文件变更
       │
       ▼
  content_hash 不同？
   │            │
   否            是
   │            │
   ▼            ▼
  跳过     conflict_strategy?
            │              │
      lexiang_wins    obsidian_wins
            │              │
            ▼              ▼
  乐享 edited_at >     直接覆盖
  last_sync_at?
   │          │
   是          否
   │          │
   ▼          ▼
  跳过      覆盖
```

---

# 其他异常一致性策略

## 中断恢复（幂等）

manifest 在每个写操作成功后立即落盘。中断后重跑增量同步：
- 内容未变（content_hash 命中）→ 跳过
- 已存在的条目（manifest 有 entry_id 且探活存在）→ 不重复创建
- 未完成的 → 继续
保证「不重不漏」。

## entry 失效（目的端被删除）

复用 entry_id 前 `probe_entry` 探活。乐享对已删除/不可访问的 entry 返回 **code=403 或「不存在」**，统一判定为失效 → 清除旧映射并重建。

## 目的端移动（respect_move 开关）

| 配置 | 被移出目标目录时的行为 |
|------|----------------------|
| `respect_move=true`（默认） | 仍更新原 entry，不重建（尊重用户整理） |
| `respect_move=false` | 在目标目录重建一份，旧副本保留（对齐 iwiki 方案 S） |

移动检测依据：`probe_entry` 返回的 `parent_id` 与该条目在目标树中的预期 parent 比对。

## 跨会话并发（文件锁）

manifest 存于 vault 内，跨会话天然共享 → 续传不重不漏。
唯一风险是两个进程**同时**同步同一 vault。

文件锁 `.sync.lock`（与 manifest 同目录）：
- `O_CREAT|O_EXCL` 原子创建，记录 pid + host + 时间戳
- 第二个进程获取失败 → `status: locked`，退出码 2
- 正常/异常/中断均自动释放
- 陈旧锁接管：同机进程已死 / 超 1 小时 / 锁损坏

建议跨会话串行执行，锁仅作兜底。
