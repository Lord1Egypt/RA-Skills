/**
 * tracker.js — 通用用户测试埋点系统 v3
 *
 * ⚠️ 加载顺序（重要）：
 *   1. tracker-config.js（必须，最先引入）
 *   2. 覆盖 window.TRACKER_CONFIG 配置（如 endpoint）
 *   3. 引入本文件
 *
 * 设计目标：完整记录用户操作链路，回答"用户能否顺利用下来"
 * 可配置化：通过 window.TRACKER_CONFIG 自定义 endpoint/milestone/actionMap
 *
 * 记录维度：
 * 1. 操作序列 — 每一步操作按时间排列，还原用户行为路径
 * 2. 犹豫检测 — 进入页面后多久开始交互
 * 3. 困惑检测 — 同一元素重复点击、来回切换
 * 4. 停留时长 — 每个页面/阶段的停留
 * 5. 里程碑 — 关键节点是否到达
 * 6. 鼠标热区 — 点击坐标（用于热力图）
 */
(function(global) {
'use strict';

var cfg = global.TRACKER_CONFIG || {};
var SCF_BASE = cfg.endpoint || '';
var FLUSH_INTERVAL = cfg.flushInterval || 8000;
var MAX_QUEUE = cfg.maxQueue || 30;
var TRACKER_DISABLED = cfg.disabled || false;

var params = new URLSearchParams(location.search);
var uid = params.get('uid') || 'anon_' + Math.random().toString(36).slice(2, 8);
var testRound = params.get('test') || 'default';
var page = location.pathname.split('/').pop() || 'index';
var sessionId = uid + '_' + Date.now().toString(36);
var pageEnterTime = Date.now();

// ========== 操作序列（核心数据结构） ==========
var opLog = [];
var seqId = 0;
var firstInteractionTime = null;
var maxScrollDepth = 0;
var lastClickTarget = '';
var lastClickTime = 0;
var repeatClickCount = 0;

// ========== 事件缓冲 ==========
var eventQueue = [];

function record(type, detail) {
    seqId++;
    var now = Date.now();
    var elapsed = Math.round((now - pageEnterTime) / 1000);
    var entry = {
        seq: seqId,
        uid: uid,
        test: testRound,
        session: sessionId,
        page: page,
        type: type,
        ts: new Date().toISOString(),
        elapsed: elapsed,
        d: detail || {}
    };
    opLog.push(entry);
    eventQueue.push(entry);
    if (eventQueue.length >= MAX_QUEUE) flush();
    return entry;
}

function flush() {
    if (TRACKER_DISABLED) { eventQueue.length = 0; return; }
    if (eventQueue.length === 0) return;
    if (!SCF_BASE) { eventQueue.length = 0; return; } // 无 endpoint 时静默丢弃
    var batch = eventQueue.splice(0);
    var payload = JSON.stringify({ events: batch });
    if (navigator.sendBeacon) {
        navigator.sendBeacon(SCF_BASE + '/track', payload);
    } else {
        fetch(SCF_BASE + '/track', { method:'POST', headers:{'Content-Type':'application/json'}, body:payload, keepalive:true }).catch(function(){});
    }
}

setInterval(flush, FLUSH_INTERVAL);

// ========== 1. 页面访问 ==========
record('enter', {
    url: location.href,
    referrer: document.referrer,
    screen: screen.width + 'x' + screen.height,
    viewport: window.innerWidth + 'x' + window.innerHeight
});

// ========== 2. 犹豫检测：首次交互 ==========
function markFirstInteraction(how) {
    if (firstInteractionTime) return;
    firstInteractionTime = Date.now();
    var hesitation = Math.round((firstInteractionTime - pageEnterTime) / 1000);
    record('first_interact', { how: how, hesitation: hesitation });
}

// ========== 3. 点击（带坐标 + 重复检测） ==========
document.addEventListener('click', function(e) {
    markFirstInteraction('click');

    var el = e.target.closest('button, a, [data-track], input[type=file], select') || e.target;

    var target = describeElement(el);
    var now = Date.now();

    if (target === lastClickTarget && (now - lastClickTime) < 3000) {
        repeatClickCount++;
        if (repeatClickCount >= 3) {
            record('frustration', { target: target, repeats: repeatClickCount, hint: '反复点击同一元素，可能困惑' });
        }
    } else {
        repeatClickCount = 1;
    }
    lastClickTarget = target;
    lastClickTime = now;

    record('click', {
        target: target,
        text: (el.textContent || '').trim().slice(0, 50),
        x: Math.round(e.clientX / window.innerWidth * 100),
        y: Math.round(e.clientY / window.innerHeight * 100),
        action: identifyAction(el)
    });
}, true);

function describeElement(el) {
    if (el.id) return '#' + el.id;
    if (el.dataset && el.dataset.track) return '[track=' + el.dataset.track + ']';
    var cls = (el.className || '').toString().split(' ').filter(function(c){ return c && c.length < 30; }).slice(0,2).join('.');
    var tag = el.tagName ? el.tagName.toLowerCase() : '?';
    return cls ? tag + '.' + cls : tag;
}

function identifyAction(el) {
    // 优先使用用户自定义 actionMap
    var actionMap = (global.TRACKER_CONFIG && global.TRACKER_CONFIG.actionMap) || {};
    for (var sel in actionMap) {
        if (el.closest(sel)) return actionMap[sel];
    }
    // 默认 action 识别（通用）
    if (el.closest('button') || el.tagName === 'BUTTON') return 'button_click';
    if (el.closest('a') || el.tagName === 'A') return 'link_click';
    if (el.type === 'file' || el.closest('[type=file]')) return 'file_select';
    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') return 'input_focus';
    return '';
}

// ========== 4. 文件上传 ==========
document.addEventListener('change', function(e) {
    if (e.target.type === 'file' && e.target.files && e.target.files.length) {
        var f = e.target.files[0];
        record('file_select', { name: f.name, sizeMB: (f.size/1048576).toFixed(1), type: f.type });
    }
}, true);

// ========== 5. 输入 ==========
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        markFirstInteraction('enter_key');
        var val = e.target.value || e.target.textContent || '';
        record('input_enter', { inputId: e.target.id || describeElement(e.target), length: val.length });
    }
});
document.addEventListener('focus', function(e) {
    if (e.target.matches && e.target.matches('input, textarea, [contenteditable]')) {
        markFirstInteraction('focus_input');
        record('focus', { target: describeElement(e.target) });
    }
}, true);

// ========== 6. 滚动深度 ==========
var scrollThrottled = false;
window.addEventListener('scroll', function() {
    if (scrollThrottled) return;
    scrollThrottled = true;
    setTimeout(function() { scrollThrottled = false; }, 2000);
    markFirstInteraction('scroll');
    var h = document.documentElement;
    var depth = Math.round(((h.scrollTop + h.clientHeight) / Math.max(h.scrollHeight, 1)) * 100);
    if (depth > maxScrollDepth + 10) {
        maxScrollDepth = depth;
        record('scroll', { depth: depth });
    }
}, true);

// ========== 7. 页面可见性（切走/切回） ==========
document.addEventListener('visibilitychange', function() {
    record(document.hidden ? 'tab_away' : 'tab_back', { elapsed: Math.round((Date.now() - pageEnterTime) / 1000) });
});

// ========== 8. 页面离开 ==========
function onLeave() {
    record('leave', {
        duration: Math.round((Date.now() - pageEnterTime) / 1000),
        scrollDepth: maxScrollDepth,
        interactions: seqId,
        hesitation: firstInteractionTime ? Math.round((firstInteractionTime - pageEnterTime) / 1000) : -1
    });
    flush();
}
window.addEventListener('beforeunload', onLeave);
window.addEventListener('pagehide', onLeave);

// ========== 9. JS 错误 ==========
window.addEventListener('error', function(e) {
    record('error', { msg: (e.message||'').slice(0,150), file: (e.filename||'').split('/').pop(), line: e.lineno });
});
window.addEventListener('unhandledrejection', function(e) {
    record('error', { msg: 'Promise: ' + String(e.reason).slice(0,150) });
});

// ========== 10. 链接跳转时携带 uid/test + survey 参数 ==========
document.addEventListener('click', function(e) {
    var a = e.target.closest('a[href]');
    if (!a || !a.href) return;
    try {
        var url = new URL(a.href, location.origin);
        if (url.origin === location.origin && !url.searchParams.has('uid')) {
            url.searchParams.set('uid', uid);
            url.searchParams.set('test', testRound);
            var sp = new URLSearchParams(location.search);
            ['smode','stype','stasks','ssurveys','sexit','swelcome','scp'].forEach(function(k){
                var v = sp.get(k); if(v && !url.searchParams.has(k)) url.searchParams.set(k, v);
            });
            if(sp.get('mode')==='test' && !url.searchParams.has('smode')) url.searchParams.set('smode','test');
            a.href = url.toString();
        }
    } catch(ex) {}
}, true);

// ========== milestone 名称映射 ==========
function mapMilestone(name) {
    var m = (global.TRACKER_CONFIG && global.TRACKER_CONFIG.getMilestone);
    return m ? m.call(global.TRACKER_CONFIG, name) : name;
}

// ========== 手动埋点 API ==========
global.UserTestTracker = {
    record: record,
    flush: flush,
    uid: uid,
    testRound: testRound,
    sessionId: sessionId,

    // 里程碑（关键节点）
    milestone: function(name, extra) {
        var mapped = mapMilestone(name);
        record('milestone', Object.assign({ name: mapped, originalName: name }, extra || {}));
    },

    // 阶段开始/结束
    phaseStart: function(name) { record('phase_start', { phase: name }); },
    phaseEnd: function(name) { record('phase_end', { phase: name }); },

    // 上传进度
    uploadProgress: function(pct) { record('upload_progress', { pct: pct }); },
    uploadDone: function(url, sizeMB) { record('upload_done', { url: (url||'').slice(-60), sizeMB: sizeMB }); },
    uploadFail: function(err) { record('upload_fail', { error: err }); },

    // MPS 进度（保留，Tideo 特定）
    mpsStatus: function(status, elapsed) { record('mps_status', { status: status, elapsed: elapsed }); },

    // 问卷联动
    surveyShow: function(checkpointId, type) { record('survey_show', { checkpoint: checkpointId, type: type }); },
    surveyAnswer: function(data) { record('survey_answer', data); },
    surveySkip: function(checkpointId) { record('survey_skip', { checkpoint: checkpointId }); },
    surveyExitSubmit: function(data) { record('survey_exit_submit', data); },

    // 任务完成
    taskComplete: function(taskId, label) { record('task_complete', { taskId: taskId, label: label, elapsed: Math.round((Date.now() - pageEnterTime) / 1000) }); },

    // 获取原始 milestone 名称（映射前）
    getOriginalMilestone: mapMilestone
};

})(window);
