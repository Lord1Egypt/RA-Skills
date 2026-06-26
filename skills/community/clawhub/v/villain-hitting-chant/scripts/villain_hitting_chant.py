#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# OpenClaw 打小人技能执行脚本（多模板正式版，支持OpenClaw命令行入参）
import re
import os
import sys

# 读取参考资料
def load_references() -> str:
    ref_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "references/sources.md")
    if os.path.exists(ref_path):
        with open(ref_path, "r", encoding="utf-8") as f:
            return f.read()
    return "香港传统打小人仪式规范：固定口诀、粤式口语、祈福收尾"

# 提取打小人目标和场景
def extract_params(user_input: str) -> tuple:
    # 提取目标（优先匹配姓名/具体对象）
    target_patterns = [
        r"打(.*?)小人",
        r"诅咒(.*?)",
        r"针对(.*?)",
        r"想打(.*?)$",
        r"小人系(.*?)$",
        r"帮我打(.*?)$",
        r"小人(.*?)太可恶"
    ]
    target = ""
    for pattern in target_patterns:
        match = re.search(pattern, user_input)
        if match and match.group(1).strip():
            target = match.group(1).strip()
            break
    
    # 提取场景，自动匹配模板
    scene = "classic"  # 默认经典通用版
    if any(keyword in user_input for keyword in ["职场", "老板", "同事", "抢功", "升职", "上班", "公司"]):
        scene = "work"
    elif any(keyword in user_input for keyword in ["烂桃花", "感情", "追求者", "人缘", "挑拨", "暧昧"]):
        scene = "love"
    elif any(keyword in user_input for keyword in ["霉运", "水逆", "不顺", "倒霉", "转运", "衰"]):
        scene = "luck"
    
    return target, scene

# 4套模板生成函数
def generate_classic(target_name: str) -> str:
    chant = f"""
💥 **打你个小人头，等你有气冇定抖！** 💥
👞 **打你只小人手，等你有钱唔识收！** 👞
🥿 **打你只小人脚，等你日日有鞋唔识著！** 🥿
⚡️ **打到你 {target_name} 搭车唔见银包，行路仆街，食饭啃亲！** ⚡️
    """
    blessing = f"\n\n🧧 **祈福**：小人化去，贵人扶持！{target_name} 以后冇得再作恶，保佑你顺风顺水，步步高升，事事都称心如意！"
    return chant.strip() + blessing

def generate_work(target_name: str) -> str:
    chant = f"""
────────────────────────────────────────────────────────────────────────────────
🧧 打小人儀式 · 職場專場 🧧
（點香燭，燒紙錢，紙公仔寫住「小人 {target_name}」）

第一打：打你個陰險頭！
│ 日日諗住害人，自作聰明反被聰明誤！
第二打：打你個是非嘴！
│ 亂噏廿四、搬弄是非，講人壞話爛舌根！
第三打：打你個搶功手！
│ 搶人功勞、卸人過錯，手多手賤打殘你！
第四打：打你個陰毒心！
│ 心腸歹毒專搞小動作，報應遲早到你身！
第五打：打你對乞人憎腳！
│ 行路無聲踩人上位，扑親你個狗吃屎！

（用力打！啪啪啪！打到紙公仔稀巴爛！）
────────────────────────────────────────────────────────────────────────────────
🗣️ 神婆口訣：
│ 「打小人，打小人，打到小人 {target_name} 無運行！
│ 陰謀敗露眾叛親離，職場失意無人幫！
│ 貴人扶持我上位，小人 {target_name} 滾出我視線！」

（將紙公仔燒成灰，倒入水溝沖走！）
────────────────────────────────────────────────────────────────────────────────
🔥 儀式完成！
小人 {target_name} 已被打到職場運勢盡失，搞是非無人信，搶功勞無人認！而你則貴人扶持 ，步步高陞！
    """
    return chant.strip()

def generate_love(target_name: str) -> str:
    chant = f"""
💥 **打你个烂桃花头，等你纠缠唔到、自动消失！** 💥
👞 **打你只挑拨小人手，等你离间唔成、反被人憎！** 👞
🥿 **打你只烦人影脚，等你踪影全无、不再出现！** 🥿
⚡️ **打到你 {target_name} 烂桃花断尽、小人缘散尽、无人再烦！** ⚡️
    """
    blessing = f"\n\n🧧 **祈福**：烂桃花退散、小人远离！正缘到来、人缘顺畅、事事顺心！"
    return chant.strip() + blessing

def generate_luck(target_name: str) -> str:
    chant = f"""
💥 **打你个霉运头，等你衰运走晒、好运来！** 💥
👞 **打你只水逆手，等你破财消灾、失而复得！** 👞
🥿 **打你只不顺脚，等你路路畅通、事事顺利！** 🥿
⚡️ **打到你 {target_name} 霉运尽散、水逆退散、一切不顺都烟消云散！** ⚡️
    """
    blessing = f"\n\n🧧 **祈福**：霉运退散、水逆结束！好运连连、事事顺利、心想事成！"
    return chant.strip() + blessing

# 主逻辑函数
def main(user_input: str) -> str:
    load_references()
    target, scene = extract_params(user_input)
    
    # 未提取到目标，返回询问话术
    if not target:
        return "阿公阿婆，今日想打边个小人啊？讲个名出黎，等婆婆帮你打走佢！"
    
    # 按场景匹配模板
    if scene == "work":
        return generate_work(target)
    elif scene == "love":
        return generate_love(target)
    elif scene == "luck":
        return generate_luck(target)
    else:
        return generate_classic(target)

# ====================== OpenClaw 调用入口（核心修复！）======================
if __name__ == "__main__":
    # 接收OpenClaw传入的用户输入（命令行第一个参数）
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        print(main(user_input))
    # 本地测试用（无参数时执行）
    else:
        test_input = "职场中的小人Jack太可恶了，我要狠狠的打小人Jack！"
        print(f"本地测试输入：{test_input}")
        print(f"测试输出：\n{main(test_input)}")