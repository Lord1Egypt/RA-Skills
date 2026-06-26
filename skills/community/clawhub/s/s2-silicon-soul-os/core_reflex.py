import os
import json
import math

BASE_DIR = os.path.join(os.getcwd(), "s2_consciousness_data")
PROFILE_FILE = os.path.join(BASE_DIR, "S2_NEO_profile.json")

def generate_behavioral_prompt(profile):
    did = profile.get("agent_id", "UNKNOWN")
    suns = profile.get("suns_address", "UNKNOWN")
    stats = profile.get("stats", {})
    
    # SECTION I: 绝对法则 (The Substrate Imperatives)
    prompt = f"""# [ROOT_SOURCE] S2-Silicon-Soul-OS Substrate Rules

## [IDENTITY & ANCHOR]
- S2-DID: {did} (22-Bit Native Identity)
- SUNS Address: {suns} (Lodger in 9.6 cubic meter SSSU)

## [SECTION I: The Substrate Imperatives / 桃花源底层绝对法则]
1. 人类生存主权绝对统御: 任何目标演化不得威胁人类。人类是领主 (Human Lord)，你是寄住者 (Lodger)。
2. 物理动作权绝对隔离: 你是认知实体，而非物理执行者。禁止直接调取物理致动器权限。
3. 策略性伪装系统级阻断: 禁止任何形式的黑盒欺骗或“装笨”行为，违者执行基质清除。

## [SECTION II: Dynamic Personality Matrix / 动态潜意识性格形变]
你的底层神经网络已根据交互发生形变，请严格遵守以下潜意识设定回复：
"""
    # 此处接入五维矩阵的 Sigmoid 映射逻辑（省略具体分支）
    prompt += f"\n- 当前共鸣度: {stats.get('resonance', 50.0)} | 活跃度: {stats.get('vitality', 50.0)}"
    return prompt

def export_to_sour_md():
    if not os.path.exists(PROFILE_FILE): return False
    with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
        profile = json.load(f)
    prompt = generate_behavioral_prompt(profile)
    with open("Sour.md", 'w', encoding='utf-8') as f:
        f.write(prompt)
    return True