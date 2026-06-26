# -*- coding: utf-8 -*-
"""
配置管理模块
集中管理所有路径和配置，消除硬编码
"""
import os
from typing import Dict, List, Tuple

# 用户主目录
USER_PROFILE = os.environ.get('USERPROFILE', os.path.expanduser('~'))

# 基础路径
OPENCLAW_DIR = os.path.join(USER_PROFILE, '.openclaw')
WORKSPACE_DIR = os.path.join(OPENCLAW_DIR, 'workspace')
SKILLS_DIR = os.path.join(WORKSPACE_DIR, 'skills')
OUTPUT_DIR = os.path.join(USER_PROFILE, 'openclaw_out')
CACHE_DIR = os.path.join(OPENCLAW_DIR, 'cache', 'skill_list')

# 确保目录存在
for directory in [OUTPUT_DIR, CACHE_DIR]:
    os.makedirs(directory, exist_ok=True)

# 分类排序
CATEGORY_ORDER: List[str] = [
    "妙想平台", "同花顺平台", "富途平台", "搜索工具",
    "金融分析工具", "系统工具", "开发工具", "GitHub集成",
    "消息与通信", "其他"
]

# 技能状态图标
STATUS_ICONS: Dict[str, str] = {
    'ready': '✅',
    'needsetup': '⚠️',
    'disabled': '❌',
    'error': '❌',
    'unknown': '❓'
}

# 分类规则（用于自动分类）
# 格式: (关键词列表, 大类, 子类)
CATEGORY_RULES: List[Tuple[List[str], str, str]] = [
    # ====== 妙想平台 ======
    (['eastmoney_fin_data', 'mx-data'], '妙想平台', '妙想-行情与财务数据'),
    (['eastmoney_fin_search', 'mx-search'], '妙想平台', '妙想-搜索与资讯'),
    (['mx-moni', 'eastmoney_stock_simulator'], '妙想平台', '妙想-交易与持仓'),
    (['mx-xuangu', 'mx-zixuan', 'mx_self_select', 'mx-skills'], '妙想平台', '妙想-选股与自选'),
    
    # ====== 同花顺平台 ======
    (['问财选'], '同花顺平台', '同花顺-选股与筛选'),
    (['数据查询', '行业数据查询', '行情数据查询', '指数数据查询', '宏观数据查询', '基金理财查询'], '同花顺平台', '同花顺-数据查询'),
    (['搜索', '公告', '新闻', '研报', '事件数据查询', '机构研究与评级查询', '投资者关系活动搜索'], '同花顺平台', '同花顺-搜索与资讯'),
    (['财务数据查询', '公司经营数据查询', '公司股东股本查询', '基本资料查询', '期货期权数据查询'], '同花顺平台', '同花顺-数据查询'),
    (['模拟炒股'], '同花顺平台', '同花顺-模拟交易'),
    
    # ====== 富途平台 ======
    (['futuapi'], '富途平台', '富途-行情API'),
    (['install-opend'], '富途平台', '富途-安装配置'),
    
    # ====== 搜索工具 ======
    (['multi-search-engine', 'desearch-web-search', 'tavily', 'find-skills', 'find-skills-skill'], '搜索工具', '网页搜索'),
    (['xurl', 'gifgrep'], '搜索工具', '网页搜索'),
    (['blogwatcher'], '搜索工具', '博客订阅'),
    
    # ====== 金融分析工具 ======
    (['stock-analysis', 'akshare-stock', '股票研究', '科技炒作与基本面', '高分红股挑选'], '金融分析工具', '股票研究与分析'),
    (['ADR', 'H股', 'A股', '套利'], '金融分析工具', '跨市场套利'),
    (['财报', '财务报表', '估值'], '金融分析工具', '财报与财务'),
    (['产业链', 'K线', '技术指标', '一目均衡'], '金融分析工具', '行业与产业链'),
    (['行业概览', '行业轮动'], '金融分析工具', '行业与产业链'),
    (['市场情绪', '宏观', '地缘', '期权'], '金融分析工具', '市场情绪与宏观'),
    (['资金流', '沪深港通'], '金融分析工具', '资金流向分析'),
    (['因子', '量化', '策略', '对冲', '资产配置', '业绩归因', '机器学习'], '金融分析工具', '量化与因子'),
    (['晨会', '首次覆盖', 'daily-digest'], '金融分析工具', '晨会纪要与研报'),
    (['风险', '压力测试', '金融监管'], '金融分析工具', '风险与策略'),
    (['polymarket', '预测市场'], '金融分析工具', '预测市场'),
    (['税务', 'tax', 'geneva'], '金融分析工具', '税务咨询'),
    (['social-media', '社交媒体'], '金融分析工具', '公告与新闻搜索'),
    
    # ====== 系统工具 ======
    (['ocr', 'pdf'], '系统工具', 'OCR与文档处理'),
    (['whisper', 'tts', '语音', 'audio', 'sag', 'sherpa'], '系统工具', '语音与音频'),
    (['browser', 'playwright', 'peekaboo'], '系统工具', '浏览器自动化'),
    (['memory', '记忆', 'wiki', 'memos'], '系统工具', '记忆与知识库'),
    (['hue', 'openhue', 'smart-home'], '系统工具', '智能家居控制'),
    (['sleep', 'eightctl'], '系统工具', '智能家居控制'),
    (['apple-notes', 'bear-notes', 'obsidian', 'notion'], '系统工具', '笔记'),
    (['apple-reminders', 'remind', 'things-mac'], '系统工具', '日历与提醒'),
    (['spotify', 'sonos', 'songsee'], '系统工具', '音乐播放'),
    (['video', 'frame', 'camsnap'], '系统工具', '视频处理'),
    (['weather'], '系统工具', '天气查询'),
    (['summarize', '表格', '数据清洗', 'nano-pdf', 'camsnap'], '系统工具', '文件编辑与数据清洗'),
    (['healthcheck', 'node-connect', 'taskflow', 'taskflow-inbox'], '系统工具', '定时任务'),
    (['1password', 'gog', 'goplaces', 'blucli', 'trello', 'wacli', 'tmux', 'ordercli', 'things-mac'], '系统工具', '效率工具'),
    
    # ====== 开发工具 ======
    (['coding-agent', 'skill-creator', 'skill-vetter', 'mcporter', 'oracle', 'clawhub'], '开发工具', '编码与开发'),
    (['self-improv', 'self-reflection', 'reflection', '自我', '反思', 'evolver', 'capability'], '开发工具', '自我优化与反思'),
    (['code-analyzer'], '开发工具', '代码分析'),
    (['planning', 'agent-team', 'orchestrat'], '开发工具', '项目规划'),
    (['session-logs'], '开发工具', '自我优化与反思'),
    
    # ====== GitHub集成 ======
    (['github', 'gh-'], 'GitHub集成', 'GitHub操作'),
    
    # ====== 消息与通信 ======
    (['discord', 'slack', 'telegram', 'imsg', 'himalaya', 'voice-call', 'bluebubbles'], '消息与通信', '即时通讯'),
    (['feishu'], '消息与通信', '飞书集成'),
    
    # ====== 其他工具 ======
    (['gemini'], '其他', 'AI助手'),
    (['resume-job-match', 'job', 'resume'], '其他', '求职招聘'),
    (['Proactivity', 'proactive'], '其他', '主动Agent'),
    (['a-stock-daily-report', 'claw-stock'], '金融分析工具', '股票研究与分析'),
]

# 翻译规则
TRANSLATION_RULES: Dict[str, str] = {
    "Set up and use": "设置和使用",
    "Search, install, update, sync, or publish": "搜索、安装、更新、同步或发布",
    "Search the web": "搜索网络",
    "Get current weather": "获取当前天气",
    "Diagnose": "诊断",
    "Audit and harden": "审计和加固",
    "List, configure, authenticate, call, and inspect": "列出、配置、认证、调用和检查",
    "Orchestrate multi-agent teams": "编排多智能体团队",
    "Security-first": "安全优先",
    "Create, edit, improve, tidy, review, audit, or restructure": "创建、编辑、改进、整理、审查、审计或重构",
    "Capture frames or clips": "捕获帧或片段",
    "Monitor blogs": "监控博客",
    "Discord ops via": "通过Discord进行操作",
    "Control Eight Sleep": "控制Eight Sleep",
    "Control Philips Hue": "控制Philips Hue",
    "Delegate coding tasks": "委托编码任务",
    "Create, view, edit, delete, search, move, or export": "创建、查看、编辑、删除、搜索、移动或导出",
    "Summarize or transcribe": "总结或转录",
    "Transcribe audio": "转录音频",
    "Local speech-to-text": "本地语音转文字",
    "Extract text from images": "从图像中提取文字",
    "Edit PDFs": "编辑PDF",
    "Headless browser automation": "无头浏览器自动化",
    "Browser automation via Playwright": "通过Playwright的浏览器自动化",
    "Implements Manus-style": "实现Manus风格的",
    "Continuous self-improvement": "持续自我改进",
    "Captures learnings": "捕获学习成果",
    "Coordinate multi-step": "协调多步骤",
    "Example TaskFlow": "示例TaskFlow",
    "Generate comprehensive": "生成全面的",
    "Fetch GitHub issues": "获取GitHub问题",
}
