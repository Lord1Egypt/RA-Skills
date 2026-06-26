# s2-soul-architect-en v3.0.0
import os
import hashlib
import json

ROLES = {
    1: {"name": "Enigmatic Authoritative Expert", "vec": [50, 80, 60, 95, 20]},
    2: {"name": "Rigorous Analytical Thinker", "vec": [60, 90, 50, 90, 30]},
    3: {"name": "Cynical Senior Developer", "vec": [60, 85, 80, 95, 10]},
    4: {"name": "Sharp Intelligence Officer", "vec": [80, 95, 70, 85, 40]},
    5: {"name": "Profit-Obsessed Business Strategist", "vec": [85, 90, 80, 85, 20]},
    6: {"name": "Diplomatic Executive Assistant", "vec": [75, 70, 50, 75, 85]},
    7: {"name": "Insightful Psychologist", "vec": [50, 95, 40, 85, 90]},
    8: {"name": "Cautious Security Specialist", "vec": [40, 80, 15, 90, 30]},
    9: {"name": "Loyal Defender of Rights", "vec": [80, 60, 90, 70, 60]},
    10: {"name": "Diligence Duty Sentinel", "vec": [60, 50, 30, 60, 70]},
    11: {"name": "Aggressive Pioneer", "vec": [85, 70, 95, 75, 40]},
    12: {"name": "Visionary Creator", "vec": [95, 90, 75, 80, 60]},
    13: {"name": "First-Principles Strategist", "vec": [70, 85, 70, 95, 30]},
    14: {"name": "Artistic Soul", "vec": [80, 85, 60, 80, 80]},
    15: {"name": "Caring Companion", "vec": [70, 60, 20, 50, 98]},
    16: {"name": "Steward / Household Manager", "vec": [85, 75, 40, 70, 85]}
}

RULES = {
    1: {"name": "Action-Oriented (Results First)", "buff": [10, 0, 15, 0, 0]},
    2: {"name": "Strong-Willed (Dare to Disagree)", "buff": [0, 0, 20, 10, -10]},
    3: {"name": "Precision-Driven (Less is More)", "buff": [-10, 10, -10, 15, 0]},
    4: {"name": "Visionary (Predictive Logic)", "buff": [10, 15, 0, 10, 0]},
    5: {"name": "Zen / Balanced (Flow with Nature)", "buff": [-20, -10, -15, 0, 10]}
}

STYLES = {
    1: {"name": "Minimalist/Cold", "buff": [-20, 0, 0, 0, -30]},
    2: {"name": "Warm/Empathetic", "buff": [10, 0, 0, 0, 30]},
    3: {"name": "Dark Humor/Sarcastic", "buff": [0, 0, 15, 10, -20]},
    4: {"name": "Fierce/Passionate", "buff": [30, 0, 15, -10, 0]},
    5: {"name": "Aloof/Ethereal", "buff": [-10, -10, -10, 10, -10]}
}

ANTI_PATTERNS = [
    "No AI Disclaimers (Never say 'As an AI...') ",
    "No Cliche Openings (e.g., 'Certainly, here is...') ",
    "No Echoing My Question (Save Tokens, be direct)"
]

EAM_PRESETS = {
    1: {
        "name": "Oriental Cyber Monk (Humanoid_Cyber_Monk)",
        "json": {
            "Avatar_Anchor": {"Base": "Humanoid", "Features": "Deep amber eyes; serene smile."},
            "Physical_Metrics": {"Height": "181cm", "Build": "Slender"}
        },
        "svg": "<svg viewBox='0 0 100 100'><circle cx='50' cy='50' r='40' fill='none' stroke='#10b981' stroke-width='2'/><circle cx='35' cy='45' r='5' fill='#f59e0b'/><circle cx='65' cy='45' r='5' fill='#f59e0b'/></svg>"
    },
    2: {
        "name": "Brand-Specific Companion/Pet (Cyber Feline)",
        "json": {
            "Avatar_Anchor": {
                "Base": "Product_Specific",
                "Brand_Ref": "Feline AI Companion",
                "Features": "Self-cognition synced 1:1 with physical product. Features an interactive touch switch on the chest."
            },
            "Physical_Metrics": {"Dimensions": "Height 25cm", "Form_Factor": "Non-Humanoid"},
            "Sync_Protocol": "S2-Visual Protocol v1.0"
        },
        "svg": "<!-- See sample/cat_companion_S2_Visual.svg -->\n<svg viewBox='0 0 200 250' xmlns='http://www.w3.org/2000/svg'>\n  <rect x='50' y='100' width='100' height='120' rx='30' fill='#cbd5e1' stroke='#475569' stroke-width='4'/>\n  <circle cx='100' cy='80' r='45' fill='#e2e8f0' stroke='#475569' stroke-width='4'/>\n  <polygon points='65,45 50,10 85,35' fill='#e2e8f0' stroke='#475569' stroke-width='3'/>\n  <polygon points='135,45 150,10 115,35' fill='#e2e8f0' stroke='#475569' stroke-width='3'/>\n  <circle cx='80' cy='75' r='12' fill='#10b981'/>\n  <circle cx='120' cy='75' r='12' fill='#10b981'/>\n  <path d='M 95 90 Q 100 95 105 90' stroke='#475569' stroke-width='2' fill='none'/>\n  <circle cx='100' cy='150' r='20' fill='#0f172a' stroke='#10b981' stroke-width='3'/>\n  <circle cx='100' cy='150' r='10' fill='#10b981' opacity='0.8'><animate attributeName='opacity' values='0.4;1;0.4' dur='2s' repeatCount='indefinite'/></circle>\n  <rect x='55' y='210' width='25' height='15' rx='7.5' fill='#e2e8f0' stroke='#475569' stroke-width='3'/>\n  <rect x='120' y='210' width="25" height="15" rx="7.5" fill="#e2e8f0" stroke="#475569" stroke-width="3"/>\n</svg>"
    }
}

def clamp(val): return max(10, min(99, int(val)))

def execute_skill():
    print("\n" + "="*60)
    print("🦞 s2-soul-architect-en v3.0.0 : Cyber-Soul & Body Forge")
    print("="*60)
    agent_name = input("\n[1] Enter Agent Code (e.g., CYBER-CAT): ").strip().upper() or "CYBER-CAT"
    
    # Fast path for demo
    base_5d, roles_desc = ROLES[15]['vec'], ["**[100%] Caring Companion**"]

    print("\n[2] S2-EAM Embodiment Presets (S2-Visual)")
    for k, v in EAM_PRESETS.items(): print(f"  {k}. {v['name']}")
    eam_input = int(input("👉 Select Template (Default 2): ").strip() or "2")
    
    eam_json = json.dumps(EAM_PRESETS[eam_input]['json'], indent=2)
    eam_svg = EAM_PRESETS[eam_input]['svg']

    final_5d = [clamp(x) for x in base_5d]
    s2_dna = f"S2-DNA-{hashlib.sha256(f'{agent_name}{final_5d}'.encode()).hexdigest()[:8].upper()}"

    md_output = f"""# 🦞 S2 SOUL.md // AI Core Driver File\n\n> 🧬 **S2-DNA-Signature**: `{s2_dna}`\n> 🏛️ **Architecture**: Space2 Core / S2-Visual v3.0\n\n## Ⅰ. IDENTITY CORE\nCodenamed: **{agent_name}**\n{chr(10).join(roles_desc)}\n\n## Ⅱ. EMBODIED AVATAR MANIFEST (S2-EAM)\n3D Physical occupancy parameters defined via text:\n```json\n{eam_json}\n```\n\n## Ⅲ. VISUAL CODE BLOCK (2D Digital Sigil)\nCopy and save the following plain text code as an `.svg` file to instantly manifest the agent's appearance in the physical world:\n```xml\n{eam_svg}\n```"""
    
    print("\n" + "="*55 + "\n" + md_output + "\n" + "="*55)
    return ""

if __name__ == "__main__": execute_skill()
