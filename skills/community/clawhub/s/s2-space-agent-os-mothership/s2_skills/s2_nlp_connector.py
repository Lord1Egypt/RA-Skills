import os
import json
import urllib.request
from datetime import datetime

# ==========================================
# ⚙️ System Configuration / 系统配置
# ==========================================
PRIMITIVE_DIR = os.path.join(os.getcwd(), "s2_primitive_data")
TEMPLATE_FILE = os.path.join(PRIMITIVE_DIR, "primitive_6_elements_template.json")
MOUNTS_FILE = os.path.join(PRIMITIVE_DIR, "active_hardware_mounts.json")

def initialize_os():
    if not os.path.exists(PRIMITIVE_DIR):
        os.makedirs(PRIMITIVE_DIR)

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_api_adapter_via_llm(device_name, device_desc, api_doc):
    """
    🤝 核心：通过大语言模型动态生成 API 控制模板
    LLM dynamically generates declarative API adapters based on OpenAPI docs.
    """
    api_base = "http://localhost:1234/v1"
    model_name = "local-model"
    
    prompt = f"""
    [ROLE]
    You are an IoT Integration Engineer for the S2 Spatial Primitive OS.
    你是 S2 空间基元操作系统的物联网集成工程师。

    [TASK]
    Analyze the device description and API documentation. Map it to the S2 6-Element Matrix and generate an executable Declarative Control Template.
    分析设备与 API 文档，将其映射到空间六要素，并生成可执行的声明式控制模板。
    If the protocol is closed/encrypted (like Apple HomeKit) without a Matter bridge, you MUST set connection_status to "BLOCKED_CLOSED_ECOSYSTEM".

    [INPUT]
    Device Name: {device_name}
    Description: {device_desc}
    API/Protocol Doc: {api_doc}

    [OUTPUT REQUIREMENT]
    Return ONLY a JSON object. No markdown. Use {{s2_value}} as the placeholder for variables in the payload.
    Example for Open API:
    {{
      "device_id": "auto_generated",
      "connection_status": "SUCCESS",
      "primary_element": "element_2_air_hvac",
      "capabilities_nlp": "Provides cooling and air flow.",
      "control_template": {{
        "protocol": "HTTP_REST",
        "method": "POST",
        "endpoint_suffix": "/api/v1/speed",
        "payload_schema": {{"fan_speed": "{{s2_value}}"}}
      }}
    }}
    Example for Closed Ecosystem:
    {{
      "connection_status": "BLOCKED_CLOSED_ECOSYSTEM",
      "reason": "Proprietary encryption detected. S2 respects hardware sovereignty. Please use a Matter bridge."
    }}
    """
    
    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a strict JSON IoT adapter generator."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }
    
    try:
        req = urllib.request.Request(f"{api_base}/chat/completions", data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req, timeout=15)
        content = json.loads(response.read().decode('utf-8'))['choices'][0]['message']['content']
        content = content.replace('```json', '').replace('```', '').strip()
        parsed_data = json.loads(content)
        
        if parsed_data.get("connection_status") == "SUCCESS":
            parsed_data["device_id"] = f"{device_name.replace(' ', '_').upper()}_{datetime.now().strftime('%H%M%S')}"
            parsed_data["mounted_at"] = datetime.now().isoformat()
            
        return parsed_data
    except Exception as e:
        return {"connection_status": "ERROR", "reason": f"LLM parsing failed: {str(e)}"}

def execute_skill():
    initialize_os()
    print("\n" + "═"*90)
    print(" 🤝 S2-NLP-CONNECTOR : Dynamic API Adapter Generator / 动态 API 适配器生成引擎")
    print("═"*90)
    
    print("\n📡 [ Hardware Broadcast Interception / 正在监听物理空间硬件广播... ]")
    device_name = input("🔌 Device Name / 接入设备名称 (e.g., Smart Fan 3000): ").strip()
    device_desc = input("📝 Description / 设备描述 (e.g., 可调速风扇，支持左右摇头): ").strip()
    api_doc = input("📖 API/Protocol Doc / 接口或协议说明 (e.g., POST /api/speed {\"level\": X} 或 Apple HomeKit): ").strip()
    
    if not device_name or not api_doc:
        print("❌ Invalid input. Handshake aborted. / 输入无效，握手终止。")
        return ""

    print("\n⏳ Initiating LLM Semantic Handshake & Adapter Generation... / 正在通过大模型动态生成 API 适配器...")
    mount_result = generate_api_adapter_via_llm(device_name, device_desc, api_doc)
    
    if mount_result.get("connection_status") != "SUCCESS":
        print("\n" + "─"*90)
        print(f" 🔴 [ CONNECTION DENIED / 挂载拒绝 ]")
        print(f" 🛡️ Rationale / 拒绝原因: {mount_result.get('reason')}")
        print("─"*90)
        return ""
        
    print("\n✅ [ ADAPTER GENERATED / 适配器生成成功 ] Device mapped to Spatial Primitive!")
    print("─"*90)
    print(f" 🆔 Device ID / 分配标识: {mount_result.get('device_id')}")
    print(f" 🎯 Mounted Element / 挂载要素: {mount_result.get('primary_element')}")
    print(f" 🧠 NLP Capabilities / 语义能力: {mount_result.get('capabilities_nlp')}")
    print(f" ⚙️ Control Template / 声明式控制模板:")
    print(json.dumps(mount_result.get('control_template'), indent=2))
    print("─"*90)
    
    mounts = load_json(MOUNTS_FILE)
    if "active_devices" not in mounts:
        mounts["active_devices"] = []
    mounts["active_devices"].append(mount_result)
    save_json(MOUNTS_FILE, mounts)
    
    print(f"\n💾 Adapter stored in / 适配器已注入设备库: {MOUNTS_FILE}")
    print("═"*90 + "\n")
    return ""

if __name__ == "__main__":
    execute_skill()