#!/usr/bin/env python3
"""
SBTI 人格测试 V3 - 梗王版

基于用户提供的接地气人格类型，每个都有独特的ASCII艺术宠物
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class Question:
    """测试题目 - 4选项版本"""
    id: int
    text: str
    dimensions: List[str]
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    scores_a: Dict[str, int]
    scores_b: Dict[str, int]
    scores_c: Dict[str, int]
    scores_d: Dict[str, int]


@dataclass
class SBTIType:
    """SBTI人格类型 + ASCII宠物"""
    code: str
    name: str
    nickname: str
    emoji: str
    description: str
    traits: List[str]
    pet_art: str
    pet_name: str


# ==================== 新梗王版ASCII艺术宠物库 ====================

PET_ARTS = {
    "IMSB": """
      💔 IMSB
    ╭────────╮
    │  (╥﹏╥)  │
    │  我垃圾  │
    │  我不行  │
    ╰────┬───╯
       🔪│🔪
        🩸
     自我攻击刺猬
    """,
    
    "BOSS": """
      👔 BOSS
    ╭────────╮
    │ 😎😎😎 │
    │  听我的 │
    │  我说了算│
    ╰────┬───╯
       💼│💼
        🎩
     霸道总裁狮
    """,
    
    "MUM": """
      👩 MUM
    ╭────────╮
    │ 🍳🍳🍳 │
    │ 穿秋裤 │
    │ 吃饱没 │
    ╰────┬───╯
       🩴│🩴
        ❤️
      唠叨妈妈兔
    """,
    
    "FAKE": """
      🎭 FAKE
    ╭────────╮
    │ 🤖🤖🤖 │
    │  假装人类│
    │  情绪稳定│
    ╰────┬───╯
       👔│👔
        💾
      伪人机器人
    """,
    
    "DEAD": """
      ☠️ DEAD
    ╭────────╮
    │  💀💀  │
    │  已死   │
    │  勿cue │
    ╰────┬───╯
       ⚰️│⚰️
        🪦
      真·死者骷髅
    """,
    
    "ZZZZ": """
      😴 ZZZZ
    ╭────────╮
    │  💤💤  │
    │ 装死中 │
    │ 勿扰   │
    ╰────┬───╯
       🛏️│🛏️
        💤
      装死树懒
    """,
    
    "GOGO": """
      🏃 GOGO
    ╭────────╮
    │  🏃‍♂️💨  │
    │  冲！  │
    │  不停下 │
    ╰────┬───╯
       👟│👟
        🏁
      永动行者狼
    """,
    
    "FUCK": """
      🌿 FUCK
    ╭────────╮
    │  🖕🖕  │
    │  草！  │
    │  全世界 │
    ╰────┬───╯
       🔥│🔥
        💥
      暴躁草泥马
    """,
    
    "CTRL": """
      👌 CTRL
    ╭────────╮
    │  😏   │
    │ 拿捏了 │
    │  全掌控 │
    ╰────┬───╯
       🎮│🎮
        👑
      拿捏大师蜘蛛
    """,
    
    "HHHH": """
      😄 HHHH
    ╭────────╮
    │  🤣🤣  │
    │ 哈哈哈 │
    │ 傻乐呢 │
    ╰────┬───╯
       🦶│🦶
        🎈
      傻乐哈士奇
    """,
    
    "SEXY": """
      🔥 SEXY
    ╭────────╮
    │  😘💋  │
    │  尤物  │
    │  天生魅 │
    ╰────┬───╯
       👠│👠
        🌹
      性感狐狸精
    """,
    
    "OJBK": """
      👌 OJBK
    ╭────────╮
    │  😐   │
    │  都行  │
    │  无所谓 │
    ╰────┬───╯
       🤷│🤷
        🍵
      佛系水豚
    """,
    
    "POOR": """
      💸 POOR
    ╭────────╮
    │  😭💸  │
    │  穷死  │
    │  吃土中 │
    ╰────┬───╯
       👟│👟
        🥬
      贫穷老鼠
    """,
    
    "OHNO": """
      😱 OHNO
    ╭────────╮
    │  😱😱  │
    │  完了  │
    │  芭比Q │
    ╰────┬───╯
       🏃│🏃
        💦
      慌张松鼠
    """,
    
    "MONK": """
      🙏 MONK
    ╭────────╮
    │  😌📿  │
    │  阿弥陀佛│
    │  随缘   │
    ╰────┬───╯
       🧘│🧘
        🪷
      僧人乌龟
    """,
    
    "SHIT": """
      💩 SHIT
    ╭────────╮
    │  🤮   │
    │  狗屎  │
    │  毁灭吧 │
    ╰────┬───╯
       👎│👎
        🚮
      狗屎人臭鼬
    """,
    
    "THANK": """
      🙏 THANK
    ╭────────╮
    │  🥹   │
    │  感恩  │
    │  谢谢你 │
    ╰────┬───╯
       ❤️│❤️
        ✨
      感恩小狗
    """,
    
    "MALO": """
      🐒 MALO
    ╭────────╮
    │  🐒🍌  │
    │  吗喽  │
    │  命也是命│
    ╰────┬───╯
       🍌│🍌
        🌴
      吗喽猴子
    """,
    
    "ATM": """
      💳 ATM
    ╭────────╮
    │  🤑💰  │
    │  送钱  │
    │  大冤种 │
    ╰────┬───╯
       💸│💸
        🏧
      ATM提款机熊
    """,
    
    "THINK": """
      🤔 THINK
    ╭────────╮
    │  🤔💡  │
    │  思考  │
    │  别吵我 │
    ╰────┬───╯
       📖│📖
        🧠
      思考者猫头鹰
    """,
    
    "SOLO": """
      🚶 SOLO
    ╭────────╮
    │  😶   │
    │  孤儿  │
    │  一个人 │
    ╰────┬───╯
       🎧│🎧
        🌙
      孤狼
    """,
    
    "LOVER": """
      💕 LOVER
    ╭────────╮
    │  🥰💖  │
    │  多情  │
    │  都爱我 │
    ╰────┬───╯
       💘│💘
        🌹
      多情种孔雀
    """,
    
    "WOC": """
      🤯 WOC
    ╭────────╮
    │  🤯‼️  │
    │  握草  │
    │  震惊了 │
    ╰────┬───╯
       ⚡│⚡
        💥
      震惊猫
    """,
    
    "DRUNK": """
      🍺 DRUNK
    ╭────────╮
    │  🥴🍺  │
    │  喝！  │
    │  再来一杯│
    ╰────┬───╯
       🍻│🍻
        🍾
      酒鬼熊猫
    """,
    
    "IMFW": """
      🗑️ IMFW
    ╭────────╮
    │  😪   │
    │  废物  │
    │  开摆   │
    ╰────┬───╯
       🛋️│🛋️
        📺
      废物咸鱼
    """,
    
    "JOKER": """
      🤡 JOKER
    ╭────────╮
    │  🤡🤡  │
    │  小丑  │
    │  竟是我自己│
    ╰────┬───╯
       🃏│🃏
        🎪
      小丑面具
    """,
    
    "DIORS": """
      👟 DIORS
    ╭────────╮
    │  😅   │
    │  屌丝  │
    │  习惯了 │
    ╰────┬───╯
       👟│👟
        💼
      屌丝青蛙
    """,
}


class SBTITestV3:
    """SBTI 测试 V3 - 梗王版"""
    
    # 30道测试题目
    QUESTIONS = [
        # 维度1: 社交倾向
        Question(1, "周末有人约你出去玩，你的反应是？", ["social"],
            "推掉所有邀约，宅家最舒服",
            "看心情，偶尔出去一下",
            "愉快答应，但要挑喜欢的活动",
            "太好了！马上出发！还要叫更多人！",
            {"social": -2}, {"social": -1}, {"social": 1}, {"social": 2}),
        
        Question(2, "在聚会上，你通常", ["social"],
            "找个角落玩手机，希望没人注意我",
            "和一两个熟人聊天",
            "主动加入有趣的话题",
            "全场穿梭，组织游戏，成为焦点",
            {"social": -2}, {"social": -1}, {"social": 1}, {"social": 2}),
        
        Question(3, "面对陌生人搭话，你会", ["social"],
            "紧张，希望能快速结束对话",
            "礼貌回应，但不主动",
            "友好交流，留下好印象",
            "自来熟，马上变成朋友",
            {"social": -2}, {"social": -1}, {"social": 1}, {"social": 2}),
        
        # 维度2: 情绪表达
        Question(4, "做决定时，你更依赖", ["emotion"],
            "完全凭直觉和感受",
            "感受为主，参考逻辑",
            "逻辑为主，兼顾感受",
            "严格的逻辑和数据",
            {"emotion": 2}, {"emotion": 1}, {"emotion": -1}, {"emotion": -2}),
        
        Question(5, "看电影时，你更容易", ["emotion"],
            "完全沉浸在情感中，哭得稀里哗啦",
            "被情节打动，但保持一定理智",
            "一边看一边分析剧情合理性",
            "专注于找bug和逻辑漏洞",
            {"emotion": 2}, {"emotion": 1}, {"emotion": -1}, {"emotion": -2}),
        
        Question(6, "朋友失恋找你哭诉，你会", ["emotion"],
            "陪他一起哭，感同身受",
            "先安慰情绪，再慢慢分析",
            "理性分析问题，给实用建议",
            "直接指出他/她的问题",
            {"emotion": 2}, {"emotion": 1}, {"emotion": -1}, {"emotion": -2}),
        
        # 维度3: 能量来源
        Question(7, "你的能量来源是", ["energy"],
            "独处充电，社交耗电",
            "更喜欢独处，偶尔社交",
            "社交独处都可以，看情况",
            "社交让我充满活力",
            {"energy": -2}, {"energy": -1}, {"energy": 1}, {"energy": 2}),
        
        Question(8, "工作需要团队协作时，你", ["energy"],
            "强烈希望独立完成任务",
            "可以合作，但更喜欢分工明确",
            "享受协作，但保留独立思考空间",
            "最爱头脑风暴，人多力量大",
            {"energy": -2}, {"energy": -1}, {"energy": 1}, {"energy": 2}),
        
        Question(9, "描述自己时，你倾向于", ["energy"],
            "倾听为主，很少表达",
            "倾听多于表达",
            "表达倾听差不多",
            "表达欲旺盛，话痨一个",
            {"energy": -2}, {"energy": -1}, {"energy": 1}, {"energy": 2}),
        
        # 维度4: 生活态度
        Question(10, "面对deadline，你通常", ["attitude"],
            "完全不慌，最后一天再说",
            "稍微提前一点，但也不会太早",
            "提前规划，稳步推进",
            "提前完成，还要超额交付",
            {"attitude": -2}, {"attitude": -1}, {"attitude": 1}, {"attitude": 2}),
        
        Question(11, "对于人生规划，你的态度是", ["attitude"],
            "躺平就好，顺其自然",
            "大致有个方向就行",
            "需要阶段性目标",
            "必须有详细的人生规划",
            {"attitude": -2}, {"attitude": -1}, {"attitude": 1}, {"attitude": 2}),
        
        Question(12, "遇到难题时，你会", ["attitude"],
            "先放一边，玩会儿再说",
            "做点别的转移注意力",
            "先尝试解决，不行再求助",
            "立即着手，必须攻克",
            {"attitude": -2}, {"attitude": -1}, {"attitude": 1}, {"attitude": 2}),
        
        # 维度5: 思维方式
        Question(13, "学习新技能，你更喜欢", ["thinking"],
            "直接上手，边做边学",
            "先看教程，然后实践",
            "系统学习理论再实践",
            "必须完整掌握理论才行",
            {"thinking": 2}, {"thinking": 1}, {"thinking": -1}, {"thinking": -2}),
        
        Question(14, "面对未知情况，你倾向于", ["thinking"],
            "凭直觉先试试看",
            "大致了解一下再行动",
            "研究清楚再谨慎行动",
            "必须完全了解才敢动",
            {"thinking": 2}, {"thinking": 1}, {"thinking": -1}, {"thinking": -2}),
        
        Question(15, "你更相信", ["thinking"],
            "第六感和预感",
            "直觉+经验",
            "经验和实证",
            "数据和科学验证",
            {"thinking": 2}, {"thinking": 1}, {"thinking": -1}, {"thinking": -2}),
        
        # 维度6: 说话风格
        Question(16, "开玩笑的尺度，你", ["bullshit"],
            "很有分寸，从不开玩笑",
            "比较保守，偶尔开玩笑",
            "比较随意，经常开玩笑",
            "没有边界，啥都敢说",
            {"bullshit": -2}, {"bullshit": -1}, {"bullshit": 1}, {"bullshit": 2}),
        
        Question(17, "朋友说你", ["bullshit"],
            "严肃认真，一丝不苟",
            "靠谱稳重",
            "有点皮",
            "神经病一个",
            {"bullshit": -2}, {"bullshit": -1}, {"bullshit": 1}, {"bullshit": 2}),
        
        Question(18, "在严肃场合，你会", ["bullshit"],
            "绝对正经，保持严肃",
            "努力保持正经",
            "偶尔忍不住皮一下",
            "总是忍不住想逗笑大家",
            {"bullshit": -2}, {"bullshit": -1}, {"bullshit": 1}, {"bullshit": 2}),
        
        # 维度7: 自我认知
        Question(19, "照镜子时，你觉得", ["identity"],
            "我是什么丑东西",
            "还行吧，普通人",
            "不错，挺好看的",
            "老子天下第一帅/美",
            {"identity": -2}, {"identity": -1}, {"identity": 1}, {"identity": 2}),
        
        Question(20, "面对挑战，你的第一反应", ["identity"],
            "我肯定不行...",
            "有点担心，但试试看",
            "应该可以，全力以赴",
            "我可以！肯定能成！",
            {"identity": -2}, {"identity": -1}, {"identity": 1}, {"identity": 2}),
        
        Question(21, "被人夸奖时，你会", ["identity"],
            "觉得对方在客套或讽刺",
            "有点不好意思",
            "坦然接受，说谢谢",
            "那当然！老子本来就优秀！",
            {"identity": -2}, {"identity": -1}, {"identity": 1}, {"identity": 2}),
        
        # 维度8: 脾气控制
        Question(22, "遇到糟心事，你会", ["temper"],
            "当场爆炸，忍不了一点",
            "很生气，但努力克制",
            "有点不爽，但很快平复",
            "心平气和，理性处理",
            {"temper": -2}, {"temper": -1}, {"temper": 1}, {"temper": 2}),
        
        Question(23, "排队被人插队，你会", ["temper"],
            "直接怼回去，不能忍",
            "很生气地提醒对方",
            "心里不爽，算了",
            "完全不在意",
            {"temper": -2}, {"temper": -1}, {"temper": 1}, {"temper": 2}),
        
        Question(24, "游戏输了，你", ["temper"],
            "rage quit，砸键盘",
            "很生气，抱怨队友",
            "有点沮丧，再来一局",
            "无所谓，游戏而已",
            {"temper": -2}, {"temper": -1}, {"temper": 1}, {"temper": 2}),
        
        # 维度9: 规划能力
        Question(25, "有钱到手，你会", ["planning"],
            "马上花掉，享受当下",
            "大部分花掉，存一点点",
            "大部分存起来，花一点点",
            "全部存起来，为未来打算",
            {"planning": -2}, {"planning": -1}, {"planning": 1}, {"planning": 2}),
        
        Question(26, "对于生活，你认为", ["planning"],
            "及时行乐最重要",
            "现在快乐+一点点规划",
            "为未来准备更重要",
            "每一步都要有明确计划",
            {"planning": -2}, {"planning": -1}, {"planning": 1}, {"planning": 2}),
        
        Question(27, "周末安排，你更喜欢", ["planning"],
            "完全随机，走到哪算哪",
            "大概有个方向就行",
            "提前想好要做什么",
            "精确到分钟的计划表",
            {"planning": -2}, {"planning": -1}, {"planning": 1}, {"planning": 2}),
        
        # 混合维度题目
        Question(28, "如果世界末日，你会", ["emotion", "planning"],
            "和爱的人静静等待",
            "和爱的人享受最后时光",
            "疯狂一把，完成心愿清单",
            "疯狂一把，想干啥干啥",
            {"emotion": 2, "planning": -2}, {"emotion": 2, "planning": -1}, 
            {"emotion": 1, "planning": -2}, {"emotion": 1, "planning": -1}),
        
        Question(29, "描述理想生活", ["attitude", "emotion"],
            "平淡安稳，岁月静好",
            "安稳中有一些小惊喜",
            "精彩刺激，充满挑战",
            "跌宕起伏，轰轰烈烈",
            {"attitude": -1, "emotion": 1}, {"attitude": 0, "emotion": 1}, 
            {"attitude": 1, "emotion": 2}, {"attitude": 2, "emotion": 2}),
        
        Question(30, "你认为自己的本质是", ["identity", "bullshit"],
            "一个善良的老实人",
            "一个好人",
            "一个有缺点的普通人",
            "一个混蛋（但可爱）",
            {"identity": 1, "bullshit": -2}, {"identity": 1, "bullshit": -1}, 
            {"identity": 0, "bullshit": 0}, {"identity": 2, "bullshit": 2}),
    ]
    
    # 梗王版人格类型
    PERSONALITY_TYPES = {
        "IMSB": SBTIType("IMSB", "自我攻击者", "I'm Shit, Boss", "💔",
            "你对自己有着超乎寻常的严苛标准。每次失败都像是世界末日，你总觉得自己不够好。",
            ["自我批评", "高标准", "内耗严重", "需要认可"],
            PET_ARTS["IMSB"], "自我攻击刺猬"),
        
        "BOSS": SBTIType("BOSS", "领导者", "The Boss", "👔",
            "天生的领袖气质。你说一不二，所有人都要听你的。气场强大到让人不敢直视。",
            ["气场强大", "决策果断", "掌控全局", "说一不二"],
            PET_ARTS["BOSS"], "霸道总裁狮"),
        
        "MUM": SBTIType("MUM", "妈妈", "The Mum", "👩",
            "你有着与生俱来的照顾欲。穿秋裤了吗？吃饱了吗？早点睡——你的口头禅。",
            ["无微不至", "操心命", "温暖贴心", "爱唠叨"],
            PET_ARTS["MUM"], "唠叨妈妈兔"),
        
        "FAKE": SBTIType("FAKE", "伪人", "The Fake Human", "🎭",
            "你完美地扮演着情绪稳定的成年人。表面云淡风轻，内心早已崩溃一万次。",
            ["伪装大师", "情绪稳定", "隐藏真实", "社交面具"],
            PET_ARTS["FAKE"], "伪人机器人"),
        
        "DEAD": SBTIType("DEAD", "死者", "The Dead", "☠️",
            "你已经死透了。对一切都提不起兴趣，像行尸走肉一样活着。",
            ["生无可恋", "极度疲惫", "失去热情", "心如死灰"],
            PET_ARTS["DEAD"], "真·死者骷髅"),
        
        "ZZZZ": SBTIType("ZZZZ", "装死者", "The Pretender", "😴",
            "你没死，但你在装死。遇到困难第一反应就是躺平，逃避虽然可耻但有用。",
            ["逃避大师", "装死专家", "能躲就躲", "间歇性诈尸"],
            PET_ARTS["ZZZZ"], "装死树懒"),
        
        "GOGO": SBTIType("GOGO", "行者", "The Go-Getter", "🏃",
            "停不下来，根本停不下来。你的生命就是一场永无止境的冲刺。",
            ["永动机", "执行力MAX", "停不下来", "目标导向"],
            PET_ARTS["GOGO"], "永动行者狼"),
        
        "FUCK": SBTIType("FUCK", "草者", "The F-word", "🌿",
            "你的口头禅是草。对这个世界充满愤怒，看谁都不顺眼。",
            ["暴躁老哥", "出口成脏", "愤世嫉俗", "一点就着"],
            PET_ARTS["FUCK"], "暴躁草泥马"),
        
        "CTRL": SBTIType("CTRL", "拿捏者", "The Controller", "👌",
            "一切尽在掌控。你能精准把握每个人的心理，把局面玩弄于股掌之间。",
            ["掌控欲强", "心理大师", "游刃有余", "让人又爱又怕"],
            PET_ARTS["CTRL"], "拿捏大师蜘蛛"),
        
        "HHHH": SBTIType("HHHH", "傻乐者", "The Happy-Go-Lucky", "😄",
            "你每天都在哈哈哈。没什么大不了的，笑一笑就过去了。",
            ["乐天派", "笑点低", "没心没肺", "快乐传染源"],
            PET_ARTS["HHHH"], "傻乐哈士奇"),
        
        "SEXY": SBTIType("SEXY", "尤物", "The Sexy One", "🔥",
            "行走的荷尔蒙。不用刻意，天生自带魅惑光环，让人移不开眼。",
            ["天生魅", "吸引力MAX", "自信爆棚", "气场强大"],
            PET_ARTS["SEXY"], "性感狐狸精"),
        
        "OJBK": SBTIType("OJBK", "无所谓人", "The Carefree", "👌",
            "都行，可以，没关系。佛系到让人怀疑你是不是真的没有欲望。",
            ["佛系", "无欲望", "随遇而安", "不争不抢"],
            PET_ARTS["OJBK"], "佛系水豚"),
        
        "POOR": SBTIType("POOR", "贫穷者", "The Broke", "💸",
            "穷是你的标签。吃土是日常，但你在贫穷中找到了独特的快乐。",
            ["吃土日常", "省钱大师", "穷开心", "精打细算"],
            PET_ARTS["POOR"], "贫穷老鼠"),
        
        "OHNO": SBTIType("OHNO", "哦不人", "The Panicker", "😱",
            "完了，芭比Q了。你总是第一时间想到最坏的结果，然后开始慌乱。",
            ["悲观主义者", "容易慌乱", "灾难思维", "杞人忧天"],
            PET_ARTS["OHNO"], "慌张松鼠"),
        
        "MONK": SBTIType("MONK", "僧人", "The Monk", "🙏",
            "阿弥陀佛，一切随缘。你已经达到了超然物外的境界。",
            ["佛系", "看透红尘", "内心平静", "与世无争"],
            PET_ARTS["MONK"], "僧人乌龟"),
        
        "SHIT": SBTIType("SHIT", "狗屎人", "The Shitty One", "💩",
            "你觉得这个世界就是狗屎。看什么都不顺眼，但你说得还挺有道理。",
            ["愤世嫉俗", "毒舌", "吐槽犀利", "悲观但真实"],
            PET_ARTS["SHIT"], "狗屎人臭鼬"),
        
        "THANK": SBTIType("THANK", "感恩者", "The Grateful", "🙏",
            "谢谢，太感谢了，感恩。你总是把谢谢挂在嘴边，对一切都充满感激。",
            ["感恩", "礼貌", "温暖", "正能量"],
            PET_ARTS["THANK"], "感恩小狗"),
        
        "MALO": SBTIType("MALO", "吗喽", "The Monkey", "🐒",
            "吗喽的命也是命。你在社会中挣扎求生，像只猴子一样忙碌。",
            ["打工人", "社畜", "忙碌", "命苦"],
            PET_ARTS["MALO"], "吗喽猴子"),
        
        "ATM": SBTIType("ATM", "送钱者", "The ATM", "💳",
            "你是行走的提款机。总是忍不住为别人花钱，冤种本种。",
            ["冤种", "爱花钱", "对人好", "容易被利用"],
            PET_ARTS["ATM"], "ATM提款机熊"),
        
        "THINK": SBTIType("THINK", "思考者", "The Thinker", "🤔",
            "你在思考，别吵。脑子里永远有十万个为什么，喜欢深入分析问题。",
            ["爱思考", "理性", "深度", "哲学气质"],
            PET_ARTS["THINK"], "思考者猫头鹰"),
        
        "SOLO": SBTIType("SOLO", "孤儿", "The Lone Wolf", "🚶",
            "你是一个人在战斗。习惯了孤独，一个人也能活得很好。",
            ["独来独往", "自给自足", "孤独", "强大"],
            PET_ARTS["SOLO"], "孤狼"),
        
        "LOVER": SBTIType("LOVER", "多情者", "The Lover", "💕",
            "你的爱很泛滥。见一个爱一个，每个人都值得你的爱。",
            ["多情", "浪漫", "爱所有人", "情感丰富"],
            PET_ARTS["LOVER"], "多情种孔雀"),
        
        "WOC": SBTIType("WOC", "握草人", "The Shocker", "🤯",
            "握草！你每天都在震惊。世界太疯狂，你的眼睛已经看不过来了。",
            ["震惊体", "反应夸张", "情绪外露", "表情包本人"],
            PET_ARTS["WOC"], "震惊猫"),
        
        "DRUNK": SBTIType("DRUNK", "酒鬼", "The Drunkard", "🍺",
            "酒是你的灵魂伴侣。微醺是常态，宿醉是勋章。",
            ["爱喝酒", "微醺美学", "社交润滑剂", "宿醉常客"],
            PET_ARTS["DRUNK"], "酒鬼熊猫"),
        
        "IMFW": SBTIType("IMFW", "废物", "The Waste", "🗑️",
            "承认吧，你就是废物。但那又怎样，废物也有废物的快乐。",
            ["躺平", "废物", "开摆", "快乐废物"],
            PET_ARTS["IMFW"], "废物咸鱼"),
        
        "JOKER": SBTIType("JOKER", "小丑", "The Joker", "🤡",
            "小丑竟是我自己。总是在关系中付出更多，最后受伤的还是你。",
            ["付出型", "容易受伤", "舔狗", "自嘲"],
            PET_ARTS["JOKER"], "小丑面具"),
        
        "DIORS": SBTIType("DIORS", "屌丝", "The Loser", "👟",
            "屌丝是你的标签，但你已经习惯了。在平凡中寻找自己的快乐。",
            ["平凡", "自嘲", "接地气", "乐观"],
            PET_ARTS["DIORS"], "屌丝青蛙"),
    }
    
    def __init__(self):
        self.answers: Dict[int, str] = {}
        self.current_question: int = 0
        self.dimensions = {
            "social": 0,
            "emotion": 0,
            "energy": 0,
            "attitude": 0,
            "thinking": 0,
            "bullshit": 0,
            "identity": 0,
            "temper": 0,
            "planning": 0,
        }
    
    def get_current_question(self) -> Question:
        """获取当前题目"""
        if self.current_question < len(self.QUESTIONS):
            return self.QUESTIONS[self.current_question]
        return None
    
    def answer(self, choice: str) -> bool:
        """回答当前题目，choice: 'A', 'B', 'C', 'D'"""
        if self.current_question < len(self.QUESTIONS):
            choice = choice.upper()
            self.answers[self.current_question] = choice
            
            question = self.QUESTIONS[self.current_question]
            if choice == 'A':
                scores = question.scores_a
            elif choice == 'B':
                scores = question.scores_b
            elif choice == 'C':
                scores = question.scores_c
            else:
                scores = question.scores_d
            
            for dim, score in scores.items():
                if dim in self.dimensions:
                    self.dimensions[dim] += score
            
            self.current_question += 1
            return self.current_question < len(self.QUESTIONS)
        return False
    
    def calculate_result(self) -> Tuple[SBTIType, Dict]:
        """计算测试结果"""
        dims = self.dimensions
        
        type_scores = {}
        
        # 自我攻击者：高自卑 + 高感性 + 低自信
        type_scores['IMSB'] = (-dims['identity'] * 2 + dims['emotion'])
        
        # 领导者：高自信 + 高奋斗 + 社牛 + 理性
        type_scores['BOSS'] = (dims['identity'] + dims['attitude'] + 
                               dims['social'] + (-dims['emotion']))
        
        # 妈妈：高感性 + 高关心 + 正经
        type_scores['MUM'] = (dims['emotion'] + (-dims['bullshit']))
        
        # 伪人：中等 + 隐藏真实 + 社交面具
        type_scores['FAKE'] = (abs(dims['identity']) + dims['social'])
        
        # 死者：极度摆烂 + 极度内向 + 无能量
        type_scores['DEAD'] = ((-dims['attitude']) * 2 + (-dims['energy']) * 2)
        
        # 装死者：摆烂 + 逃避
        type_scores['ZZZZ'] = (-dims['attitude'] + (-dims['planning']))
        
        # 行者：高奋斗 + 高外向 + 不停止
        type_scores['GOGO'] = (dims['attitude'] + dims['energy'] + dims['social'])
        
        # 草者：暴躁 + 胡扯
        type_scores['FUCK'] = ((-dims['temper']) + dims['bullshit'])
        
        # 拿捏者：自信 + 社牛 + 冷静 + 计划
        type_scores['CTRL'] = (dims['identity'] + dims['social'] + 
                               dims['temper'] + dims['planning'])
        
        # 傻乐者：高感性 + 随性 + 不暴躁
        type_scores['HHHH'] = (dims['emotion'] + (-dims['planning']) + dims['temper'])
        
        # 尤物：自信 + 社牛 + 感性
        type_scores['SEXY'] = (dims['identity'] + dims['social'] + dims['emotion'])
        
        # 无所谓人：佛系 = 中等一切
        type_scores['OJBK'] = -(abs(dims['social']) + abs(dims['emotion']) + 
                                 abs(dims['attitude']))
        
        # 贫穷者：摆烂 + 无计划 + 内向
        type_scores['POOR'] = (-dims['attitude'] + (-dims['planning']) + 
                               (-dims['social']))
        
        # 哦不人：悲观 = 低自信 + 低冷静
        type_scores['OHNO'] = ((-dims['identity']) + (-dims['temper']))
        
        # 僧人：冷静 + 佛系 + 正经
        type_scores['MONK'] = (dims['temper'] + (-dims['bullshit']) + 
                               (-abs(dims['attitude'])))
        
        # 狗屎人：愤世嫉俗 = 胡扯 + 暴躁
        type_scores['SHIT'] = (dims['bullshit'] + (-dims['temper']))
        
        # 感恩者：感性 + 正经 + 外向
        type_scores['THANK'] = (dims['emotion'] + (-dims['bullshit']) + 
                                dims['social'])
        
        # 吗喽：社畜 = 奋斗 + 内向 + 疲惫
        type_scores['MALO'] = (dims['attitude'] + (-dims['energy']))
        
        # 送钱者：冤种 = 感性 + 随性 + 不太自信
        type_scores['ATM'] = (dims['emotion'] + (-dims['planning']) + 
                              (-dims['identity']))
        
        # 思考者：理性 + 内向 + 计划
        type_scores['THINK'] = ((-dims['emotion']) + (-dims['energy']) + 
                                dims['planning'])
        
        # 孤儿：独来独往 = 极度内向 + 社恐
        type_scores['SOLO'] = ((-dims['energy']) * 2 + (-dims['social']) * 2)
        
        # 多情者：感性 + 社牛 + 不太正经
        type_scores['LOVER'] = (dims['emotion'] + dims['social'] + 
                                dims['bullshit'])
        
        # 握草人：震惊体 = 感性 + 不冷静
        type_scores['WOC'] = (dims['emotion'] + (-dims['temper']))
        
        # 酒鬼：享乐 + 胡扯 + 感性
        type_scores['DRUNK'] = ((-dims['planning']) + dims['bullshit'] + 
                                dims['emotion'])
        
        # 废物：摆烂 + 自卑 + 随性
        type_scores['IMFW'] = ((-dims['attitude']) + (-dims['identity']) + 
                               (-dims['planning']))
        
        # 小丑：付出型 = 感性 + 不太自信
        type_scores['JOKER'] = (dims['emotion'] + (-dims['identity']))
        
        # 屌丝：平凡 = 中等偏下
        type_scores['DIORS'] = -(dims['identity'] + dims['attitude'] + 
                                 dims['social'])
        
        result_type = max(type_scores, key=type_scores.get)
        max_score = type_scores[result_type]
        
        match_score = min(95, max(40, 50 + max_score * 2))
        
        personality = self.PERSONALITY_TYPES[result_type]
        
        analysis = {
            "dimensions": self.dimensions,
            "type_scores": type_scores,
            "match_percentage": match_score,
        }
        
        return personality, analysis
    
    def get_progress(self) -> str:
        return f"{self.current_question + 1} / {len(self.QUESTIONS)}"
    
    def is_complete(self) -> bool:
        return self.current_question >= len(self.QUESTIONS)


def format_result(personality: SBTIType, analysis: Dict) -> str:
    """格式化结果为ASCII艺术风格"""
    lines = []
    lines.append("=" * 60)
    lines.append("🎉 SBTI 梗王版测试完成！")
    lines.append("=" * 60)
    lines.append("")
    lines.append(personality.pet_art)
    lines.append("")
    lines.append(f"    🏷️  类型: {personality.code} - {personality.name}")
    lines.append(f"    📛 英文名: {personality.nickname}")
    lines.append(f"    🎯 匹配度: {analysis['match_percentage']}%")
    lines.append("")
    lines.append("📋 人格描述:")
    lines.append(f"    {personality.description}")
    lines.append("")
    lines.append("✨ 主要特征:")
    for trait in personality.traits:
        lines.append(f"    • {trait}")
    lines.append("")
    
    lines.append("📊 维度分析:")
    dims = analysis['dimensions']
    dim_names = {
        'social': '社交', 'emotion': '感性', 'energy': '外向',
        'attitude': '奋斗', 'thinking': '直觉', 'bullshit': '胡扯',
        'identity': '自信', 'temper': '冷静', 'planning': '计划'
    }
    for dim, name in dim_names.items():
        val = dims[dim]
        bar = "█" * abs(int(val)) + "░" * (4 - abs(int(val)))
        lines.append(f"    {name:4s} [{bar}] {val:+.0f}")
    
    lines.append("")
    lines.append("=" * 60)
    lines.append("⚠️  友情提示：本测试仅供娱乐！")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def run_interactive_test():
    """交互式运行测试"""
    print("=" * 60)
    print("🧠 SBTI 人格测试 V3 - 梗王版")
    print("=" * 60)
    print("\n更接地气的人格类型，更搞笑的描述！")
    print("共30道题，每题4个选项。\n")
    
    test = SBTITestV3()
    
    while not test.is_complete():
        question = test.get_current_question()
        print(f"\n【{test.get_progress()}】{question.text}")
        print(f"  A. {question.option_a}")
        print(f"  B. {question.option_b}")
        print(f"  C. {question.option_c}")
        print(f"  D. {question.option_d}")
        
        while True:
            choice = input("\n你的选择 (A/B/C/D): ").strip().upper()
            if choice in ['A', 'B', 'C', 'D']:
                break
            print("请输入 A, B, C 或 D")
        
        test.answer(choice)
    
    personality, analysis = test.calculate_result()
    print("\n" + format_result(personality, analysis))


if __name__ == "__main__":
    run_interactive_test()
