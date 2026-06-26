# Tracker.js 完整 API 参考

## 全局变量

| 变量 | 类型 | 说明 |
|------|------|------|
| `SCF_BASE` | string | 上报端点基础 URL |
| `uid` | string | 用户 ID（URL 参数或随机生成） |
| `testRound` | string | 测试轮次（URL 参数） |
| `page` | string | 当前页面文件名 |
| `sessionId` | string | 会话唯一标识 = uid + 时间戳 |
| `opLog` | Array | 所有操作记录的完整数组 |
| `TRACKER_DISABLED` | boolean | 停用上报开关（保留记录） |

## 核心函数

### record(type, detail)

底层记录函数。每条记录包含：

```typescript
interface EventEntry {
  seq: number;           // 序号（自增）
  uid: string;           // 用户 ID
  test: string;          // 测试轮次
  session: string;       // 会话 ID
  page: string;          // 页面名
  type: string;          // 事件类型
  ts: string;            // ISO 时间戳
  elapsed: number;       // 距页面进入的秒数
  d: object;             // 详情数据
}
```

### flush()

强制刷新缓冲队列。通过 sendBeacon/fetch POST 到 `{SCF_BASE}/track`。

### describeElement(el): string

生成元素描述符：
- 有 id → `#xxx`
- 有 data-track → `[track=xxx]`
- 有 class → `tag.class1.class2`
- 兜底 → `tag`

### identifyAction(el): string

将点击目标映射为业务动作。匹配规则按优先级排列。

## TideoTracker 公开 API

```typescript
interface TideoTrackerAPI {
  record(type: string, detail?: object): EventEntry;
  flush(): void;
  uid: string;
  testRound: string;
  sessionId: string;
  
  // 里程碑
  milestone(name: string, extra?: object): void;
  
  // 阶段
  phaseStart(name: string): void;
  phaseEnd(name: string): void;
  
  // 上传
  uploadProgress(pct: number): void;
  uploadDone(url: string, sizeMB: number): void;
  uploadFail(err: string): void;
  
  // MPS
  mpsStatus(status: string, elapsed?: number): void;
  
  // 问卷联动
  surveyShow(checkpointId: string, type: string): void;
  surveyAnswer(data: object): void;
  surveySkip(checkpointId: string): void;
  surveyExitSubmit(data: object): void;
  taskComplete(taskId: string, label: string): void;
}
```

## 事件类型完整列表

| type | 触发时机 | d 字段 |
|------|---------|--------|
| `enter` | 页面加载 | url, referrer, screen, viewport |
| `first_interact` | 首次用户交互 | how(交互方式), hesitation(秒) |
| `click` | 点击 | target, text, x(%), y(%), action |
| `frustration` | 困惑检测(3s内同元素≥3次点击) | target, repeats, hint |
| `file_select` | 文件选择 | name, sizeMB, type |
| `focus` | 输入框聚焦 | target |
| `input_enter` | 回车提交 | inputId, length |
| `scroll` | 滚动(深度变化>10%) | depth(百分比) |
| `tab_away` | 切走标签页 | elapsed |
| `tab_back` | 切回标签页 | elapsed |
| `leave` | 页面离开 | duration, scrollDepth, interactions, hesitation |
| `error` | JS 错误 | msg, file, line |
| `milestone` | 业务里程碑 | name, ...extra |
| `phase_start` | 阶段开始 | phase |
| `phase_end` | 阶段结束 | phase |
| `upload_progress` | 上传进度 | pct |
| `upload_done` | 上传完成 | url(后60字), sizeMB |
| `upload_fail` | 上传失败 | error |
| `mps_status` | MPS 状态变更 | status, elapsed |
| `survey_show` | 问卷展示 | checkpoint, type |
| `survey_answer` | 问卷回答 | (各题型不同) |
| `survey_skip` | 问卷跳过 | checkpoint |
| `survey_exit_submit` | 总结问卷提交 | sus, susScore, ev, evAvg, nps, ... |
| `task_complete` | 任务完成 | taskId, label, elapsed |

## action 自动分类表

| action | 匹配条件 |
|--------|---------|
| `select_skill` | `.skill-card` 内的点击 |
| `submit` | `#submitBtn` 或含"提交"文字 |
| `export` | 含"导出/下载"或 `.ra-btn-export` |
| `finetune` | 含"精调"或 `.ra-btn-re` |
| `back` | `.v8-back` 或 `#backBtn` |
| `finetune_done` | `.v8-done-btn` |
| `finetune_cancel` | `.v8-cancel-fp` |
| `tab_switch` | `.v8-tab` |
| `dimmer_action` | `.v8-dbtn` |
| `restore_task` | `.min-task-card` |
| `nav_xxxx` | `.nav-item` 取前4字 |
| `play_toggle` | `#scrubPlay` 或 `#tlPlay` |
| `upload_trigger` | file input 或含 triggerUpload |

## 缓冲队列机制

```
事件产生 → push eventQueue → 
  ├─ queue.length >= MAX_QUEUE(30)? → 立即 flush()
  └─ setInterval(flush, FLUSH_INTERVAL(8000))

flush():
  ├─ TRACKER_DISABLED → 清空队列，不上报
  └─ 正常 → sendBeacon POST /track (JSON {events: [...]})
       ↓ 失败 → fetch keepalive POST /track
```
