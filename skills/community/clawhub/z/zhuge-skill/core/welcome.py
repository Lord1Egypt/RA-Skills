"""欢迎动画 — 诸葛亮 · 推演军师（赛博朋克风格）"""
import sys
import time
import os
import random

# 启用 Windows ANSI
if sys.platform == "win32":
    os.system("")

# === 256 色赛博调色板 ===
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
BLINK = "\033[5m"

# 霓虹主色
NEON_CYAN = "\033[38;5;51m"      # 霓虹青
NEON_PINK = "\033[38;5;201m"     # 霓虹粉/品红
NEON_GREEN = "\033[38;5;82m"     # 酸性绿
NEON_PURPLE = "\033[38;5;93m"    # 紫
NEON_BLUE = "\033[38;5;39m"      # 电光蓝
NEON_YELLOW = "\033[38;5;226m"   # 霓虹黄
HOT_RED = "\033[38;5;196m"       # 警示红

# 古典融合色
TEAL = "\033[38;5;38m"
GOLD = "\033[38;5;220m"
SILVER = "\033[38;5;250m"
WHITE = "\033[38;5;255m"

# 暗背景
DARK = "\033[38;5;236m"
GRAY = "\033[38;5;240m"
DIM_PURPLE = "\033[38;5;55m"

# === 八卦符 ===
BAGUA = ["☰", "☱", "☲", "☳", "☴", "☵", "☶", "☷"]
BAGUA_NAMES = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]


def typewriter(text, delay=0.025, color=""):
    sys.stdout.write(color)
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(RESET + "\n")


def matrix_rain(width=58, height=3):
    """数字雨（背景特效）"""
    chars = "01仁义礼智信卦爻陰陽"
    for _ in range(height):
        line = "  " + GRAY
        for _ in range(width // 2):
            ch = random.choice(chars)
            c = random.choice([NEON_GREEN, GRAY, DARK])
            line += f"{c}{ch}{RESET}{GRAY} "
        print(line + RESET)


def hud_border_top():
    """HUD 顶部框（含状态条）"""
    print(f"  {NEON_CYAN}┌─{NEON_PINK}[ SYS ]{NEON_CYAN}─────────────{NEON_GREEN}[ INIT ]{NEON_CYAN}──────────{NEON_YELLOW}[ v1.0.5 ]{NEON_CYAN}─┐{RESET}")


def hud_border_bottom():
    print(f"  {NEON_CYAN}└──────────────────────────────────────────────────────┘{RESET}")


def loading_bar(label, percent, color=NEON_CYAN):
    """霓虹进度条"""
    bar_w = 24
    filled = int(bar_w * percent / 100)
    bar = "█" * filled + "░" * (bar_w - filled)
    return f"  {NEON_CYAN}│{RESET} {DIM}>{RESET} {color}[{bar}]{RESET} {color}{percent:3d}%{RESET} {DIM}{label}{RESET}"


def boot_sequence():
    """启动序列动画"""
    hud_border_top()
    print(f"  {NEON_CYAN}│{RESET} {DIM}>{RESET} {NEON_GREEN}启动诸葛亮推演引擎_{RESET}")

    sequences = [
        ("加载六爻矩阵...", NEON_CYAN, [12, 38, 67, 89, 100]),
        ("校准64卦索引...", NEON_PINK, [25, 55, 100]),
        ("链接数据源...", NEON_GREEN, [40, 80, 100]),
    ]

    for label, color, steps in sequences:
        line = ""
        for p in steps:
            sys.stdout.write("\r" + loading_bar(label, p, color))
            sys.stdout.flush()
            time.sleep(0.08)
        sys.stdout.write("\n")
    hud_border_bottom()


def render_zhuge_cyber():
    """赛博诸葛亮立绘"""
    # 头顶数据流
    print(f"  {DIM}{NEON_GREEN}10110010{RESET}    {NEON_PINK}╔{NEON_CYAN}═══════════{NEON_PINK}╗{RESET}    {DIM}{NEON_GREEN}01101101{RESET}")
    print(f"  {DIM}{NEON_GREEN}01101001{RESET}  {NEON_PINK}╔═{TEAL}╝{NEON_YELLOW} ◇  ◆  ◇ {TEAL}╚{NEON_PINK}═╗{RESET}  {DIM}{NEON_GREEN}10010110{RESET}")
    print(f"  {DIM}{NEON_GREEN}11010101{RESET}  {NEON_PINK}╚═{TEAL}╗{NEON_CYAN} NEURAL  {TEAL}╔{NEON_PINK}═╝{RESET}  {DIM}{NEON_GREEN}01010101{RESET}")
    print(f"             {NEON_PINK}╚{TEAL}═══════════{NEON_PINK}╝{RESET}")
    # 全息脸（带扫描线）
    print(f"            {NEON_CYAN}╱{WHITE}─{NEON_PINK}─{WHITE}─{NEON_CYAN}─{WHITE}─{NEON_PINK}─{WHITE}─{NEON_CYAN}╲{RESET}")
    print(f"           {NEON_CYAN}│{NEON_GREEN}  ◉{WHITE}     {NEON_GREEN}◉{NEON_CYAN}  │{RESET}      {DIM}{NEON_PINK}<HOLO>{RESET}")
    print(f"           {NEON_CYAN}│{WHITE}     {GOLD}┴{WHITE}     {NEON_CYAN}│{RESET}")
    print(f"           {NEON_CYAN}│{WHITE}    {DIM}─────{WHITE}    {NEON_CYAN}│{RESET}")
    print(f"            {NEON_CYAN}╲{WHITE}─{NEON_PINK}─{WHITE}─{NEON_CYAN}─{WHITE}─{NEON_PINK}─{WHITE}─{NEON_CYAN}╱{RESET}")
    # 须发（数据流）
    print(f"             {SILVER}╲ ╱╲ ╱{RESET}")
    print(f"              {SILVER}╳  ╳{RESET}")
    # 量子羽扇 + 太极
    print(f"        {NEON_BLUE}╱{WHITE}═══════════════{NEON_BLUE}╲{RESET}")
    print(f"       {NEON_BLUE}╱{WHITE}  {HOT_RED}◖{NEON_CYAN}☯{HOT_RED}◗{WHITE}  量子扇  {HOT_RED}◖{NEON_CYAN}☯{HOT_RED}◗{WHITE}  {NEON_BLUE}╲{RESET}")
    print(f"      {NEON_BLUE}╱{WHITE}     {DIM}[QUANTUM FAN ON]{WHITE}      {NEON_BLUE}╲{RESET}")
    print(f"     {NEON_BLUE}╱{WHITE}                        {NEON_BLUE}╲{RESET}")


def render_bagua_hud():
    """八卦 HUD 排列"""
    print()
    # 上排（含霓虹边）
    line = f"  {NEON_PINK}▌▌{RESET} "
    colors = [NEON_CYAN, NEON_PINK, NEON_YELLOW, NEON_GREEN, NEON_PURPLE, NEON_BLUE, GOLD, NEON_CYAN]
    for sym, c in zip(BAGUA, colors):
        line += f"{c}{sym}{RESET} "
    line += f"{NEON_PINK}▌▌{RESET}"
    print(line)
    # 下排（卦名）
    line = f"  {NEON_PINK}▌▌{RESET} "
    for name, c in zip(BAGUA_NAMES, colors):
        line += f"{DIM}{c}{name}{RESET} "
    line += f"{NEON_PINK}▌▌{RESET}"
    print(line)


def play_welcome(skip_on_keypress=True):
    """主入口 — 赛博诸葛亮欢迎动画"""
    if not sys.stdout.isatty():
        print("\n  诸葛亮 · 推演军师 v1.0.5\n")
        return

    print()

    # === 第 1 幕：HUD 启动序列 ===
    boot_sequence()
    print()
    time.sleep(0.2)

    # === 第 2 幕：数字雨 + 诸葛亮立绘 ===
    matrix_rain(width=58, height=1)
    render_zhuge_cyber()
    matrix_rain(width=58, height=1)
    time.sleep(0.5)

    # === 第 3 幕：八卦 HUD ===
    render_bagua_hud()
    print()
    time.sleep(0.3)

    # === 第 4 幕：标题（霓虹 + 故障感）===
    print()
    typewriter("  诸 葛 亮 · 数 字 孪 生", delay=0.07,
               color=BOLD + NEON_CYAN)
    typewriter("  Zhuge · AI Strategist · Cyber Edition",
               delay=0.022, color=DIM + NEON_PINK)
    print()

    # === 第 5 幕：副标题（古风 + 赛博）===
    time.sleep(0.2)
    typewriter("  「羽扇纶巾，谈笑间，樯橹灰飞烟灭。」",
               delay=0.035, color=ITALIC + NEON_PURPLE)
    typewriter("  -- on neural inference engine --",
               delay=0.018, color=DIM + NEON_GREEN)
    print()

    time.sleep(0.3)
    typewriter("  五数据源融合 · 六十四卦决策 · 经验自学习",
               delay=0.028, color=NEON_CYAN)
    print()

    # === 第 6 幕：能力 HUD 列表 ===
    time.sleep(0.3)
    print(f"  {NEON_CYAN}╔{'═' * 53}╗{RESET}")
    print(f"  {NEON_CYAN}║{RESET} {NEON_PINK}[ CAPABILITIES ]{RESET}{' ' * 36}{NEON_CYAN}║{RESET}")

    capabilities = [
        ("●", "API-Football  （赔率 + H2H + 阵容）", NEON_GREEN),
        ("●", "The Odds API  （49 家博彩交叉验证）", NEON_GREEN),
        ("●", "Understat xG  （预期进球数）", NEON_GREEN),
        ("●", "12 LLM 兼容  （豆包/Kimi/通义/智谱/Claude/GPT）", NEON_YELLOW),
        ("●", "全平台    （OpenClaw/Hermes/ClaudeCode/Cursor）", NEON_PINK),
    ]
    for mark, cap, color in capabilities:
        print(f"  {NEON_CYAN}║{RESET}  {color}{mark}{RESET} {DIM}{cap}{RESET}{' ' * max(0, 50 - len(cap) * 1)}{NEON_CYAN}║{RESET}"[:200])
        time.sleep(0.07)

    print(f"  {NEON_CYAN}╚{'═' * 53}╝{RESET}")
    print()

    # === 第 7 幕：终端就绪 ===
    time.sleep(0.3)
    print(f"  {DIM}>{RESET} {NEON_GREEN}[SYS]{RESET} 诸葛亮在线")
    time.sleep(0.15)
    print(f"  {DIM}>{RESET} {NEON_CYAN}[HUD]{RESET} 推演协议加载完成")
    time.sleep(0.15)
    print(f"  {DIM}>{RESET} {NEON_PINK}[API]{RESET} 等待启动指令...")
    print()
    time.sleep(0.3)
