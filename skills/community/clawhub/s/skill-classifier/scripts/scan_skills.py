#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能列表扫描脚本
功能: 扫描 OpenClaw 所有技能,按激活状态和功能分类输出
"""

import os
import re
import json
import subprocess
from pathlib import Path

# 配置路径
OPENCLAW_CONFIG = r"C:\Users\ktao\.openclaw\openclaw.json"
SKILLS_DIR = r"C:\Users\ktao\.openclaw\workspace\skills"
OUTPUT_DIR = r"C:\Users\ktao\openclaw_out"

# 技能说明翻译（英文->中文）
DESCRIPTION_TRANSLATION = {
    "Search the web and get real-time SERP-style": "网页搜索，获取实时SERP格式结果，包含标题、URL和摘要",
    "Browser automation via Playwright MCP server": "通过Playwright MCP服务器实现浏览器自动化",
    "Extract text from images using Tesseract.js": "使用Tesseract.js OCR进行图片文字提取（100%本地，无需API Key）",
    "Edit PDFs with natural-language instructions": "使用自然语言指令编辑PDF文件",
    "A quantitative trading development framework": "量化交易开发框架",
    "Multi search engine integration with 17 engines": "多搜索引擎集成，支持17个搜索引擎",
    "Search and discover OpenClaw skills from various": "搜索发现OpenClaw技能",
    "Security-first skill vetting for AI agents": "AI Agent安全优先的技能审查",
    "Implements Manus-style file-based planning": "实现Manus风格的基于文件的规划工具",
    "Search your own session logs (older/parent conversations)": "搜索自己的会话日志（历史/上级对话）",
}

# 系列技能分组
SKILL_GROUPS = {
    "妙想系列技能": ["mx-data", "mx-search", "mx-select-stock", "mx-selfselect", "mx-skills", "mx-stock-simulator"],
    "富途系列技能": ["futuapi", "install-opend"],
    "AkShare系列技能": ["akshare-stock", "akshare-stock-financial-data-acquisition", "akshare-connection-troubleshooting"],
    "多代理协作系列": ["agent-team-orchestration", "multi-agent-system-status-check", "multi-agent-system-status-checking"],
    "Desearch系列技能": ["desearch-web-search", "openclaw-desearch-plugin-switch", "desearch-web-search-uninstall-install", "desearch-web-search-uninstall-reinstall"],
    "Gateway运维系列": ["gateway-auto-restart-failure", "fix-openclaw-timed-task-gateway", "fix-openclaw-gateway-cron"],
    "系统配置系列": ["openclaw-environment-configuration", "openclaw-system-config-cleanup", "openclaw-system-config-cleanup-and-gateway", "openclaw-system-configuration-check", "openclaw-system-configuration-cleanup"],
    "同花顺系列技能": ["模拟炒股", "问财选股"],
}

# 功能分类映射 - 按优先级排序
CATEGORY_KEYWORDS = {
    # ========== 金融类 9个 ==========
    "金融行情数据": [
        "akshare", "行情", "quote", "market", "fundamental",
        "行情数据", "市场数据", "股票行情", "价格", "quote", "数据查询"
    ],
    "金融基本面数据": [
        "财报", "财务", "基本面", "finance", "financial",
        "财务数据", "财务报表", "业绩", "利润表", "资产负债表", "经营数据", "股东股本"
    ],
    "金融资讯获取": [
        "新闻", "资讯", "公告", "财联社", "news", "announcement",
        "研报", "事件", "市场动态", "mx-search", "晨会", "资讯搜索", "资讯获取"
    ],
    "金融筛选工具": [
        "选股", "筛选", "filter", "selector", "问财", "select",
        "智能选股", "条件选股", "选债", "选ETF", "多因子"
    ],
    "金融分析工具": [
        "分析", "研究", "报告", "策略", "情绪", "产业链", "估值",
        "analysis", "research", "股票研究", "技术分析", "财报分析",
        "估值分析", "风险分析", "财报体检", "市场情绪"
    ],
    "金融预测评级": [
        "评级", "预测", "首次覆盖", "rating", "prediction",
        "目标价", "盈利预测", "券商评级"
    ],
    "交易执行与持仓": [
        "交易", "持仓", "trade", "position", "simulator",
        "交易执行", "持仓管理", "模拟炒股", "买卖", "下单",
        "撤单", "实盘", "模拟交易"
    ],
    "行业与板块": [
        "行业", "板块", "industry", "sector", "板块分析",
        "行业概览", "产业链"
    ],
    "风险与压力测试": [
        "风险", "压力测试", "risk", "风控", "风险分析"
    ],
    
    # ========== 工具类 5个 ==========
    "搜索工具": [
        "搜索", "search", "desearch", "multi-search", "tavily",
        "find", "搜索引擎", "网页搜索", "查询", "投资者关系活动", "机构研究"
    ],
    "OCR技能": [
        "ocr", "文字识别", "图像识别", "文字提取", "识别图片"
    ],
    "浏览器自动化": [
        "浏览器", "browser", "playwright", "automation",
        "网页抓取", "页面操作", "动态页面"
    ],
    "文档与数据处理": [
        "文档处理", "pdf", "数据清洗", "数据处理", "excel",
        "表格", "文档", "document", "data", "电子表格",
        "文件处理", "格式转换", "数据整理", "数据处理程序"
    ],
    "语音与音频": [
        "语音", "音频", "audio", "voice", "whisper",
        "语音识别", "语音合成", "语音转文字"
    ],
    
    # ========== 系统与开发类 4个 ==========
    "自我优化技能": [
        "自我", "self-", "reflection", "improving",
        "优化", "改进", "反思", "自我提升", "自我进化"
    ],
    "开发工具": [
        "代码", "开发", "coding", "code-analyzer", "编程",
        "开发工具", "代码分析", "代码生成", "开发辅助", "coding-agent"
    ],
    "系统配置与运维": [
        "系统", "运维", "配置", "gateway", "system", "config",
        "故障排查", "gateway服务", "定时任务", "系统配置",
        "环境配置", "服务注册", "运维工具", "管理", "清理", "故障"
    ],
    "多代理协作": [
        "多代理", "agent", "team", "协作", "多智能体",
        "agent-team", "代理管理", "会话管理", "agent管理"
    ],
    
    # ========== 知识管理类 ==========
    "知识记忆系统": [
        "记忆", "memory", "知识库", "memos", "金融记忆",
        "知识管理", "知识存储", "记忆系统"
    ],
    
    # ========== 集成类 2个 ==========
    "飞书集成": [
        "feishu", "飞书", "lark", "飞书文档", "飞书云",
        "飞书权限", "飞书集成"
    ],
    "即时通讯集成": [
        "微信", "wechat", "im", "即时通讯", "微信集成", "企业微信"
    ],
}

# 系统自带技能列表
SYSTEM_SKILLS = [
    "self-reflection",
    "self-improving", 
    "planning-with-files",
    "session-logs",
    "find-skills",
    "skill-vetter",
    "verify-and-delete",
    "memos-memory",
    "agent-team",
    "agent-browser",
    "healthcheck",
]


def get_skill_status_from_cli():
    """通过 openclaw skills list 命令获取技能状态 - 纯文本解析"""
    try:
        # 使用 cmd 执行，避免 PowerShell 编码问题
        result = subprocess.run(
            ['cmd', '/c', 'openclaw skills list'],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=r"C:\Users\ktao\.openclaw\workspace",
            encoding='utf-8',
            errors='ignore'
        )
        
        output = result.stdout
        status_map = {}
        
        # 逐行解析，查找 "ready" 或 "need setup" 关键词
        lines = output.split('\n')
        for line in lines:
            line_lower = line.lower()
            
            # 判断状态
            is_ready = 'ready' in line_lower and 'needs setup' not in line_lower
            needs_setup = 'needs setup' in line_lower
            
            if not is_ready and not needs_setup:
                continue
                
            # 提取技能名称 - 查找在 markdown 表格中的第二列
            parts = line.split('|')
            if len(parts) >= 3:
                # parts[0] = 状态列, parts[1] = emoji, parts[2] = 技能名称
                skill_name = parts[2].strip() if len(parts) > 2 else ''
                if skill_name and skill_name != 'Skill' and skill_name != '---':
                    status_map[skill_name] = is_ready and not needs_setup
        
        return status_map if status_map else None
    except Exception as e:
        print(f"获取 CLI 状态失败: {e}")
        return None


def translate_description(desc):
    """翻译技能说明为中文"""
    if not desc or desc == "技能说明待补充":
        return desc
    
    # 查找匹配的翻译
    for en, zh in DESCRIPTION_TRANSLATION.items():
        if en in desc:
            return zh + " | " + desc[:50] + "..." if len(desc) > 50 else zh
    
    # 如果已经包含中文，直接返回
    if any('\u4e00' <= c <= '\u9fff' for c in desc):
        return desc
    
    return desc


def get_skill_group(name):
    """判断技能所属系列分组"""
    for group, keywords in SKILL_GROUPS.items():
        for kw in keywords:
            if kw.lower() in name.lower():
                return group
    return None


def load_config():
    """加载 OpenClaw 配置"""
    with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_yaml_frontmatter(content):
    """解析 YAML frontmatter"""
    if not content.startswith('---\n'):
        return None, content
    
    lines = content.split('\n')
    end_idx = -1
    for i in range(1, min(30, len(lines))):
        if lines[i].strip() == '---':
            end_idx = i
            break
    
    if end_idx == -1:
        return None, content
    
    frontmatter = {}
    for line in lines[1:end_idx]:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip().strip('\'"')
    
    return frontmatter, '\n'.join(lines[end_idx+1:])


def get_skill_description(skill_dir):
    """获取技能说明"""
    skill_md = os.path.join(skill_dir, 'SKILL.md')
    if not os.path.exists(skill_md):
        return ""
    
    try:
        with open(skill_md, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return ""
    
    frontmatter, body = parse_yaml_frontmatter(content)
    
    # 优先使用 frontmatter 的 description
    if frontmatter and 'description' in frontmatter:
        desc = frontmatter['description']
        if len(desc) > 150:
            desc = desc[:147] + '...'
        return desc
    
    # 否则读取正文第一行
    body_lines = [l.strip() for l in body.split('\n') if l.strip()]
    for line in body_lines[:8]:
        if line and len(line) > 5:
            # 移除 markdown 标题标记
            line = re.sub(r'^#+\s*', '', line)
            if len(line) > 150:
                line = line[:147] + '...'
            return line
    
    return ""


def get_category(skill_name, description, group=None):
    """判断技能功能分类 - 按优先级匹配"""
    skill_lower = skill_name.lower()
    desc_lower = description.lower() if description else ""
    
    # 如果有分组，优先按分组判断
    if group:
        if "妙想" in group:
            return "金融资讯获取"
        elif "富途" in group:
            return "交易执行与持仓"
        elif "AkShare" in group:
            return "金融行情数据"
        elif "Desearch" in group:
            return "搜索工具"
        elif "Gateway" in group or "系统配置" in group:
            return "系统配置与运维"
        elif "多代理" in group:
            return "多代理协作"
        elif "同花顺" in group:
            return "交易执行与持仓"
    
    # 遍历所有分类,找到第一个匹配的
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in skill_lower or kw_lower in desc_lower:
                return category
    
    return "其他工具"


def get_source(skill_name, group=None):
    """判断技能来源"""
    if skill_name.startswith('kt_skill_'):
        return "用户创建"
    
    skill_lower = skill_name.lower()
    for sys_kw in SYSTEM_SKILLS:
        if sys_kw.lower() in skill_lower:
            return "系统自带"
    
    if group:
        if "妙想" in group:
            return "东方财富"
        elif "富途" in group:
            return "富途证券"
        elif "同花顺" in group:
            return "同花顺"
    
    return "安装"


def is_activated(skill_name, config, cli_status=None):
    """判断技能是否激活"""
    # kt_skill_ 前缀默认激活(用户创建的技能)
    if skill_name.startswith('kt_skill_'):
        return True
    
    # 优先使用 CLI 状态
    if cli_status is not None:
        # 精确匹配
        if skill_name in cli_status:
            return cli_status[skill_name]
        
        # 部分匹配
        skill_lower = skill_name.lower()
        for name, status in cli_status.items():
            if name.lower() in skill_lower or skill_lower in name.lower():
                return status
    
    # 检查 plugins.entries
    if config and 'plugins' in config and 'entries' in config['plugins']:
        entries = config['plugins']['entries']
        skill_lower = skill_name.lower()
        
        # 精确匹配
        if skill_name in entries:
            return entries[skill_name].get('enabled', False)
        
        # 部分匹配
        for name in entries:
            if name.lower() in skill_lower:
                return entries[name].get('enabled', False)
    
    # 其他已安装技能默认为激活状态
    return True


def scan_skills():
    """扫描所有技能"""
    config = load_config()
    cli_status = get_skill_status_from_cli()
    
    # 调试：输出获取到的状态
    if cli_status:
        print(f"成功获取 {len(cli_status)} 个技能的CLI状态")
        for name, ready in list(cli_status.items())[:10]:
            print(f"  - {name}: {'ready' if ready else 'need setup'}")
    else:
        print("⚠️ 未能获取 CLI 状态")
    
    skills = []
    
    if not os.path.exists(SKILLS_DIR):
        print(f"技能目录不存在: {SKILLS_DIR}")
        return []
    
    for entry in os.listdir(SKILLS_DIR):
        skill_dir = os.path.join(SKILLS_DIR, entry)
        if not os.path.isdir(skill_dir):
            continue
            
        original_name = entry
        group = get_skill_group(original_name)
        description = get_skill_description(skill_dir)
        
        # 翻译技能说明（而不是技能名称）
        translated_desc = translate_description(description)
        
        category = get_category(original_name, description, group)
        source = get_source(original_name, group)
        activated = is_activated(original_name, config, cli_status)
        
        skills.append({
            'original_name': original_name,
            'group': group,
            'category': category,
            'source': source,
            'description': translated_desc or "技能说明待补充",
            'activated': activated
        })
    
    return skills


def generate_markdown(skills, title):
    """生成 Markdown 文档"""
    md = f"# {title}\n\n"
    md += f"> 生成时间: {os.popen('powershell -Command Get-Date').read().strip()}\n\n"
    
    # 统计信息
    md += f"## 概览\n\n"
    md += f"| 项目 | 数量 |\n"
    md += f"|------|------|\n"
    
    # 统计各来源数量
    sources = sorted(set(s['source'] for s in skills))
    for source in sources:
        count = len([s for s in skills if s['source'] == source])
        md += f"| {source} | {count} 个 |\n"
    
    md += f"| **合计** | **{len(skills)} 个** |\n"
    
    md += "\n---\n\n"
    
    global_idx = 1  # 全局连贯序号
    
    # 按来源分组输出
    for source in sources:
        source_skills = [s for s in skills if s['source'] == source]
        md += f"## {source}\n\n"
        
        # 来源内先按系列分组,再按功能分类
        groups = sorted(set(s['group'] for s in source_skills if s['group']))
        ungrouped = [s for s in source_skills if not s['group']]
        
        # 输出系列技能
        for group in groups:
            group_skills = [s for s in source_skills if s['group'] == group]
            md += f"### {group}\n\n"
            
            # 系列内按功能分类
            categories = sorted(set(s['category'] for s in group_skills))
            
            for category in categories:
                category_skills = [s for s in group_skills if s['category'] == category]
                md += f"#### {category}\n\n"
                
                md += "| 序号 | 技能名称 | 功能分类 | 来源 | 说明 |\n"
                md += "|------|----------|----------|------|------|\n"
                
                for skill in category_skills:
                    desc = skill['description'].replace('|', '\\|')
                    md += f"| {global_idx} | {skill['original_name']} | {skill['category']} | {skill['source']} | {desc} |\n"
                    global_idx += 1
                
                md += "\n"
        
        # 输出未分组技能
        if ungrouped:
            categories = sorted(set(s['category'] for s in ungrouped))
            
            for category in categories:
                category_skills = [s for s in ungrouped if s['category'] == category]
                md += f"### {category}\n\n"
                
                md += "| 序号 | 技能名称 | 功能分类 | 来源 | 说明 |\n"
                md += "|------|----------|----------|------|------|\n"
                
                for skill in category_skills:
                    desc = skill['description'].replace('|', '\\|')
                    md += f"| {global_idx} | {skill['original_name']} | {skill['category']} | {skill['source']} | {desc} |\n"
                    global_idx += 1
                
                md += "\n"
    
    return md


def main():
    print("开始扫描技能...")
    
    skills = scan_skills()
    print(f"共发现 {len(skills)} 个技能")
    
    activated = [s for s in skills if s['activated']]
    deactivated = [s for s in skills if not s['activated']]
    
    print(f"已激活(ready): {len(activated)}, 未激活(need setup): {len(deactivated)}")
    
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 生成已激活技能列表
    activated_md = generate_markdown(activated, "已激活技能列表")
    with open(os.path.join(OUTPUT_DIR, '已激活技能列表.md'), 'w', encoding='utf-8') as f:
        f.write(activated_md)
    
    # 生成未激活技能列表
    deactivated_md = generate_markdown(deactivated, "未激活技能列表")
    with open(os.path.join(OUTPUT_DIR, '未激活技能列表.md'), 'w', encoding='utf-8') as f:
        f.write(deactivated_md)
    
    print("\n✅ 生成完成!")
    print(f"   - {os.path.join(OUTPUT_DIR, '已激活技能列表.md')}")
    print(f"   - {os.path.join(OUTPUT_DIR, '未激活技能列表.md')}")


if __name__ == '__main__':
    main()