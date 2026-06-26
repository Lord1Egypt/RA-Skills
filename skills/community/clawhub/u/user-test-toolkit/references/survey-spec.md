# Survey.js 完整配置参考

## 激活条件

```javascript
// 必须同时满足：
const testMode = params.get('smode') || params.get('mode'); // 必须 === 'test'
const uid = params.get('uid');                               // 必须非空
if (testMode !== 'test' || !uid) return;                      // 否则不执行任何代码
```

## URL 参数完整表

| 参数 | 类型 | 默认值 | 可选值 | 说明 |
|------|------|--------|--------|------|
| `smode` | string | - | `test` | **必填** 激活开关 |
| `mode` | string | - | `test` | 兼容旧版（smode 优先） |
| `uid` | string | - | 任意非空 | **必填** 用户标识 |
| `test` | string | `default` | 任意 | 测试轮次标识 |
| `stype` | string | auto | `internal` / `user` / 空 | 测试类型（空=自动判断） |
| `stasks` | string | `1` | `0` / `1` | 任务面板开关 |
| `ssurveys` | string | `1` | `0` / `1` | 情境问卷开关 |
| `sexit` | string | `1` | `0` / `1` | 总结问卷开关 |
| `swelcome` | string | `1` | `0` / `1` | 欢迎页开关 |
| `scp` | string | all | 逗号分隔的 cp id | 只启用指定的 checkpoint |

## 任务配置

### TASKS_INTERNAL（内部测试，3步）

| id | label | hint | detect |
|----|-------|------|---------|
| T1 | 把一个视频翻译成英文 | 用你觉得合适的方式完成 | mps_complete |
| T2 | 对翻译结果做一些修改 | 比如改条字幕、调个区域 | finetune_edit |
| T3 | 把最终结果导出 | 下载你满意的版本 | export |

### TASKS_USER（外部用户，2步）

| id | label | hint | detect |
|----|-------|------|---------|
| T1 | 把这个视频翻译成中文 | | mps_complete |
| T2 | 下载翻译好的视频 | | export |

## Checkpoint（情境微问卷）配置

### CP_INTERNAL（4个）

| id | trigger | delay(ms) | type | question | 特殊配置 |
|----|---------|-----------|------|----------|---------|
| upload_ease | upload_done | 1500 | rating | 刚才找到上传入口顺利吗？ | scale:5, allowComment:true |
| wait_sam | processing_wait_30s | 500 | sam | 等 AI 处理的这段时间感觉怎样？ | dims:[arousal,valence] |
| result_sam | view_result | 3000 | sam | 看到 AI 处理的结果，感觉如何？ | dims:[valence,dominance] |
| finetune_ease | finetune_edit | 1500 | rating | 刚才修改结果的操作顺利吗？ | scale:5, allowComment:true |

### CP_USER（2个）

| id | trigger | delay(ms) | type | question | 特殊配置 |
|----|---------|-----------|------|----------|---------|
| upload_ease | upload_done | 2000 | rating | 上传视频顺利吗？ | scale:5, allowComment:false |
| result_quality | view_result | 3000 | rating | 翻译的效果你满意吗？ | scale:5, allowComment:true |

## 问卷类型详解

### Rating（李克特评分）

```javascript
{
  id: 'xxx',
  trigger: 'event_name',     // 触发事件名
  delay: 1500,               // 延迟毫秒
  type: 'rating',
  question: '问题文本',
  scale: 5,                  // 分制（5或7）
  labels: ['很困难', '...','一下就找到了'],  // 两端标签
  allowComment: true,        // 是否显示评论框
  commentPH: '补充说明（可选）'                    // 评论占位符
}
```

UI：5/7 个按钮横排，点击高亮自身及左侧所有按钮。底部可选 textarea。

### SAM（Self-Assessment Mannequin）

```javascript
{
  id: 'xxx',
  trigger: 'event_name',
  delay: 500,
  type: 'sam',
  question: '问题文本',
  dims: [
    { id: 'arousal', label: '紧张程度', l: '很放松', r: '很焦虑' },
    { id: 'valence',  label: '心情', l: '不太好', r: '挺好的' },
    // 最多4个维度
  ]
}
```

UI：每个维度一个滑块（1-9分），左右标签 + 实时数值显示。

## 总结问卷结构

### SUS（系统可用性量表）

标准 10 题（国际通用），5 分制（非常不同意→非常同意）：

```
1. 我会经常使用此产品
2. 此产品不必要地复杂
3. 此产品很容易使用
4. 我需要技术人员支持才能使用
5. 此产品各项功能整合得很好
6. 此产品有太多不一致之处
7. 大多数人能很快学会使用
8. 此产品用起来很麻烦
9. 使用时我感到很有信心
10. 我需要学很多东西才能使用
```

**计分**：奇数题原分，偶数题反转(5-分)，求和×2.5 = 0-100分

### EV（情绪价值量表）

9 题，5 分制（非常不同意→非常同意）：

```
1. 使用过程让我感到愉悦
2. 等待 AI 处理时我不觉得无聊
3. 看到成片效果让我惊喜
4. 产品让我觉得不再困难
5. 整体过程让我有掌控感
6. 我愿意向朋友展示成果
7. 界面让我感到专业和可信
8. 处理中的角色让体验更有趣
9. 整体体验超出预期
```

**计分**：简单平均 = 1-5分

### NPS（推荐意愿）

1 题 0-10 分 + 开放原因文本框。

**分级**：0-6( detractor/贬损者 ) / 7-8( passive/被动者 ) / 9-10( promoter/推荐者 )

### 三词描述

3 个 `<input>` 并排，各占一行。

### 开放反馈

2 个 `<textarea>`：
- "最困惑/卡住的地方"
- "最有价值的功能"

## CSS 类名速查

| 类名 | 元素 | 说明 |
|------|------|------|
| `sv-overlay` | 全屏遮罩 | 欢迎页+总结问卷背景 |
| `sv-card` | 内容卡片 | 居中圆角卡片容器 |
| `sv-btn` | 主按钮 | 渐变紫，圆角12px |
| `sv-tp` | 任务面板 | 右上角悬浮 |
| `sv-tp.min` | 收起态 | 右下角 FAB 气泡 |
| `sv-fab` | 气泡内容 | 进度环+任务名 |
| `sv-fab-ring` | 进度环 | SVG 圆形进度条 |
| `sv-mo` | 微问卷 | 右下角弹窗 |
| `sv-rs` | 评分按钮 | 方形圆角按钮 |
| `sv-sam-s` | SAM滑块 | 自定义 range 样式 |
| `sv-exit` | 总结问卷 | 全屏弹窗 |
| `sv-exit-c` | 总结内容 | 最大宽600px，可滚动 |
| `sv-sec` | 问卷分区 | SUS/EV/NPS/三词/开放 |
| `sv-sq-o` | SUS选项 | 小方块按钮 |
| `sv-nps-b` | NPS数字 | 0-10，红/黄/绿三色 |
| `sv-ev-o` | EV选项 | 橙色系按钮 |
| `sv-thx` | 感谢页 | 居中感谢+分数展示 |

## 状态持久化格式

```json
{
  "taskStates": ["pending", "done", "pending"],
  "answered": {"upload_ease": true},
  "startTs": 1713345600000,
  "exitShown": false
}
```

Key: `sv_state_{uid}` 存储在 sessionStorage 中。
