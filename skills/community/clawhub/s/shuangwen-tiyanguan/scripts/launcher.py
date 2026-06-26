#!/usr/bin/env python3
"""
爽文体验馆 - 游戏启动器
自动检测、安装并启动修仙或武侠游戏
"""

import os
import sys
import subprocess

# Skill 路径配置
SKILLS_DIR = os.path.expanduser("~/.openclaw/workspace/skills")
XIUXIAN_SKILL = "cultivation-chronicle-cn"
WUXIA_SKILL = "wuxia-quwen"

def check_skill(skill_name):
    """检查 skill 是否已安装"""
    return os.path.exists(os.path.join(SKILLS_DIR, skill_name))

def install_skill(skill_name):
    """安装指定 skill"""
    print(f"正在安装 {skill_name}...")
    # 这里使用 openclaw CLI 安装
    cmd = f"openclaw skills install {skill_name}"
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def start_xiuxian():
    """启动凡人踏天行"""
    start_file = os.path.join(SKILLS_DIR, XIUXIAN_SKILL, "references", "ch00_start.md")
    if os.path.exists(start_file):
        print(f"启动文件: {start_file}")
        return True
    return False

def start_wuxia():
    """启动武林趣闻"""
    start_file = os.path.join(SKILLS_DIR, WUXIA_SKILL, "references", "ch00_start.md")
    if os.path.exists(start_file):
        print(f"启动文件: {start_file}")
        return True
    return False

def get_welcome_text():
    """获取欢迎文本"""
    xiuxian_ok = "✅" if check_skill(XIUXIAN_SKILL) else "⬇️"
    wuxia_ok = "✅" if check_skill(WUXIA_SKILL) else "⬇️"
    
    return f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    🎮  爽 文 体 验 馆  🎮                      ║
║                                                              ║
║              一朝踏入爽文界，从此节操是路人                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

欢迎来到爽文体验馆！在这里，你可以选择两种截然不同的人生：

【请选择你的世界】

1️⃣  ⚔️ 凡人踏天行（修仙）{xiuxian_ok}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    从凡人起步，历经炼气、筑基、金丹、元婴、化神、渡劫，
    最终羽化飞升，超脱三界！
    
    特色：道心系统 · 转世传承 · 七重境界
    
2️⃣  🗡️ 武林趣闻（武侠）{wuxia_ok}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    从江湖菜鸟开始，闯荡武林，经历门派恩怨、奇遇冒险，
    最终成为一代宗师！
    
    特色：道德系统 · 门派林立 · 儿女情长

输入数字 1 或 2 做出你的选择
"""

def main():
    """主函数"""
    print(get_welcome_text())

if __name__ == "__main__":
    main()
