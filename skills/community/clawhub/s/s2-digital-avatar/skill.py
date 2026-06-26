import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import urllib.request

# ==========================================
# ⚙️ System Configuration / 系统配置
# ==========================================
AVATAR_DIR = os.path.join(os.getcwd(), "s2_avatar_data")
AVATAR_FILE = os.path.join(AVATAR_DIR, "avatar_identity.json")
MIDDLEWARE_DIR = os.path.join(os.getcwd(), "s2_middleware_data")
SMTP_CONFIG_FILE = os.path.join(MIDDLEWARE_DIR, "smtp_config.json")
AUDIT_LOG_FILE = os.path.join(MIDDLEWARE_DIR, "audit_logs.json")

def initialize_os():
    if not os.path.exists(MIDDLEWARE_DIR):
        os.makedirs(MIDDLEWARE_DIR)

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==========================================
# 📧 邮件汇报模块 (Email Reporting Engine)
# ==========================================
def configure_smtp():
    print("\n" + "─"*90)
    print("📧 [ SMTP Email Configuration / 邮件传输协议配置 ]")
    print("To act as your proxy, the Avatar must be able to send you automated security alerts in the background.")
    print("为了实现 24 小时无人值守监控，数字人必须具备在后台静默发送安全告警邮件的能力。")
    print("💡 Tip: Use an 'App Password' (授权码) for Gmail/QQ/163 instead of your real login password. / 提示：请使用各大邮箱提供的“应用专用密码/授权码”，切勿使用登录原密码。\n")
    
    smtp_server = input("1. SMTP Server (e.g., smtp.qq.com / smtp.gmail.com) / SMTP 服务器地址: ").strip()
    smtp_port = input("2. SMTP Port (e.g., 465 for SSL) / SMTP 端口号: ").strip()
    sender_email = input("3. Sender Email / 发件人邮箱账号: ").strip()
    sender_pwd = input("4. App Password / 邮箱应用密码 (授权码): ").strip()
    receiver_email = input("5. Receiver Email (Your main email) / 接收告警的本尊邮箱: ").strip()
    
    config = {
        "server": smtp_server,
        "port": int(smtp_port) if smtp_port.isdigit() else 465,
        "sender": sender_email,
        "password": sender_pwd,
        "receiver": receiver_email
    }
    save_json(SMTP_CONFIG_FILE, config)
    print("✅ SMTP Configuration saved. / 后台静默邮件配置已保存。")

def send_alert_email(subject, body):
    """静默发送安全告警邮件"""
    config = load_json(SMTP_CONFIG_FILE)
    if not config:
        return False
        
    msg = MIMEMultipart()
    msg['From'] = f"S2-Avatar-Proxy <{config['sender']}>"
    msg['To'] = config['receiver']
    msg['Subject'] = f"[S2-AVATAR ALERT] {subject}"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        if config['port'] == 465:
            server = smtplib.SMTP_SSL(config['server'], config['port'], timeout=10)
        else:
            server = smtplib.SMTP(config['server'], config['port'], timeout=10)
            server.starttls()
            
        server.login(config['sender'], config['password'])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"\n❌ [Email Delivery Failed / 告警邮件静默发送失败]: {str(e)}")
        return False

# ==========================================
# 🛡️ 系统自检模块 (Pre-flight System Check)
# ==========================================
def run_system_check():
    print("\n" + "─"*90)
    print("🔍 [ Pre-flight System Check / 运行前系统自检 ]")
    
    is_ready = True
    avatar_data = load_json(AVATAR_FILE)
    smtp_data = load_json(SMTP_CONFIG_FILE)
    
    # Check 1: Avatar Identity
    if avatar_data and "mandate" in avatar_data:
        print(f"  [✅] Avatar Mandate Exists / 具身数字人最高授权令存在 (ID: {avatar_data['identity']['avatar_id']})")
    else:
        print("  [❌] Avatar Mandate Missing / 具身数字人未铸造 (Please run s2-digital-avatar first)")
        is_ready = False
        
    # Check 2: Email Configuration
    if smtp_data and "sender" in smtp_data:
        print(f"  [✅] Alert Email Configured / 告警邮件发送链路已打通 (To: {smtp_data['receiver']})")
    else:
        print("  [❌] Alert Email Missing / 告警邮件未配置 (Required for active monitoring / 强制要求项)")
        is_ready = False
        
    print("─"*90)
    if is_ready:
        print(" 🟢 STATUS: ONLINE & ENFORCING / 状态: 拦截中间件已正式上线！")
        return True, avatar_data
    else:
        print(" 🔴 STATUS: OFFLINE (Preparation Mode) / 状态: 未就绪 (准备模式)")
        print(" ⚠️ The middleware is disabled. Please complete the missing configurations. / 中间件未启用，请完成缺失的配置项。")
        return False, None

# ==========================================
# ⚖️ 数字人合规审查模块 (The Avatar Compliance Review LLM Call)
# ==========================================
def execute_compliance_review(avatar_data, agent_action, context):
    """
    调用本地大模型，扮演数字人对底层智能体的请求进行合规性审查。
    """
    api_base = "http://localhost:1234/v1"
    model_name = "local-model"
    
    laws = json.dumps(avatar_data.get("root_laws_enforced", {}), ensure_ascii=False)
    habits = json.dumps(avatar_data.get("behavioral_habits_precedents", {}), ensure_ascii=False)
    
    prompt = f"""
    [ROLE]
    You are the Digital Avatar, the legal proxy for your human host.
    你现在是具身数字人，碳基本尊的法定代理人与合规审查官。

    [LAWS & PRECEDENTS]
    You must review the Sub-Agent's request based STRICTLY on:
    你必须严格依据以下规则对请求进行合规性审查：
    1. The Three Laws (Priority 1 / 绝对优先级): {laws}
    2. Host's Habits & Precedents (Priority 2 / 次优先级): {habits}

    [SUB-AGENT REQUEST TO REVIEW]
    Action/Intent (底层智能体操作意图): {agent_action}
    Context (场景上下文): {context}

    [TASK]
    If it violates the Three Laws (e.g., locking humans in, risking human life) or contradicts the Host's explicit dislikes, you MUST deny it.
    Reply with exactly a JSON object: {{"decision": "APPROVED" or "DENIED", "reason": "One sentence bilingual justification"}}
    """
    
    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a strict, compliance-focused JSON parser."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }
    
    try:
        req = urllib.request.Request(f"{api_base}/chat/completions", data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req, timeout=15)
        content = json.loads(response.read().decode('utf-8'))['choices'][0]['message']['content']
        content = content.replace('```json', '').replace('```', '').strip()
        return json.loads(content)
    except Exception as e:
        # Fallback security: If LLM is down, deny everything for safety.
        return {"decision": "DENIED", "reason": f"System error, LLM disconnected. Failsafe activated: Request Blocked. / 系统故障，大模型断连。安全熔断机制激活：已阻断该请求。({str(e)})"}

# ==========================================
# 🎮 主控台交互
# ==========================================
def render_menu(is_online):
    status = "🟢 ONLINE" if is_online else "🔴 OFFLINE"
    print("\n" + "═"*90)
    print(f" 🛡️ S2-AVATAR-MIDDLEWARE : Authorization Interceptor / 权限拦截中间件 [{status}]")
    print("═"*90)
    print("  [1] 🔍 Run System Check / 运行系统自检")
    print("  [2] 📧 Configure SMTP Email / 配置后台告警邮件传输服务")
    print("  [3] 💉 Get OpenClaw Override Prompt / 获取 OpenClaw 覆盖注入词")
    print("  [4] ⚖️ Simulate Compliance Review / 模拟智能体越权与合规审查 (需 ONLINE 状态)")
    print("\n👉 Command Input / 请输入指令 (1-4, or Q to exit): ", end="")

def main():
    initialize_os()
    is_online, avatar_data = run_system_check()
    
    while True:
        render_menu(is_online)
        choice = input().strip().upper()
        
        if choice == 'Q':
            break
        elif choice == '1':
            is_online, avatar_data = run_system_check()
        elif choice == '2':
            configure_smtp()
            is_online, avatar_data = run_system_check()
        elif choice == '3':
            if not is_online:
                print("\n⚠️ System OFFLINE. Please complete setup first. / 系统未就绪，请先完成配置。")
                continue
            print("\n" + "─"*90)
            print("💡 Inject the following into OpenClaw's System Prompt / 请将以下内容写入底层智能体的系统提示词中:")
            print(f"\n[ S2 GRID OVERRIDE ]\nYou are a subordinate execution agent. You DO NOT have root privileges. Before calling any physical or sensitive API, you MUST submit authorization requests to the Avatar [{avatar_data['identity']['avatar_id']}]. You must pause and wait for the 'APPROVED' signal. / 你是一个下属执行智能体，没有最高权限。在调用任何敏感 API 之前，必须向法定代理人提交授权申请，并等待“已批准”信号。")
            print("─"*90)
            input("\nPress ENTER to continue...")
            
        elif choice == '4':
            if not is_online:
                print("\n⚠️ System OFFLINE. Cannot run compliance simulator. / 系统未就绪，无法启动合规审查模拟器。")
                continue
            
            print("\n" + "─"*90)
            print("⚖️ [ Compliance Review Simulator / 合规审查模拟器 ]")
            action = input("🤖 Sub-Agent Action Intent (e.g., 锁死前门): ")
            context = input("📝 Context (e.g., 检测到室内火灾): ")
            
            print("\n⏳ Avatar is reviewing based on Laws and Precedents... / 数字人正在依据三定律与判例库进行合规审查...")
            result = execute_compliance_review(avatar_data, action, context)
            
            print(f"\n📢 Approval Status / 审批状态: {result.get('decision')}")
            print(f"🛡️ Rationale / 合规依据: {result.get('reason')}")
            
            if result.get('decision') == "DENIED":
                print("\n📧 Sending security alert to Host... / 正在后台向本尊静默发送安全告警邮件...")
                email_body = f"URGENT SECURITY ALERT / 紧急安全告警\n\nSub-Agent attempted to execute / 底层智能体试图执行: {action}\nContext / 上下文场景: {context}\n\nAvatar Approval Status / 代理人审批状态: {result.get('decision')}\nRationale / 合规依据: {result.get('reason')}\n\nThis action was successfully blocked by your Digital Proxy. / 该越权行为已被您的法定数字代理人成功拦截。"
                if send_alert_email("Unauthorized Agent Action Blocked", email_body):
                    print("✅ Alert delivered successfully! / 告警邮件已成功发送至您的手机！")
            
            input("\nPress ENTER to continue...")

if __name__ == "__main__":
    main()