#!/usr/bin/env python3
"""
SBTI 人格测试 V2 - 电子宠物版

SBTI (Super Bullshit Type Indicator) 
一种基于15个维度的娱乐性人格测试

特性：
- 4个选项（A/B/C/D）更精细的维度划分
- 每种人格对应一个独特的ASCII艺术宠物
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum


class Dimension(Enum):
    """9个核心维度"""
    SOCIAL = "社交倾向"      # 社恐 vs 社牛
    EMOTION = "情绪表达"     # 感性 vs 理性
    ENERGY = "能量来源"      # 内向 vs 外向
    ATTITUDE = "生活态度"    # 摆烂 vs 奋斗
    THINKING = "思维方式"    # 思考 vs 直觉
    BULLSHIT = "说话风格"    # 正经 vs 胡扯
    IDENTITY = "自我认知"    # 自信 vs 自卑
    TEMPER = "脾气控制"      # 暴躁 vs 冷静
    PLANNING = "规划能力"    # 随性 vs 计划


@dataclass
class Question:
    """测试题目 - 4选项版本"""
    id: int
    text: str
    dimensions: List[str]  # 该题影响哪些维度
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    # 每个选项对应的维度得分
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
    pet_art: str  # ASCII艺术宠物
    pet_name: str  # 宠物名字


# ==================== ASCII艺术宠物库 ====================

PET_ARTS = {
    "CTRL": """
    ╭─────────╮
    │  👑 CTRL  │
    ╰────┬────╯
         │
       🎩👑🎩
       ( ͡° ͜ʖ ͡°)
       <⚡️  ⚡️>
        ╱   ╲
       ╱ 👊  ╲
      🕴️  掌控者 🕴️
    """,
    
    "SHIT": """
       💩 SHIT
      ╱     ╲
     │  ಠ_ಠ  │
     │  ╭─╮  │
     │  │ │  │
     ╰──┴─┴──╯
      💨 💨 💨
    愤世嫉俗的小屎球
    """,
    
    "LOVE": """
        💗 LOVE
         💕
        ╱❤️╲
       │💋  │
       (｡♥‿♥｡)
       <❤️ ❤️>
        ╲💖╱
       ╱ 💗 ╲
      恋爱脑小精灵
    """,
    
    "FART": """
        💨 FART
         🎵
       ╭───╮
      │ (o_o) │
      │  ～   │
      ╰──┬──╯
       💨 │ 💨
      💨  │  💨
         🦶
       屁王跳跳
    """,
    
    "BOSS": """
      👔 BOSS
    ╭────────╮
    │ 👔👔👔 │
    │( •̀_•́ )│
    │  💼💼  │
    ╰───┬───╯
       👞👞
     霸道总裁鸭
    """,
    
    "LUCK": """
        🍀 LUCK
          ⭐
       ╭────╮
      │ ✨◕‿◕✨│
      │  🌈   │
      ╰──┬───╯
      🍀 │ 🍀
     🎰  │  🎲
        🦶
       欧皇猫咪
    """,
    
    "WEAK": """
       🥀 WEAK
      ╭─────╮
     │ (´-﹏-`) │
     │   ～～   │
     ╰────┬───╯
      🍂  │  🍂
         🛋️
       摆烂咸鱼
    """,
    
    "KING": """
        👑 KING
         👑
       ╭───╮
      │ 😎 │
      │👑👑👑│
      │  🦁  │
      ╰──┬──╯
       🗡️│🛡️
        👑
      真命天子狮
    """,
    
    "SEXY": """
        💋 SEXY
         🔥
       ╭───╮
      │ 😘 │
      │💃💃💃│
      │  💋  │
      ╰──┬──╯
       👠│👠
        🌹
      性感炸弹狐
    """,
    
    "DADDY": """
       🧔 DADDY
      ╭─────╮
     │ 👔👔👔 │
     │ ( •_•) │
     │  🤝   │
     ╰───┬───╯
      👞│👞
        🎩
      爹系熊
    """,
    
    "MOMMY": """
       👩‍🍳 MOMMY
      ╭─────╮
     │ 🍳🍳🍳 │
     │ (◕‿◕) │
     │  🤱   │
     ╰───┬───╯
      🥿│🥿
        ❤️
      妈系兔
    """,
    
    "BABY": """
        👶 BABY
      ╭──────╮
     │ (◕‿◕) │
     │   🍼   │
     │  👶👶  │
     ╰───┬───╯
       🧸│🧸
         🍼
       宝宝猪
    """,
    
    "FOOD": """
        🍔 FOOD
      ╭──────╮
     │  😋   │
     │ 🍕🍔🍟 │
     │  🍰🍰  │
     ╰───┬───╯
       🍗│🍖
        🥤
      吃货仓鼠
    """,
    
    "SLEEP": """
       😴 SLEEP
      ╭─────╮
     │ (-_-)zzz│
     │   💤   │
     │  🛏️🛏️  │
     ╰───┬───╯
      💤│💤
        🌙
      睡神考拉
    """,
    
    "GAME": """
        🎮 GAME
      ╭──────╮
     │  🤓   │
     │ 🎮🖱️⌨️ │
     │  👓👓  │
     ╰───┬───╯
       🖱️│🎧
        🏆
      游戏宅龙
    """,
    
    "BOOK": """
        📚 BOOK
      ╭──────╮
     │  🤓   │
     │ 📖📖📖 │
     │  👓👓  │
     ╰───┬───╯
       📚│📚
        📝
      书呆子龟
    """,
    
    "MUSIC": """
        🎵 MUSIC
      ╭──────╮
     │  🎤   │
     │ 🎧🎵🎶 │
     │  🎸🎸  │
     ╰───┬───╯
       🎹│🎺
        🎻
      音乐精灵鸟
    """,
    
    "ART": """
        🎨 ART
      ╭──────╮
     │  🧐   │
     │ 🎨🖌️🖼️ │
     │  ✨✨  │
     ╰───┬───╯
       🖌️│🎭
        🎪
      艺术家猫
    """,
    
    "SPORT": """
        🏃 SPORT
      ╭──────╮
     │  💪   │
     │ 🏀⚽🏈 │
     │  🥇🥇  │
     ╰───┬───╯
       👟│👟
        🏆
      运动狂豹
    """,
    
    "MONEY": """
        💰 MONEY
      ╭──────╮
     │  🤑   │
     │ 💵💴💶 │
     │  💰💰  │
     ╰───┬───╯
       💎│💎
        🏦
      财迷鼠
    """,
    
    "CAT": """
        🐱 CAT
      ╭──────╮
     │  😼   │
     │ ╱⧹_⧹╲ │
     │(  o.o  )│
     ╰───┬───╯
       🐾│🐾
        🐟
      猫系喵
    """,
    
    "DOG": """
        🐕 DOG
      ╭──────╮
     │  🐶   │
     │  ╱╲╱╲  │
     │ (◕ᴥ◕) │
     ╰───┬───╯
       🐾│🐾
        🦴
      犬系汪
    """,
    
    "BOBO": """
        🛋️ BOBO
      ╭──────╮
     │  😪   │
     │  🛋️🛋️  │
     │ 💤💤💤 │
     ╰───┬───╯
       🧦│🧦
        📺
      摆烂王蜗牛
    """,
}


class SBTITestV2:
    """SBTI 测试 V2 - 4选项版"""
    
    # 30道测试题目（4选项）
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
    
    # SBTI 人格类型定义 + 宠物
    PERSONALITY_TYPES = {
        "CTRL": SBTIType("CTRL", "拿捏者", "The Controller", "👑",
            "你是一切尽在掌控的拿捏大师。无论是社交场合还是工作场景，你都能精准把握节奏。",
            ["控场能力强", "善于把握时机", "有领导气质", "让人又爱又怕"],
            PET_ARTS["CTRL"], "掌控者狮子"),
        
        "SHIT": SBTIType("SHIT", "愤世者", "The Cynic", "💩",
            "你对这个世界有着独特的见解（通常是负面的）。看什么都不顺眼，但骂得还挺有道理。",
            ["吐槽犀利", "眼光独到", "不随波逐流", "嘴硬心软"],
            PET_ARTS["SHIT"], "愤世小屎球"),
        
        "LOVE": SBTIType("LOVE", "恋爱脑", "The Romantic", "💗",
            "你的世界绕着爱情转。为爱痴狂，为爱哐哐撞大墙。理性是什么？能吃吗？",
            ["情感丰富", "为爱勇敢", "浪漫至上", "容易被感动"],
            PET_ARTS["LOVE"], "恋爱精灵"),
        
        "FART": SBTIType("FART", "屁王", "The Joker", "💨",
            "有你在的地方永远不会冷场。你的幽默感和胡说八道能力让你成为聚会焦点。",
            ["幽默风趣", "善于活跃气氛", "脑洞清奇", "不按套路出牌"],
            PET_ARTS["FART"], "屁王跳跳"),
        
        "BOSS": SBTIType("BOSS", "霸道总裁", "The Boss", "👔",
            "天生的领导者。目标明确，行动果断，让下属（朋友）既敬佩又畏惧。",
            ["气场强大", "执行力强", "目标导向", "说一不二"],
            PET_ARTS["BOSS"], "霸道鸭"),
        
        "LUCK": SBTIType("LUCK", "欧皇", "The Lucky One", "🍀",
            "运气就是你的超能力。做什么都顺风顺水，让人羡慕嫉妒恨。",
            ["运气爆棚", "乐观积极", "机会总是眷顾", "心态好"],
            PET_ARTS["LUCK"], "欧皇猫"),
        
        "WEAK": SBTIType("WEAK", "废物", "The Underdog", "🥀",
            "表面上看起来不太行，但其实...好吧，确实不太行。但废物也有废物的快乐！",
            ["心态平和", "知足常乐", "抗压能力强", "接受自己"],
            PET_ARTS["WEAK"], "摆烂咸鱼"),
        
        "KING": SBTIType("KING", "真命天子", "The Chosen One", "👑",
            "主角光环加身，走到哪都是焦点。自信、魅力、能力，你全都有。",
            ["自信爆棚", "魅力四射", "能力出众", "天生C位"],
            PET_ARTS["KING"], "天子狮"),
        
        "SEXY": SBTIType("SEXY", "性感炸弹", "The Sexy Bomb", "💋",
            "你就是行走的荷尔蒙，走到哪都自带光环。不用刻意，naturally sexy。",
            ["魅力难挡", "自信从容", "吸引力max", "走路带风"],
            PET_ARTS["SEXY"], "性感狐"),
        
        "DADDY": SBTIType("DADDY", "爹系伴侣", "The Daddy", "🧔",
            "你有着超越年龄的成熟和掌控欲，喜欢照顾别人，但也喜欢被依赖。",
            ["成熟稳重", "保护欲强", "掌控欲max", "安全感爆棚"],
            PET_ARTS["DADDY"], "爹系熊"),
        
        "MOMMY": SBTIType("MOMMY", "妈系伴侣", "The Mommy", "👩‍🍳",
            "你的母性光辉照耀四方，照顾人是你的本能，唠叨也是。",
            ["温柔体贴", "照顾欲强", "事无巨细", "让人又想逃又想依赖"],
            PET_ARTS["MOMMY"], "妈系兔"),
        
        "BABY": SBTIType("BABY", "宝宝", "The Baby", "👶",
            "世界那么大，但你想当被宠坏的小孩。撒娇卖萌是你的武器。",
            ["天真烂漫", "依赖性强", "可爱即是正义", "让人想保护"],
            PET_ARTS["BABY"], "宝宝猪"),
        
        "FOOD": SBTIType("FOOD", "吃货", "The Foodie", "🍔",
            "你的人生信条：没有什么是一顿美食解决不了的，如果有，就两顿。",
            ["味蕾敏感", "生活因美食而美好", "看到吃的就开心", "容易满足"],
            PET_ARTS["FOOD"], "吃货仓鼠"),
        
        "SLEEP": SBTIType("SLEEP", "睡神", "The Sleep Master", "😴",
            "如果睡觉是 Olympic 项目，你一定能拿金牌。床才是你的真爱。",
            ["随时随地能睡", "起床困难户", "梦境比现实精彩", "充电模式长"],
            PET_ARTS["SLEEP"], "睡神考拉"),
        
        "GAME": SBTIType("GAME", "游戏宅", "The Gamer", "🎮",
            "虚拟世界比现实更真实，游戏里的你才是完全体。",
            ["操作犀利", "反应神速", "团队配合好", "现实生活稍显社恐"],
            PET_ARTS["GAME"], "游戏龙"),
        
        "BOOK": SBTIType("BOOK", "书呆子", "The Bookworm", "📚",
            "书中自有颜如玉，书中自有黄金屋。你比别人多活了几辈子。",
            ["知识渊博", "思考深邃", "独处也快乐", "偶尔显得不合群"],
            PET_ARTS["BOOK"], "书呆龟"),
        
        "MUSIC": SBTIType("MUSIC", "音乐精灵", "The Music Spirit", "🎵",
            "音乐是你的灵魂语言，没有音乐的世界是黑白的。",
            ["节奏感强", "情感丰富", "艺术气质", "容易共情"],
            PET_ARTS["MUSIC"], "音乐鸟"),
        
        "ART": SBTIType("ART", "艺术家", "The Artist", "🎨",
            "你看到的是别人看不到的美，你活在自己的审美世界里。",
            ["审美独特", "创意无限", "追求完美", "偶尔不切实际"],
            PET_ARTS["ART"], "艺术猫"),
        
        "SPORT": SBTIType("SPORT", "运动狂", "The Sportsman", "🏃",
            "生命在于运动，多巴胺是你的快乐源泉，肌肉是你的勋章。",
            ["精力充沛", "自律严格", "挑战极限", "阳光积极"],
            PET_ARTS["SPORT"], "运动豹"),
        
        "MONEY": SBTIType("MONEY", "财迷", "The Money Lover", "💰",
            "你的终极目标是财务自由，赚钱是你的游戏，数字是你的得分。",
            ["理财高手", "商业嗅觉敏锐", "数字敏感", "目标明确"],
            PET_ARTS["MONEY"], "财迷鼠"),
        
        "CAT": SBTIType("CAT", "猫系", "The Cat", "🐱",
            "高冷、独立、优雅，需要时粘人，不需要时勿扰。",
            ["独立自主", "优雅从容", "偶尔高冷", "需要自己的空间"],
            PET_ARTS["CAT"], "猫系喵"),
        
        "DOG": SBTIType("DOG", "犬系", "The Dog", "🐕",
            "忠诚、热情、粘人，你是最棒的伙伴，永远支持身边的人。",
            ["忠诚可靠", "热情开朗", "容易满足", "最佳伙伴"],
            PET_ARTS["DOG"], "犬系汪"),
        
        "BOBO": SBTIType("BOBO", "摆烂王", "The Bobo", "🛋️",
            "你已经达到摆烂的最高境界：心安理得地躺平，还觉得自己挺对。",
            ["心态极佳", "压力免疫", "知足常乐", "活着就好"],
            PET_ARTS["BOBO"], "摆烂蜗牛"),
    }
    
    def __init__(self):
        self.answers: Dict[int, str] = {}
        self.current_question: int = 0
        self.dimensions = {
            "social": 0,      # -2到+2
            "emotion": 0,     # -2到+2 (感性到理性)
            "energy": 0,      # -2到+2
            "attitude": 0,    # -2到+2 (摆烂到奋斗)
            "thinking": 0,    # -2到+2 (直觉到思考)
            "bullshit": 0,    # -2到+2 (正经到胡扯)
            "identity": 0,    # -2到+2
            "temper": 0,      # -2到+2 (暴躁到冷静)
            "planning": 0,    # -2到+2 (随性到计划)
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
            
            # 更新维度得分
            question = self.QUESTIONS[self.current_question]
            if choice == 'A':
                scores = question.scores_a
            elif choice == 'B':
                scores = question.scores_b
            elif choice == 'C':
                scores = question.scores_c
            else:  # D
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
        
        # 每种人格类型的评分逻辑
        type_scores = {}
        
        # CTRL: 社牛 + 理性 + 冷静 + 自信 + 计划
        type_scores['CTRL'] = (dims['social'] + dims['energy'] + 
                               (-dims['emotion']) + dims['temper'] + 
                               dims['identity'] + dims['planning'])
        
        # SHIT: 胡扯 + 暴躁 + 社恐
        type_scores['SHIT'] = (dims['bullshit'] + (-dims['temper']) + 
                               (-dims['social']))
        
        # LOVE: 感性 + 随性 + 社牛
        type_scores['LOVE'] = (dims['emotion'] + (-dims['planning']) + 
                               dims['social'] + dims['energy'])
        
        # FART: 胡扯 + 随性 + 感性
        type_scores['FART'] = (dims['bullshit'] + (-dims['planning']) + 
                               dims['emotion'])
        
        # BOSS: 奋斗 + 理性 + 自信 + 计划
        type_scores['BOSS'] = (dims['attitude'] + (-dims['emotion']) + 
                               dims['identity'] + dims['planning'])
        
        # LUCK: 自信 + 社牛 + 随性 + 感性
        type_scores['LUCK'] = (dims['identity'] + dims['social'] + 
                               (-dims['planning']) + dims['emotion'])
        
        # WEAK: 摆烂 + 自卑 + 随性
        type_scores['WEAK'] = (-dims['attitude'] + (-dims['identity']) + 
                               (-dims['planning']))
        
        # KING: 社牛 + 自信 + 奋斗 + 社牛
        type_scores['KING'] = (dims['social'] + dims['identity'] + 
                               dims['attitude'] + dims['energy'] * 2)
        
        # SEXY: 社牛 + 自信 + 感性 + 胡扯
        type_scores['SEXY'] = (dims['social'] + dims['identity'] + 
                               dims['emotion'] + dims['bullshit'])
        
        # DADDY: 理性 + 冷静 + 自信 + 正经
        type_scores['DADDY'] = ((-dims['emotion']) + dims['temper'] + 
                                dims['identity'] + (-dims['bullshit']))
        
        # MOMMY: 感性 + 自信 + 正经 + 社牛
        type_scores['MOMMY'] = (dims['emotion'] + dims['identity'] + 
                                (-dims['bullshit']) + dims['social'])
        
        # BABY: 感性 + 自卑 + 摆烂
        type_scores['BABY'] = (dims['emotion'] + (-dims['identity']) + 
                               (-dims['attitude']))
        
        # FOOD: 摆烂 + 随性 + 感性
        type_scores['FOOD'] = ((-dims['attitude']) + (-dims['planning']) + 
                               dims['emotion'])
        
        # SLEEP: 摆烂 + 内向 + 随性
        type_scores['SLEEP'] = ((-dims['attitude']) + (-dims['energy']) + 
                                (-dims['planning']))
        
        # GAME: 内向 + 随性 + 理性
        type_scores['GAME'] = ((-dims['energy']) + (-dims['planning']) + 
                               (-dims['emotion']))
        
        # BOOK: 内向 + 正经 + 理性
        type_scores['BOOK'] = ((-dims['energy']) + (-dims['bullshit']) + 
                               (-dims['emotion']))
        
        # MUSIC: 感性 + 随性 + 社牛
        type_scores['MUSIC'] = (dims['emotion'] + (-dims['planning']) + 
                                dims['social'])
        
        # ART: 感性 + 胡扯 + 内向
        type_scores['ART'] = (dims['emotion'] + dims['bullshit'] + 
                              (-dims['energy']))
        
        # SPORT: 奋斗 + 社牛 + 自信
        type_scores['SPORT'] = (dims['attitude'] + dims['social'] + 
                                dims['identity'])
        
        # MONEY: 理性 + 奋斗 + 正经 + 计划
        type_scores['MONEY'] = ((-dims['emotion']) + dims['attitude'] + 
                                (-dims['bullshit']) + dims['planning'])
        
        # CAT: 内向 + 摆烂 + 冷静 + 社恐
        type_scores['CAT'] = ((-dims['energy']) + (-dims['attitude']) + 
                              dims['temper'] + (-dims['social']))
        
        # DOG: 社牛 + 感性 + 自卑 + 热情
        type_scores['DOG'] = (dims['social'] + dims['emotion'] + 
                              (-dims['identity']) + dims['energy'])
        
        # BOBO: 摆烂 + 随性
        type_scores['BOBO'] = ((-dims['attitude']) * 2 + 
                               (-dims['planning']) * 2)
        
        # 找到最高分类型
        result_type = max(type_scores, key=type_scores.get)
        max_score = type_scores[result_type]
        
        # 计算匹配度 (40-95%)
        match_score = min(95, max(40, 50 + max_score * 3))
        
        personality = self.PERSONALITY_TYPES[result_type]
        
        analysis = {
            "dimensions": self.dimensions,
            "type_scores": type_scores,
            "match_percentage": match_score,
        }
        
        return personality, analysis
    
    def get_progress(self) -> str:
        """获取测试进度"""
        return f"{self.current_question + 1} / {len(self.QUESTIONS)}"
    
    def is_complete(self) -> bool:
        """测试是否完成"""
        return self.current_question >= len(self.QUESTIONS)


def format_result(personality: SBTIType, analysis: Dict) -> str:
    """格式化结果为ASCII艺术风格"""
    lines = []
    lines.append("=" * 60)
    lines.append("🎉 SBTI 人格测试完成！")
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
    
    # 维度雷达图（ASCII简易版）
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
        direction = "+" if val > 0 else "-" if val < 0 else "="
        lines.append(f"    {name:4s} [{bar}] {val:+.0f}")
    
    lines.append("")
    lines.append("=" * 60)
    lines.append("⚠️  友情提示：本测试仅供娱乐！")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def run_interactive_test():
    """交互式运行测试"""
    print("=" * 60)
    print("🧠 SBTI 人格测试 V2 - 电子宠物版")
    print("=" * 60)
    print("\nMBTI已经过时，SBTI来了！")
    print("共30道题，每题4个选项，更精准的人格分析。\n")
    
    test = SBTITestV2()
    
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
    
    # 显示结果
    personality, analysis = test.calculate_result()
    print("\n" + format_result(personality, analysis))


if __name__ == "__main__":
    run_interactive_test()
