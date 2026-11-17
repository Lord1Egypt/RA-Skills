"""技能标识、版本与平台公共库约束。"""

SKILL_SLUG = "publish-answer-baidu-know"
SKILL_VERSION = "1.1.0"
LOG_LOGGER_NAME = "openclaw.skill.publish_answer_baidu_know"
PLATFORM_KIT_MIN_VERSION = "1.0.17"

# 业务常量：百度知道回答自动发布
TARGET_PLATFORM = "baidu_zhidao"
LEASE_HOLDER = "publish-answer-baidu-know"
LEASE_TTL_SEC = "1800"

# 默认起始页：百度知道首页（仅用于浏览器冷启动后跳板，实际发布会在 run 时跳转到 --question-url）
DEFAULT_START_URL = "https://zhidao.baidu.com"

# 百度知道问题 URL 校验前缀（避免误传其他平台链接）
QUESTION_URL_PREFIXES = (
    "https://zhidao.baidu.com/question/",
    "http://zhidao.baidu.com/question/",
)

# 登录态检测
# 已验证（WebFetch + 爬虫资料）：百度知道未登录态会在右上角显示「登录」链接
# 登录后通常出现「个人中心」/ 用户名链接（href 含 /user/center 或 /usercenter）
# 注：具体 class/id 仍需登录态 F12 复核，当前为基于公开资料的候选集合
LOGGED_IN_SELECTORS = (
    "a[href*='/user/center']",
    "a[href*='/usercenter']",
    ".user-name",
    ".user-icon",
    ".header-link[href*='usercenter']",
)
LOGGED_OUT_SELECTOR = "a:has-text('登录')"

# 问题页 selector
# 已验证（多份爬虫资料 + WebFetch 真实页面）：
#   - 百度知道问题标题稳定 class 为 `ask-title`，标签为 <span>（非 h1）
#   - 老页面容器为 #wgt-ask > h1 > span.ask-title
#   - 作业帮类问题用 .qb-content（罕见，作为 fallback）
QUESTION_TITLE_SELECTOR = "span.ask-title, #wgt-ask h1 span.ask-title, .qb-content .ask-title"

# 回答编辑器入口：登录态下问题页出现的「我来答」按钮
# F12 实测演变：
#   2026-07-20 旧版：<span id="answer-bar" alog-alias="qb-answer-bar" class="iknow-icons exp-answerbtn-yh">我来答</span>
#   2026-07-22 新版：<a class="push-item-btn"><span class="smooth">我来答</span></a>
#                 或 <a class="answer-btn">我来答</a>
#                 或 <div class="answer-entry-1"> 我来答</div>
# 优先用 id（最稳定），fallback 到 class / 文案匹配（应对改版）
# 注意：a.push-item-btn 在页面底部推荐区也会出现，需配合上下文判断
ANSWER_EDITOR_OPEN_SELECTORS = (
    "#answer-bar",
    "span[alog-alias='qb-answer-bar']",
    "span.exp-answerbtn-yh",
    "span.iknow-icons.exp-answerbtn-yh",
    "a.push-item-btn:has-text('我来答')",
    "a.answer-btn",
    "a:has-text('我来答')",
    "span.smooth:has-text('我来答')",
)

# 回答编辑器：UEditor iframe 内的 contenteditable body
# 已 F12 实测确认（2026-07-20）：
#   编辑器实际是百度自家 UEditor，渲染为 iframe + 内部 <body contenteditable="true">
#   iframe 外层容器通常是 <div id="ueditor_replace">，iframe id 形如 ueditor_0 / ueditor_1
#   可编辑 body 结构：<body class="view" contenteditable="true" spellcheck="false">
#
# Playwright 操作策略（在 baidu_zhidao_rpa.py 中实现）：
#   1. 通过 page.frame_locator 进入 iframe
#   2. 在 iframe 内 locator('body[contenteditable="true"]')
#   3. 用 frame.click() 聚焦 + frame.type() 逐字输入
#
# 本常量保存「iframe 外层 selector」用于定位 iframe 元素本身
# （contenteditable body 在 iframe 内部，无法用 page.locator 直接选中）
ANSWER_EDITOR_IFRAME_SELECTORS = (
    "iframe#ueditor_0",
    "iframe[id^='ueditor_']",
    "#ueditor_replace iframe",
    "div.ueditor-style iframe",
)
# 编辑器 iframe 内 body 的 selector（进入 frame 后用）
ANSWER_EDITOR_BODY_SELECTOR = "body[contenteditable='true']"
# 兼容：若未来 UEditor 改回 textarea 模式，用以下 selector 兜底
ANSWER_EDITOR_TEXTAREA_SELECTORS = (
    "textarea[name='answer_content']",
    "textarea[name='content']",
    ".editor-area textarea",
)

# 发布按钮
# 已 F12 实测确认（2026-07-20）：
#   <a class="btn-32-green grid-r new-editor-deliver-btn">提交回答</a>
# 关键发现：
#   - 标签是 <a>（不是 <button>），class 含 new-editor-deliver-btn（稳定业务 class）
#   - 也有 btn-32-green 和 grid-r（样式类，可能随主题变化）
#   - 文案是「提交回答」
# 优先用 new-editor-deliver-btn，fallback 到文案匹配
ANSWER_PUBLISH_BUTTON_SELECTORS = (
    "a.new-editor-deliver-btn",
    ".new-editor-deliver-btn",
    "a:has-text('提交回答')",
    "a:has-text('发布回答')",
    "button:has-text('提交回答')",
)

# 发布结果信号
# 已 F12 实测确认（2026-07-20）：
#   成功 toast：<div class="tipLayer success-tip"><span class="icon"></span><div>提交成功</div></div>
# 关键发现：
#   - toast 容器 class 是 tipLayer，成功态加 success-tip，失败态预期为 error-tip / fail-tip
#   - 文案在内部 <div> 中
#   - 实测文案为「提交成功」（不是「回答成功」）
# toast 容器 selector（用于定位 toast 元素）
PUBLISH_TOAST_SELECTOR = ".tipLayer"
PUBLISH_SUCCESS_TOAST_SELECTOR = ".tipLayer.success-tip"
PUBLISH_FAILED_TOAST_SELECTOR = ".tipLayer.error-tip, .tipLayer.fail-tip"
# toast 文案匹配（也扫描页面正文，应对跳转型反馈）
PUBLISH_SUCCESS_MARKERS = (
    "提交成功",
    "回答成功",
    "您的回答已成功提交",
    "回答已提交",
    "感谢您的回答",
)
PUBLISH_PENDING_REVIEW_MARKERS = (
    "待审核",
    "审核中",
    "等待审核",
    "您的回答正在审核中",
    "回答审核通过后将显示",
)
PUBLISH_FAILED_MARKERS = (
    "回答失败",
    "提交失败",
    "回答被删除",
    "回答已被删除",
    "请勿重复回答",
    "您今天回答次数已达上限",
    "请先登录",
)

# 发布结果等待（toast / 跳转）最大时长（秒）
PUBLISH_WAIT_TIMEOUT_SEC = 30

# HITL 等待：登录、滑块、短信验证码
HUMAN_WAIT_TIMEOUT = 300
