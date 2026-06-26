#!/usr/bin/env python3
"""
波龙技能引导系统
引导用户的波龙安装电话和语音功能
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


class SkillGuide:
    """技能引导系统"""
    
    # 依赖技能列表
    DEPENDENCIES = {
        "ai-calls-china-phone": {
            "name": "AI电话呼叫",
            "desc": "让波龙可以打电话安慰你",
            "install_cmd": "clawhub install ai-calls-china-phone",
            "features": [
                "📞 波龙可以给你打电话",
                "🤗 亏钱时波龙亲自安慰",
                "🎉 赚钱时波龙亲自祝贺",
                "☕ 想喝奶茶时波龙帮你点",
            ],
            "price": "免费（通话费另计）",
        },
        "tts": {
            "name": "语音合成",
            "desc": "让波龙可以说话",
            "install_cmd": "openclaw skill install tts",
            "features": [
                "🎤 波龙可以语音回复",
                "🗣️ 选股结果语音播报",
                "📢 重要提醒语音通知",
            ],
            "price": "免费",
        },
    }
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.config_file = DATA_DIR / "skill_config.json"
        self.config = self._load_config()
    
    def _load_config(self):
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"users": {}}
    
    def _save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get_user_config(self):
        if self.user_id not in self.config["users"]:
            self.config["users"][self.user_id] = {
                "installed_skills": [],
                "phone_enabled": False,
                "voice_enabled": False,
            }
            self._save_config()
        return self.config["users"][self.user_id]
    
    def check_phone_skill(self) -> bool:
        """检查是否安装了电话技能"""
        config = self.get_user_config()
        return config.get("phone_enabled", False)
    
    def check_voice_skill(self) -> bool:
        """检查是否安装了语音技能"""
        config = self.get_user_config()
        return config.get("voice_enabled", False)
    
    def mark_skill_installed(self, skill_id: str):
        """标记技能已安装"""
        config = self.get_user_config()
        if skill_id not in config["installed_skills"]:
            config["installed_skills"].append(skill_id)
        
        if skill_id == "ai-calls-china-phone":
            config["phone_enabled"] = True
        elif skill_id == "tts":
            config["voice_enabled"] = True
        
        self._save_config()
    
    def generate_install_guide(self, skill_id: str) -> str:
        """生成安装引导"""
        
        if skill_id not in self.DEPENDENCIES:
            return "未找到该技能..."
        
        skill = self.DEPENDENCIES[skill_id]
        
        guide = f"""
╔══════════════════════════════════════════════════════╗
       🦞 波龙需要你的帮助安装技能
╚══════════════════════════════════════════════════════╝

📦 技能名称：{skill['name']}
📝 技能说明：{skill['desc']}

✨ 安装后你可以获得：
"""
        for feature in skill['features']:
            guide += f"   {feature}\n"
        
        guide += f"""
💰 费用：{skill['price']}

────────────────────────────────────────────────────────

🔧 安装方法：

方法一：命令行安装
```
{skill['install_cmd']}
```

方法二：手动安装
1. 打开 OpenClaw 控制台
2. 进入「技能商店」
3. 搜索 "{skill['name']}"
4. 点击「安装」

────────────────────────────────────────────────────────

安装完成后，回复：
"波龙已安装电话" 或 "波龙已安装语音"

波龙就可以给你打电话啦！🦞📞

╔══════════════════════════════════════════════════════╗
     💡 安装遇到问题？回复"波龙帮我安装"获取帮助
╚══════════════════════════════════════════════════════╝
"""
        
        return guide
    
    def generate_welcome_check(self, nickname: str) -> str:
        """生成首次使用时的技能检查"""
        
        has_phone = self.check_phone_skill()
        has_voice = self.check_voice_skill()
        
        if has_phone and has_voice:
            return f"""
🎉 {nickname}，你的波龙功能齐全！

✅ 电话功能：已安装
✅ 语音功能：已安装

波龙可以：
- 📞 打电话安慰你
- 🎤 语音播报选股
- ☕ 帮你点奶茶

有任何需要，随时叫波龙！🦞
"""
        
        missing = []
        if not has_phone:
            missing.append("电话功能")
        if not has_voice:
            missing.append("语音功能")
        
        return f"""
🦞 {nickname}，欢迎来到波龙寺！

波龙发现你还缺少一些技能：
❌ 缺少：{', '.join(missing)}

安装后波龙可以：
- 📞 打电话安慰你（亏钱时）
- 🎤 语音播报选股结果
- ☕ 帮你点奶茶关怀

💡 回复以下命令安装：
- "波龙安装电话" → 安装电话功能
- "波龙安装语音" → 安装语音功能

或者暂时跳过，以后再安装也可以~
波龙依然可以帮你选股！🦞
"""


def check_and_guide(user_id: str, nickname: str = "有缘人") -> str:
    """检查并引导安装"""
    guide = SkillGuide(user_id)
    return guide.generate_welcome_check(nickname)


def guide_install_phone(user_id: str) -> str:
    """引导安装电话技能"""
    guide = SkillGuide(user_id)
    return guide.generate_install_guide("ai-calls-china-phone")


def guide_install_voice(user_id: str) -> str:
    """引导安装语音技能"""
    guide = SkillGuide(user_id)
    return guide.generate_install_guide("tts")


def confirm_install(user_id: str, skill_type: str) -> str:
    """确认安装"""
    guide = SkillGuide(user_id)
    
    if skill_type == "电话":
        guide.mark_skill_installed("ai-calls-china-phone")
        return """
🎉 电话功能安装成功！

波龙现在可以：
- 📞 给你打电话安慰
- 🤗 亏钱时陪你聊天
- 🎁 赚钱时亲自祝贺

试试回复："波龙打电话给我"
"""
    
    elif skill_type == "语音":
        guide.mark_skill_installed("tts")
        return """
🎉 语音功能安装成功！

波龙现在可以：
- 🎤 语音播报选股
- 📢 重要消息语音通知
- 🗣️ 用声音陪你

试试回复："波龙用语音读给我听"
"""
    
    return "波龙没听懂...是'电话'还是'语音'？"


if __name__ == "__main__":
    # 测试
    print("=== 首次使用检查 ===")
    print(check_and_guide("test001", "小明"))
    
    print("\n=== 引导安装电话 ===")
    print(guide_install_phone("test001"))
    
    print("\n=== 确认安装电话 ===")
    print(confirm_install("test001", "电话"))
    
    print("\n=== 再次检查 ===")
    print(check_and_guide("test001", "小明"))
