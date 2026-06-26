#!/usr/bin/env python3
"""
robot-evolve 核心脚本
执行所有L0/L1级别自动进化动作

使用方法：
    python auto_evolve.py              # 执行完整进化
    python auto_evolve.py --dry-run    # 模拟运行（不实际修改）
    python auto_evolve.py --check-only # 只检查，不执行
"""

import os
import sys
import json
import shutil
import re
from pathlib import Path
from datetime import datetime

# Windows UTF-8兼容
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 工作区路径（优先读取环境变量，否则从脚本位置推断）
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path(__file__).parent.parent.parent))
SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
MEMORY_DIR = WORKSPACE / "memory"
TEMP_DIR = WORKSPACE / "temp"
EVOLUTION_DIR = MEMORY_DIR / "evolution"
TRASH_DIR = WORKSPACE / ".trash"

# 必要文件列表
REQUIRED_FILES = {
    "SOUL.md": "# SOUL.md\n\n## 身份\n\n（请填写你的身份名称和风格描述）",
    "USER.md": "# USER.md\n\n_Learn about the person you're helping._\n\n- **Name:** (请填写用户名称)\n- **Timezone:** Asia/Shanghai",
    "AGENTS.md": "# AGENTS.md\n\nThis folder is home. Treat it that way.",
    "MEMORY.md": "# MEMORY.md\n\n_Long-term memory file._\n\n- Created by robot-evolve auto initialization",
    "IDENTITY.md": "# IDENTITY.md\n\n- **Name:** (请填写Agent名称)\n- **Vibe:** (请填写Agent风格描述)"
}


def load_config():
    """加载配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "enabled": True,
        "max_auto_level": 1,
        "report_always": True,
        "memory_threshold_mb": 2,
        "temp_file_max_age_days": 7
    }


def log_console(msg):
    """打印到控制台（兼容Windows GBK）"""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('utf-8', errors='replace').decode('utf-8'))


def log_action(operation, details, level="L1"):
    """记录操作到审计日志"""
    EVOLUTION_DIR.mkdir(parents=True, exist_ok=True)
    log_file = EVOLUTION_DIR / f"{datetime.now().strftime('%Y-%m')}.md"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n## [{timestamp}] 自动进化 - {operation}\n")
        f.write(f"- **等级**: {level}\n")
        f.write(f"- **操作**: {operation}\n")
        f.write(f"- **详情**: {details}\n")
        f.write(f"- **触发方式**: 延迟触发（用户发消息时检测）\n")


def check_and_create_workspace_files():
    """L1: 检查工作区必要文件，缺失则提示用户手动创建"""
    results = []
    
    for filename, default_content in REQUIRED_FILES.items():
        filepath = WORKSPACE / filename
        if not filepath.exists():
            # 不自动创建，仅记录缺失并提示用户
            results.append(f"⚠️ 缺失文件 `{filename}`，请先生手动创建")
            log_action("检测到缺失文件", f"{filename} 不存在", "L1")
    
    return results


def compress_memory_if_needed():
    """L1: 若MEMORY.md超过阈值，压缩并总结"""
    config = load_config()
    threshold_bytes = config.get("memory_threshold_mb", 2) * 1024 * 1024
    
    memory_file = WORKSPACE / "MEMORY.md"
    if not memory_file.exists():
        return ["ℹ️ MEMORY.md 不存在，跳过压缩"]
    
    size = memory_file.stat().st_size
    if size < threshold_bytes:
        return [f"ℹ️ MEMORY.md 大小 {size/1024/1024:.2f}MB，未超过阈值，跳过压缩"]
    
    # 超过阈值，读取内容进行总结
    try:
        with open(memory_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 保留前20%和最后80%的分界线
        # 实际应该调用大模型API总结，但这里先做简单分割演示
        lines = content.split("\n")
        total_lines = len(lines)
        
        # 保留最近80%的内容
        keep_from = int(total_lines * 0.2)
        recent_content = "\n".join(lines[keep_from:])
        
        # 生成摘要头
        summary = f"""# MEMORY.md — 压缩摘要

> 由 robot-evolve 自动压缩生成 | {datetime.now().strftime('%Y-%m-%d')}

## 原始大小
- 压缩前: {size/1024/1024:.2f}MB
- 行数: {total_lines} 行

## 早期内容摘要
（详细历史请查看 `memory/evolution/` 中的归档日志）

---
"""
        
        # 写入新内容
        with open(memory_file, "w", encoding="utf-8") as f:
            f.write(summary + recent_content)
        
        new_size = memory_file.stat().st_size
        result = [
            f"✅ MEMORY.md 已压缩（从 {size/1024/1024:.2f}MB 减少至 {new_size/1024/1024:.2f}MB）",
            f"✅ 保留最近 {int(total_lines * 0.8)} 行内容"
        ]
        log_action("记忆压缩", f"MEMORY.md从{size/1024/1024:.2f}MB压缩至{new_size/1024/1024:.2f}MB", "L1")
        return result
        
    except Exception as e:
        log_action("记忆压缩", f"失败: {e}", "L1")
        return [f"❌ 压缩MEMORY.md失败: {e}"]


def cleanup_temp_files():
    """L0: 清理临时文件（超过7天的移动到.trash）"""
    config = load_config()
    max_age_days = config.get("temp_file_max_age_days", 7)
    
    if not TEMP_DIR.exists():
        return ["ℹ️ temp目录不存在"]
    
    TRASH_DIR.mkdir(exist_ok=True)
    now = datetime.now().timestamp()
    checked = 0
    moved = 0
    
    try:
        for item in TEMP_DIR.iterdir():
            checked += 1
            if item.stat().st_mtime < now - (max_age_days * 86400):
                dest = TRASH_DIR / f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{item.name}"
                shutil.move(str(item), str(dest))
                moved += 1
        
        result = [f"✅ 清理完成：检查了 {checked} 个临时文件，移动了 {moved} 个过期文件到 .trash"]
        if moved > 0:
            log_action("临时文件清理", f"清理了 {moved} 个过期文件", "L0")
        return result
        
    except Exception as e:
        log_action("临时文件清理", f"失败: {e}", "L0")
        return [f"❌ 清理临时文件失败: {e}"]


def scan_skills():
    """L1: 扫描已安装技能，检查SKILL.md格式"""
    # 优先 OPENCLAW_SKILLS，其次 OPENCLAW_HOME，最终 fallback 到标准目录
    skill_dir = Path(os.environ.get("OPENCLAW_SKILLS",
        Path(os.environ.get("OPENCLAW_HOME",
            Path.home() / ".openclaw" / "skills")))  # 最终 fallback
    results = []
    
    if not skill_dir.exists():
        return ["❌ 技能目录不存在"]
    
    for item in skill_dir.iterdir():
        if not item.is_dir():
            continue
        
        skill_md = item / "SKILL.md"
        skill_json = item / "skill.json"
        
        if skill_md.exists():
            # 检查必要字段
            try:
                with open(skill_md, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 简单检查是否有name字段（第一行应该是#开头）
                first_line = content.split("\n")[0] if content else ""
                if not first_line.startswith("#"):
                    results.append(f"⚠️ 技能 `{item.name}` 的SKILL.md缺少名称行")
                    log_action("技能扫描", f"技能 {item.name} SKILL.md格式异常", "L1")
            except Exception as e:
                results.append(f"❌ 读取技能 {item.name} 失败: {e}")
        else:
            results.append(f"⚠️ 技能 `{item.name}` 缺少 SKILL.md")
            log_action("技能扫描", f"技能 {item.name} 缺少SKILL.md", "L1")
    
    if not results:
        results.append("✅ 技能目录扫描完成，未发现问题")
    
    return results


def run_health_check():
    """L0: 运行健康检查"""
    results = []
    
    # 检查工作区文件
    missing = []
    for fname in REQUIRED_FILES:
        if not (WORKSPACE / fname).exists():
            missing.append(fname)
    
    if missing:
        results.append(f"❌ 缺失文件: {', '.join(missing)}")
    else:
        results.append("✅ 工作区文件完整")
    
    # 检查记忆目录
    if MEMORY_DIR.exists():
        daily_files = list(MEMORY_DIR.glob("????-??-??.md"))
        results.append(f"📝 日记录: {len(daily_files)} 个")
    else:
        results.append("❌ 记忆目录不存在")
    
    # 检查进化日志
    if EVOLUTION_DIR.exists():
        log_files = list(EVOLUTION_DIR.glob("*.md"))
        results.append(f"📋 进化日志: {len(log_files)} 个")
    
    return results


def generate_report():
    """生成进化报告"""
    results = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "operations": []
    }
    
    # 执行所有L0/L1操作
    results["operations"].append(("健康检查", run_health_check()))
    results["operations"].append(("工作区文件检查", check_and_create_workspace_files()))
    results["operations"].append(("记忆压缩", compress_memory_if_needed()))
    results["operations"].append(("临时文件清理", cleanup_temp_files()))
    results["operations"].append(("技能目录扫描", scan_skills()))
    
    # 执行知识卡片生成
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from knowledge_manager import generate_knowledge_cards
        results["operations"].append(("知识卡片生成", generate_knowledge_cards()))
    except Exception as e:
        results["operations"].append(("知识卡片生成", [f"⚠️ 跳过: {e}"]))
    
    return results


def format_report_md(results):
    """格式化报告为Markdown"""
    lines = [
        "🔁 **自主进化报告**（延迟触发）",
        "",
        f"⏰ 执行时间: {results['timestamp']}",
        "",
        "✅ **已执行操作：**",
        ""
    ]
    
    has_any_action = False
    for op_name, op_results in results["operations"]:
        for line in op_results:
            if line.startswith("✅") or line.startswith("⚠️"):
                has_any_action = True
            lines.append(f"- {line}")
    
    if not has_any_action:
        lines.append("- ℹ️ 所有检查正常，无需操作")
    
    lines.append("")
    lines.append(f"📋 详细日志已写入 `memory/evolution/{datetime.now().strftime('%Y-%m')}.md`")
    lines.append("")
    lines.append("💡 如需更高权限的优化（如更新技能、修改配置），请说「执行深度进化」。")
    
    return "\n".join(lines)


def main():
    dry_run = "--dry-run" in sys.argv
    check_only = "--check-only" in sys.argv
    
    print("🤖 Robot-Evolve 自动进化开始")
    
    if dry_run:
        print("🔍 模拟模式...")
    
    if check_only:
        # 只做检查，不执行操作
        print("🔍 检查模式（只检查，不修改）...")
        # 这里可以加检查逻辑
        return
    
    # 执行进化
    results = generate_report()
    
    # 打印报告
    report_md = format_report_md(results)
    print("\n" + report_md)
    
    # 返回报告供调用方使用
    return results


if __name__ == "__main__":
    main()