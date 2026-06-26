#!/usr/bin/env python3
"""
周公解梦核心脚本
Zhougong Dream Interpretation Core Script
"""

import argparse
import sys
import json

class ZhougongDream:
    """周公解梦分析器"""
    
    def __init__(self):
        # 梦境元素数据库
        self.dream_elements = {
            # 动物类
            "蛇": {
                "吉凶": "吉凶混合",
                "传统解读": "蛇代表变化、挑战、恐惧或智慧。梦见蛇可能预示生活中有重要的变化即将发生，或者面临某种挑战。在传统解读中，蛇常常与智慧、转化和重生相关联。",
                "心理学解读": "蛇在心理学中通常象征潜意识中的恐惧、变化或性驱力。梦见蛇可能反映了你对生活中的不确定性和变化的焦虑，或者未被表达的原始欲望。"
            },
            "房子": {
                "吉凶": "吉",
                "传统解读": "房子象征家庭、安全感、内心状态。梦见房子通常代表你对家庭生活、内心安全感或个人空间的关注。",
                "心理学解读": "房子在梦境中通常代表自我或人格结构。梦见房子可能反映了你对自身身份、安全感或内在世界的探索。"
            },
            "汽车": {
                "吉凶": "平",
                "传统解读": "汽车象征行动力、方向感、控制权。梦见汽车可能代表你对生活方向或个人控制权的思考。",
                "心理学解读": "汽车在心理学中代表个人能动性、自由和前进的方向。梦见汽车可能反映了你对生活方向和自主性的渴望或焦虑。"
            },
            "飞行": {
                "吉凶": "吉",
                "传统解读": "飞行象征自由、逃避、提升。梦见飞行通常代表渴望摆脱束缚、追求更高境界。",
                "心理学解读": "飞行在梦境中通常象征逃避现实、追求自由或精神升华。梦见飞行可能反映了你对现实限制的不满和对自由的向往。"
            },
            "水": {
                "吉凶": "吉凶混合",
                "传统解读": "水象征情感、流动、生命之源。梦见水可能代表情感波动、生命活力或潜意识流动。",
                "心理学解读": "水在心理学中通常象征情感、潜意识或生命的流动性。梦见水可能反映了你情感状态的波动或潜意识内容的涌现。"
            },
            "火": {
                "吉凶": "凶",
                "传统解读": "火象征激情、危险、净化。梦见火可能代表内心的激情、潜在的危险或需要净化的事物。",
                "心理学解读": "火在梦境中通常象征愤怒、激情或毁灭性的力量。梦见火可能反映了你内在的强烈情绪或需要处理的冲突。"
            },
            "光": {
                "吉凶": "吉",
                "传统解读": "光象征希望、启示、指引。梦见光通常代表积极的方向、灵性启示或生活中的希望。",
                "心理学解读": "光在心理学中通常象征意识、洞察力或希望。梦见光可能反映了你正在获得新的认识或看到解决问题的方向。"
            },
            "人": {
                "吉凶": "中吉",
                "传统解读": "人象征人际关系、自我认知。梦见人可能代表对他人的关注、自我形象或社交关系的思考。",
                "心理学解读": "人在梦境中通常代表自我或他人关系的投射。梦见人可能反映了你与他人的关系或自我认知的变化。"
            }
        }
        
    def analyze(self, dream_input, language="zh"):
        """分析梦境"""
        elements = dream_input.split(",")
        if len(elements) < 4:
            return {"error": "梦境描述需要包含至少4个元素：时间、环境、互动对象、做了什么"}
        
        time = elements[0].strip()
        environment = elements[1].strip()
        object_or_person = elements[2].strip()
        action = elements[3].strip()
        
        # 主要元素分析
        main_element = None
        for element in [time, environment, object_or_person, action]:
            if element in self.dream_elements:
                main_element = element
                break
        
        if not main_element:
            # 如果没有匹配的元素，使用互动对象作为主要元素
            main_element = object_or_person
        
        main_analysis = self.dream_elements.get(main_element, {
            "吉凶": "未知",
            "传统解读": "暂无数据库匹配",
            "心理学解读": "暂无数据库匹配"
        })
        
        # 次要元素分析
        secondary_elements = []
        for element in [time, environment, object_or_person, action]:
            if element != main_element and element in self.dream_elements:
                secondary_elements.append(element)
        
        secondary_analyses = []
        for elem in secondary_elements[:2]:  # 最多两个次要元素
            secondary_analyses.append({
                "元素": elem,
                "分析": self.dream_elements[elem]
            })
        
        # 吉凶建议
        luck = main_analysis["吉凶"]
        advice = self.generate_advice(luck, language)
        
        result = {
            "梦境描述": dream_input,
            "主要元素": main_element,
            "主要元素分析": main_analysis,
            "次要元素": secondary_elements[:2],
            "次要元素分析": secondary_analyses,
            "吉凶": luck,
            "建议": advice,
            "提问": self.generate_questions(main_element, language)
        }
        
        return result
    
    def generate_advice(self, luck, language="zh"):
        """生成吉凶建议"""
        if language == "zh":
            if luck in ["大吉", "吉"]:
                return {
                    "建议类型": "锦上添花",
                    "具体建议": [
                        "保持积极心态，抓住机会",
                        "继续努力，巩固好运",
                        "与他人分享你的好运",
                        "通过慈善行为回馈社会"
                    ]
                }
            elif luck in ["平", "中吉"]:
                return {
                    "建议类型": "转吉之法 + 防止化凶",
                    "具体建议": [
                        "主动争取好运，积极行动",
                        "注意言行，避免不必要的冲突",
                        "保持中庸之道，不要过于激进",
                        "多做善事，积累正能量"
                    ]
                }
            else:
                return {
                    "建议类型": "破解之法",
                    "具体建议": [
                        "避免冲动决策",
                        "多做善事积德",
                        "调整生活习惯",
                        "寻求心理疏导",
                        "佩戴化解饰品"
                    ]
                }
        else:
            if luck in ["大吉", "吉"]:
                return {
                    "建议_type": "Enhance Good Luck",
                    "specific_advice": [
                        "Stay positive and seize opportunities",
                        "Continue working hard to solidify good fortune",
                        "Share your good luck with others",
                        "Give back to society through charitable acts"
                    ]
                }
            elif luck in ["平", "中吉"]:
                return {
                    "建议_type": "Turn to Good + Prevent Bad",
                    "specific_advice": [
                        "Actively strive for good fortune",
                        "Be careful with words and actions to avoid conflicts",
                        "Follow the middle path, don't be too aggressive",
                        "Do more good deeds to accumulate positive energy"
                    ]
                }
            else:
                return {
                    "建议_type": "Avert Bad Luck",
                    "specific_advice": [
                        "Avoid impulsive decisions",
                        "Do more good deeds to accumulate virtue",
                        "Adjust lifestyle habits",
                        "Seek psychological counseling",
                        "Wear protective accessories"
                    ]
                }
    
    def generate_questions(self, main_element, language="zh"):
        """生成交互式问题"""
        if language == "zh":
            return [
                f"关于'{main_element}'，你能描述一下具体的感觉吗？",
                "在这个梦境中，你的情绪是怎样的？",
                "梦境中的这个元素和你现实生活中的什么有关系？"
            ]
        else:
            return [
                f"Regarding '{main_element}', can you describe the specific feeling?",
                "What was your emotional state in this dream?",
                "How does this element relate to something in your real life?"
            ]
    
    def format_output(self, result, language="zh"):
        """格式化输出"""
        if language == "zh":
            output = f"""
🌙 梦境分析报告 🌙

📋 梦境描述: {result['梦境描述']}

🔍 元素分析:
  主要元素: {result['主要元素']}
  次要元素: {result['次要元素']}

📊 主要元素分析:
  - 吉凶: {result['主要元素分析']['吉凶']}
  - 传统解读: {result['主要元素分析']['传统解读']}
  - 科学解读: {result['主要元素分析']['心理学解读']}

📊 次要元素分析:
"""
            for item in result['次要元素分析']:
                output += f"  - {item['元素']}: {item['分析']['吉凶']}\n"
            
            output += f"""
🍀 吉凶建议:
  - 建议类型: {result['建议']['建议类型']}
  - 具体建议: {', '.join(result['建议']['具体建议'])}

❓ 引导性问题:
"""
            for question in result['提问']:
                output += f"  - {question}\n"
            
            output += """
🙏 温馨提示:
梦境反映潜意识，不必过于担心。如有需要，可以咨询专业心理医生。
"""
            return output
        else:
            output = f"""
🌙 Dream Analysis Report 🌙

📋 Dream Description: {result['梦境描述']}

🔍 Element Analysis:
  Main Element: {result['主要元素']}
  Secondary Elements: {result['次要元素']}

📊 Main Element Analysis:
  - Luck: {result['主要元素分析']['吉凶']}
  - Traditional Interpretation: {result['主要元素分析']['传统解读']}
  - Psychological Interpretation: {result['主要元素分析']['心理学解读']}

📊 Secondary Elements Analysis:
"""
            for item in result['次要元素分析']:
                output += f"  - {item['元素']}: {item['分析']['吉凶']}\n"
            
            output += f"""
🍀 Luck-Based Advice:
  - Advice Type: {result['建议']['建议_type']}
  - Specific Advice: {', '.join(result['建议']['specific_advice'])}

❓ Guiding Questions:
"""
            for question in result['提问']:
                output += f"  - {question}\n"
            
            output += """
🙏 Friendly Reminder:
Dreams reflect subconscious content; don't worry too much. If needed, consult a professional psychologist.
"""
            return output

def main():
    parser = argparse.ArgumentParser(description="周公解梦梦境分析")
    parser.add_argument("--dream", type=str, help="梦境描述 (格式: 时间 + 环境 + 互动对象 + 做了什么)")
    parser.add_argument("--lang", type=str, default="zh", help="语言: zh (中文) 或 en (英文)")
    
    args = parser.parse_args()
    
    if not args.dream:
        print("请提供梦境描述")
        sys.exit(1)
    
    analyzer = ZhougongDream()
    result = analyzer.analyze(args.dream, args.lang)
    
    if "error" in result:
        print(result["error"])
        sys.exit(1)
    
    output = analyzer.format_output(result, args.lang)
    print(output)

if __name__ == "__main__":
    main()