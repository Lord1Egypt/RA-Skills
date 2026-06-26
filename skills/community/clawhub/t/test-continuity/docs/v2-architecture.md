# V2 Architecture — Event Store + Hook Store 雙層結構

## 概念

```
使用者對話 → 事件偵測 → Event Store → (條件成立) → Hook Store → 排程/dispatch
                                    ↓
                              Runtime Context → 新對話承接 / 時間感知 / 因果鏈
```

**Event**（事件）= 發生了什麼、為什麼要追、現在什麼狀態、下次怎麼接。
**Hook**（鉤子）= 什麼時候做什麼、dispatch 排程、render 輸出。

## Event Store Schema

檔案：`workspace/personal-hooks/events.json`

```json
{
  "version": 1,
  "updated_at": "ISO timestamp",
  "events": [
    {
      "event_id": "EVT-YYYYMMDD-HHMMSS-xxxxxx",
      "event_type": "defer | wake_followup | checkin | reminder_intent | unresolved_topic | health_event | emotional_event | work_event | relationship_event | task_progress | incident | custom",
      "title": "人可讀的事件標題",
      "status": "active | parked | due | completed | cancelled | superseded",
      "priority": "low | medium | high | critical",
      "owner": "system | user | agent",
      "cause_summary": "為什麼這件事存在",
      "desired_followup": "希望怎麼追",
      "source_session": "產生這個事件的 session key",
      "source_channel": "direct | web | ...",
      "source_turn_range": "產生的對話回合範圍",
      "created_at": "ISO",
      "last_update_at": "ISO",
      "next_check_at": "ISO（空=不定時）",
      "linked_hook_ids": ["HK-xxx"],
      "linked_memory_refs": ["memory key"],
      "closure_reason": "完成或取消的原因",
      "metadata": {}
    }
  ]
}
```

## Event Lifecycle

```
create → active → [parked] → due → completed
                     ↑          ↓
                  (使用者說先放著)  cancelled
                                  superseded
```

| 狀態 | 意義 | 觸發 |
|------|------|------|
| active | 正在追蹤 | 事件建立時 |
| parked | 暫停（「先放著」） | 使用者明確暫停 |
| due | 該追問了 | next_check_at 到期 |
| completed | 已結束 | 使用者確認完成或不再需要 |
| cancelled | 取消 | 使用者取消或過期 |
| superseded | 被取代 | 新事件覆蓋舊事件 |

## Event → Hook 生成規則

| Event Type | 自動生成 Hook? | Hook Type | 條件 |
|---|---|---|---|
| defer | ✅ 有 next_check_at 時 | progress_followup | next_check_at 到期 |
| wake_followup | ✅ | care_message | 使用者起床後 |
| checkin | ✅ 有 next_check_at 時 | progress_followup | next_check_at 到期 |
| reminder_intent | ✅ | progress_followup | next_check_at 到期 |
| health_event | ✅ | health_followup | 自動 |
| emotional_event | ✅ | emotional_followup | 自動 |
| unresolved_topic | ❌ 只留在 event store | — | 等使用者回來接 |
| work_event | ❌ 留在 event store | — | 時間感知決定 |
| task_progress | ✅ 有 next_check_at 時 | progress_followup | next_check_at 到期 |

## Runtime Context 注入順序

```
1. event_new_session_carryover   (新對話：未結束事件摘要)
2. event_context_prompt          (當前追蹤中的事件)
3. carryover_prompt              (上一輪對話 carryover)
4. pending_topics_prompt         (pending hooks/incidents)
5. schedule_context_prompt       (時間感知/作息)
6. recent_dispatch_awareness     (最近 cron/heartbeat dispatch)
7. active_preferences_prompt     (使用者偏好)
```

## Priority Chain（優先序）

以下設定按優先級排列（高→低），高的覆蓋低的：

```
1. rest_suppress          — 使用者明確在休息（最高優先，壓掉一切主動）
2. work_dnd               — 工作勿擾模式
3. quiet_hours            — 靜音時段（proactive_chat.quiet_hours）
4. same_type_cooldown     — 同類型 hook 冷卻（profile.inactivity_routine.same_type_cooldown_hours）
5. routine_schedule.phase — 當前階段（sleep / wake_window / active_day）
   - sleep: proactive 全停
   - wake_window: interval 縮短到 0.5hr
   - active_day: 用 proactive_chat.interval_hours
6. proactive_chat.interval_hours    — 主動聊天最小間隔
7. proactive_chat.max_per_day       — 每日上限
8. inactivity_routine.*_after_hours — 按時間升級（light → playful → care → concern）
9. followup_window                  — follow-up hook 有效期
```

### Shared 預設 vs Live 私有

| 設定 | Shared 預設 | Instance A | Instance B |
|------|---|---|---|
| proactive_chat.interval_hours | 3 | 3 | 1 |
| proactive_chat.quiet_hours | 無 | 6-12 | 0-8 |
| proactive_chat.max_per_day | 2 | 2 | 2 |
| routine_schedule.sleep_time | — | (per profile) | (per profile) |
| routine_schedule.wake_time | — | (per profile) | (per profile) |
| inactivity_routine.light_after_hours | 2 | 2 | 1 |
| same_type_cooldown_hours | 6 | 6 | 6 |

**原則**：shared 只定義 schema 和預設值，live 私有設定不偷渡成公版預設。

## 自然語言 → Event 偵測

以下信號自動觸發事件建立：

| 信號類型 | 範例 | Event Type |
|---|---|---|
| 暫緩 | 「先放著」「晚點再說」「先跳過」 | defer |
| 起床 | 「醒來再聊」「起床後提醒我」 | wake_followup |
| 追蹤 | 「提醒我」「之後問我」「follow up」 | checkin |
| 健康 | 「跌倒」「住院」「不舒服」 | health_event |
| 情緒 | 「壓力」「難過」「心情不好」 | emotional_event |

## 事件建立入口（Entry Layer）

三種入口模式，依信心度與使用者意圖區分：

### Manual（使用者手動建立）

使用者在對話中明確要求追蹤：
- 「幫我記住 / 幫我記 / 記住這件事」
- 「提醒我 / 之後提醒 / 晚點提醒」
- 「之後問我 / 晚點問我 / 記得問我」
- 「追蹤這 / 追這件事 / 幫我追」

→ 直接建立 event（owner=user），前台回覆「✅ 已記住：{title}」

### Auto（AI 自動建立，高信心）

偵測到明確信號且 event type 在允許清單內：

| Event Type | 允許 Auto？ | 原因 |
|---|---|---|
| defer | ✅ | 使用者主動暫緩 = 明確意圖 |
| wake_followup | ✅ | 使用者說醒來再聊 = 明確意圖 |
| reminder_intent | ✅ | 使用者說提醒我 = 明確意圖 |
| health_event | ✅ | 關鍵字精準（頭痛/住院/跌倒） |
| emotional_event | ✅ | 關鍵字精準（壓力/難過/崩潰） |

→ 靜默建立 event（owner=system），不打擾前台

### Suggest（AI 建議建立，先問）

偵測到疑似重要事件但信心不夠高：

| Event Type | 走 Suggest？ | 原因 |
|---|---|---|
| checkin | ✅ | 可能只是隨口一提 |
| work_event | ✅ | 不確定使用者是否要追 |
| relationship_event | ✅ | 私密，應先問 |
| task_progress | ✅ | 可能只是聊天 |
| unresolved_topic | ✅ | 模糊 |
| incident | ✅ | 視情況 |
| custom | ✅ | 不確定 |

→ 建立 event 但 status=suggested，注入提示讓模型問一句：「這件事要我幫你記著追嗎？」
→ 使用者回「好/對/要」→ 升為 active
→ 使用者回「不用/算了」→ 取消

### CRUD 操作（對話中管理事件）

| 操作 | 觸發語句 | 動作 |
|---|---|---|
| 查看 | 「現在追蹤什麼」「在追什麼」「追蹤中」 | 列出所有 active/parked/due 事件 |
| 完成 | 「完成了」「搞定了」「解決了」 | 標記最匹配的 event 為 completed |
| 取消 | 「取消追蹤」「不追了」「不用追了」 | 標記最匹配的 event 為 cancelled |
| 暫停 | 「暫停追蹤」「先擱著」 | 標記最匹配的 event 為 parked |

匹配邏輯：單一 active event 直接命中；多個時依文字關鍵字重疊度匹配。

### 優先序

```
1. pending suggestion 確認/拒絕（最優先檢查）
2. CRUD 操作（view / complete / cancel / park）
3. Manual create（使用者明確要求）
4. Auto create（高信心偵測）
5. Suggest create（低信心偵測）
```

### 前台語句原則

- 短，不像 debug log
- manual create: 「✅ 已記住：{title}」
- auto create: 靜默（不打擾）
- suggest: 模型自然地問一句（由 prompt injection 引導）
- complete: 「✅ 已完成：{title}」
- cancel: 「已取消追蹤：{title}」
- park: 「⏸️ 已暫停：{title}」
- view: 列表格式

### Shared vs Live

- `event_store.py` 和入口邏輯 = **shared**（兩邊完全相同的模組）
- `events.json` = **live 私有**（各自的事件資料）
- `personal_hooks.py` 整合區塊 = **live 私有**（各自微調但結構一致）

## 檔案結構

```
scripts/
  event_store.py          — Event Store 模組（獨立，可 CLI / import）
  personal_hooks.py       — Hook Store + arbiter + runtime-context
plugins/
  personal-hooks-host-adapter/
    index.ts              — Gateway adapter（注入 event context）
data/
  events.json             — Event Store 資料
  hooks.json              — Hook Store 資料
  settings.json           — 統一設定
  profile.json            — 使用者/agent 配置
```
