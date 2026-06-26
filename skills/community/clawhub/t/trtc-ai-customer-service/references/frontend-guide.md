# TRTC AI 智能客服 - 前端集成指南

## 目录

1. [TRTC Web SDK 集成](#trtc-web-sdk-集成)
2. [对话生命周期](#对话生命周期)
3. [消息处理协议](#消息处理协议)
4. [文字输入（跳过 ASR）](#文字输入跳过-asr)
5. [关键词检测](#关键词检测)
6. [字幕增量/累积自适应](#字幕增量累积自适应)
7. [转人工流程](#转人工流程)
8. [UI 组件结构](#ui-组件结构)
9. [国际化系统](#国际化系统)
10. [状态管理](#状态管理)

---

## TRTC Web SDK 集成

### 引入 SDK

```html
<script src="https://web.sdk.qcloud.com/trtc/webrtc/v5/dist/trtc.js"></script>
```

### 初始化与进房

```javascript
// 创建 TRTC 客户端
const trtcClient = TRTC.create();

// 绑定事件
trtcClient.on(TRTC.EVENT.CUSTOM_MESSAGE, handleMessage);           // 字幕 + AI 状态
trtcClient.on(TRTC.EVENT.REMOTE_USER_LEAVE, onRobotLeave);         // 机器人退房
trtcClient.on(TRTC.EVENT.REMOTE_VIDEO_AVAILABLE, onVideoAvailable); // 数字人视频流

// 进房
await trtcClient.enterRoom({
    roomId: roomId,        // 房间号（数字）
    scene: 'rtc',
    sdkAppId: sdkAppId,
    userId: userId,
    userSig: userSig,
});

// 开麦克风（纯语音场景）
await trtcClient.startLocalAudio();
```

### 退房

```javascript
await trtcClient.stopLocalAudio();
await trtcClient.exitRoom();
trtcClient.destroy();
```

---

## 对话生命周期

```
idle → connecting → active → ending → idle
                              ↓
                         transferring → idle
```

### 启动流程（startCall）

```javascript
async function startCall() {
    STATE.callState = 'connecting';

    // 1. join：获取 UserSig
    const joinData = await postAction('join', { userid: STATE.userId });
    STATE.sdkAppId = joinData.sdkappid;
    STATE.userSig = joinData.usersig;
    STATE.robotUserId = joinData.robot_userid;
    STATE.robotUserSig = joinData.robot_usersig;
    STATE.endKeywords = joinData.end_keywords;
    STATE.farewellMessage = joinData.farewell_message;
    STATE.transferKeywords = joinData.transfer_keywords;
    STATE.avatarAvailable = joinData.avatar_available;

    // 2. 创建 TRTC 客户端并进房
    trtcClient = TRTC.create();
    bindEvents(trtcClient);
    await trtcClient.enterRoom({ roomId, scene: 'rtc', sdkAppId, userId, userSig });
    await trtcClient.startLocalAudio();

    // 3. StartAIConversation
    const startData = await postAction('StartAIConversation', {
        RoomId: STATE.roomId,
        AgentConfig: {
            UserId: STATE.robotUserId,
            UserSig: STATE.robotUserSig,
            TargetUserId: STATE.userId,
            Lang: USER_CFG.lang,
        },
        UserConfig: {
            InterruptMode: USER_CFG.interruptMode,
            InterruptSpeechDuration: USER_CFG.interruptSpeechDuration,
            VadLevel: USER_CFG.vadLevel,
            VadSilenceTime: USER_CFG.vadSilenceTime,
            Gender: STATE.gender,
        },
        UseAvatar: STATE.useAvatar,
        AvatarConfig: STATE.useAvatar ? {
            AvatarUserID: STATE.avatarUserId,
            AvatarUserSig: STATE.avatarUserSig,
        } : undefined,
    });
    STATE.taskId = startData.TaskId;
    STATE.callState = 'active';
}
```

### 结束流程（farewellAndEnd）

```javascript
async function farewellAndEnd() {
    STATE.callState = 'ending';

    // 1. 发送 FarewellAndStop
    await postAction('FarewellAndStop', {
        TaskId: STATE.taskId,
        Lang: USER_CFG.lang,
    });

    // 2. 等待机器人退房（onRobotLeave 回调）
    // 3. 退房
    await cleanupRoom();

    // 4. 显示评分弹窗
    showRatingOverlay();
}
```

### 机器人退房回调

```javascript
function onRobotLeave(event) {
    const { userId } = event;
    if (userId === STATE.robotUserId || userId === STATE.avatarUserId) {
        if (STATE.callState === 'ending' || STATE.callState === 'transferring') {
            cleanupRoom();
        }
    }
}
```

---

## 消息处理协议

所有云端消息通过 `TRTC.EVENT.CUSTOM_MESSAGE` 事件接收：

```javascript
function handleMessage(event) {
    const { data } = event;
    const msg = JSON.parse(new TextDecoder().decode(data));

    switch (msg.type) {
        case 10000:  // 字幕
            handleSubtitle(msg);
            break;
        case 10001:  // AI 状态
            handleAIState(msg);
            break;
    }
}
```

### type: 10000 - 字幕消息

```json
{
    "type": 10000,
    "sender": "user_xxx_robot",
    "payload": {
        "roundid": "round_123",
        "userid": "user_xxx",       // 发言者
        "text": "你好，请问...",
        "end": false                 // true=该轮结束
    }
}
```

**区分用户和 AI**：
- `payload.userid === STATE.userId` → 用户的 ASR 文本
- `payload.userid !== STATE.userId` → AI 的回复文本

### type: 10001 - AI 状态

```json
{
    "type": 10001,
    "payload": {
        "state": 1,         // 1=聆听 2=思考 3=说话 4=打断 5=结束
        "roundid": "round_123"
    }
}
```

| state | 含义 | 前端响应 |
|-------|------|----------|
| 1 | 聆听 | 显示"聆听中..." |
| 2 | 思考 | 显示 typing 动画 |
| 3 | 说话 | 更新语音状态指示 |
| 4 | 打断 | 标记当前回复被打断 |
| 5 | 结束 | 触发结束流程 |

---

## 文字输入（跳过 ASR）

使用 `type: 20000` 自定义消息协议，文字直接发送到 LLM：

```javascript
function sendTextMessage(text) {
    const message = {
        type: 20000,
        sender: STATE.userId,
        receiver: [STATE.robotUserId],
        payload: {
            id: crypto.randomUUID(),
            message: text,
            timestamp: Date.now(),
        },
    };

    trtcClient.sendCustomMessage({
        cmdId: 2,
        data: new TextEncoder().encode(JSON.stringify(message)).buffer,
    });
}
```

**关键点**：
- `cmdId: 2` 是固定值
- `receiver` 指定机器人 userId
- 文本跳过 ASR 引擎，直接送入 LLM，适合不便说话场景
- 用户发送文字后可无缝切回语音模式

---

## 关键词检测

### 构建正则

```javascript
function buildKeywordRegex(keywords) {
    if (!keywords || keywords.length === 0) return null;

    const patterns = keywords.map(kw => {
        const escaped = kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const hasChineseChar = /[\u4e00-\u9fa5]/.test(kw);

        if (hasChineseChar) {
            // 中文：两侧非中文字母数字边界
            return `(^|[^\\u4e00-\\u9fa5A-Za-z0-9])${escaped}(?=[^\\u4e00-\\u9fa5A-Za-z0-9]|$)`;
        } else {
            // 英文：标准词边界
            return `\\b${escaped}\\b`;
        }
    });

    return new RegExp(patterns.join('|'), 'i');
}
```

### 检测触发

```javascript
function detectEndKeyword(text) {
    const lang = USER_CFG.lang;
    const keywords = STATE.endKeywords[lang] || [];
    const regex = buildKeywordRegex(keywords);
    return regex && regex.test(text);
}

// 在用户 ASR 文本结束时检测
if (payload.end && payload.userid === STATE.userId) {
    if (detectEndKeyword(payload.text)) {
        farewellAndEnd();
    } else if (detectTransferKeyword(payload.text)) {
        triggerTransfer();
    }
}
```

---

## 字幕增量/累积自适应

TRTC 下发字幕可能是增量或累积模式，前端自动适配：

```javascript
function processSubtitleText(roundId, newText) {
    const accumulated = STATE.aiRoundText[roundId] || '';

    if (newText.startsWith(accumulated)) {
        // 累积模式：新文本是旧文本的超集
        STATE.aiRoundText[roundId] = newText;
    } else {
        // 增量模式：新文本是新增部分
        STATE.aiRoundText[roundId] = accumulated + newText;
    }

    return STATE.aiRoundText[roundId];
}
```

---

## 转人工流程

```javascript
async function triggerTransfer() {
    STATE.callState = 'transferring';

    // 1. 播报转接提示语
    await postAction('TransferAndStop', {
        TaskId: STATE.taskId,
        Lang: USER_CFG.lang,
    });

    // 2. 等待机器人退房
    // 3. 显示排队进度弹窗
    showTransferOverlay();

    // 4. 模拟排队（MVP）
    await simulateQueueProgress();

    // 5. 排队失败 → 恢复 AI 对话（或对接真实呼叫中心）
    restartAIConversation();
}
```

---

## UI 组件结构

```
┌─────────────────────────────────────────────────┐
│  Top Bar                                          │
│  [☰ 侧边栏] [AI 电商客服]      [🌐 简体中文 ▼]     │
├──────────┬──────────────────────────────────────┤
│          │                                       │
│ Sidebar  │  Main Area                            │
│          │                                       │
│ ┌──────┐ │  ┌────────────────────────────────┐  │
│ │对话模式│ │  │  Agent Select Area              │  │
│ │断句模式│ │  │  [👩 女客服]  [👨 男客服]         │  │
│ │打断模式│ │  │       [开始对话]                 │  │
│ │VAD设置│ │  └────────────────────────────────┘  │
│ │       │ │                                      │
│ └──────┘ │  ┌────────────────────────────────┐  │
│          │  │  Chat Messages                   │  │
│          │  │  [AI] 您好，请问有什么...          │  │
│          │  │          [User] 查询订单          │  │
│          │  │  [AI] 好的，请提供订单号...        │  │
│          │  └────────────────────────────────┘  │
│          │                                      │
│          │  ┌────────────────────────────────┐  │
│          │  │  Input Bar                       │  │
│          │  │  [⌨️/🎤] [📦订单] [🔁转人工] [📞挂断] │  │
│          │  └────────────────────────────────┘  │
├──────────┴──────────────────────────────────────┤
│  Overlays: 评分弹窗 / 订单面板 / 转人工弹窗      │
└─────────────────────────────────────────────────┘
```

### CSS 设计要点

- **CSS 变量系统**：`--primary`、`--bg`、`--surface` 等统一管理主题色
- **响应式**：768px 断点移动端适配，侧边栏可折叠
- **动效**：消息入场 `fadeInUp`、typing dots、评分弹窗滑入
- **无外部依赖**：纯 CSS + 内联 SVG 图标

---

## 国际化系统

### 架构

```javascript
// i18n.js - IIFE 模式
(function() {
    const DICT = {
        zh: { appName: 'AI 电商客服', ... },
        yue: { appName: 'AI 電商客服', ... },
        en: { appName: 'AI Customer Service', ... },
    };

    window.I18N = {
        getLang() { ... },           // 从 localStorage 读取
        setLang(lang) { ... },       // 保存到 localStorage + 广播事件
        t(key, params) { ... },      // 翻译（支持 {param} 模板替换）
    };
})();
```

### 使用

```javascript
// HTML 中
<span data-i18n="appName"></span>

// JS 中
const text = I18N.t('tipConnecting');  // "正在连接..."
const text = I18N.t('duration', { time: '5:30' });  // "通话时长: 5:30"

// 语言切换监听
window.addEventListener('langChange', (e) => {
    const lang = e.detail.lang;
    updateAllTexts();
});
```

### 语言存储

- `localStorage` key: `cs_lang`
- 默认值：跟随浏览器 `navigator.language`
- 切换通过 `CustomEvent('langChange')` 事件广播

---

## 状态管理

前端使用简单的全局对象管理状态：

```javascript
const STATE = {
    // 连接状态
    userId: '',
    roomId: 0,
    sdkAppId: 0,
    userSig: '',
    robotUserId: '',
    robotUserSig: '',
    avatarUserId: '',
    avatarUserSig: '',

    // 功能开关
    avatarAvailable: false,
    useAvatar: false,
    gender: 'female',

    // 通话状态
    callState: 'idle',       // idle | connecting | active | ending | transferring
    taskId: null,
    startTime: null,
    muted: false,
    aiSpeaking: false,

    // 关键词（从 join 响应获取）
    endKeywords: { zh: [], yue: [], en: [] },
    farewellMessage: { zh: '', yue: '', en: '' },
    transferKeywords: { zh: [], yue: [], en: [] },
    transferMessage: { zh: '', yue: '', en: '' },

    // 消息管理
    messages: [],             // 消息气泡列表
    typingMsgId: null,        // AI typing 状态
    aiRoundText: {},          // roundid → 累积文本
    aiRoundLast: {},          // roundid → 上一次文本（去重）
    aiRoundMsgId: {},         // roundid → 消息气泡 ID
};

const USER_CFG = {
    lang: I18N.getLang(),
    mode: 'voice',            // voice | avatar
    inputMode: 'voice',       // voice | text
    interruptMode: 0,         // 0=智能打断 1=手动打断
    interruptSpeechDuration: 600,
    vadLevel: 3,
    vadSilenceTime: 600,
    turnDetectionMode: 3,     // 3=语义断句 0=VAD断句
};
```

### HTTP 请求封装

```javascript
async function postAction(action, body = {}) {
    const resp = await fetch('/action', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Action': action,
        },
        body: JSON.stringify(body),
    });
    const data = await resp.json();
    if (data.Response?.Error) {
        throw new Error(data.Response.Error.Message);
    }
    return data;
}
```
