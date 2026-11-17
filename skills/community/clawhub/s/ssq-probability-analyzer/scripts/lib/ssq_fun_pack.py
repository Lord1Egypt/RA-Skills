# -*- coding: utf-8 -*-
"""双色球 · 招财猫萌宠 & 娱乐互动专区（Tier1 升级包）

包含 5 大娱乐模块，全部纯前端（localStorage 持久化 + 内联 JS），
零联网、零第三方依赖，直接注入 ssq_auto.py 报告模板。

模块清单：
  0. 招财猫萌宠（漂浮在报告中，会叫"主人"，陪你互动；每买一注=喂养一次）
  A. 生日 / 纪念日选号器（纯娱乐，有故事的号码）
  B. 公益贡献可视化（每注约 0.72 元进公益金，正向激励）
  C. 理性购彩成就徽章（用游戏化奖励"负责任"）
  D. 幸运卡片一键分享（canvas 导出 PNG，不涉资金、非真实跟单）

责任红线（遵守全网研究结论）：
  - 游戏化只奖励"理性行为"，绝不诱导加码消费
  - 虚拟奖励不可兑现金
  - 模拟 / 娱乐 与 真实开奖 严格区分
  - 内置诚实标注与冷静提醒
"""

# ---------------------------------------------------------------------------
# CSS（普通字符串，含 { } 不被 f-string 二次解析）
# ---------------------------------------------------------------------------
FUN_PACK_CSS = """
/* ===== 招财猫娱乐专区 ===== */
.fp-section { margin: 18px 0; }
.fp-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; margin-top: 12px; }
@media (max-width: 680px) { .fp-grid { grid-template-columns: 1fr; } }
.fp-card { background: linear-gradient(135deg, #2a1740 0%, #3a1d55 100%); border: 1px solid #7a4cff; border-radius: 14px; padding: 14px 16px; box-shadow: 0 4px 18px rgba(122,76,255,0.18); }
.fp-card h3 { margin: 0 0 8px; font-size: 15px; color: #ffd86b; display: flex; align-items: center; gap: 6px; }
.fp-card p.tip { margin: 6px 0 0; font-size: 12px; color: #c9b8ff; line-height: 1.5; }
.fp-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
.fp-input { background: rgba(255,255,255,0.08); border: 1px solid #7a4cff; color: #fff; border-radius: 8px; padding: 6px 8px; font-size: 13px; }
.fp-btn { background: linear-gradient(135deg, #ff9d3d, #ff6a3d); color: #fff; border: none; border-radius: 9px; padding: 7px 12px; font-size: 13px; cursor: pointer; transition: transform .12s, filter .12s; }
.fp-btn:hover { transform: translateY(-1px); filter: brightness(1.08); }
.fp-btn.sec { background: linear-gradient(135deg, #6c4cff, #9b7bff); }
.fp-num { display: inline-flex; align-items: center; justify-content: center; min-width: 26px; height: 26px; padding: 0 4px; margin: 2px; border-radius: 50%; font-size: 12px; font-weight: 700; color: #fff; }
.fp-num.r { background: radial-gradient(circle at 30% 30%, #ff7a7a, #d10000); }
.fp-num.b { background: radial-gradient(circle at 30% 30%, #6db8ff, #0048c8); }
.fp-out { margin-top: 8px; font-size: 13px; color: #ffe9b0; min-height: 22px; }

/* 公益进度树 */
.fp-tree { font-size: 40px; text-align: center; margin: 6px 0; transition: transform .4s; }
.fp-bar { height: 12px; border-radius: 6px; background: rgba(255,255,255,0.1); overflow: hidden; margin-top: 8px; }
.fp-bar > i { display: block; height: 100%; width: 0; background: linear-gradient(90deg, #5ee0ff, #9b7bff); transition: width .8s cubic-bezier(.2,.8,.2,1); }
.fp-charity-num { font-size: 22px; font-weight: 800; color: #5ee0ff; text-align: center; }
.fp-charity-sub { font-size: 12px; color: #c9b8ff; text-align: center; }

/* 成就徽章 */
.fp-badges { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 6px; }
.fp-badge { text-align: center; padding: 10px 4px; border-radius: 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); transition: transform .15s; }
.fp-badge .ico { font-size: 28px; filter: grayscale(1) opacity(.4); }
.fp-badge.on .ico { filter: none; }
.fp-badge.on { background: linear-gradient(135deg, rgba(255,216,107,0.18), rgba(255,154,61,0.12)); border-color: #ffd86b; }
.fp-badge .nm { font-size: 11px; color: #d8ccff; margin-top: 4px; }
.fp-badge.on .nm { color: #ffe9b0; }

/* 漂浮招财猫（精致萌版 · 互动升级） */
.cat-widget { position: fixed; right: 14px; top: 140px; z-index: 9999; width: 320px; max-width: 90vw; user-select: none; font-family: inherit; will-change: transform; }
.cat-bubble { position: relative; background: linear-gradient(135deg,#ffffff,#fff4e0); color: #8a4a00; font-size: 13px; line-height: 1.5; padding: 9px 12px; border-radius: 14px; margin-bottom: 8px; box-shadow: 0 6px 18px rgba(0,0,0,0.35); animation: catBubbleBob 3s ease-in-out infinite; min-height: 20px; }
.cat-bubble:after { content: ""; position: absolute; right: 44px; bottom: -8px; border: 8px solid transparent; border-top-color: #fff4e0; border-bottom: 0; }
@keyframes catBubbleBob { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-4px)} }
.cat-stage { display: flex; align-items: flex-end; gap: 10px; }
.cat-avatar { position: relative; width: 156px; height: 156px; cursor: pointer; animation: catFloat 3.6s ease-in-out infinite; filter: drop-shadow(0 8px 14px rgba(0,0,0,.42)); flex: 0 0 auto; }
.cat-avatar:hover { filter: drop-shadow(0 8px 18px rgba(255,180,60,.5)); }
@keyframes catFloat { 0%,100%{transform:translateY(0) rotate(-1.5deg)} 50%{transform:translateY(-11px) rotate(1.5deg)} }
.cat-avatar svg { width: 100%; height: 100%; display: block; overflow: visible; }
.cat-avatar.wave { animation: catWave .7s ease; }
@keyframes catWave { 0%,100%{transform:rotate(0) translateY(0)} 20%{transform:rotate(-8deg) translateY(-8px)} 60%{transform:rotate(8deg) translateY(-8px)} }
.cat-avatar.sleep { animation: catSleep 3.4s ease-in-out infinite; }
@keyframes catSleep { 0%,100%{transform:translateY(0) scale(1);} 50%{transform:translateY(2px) scale(1.04);} }
.cat-eye-pupil { transition: transform .12s ease-out; }
.cat-costume { transition: transform .3s, opacity .3s; transform-origin: 80px 26px; }
.cat-stats { flex: 1; font-size: 12px; color: #fff; background: rgba(34,18,54,0.94); border: 1px solid #7a4cff; border-radius: 14px; padding: 10px 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.4); }
.cat-stats .row { display: flex; justify-content: space-between; align-items: center; margin: 3px 0; }
.cat-stats b { color: #ffd86b; }
.cat-stats .lv { color: #5ee0ff; font-weight: 800; }
.cat-ring { width: 48px; height: 48px; border-radius: 50%; background: conic-gradient(#ffd24a calc(var(--p,0)*1%), rgba(255,255,255,.14) 0); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 800; color: #fff; margin: 5px auto 2px; position: relative; }
.cat-ring:after { content: ""; position: absolute; inset: 5px; border-radius: 50%; background: rgba(34,18,54,0.97); }
.cat-ring span { position: relative; z-index: 1; }
/* 需求条（饱食/精力/心情） */
.cat-needs { margin-top: 8px; }
.cat-need { display: flex; align-items: center; gap: 6px; margin: 4px 0; font-size: 11px; color: #c9b8ff; }
.cat-need .lab { width: 36px; }
.cat-need .bar { flex: 1; height: 8px; border-radius: 4px; background: rgba(255,255,255,.12); overflow: hidden; }
.cat-need .bar > i { display: block; height: 100%; width: 0; transition: width .5s; }
.cat-need.hunger .bar > i { background: linear-gradient(90deg,#ffb347,#ff7a18); }
.cat-need.energy .bar > i { background: linear-gradient(90deg,#5ee0ff,#4c8bff); }
.cat-need.mood .bar > i { background: linear-gradient(90deg,#ff8ad8,#ff4a9e); }
.cat-btns { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.cat-panel { display: none; margin-top: 8px; background: rgba(34,18,54,0.97); border: 1px solid #7a4cff; border-radius: 14px; padding: 10px; box-shadow: 0 4px 18px rgba(0,0,0,0.45); }
.cat-panel.show { display: block; }
.cat-panel input { width: 100%; box-sizing: border-box; margin-bottom: 6px; }
.cat-mini { font-size: 12px; margin: 2px 3px 0 0; }
.cat-poke { position: absolute; font-size: 20px; pointer-events: none; opacity: 0; }
.cat-heart, .cat-spark { position: fixed; z-index: 10000; pointer-events: none; animation: catRise 1s ease-out forwards; }
.cat-heart { font-size: 22px; }
.cat-spark { font-size: 16px; }
@keyframes catRise { 0%{opacity:1; transform:translateY(0) scale(.6);} 100%{opacity:0; transform:translateY(-72px) scale(1.3);} }
/* 每日任务 / 金币 */
.cat-coins { color: #ffd24a; font-weight: 800; }
.cat-quests { margin-top: 8px; font-size: 11px; color: #c9b8ff; }
.cat-quest { display: flex; align-items: center; gap: 6px; margin: 4px 0; }
.cat-quest .q-box { width: 15px; height: 15px; border: 1px solid #7a4cff; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 10px; flex: 0 0 auto; }
.cat-quest.done .q-box { background: #5ee07a; color: #06240f; border-color: #5ee07a; }
.cat-quest.done { color: #9affc0; }
/* 小游戏浮层 */
.cat-mgame { position: fixed; z-index: 10002; right: 14px; bottom: 340px; width: 300px; max-width: 92vw; background: rgba(34,18,54,0.98); border: 1px solid #7a4cff; border-radius: 16px; padding: 12px; box-shadow: 0 8px 26px rgba(0,0,0,.55); display: none; }
.cat-mgame.show { display: block; }
.cat-mgame .mg-title { font-size: 13px; color: #ffd86b; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
.cat-mgame .mg-close { cursor: pointer; color: #c9b8ff; font-size: 16px; line-height: 1; }
.cat-feather, .cat-fishfall { cursor: pointer; user-select: none; position: relative; }
.cat-zzz { position: fixed; z-index: 10000; pointer-events: none; font-size: 18px; animation: catZzz 1.6s ease-out forwards; }
@keyframes catZzz { 0%{opacity:0; transform:translateY(0) scale(.6) rotate(-10deg);} 25%{opacity:1;} 100%{opacity:0; transform:translateY(-66px) scale(1.3) rotate(10deg);} }
.cat-coin-fly { position: fixed; z-index: 10002; pointer-events: none; font-size: 20px; animation: catCoinFly 1s ease-out forwards; }
@keyframes catCoinFly { 0%{opacity:1; transform:translateY(0) scale(1);} 100%{opacity:0; transform:translateY(-54px) scale(1.5);} }

.fp-note { font-size: 12px; color: #ffb3b3; text-align: center; margin-top: 12px; line-height: 1.6; }

/* 心愿单（理性储蓄） */
.fp-wish-goal { font-size: 13px; color: #ffe9b0; margin-top: 6px; }
.fp-wish-bar { height: 14px; border-radius: 7px; background: rgba(255,255,255,0.1); overflow: hidden; margin-top: 8px; }
.fp-wish-bar > i { display: block; height: 100%; width: 0; background: linear-gradient(90deg, #ffd24a, #ff7a18); transition: width .8s cubic-bezier(.2,.8,.2,1); }
.fp-wish-stat { font-size: 12px; color: #c9b8ff; margin-top: 6px; line-height: 1.5; }

/* 彩友圈（本地模拟） */
.fp-friends { max-height: 180px; overflow-y: auto; margin-top: 8px; }
.fp-post { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 8px 10px; margin-bottom: 8px; }
.fp-post .who { font-size: 12px; color: #ffd86b; font-weight: 700; }
.fp-post .msg { font-size: 12px; color: #e3dfff; line-height: 1.5; margin-top: 3px; }
.fp-post.me .who { color: #5ee0ff; }
.fp-note2 { font-size: 11px; color: #8f9bd6; text-align: center; margin-top: 6px; line-height: 1.5; }

/* 远程连接指示 */
.fp-remote { font-size: 11px; color: #7ee0a0; text-align: center; margin-top: 6px; }
"""


# ---------------------------------------------------------------------------
# 0. 招财猫萌宠（漂浮）
# ---------------------------------------------------------------------------
def generate_fortune_cat_html():
    return (
        '<div class="cat-widget" id="fpCat">'
        '  <div class="cat-bubble" id="catBubble">\u4E3B\u4EBA~\u6211\u662F\u62DB\u8D22\u732B\uff0c\u70B9\u6211\u783B\u783B\u3001\u5582\u5582\u6211\u3001\u6362\u88C5\u90FD\u884C\uFF0C\u8D8A\u73A9\u8D8A\u4EB2\u5BC6\u54DF\U0001F49E</div>'
        '  <div class="cat-stage">'
        '    <div class="cat-avatar" id="catAvatar" title="\u70B9\u6211\u783B\u783B / \u5582\u5582\u6211 / \u6362\u88C5">'
        '      <svg viewBox="0 0 160 170" xmlns="http://www.w3.org/2000/svg" aria-label="\u62DB\u8D22\u732B">'
        '        <defs>'
        '          <radialGradient id="catBody" cx="40%" cy="32%" r="75%">'
        '            <stop offset="0%" stop-color="#ffffff"/><stop offset="100%" stop-color="#e9ecf5"/>'
        '          </radialGradient>'
        '          <linearGradient id="catCoin" x1="0" y1="0" x2="0" y2="1">'
        '            <stop offset="0%" stop-color="#ffe07a"/><stop offset="100%" stop-color="#f5a623"/>'
        '          </linearGradient>'
        '        </defs>'
        '        <text id="catMoodEmoji" x="80" y="6" font-size="22" text-anchor="middle">\U0001F638</text>'
        '        <ellipse cx="80" cy="132" rx="46" ry="34" fill="url(#catBody)" stroke="#d7dbe8" stroke-width="1.5"/>'
        '        <circle cx="80" cy="74" r="43" fill="url(#catBody)" stroke="#d7dbe8" stroke-width="1.5"/>'
        '        <path d="M44 44 L40 12 L72 40 Z" fill="url(#catBody)" stroke="#d7dbe8" stroke-width="1.5"/>'
        '        <path d="M116 44 L120 12 L88 40 Z" fill="url(#catBody)" stroke="#d7dbe8" stroke-width="1.5"/>'
        '        <path d="M50 38 L47 22 L63 36 Z" fill="#ffc2cf"/>'
        '        <path d="M110 38 L113 22 L97 36 Z" fill="#ffc2cf"/>'
        '        <g class="cat-eye" transform="translate(64,72)">'
        '          <circle r="8" fill="#2b2440"/>'
        '          <circle id="catPupilL" class="cat-eye-pupil" r="4.6" fill="#000"/>'
        '          <circle cx="2.4" cy="-2.4" r="1.8" fill="#fff"/>'
        '        </g>'
        '        <g class="cat-eye" transform="translate(96,72)">'
        '          <circle r="8" fill="#2b2440"/>'
        '          <circle id="catPupilR" class="cat-eye-pupil" r="4.6" fill="#000"/>'
        '          <circle cx="2.4" cy="-2.4" r="1.8" fill="#fff"/>'
        '        </g>'
        '        <ellipse cx="57" cy="86" rx="7" ry="4.5" fill="#ffb3c1" opacity=".75"/>'
        '        <ellipse cx="103" cy="86" rx="7" ry="4.5" fill="#ffb3c1" opacity=".75"/>'
        '        <path d="M80 80 l-4 4 h8 z" fill="#ff8aa0"/>'
        '        <path id="catMouth" d="M80 84 q-7 7 -13 2 M80 84 q7 7 13 2" stroke="#caa" stroke-width="2" fill="none" stroke-linecap="round"/>'
        '        <g stroke="#cfd4e6" stroke-width="1.4" stroke-linecap="round">'
        '          <line x1="48" y1="80" x2="30" y2="76"/><line x1="48" y1="86" x2="30" y2="88"/>'
        '          <line x1="112" y1="80" x2="130" y2="76"/><line x1="112" y1="86" x2="130" y2="88"/>'
        '        </g>'
        '        <path d="M40 104 Q80 124 120 104 L120 116 Q80 136 40 116 Z" fill="#ff5a5a"/>'
        '        <circle cx="80" cy="110" r="6" fill="#ffd24a" stroke="#e0962a" stroke-width="1.2"/>'
        '        <ellipse cx="36" cy="118" rx="13" ry="10" fill="url(#catBody)" stroke="#d7dbe8" stroke-width="1.4"/>'
        '        <ellipse cx="34" cy="116" rx="5" ry="4" fill="#ffd1dc"/>'
        '        <g>'
        '          <circle cx="120" cy="120" r="17" fill="url(#catCoin)" stroke="#e0962a" stroke-width="1.6"/>'
        '          <text x="120" y="127" font-size="20" font-weight="900" fill="#a85b00" text-anchor="middle">\u5E8A</text>'
        '        </g>'
        '        <ellipse class="cat-tail" cx="124" cy="150" rx="20" ry="9" fill="url(#catBody)" stroke="#d7dbe8" stroke-width="1.4" transform="rotate(20 124 150)"/>'
        '        <g class="cat-costume" id="catCostume"></g>'
        '      </svg>'
        '    </div>'
        '    <div class="cat-stats" id="catStats"></div>'
        '  </div>'
        '  <div class="cat-btns">'
        '    <button class="fp-btn sec cat-mini" onclick="catFeed()">\U0001F37C \u5582\u6211</button>'
        '    <button class="fp-btn sec cat-mini" onclick="catPlay()">\U0001F3A3 \u9017\u732B\u68D2</button>'
        '    <button class="fp-btn sec cat-mini" onclick="catCatch()">\U0001F41F \u63A5\u5C0F\u9C7C</button>'
        '    <button class="fp-btn sec cat-mini" onclick="catCostumeCycle()">\U0001F451 \u6362\u88C5</button>'
        '    <button class="fp-btn sec cat-mini" onclick="catSleepToggle()">\U0001F4A4 \u7761\u89C9</button>'
        '    <button class="fp-btn sec cat-mini" onclick="catTickle()">\U0001F63B \u67C9\u75AE</button>'
        '    <button class="fp-btn sec cat-mini" onclick="catCheckin()">\U0001F525 \u7B7E\u5230</button>'
        '    <button class="fp-btn sec cat-mini" onclick="catTogglePanel()">\u2699 \u66F4\u591A</button>'
        '  </div>'
        '  <div class="cat-panel" id="catPanel">'
        '    <input class="fp-input" id="catName" placeholder="\u7ED9\u62DB\u8D22\u732B\u8D77\u4E2A\u540D\u5B57" maxlength="8" />'
        '    <button class="fp-btn" onclick="catNameOk()">\u2713 \u547D\u540D</button>'
        '    <div class="fp-remote" id="catRemote"></div>'
        '  </div>'
        '  <div class="cat-mgame" id="catMgame">'
        '    <div class="mg-title"><span id="mgTitle">\u5C0F\u6E38\u620F</span><span class="mg-close" onclick="catMgClose()">\u2715</span></div>'
        '    <div id="mgBody"></div>'
        '  </div>'
        '</div>'
    )


# ---------------------------------------------------------------------------
# A. 生日 / 纪念日选号器
# ---------------------------------------------------------------------------
def generate_birthday_html():
    return (
        '<div class="fp-card">'
        '  <h3>\U0001F388 A \u00B7 \u751F\u65E5/\u7EAA\u5FF5\u65E5\u9009\u53F7\u5668</h3>'
        '  <p class="tip">\u9009\u4E2A\u5BF9\u4F60\u6709\u610F\u4E49\u7684\u65E5\u5B50\uFF0C\u751F\u6210\u4E00\u7EC4"\u6709\u6545\u4E8B"\u7684\u53F7\u7801\uFF08\u7EAF\u5A31\u4E50\u53C2\u8003\uFF0C\u4E0E\u5F00\u5956\u65E0\u5173\uFF09\u3002</p>'
        '  <div class="fp-row">'
        '    <input type="date" class="fp-input" id="fpBday" />'
        '    <button class="fp-btn" onclick="fpBday()">\u2728 \u751F\u6210\u6211\u7684\u53F7\u7801</button>'
        '  </div>'
        '  <div class="fp-out" id="fpBdayOut"></div>'
        '</div>'
    )


# ---------------------------------------------------------------------------
# B. 公益贡献可视化
# ---------------------------------------------------------------------------
def generate_charity_html():
    return (
        '<div class="fp-card">'
        '  <h3>\U0001F331 B \u00B7 \u516C\u76CA\u8D21\u732E\u53EF\u89C6\u5316</h3>'
        '  <p class="tip">\u6BCF\u6CE8\u53CC\u8272\u7403\u6709\u7EA6 0.72 \u5143\uFF0836%\uFF09\u8FDB\u5165\u516C\u76CA\u91D1\uFF0C\u7528\u4E8E\u52A9\u5B66\u3001\u517B\u8001\u3001\u6324\u707E\u3002</p>'
        '  <div class="fp-tree" id="fpTree">\U0001F331</div>'
        '  <div class="fp-charity-num" id="fpCharityNum">\u00A50.00</div>'
        '  <div class="fp-charity-sub" id="fpCharitySub">\u5582\u62DB\u8D22\u55B5\u8D8A\u591A\uFF0C\u516C\u76CA\u6811\u8D8A\u957F~</div>'
        '  <div class="fp-bar"><i id="fpCharityBar"></i></div>'
        '</div>'
    )


# ---------------------------------------------------------------------------
# C. 理性购彩成就徽章
# ---------------------------------------------------------------------------
def generate_badges_html():
    return (
        '<div class="fp-card">'
        '  <h3>\U0001F3C5 C \u00B7 \u7406\u6027\u8D2D\u5F69\u6210\u5C31\u5FBD\u7AE0</h3>'
        '  <p class="tip">\u6E38\u620F\u5316\u53EA\u5956\u52B1"\u8D23\u4EFB\u4EFB"\u7684\u884C\u4E3A\u3002\u70B9\u4EAE\u5168\u90E8\u5FBD\u7AE0\uFF0C\u4F60\u5C31\u662F\u5408\u683C\u5F69\u6C11\uFF01</p>'
        '  <div class="fp-badges" id="fpBadges"></div>'
        '  <div class="fp-row">'
        '    <button class="fp-btn sec" onclick="fpCheckin()">\U0001F4C5 \u4ECA\u65E5\u7406\u6027\u6253\u5361</button>'
        '    <button class="fp-btn sec" onclick="fpPledge(\'spare\')">\U0001F4B0 \u6211\u53EA\u7528\u95F2\u94B1</button>'
        '    <button class="fp-btn sec" onclick="fpPledge(\'noguru\')">\U0001F6D0 \u4E0D\u4FE1\u5927\u5E08\u5305\u4E2D</button>'
        '    <button class="fp-btn sec" onclick="fpPledge(\'know\')">\U0001F4DA \u5DF2\u8BFB\u9632\u5272\u8292\u83CA\u76FE</button>'
        '  </div>'
        '</div>'
    )


# ---------------------------------------------------------------------------
# D. 幸运卡片一键分享
# ---------------------------------------------------------------------------
def generate_lucky_card_html():
    return (
        '<div class="fp-card">'
        '  <h3>\u2728 D \u00B7 \u5E78\u8FD0\u5361\u7247\u4E00\u952E\u5206\u4EAB</h3>'
        '  <p class="tip">\u751F\u6210\u4E13\u5C5E\u597D\u8FD0\u5361\uFF0C\u4E0B\u8F7D\u6216\u5206\u4EAB\u7ED9\u670B\u53CB\uFF08\u975E\u771F\u5B9E\u8DDF\u5355\u3001\u4E0D\u6D89\u53CA\u8D44\u91D1\uFF09\u3002</p>'
        '  <div class="fp-row">'
        '    <button class="fp-btn" onclick="fpMakeCard()">\U0001F300 \u751F\u6210\u597D\u8FD0\u5361</button>'
        '    <button class="fp-btn sec" onclick="fpDownloadCard()">\u2B07 \u4E0B\u8F7D PNG</button>'
        '    <button class="fp-btn sec" onclick="fpShareCard()">\u2728 \u5206\u4EAB</button>'
        '  </div>'
    '  <canvas id="fpCardCv" width="360" height="520" style="display:none;margin-top:10px;border-radius:12px;max-width:100%;"></canvas>'
    '</div>'
)


# ---------------------------------------------------------------------------
# E. 心愿单（理性储蓄挂钩）
# ---------------------------------------------------------------------------
def generate_wishlist_html():
    return (
        '<div class="fp-card">'
        '  <h3>\U0001F3C6 E \u00B7 \u5FC3\u613F\u5355\uFF08\u7406\u6027\u50A8\u84C4\uFF09</h3>'
        '  <p class="tip">\u8BBE\u4E2A\u5FC3\u613F\uFF0C\u628A\u7701\u4E0B\u7684\u4E70\u5F69\u94B1\u6162\u6162\u50A8\u8D77\u6765\u3002\u7406\u6027\u50A8\u84C4\uFF0C\u8BA9\u5FC3\u613F\u66F4\u5FEB\u6210\u771F\uFF08\u4E0E\u5F69\u7968\u65E0\u5173\uFF0C\u4E0D\u662F\u6295\u8D44\uFF09\u3002</p>'
        '  <div class="fp-row">'
        '    <input class="fp-input" id="fpWishName" placeholder="\u5FC3\u613F\u540D\u5B57\uFF08\u5982\uFF1A\u65B0\u8033\u673A\uFF09" maxlength="12" />'
        '    <input class="fp-input" id="fpWishTarget" type="number" placeholder="\u76EE\u6807\u91D1\u989D\uFF08\u5143\uFF09" style="width:110px;" />'
        '    <button class="fp-btn" onclick="fpWishSet()">\u2713 \u8BBE\u5B9A</button>'
        '  </div>'
        '  <div class="fp-wish-goal" id="fpWishGoal"></div>'
        '  <div class="fp-wish-bar"><i id="fpWishBar"></i></div>'
        '  <div class="fp-row" style="margin-top:8px;">'
        '    <button class="fp-btn sec cat-mini" onclick="fpWishAdd(10)">+ \u00A510</button>'
        '    <button class="fp-btn sec cat-mini" onclick="fpWishAdd(50)">+ \u00A550</button>'
        '    <button class="fp-btn sec cat-mini" onclick="fpWishSaveToday()">\u4ECA\u5929\u7701\u4E0B\u4E00\u6CE8\uFF08+\u00A52\uFF09</button>'
        '  </div>'
        '  <div class="fp-wish-stat" id="fpWishStat"></div>'
        '</div>'
    )


# ---------------------------------------------------------------------------
# F. 彩友社交（本地模拟彩友圈）
# ---------------------------------------------------------------------------
def generate_friend_circle_html():
    return (
        '<div class="fp-card">'
        '  <h3>\U0001F3AD F \u00B7 \u5F69\u53CB\u5708\uFF08\u672C\u5730\u6A21\u62DF\uFF09</h3>'
        '  <p class="tip">\u865A\u6784\u5F69\u53CB\uFF0C\u7EAF\u731C\u4E50\u3002\u53D1\u5E03\u4F60\u7684\u5FC3\u60C5/\u597D\u8FD0\u5361\u5230\u5708\u5B50\uFF0C\u4E0D\u8054\u7F51\u3001\u975E\u771F\u5B9E\u793E\u4EA4\u3002</p>'
        '  <div class="fp-friends" id="fpFriends"></div>'
        '  <div class="fp-row" style="margin-top:8px;">'
        '    <input class="fp-input" id="fpFriendMsg" placeholder="\u8BF4\u70B9\u4EC0\u4E48\uFF08\u5982\uFF1A\u4ECA\u5929\u53EA\u4E70\u4E86\u4E00\u6CE8~\uFF09" maxlength="60" style="flex:1;" />'
        '    <button class="fp-btn" onclick="fpFriendPost()">\u53D1\u5E03</button>'
        '  </div>'
        '  <div class="fp-note2">\u26A0\uFE0F \u5F69\u53CB\u5747\u4E3A\u865A\u6784\u89D2\u8272\uFF0C\u4EC5\u4F9B\u73A9\u7C7B\uFF1B\u4E0D\u4EE3\u8868\u771F\u5B9E\u4EBA\u58F0\u3001\u4E0D\u6D89\u8D44\u91D1\u3002</div>'
        '</div>'
    )


# ---------------------------------------------------------------------------
# 汇总入口（注入报告）
# ---------------------------------------------------------------------------
def generate_fun_pack_section(period=None, ledger=None):
    p = str(period) if period else ""
    real = {"zhu": 0, "spend": 0, "charity": 0, "wins": 0, "periods": 0}
    if ledger:
        real = {
            "zhu": int(ledger.get("total_zhu", 0) or 0),
            "spend": float(ledger.get("total_spend", 0) or 0),
            "charity": float(ledger.get("charity", 0) or 0),
            "wins": float(ledger.get("total_wins", 0) or 0),
            "periods": int(ledger.get("periods", 0) or 0),
        }
    html = []
    html.append('<div class="fp-section">')
    html.append('<div class="section-title">\U0001F431 \u62DB\u8D22\u732B\u840C\u5BA0 \u00B7 \u5A31\u4E50\u4E92\u52A8\u4E13\u533A</div>')
    html.append(generate_fortune_cat_html())
    html.append('<div class="fp-grid">')
    if _render_ledger:
        html.append(_render_ledger())
    html.append(generate_birthday_html())
    html.append(generate_charity_html())
    html.append(generate_badges_html())
    html.append(generate_lucky_card_html())
    html.append(generate_wishlist_html())
    html.append(generate_friend_circle_html())
    html.append('</div>')
    html.append('<div class="fp-note">'
                '\u26A0\uFE0F \u4EE5\u4E0A\u5747\u4E3A\u7EAF\u5A31\u4E50\u529F\u80FD\uFF0C\u4E0E\u771F\u5B9E\u5F00\u5956\u65E0\u5173\uFF1B\u865A\u62DF\u5956\u52B1\u4E0D\u53EF\u514F\u6362\u73B0\u91D1\uFF1B'
                '\u6A21\u62DF\u53F7\u7801\u2260\u4E2D\u5956\u53F7\u7801\u3002\u8BF7\u5A31\u4E50\u91CF\u529B\uFF0C\u7EDD\u4E0D\u53EF\u5F53\u4F5C"\u6709\u6536\u76CA"\u7684\u4F9D\u636E\u3002'
                '\uFF08\u672C\u671F\uFF1A' + p + '\uFF09</div>')
    html.append('</div>')
    import json as _json
    fp_real_json = _json.dumps(real, ensure_ascii=False)
    js = FUN_PACK_JS.replace("/*FP_REAL_PLACEHOLDER*/", fp_real_json)
    html.append(js)
    return "".join(html)


# ---------------------------------------------------------------------------
# JS（普通字符串，含 { } 不被二次解析；ES5 兼容、零联网）
# ---------------------------------------------------------------------------
try:
    from ssq_ledger import render_ledger_html as _render_ledger
except Exception:
    _render_ledger = None


FUN_PACK_JS = """
<script>
(function(){
  "use strict";
  var FP_REAL = /*FP_REAL_PLACEHOLDER*/;
  var FP_API = (location.protocol === "http:" && (location.hostname === "localhost" || location.hostname === "127.0.0.1")) ? (location.origin + "/") : "";
  var KEY = "ssq_felicity_cat_v1";
  function httpGet(u){ try { var x = new XMLHttpRequest(); x.open("GET", u, false); x.send(); if(x.status === 200) return x.responseText; } catch(e){} return null; }
  function httpPost(u, obj){ try { var x = new XMLHttpRequest(); x.open("POST", u, true); x.setRequestHeader("Content-Type","application/json"); x.send(JSON.stringify(obj)); } catch(e){} }
  function load(){
    if(FP_API){
      var r = httpGet(FP_API + "api/state");
      if(r){ try { return JSON.parse(r); } catch(e){} }
    }
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch(e){ return {}; }
  }
  function save(s){
    if(FP_API) httpPost(FP_API + "api/state", s);
    try { localStorage.setItem(KEY, JSON.stringify(s)); } catch(e){}
  }
  var S = load();
  if(!S.name) S.name = "\u62DB\u8D22\u5566";
  if(typeof S.feed !== "number") S.feed = 0;
  if(typeof S.intimacy !== "number") S.intimacy = 0;
  if(typeof S.level !== "number") S.level = 1;
  if(!S.badges) S.badges = {};
  if(!S.checkins) S.checkins = [];
  if(!S.pledges) S.pledges = {};
  if(FP_REAL.zhu && (typeof S.feed !== "number" || S.feed < FP_REAL.zhu)) S.feed = FP_REAL.zhu;
  if(!S.wish) S.wish = {name:"", target:0, saved:0};
  if(!S.friends) S.friends = [];
  if(typeof S.fish !== "number") S.fish = 0;
  if(!S.level) S.level = levelOf(S.feed);
  save(S);

  var TALKS = ["\u4E3B\u4EBA\u4ECA\u5929\u4E5F\u597D\u53EF\u7231~","\u5438\u6E9F~\u8D22\u6C14+1","\u55B5\u545A\uFF0C\u966A\u4F60\u5230\u5929\u8352\u5730\u8001","\u4ECA\u665A\u6708\u4EAE\u50CF\u9C7C\u5E72","\u4E3B\u4EBA\u6700\u68D2\u5566\uFF01","\u547C\u9C81\u547C\u9C81~"];
  function rnd(a){ return a[Math.floor(Math.random()*a.length)]; }

  function levelOf(feed){ return 1 + Math.floor(feed / 5); }

  /* ===== 招财猫 · 互动升级版（情绪/需求/音效/小游戏/每日任务） ===== */
  function todayStr(){ try { return new Date().toISOString().slice(0,10); } catch(e){ return ""; } }
  // 升级版状态初始化
  if(typeof S.hunger !== "number") S.hunger = 80;
  if(typeof S.energy !== "number") S.energy = 80;
  if(typeof S.mood !== "number") S.mood = 60;
  if(typeof S.coins !== "number") S.coins = 0;
  if(typeof S.costume !== "number") S.costume = 0;
  if(typeof S.sleeping !== "boolean") S.sleeping = false;
  if(!S.q || S.q.date !== todayStr()) S.q = {feed:0, play:0, ck:false, date: todayStr()};
  var HATS = ["", "\U0001F451", "\U0001F380", "\U0001F98E", "\U0001F36C", "\U0001F34C"];
  save(S);

  /* --- Web Audio 合成音效（零素材、零联网） --- */
  var AC = null;
  function actx(){ if(!AC){ try { AC = new (window.AudioContext || window.webkitAudioContext)(); } catch(e){} } return AC; }
  function tone(freq, dur, type, vol){ var c = actx(); if(!c) return; var o = c.createOscillator(), g = c.createGain(); o.type = type || 'sine'; o.frequency.value = freq; g.gain.value = vol || 0.05; o.connect(g); g.connect(c.destination); var t = c.currentTime; o.start(t); g.gain.exponentialRampToValueAtTime(0.0001, t + (dur || 0.2)); o.stop(t + (dur || 0.2)); }
  function meow(){ var c = actx(); if(!c) return; var o = c.createOscillator(), g = c.createGain(); o.type = 'sawtooth'; var t = c.currentTime; o.frequency.setValueAtTime(680, t); o.frequency.exponentialRampToValueAtTime(1150, t + 0.12); o.frequency.exponentialRampToValueAtTime(560, t + 0.32); g.gain.setValueAtTime(0.06, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.34); o.connect(g); g.connect(c.destination); o.start(t); o.stop(t + 0.35); }
  function purr(){ for(var i=0;i<3;i++){ (function(k){ setTimeout(function(){ tone(120, 0.13, 'square', 0.035); }, k*130); })(i); } }
  function coinSnd(){ tone(988, 0.08, 'square', 0.05); setTimeout(function(){ tone(1319, 0.13, 'square', 0.05); }, 70); }

  function clamp(v, a, b){ return v < a ? a : (v > b ? b : v); }
  function moodFace(){
    if(S.sleeping) return "\U0001F4A4";
    if(S.hunger < 25) return "\U0001F63F";
    if(S.energy < 20) return "\U0001F634";
    if(S.mood < 30) return "\U0001F63E";
    if(S.mood >= 78 && S.hunger > 40 && S.energy > 40) return "\U0001F63B";
    return "\U0001F638";
  }
  function mouthFor(){
    if(S.sleeping) return "M76 88 h8";
    if(S.mood < 30) return "M74 89 l12 0";
    if(S.hunger < 25) return "M80 88 q-7 -6 -13 -1 M80 88 q7 -6 13 -1";
    return "M80 84 q-7 9 -13 3 M80 84 q7 9 13 3";
  }
  function needBar(cls, lab, v){
    return '<div class="cat-need '+cls+'"><span class="lab">'+lab+'</span><span class="bar"><i style="width:'+clamp(v,0,100)+'%"></i></span></div>';
  }
  function renderCat(){
    var lv = levelOf(S.feed);
    S.level = lv;
    var el = document.getElementById("catStats");
    if(el){
      var q = S.q || {};
      var quests =
        '<div class="cat-quests">\u4ECA\u65E5\u4EFB\u52A1\uff1a'
        + '<div class="cat-quest'+(q.feed>=3?' done':'')+'"><span class="q-box">'+(q.feed>=3?'\u2713':'')+'</span>\u5582\u6211 3 \u6B21 ('+Math.min(q.feed,3)+'/3)</div>'
        + '<div class="cat-quest'+(q.play>=1?' done':'')+'"><span class="q-box">'+(q.play>=1?'\u2713':'')+'</span>\u9017\u732B\u68D2 1 \u6B21 ('+Math.min(q.play,1)+'/1)</div>'
        + '<div class="cat-quest'+(q.ck?' done':'')+'"><span class="q-box">'+(q.ck?'\u2713':'')+'</span>\u7B7E\u5230 (\u8FDE'+(S.checkins?S.checkins.length:0)+'\u5929)</div>'
        + '</div>';
      el.innerHTML =
        '<div class="row"><b>'+S.name+'</b><span class="lv">Lv.'+lv+'</span></div>'
        + '<div class="cat-ring" id="catRing" style="--p:'+S.intimacy+'"><span>'+S.intimacy+'</span></div>'
        + needBar('hunger', '\u9971\u98DF', S.hunger)
        + needBar('energy', '\u7CBE\u529B', S.energy)
        + needBar('mood', '\u5FC3\u60C5', S.mood)
        + '<div class="row"><span>\U0001F4B0\u91D1\u5E01</span><b class="cat-coins">'+(S.coins||0)+'</b></div>'
        + '<div class="row"><span>\U0001F41F\u9C7C\u5E72</span><b>'+(S.fish||0)+'\u6761</b></div>'
        + quests;
    }
    // SVG 表情 / 嘴 / 换装 / 睡觉
    var me = document.getElementById("catMoodEmoji"); if(me) me.textContent = moodFace();
    var mo = document.getElementById("catMouth"); if(mo) mo.setAttribute("d", mouthFor());
    var av = document.getElementById("catAvatar"); if(av) av.classList.toggle("sleep", !!S.sleeping);
    var co = document.getElementById("catCostume"); if(co) co.innerHTML = HATS[S.costume] ? '<text x="80" y="20" font-size="30" text-anchor="middle">'+HATS[S.costume]+'</text>' : '';
  }

  // 眼睛跟随光标（"它在看我"）
  document.addEventListener("mousemove", function(e){
    var pl = document.getElementById("catPupilL"), pr = document.getElementById("catPupilR");
    var av = document.getElementById("catAvatar");
    if(!pl || !pr || !av) return;
    var r = av.getBoundingClientRect();
    var cx = r.left + r.width/2, cy = r.top + r.height*0.46;
    var dx = clamp((e.clientX - cx) * 0.018, -3.2, 3.2);
    var dy = clamp((e.clientY - cy) * 0.018, -2.6, 2.6);
    pl.setAttribute("transform", "translate("+dx+","+dy+")");
    pr.setAttribute("transform", "translate("+dx+","+dy+")");
  });

  // 需求随时间衰减（跨报告持久）
  if(S._tick !== todayStr()){
    S._tick = todayStr();
  }
  setInterval(function(){
    if(!S.sleeping){
      S.hunger = clamp(S.hunger - 1, 0, 100);
      S.energy = clamp(S.energy - 1, 0, 100);
    } else {
      S.energy = clamp(S.energy + 2, 0, 100);
      S.hunger = clamp(S.hunger - 0.5, 0, 100);
      if(S.energy >= 95){ S.sleeping = false; }
    }
    S.mood = clamp(S.mood - (S.hunger<25||S.energy<20 ? 1.5 : 0.4), 0, 100);
    save(S); renderCat();
  }, 30000);

  function flyCoin(){
    var p = catTop();
    var d = document.createElement("div"); d.className = "cat-coin-fly"; d.textContent = "\U0001F4B0";
    d.style.left = p.x + "px"; d.style.top = p.y + "px";
    document.body.appendChild(d);
    setTimeout(function(){ if(d.parentNode) d.parentNode.removeChild(d); }, 1000);
  }
  function zzz(){
    var av = document.getElementById("catAvatar"); if(!av) return;
    var r = av.getBoundingClientRect();
    for(var i=0;i<3;i++){ (function(k){
      setTimeout(function(){
        var d = document.createElement("div"); d.className = "cat-zzz"; d.textContent = "\U0001F4AB";
        d.style.left = (r.left + r.width*0.6 + k*10) + "px"; d.style.top = (r.top + k*6) + "px";
        document.body.appendChild(d);
        setTimeout(function(){ if(d.parentNode) d.parentNode.removeChild(d); }, 1600);
      }, k*500);
    })(i); }
  }

  window.catTogglePanel = function(){ var p = document.getElementById("catPanel"); if(p) p.classList.toggle("show"); };
  window.catNameOk = function(){
    var i = document.getElementById("catName"); if(!i) return;
    var n = (i.value || "").trim();
    if(!n){ alert("\u5148\u7ED9\u62DB\u8D22\u5566\u60F3\u4E2A\u540D\u5B57\u5427~"); return; }
    S.name = n; save(S); renderCat();
    catSay("\u4EE5\u540E\u8BF7\u53EB\u6211 "+n+" \uFF0C\u4E3B\u4EBA~");
  };
  window.catFeed = function(){
    S.hunger = clamp(S.hunger + 30, 0, 100);
    S.mood = clamp(S.mood + 4, 0, 100);
    S.intimacy = clamp(S.intimacy + 4, 0, 100);
    if(S.q.feed < 99) S.q.feed += 1;
    save(S); renderCat(); renderCharity(); renderBadges();
    purr();
    catSay(rnd(["\U0001F618 \u4E3B\u4EBA\u6700\u597D\u4E86~\u2764\uFE0F","\U0001F98A \u8D22\u6C14\u5438\u5438\u5438~","\U0001F63B \u55B5\uFF01\u53C8\u5582\u6211\u5566"]));
    var p = catTop(); catBurst(p.x, p.y);
    if(S.q.feed === 3) rewardQuest();
  };
  var av = document.getElementById("catAvatar");
  if(av){
    av.addEventListener("click", function(){
      this.classList.remove("wave"); void this.offsetWidth; this.classList.add("wave");
      S.intimacy = clamp(S.intimacy + 2, 0, 100);
      S.mood = clamp(S.mood + 1, 0, 100);
      save(S); renderCat();
      meow(); catSay(rnd(TALKS));
      var p = catTop(); catBurst(p.x, p.y);
    });
  }
  window.catFish = function(){
    S.fish = (S.fish||0) + 1;
    S.mood = clamp(S.mood + 1, 0, 100);
    save(S); renderCat();
    catSay("\u55B5~\u5C0F\u9C7C\u5E72\u771F\u9999\U0001F41F");
    var p = catTop(); catBurst(p.x, p.y);
  };
  window.catCheckin = function(){
    var today = todayStr();
    if(S.checkins.indexOf(today) < 0){
      S.checkins.push(today);
      S.q.ck = true;
      S.intimacy = clamp(S.intimacy + 8, 0, 100);
      save(S); renderCat(); renderBadges();
      catSay("\U0001F525 \u4ECA\u65E5\u7B7E\u5230\uff0c\u4EB2\u5BC6\u5EA6+\uFF01\u660E\u5929\u518D\u6765\u5582~");
      if(S.q.ck) rewardQuest();
    } else {
      catSay("\u4ECA\u5929\u7B7E\u8FC7\u5566~\u660E\u5929\u6765\u62FF\u8FDE\u7B7E\u5956\u52B1\U0001F60A");
    }
    var p = catTop(); catBurst(p.x, p.y);
  };
  function rewardQuest(){
    var all = (S.q.feed>=3 && S.q.play>=1 && S.q.ck);
    if(all && !S.q.rewarded){
      S.q.rewarded = true; S.coins = (S.coins||0) + 20;
      save(S); renderCat(); flyCoin(); coinSnd();
      catSay("\U0001F389 \u4ECA\u65E5\u4EFB\u52A1\u5168\u90E6\u5B8C\u6210\uFF01\u5956\u52B1 20 \u91D1\u5E01\U0001F4B0");
    }
  }

  /* --- 逗猫棒小游戏 --- */
  window.catPlay = function(){
    var mg = document.getElementById("catMgame"), bd = document.getElementById("mgBody"), tt = document.getElementById("mgTitle");
    if(!mg || !bd) return;
    tt.textContent = "\U0001F3A3 \u9017\u732B\u68D2\uff1a\u70B9\u7FBD\u6BDB\u8BA9\u62DB\u8D22\u732B\u6253\u51FB\U0001F4A4";
    mg.classList.add("show");
    bd.innerHTML = '<div id="mgPlay" style="position:relative;height:200px;background:radial-gradient(circle at 50% 40%,#3a1d55,#1a1030);border-radius:10px;overflow:hidden;"><div id="feather" class="cat-feather" style="position:absolute;left:40%;top:40%;font-size:40px;">\U0001FAB6</div><div style="position:absolute;bottom:6px;left:0;right:0;text-align:center;color:#c9b8ff;font-size:11px;">\u6253\u4E2D 5 \u6B21\u83B7\u5956\U0001F4B0</div></div>';
    var f = document.getElementById("feather"), box = document.getElementById("mgPlay");
    var hits = 0;
    function moveFeather(){ if(!f) return; var w = box.clientWidth - 50, h = box.clientHeight - 50; f.style.left = (Math.random()*w)+"px"; f.style.top = (Math.random()*h)+"px"; }
    moveFeather(); var iv = setInterval(moveFeather, 650);
    f.onclick = function(){
      hits++; meow(); S.mood = clamp(S.mood+6,0,100); S.coins = (S.coins||0)+2;
      if(S.q.play < 99) S.q.play += 1;
      save(S); renderCat(); flyCoin(); catSay("\U0001F63B \u54D2\u54D2\u54D2\U0001F4A4");
      if(hits >= 5){ clearInterval(iv); coinSnd(); catSay("\U0001F389 \u6253\u4E2D 5 \u6B21\uff0c\u5956\u52B1\u5165\u888B\U0001F4B0"); setTimeout(function(){ if(mg) mg.classList.remove("show"); }, 700); return; }
      moveFeather();
    };
  };

  /* --- 接小鱼小游戏 --- */
  window.catCatch = function(){
    var mg = document.getElementById("catMgame"), bd = document.getElementById("mgBody"), tt = document.getElementById("mgTitle");
    if(!mg || !bd) return;
    tt.textContent = "\U0001F41F \u63A5\u5C0F\u9C7C\uff1a\u70B9\u6389\u843D\u4E0B\u7684\u9C7C\U0001F4B0";
    mg.classList.add("show");
    bd.innerHTML = '<div id="mgCatch" style="position:relative;height:220px;background:linear-gradient(180deg,#0a2a4a,#102a4d);border-radius:10px;overflow:hidden;"><div style="position:absolute;bottom:6px;left:0;right:0;text-align:center;color:#bfe0ff;font-size:11px;">\u63A5\u4F4F 6 \u6761\u5C0F\u9C7C\U0001F4B0</div></div>';
    var box = document.getElementById("mgCatch"); var got = 0; var dropped = 0;
    function spawn(){
      if(!box || dropped >= 10) return;
      dropped++;
      var fish = document.createElement("div"); fish.className = "cat-fishfall"; fish.textContent = "\U0001F41F";
      fish.style.position = "absolute"; fish.style.left = (Math.random()*80+5)+"%"; fish.style.top = "0"; fish.style.fontSize = "30px";
      box.appendChild(fish);
      var y = 0; var iv = setInterval(function(){
        y += 6; fish.style.top = y + "px";
        if(y > box.clientHeight - 36){ clearInterval(iv); if(fish.parentNode) fish.parentNode.removeChild(fish); if(dropped>=10 && got<6) endGame(); }
      }, 40);
      fish.onclick = function(){ clearInterval(iv); if(fish.parentNode) fish.parentNode.removeChild(fish); got++; meow(); S.coins=(S.coins||0)+1; S.mood=clamp(S.mood+2,0,100); save(S); renderCat(); flyCoin(); if(got>=6){ coinSnd(); catSay("\U0001F389 \u63A5\u6EE1 6 \u6761\U0001F4B0\uFF01"); setTimeout(function(){ if(mg) mg.classList.remove("show"); }, 700);} };
    }
    function endGame(){ if(mg) mg.classList.remove("show"); catSay("\U0001F4A6 \u4ECA\u5929\u5C0F\u9C7C\u8DF3\u5FEB\u4E86\uff0c\u660E\u5929\u518D\u6765\U0001F41F"); }
    var sp = setInterval(spawn, 700);
    setTimeout(function(){ clearInterval(sp); }, 7500);
  };
  window.catMgClose = function(){ var mg = document.getElementById("catMgame"); if(mg) mg.classList.remove("show"); };

  /* --- 换装 --- */
  window.catCostumeCycle = function(){
    S.costume = (S.costume + 1) % HATS.length;
    save(S); renderCat();
    catSay(HATS[S.costume] ? ("\U0001F451 \u6362\u4E0A"+HATS[S.costume]+"\u5566\uff0C\u597D\u770B\u5417\U0001F63B") : "\U0001F451 \u6362\u56DE\u7A7A\u624B\u51FA\u62F3\U0001F63A");
  };

  /* --- 睡觉 --- */
  window.catSleepToggle = function(){
    S.sleeping = !S.sleeping; save(S); renderCat();
    if(S.sleeping){ zzz(); catSay("\U0001F4A4 \u7761\u89C9\u5566~\u660E\u5929\u7CBE\u795E\u70B9\U0001F63A"); }
    else { meow(); catSay("\U0001F63B \u9192\u4E86\uff0c\u63A5\u7740\u73A9\U0001F4A4"); }
  };

  /* --- 挠痒 --- */
  window.catTickle = function(){
    S.mood = clamp(S.mood + 3, 0, 100);
    S.intimacy = clamp(S.intimacy + 2, 0, 100);
    save(S); renderCat();
    meow();
    catSay("\U0001F638 \u559C\u559C\u559C\u559C\u4E0D\u8981\u69A7\u6211\u8DDF\u5FC3\U0001F63B");
    var p = catTop(); catBurst(p.x, p.y);
  };

  function catSay(t){
    var b = document.getElementById("catBubble");
    if(b) b.innerHTML = t;
  }
  function catTop(){
    var w = document.getElementById("fpCat");
    if(!w) return {x: 200, y: 200};
    var r = w.getBoundingClientRect();
    return { x: r.left + r.width/2, y: r.top + 8 };
  }
  function catBurst(x, y){
    var emo = ["\u2764\uFE0F","\u2728","\U0001F496","\u2B50","\U0001F338","\U0001F31F"];
    for(var i=0;i<7;i++){
      var d = document.createElement("div");
      d.className = (i%2===0) ? "cat-heart" : "cat-spark";
      d.textContent = emo[Math.floor(Math.random()*emo.length)];
      d.style.left = (x + (Math.random()*70-35)) + "px";
      d.style.top = (y - Math.random()*24) + "px";
      document.body.appendChild(d);
      (function(node){ setTimeout(function(){ if(node.parentNode) node.parentNode.removeChild(node); }, 1000); })(d);
    }
  }

  /* ---------- A. \u751F\u65E5 / \u7EAA\u5FF5\u65E5\u9009\u53F7 ---------- */
  window.fpBday = function(){
    var v = document.getElementById("fpBday").value;
    var out = document.getElementById("fpBdayOut");
    if(!v){ out.innerHTML = "\U0001F447 \u5148\u9009\u4E2A\u751F\u65E5\u6216\u7EAA\u5FF5\u65E5~"; return; }
    var p = v.split("-"); var Y=+p[0], M=+p[1], D=+p[2];
    var reds = [];
    function push(n){ n = ((n-1)%33+33)%33+1; if(reds.indexOf(n)<0 && reds.length<6) reds.push(n); }
    push(Y%100 + 1); push(M + D); push(Y%100 + M); push(D*3 + 1); push(M*5 + 1); push((Y%10)*2 + (D%10) + 1);
    var i = 1; while(reds.length < 6){ push(reds[reds.length-1] + i); i++; }
    reds.sort(function(a,b){ return a-b; });
    var blue = ((M + D) % 16) + 1;
    var html = "\u4F60\u7684 <b>"+v+"</b> \u2192 \u7EA2\u7403 ";
    reds.forEach(function(n){ html += '<span class="fp-num r">'+("0"+n).slice(-2)+'</span>'; });
    html += ' 蓝球 <span class="fp-num b">'+("0"+blue).slice(-2)+'</span>';
    html += "<br><span style='font-size:11px;color:#c9b8ff;'>\u5E74/\u6708/\u65E5\u90FD\u85CF\u8FDB\u53F7\u7801\u91CC\u5566\uFF0C\u7EAF\u5A31\u4E50~</span>";
    out.innerHTML = html;
  };

  /* ---------- B. \u516C\u76CA\u8D21\u732E ---------- */
  function renderCharity(){
    var c = (FP_REAL.charity ? FP_REAL.charity : (S.feed * 0.72));
    var tree = c < 5 ? "\U0001F331" : c < 20 ? "\U0001F33F" : c < 50 ? "\U0001F333" : "\U0001F332";
    var t = document.getElementById("fpTree"); if(t) t.textContent = tree;
    var n = document.getElementById("fpCharityNum"); if(n) n.textContent = "\u00A5" + c.toFixed(2);
    var sub = document.getElementById("fpCharitySub");
    if(sub) sub.textContent = "\u4F60\u771F\u5B9E\u8D2D\u5F69 "+S.feed+" \u6CE8 \u2248 \u8D21\u732E\u516C\u76CA\u91D1 \u00A5" + c.toFixed(2) + "\uff08\u6BCF\u6CE8 0.72 \u5143\uff09";
    var bar = document.getElementById("fpCharityBar");
    if(bar) bar.style.width = Math.min(100, (c/50)*100) + "%";
  }

  /* ---------- C. \u6210\u5C31\u5FBD\u7AE0 ---------- */
  var BADGES = [
    {id:"know",    ico:"\U0001F4DA", nm:"\u7406\u6027\u65B0\u624B"},
    {id:"spare",   ico:"\U0001F4B0", nm:"\u95F2\u94B1\u539F\u5219"},
    {id:"noguru",  ico:"\U0001F4D0", nm:"\u4E0D\u4FE1\u5927\u5E08"},
    {id:"cat",     ico:"\U0001F431", nm:"\u94F2\u5C38\u5B98"},
    {id:"charity", ico:"\U0001F333", nm:"\u516C\u76CA\u8FBE\u4EBA"},
    {id:"streak",  ico:"\U0001F4C5", nm:"\u6253\u5361\u8FBE\u4EBA"}
  ];
  function renderBadges(){
    if(S.feed >= 10) S.badges.cat = true;
    if((FP_REAL.charity || 0) >= 10 || S.feed * 0.72 >= 10) S.badges.charity = true;
    if(S.checkins.length >= 3) S.badges.streak = true;
    save(S);
    var box = document.getElementById("fpBadges");
    if(!box) return;
    var html = "";
    BADGES.forEach(function(b){
      var on = S.badges[b.id] ? " on" : "";
      var cls = S.badges[b.id] ? "" : "\uFF08\u5F85\u89E3\u9501\uFF09";
      html += '<div class="fp-badge'+on+'"><div class="ico">'+b.ico+'</div><div class="nm">'+b.nm+cls+'</div></div>';
    });
    box.innerHTML = html;
  }
  window.fpPledge = function(k){
    S.pledges[k] = true;
    if(k==="spare"||k==="noguru"||k==="know") S.badges[k] = true;
    save(S); renderBadges();
    catSay("\u4E3B\u4EBA\u8BF4\u5230\u505A\u5230\uFF0C\u55B5\u2764\uFE0F");
  };
  window.fpCheckin = function(){
    var today = new Date().toISOString().slice(0,10);
    if(S.checkins.indexOf(today) < 0) S.checkins.push(today);
    save(S); renderBadges();
    catSay("\u8FDE\u7EED\u7406\u6027 "+S.checkins.length+" \u5929\uFF0C\u4E3B\u4EBA\u771F\u7A33\uFF01");
  };

  /* ---------- D. \u5E78\u8FD0\u5361\u7247 ---------- */
  var lastNums = null;
  window.fpMakeCard = function(){
    var reds = [], i = 1;
    while(reds.length < 6){ var n = Math.floor(Math.random()*33)+1; if(reds.indexOf(n)<0) reds.push(n); }
    reds.sort(function(a,b){return a-b;});
    var blue = Math.floor(Math.random()*16)+1;
    lastNums = {reds:reds, blue:blue};
    drawCard(reds, blue);
  };
  function drawCard(reds, blue){
    var cv = document.getElementById("fpCardCv"); if(!cv) return;
    cv.style.display = "block";
    var ctx = cv.getContext("2d");
    var g = ctx.createLinearGradient(0,0,360,520);
    g.addColorStop(0,"#3a1d55"); g.addColorStop(1,"#7a2a14");
    ctx.fillStyle = g; ctx.fillRect(0,0,360,520);
    ctx.fillStyle = "#ffd86b"; ctx.textAlign = "center";
    ctx.font = "bold 22px sans-serif";
    ctx.fillText("\u2728 \u6211\u7684\u53CC\u8272\u7403\u597D\u8FD0\u5361 \u2728", 180, 46);
    ctx.font = "14px sans-serif"; ctx.fillStyle = "#ffe9b0";
    ctx.fillText("\u62DB\u8D22\u5566 \u00B7 " + S.name, 180, 74);
    ctx.font = "bold 18px sans-serif";
    var x = 70, y = 150;
    for(var i=0;i<6;i++){
      ctx.beginPath(); ctx.arc(x + i*44, y, 17, 0, Math.PI*2);
      ctx.fillStyle = "#d10000"; ctx.fill();
      ctx.fillStyle = "#fff"; ctx.fillText(("0"+reds[i]).slice(-2), x + i*44, y+6);
    }
    ctx.beginPath(); ctx.arc(180, y+60, 17, 0, Math.PI*2);
    ctx.fillStyle = "#0048c8"; ctx.fill();
    ctx.fillStyle = "#fff"; ctx.fillText(("0"+blue).slice(-2), 180, y+66);
    ctx.font = "13px sans-serif"; ctx.fillStyle = "#c9b8ff";
    ctx.fillText("\u7EA2\u7403 6 \u00B7 \u84DD\u7403 1\uFF08\u7EAF\u5A31\u4E50\u00B7\u975E\u771F\u5B9E\u8DDF\u5355\uFF09", 180, y+110);
    ctx.font = "15px sans-serif"; ctx.fillStyle = "#ffe9b0";
    ctx.fillText("\u201C \u4ECA\u5929\u4E5F\u8981\u5F00\u5FC3\uFF0C\u8D22\u6C14\u81EA\u5DF1\u6765 ~ \u201D", 180, 380);
    ctx.font = "12px sans-serif"; ctx.fillStyle = "#9b8bff";
    ctx.fillText(new Date().toLocaleDateString(), 180, 470);
    ctx.fillText("\u7406\u6027\u8D2D\u5F69 \u00B7 \u91CF\u529B\u800C\u884C", 180, 492);
  }
  window.fpDownloadCard = function(){
    var cv = document.getElementById("fpCardCv"); if(!cv || cv.style.display==="none"){ fpMakeCard(); }
    var url = cv.toDataURL("image/png");
    var a = document.createElement("a");
    a.href = url; a.download = "\u53CC\u8272\u7403\u597D\u8FD0\u5361.png";
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
  };
  window.fpShareCard = function(){
    var cv = document.getElementById("fpCardCv"); if(!cv || cv.style.display==="none"){ fpMakeCard(); }
    cv.toBlob(function(blob){
      if(blob && navigator.share){
        navigator.share({ title:"\u6211\u7684\u53CC\u8272\u7403\u597D\u8FD0\u5361", files:[new File([blob], "card.png", {type:"image/png"})] }).catch(function(){});
      } else {
        fpDownloadCard();
      }
    });
  };

  /* ---------- E. 心愿单 ---------- */
  function renderWish(){
    var g = document.getElementById("fpWishGoal");
    var bar = document.getElementById("fpWishBar");
    var stat = document.getElementById("fpWishStat");
    if(!g) return;
    if(!S.wish.name){
      g.innerHTML = "\u8BBE\u4E2A\u5FC3\u613F\u5427~\uFF08\u4F8B\uFF1A\u65B0\u8033\u673A 800\uFF09";
      if(bar) bar.style.width = "0%";
      if(stat) stat.innerHTML = "";
      return;
    }
    var pct = S.wish.target > 0 ? Math.min(100, S.wish.saved / S.wish.target * 100) : 0;
    g.innerHTML = "\U0001F31F " + S.wish.name + " \u00B7 \u5DF2\u50A8 \u00A5" + S.wish.saved.toFixed(2) + " / \u00A5" + S.wish.target;
    if(bar) bar.style.width = pct + "%";
    var reflect = "";
    if(FP_REAL.spend > 0 && S.wish.target > 0){
      var n = (FP_REAL.spend / S.wish.target);
      reflect = "\u4F60\u5DF2\u82B1\u5728\u53CC\u8272\u7403 \u00A5" + FP_REAL.spend.toFixed(2) + "\uff0c\u7EA6\u53EF\u4E70 " + n.toFixed(1) + " \u4E2A\u300C" + S.wish.name + "\u300D\u3002\u7701\u4E0B\u4E00\u6CE8\uff0c\u5FC3\u613F\u66F4\u8FD1~";
    }
    if(stat) stat.innerHTML = (S.wish.saved >= S.wish.target && S.wish.target > 0)
      ? "\U0001F4B0 \u5FC3\u613F\u5DF2\u5B9E\u73B0\uFF01\u7EE7\u7EED\u4FDD\u6301\u7406\u6027\u54E6~"
      : reflect;
  }
  window.fpWishSet = function(){
    var n = (document.getElementById("fpWishName").value || "").trim();
    var t = parseFloat(document.getElementById("fpWishTarget").value);
    if(!n || !(t > 0)){ alert("\u8BF7\u586B\u5FC3\u613F\u540D\u5B57\u548C\u76EE\u6807\u91D1\u989D~"); return; }
    S.wish = {name:n, target:t, saved: S.wish.saved || 0};
    save(S); renderWish();
    catSay("\u5FC3\u613F\u300C" + n + "\u300D\u5DF2\u8BB0\u4E0B\uFF0C\u4E3B\u4EBA\u52A0\u6CB9\u50A8\u94B1~");
  };
  window.fpWishAdd = function(v){
    if(!S.wish.name){ alert("\u5148\u8BBE\u5B9A\u5FC3\u613F\u5427~"); return; }
    S.wish.saved = (S.wish.saved || 0) + v;
    save(S); renderWish();
    catSay("\u50A8\u4E86 \u00A5" + v + "\uFF0C\u79BB\u5FC3\u613F\u53C8\u8FD1\u4E00\u6B65~");
  };
  window.fpWishSaveToday = function(){
    if(!S.wish.name){ alert("\u5148\u8BBE\u5B9A\u5FC3\u613F\u5427~"); return; }
    S.wish.saved = (S.wish.saved || 0) + 2;
    save(S); renderWish();
    catSay("\u4ECA\u5929\u7701\u4E0B\u4E00\u6CE8\uff0c\u50A8\u4E0B \u00A52~ \u2764\uFE0F");
  };

  /* ---------- F. 彩友圈（本地模拟） ---------- */
  var FRIENDS_SEED = [
    {who:"\u7406\u6027\u8001\u738B", msg:"\u4ECA\u5929\u53EA\u4E70\u4E861\u6CE8\uFF0C\u5269\u4E0B\u7684\u94B1\u7ED9\u56DA\u5973\u4E70\u51B0\u68D8\u4E86\U0001F366 \u7406\u6027\u7B2C\u4E00\uFF01"},
    {who:"\u9526\u9CB8\u5C0F\u59B9", msg:"\u62DB\u8D22\u732B\u8BF4\u6211\u4EB2\u5BC6\u5EA6\u6EE1\u7EA7\u5566~\u4F46\u4E2D\u4E0D\u4E2D\u968F\u7F18\u54E6\U0001F431"},
    {who:"\u4F5B\u7CFB\u963F\u5F3A", msg:"\u8FDE\u7EED30\u5929\u7406\u6027\u6253\u5361\uFF0C\u5FBD\u7AE0\u96C6\u9F50\uFF0C\u6211\u624D\u662F\u8D62\u5BB6\U0001F60E"},
    {who:"\u5E78\u8FD0\u661F", msg:"\u5206\u4EAB\u4E00\u5F20\u597D\u8FD0\u5361\u7ED9\u670B\u53CB\uFF0C\u56FE\u4E2A\u5F00\u5FC3\u2728"}
  ];
  function renderFriends(){
    var box = document.getElementById("fpFriends");
    if(!box) return;
    var list = FRIENDS_SEED.concat((S.friends || []).map(function(m){ return {who:"\u6211 (\u4E3B\u4EBA)", msg:m, me:true}; }));
    var html = "";
    list.forEach(function(p){
      html += '<div class="fp-post' + (p.me ? " me" : "") + '"><div class="who">' + p.who + '</div><div class="msg">' + p.msg + '</div></div>';
    });
    box.innerHTML = html;
  }
  window.fpFriendPost = function(){
    var i = document.getElementById("fpFriendMsg");
    var m = (i.value || "").trim();
    if(!m){ alert("\u8BF4\u70B9\u4EC0\u4E48\u518D\u53D1\u5E03\u5440~"); return; }
    if(!S.friends) S.friends = [];
    S.friends.unshift(m);
    if(S.friends.length > 20) S.friends = S.friends.slice(0, 20);
    save(S); renderFriends();
    i.value = "";
    catSay("\u5DF2\u53D1\u5230\u5F69\u53CB\u5708\uFF0C\u4E3B\u4EBA\u6700\u68D2~");
  };

  /* ---------- \u521D\u59CB\u5316 ---------- */
  renderCat(); renderCharity(); renderBadges(); renderWish(); renderFriends();
  var rm = document.getElementById("catRemote"); if(rm) rm.textContent = FP_API ? "\u2705 \u5DF2\u8FDE\u672C\u5730\u670D\u52A1\uFF0C\u62DB\u8D22\u732B\u8DE8\u62A5\u544A\u4FDD\u5B58" : "\u2728 \u672C\u5730\u6A21\u5F0F\uFF08\u53CC\u51FB html \u7528\uFF0C\u72B6\u6001\u4EC5\u672C\u6587\u4EF6\uFF09";
  var _realC = (FP_REAL.charity ? FP_REAL.charity : (S.feed * 0.72));
  catSay("\u4E3B\u4EBA~ \u6211\u5DF2\u966A\u4F60\u4E70\u4E86 "+S.feed+" \u6CE8\uFF0C\u5438\u4E86 \u00A5"+_realC.toFixed(2)+" \u516C\u76CA\u91D1\U0001F431");
})();
/* 招财猫随页面滚动漂浮：滚动进度驱动大幅位移 + 持续呼吸式漂浮 */
(function(){
  var cat = document.getElementById('fpCat');
  if(!cat) return;
  if(cat.parentElement) document.body.appendChild(cat); /* 脱离嵌套容器，让 fixed 相对视口生效 */
  var lastY = window.scrollY || 0, cur = 0;
  function loop(){
    var y = window.scrollY || window.pageYOffset || 0;
    var docH = document.documentElement.scrollHeight || document.body.scrollHeight;
    var max = docH - window.innerHeight;
    var prog = max > 0 ? Math.min(1, Math.max(0, y / max)) : 0;
    var dy = y - lastY; lastY = y;
    var room = Math.max(120, window.innerHeight - 420);
    var drift = prog * Math.min(window.innerHeight * 0.55, room);
    var wob = Math.max(-34, Math.min(34, -dy * 1.4));
    var breathe = Math.sin(Date.now() / 850) * 9;
    var target = drift + wob + breathe;
    cur += (target - cur) * 0.14;
    var rot = Math.max(-10, Math.min(10, -dy * 0.06));
    cat.style.transform = 'translateY(' + cur.toFixed(2) + 'px) rotate(' + rot.toFixed(2) + 'deg)';
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
})();
</script>

"""
