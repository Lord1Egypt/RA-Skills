# -*- coding: utf-8 -*-
"""
技能列表生成脚本
执行 openclaw skills list --json，获取已激活/未激活技能列表并分类输出
"""
import subprocess
import json
import re
import os
import glob

SKILLS_DIR = r"C:\Users\ktao\.openclaw\workspace\skills"

# ============ 分类映射表 ============
CATEGORY_MAP = {
    # ====== 妙想平台 ======
    "eastmoney_fin_data": ("妙想平台", "妙想-行情与财务数据"),
    "eastmoney_fin_search": ("妙想平台", "妙想-搜索与资讯"),
    "eastmoney_stock_simulator": ("妙想平台", "妙想-交易与持仓"),
    "mx_self_select": ("妙想平台", "妙想-选股与自选"),
    # ====== 同花顺平台（所有依赖 IWENCAI_BASE_URL 的技能）= 26 个 ======
    "问财选A股": ("同花顺平台", "同花顺-选股与筛选"),
    "问财选ETF": ("同花顺平台", "同花顺-选股与筛选"),
    "问财选板块": ("同花顺平台", "同花顺-选股与筛选"),
    "问财选港股": ("同花顺平台", "同花顺-选股与筛选"),
    "问财选美股": ("同花顺平台", "同花顺-选股与筛选"),
    "问财选基金": ("同花顺平台", "同花顺-选股与筛选"),
    "问财选基金公司": ("同花顺平台", "同花顺-选股与筛选"),
    "问财选可转债": ("同花顺平台", "同花顺-选股与筛选"),
    "问财选期货期权": ("同花顺平台", "同花顺-选股与筛选"),
    "财务数据查询": ("同花顺平台", "同花顺-数据查询"),
    "公司经营数据查询": ("同花顺平台", "同花顺-数据查询"),
    "公司股东股本查询": ("同花顺平台", "同花顺-数据查询"),
    "基本资料查询": ("同花顺平台", "同花顺-数据查询"),
    "宏观数据查询": ("同花顺平台", "同花顺-数据查询"),
    "行情数据查询": ("同花顺平台", "同花顺-数据查询"),
    "行业数据查询": ("同花顺平台", "同花顺-数据查询"),
    "指数数据查询": ("同花顺平台", "同花顺-数据查询"),
    "基金理财查询": ("同花顺平台", "同花顺-数据查询"),
    "期货期权数据查询": ("同花顺平台", "同花顺-数据查询"),
    "公告搜索": ("同花顺平台", "同花顺-搜索与资讯"),
    "新闻搜索": ("同花顺平台", "同花顺-搜索与资讯"),
    "研报搜索": ("同花顺平台", "同花顺-搜索与资讯"),
    "投资者关系活动搜索": ("同花顺平台", "同花顺-搜索与资讯"),
    "机构研究与评级查询": ("同花顺平台", "同花顺-搜索与资讯"),
    "事件数据查询": ("同花顺平台", "同花顺-搜索与资讯"),
    "模拟炒股": ("同花顺平台", "同花顺-模拟交易"),
    # ====== 富途平台 ======
    "futuapi": ("富途平台", "富途-行情API"),
    "install-opend": ("富途平台", "富途-安装配置"),
    # ====== 搜索工具 ======
    "multi-search-engine": ("搜索工具", "网页搜索"),
    "desearch-web-search": ("搜索工具", "网页搜索"),
    "desearch-web-search-uninstall-install-configure-troubleshooting": ("搜索工具", "网页搜索"),
    "find-skills": ("搜索工具", "网页搜索"),
    "tavily": ("搜索工具", "网页搜索"),
    # ====== 金融分析工具 ======
    "stock-analysis": ("金融分析工具", "股票研究与分析"),
    "akshare-stock": ("金融分析工具", "股票研究与分析"),
    "上市公司财报体检": ("金融分析工具", "股票研究与分析"),
    "股票研究": ("金融分析工具", "股票研究与分析"),
    "科技炒作与基本面": ("金融分析工具", "股票研究与分析"),
    "高分红股挑选": ("金融分析工具", "股票研究与分析"),
    "财务报表深度解读": ("金融分析工具", "财报与财务"),
    "估值模型方法论": ("金融分析工具", "财报与财务"),
    "产业链解读": ("金融分析工具", "行业与产业链"),
    "行业概览": ("金融分析工具", "行业与产业链"),
    "行业轮动分析": ("金融分析工具", "行业与产业链"),
    "K线形态识别": ("金融分析工具", "行业与产业链"),
    "基础技术指标信号引擎": ("金融分析工具", "行业与产业链"),
    "市场情绪分析": ("金融分析工具", "市场情绪与宏观"),
    "市场情绪偏离分析": ("金融分析工具", "市场情绪与宏观"),
    "市场微观结构分析": ("金融分析工具", "市场情绪与宏观"),
    "宏观周期分析": ("金融分析工具", "市场情绪与宏观"),
    "全球宏观分析框架": ("金融分析工具", "市场情绪与宏观"),
    "地缘政治风险分析": ("金融分析工具", "市场情绪与宏观"),
    "期权盈亏分析": ("金融分析工具", "市场情绪与宏观"),
    "多因子选股策略": ("金融分析工具", "量化与因子"),
    "基本面因子筛选": ("金融分析工具", "量化与因子"),
    "策略生成与优化": ("金融分析工具", "量化与因子"),
    "量化统计方法": ("金融分析工具", "量化与因子"),
    "机器学习策略": ("金融分析工具", "量化与因子"),
    "对冲策略设计": ("金融分析工具", "量化与因子"),
    "资产配置与组合优化": ("金融分析工具", "量化与因子"),
    "业绩归因分析": ("金融分析工具", "量化与因子"),
    "晨会纪要": ("金融分析工具", "晨会纪要与研报"),
    "首次覆盖报告": ("金融分析工具", "晨会纪要与研报"),
    "社交媒体情报分析": ("金融分析工具", "公告与新闻搜索"),
    "风险分析与压力测试": ("金融分析工具", "风险与策略"),
    "金融监管知识库": ("金融分析工具", "风险与策略"),
    "沪深港通资金流分析": ("金融分析工具", "资金流向分析"),
    # ====== 系统工具 ======
    "ocr-local": ("系统工具", "OCR与文档处理"),
    "openai-whisper": ("系统工具", "语音与音频"),
    "openai-whisper-api": ("系统工具", "语音与音频"),
    "sag": ("系统工具", "语音与音频"),
    "sherpa-onnx-tts": ("系统工具", "语音与音频"),
    "agent-browser": ("系统工具", "浏览器自动化"),
    "playwright-mcp": ("系统工具", "浏览器自动化"),
    "nano-pdf": ("系统工具", "文件编辑与数据清洗"),
    "电子表格数据清洗": ("系统工具", "文件编辑与数据清洗"),
    "summarize": ("系统工具", "文件编辑与数据清洗"),
    "kt_skill_financial_memory": ("系统工具", "记忆与知识库"),
    "memos-memory-guide": ("系统工具", "记忆与知识库"),
    "healthcheck": ("系统工具", "定时任务与系统运维"),
    "node-connect": ("系统工具", "定时任务与系统运维"),
    "taskflow": ("系统工具", "定时任务与系统运维"),
    "taskflow-inbox-triage": ("系统工具", "定时任务与系统运维"),
    "weather": ("系统工具", "定时任务与系统运维"),
    "verify-and-delete-multiple-agents": ("系统工具", "定时任务与系统运维"),
    # ====== 开发工具 ======
    "self-improvement": ("开发工具", "自我优化与反思"),
    "Self-Improving + Proactive Agent": ("开发工具", "自我优化与反思"),
    "self-reflection": ("开发工具", "自我优化与反思"),
    "session-logs": ("开发工具", "自我优化与反思"),
    "coding-agent": ("开发工具", "编码与开发"),
    "skill-creator": ("开发工具", "编码与开发"),
    "skill-vetter": ("开发工具", "编码与开发"),
    "clawhub": ("开发工具", "编码与开发"),
    "code-analyzer": ("开发工具", "代码分析"),
    "planning-with-files": ("开发工具", "项目规划"),
    "agent-team-orchestration": ("开发工具", "项目规划"),
    # ====== GitHub集成 ======
    "gh-issues": ("GitHub集成", "GitHub操作"),
    "github": ("GitHub集成", "GitHub操作"),
    # ====== 消息与通信 ======
    "discord": ("消息与通信", "Discord/Telegram/Slack"),
    "slack": ("消息与通信", "Discord/Telegram/Slack"),
    "voice-call": ("消息与通信", "Discord/Telegram/Slack"),
    "feishu-doc": ("消息与通信", "飞书集成"),
    "feishu-drive": ("消息与通信", "飞书集成"),
    "feishu-perm": ("消息与通信", "飞书集成"),
    "feishu-wiki": ("消息与通信", "飞书集成"),
    # ====== needsetup 技能 ======
    # 妙想平台
    "mx-skills": ("妙想平台", "妙想-选股与自选"),
    # 金融分析
    "gemini": ("金融分析工具", "股票研究与分析"),
    "akshare-connection-troubleshooting-and-financial-data-query-for-ai-agent": ("金融分析工具", "股票研究与分析"),
    "akshare-stock-financial-data-acquisition-and-tls-connection-troubleshooting": ("金融分析工具", "股票研究与分析"),
    "daily-digest": ("金融分析工具", "晨会纪要与研报"),
    "kt_skill_cls_news": ("金融分析工具", "公告与新闻搜索"),
    # 搜索工具
    "desearch-web-search-uninstall-reinstall-configure-workflow": ("搜索工具", "网页搜索"),
    "xurl": ("搜索工具", "网页搜索"),
    "blogwatcher": ("搜索工具", "网页搜索"),
    "gifgrep": ("搜索工具", "网页搜索"),
    # 系统工具
    "clawhub-ocr-installation-web-search-api-configuration": ("系统工具", "OCR与文档处理"),
    "apple-notes": ("系统工具", "文件编辑与数据清洗"),
    "bear-notes": ("系统工具", "文件编辑与数据清洗"),
    "notion": ("系统工具", "文件编辑与数据清洗"),
    "obsidian": ("系统工具", "文件编辑与数据清洗"),
    "camsnap": ("系统工具", "文件编辑与数据清洗"),
    "video-frames": ("系统工具", "文件编辑与数据清洗"),
    "songsee": ("系统工具", "语音与音频"),
    "sonoscli": ("系统工具", "语音与音频"),
    "spotify-player": ("系统工具", "语音与音频"),
    "peekaboo": ("系统工具", "浏览器自动化"),
    "memos-plugin-embedding-ollama-troubleshooting-and-fix": ("系统工具", "记忆与知识库"),
    "kt_skill_list_skill": ("系统工具", "定时任务与系统运维"),
    "kt_skill_model_summary": ("系统工具", "定时任务与系统运维"),
    "1password": ("系统工具", "定时任务与系统运维"),
    "apple-reminders": ("系统工具", "定时任务与系统运维"),
    "eightctl": ("系统工具", "定时任务与系统运维"),
    "gog": ("系统工具", "定时任务与系统运维"),
    "goplaces": ("系统工具", "定时任务与系统运维"),
    "blucli": ("系统工具", "定时任务与系统运维"),
    "model-usage": ("系统工具", "定时任务与系统运维"),
    "openhue": ("系统工具", "定时任务与系统运维"),
    "ordercli": ("系统工具", "定时任务与系统运维"),
    "things-mac": ("系统工具", "定时任务与系统运维"),
    "tmux": ("系统工具", "定时任务与系统运维"),
    "trello": ("系统工具", "定时任务与系统运维"),
    "wacli": ("系统工具", "定时任务与系统运维"),
    "fix-openclaw-gateway-cron-error-and-configure-self-reflection-heartbeat": ("系统工具", "定时任务与系统运维"),
    "fix-openclaw-timed-task-gateway-error-and-config-auto-start": ("系统工具", "定时任务与系统运维"),
    "gateway-auto-restart-failure-troubleshooting-windows-task-scheduler": ("系统工具", "定时任务与系统运维"),
    "multi-platform-position-record-management-and-uv-installation-configuration": ("系统工具", "定时任务与系统运维"),
    "openclaw-coding-agent-activation-claude-code-data-processing-program": ("系统工具", "定时任务与系统运维"),
    "openclaw-desearch-plugin-switch-install-config": ("系统工具", "定时任务与系统运维"),
    "openclaw-environment-configuration-and-troubleshooting": ("系统工具", "定时任务与系统运维"),
    "openclaw-model-statistics-switch-config-fix": ("系统工具", "定时任务与系统运维"),
    "openclaw-session-agent-management-and-reasoning-level-configuration": ("系统工具", "定时任务与系统运维"),
    "openclaw-skill-installation-validation-and-api-configuration": ("系统工具", "定时任务与系统运维"),
    "openclaw-system-config-cleanup-and-gateway-registration": ("系统工具", "定时任务与系统运维"),
    "openclaw-system-config-cleanup-and-gateway-service-registration": ("系统工具", "定时任务与系统运维"),
    "openclaw-system-configuration-check-and-troubleshooting": ("系统工具", "定时任务与系统运维"),
    "openclaw-system-configuration-cleanup-and-gateway-service-registration": ("系统工具", "定时任务与系统运维"),
    "openclaw-system-configuration-cleanup-and-optimization": ("系统工具", "定时任务与系统运维"),
    # 开发工具
    "mcporter": ("开发工具", "编码与开发"),
    "oracle": ("开发工具", "编码与开发"),
    "configure-activate-system-builtin-coding-agent-for-claude-code": ("开发工具", "编码与开发"),
    "multi-agent-system-status-check-and-operations": ("开发工具", "项目规划"),
    "multi-agent-system-status-checking-and-configuration-tuning": ("开发工具", "项目规划"),
    # 消息与通信
    "himalaya": ("消息与通信", "Discord/Telegram/Slack"),
    "imsg": ("消息与通信", "Discord/Telegram/Slack"),
    "bluebubbles": ("消息与通信", "Discord/Telegram/Slack"),
    "cleanup-cron-feishu-config-register-gateway-service": ("消息与通信", "飞书集成"),
}

# ============ 大类排序 ============
CATEGORY_ORDER = ["妙想平台", "同花顺平台", "富途平台", "搜索工具", "金融分析工具", "系统工具", "开发工具", "GitHub集成", "消息与通信"]

# ============ 英文翻译规则 ============
TRANSLATION_RULES = {
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


def load_meta_data():
    """读取各技能的 _meta.json，返回 { skill_name: { version, author } }"""
    meta = {}
    for meta_file in glob.glob(os.path.join(SKILLS_DIR, "*", "_meta.json")):
        dir_name = os.path.basename(os.path.dirname(meta_file))
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            v = data.get("version", "")
            owner = data.get("ownerId", "")
            # ownerId 是 hash，没有可读的作者名；但保留用作追溯
            meta[dir_name] = {"version": v, "author": owner}
        except Exception:
            pass
    return meta


def get_version_author(name, meta_data, data_dict):
    """获取技能的版本号和作者"""
    # 优先从 _meta.json 获取（slug 或 dir_name 可能不同）
    # 检查 data_dict 中是否有 name 对应的 entry
    info = data_dict.get(name, meta_data.get(name, {}))
    return info.get("version", ""), info.get("author", "")


def translate_description(desc):
    if not desc:
        return desc
    result = desc
    for eng, chn in TRANSLATION_RULES.items():
        if result.startswith(eng):
            result = chn + result[len(eng):]
            break
    return result


def clean_json_text(text):
    if not text:
        return ""
    if text.startswith('\ufeff'):
        text = text[1:]
    text = re.sub(r'[\ue000-\uf8ff]', '', text)
    return text


def get_category(skill_name):
    if skill_name in CATEGORY_MAP:
        return CATEGORY_MAP[skill_name]
    return ("其他", "其他")


def main():
    # 加载 meta 数据
    meta_data = load_meta_data()

    # 构建 _meta.json 中 slug 到 name 的反向映射
    slug_to_name = {}
    for meta_file in glob.glob(os.path.join(SKILLS_DIR, "*", "_meta.json")):
        dir_name = os.path.basename(os.path.dirname(meta_file))
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            slug = data.get("slug", "")
            if slug and slug != dir_name:
                slug_to_name[slug] = dir_name
        except Exception:
            pass

    # 执行 openclaw skills list --json
    try:
        result = subprocess.run(
            ['node', '-e', "console.log(require('child_process').execSync('openclaw skills list --json', {encoding: 'utf8', timeout: 30000}))"],
            capture_output=True, text=True, encoding='utf-8', timeout=60
        )
        raw_output = result.stdout
    except Exception as e:
        print(f"执行 openclaw skills list --json 失败: {e}")
        return

    cleaned = clean_json_text(raw_output)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        print("原始输出前500字符:", raw_output[:500])
        return

    if isinstance(data, dict) and 'skills' in data:
        skills_list = data['skills']
    elif isinstance(data, list):
        skills_list = data
    else:
        print(f"未知的JSON格式")
        return

    activated = []
    not_activated = []

    # 从 openclaw skills list 获取的技能名
    registered_names = set()

    for skill in skills_list:
        name = skill.get('name', '')
        if name:
            registered_names.add(name)
        eligible = skill.get('eligible', False)
        disabled = skill.get('disabled', False)
        description = skill.get('description', '')

        # 从 _meta.json 获取版本和作者
        version = ""
        author = ""
        # 尝试直接匹配 name
        if name in meta_data:
            version = meta_data[name].get("version", "")
            author = meta_data[name].get("author", "")
        # 尝试通过 slug 匹配
        if not version and name in slug_to_name:
            dir_name = slug_to_name[name]
            if dir_name in meta_data:
                version = meta_data[dir_name].get("version", "")
                author = meta_data[dir_name].get("author", "")
        # 尝试匹配将 - 换成 _
        alt_name = name.replace("-", "_")
        if not version and alt_name in meta_data:
            version = meta_data[alt_name].get("version", "")
            author = meta_data[alt_name].get("author", "")
        # 妙想平台的 slug 有不同命名规则
        mx_variants = {
            "eastmoney_fin_data": "eastmoney-fin-data",
            "eastmoney_fin_search": "eastmoney-fin-search",
            "eastmoney_stock_simulator": "eastmoney-stock-simulator",
            "mx_self_select": "eastmoney-self-select",
        }
        if not version and name in mx_variants:
            slug = mx_variants[name]
            dir_name = slug_to_name.get(slug, "")
            if dir_name and dir_name in meta_data:
                version = meta_data[dir_name].get("version", "")
                author = meta_data[dir_name].get("author", "")

        skill_info = {
            'name': name,
            'description': description,
            'version': version,
            'author': author,
        }

        if eligible and not disabled:
            activated.append(skill_info)
        else:
            not_activated.append(skill_info)

    # >>> 扫描 skills 目录中未在 openclaw 注册的技能 <<<
    # 已知的目录名 → openclaw 技能名映射（避免重复）
    DIR_TO_NAME = {
        "mx-data": "eastmoney_fin_data",
        "mx-search": "eastmoney_fin_search",
        "mx-select-stock": "eastmoney_fin_search",
        "mx-selfselect": "mx_self_select",
        "mx-stock-simulator": "eastmoney_stock_simulator",
        "agent-browser-clawdbot": "agent-browser",
        "kt_skill_financial_memory": "kt_skill_financial_memory",
        "self-improving": "self-improvement",
        "self-improving-agent": "Self-Improving + Proactive Agent",
        "openai-whisper": "openai-whisper",
        "desearch-web-search-uninstall-install-configure-troubleshooting": "desearch-web-search-uninstall-install-configure-troubleshooting",
        "clawhub-ocr-installation-web-search-api-configuration": "clawhub-ocr-installation-web-search-api-configuration",
    }
    
    for entry in sorted(os.scandir(SKILLS_DIR), key=lambda e: e.name):
        if not entry.is_dir():
            continue
        dir_name = entry.name
        # 检查是否已注册（直接名或映射名）
        mapped = DIR_TO_NAME.get(dir_name, dir_name)
        if mapped in registered_names:
            continue
        if dir_name in registered_names:
            continue
        # 跳过非技能目录（以下划线开头的特殊目录）
        if dir_name.startswith('.'):
            continue
        skill_md = os.path.join(entry.path, "SKILL.md")
        if not os.path.exists(skill_md):
            # 尝试子目录（问财选等技能的 SKILL.md 在子目录中）
            for sub in sorted(os.scandir(entry.path), key=lambda e: e.name):
                if sub.is_dir():
                    sub_md = os.path.join(sub.path, "SKILL.md")
                    if os.path.exists(sub_md):
                        skill_md = sub_md
                        break
        if not os.path.exists(skill_md):
            continue
        # 读取 SKILL.md 第一行获取描述
        desc = ""
        try:
            with open(skill_md, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#"):
                        desc = line.lstrip("#").strip()
                        break
        except Exception:
            pass
        # 元数据
        version = ""
        author = ""
        if dir_name in meta_data:
            version = meta_data[dir_name].get("version", "")
            author = meta_data[dir_name].get("author", "")
        skill_info = {
            "name": dir_name,
            "description": desc,
            "version": version,
            "author": author,
        }
        # 这些技能存在于文件系统，视为已激活
        activated.append(skill_info)

    output_dir = r"C:\Users\ktao\openclaw_out"
    os.makedirs(output_dir, exist_ok=True)

    # 生成输出
    for skills, title, is_activated in [
        (activated, "已激活技能列表", True),
        (not_activated, "未激活技能列表", False),
    ]:
        # 按大类+子类分组
        categories = {}
        for skill in skills:
            cat = get_category(skill['name'])
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(skill)

        lines = []
        total = len(skills)
        lines.append(f"# {title}")
        lines.append(f"> 数据来源：openclaw skills list | 共 **{total}** 个{'已' if is_activated else '未'}激活技能")
        lines.append("")

        def sort_key(item):
            (big_cat, sub_cat), _ = item
            big_idx = CATEGORY_ORDER.index(big_cat) if big_cat in CATEGORY_ORDER else 999
            return (big_idx, sub_cat)

        big_counter = 0
        sub_counter_map = {}
        prev_big = None

        idx = 0
        for (big_cat, sub_cat), cat_skills in sorted(categories.items(), key=sort_key):
            if big_cat != prev_big:
                big_counter += 1
                sub_counter_map[big_cat] = 0
                prev_big = big_cat
                lines.append(f"{big_counter}. {big_cat}")
                lines.append("")
            sub_counter_map[big_cat] += 1
            sc = sub_counter_map[big_cat]
            lines.append(f"   {big_counter}.{sc} {sub_cat}")
            lines.append("")
            lines.append("| 序号 | 技能名称 | 描述 |")
            lines.append("|------|----------|------|")
            for skill in cat_skills:
                idx += 1
                desc = translate_description(skill.get('description', ''))
                lines.append(f"| {idx} | {skill['name']} | {desc} |")
            lines.append("")

        output_path = os.path.join(output_dir, f"{title}.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    print(f"已激活技能: {len(activated)} 个")
    print(f"未激活技能: {len(not_activated)} 个")
    print("文件已生成")


if __name__ == "__main__":
    main()
