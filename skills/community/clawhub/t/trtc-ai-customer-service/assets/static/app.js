// ===================================================================
// AI 智能客服 - 前端逻辑（IM 风格 + 语音/文字双模 + 手动评分）
// ===================================================================
'use strict';

const STATE = {
    userId: '',
    roomId: 0,
    sdkAppId: 0,
    userSig: '',
    robotUserId: '',
    robotUserSig: '',
    avatarUserId: '',
    avatarUserSig: '',
    avatarAvailable: false,
    useAvatar: false,
    gender: 'female',
    callState: 'idle',       // idle | connecting | active | ending
    taskId: null,
    startTime: null,
    muted: false,
    localMuted: false,
    aiSpeaking: false,
    endKeywords: { zh: [], yue: [], en: [] },
    farewellMessage: { zh: '', yue: '', en: '' },
    transferKeywords: { zh: [], yue: [], en: [] },
    transferMessage: { zh: '', yue: '', en: '' },

    // 消息管理
    messages: [],             // [{id, role: 'user'|'ai', text, time, streaming}]
    typingMsgId: null,        // 当前 AI 正在输入的消息 ID
    addedUserTexts: new Set(),
    addedAIRounds: new Set(),
    aiRoundText: {},          // roundid -> accumulated text
    aiRoundLast: {},          // roundid -> last chunk (for dedup)
    aiRoundMsgId: {},         // roundid -> message bubble id
};

const USER_CFG = {
    lang: I18N.getLang(),
    mode: 'voice',            // voice | avatar
    inputMode: 'voice',       // voice | text
    interruptMode: 0,
    interruptSpeechDuration: 600,
    vadLevel: 3,
    vadSilenceTime: 600,
    turnDetectionMode: 3,
};

const $ = (id) => document.getElementById(id);

// Avatar CDN fallback (when local avatars are missing, e.g. ClawHub install without .png)
const AVATAR_CDN = 'https://raw.githubusercontent.com/jerryang-cool/trtc-ai-customer-service-skill/main/assets/static/avatars';

// ========== DOM refs ==========
const els = {
    sidebar: $('sidebar'),
    sidebarOverlay: $('sidebar-overlay'),
    btnToggleSidebar: $('btn-toggle-sidebar'),
    toggleSidebarText: $('toggle-sidebar-text'),
    langSwitchLabel: $('lang-switch-label'),
    langFlag: $('lang-flag'),
    langDropdown: $('lang-dropdown'),
    langToggle: $('lang-toggle'),
    langMenu: $('lang-menu'),
    modeSwitch: $('mode-switch'),
    modeAvatarBtn: $('mode-avatar-btn'),
    turnSwitch: $('turn-switch'),
    interruptSwitch: $('interrupt-switch'),
    advToggle: $('adv-toggle'),
    advContainer: $('adv-container'),
    sliderVadSilence: $('slider-vad-silence'),
    valVadSilence: $('val-vad-silence'),
    sliderVadLevel: $('slider-vad-level'),
    valVadLevel: $('val-vad-level'),
    sliderInterruptDuration: $('slider-interrupt-duration'),
    valInterruptDuration: $('val-interrupt-duration'),
    groupInterruptDuration: $('group-interrupt-duration'),

    agentSelectArea: $('agent-select-area'),
    agentCards: $('agent-cards'),
    avatarImgFemale: $('avatar-img-female'),
    avatarImgMale: $('avatar-img-male'),
    btnStart: $('btn-start'),

    chatArea: $('chat-area'),
    chatMessages: $('chat-messages'),
    avatarVideoLayer: $('avatar-video-layer'),
    avatarVideoContainer: $('avatar-video-container'),
    voicePanel: $('voice-panel'),
    textPanel: $('text-panel'),
    voiceStatus: $('voice-status'),
    micBtn: $('mic-btn'),
    btnInputModeSwitch: $('btn-input-mode-switch'),
    modeIconKeyboard: $('mode-icon-keyboard'),
    modeIconMic: $('mode-icon-mic'),
    textInput: $('text-input'),
    btnEnd: $('btn-end'),
    btnEnd: $('btn-end'),

    ratingOverlay: $('rating-overlay'),
    ratingMain: $('rating-main'),
    ratingThanks: $('rating-thanks'),
    ratingDimensions: $('rating-dimensions'),
    btnRatingSkip: $('btn-rating-skip'),
    btnRatingSubmit: $('btn-rating-submit'),
    btnRatingClose: $('btn-rating-close'),
    btnRatingRestart: $('btn-rating-restart'),
    ratingThanksDesc: $('rating-thanks-desc'),
};

let trtcClient = null;

// ========== Utils ==========
function randomId(n = 6) {
    const chars = 'abcdefghijklmnop';
    let s = '';
    for (let i = 0; i < n; i++) s += chars[Math.floor(Math.random() * chars.length)];
    return s;
}
function uuid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
        const r = Math.random() * 16 | 0;
        return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
}
function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
async function postAction(action, payload) {
    const res = await fetch('/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Action': action },
        body: JSON.stringify(payload || {}),
    });
    return res.json();
}

// ========== Mock 订单数据（从 mock-orders.json 加载，方便用户自定义商品） ==========
const _oi = (emoji) => `data:image/svg+xml,${encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80"><rect width="80" height="80" rx="8" fill="%23F3F4F6"/><text x="50%" y="54%" text-anchor="middle" dominant-baseline="middle" font-size="36">${emoji}</text></svg>`)}`;

// 默认订单（如果 mock-orders.json 加载失败则使用）
let MOCK_ORDERS = [
    { id: 'CS20260510001', name: { zh: '无线降噪耳机 Pro', yue: '無線降噪耳機 Pro', en: 'Wireless ANC Headphones Pro' }, price: { zh: '¥699', yue: 'HK$759', en: '$96' }, status: 'shipped', date: '2026-05-10', emoji: '🎧' },
    { id: 'CS20260508002', name: { zh: '轻薄笔记本电脑 14寸', yue: '輕薄筆記本電腦 14吋', en: 'Ultra-slim Laptop 14"' }, price: { zh: '¥5,299', yue: 'HK$5,749', en: '$729' }, status: 'delivered', date: '2026-05-08', emoji: '💻' },
    { id: 'CS20260507003', name: { zh: '智能手表 S9', yue: '智能手錶 S9', en: 'Smart Watch S9' }, price: { zh: '¥1,299', yue: 'HK$1,409', en: '$179' }, status: 'pending', date: '2026-05-07', emoji: '⌚' },
    { id: 'CS20260505004', name: { zh: '真皮双肩包', yue: '真皮雙肩包', en: 'Genuine Leather Backpack' }, price: { zh: '¥399', yue: 'HK$433', en: '$55' }, status: 'refunding', date: '2026-05-05', emoji: '🎒' },
    { id: 'CS20260501005', name: { zh: '空气炸锅 5L', yue: '空氣炸鍋 5L', en: 'Air Fryer 5L' }, price: { zh: '¥259', yue: 'HK$281', en: '$36' }, status: 'delivered', date: '2026-05-01', emoji: '🍳' },
];

// 尝试从 mock-orders.json 加载自定义订单数据
fetch('/static/mock-orders.json').then(r => r.ok ? r.json() : Promise.reject()).then(data => {
    if (Array.isArray(data) && data.length > 0) {
        MOCK_ORDERS = data.map(o => ({ ...o, img: o.img || _oi(o.emoji || '📦') }));
        if (STATE.callState === 'active') renderOrderList();
    }
}).catch(() => {});

// 确保所有订单都有 img 字段
MOCK_ORDERS = MOCK_ORDERS.map(o => ({ ...o, img: o.img || _oi(o.emoji || '📦') }));

// ========== 转人工关键词检测 ==========
function detectTransferKeyword(text) {
    if (!text) return null;
    const list = STATE.transferKeywords[USER_CFG.lang] || [];
    for (const kw of list) if (buildKeywordRegex(kw).test(text)) return kw;
    return null;
}

// ========== 关键词词边界检测 ==========
function buildKeywordRegex(keyword) {
    const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    if (/[\u4e00-\u9fa5]/.test(keyword)) {
        // 中文：两侧不能紧邻同类字符（中文 / 字母数字）
        return new RegExp(`(^|[^\\u4e00-\\u9fa5A-Za-z0-9])${escaped}(?=[^\\u4e00-\\u9fa5A-Za-z0-9]|$)`, 'i');
    }
    return new RegExp(`\\b${escaped}\\b`, 'i');
}
function detectEndKeyword(text) {
    if (!text) return null;
    const list = STATE.endKeywords[USER_CFG.lang] || [];
    for (const kw of list) if (buildKeywordRegex(kw).test(text)) return kw;
    return null;
}

// ========== 消息气泡渲染 ==========
function avatarFileName(lang, gender) {
    return `${lang === 'yue' ? 'zh' : lang}_${gender || 'female'}.png`;
}
function getAgentAvatarUrl() {
    return `/static/avatars/${avatarFileName(USER_CFG.lang, STATE.gender)}`;
}
function avatarOnError(img) {
    // Fallback to GitHub CDN if local avatar is missing
    const src = img.getAttribute('src') || '';
    if (!src.startsWith(AVATAR_CDN)) {
        const filename = src.split('/').pop();
        img.src = `${AVATAR_CDN}/${filename}`;
    }
}

function renderMessage(msg) {
    // 系统通知（居中灰色文字）
    if (msg.role === 'system') {
        return `<div class="message system" data-msg-id="${msg.id}"><span class="system-notice">${escapeHtml(msg.text)}</span></div>`;
    }

    const isUser = msg.role === 'user';
    const avatarEl = isUser
        ? `<div class="msg-avatar">我</div>`
        : `<div class="msg-avatar"><img src="${getAgentAvatarUrl()}" alt="agent" onerror="avatarOnError(this)"></div>`;

    // 订单卡片渲染
    if (msg.card) {
        const c = msg.card;
        const statusCls = 'order-status-' + c.status;
        return `
            <div class="message user" data-msg-id="${msg.id}">
                ${avatarEl}
                <div class="msg-card">
                    <img class="msg-card-img" src="${c.img}" alt="">
                    <div class="msg-card-body">
                        <div class="msg-card-name">${escapeHtml(c.localName)}</div>
                        <div class="msg-card-meta">${c.id}</div>
                        <div class="msg-card-bottom">
                            <span class="msg-card-price">${c.localPrice || c.price?.zh || ''}</span>
                            <span class="order-status ${statusCls}">${c.statusText}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    const bubbleCls = msg.streaming ? 'msg-bubble typing-bubble' : 'msg-bubble';
    const content = msg.streaming && !msg.text
        ? `<div class="dots"><span></span><span></span><span></span></div>`
        : escapeHtml(msg.text || '');
    // 打断按钮：AI 消息 + streaming + 手动打断模式 + active 状态
    const showInterrupt = !isUser
        && msg.streaming
        && USER_CFG.interruptMode === 1
        && STATE.callState === 'active';
    const interruptBtn = showInterrupt
        ? `<button class="btn-interrupt" onclick="sendInterrupt()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><rect x="9" y="9" width="6" height="6" rx="0.5" fill="currentColor" stroke="none"/></svg>
            <span data-i18n="btnInterrupt">${I18N.t('btnInterrupt')}</span>
          </button>`
        : '';
    const bubbleAndBtn = isUser
        ? `<div class="${bubbleCls}">${content}</div>`
        : `<div class="ai-col">
             <div class="${bubbleCls}">${content}</div>
             ${interruptBtn}
           </div>`;
    return `
        <div class="message ${isUser ? 'user' : 'ai'}" data-msg-id="${msg.id}">
            ${avatarEl}
            ${bubbleAndBtn}
        </div>
    `;
}

function renderAllMessages() {
    els.chatMessages.innerHTML = STATE.messages.map(renderMessage).join('');
    els.chatMessages.scrollTop = els.chatMessages.scrollHeight;
}

function addMessage(role, text, opts = {}) {
    const msg = {
        id: opts.id || uuid(),
        role,
        text,
        time: Date.now(),
        streaming: !!opts.streaming,
    };
    STATE.messages.push(msg);
    renderAllMessages();
    return msg.id;
}

function setSystemNotice(text, noticeId) {
    const id = noticeId || '_sys_notice';
    const existing = STATE.messages.find(m => m.id === id);
    if (existing) {
        existing.text = text;
        const el = els.chatMessages.querySelector(`[data-msg-id="${id}"] .system-notice`);
        if (el) { el.textContent = text; els.chatMessages.scrollTop = els.chatMessages.scrollHeight; return id; }
        renderAllMessages();
        return id;
    }
    const msg = { id, role: 'system', text, time: Date.now(), streaming: false };
    STATE.messages.push(msg);
    renderAllMessages();
    return id;
}

function removeSystemNotice(noticeId) {
    const id = noticeId || '_sys_notice';
    const idx = STATE.messages.findIndex(m => m.id === id);
    if (idx !== -1) { STATE.messages.splice(idx, 1); renderAllMessages(); }
}

function updateMessage(id, text, opts = {}) {
    const msg = STATE.messages.find(m => m.id === id);
    if (!msg) return;
    const streamingChanged = typeof opts.streaming !== 'undefined' && msg.streaming !== !!opts.streaming;
    msg.text = text;
    if (typeof opts.streaming !== 'undefined') msg.streaming = opts.streaming;
    // 只更新这一条的内容，避免整体重绘
    const el = els.chatMessages.querySelector(`[data-msg-id="${id}"]`);
    if (el) {
        const bubble = el.querySelector('.msg-bubble');
        if (bubble) {
            bubble.classList.toggle('typing-bubble', !!msg.streaming);
            if (msg.streaming && !text) {
                bubble.innerHTML = `<div class="dots"><span></span><span></span><span></span></div>`;
            } else {
                bubble.innerHTML = escapeHtml(text);
            }
        }
        els.chatMessages.scrollTop = els.chatMessages.scrollHeight;
        if (streamingChanged) updateInterruptBtn();
    } else {
        renderAllMessages();
    }
}

// ========== AI 状态 ==========
function updateInterruptBtn() {
    // 同步所有 AI 消息气泡下方的打断按钮显隐
    const shouldShow = (msg) => !!msg && msg.role === 'ai'
        && msg.streaming
        && USER_CFG.interruptMode === 1
        && STATE.callState === 'active';

    STATE.messages.forEach(msg => {
        if (msg.role !== 'ai' || msg.role === 'system') return;
        const el = els.chatMessages.querySelector(`[data-msg-id="${msg.id}"] .ai-col`);
        if (!el) return;
        const existing = el.querySelector('.btn-interrupt');
        if (shouldShow(msg)) {
            if (!existing) {
                const btnHtml = `<button class="btn-interrupt" onclick="sendInterrupt()">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><rect x="9" y="9" width="6" height="6" rx="0.5" fill="currentColor" stroke="none"/></svg>
                    <span>${I18N.t('btnInterrupt')}</span>
                </button>`;
                el.insertAdjacentHTML('beforeend', btnHtml);
            }
        } else if (existing) {
            existing.remove();
        }
    });
}

const STATUS_MAP = {
    1: 'statusListening',
    2: 'statusThinking',
    3: 'statusSpeaking',
    4: 'statusInterrupted',
    5: 'statusFinished',
};
function setAIStatus(state) {
    const key = STATUS_MAP[state];
    if (!key) return;
    els.voiceStatus.textContent = I18N.t(key);

    // 追踪 AI 说话状态，控制打断按钮
    STATE.aiSpeaking = (state === 3);
    updateInterruptBtn();

    // 状态为"思考中"时给用户消息加一条 AI 打字中的占位气泡
    if (state === 2 && !STATE.typingMsgId) {
        STATE.typingMsgId = addMessage('ai', '', { streaming: true });
    }
    // 告别/转接流程中，state=5（已说完）即表示推送文本播报完成，立即触发后续流程
    // 与 REMOTE_USER_LEAVE 双保险：谁先到谁触发
    if (state === 5 && (STATE.callState === 'ending' || STATE.callState === 'transferring')) {
        if (STATE._onRobotLeave) {
            STATE._onRobotLeave();
            STATE._onRobotLeave = null;
        }
    }
}

// ========== TRTC 自定义消息处理 ==========
function handleMessage(data, eventUserId) {
    // type 10001: AI 状态
    if (data.type === 10001) {
        const state = data.payload?.state;
        if (state) setAIStatus(state);
        return;
    }
    // type 10000: 字幕
    if (data.type === 10000) {
        const text = data.payload?.text || '';
        const sender = data.sender || eventUserId || '';
        const end = data.payload?.end === true;
        const roundid = data.payload?.roundid || '';
        const isUser = (sender === STATE.userId);

        if (isUser) {
            // 用户语音 ASR 结果（仅在 end=true 才落气泡，避免累积乱码）
            if (end && text.trim() && !STATE.addedUserTexts.has(text)) {
                STATE.addedUserTexts.add(text);
                addMessage('user', text);
                // 转人工关键词检测（优先于结束关键词）
                const transferHit = detectTransferKeyword(text);
                if (transferHit) {
                    console.log(`🔄 转人工关键词命中: "${transferHit}"`);
                    triggerTransfer();
                    return;
                }
                // 结束关键词检测
                const hit = detectEndKeyword(text);
                if (hit) {
                    console.log(`🛑 结束关键词命中: "${hit}"`);
                    farewellAndEnd();
                }
            }
        } else {
            // AI 字幕（增量/累积自适应）
            if (text.trim() && roundid) {
                const last = STATE.aiRoundLast[roundid] || '';
                const cur = STATE.aiRoundText[roundid] || '';
                const isAccumulative = last && text.startsWith(last);
                STATE.aiRoundText[roundid] = isAccumulative ? text : cur + text;
                STATE.aiRoundLast[roundid] = text;

                // 确保有一个气泡对应该 round
                let msgId = STATE.aiRoundMsgId[roundid];
                if (!msgId) {
                    // 复用"思考中"占位，或新建
                    if (STATE.typingMsgId) {
                        msgId = STATE.typingMsgId;
                        STATE.typingMsgId = null;
                    } else {
                        msgId = addMessage('ai', '', { streaming: true });
                    }
                    STATE.aiRoundMsgId[roundid] = msgId;
                }
                updateMessage(msgId, STATE.aiRoundText[roundid], { streaming: !end });
            }
            if (end && roundid) {
                const msgId = STATE.aiRoundMsgId[roundid];
                if (msgId) updateMessage(msgId, STATE.aiRoundText[roundid] || text, { streaming: false });
                STATE.addedAIRounds.add(roundid);
                delete STATE.aiRoundText[roundid];
                delete STATE.aiRoundLast[roundid];
                delete STATE.aiRoundMsgId[roundid];
            }
        }
    }
}

// ========== 启动对话 ==========
async function startCall() {
    if (typeof TRTC === 'undefined') {
        alert(I18N.t('tipSdkLoadFailed'));
        return;
    }
    if (STATE.callState !== 'idle') return;

    STATE.callState = 'connecting';
    els.btnStart.disabled = true;

    // 重置
    STATE.messages = [];
    STATE.addedUserTexts = new Set();
    STATE.addedAIRounds = new Set();
    STATE.aiRoundText = {};
    STATE.aiRoundLast = {};
    STATE.aiRoundMsgId = {};
    STATE.typingMsgId = null;
    STATE.muted = false;
    STATE.localMuted = false;
    renderAllMessages();

    // 重置麦克风/静音按钮 UI
    const btnMuteEl = $('btn-mute');
    if (btnMuteEl) { btnMuteEl.classList.remove('muted'); btnMuteEl.title = I18N.t('btnMute'); }
    const micBtnEl = $('mic-btn');
    if (micBtnEl) micBtnEl.classList.remove('muted');

    STATE.userId = randomId(6);
    STATE.roomId = Math.floor(Math.random() * 90000) + 10000;

    try {
        const joinRsp = await postAction('join', { userid: STATE.userId });
        if (joinRsp.Response?.Error) throw new Error(joinRsp.Response.Error.Message);

        STATE.sdkAppId = joinRsp.sdkappid;
        STATE.userSig = joinRsp.usersig;
        STATE.robotUserId = joinRsp.robot_userid;
        STATE.robotUserSig = joinRsp.robot_usersig;
        STATE.avatarUserId = joinRsp.avatar_userid || '';
        STATE.avatarUserSig = joinRsp.avatar_usersig || '';
        STATE.avatarAvailable = !!joinRsp.avatar_available;
        STATE.endKeywords = joinRsp.end_keywords || { zh: [], yue: [], en: [] };
        STATE.farewellMessage = joinRsp.farewell_message || { zh: '', yue: '', en: '' };
        STATE.transferKeywords = joinRsp.transfer_keywords || { zh: [], yue: [], en: [] };
        STATE.transferMessage = joinRsp.transfer_message || { zh: '', yue: '', en: '' };
        STATE.useAvatar = (USER_CFG.mode === 'avatar') && STATE.avatarAvailable;

        // UI 切换
        els.agentSelectArea.style.display = 'none';
        els.chatArea.classList.add('active');
        setAIStatus(1);  // listening

        // TRTC
        trtcClient = TRTC.create();
        trtcClient.on(TRTC.EVENT.CUSTOM_MESSAGE, (event) => {
            try {
                const text = new TextDecoder().decode(event.data);
                const data = JSON.parse(text);
                handleMessage(data, event.userId);
            } catch (e) { console.warn('parse msg failed', e); }
        });
        // 数字人模式：订阅远端视频流并渲染
        trtcClient.on(TRTC.EVENT.REMOTE_VIDEO_AVAILABLE, ({ userId, streamType }) => {
            if (STATE.useAvatar && userId === STATE.avatarUserId) {
                console.log('🎬 Avatar video available:', userId, streamType);
                trtcClient.startRemoteVideo({
                    userId,
                    streamType,
                    view: 'avatar-video-container',
                });
                // 激活 avatar 视频层和 UI 模式
                enterAvatarMode();
            }
        });
        // AI 机器人退房事件（StopAfterPlay 播报完成后任务自动结束，机器人退房）
        trtcClient.on(TRTC.EVENT.REMOTE_USER_LEAVE, ({ userId }) => {
            if (userId === STATE.robotUserId && STATE._onRobotLeave) {
                STATE._onRobotLeave();
                STATE._onRobotLeave = null;
            }
        });

        await trtcClient.enterRoom({
            roomId: STATE.roomId,
            scene: 'rtc',
            sdkAppId: STATE.sdkAppId,
            userId: STATE.userId,
            userSig: STATE.userSig,
        });

        // 仅麦克风（不启动摄像头）
        try {
            await trtcClient.startLocalAudio();
        } catch (e) {
            console.error('mic failed', e);
            alert(I18N.t('tipMicrophoneFailed'));
            await trtcClient.exitRoom();
            trtcClient.destroy();
            trtcClient = null;
            STATE.callState = 'idle';
            els.btnStart.disabled = false;
            els.chatArea.classList.remove('active');
            els.agentSelectArea.style.display = 'flex';
            return;
        }

        // 启动 AI
        const body = {
            RoomId: STATE.roomId,
            AgentConfig: {
                UserId: STATE.robotUserId,
                UserSig: STATE.robotUserSig,
                TargetUserId: STATE.userId,
                Lang: USER_CFG.lang,
            },
            UserConfig: {
                TurnDetectionMode: USER_CFG.turnDetectionMode,
                InterruptMode: USER_CFG.interruptMode,
                InterruptSpeechDuration: USER_CFG.interruptSpeechDuration,
                VadLevel: USER_CFG.vadLevel,
                VadSilenceTime: USER_CFG.vadSilenceTime,
                Gender: STATE.gender,
            },
            UseAvatar: STATE.useAvatar,
            AvatarConfig: {
                AvatarUserID: STATE.avatarUserId,
                AvatarUserSig: STATE.avatarUserSig,
            },
        };
        const startRsp = await postAction('StartAIConversation', body);
        if (startRsp.Response?.Error) throw new Error(startRsp.Response.Error.Message);
        STATE.taskId = startRsp.TaskId;
        if (!STATE.taskId) throw new Error('No TaskId returned');

        STATE.callState = 'active';
        STATE.startTime = Date.now();
        console.log('✅ AI started, TaskId=' + STATE.taskId);
    } catch (e) {
        console.error('startCall failed:', e);
        alert(I18N.t('tipAIStartFailed') + (e.message || e));
        try { if (trtcClient) { await trtcClient.exitRoom(); trtcClient.destroy(); trtcClient = null; } } catch {}
        STATE.callState = 'idle';
        els.btnStart.disabled = false;
        els.chatArea.classList.remove('active');
        els.agentSelectArea.style.display = 'flex';
    }
}

// ========== 转人工流程（模拟演示，实际生产中需对接真实排队/路由系统） ==========
async function triggerTransfer() {
    if (STATE.callState !== 'active') return;
    STATE.callState = 'transferring';

    const msg = STATE.transferMessage[USER_CFG.lang] || '正在转接人工客服...';
    // 不手动 addMessage，转接提示语由 ServerPushText 播报后通过字幕回调自动展示

    // 通过 ServerPushText 播报转接提示语，播报完自动结束 AI 任务
    // 等待 AI 机器人退房（StopAfterPlay=true → 播报完 → 任务结束 → 机器人退房）
    const robotLeavePromise = new Promise(resolve => {
        STATE._onRobotLeave = resolve;
        setTimeout(() => { STATE._onRobotLeave = null; resolve(); }, 30000); // 兜底超时 30s
    });
    try {
        await postAction('TransferAndStop', {
            TaskId: STATE.taskId,
            Lang: USER_CFG.lang,
            TransferText: msg,
        });
    } catch (e) { console.warn('TransferAndStop failed', e); }

    await robotLeavePromise;

    // 模拟排队进展（系统通知，同一行更新）
    const queueSteps = {
        zh: ['正在为您查找空闲客服...（演示模式）', '前方还有 5 位用户，请稍候（演示模式）', '前方还有 3 位用户，请耐心等待（演示模式）', '前方还有 1 位用户，即将为您接通（演示模式）', '正在接通中...（演示模式）'],
        yue: ['正在為您查找空閒客服...（演示模式）', '前方仲有 5 位用戶，請稍候（演示模式）', '前方仲有 3 位用戶，請耐心等待（演示模式）', '前方仲有 1 位用戶，即將為您接通（演示模式）', '正在接通中...（演示模式）'],
        en: ['Finding an available agent... (demo mode)', '5 people ahead, please hold (demo mode)', '3 people ahead, please wait (demo mode)', '1 person ahead, almost there (demo mode)', 'Connecting you now... (demo mode)'],
    };
    const busyMsg = {
        zh: '当前人工客服繁忙，已恢复AI客服为您服务（演示模式）',
        yue: '當前人工客服繁忙，已恢復AI客服為您服務（演示模式）',
        en: 'All agents busy. AI assistant resumed for you. (demo mode)',
    };
    const steps = queueSteps[USER_CFG.lang] || queueSteps.zh;
    const noticeId = '_transfer_queue';

    for (let i = 0; i < steps.length; i++) {
        await new Promise(r => setTimeout(r, 2000));
        if (STATE.callState !== 'transferring') return;
        setSystemNotice(steps[i], noticeId);
    }

    // 排队失败，恢复 AI 对话
    await new Promise(r => setTimeout(r, 2000));
    if (STATE.callState !== 'transferring') return;
    removeSystemNotice(noticeId);
    const failMsg = busyMsg[USER_CFG.lang] || busyMsg.zh;
    setSystemNotice(failMsg, '_transfer_result');

    // 重新启动 AI 对话
    try {
        const body = {
            RoomId: STATE.roomId,
            AgentConfig: {
                UserId: STATE.robotUserId,
                UserSig: STATE.robotUserSig,
                TargetUserId: STATE.userId,
                Lang: USER_CFG.lang,
            },
            UserConfig: {
                TurnDetectionMode: USER_CFG.turnDetectionMode,
                InterruptMode: USER_CFG.interruptMode,
                InterruptSpeechDuration: USER_CFG.interruptSpeechDuration,
                VadLevel: USER_CFG.vadLevel,
                VadSilenceTime: USER_CFG.vadSilenceTime,
                Gender: STATE.gender,
            },
            UseAvatar: STATE.useAvatar,
            AvatarConfig: {
                AvatarUserID: STATE.avatarUserId,
                AvatarUserSig: STATE.avatarUserSig,
            },
        };
        const startRsp = await postAction('StartAIConversation', body);
        if (startRsp.TaskId) {
            STATE.taskId = startRsp.TaskId;
            STATE.callState = 'active';
            console.log('✅ AI resumed, TaskId=' + STATE.taskId);
            return;
        }
    } catch (e) { console.warn('resume AI failed', e); }

    STATE.callState = 'active';
}

// ========== 订单面板 ==========
function toggleOrderPanel() {
    const panel = $('order-panel');
    panel.classList.toggle('active');
    if (panel.classList.contains('active')) renderOrderList();
}

function renderOrderList() {
    const list = $('order-list');
    list.innerHTML = MOCK_ORDERS.map(order => {
        const name = order.name[USER_CFG.lang] || order.name.zh;
        const price = order.price[USER_CFG.lang] || order.price.zh;
        const statusKey = 'orderStatus_' + order.status;
        const statusText = I18N.t(statusKey);
        const statusCls = 'order-status-' + order.status;
        return `
            <div class="order-item">
                <img class="order-img" src="${order.img}" alt="">
                <div class="order-info">
                    <div class="order-name">${escapeHtml(name)}</div>
                    <div class="order-meta">${order.id} · ${order.date}</div>
                    <div class="order-bottom">
                        <span class="order-price">${price}</span>
                        <span class="order-status ${statusCls}">${statusText}</span>
                    </div>
                </div>
                <button class="order-send-btn" onclick="sendOrderCard('${order.id}')">${I18N.t('orderSend')}</button>
            </div>
        `;
    }).join('');
}

function sendOrderCard(orderId) {
    const order = MOCK_ORDERS.find(o => o.id === orderId);
    if (!order || !trtcClient || STATE.callState !== 'active') return;

    const name = order.name[USER_CFG.lang] || order.name.zh;
    const price = order.price[USER_CFG.lang] || order.price.zh;
    const statusText = I18N.t('orderStatus_' + order.status);

    // UI 显示订单卡片气泡
    const cardMsg = {
        id: uuid(),
        role: 'user',
        text: '',
        time: Date.now(),
        streaming: false,
        card: { ...order, localName: name, localPrice: price, statusText },
    };
    STATE.messages.push(cardMsg);
    renderAllMessages();

    // 发送纯文本给 AI（让 AI 理解订单上下文，语言与当前模式一致）
    let textForAI;
    if (USER_CFG.lang === 'en') {
        textForAI = `[Order Info] Order ID: ${order.id}, Product: ${name}, Price: ${price}, Status: ${statusText}, Date: ${order.date}`;
    } else if (USER_CFG.lang === 'yue') {
        textForAI = `[訂單信息] 訂單號: ${order.id}, 商品: ${name}, 價格: ${price}, 狀態: ${statusText}, 落單日期: ${order.date}`;
    } else {
        textForAI = `[订单信息] 订单号: ${order.id}, 商品: ${name}, 价格: ${price}, 状态: ${statusText}, 下单日期: ${order.date}`;
    }
    STATE.addedUserTexts.add(textForAI);

    const message = {
        type: 20000,
        sender: STATE.userId,
        receiver: [STATE.robotUserId],
        payload: { id: uuid(), message: textForAI, timestamp: Date.now() },
    };
    try {
        trtcClient.sendCustomMessage({
            cmdId: 2,
            data: new TextEncoder().encode(JSON.stringify(message)).buffer,
        });
        console.log('📦 order card sent:', orderId);
    } catch (e) { console.error('sendOrderCard failed', e); }

    // 关闭订单面板
    $('order-panel').classList.remove('active');
}

// ========== 告别 + 结束 ==========
async function farewellAndEnd() {
    if (STATE.callState !== 'active') return;
    STATE.callState = 'ending';

    const farewell = STATE.farewellMessage[USER_CFG.lang]
        || (USER_CFG.lang === 'en'
            ? 'Alright, thank you. Goodbye!'
            : '好的，感谢咨询，再见！');

    // 等待 AI 机器人退房（StopAfterPlay=true → 播报完 → 任务结束 → 机器人退房）
    const robotLeavePromise = new Promise(resolve => {
        STATE._onRobotLeave = resolve;
        setTimeout(() => { STATE._onRobotLeave = null; resolve(); }, 30000); // 兜底超时 30s
    });
    try {
        await postAction('FarewellAndStop', {
            TaskId: STATE.taskId,
            Lang: USER_CFG.lang,
            FarewellText: farewell,
        });
    } catch (e) { console.warn('FarewellAndStop failed', e); }

    await robotLeavePromise;

    try {
        if (trtcClient) {
            await trtcClient.exitRoom();
            trtcClient.destroy();
            trtcClient = null;
        }
    } catch (e) { console.warn('exitRoom failed', e); }

    exitAvatarMode();
    STATE.callState = 'idle';
    showRatingModal();
}

// ========== 手动打断 ==========
function sendInterrupt() {
    if (!trtcClient || STATE.callState !== 'active') return;
    const message = {
        type: 20001,
        sender: STATE.userId,
        receiver: [STATE.robotUserId],
        payload: {
            id: uuid(),
            timestamp: Date.now(),
        },
    };
    try {
        trtcClient.sendCustomMessage({
            cmdId: 2,
            data: new TextEncoder().encode(JSON.stringify(message)).buffer,
        });
        console.log('✋ interrupt signal sent');
    } catch (e) { console.error('sendInterrupt failed', e); }
}

// ========== 键盘输入：直连 LLM ==========
/**
 * 发送文字消息给 AI（type=20000 自定义消息，服务端跳过 ASR 直送 LLM）
 * 参考：https://cloud.tencent.com/document/product/647/115412
 */
async function sendTextMessage() {
    const text = els.textInput.value.trim();
    if (!text || !trtcClient || STATE.callState !== 'active') return;

    // 1) UI 先展示用户消息
    STATE.addedUserTexts.add(text);
    addMessage('user', text);
    els.textInput.value = '';

    // 2) 检测转人工关键词（优先）
    const transferHit = detectTransferKeyword(text);
    if (transferHit) {
        console.log(`🔄 文本转人工关键词命中: "${transferHit}"`);
        await triggerTransfer();
        return;
    }

    // 3) 检测结束关键词
    const hit = detectEndKeyword(text);
    if (hit) {
        console.log(`🛑 文本关键词命中: "${hit}"`);
        await farewellAndEnd();
        return;
    }

    // 3) 走 type=20000 发送给 AI Bot
    const message = {
        type: 20000,
        sender: STATE.userId,
        receiver: [STATE.robotUserId],
        payload: {
            id: uuid(),
            message: text,
            timestamp: Date.now(),
        },
    };
    try {
        await trtcClient.sendCustomMessage({
            cmdId: 2,
            data: new TextEncoder().encode(JSON.stringify(message)).buffer,
        });
        console.log('📤 text message sent:', text);
    } catch (e) {
        console.error('sendCustomMessage failed', e);
    }
}

// ========== 输入模式切换 ==========
function switchInputMode(mode) {
    USER_CFG.inputMode = mode;
    if (mode === 'text') {
        els.voicePanel.classList.add('hidden');
        els.textPanel.classList.remove('hidden');
        els.modeIconKeyboard.style.display = 'none';
        els.modeIconMic.style.display = 'block';
        setTimeout(() => els.textInput.focus(), 50);
    } else {
        els.voicePanel.classList.remove('hidden');
        els.textPanel.classList.add('hidden');
        els.modeIconKeyboard.style.display = 'block';
        els.modeIconMic.style.display = 'none';
    }
}

// ========== 手动评分弹窗 ==========
const RATING_DIMENSIONS = ['overall', 'resolution', 'professionalism', 'friendliness'];
const RATING_DIM_I18N = {
    overall: 'ratingDimOverall',
    resolution: 'ratingDimResolution',
    professionalism: 'ratingDimProfessionalism',
    friendliness: 'ratingDimFriendliness',
};
const USER_RATING = {};

function renderRatingBlocks() {
    els.ratingDimensions.innerHTML = RATING_DIMENSIONS.map(dim => `
        <div class="rating-dimension" data-dim="${dim}">
            <div class="rating-dim-header">
                <span class="rating-dim-name">${I18N.t(RATING_DIM_I18N[dim])}</span>
                <span class="rating-dim-value empty" id="rating-val-${dim}">—</span>
            </div>
            <div class="rating-blocks" data-dim="${dim}">
                ${Array.from({ length: 11 }, (_, i) =>
                    `<div class="rating-block" data-score="${i}">${i}</div>`
                ).join('')}
            </div>
        </div>
    `).join('');

    // 刷新某维度方块的高亮状态（0 ~ score 区间着色）
    function refreshDimBlocks(container, score) {
        container.querySelectorAll('.rating-block').forEach(b => {
            const s = parseInt(b.dataset.score, 10);
            b.classList.toggle('selected', s <= score);
        });
    }

    els.ratingDimensions.querySelectorAll('.rating-blocks').forEach(row => {
        // hover 预览：鼠标移入时临时高亮区间
        row.addEventListener('mouseover', (e) => {
            const block = e.target.closest('.rating-block');
            if (!block) return;
            const hoverScore = parseInt(block.dataset.score, 10);
            refreshDimBlocks(row, hoverScore);
        });
        // hover 离开：恢复到已选分数（无选择则清除所有）
        row.addEventListener('mouseleave', () => {
            const dim = row.dataset.dim;
            const selected = USER_RATING[dim];
            if (typeof selected !== 'undefined') {
                refreshDimBlocks(row, selected);
            } else {
                row.querySelectorAll('.rating-block').forEach(b => b.classList.remove('selected'));
            }
        });
    });

    els.ratingDimensions.querySelectorAll('.rating-block').forEach(block => {
        block.addEventListener('click', () => {
            const score = parseInt(block.dataset.score, 10);
            const dim = block.parentElement.dataset.dim;
            USER_RATING[dim] = score;
            refreshDimBlocks(block.parentElement, score);
            // 显示分数
            const valEl = $(`rating-val-${dim}`);
            valEl.textContent = score;
            valEl.classList.remove('empty');
            // 检查是否至少"整体满意度"已评
            els.btnRatingSubmit.disabled = typeof USER_RATING.overall === 'undefined';
        });
    });
}

function showRatingModal() {
    els.ratingOverlay.classList.add('active');
    els.ratingMain.classList.remove('hidden');
    els.ratingThanks.classList.remove('active');
    Object.keys(USER_RATING).forEach(k => delete USER_RATING[k]);
    renderRatingBlocks();
    els.btnRatingSubmit.disabled = true;
}

function submitRating() {
    // 至少要评 overall
    if (typeof USER_RATING.overall === 'undefined') return;
    console.log('⭐ user rating:', USER_RATING);
    // 展示感谢页
    els.ratingMain.classList.add('hidden');
    els.ratingThanks.classList.add('active');
    els.ratingThanksDesc.textContent = I18N.t('ratingThanksDesc', { overall: USER_RATING.overall });
}

function closeRating() {
    els.ratingOverlay.classList.remove('active');
    // 回到客服选择
    els.chatArea.classList.remove('active');
    els.chatArea.classList.remove('avatar-mode');
    if (els.avatarVideoLayer) els.avatarVideoLayer.classList.remove('active');
    els.agentSelectArea.style.display = 'flex';
    els.btnStart.disabled = false;
    // 重置输入模式
    switchInputMode('voice');
    // 重置麦克风/静音状态
    STATE.muted = false;
    STATE.localMuted = false;
    const btnMuteEl = $('btn-mute');
    if (btnMuteEl) { btnMuteEl.classList.remove('muted'); btnMuteEl.title = I18N.t('btnMute'); }
    const micBtnEl = $('mic-btn');
    if (micBtnEl) micBtnEl.classList.remove('muted');
}

// ========== 静音切换 ==========
function toggleMute() {
    if (!trtcClient || STATE.callState !== 'active') return;
    STATE.muted = !STATE.muted;
    trtcClient.setRemoteAudioVolume(STATE.robotUserId, STATE.muted ? 0 : 100);
    const btn = $('btn-mute');
    if (btn) {
        btn.classList.toggle('muted', STATE.muted);
        btn.title = STATE.muted ? I18N.t('btnUnmute') : I18N.t('btnMute');
    }
    console.log('🔇 remote mute:', STATE.muted);
}

function toggleLocalMute() {
    if (!trtcClient || STATE.callState !== 'active') return;
    STATE.localMuted = !STATE.localMuted;
    trtcClient.updateLocalAudio({ mute: STATE.localMuted });
    const btn = $('mic-btn');
    if (btn) btn.classList.toggle('muted', STATE.localMuted);
    console.log('🎤 local mute:', STATE.localMuted);
}

// ========== Mobile detection ==========
function isMobile() { return window.innerWidth <= 768; }

function toggleSidebar(forceCollapse) {
    const shouldCollapse = typeof forceCollapse === 'boolean'
        ? forceCollapse
        : !els.sidebar.classList.contains('collapsed');
    els.sidebar.classList.toggle('collapsed', shouldCollapse);
    if (els.sidebarOverlay) {
        els.sidebarOverlay.classList.toggle('active', !shouldCollapse && isMobile());
    }
    els.toggleSidebarText.textContent = I18N.t(shouldCollapse ? 'expandConfig' : 'collapseConfig');
}

// ========== 事件绑定 ==========
function bindEvents() {
    els.btnToggleSidebar.addEventListener('click', () => toggleSidebar());
    // 遮罩层点击关闭侧边栏
    if (els.sidebarOverlay) {
        els.sidebarOverlay.addEventListener('click', () => toggleSidebar(true));
    }
    // 移动端默认收起侧边栏
    if (isMobile()) toggleSidebar(true);

    // Pill 切换
    const bindPill = (container, cfgKey, parser = (v) => v) => {
        container.querySelectorAll('.pill').forEach(btn => {
            btn.addEventListener('click', () => {
                if (btn.disabled) return;
                container.querySelectorAll('.pill').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                USER_CFG[cfgKey] = parser(btn.dataset.value);
            });
        });
    };
    bindPill(els.modeSwitch, 'mode');
    bindPill(els.turnSwitch, 'turnDetectionMode', (v) => parseInt(v, 10));
    bindPill(els.interruptSwitch, 'interruptMode', (v) => {
        const mode = parseInt(v, 10);
        // 联动启用/禁用打断响应延迟滑块
        setTimeout(() => {
            const enabled = mode === 0;
            els.groupInterruptDuration.classList.toggle('slider-disabled', !enabled);
            els.sliderInterruptDuration.disabled = !enabled;
            updateAIForConfigChange();
        }, 0);
        return mode;
    });

    // 基础设置折叠
    const basicToggle = $('basic-toggle');
    const basicContainer = $('basic-container');
    basicToggle.addEventListener('click', () => {
        basicToggle.classList.toggle('collapsed');
        basicContainer.style.display = basicToggle.classList.contains('collapsed') ? 'none' : 'block';
    });

    // 高级设置折叠
    els.advToggle.addEventListener('click', () => {
        els.advToggle.classList.toggle('collapsed');
        els.advContainer.style.display = els.advToggle.classList.contains('collapsed') ? 'none' : 'block';
    });

    // 滑块
    const bindSlider = (slider, valEl, key, unit = '') => {
        slider.addEventListener('input', () => {
            valEl.innerHTML = slider.value + (unit ? `<span class="slider-unit">${unit}</span>` : '');
            USER_CFG[key] = parseInt(slider.value, 10);
        });
    };
    bindSlider(els.sliderVadSilence, els.valVadSilence, 'vadSilenceTime', 'ms');
    bindSlider(els.sliderVadLevel, els.valVadLevel, 'vadLevel');
    bindSlider(els.sliderInterruptDuration, els.valInterruptDuration, 'interruptSpeechDuration', 'ms');

    // 打断时长滑块松手时实时更新 AI 配置
    if (els.sliderInterruptDuration) {
        els.sliderInterruptDuration.addEventListener('change', () => updateAIForConfigChange());
    }

    // 客服选择
    els.agentCards.querySelectorAll('.agent-card').forEach(card => {
        card.addEventListener('click', () => {
            els.agentCards.querySelectorAll('.agent-card').forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            STATE.gender = card.dataset.gender;
        });
    });

    els.btnStart.addEventListener('click', startCall);
    els.btnEnd.addEventListener('click', farewellAndEnd);

    // 静音按钮
    const btnMute = $('btn-mute');
    if (btnMute) btnMute.addEventListener('click', toggleMute);
    // 麦克风静音按钮
    const micBtn = $('mic-btn');
    if (micBtn) micBtn.addEventListener('click', toggleLocalMute);

    // 订单按钮
    const btnOrders = $('btn-orders');
    if (btnOrders) btnOrders.addEventListener('click', toggleOrderPanel);
    // 转人工按钮
    const btnTransfer = $('btn-transfer');
    if (btnTransfer) btnTransfer.addEventListener('click', triggerTransfer);

    // 输入模式切换
    els.btnInputModeSwitch.addEventListener('click', () => {
        switchInputMode(USER_CFG.inputMode === 'voice' ? 'text' : 'voice');
    });

    // 文字输入（Enter 发送）
    els.textInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendTextMessage();
        }
    });

    // 评分弹窗
    els.btnRatingSkip.addEventListener('click', closeRating);
    els.btnRatingSubmit.addEventListener('click', submitRating);
    els.btnRatingClose.addEventListener('click', closeRating);
    els.btnRatingRestart.addEventListener('click', closeRating);

    // 语言变化
    window.addEventListener('langChange', () => {
        USER_CFG.lang = I18N.getLang();
        applyI18n();
        // 同步头像图（语言影响欧美/亚洲脸）
        updateAvatarImages();
        // 对话中切换语言 → 更新订单列表 + 聊天头像 + 调用 UpdateAIConversation
        if (STATE.callState === 'active' && STATE.taskId) {
            // 重新渲染消息（更新聊天中的客服头像）
            renderAllMessages();
            // 刷新订单面板（如果打开中）
            const orderPanel = $('order-panel');
            if (orderPanel && orderPanel.classList.contains('active')) renderOrderList();
            // 调用后端更新 AI 对话配置（TTSConfig + LLMConfig + STTConfig）
            updateAIForLangSwitch();
        }
    });

    // 语言下拉框交互
    if (els.langToggle) {
        els.langToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            els.langDropdown.classList.toggle('open');
        });
    }
    if (els.langMenu) {
        els.langMenu.addEventListener('click', (e) => {
            const item = e.target.closest('.lang-dropdown-item');
            if (!item) return;
            const lang = item.dataset.lang;
            if (lang) I18N.setLang(lang);
            els.langDropdown.classList.remove('open');
        });
    }
    // 点击其他区域关闭下拉框
    document.addEventListener('click', () => {
        if (els.langDropdown) els.langDropdown.classList.remove('open');
    });
}

// ========== 头像图随语言切换 ==========
function updateAvatarImages() {
    const lang = USER_CFG.lang === 'yue' ? 'zh' : USER_CFG.lang;
    els.avatarImgFemale.src = `/static/avatars/${lang}_female.png`;
    els.avatarImgFemale.onerror = function() { avatarOnError(this); };
    els.avatarImgMale.src = `/static/avatars/${lang}_male.png`;
    els.avatarImgMale.onerror = function() { avatarOnError(this); };
}

// ========== 对话中切换语言 → 更新 AI 配置 ==========
async function updateAIForLangSwitch() {
    if (!STATE.taskId || STATE.callState !== 'active') return;
    try {
        const rsp = await postAction('UpdateAIConversation', {
            TaskId: STATE.taskId,
            Lang: USER_CFG.lang,
            Gender: STATE.gender,
            UpdateWelcome: true,
        });
        if (rsp.Response?.Error) {
            console.warn('UpdateAIConversation failed:', rsp.Response.Error.Message);
        } else {
            console.log('🔄 AI config updated for lang:', USER_CFG.lang);
        }
    } catch (e) {
        console.warn('UpdateAIConversation error:', e);
    }
}

// ========== 对话中调整侧边栏配置 → 实时更新 ==========
async function updateAIForConfigChange() {
    if (!STATE.taskId || STATE.callState !== 'active') return;
    try {
        const rsp = await postAction('UpdateAIConversation', {
            TaskId: STATE.taskId,
            InterruptMode: USER_CFG.interruptMode,
            InterruptSpeechDuration: USER_CFG.interruptSpeechDuration,
        });
        if (rsp.Response?.Error) {
            console.warn('UpdateAIConversation config failed:', rsp.Response.Error.Message);
        } else {
            console.log('🔄 AI config updated: interrupt=%d/%dms', USER_CFG.interruptMode, USER_CFG.interruptSpeechDuration);
        }
    } catch (e) {
        console.warn('UpdateAIConversation config error:', e);
    }
}

// ========== 数字人视频模式 ==========
function enterAvatarMode() {
    if (!els.avatarVideoLayer || !els.chatArea) return;
    els.avatarVideoLayer.classList.add('active');
    els.chatArea.classList.add('avatar-mode');
    console.log('🎬 Entered avatar video mode');
}

function exitAvatarMode() {
    if (!els.avatarVideoLayer || !els.chatArea) return;
    els.avatarVideoLayer.classList.remove('active');
    els.chatArea.classList.remove('avatar-mode');
    // 停止远端视频
    if (trtcClient && STATE.avatarUserId) {
        try { trtcClient.stopRemoteVideo({ userId: STATE.avatarUserId }); } catch (e) {}
    }
    console.log('🎬 Exited avatar video mode');
}

// ========== i18n ==========
function applyI18n() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        el.textContent = I18N.t(key);
    });
    document.title = I18N.t('appName');
    if (els.textInput) els.textInput.placeholder = I18N.t('inputPlaceholder');
    // 语言下拉框更新
    const langMeta = { zh: { flag: '🇨🇳', label: '简体中文' }, yue: { flag: '🇭🇰', label: '粵語' }, en: { flag: '🇺🇸', label: 'English' } };
    const meta = langMeta[USER_CFG.lang] || langMeta.zh;
    if (els.langFlag) els.langFlag.textContent = meta.flag;
    if (els.langSwitchLabel) els.langSwitchLabel.textContent = meta.label;
    // 更新下拉菜单选中态
    document.querySelectorAll('.lang-dropdown-item').forEach(item => {
        item.classList.toggle('active', item.dataset.lang === USER_CFG.lang);
    });
    // tooltip 说明图标
    document.querySelectorAll('.tip-icon[data-tip-key]').forEach(el => {
        el.dataset.tip = I18N.t(el.dataset.tipKey);
    });
    // 收起/展开按钮文案
    if (els.toggleSidebarText) {
        const collapsed = els.sidebar.classList.contains('collapsed');
        els.toggleSidebarText.textContent = I18N.t(collapsed ? 'expandConfig' : 'collapseConfig');
    }
    // 数字人按钮可用性
    if (els.modeAvatarBtn) {
        const available = STATE.avatarAvailable;
        els.modeAvatarBtn.disabled = !available;
        els.modeAvatarBtn.textContent = available ? I18N.t('modeAvatar') : I18N.t('modeAvatarDisabled');
        if (!available && USER_CFG.mode === 'avatar') {
            USER_CFG.mode = 'voice';
            els.modeSwitch.querySelectorAll('.pill').forEach(b => {
                b.classList.toggle('active', b.dataset.value === 'voice');
            });
        }
    }
}

// ========== 启动前探测数字人可用性 ==========
async function probeAvatarAvailability() {
    try {
        const rsp = await postAction('join', { userid: 'probe' + randomId(4) });
        if (rsp && typeof rsp.avatar_available !== 'undefined') {
            STATE.avatarAvailable = !!rsp.avatar_available;
            STATE.endKeywords = rsp.end_keywords || STATE.endKeywords;
            STATE.farewellMessage = rsp.farewell_message || STATE.farewellMessage;
            STATE.transferKeywords = rsp.transfer_keywords || STATE.transferKeywords;
            STATE.transferMessage = rsp.transfer_message || STATE.transferMessage;
        }
    } catch (e) { console.warn('probe failed', e); }
    finally { applyI18n(); }
}

// ========== 初始化 ==========
function init() {
    USER_CFG.lang = I18N.getLang();
    updateAvatarImages();
    bindEvents();
    applyI18n();
    probeAvatarAvailability();

    // --- 移动端增强 ---
    if (isMobile()) {
        // Tooltip: 点击触发（移动端无 hover）
        document.querySelectorAll('.tip-icon').forEach(el => {
            el.addEventListener('click', (e) => {
                e.stopPropagation();
                const wasActive = el.classList.contains('touched');
                document.querySelectorAll('.tip-icon.touched').forEach(t => t.classList.remove('touched'));
                if (!wasActive) el.classList.add('touched');
            });
        });
        document.addEventListener('click', () => {
            document.querySelectorAll('.tip-icon.touched').forEach(t => t.classList.remove('touched'));
        });

        // iOS Safari: 文字输入聚焦时滚动到可见区域
        if (els.textInput) {
            els.textInput.addEventListener('focus', () => {
                setTimeout(() => {
                    els.textInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }, 300);
            });
        }

        // 开始对话时自动收起侧边栏
        els.btnStart.addEventListener('click', () => toggleSidebar(true), { capture: true });
    }

    // 屏幕旋转/尺寸变化时同步遮罩状态
    window.addEventListener('resize', () => {
        if (!isMobile() && els.sidebarOverlay) {
            els.sidebarOverlay.classList.remove('active');
        }
    });
}

document.addEventListener('DOMContentLoaded', init);
