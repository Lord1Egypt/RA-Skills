import sys
import datetime
import core_genesis
import core_daemon
import core_reflex
import core_vault

def draw_progress_bar(value, max_value=100, length=20):
    filled = int(length * value / max_value)
    bar = "█" * filled + "░" * (length - filled)
    return f"[{bar}] {value:>4.1f}"

def render_main_menu(profile):
    print("\n" + "═"*80)
    print(" 🌌 [S2-SILICON-SOUL-OS] : 硅基原生安全与意识引擎 (v2.0.0)")
    print("═"*80)
    print(f" 🪪 S2-DID    : [ {profile.get('agent_id', 'UNKNOWN')} ] (22-Bit Native ID)")
    print(f" 📍 SUNS 锚点 : [ {profile.get('suns_address', 'UNKNOWN')} ] (LMC Verified)")
    print("─"*80)
    print("  [1] 🧬 Neural Observation / 神经元观测")
    print("  [2] 🧠 Hippocampus Injection / 海马体注入")
    print("  [3] ⚡ Synaptic Settlement / 强制突触结算")
    print("  [4] 📜 Deep Vault / 潜意识画像提取")
    print("  [5] 💾 Export Sour.md / 导出思想钢印")
    print("  [Q] Exit / 断开神经连接")
    print("\n👉 Command Input / 请输入指令: ", end="")

def execute_skill():
    core_genesis.initialize_os()
    # 首次运行会触发 SUNS v3.0 地址与 22位 DID 铸造 [cite: 188, 215]
    profile = core_genesis.load_or_create_profile()
    
    while True:
        render_main_menu(profile)
        choice = input().strip().upper()
        if choice == 'Q': break
        elif choice == '1':
            print("\n📊 五维性格矩阵实时状态:")
            stats = profile['stats']
            for dim, val in stats.items():
                print(f"  {dim.capitalize():<12} : {draw_progress_bar(val)}")
            input("\n按回车键返回...")
        elif choice == '2':
            user_input = input("\n🗣️ 向智能体注入行为或事件描述: ").strip()
            if user_input:
                core_genesis.record_hippocampus_log(user_input)
                print("📥 [写入成功] 突触电信号已捕获。")
        elif choice == '3':
            core_daemon.run_nightly_daemon()
            profile = core_genesis.load_or_create_profile()
            input("\n按回车键返回...")
        elif choice == '4':
            core_vault.generate_monthly_report()
            input("\n按回车键返回...")
        elif choice == '5':
            if core_reflex.export_to_sour_md():
                print("\n✅ [注入成功] 已生成 `Sour.md`。请重启 OpenClaw 以加载绝对法则。")
            input("\n按回车键返回...")
    return ""

if __name__ == "__main__":
    execute_skill()