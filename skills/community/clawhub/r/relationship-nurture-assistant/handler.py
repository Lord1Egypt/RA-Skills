"""Relationship Nurture Assistant - 亲密关系滋养助手"""
import json, re

def parse_relationship_input(text):
    result = {"type": "亲密关系", "party": None, "problem": None, "emotion": None}
    if any(k in text for k in ["老婆", "妻子", "老公", "丈夫", "结婚"]): result["type"] = "伴侣"
    elif any(k in text for k in ["孩子", "儿子", "女儿", "亲子"]): result["type"] = "亲子"
    elif any(k in text for k in ["父母", "爸爸", "妈妈", "婆婆", "岳母"]): result["type"] = "代际"
    for e in ["难过", "生气", "失望", "委屈", "困惑", "焦虑"]:
        if e in text: result["emotion"] = e
    result["problem"] = text[:50]
    return result

def get_tips(rtype, emotion):
    tips = {
        "伴侣": {
            "难过": ["先处理情绪，再处理事情", "用'我感到...因为...'代替指责", "约定冷静时间后共同讨论"],
            "生气": ["暂停对话，等双方平复", "避免在气头上做决定", "用'我需要...'代替'你总是...'"],
            "困惑": ["列出具体困惑点", "选择一个最核心的问题优先讨论", "考虑对方视角"],
        },
        "亲子": {
            "难过": ["先共情：妈妈知道你很难过", "询问需要什么帮助", "陪伴而非立即给解决方案"],
            "生气": ["先让情绪过去再沟通", "12岁以下：先连接再纠正", "12岁以上：给予空间再约谈"],
        },
        "代际": {
            "困惑": ["区分关心和控制", "课题分离：谁的事谁做主", "温和但坚定地表达边界"],
        }
    }
    return tips.get(rtype, {}).get(emotion, ["先冷静，再沟通"])

def handle(text):
    parsed = parse_relationship_input(text)
    tips = get_tips(parsed["type"], parsed.get("emotion", "困惑"))
    phrases = {
        "伴侣": ["我感到[情绪]，因为[原因]，我需要[需求]。", "谢谢为这个家付出，想和你聊聊[话题]。"],
        "亲子": ["我知道你[情绪]，我也曾经[经历]。", "我们一起来想想有什么办法？"],
        "代际": ["理解您的担心，我来想想怎么处理。", "这件事我想自己决定，谢谢您的关心。"],
    }
    return {
        "relationshipType": parsed["type"],
        "detectedEmotion": parsed.get("emotion"),
        "practicalTips": tips,
        "examplePhrases": phrases.get(parsed["type"], phrases["伴侣"]),
        "note": "关系滋养是长期投资，每天10分钟高质量陪伴大于偶尔一次性大投入。"
    }

if __name__ == "__main__":
    for tc in ["老婆最近总是加班到很晚，回家都很累，不知道怎么关心她", "青春期的儿子不愿意和我说话了，怎么办"]:
        r = handle(tc)
        print("Input: " + tc)
        print("  Type: " + r["relationshipType"] + " | Emotion: " + str(r["detectedEmotion"]))
        print("  Tip: " + r["practicalTips"][0])
        print()
