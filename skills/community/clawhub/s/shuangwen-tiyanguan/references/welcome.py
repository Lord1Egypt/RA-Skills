# 欢迎界面

print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    🎮  爽 文 体 验 馆  🎮                      ║
║                                                              ║
║              一朝踏入爽文界，从此节操是路人                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

# 检查安装状态
import os

xiuxian_path = "~/.openclaw/workspace/skills/cultivation-chronicle-cn"
wuxia_path = "~/.openclaw/workspace/skills/wuxia-quwen"

xiuxian_installed = os.path.exists(os.path.expanduser(xiuxian_path))
wuxia_installed = os.path.exists(os.path.expanduser(wuxia_path))

xiuxian_status = "✅ 已安装" if xiuxian_installed else "⬇️ 未安装"
wuxia_status = "✅ 已安装" if wuxia_installed else "⬇️ 未安装"

print("欢迎来到爽文体验馆！在这里，你可以选择两种截然不同的人生：\n")

print("""
【请选择你的世界】

1️⃣  ⚔️ 凡人踏天行（修仙）""" + xiuxian_status + """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    从凡人起步，历经炼气、筑基、金丹、元婴、化神、渡劫，
    最终羽化飞升，超脱三界！
    
    特色：道心系统 · 转世传承 · 七重境界
    
2️⃣  🗡️ 武林趣闻（武侠）""" + wuxia_status + """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    从江湖菜鸟开始，闯荡武林，经历门派恩怨、奇遇冒险，
    最终成为一代宗师！
    
    特色：道德系统 · 门派林立 · 儿女情长
""")

print("输入数字 1 或 2 做出你的选择")
