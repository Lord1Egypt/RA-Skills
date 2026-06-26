---
name: user-test-toolkit
description: "为 AI 时代的 Vibe Coding 页面量身打造的用户测试工具链。无需修改业务代码，只要把 tracker.js 引入任意页面，即可自动采集用户的操作轨迹、犹豫点、困惑行为、停留热区；配合 survey.js，能在用户真实使用流程中嵌入式触发任务引导、微问卷检查点（Checkpoint）、SUS/EV/NPS 标准量表和 SAM 情绪评估，所有数据上报到你的服务端。适用于：可用性测试、用户研究、埋点采集、A/B 效果验证。创新点：埋点和问卷均与业务流零侵入融合，不是事后补发，而是用户"正在做事的时候"自动感知、自动触发。"
---

# User Test Toolkit Skill — Web 应用用户测试完整工具链 v3（可配置版）

## 🎯 5 分钟上手

### 最简配置（复制即用）

```html
<!-- 1. 引入配置 + 设置你的产品信息 -->
<script src="survey-config.js"></script>
<script>
  window.SURVEY_CONFIG = {
    productName: '我的产品',
    tasks: [
      { id:'T1', label:'完成注册', detect:'signup_done'    },
      { id:'T2', label:'完成下单', detect:'order_done'     },
      { id:'T3', label:'完成支付', detect:'payment_done'  }
    ]
  };
</script>

<!-- 2. 引入核心文件 -->
<script src="tracker.js"></script>
<script src="survey.js"></script>
```

### 业务代码中触发 milestone

```javascript
// 用户完成某个步骤时调用一次，Survey 自动响应
UserTestTracker.milestone('signup_done');    // 注册完成 → 触发 T1 任务
UserTestTracker.milestone('order_done');     // 下单完成 → 触发 T2 任务
UserTestTracker.milestone('payment_done');    // 支付完成 → 触发 T3 + 总结问卷
```

### 完整功能说明

| 模块 | 功能 | 定制方式 |
|------|------|---------|
| **tracker.js** | 6 维埋点（操作/犹豫/困惑/停留/里程碑/热区） | 改 `TRACKER_CONFIG.endpoint` 即可 |
| **survey.js** | 主动问卷（任务面板 + checkpoint 微问卷 + SUS/EV/NPS） | 改 `SURVEY_CONFIG.tasks` 即可 |

---

## 概述

### Step 1: 引入 tracker.js

```html
<script src="tracker-config.js"></script>
<script>
  // ★ 必须设置：数据上报地址
  window.TRACKER_CONFIG.endpoint = 'https://your-server.com/track';

  // ★ 推荐设置：milestone 映射（让 survey.js 能跨产品工作）
  window.TRACKER_CONFIG.milestones = {
    'signup_done':   'step1_done',
    'order_complete':'step2_done',
    'payment_done':  'task_done'
  };

  // ★ 可选：自定义 action 识别
  window.TRACKER_CONFIG.actionMap = {
    '.signup-btn':  'signup',
    '#checkout-btn':'purchase',
    '.play-btn':    'play_video'
  };
</script>
<script src="tracker.js"></script>
```

### Step 2: 引入 survey.js（可选，不要问卷功能可跳过）

```html
<script src="survey-config.js"></script>
<script>
  // ★ 推荐设置：产品名称（用于问卷文案）
  window.SURVEY_CONFIG.productName = '我的产品';

  // ★ 必须设置：任务列表（核心定制点）
  window.SURVEY_CONFIG.tasks = [
    { id:'T1', label:'完成注册流程', detect:'step1_done' },
    { id:'T2', label:'完成首次下单', detect:'step2_done' },
    { id:'T3', label:'完成支付',     detect:'task_done'  }
  ];

  // ★ 推荐设置：情境问卷（checkpoint）
  window.SURVEY_CONFIG.checkpoints = [
    {
      id: 'signup_ease',
      trigger: 'step1_done',
      delay: 1500,
      type: 'rating',
      question: '注册流程顺利吗？',
      scale: 5,
      labels: ['很困难', '有点绕', '还行', '比较顺', '一下就找到了'],
      allowComment: true,
      commentPH: '在哪卡住过？（可选）'
    }
  ];
</script>
<script src="survey.js"></script>
```

### Step 3: 在业务代码中触发 milestone

```javascript
// 业务完成某个步骤时调用一次，Survey 自动响应
UserTestTracker.milestone('signup_done');   // 注册完成 → 触发 T1 任务 + 对应 checkpoint
UserTestTracker.milestone('step2_done');    // 下单完成
UserTestTracker.milestone('task_done');     // 支付完成 → 触发 T3 + 任务结束 + 总结问卷
```

---

## 文件结构

```
user-test-toolkit/
├── SKILL.md                          # 本文档
├── references/
│   ├── tracker-spec.md               # Tracker 完整 API 参考
│   └── survey-spec.md                # Survey 配置参考 + 题型说明
└── assets/
    ├── tracker.js                    # 埋点系统（v3，支持配置）
    ├── tracker-config.js             # Tracker 配置模板（即插即用）
    ├── survey.js                      # 问卷引擎（v3，支持配置）
    └── survey-config.js              # Survey 配置模板（零基础定制）
```

---

## 配置化详解

### Tracker 配置（tracker-config.js）

| 配置项 | 类型 | 默认值 | 说明 |
|-------|------|--------|------|
| `endpoint` | string | `''` | **必填**。埋点上报地址，如 `'https://your-server.com/track'` |
| `flushInterval` | number | `8000` | 批量上报间隔（ms） |
| `maxQueue` | number | `30` | 缓存超过此条数立即上报 |
| `milestones` | object | 内置映射 | milestone 名称映射表：`{ 业务名: 通用名 }` |
| `actionMap` | object | `{}` | action 自动分类选择器映射 |
| `disabled` | boolean | `false` | `true` = 记录但不上报 |

### Survey 配置（survey-config.js）

| 配置项 | 类型 | 默认值 | 说明 |
|-------|------|--------|------|
| `productName` | string | `'本产品'` | 问卷文案中的产品名称 |
| `tasks` | array | 内置默认 | 任务定义数组（见下方格式） |
| `checkpoints` | array | 内置默认 | 情境问卷数组（见下方格式） |
| `welcomeInternal` | object | 内置默认 | 内部测试欢迎页文案 |
| `welcomeUser` | object | 内置默认 | 外部用户欢迎页文案 |
| `testVideoUrl` | string | `'assets/test-video.mov'` | 测试素材下载地址 |
| `openQuestion1/2` | string | 内置默认 | 总结问卷开放题文本 |

### 任务对象格式

```javascript
{
  id:     'T1',           // 唯一ID
  label:  '完成注册流程', // 显示给用户的任务描述
  hint:   '用手机号注册', // 内部模式显示的提示（可选）
  detect: 'signup_done'  // 触发的 milestone 名称（映射后）
}
```

### Checkpoint 对象格式

```javascript
// rating 型（李克特评分）
{
  id: 'signup_ease',
  trigger: 'signup_done',       // 映射前的 milestone 名称
  delay: 1500,                  // 延迟触发（ms）
  type: 'rating',
  question: '注册流程顺利吗？',
  scale: 5,                     // 5 或 7 分
  labels: ['很困难', ..., '很顺利'],  // 两端标签
  allowComment: true,           // 是否显示评论框
  commentPH: '在哪卡住过？'      // 评论 placeholder
}

// sam 型（SAM 情绪模型）
{
  id: 'post_use_sam',
  trigger: 'task_done',
  delay: 2000,
  type: 'sam',
  question: '使用后感觉如何？',
  dims: [
    { id: 'arousal', label: '紧张程度', l: '很放松', r: '很焦虑' },
    { id: 'valence', label: '满意程度', l: '不满意',  r: '很满意' }
  ]
}
```

---

## 事件类型完整清单

| type | 说明 | detail 字段 |
|------|------|------------|
| `enter` | 页面访问 | url, referrer, screen, viewport |
| `first_interact` | 首次交互 | how(click/scroll/enter_key/focus_input), hesitation(秒) |
| `click` | 点击 | target(CSS选择器), x/y(%), action(分类名称) |
| `frustration` | 困惑行为 | target, repeats(次数), hint |
| `file_select` | 文件选择 | name, sizeMB, type |
| `focus` | 输入框聚焦 | target |
| `input_enter` | 回车提交 | inputId, length |
| `scroll` | 滚动深度 | depth(%) |
| `tab_away/back` | 页面切换 | elapsed(秒) |
| `leave` | 页面离开 | duration, scrollDepth, interactions, hesitation |
| `error` | JS 错误 | msg, file, line |
| `milestone` | 业务里程碑 | name(映射后), originalName(映射前) |
| `phase_start/end` | 阶段标记 | phase |
| `upload_progress/done/fail` | 上传 | pct / url,sizeMB / error |
| `mps_status` | MPS 状态 | status, elapsed |
| `survey_show/answer/skip/exit_submit` | 问卷事件 | — |
| `task_complete` | 任务完成 | taskId, label, elapsed |

---

## UserTestTracker API

```javascript
// 底层
UserTestTracker.record(type, detail)   // 记录任意事件
UserTestTracker.flush()               // 强制刷新缓冲区

// 里程碑（最常用）
UserTestTracker.milestone(name)          // 记录 milestone（自动映射）
UserTestTracker.milestone(name, extra)   // 带附加数据

// 阶段
UserTestTracker.phaseStart(name)
UserTestTracker.phaseEnd(name)

// 上传
UserTestTracker.uploadProgress(pct)      // 0-100
UserTestTracker.uploadDone(url, sizeMB)
UserTestTracker.uploadFail(err)

// MPS 状态（保留给特定场景）
UserTestTracker.mpsStatus(status, elapsed)

// 问卷联动（Survey 内部使用）
UserTestTracker.surveyShow(id, type)
UserTestTracker.surveyAnswer(data)
UserTestTracker.surveySkip(id)
UserTestTracker.surveyExitSubmit(data)
UserTestTracker.taskComplete(taskId, label)

// 信息
UserTestTracker.uid        // 当前用户 ID
UserTestTracker.testRound  // 当前测试轮次
UserTestTracker.sessionId  // 当前会话 ID
```

---

## 使用工作流

### 工作流 A：快速 1v1 可用性测试（30分钟）

1. 准备测试素材，放入 `assets/test-video.mov`
2. 设置 `TRACKER_CONFIG.endpoint` + `SURVEY_CONFIG.tasks`
3. 生成测试链接：`?uid=user001&test=round1&smode=test`
4. 发给用户，观察操作
5. 测试结束后查看总结问卷数据

### 工作流 B：批量远程测试（N 人）

1. 批量生成链接（每个 uid 不同）
2. 外部模式自动简化任务和问卷（`stype=user`）
3. 所有数据通过 `/track` 端点汇总

### 工作流 C：只埋点不做问卷

1. 只引 `tracker.js`，不引 `survey.js`
2. 或引 survey 但不加 `smode=test` 参数

---

## 数据输出物

| 输出 | 来源 | 内容 |
|------|------|------|
| 操作序列JSON | tracker | 完整用户行为路径（时间线） |
| 犹豫/困惑标记 | tracker | 入口问题 + 困惑点定位 |
| 里程碑转化率 | tracker | 核心漏斗各步骤到达率 |
| SUS 评分 | survey exit | 可用性量化分(0-100) |
| NPS 评分 | survey exit | 推荐意愿(-100~100) |
| EV 情绪分 | survey exit | 9题情绪价值均值 |
| 三词标签 | survey exit | 用户心智关键词 |
| 开放反馈 | survey exit | 定性问题和建议 |

---

## 发布到 GitHub 的方法

```bash
cd ~/.codebuddy/skills/user-test-toolkit
git init
git add .
git commit -m "feat: user-test-toolkit v3 configurable"
git remote add origin https://github.com/YOUR_USERNAME/user-test-toolkit.git
git push -u origin main
```

其他人使用：
```bash
git clone https://github.com/YOUR_USERNAME/user-test-toolkit.git
# 或作为 submodule
```
