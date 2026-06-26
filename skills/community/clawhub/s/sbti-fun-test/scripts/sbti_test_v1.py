#!/usr/bin/env python3
"""
SBTI 人格测试 - 娱乐版性格测试

SBTI (Super Bullshit Type Indicator) 
一种基于15个维度的娱乐性人格测试

原作者：B站@蛆肉儿串儿
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum


class Dimension(Enum):
    """15个测试维度"""
    SOCIAL = "社交倾向"  # S - 社恐 vs A - 社牛
    EMOTION = "情绪表达"  # F - 感性 vs R - 理性
    ENERGY = "能量来源"  # I - 内向 vs E - 外向
    ATTITUDE = "生活态度"  # P - 摆烂 vs N - 奋斗
    THINKING = "思维方式"  # T - 思考 vs V - 直觉
    BULLSHIT = "胡说八道"  # B - 正经 vs H - 胡扯
    IDENTITY = "自我认知"  # I - 自信 vs S - 自卑
    TEMPER = "脾气控制"  # T - 暴躁 vs C - 冷静
    YOLO = "活在当下"  # Y - 享乐 vs P - 规划
    

@dataclass
class Question:
    """测试题目"""
    id: int
    text: str
    dimension: str
    option_a: str  # 偏向第一个字母
    option_b: str  # 偏向第二个字母
    weight: int = 1


@dataclass
class SBTIType:
    """SBTI人格类型"""
    code: str
    name: str
    nickname: str
    description: str
    traits: List[str]
    match_percentage: int


class SBTITest:
    """SBTI 测试主类"""
    
    # 31道测试题目
    QUESTIONS = [
        # 维度1: S(社恐) vs A(社牛)
        Question(1, "周末有人约你出去玩，你的反应是？", "SA", "太好了，马上出发！", "能推就推，在家躺着真香", 2),
        Question(2, "在聚会上，你通常", "SA", "主动找话题，成为焦点", "躲在角落，希望没人注意到我", 2),
        Question(3, "面对陌生人搭话，你会", "SA", "热情地聊起来", "礼貌性点头，心里想着怎么结束对话", 1),
        
        # 维度2: F(感性) vs R(理性)
        Question(4, "做决定时，你更依赖", "FR", "直觉和感受", "逻辑和数据", 2),
        Question(5, "看电影时，你更容易", "FR", "被情节感动得稀里哗啦", "分析剧情bug和逻辑漏洞", 2),
        Question(6, "朋友失恋找你哭诉，你会", "FR", "陪他一起哭，给予情感支持", "帮他分析问题，给出解决方案", 1),
        
        # 维度3: I(内向) vs E(外向)
        Question(7, "你的能量来源是", "IE", "独处时光，安静思考", "社交活动，与人互动", 2),
        Question(8, "工作需要团队协作时，你", "IE", "更喜欢独立完成任务", "享受头脑风暴的过程", 2),
        Question(9, "描述自己时，你倾向于", "IE", "倾听多于表达", "表达多于倾听", 1),
        
        # 维度4: P(摆烂) vs N(奋斗)
        Question(10, "面对deadline，你通常", "PN", "提前完成，甚至超额完成", "最后一天才开始，卡点交", 2),
        Question(11, "对于人生规划，你的态度是", "PN", "顺其自然，船到桥头自然直", "要有明确目标和详细计划", 2),
        Question(12, "遇到难题时，你会", "PN", "先放一边，玩会儿再说", "立即着手解决", 1),
        
        # 维度5: T(思考) vs V(直觉)
        Question(13, "学习新技能，你更喜欢", "TV", "系统学习理论知识", "直接上手，边做边学", 2),
        Question(14, "面对未知情况，你倾向于", "TV", "先研究清楚再行动", "凭直觉先试试看", 2),
        Question(15, "你更相信", "TV", "经验和实证", "灵感和预感", 1),
        
        # 维度6: B(正经) vs H(胡扯)
        Question(16, "开玩笑的尺度，你", "BH", "很有分寸，从不越界", "没有边界，啥都敢说", 2),
        Question(17, "朋友说你", "BH", "靠谱稳重", "神经病一个", 2),
        Question(18, "在严肃场合，你会", "BH", "保持正经", "忍不住想皮一下", 1),
        
        # 维度7: I(自信) vs S(自卑)
        Question(19, "照镜子时，你觉得", "IS", "老子天下第一帅", "这是哪里来的丑东西", 2),
        Question(20, "面对挑战，你的第一反应", "IS", "我可以！", "我不行...", 2),
        Question(21, "被人夸奖时，你会", "IS", "坦然接受，说谢谢", "觉得对方在客套", 1),
        
        # 维度8: T(暴躁) vs C(冷静)
        Question(22, "遇到糟心事，你会", "TC", "当场爆炸", "心平气和处理", 2),
        Question(23, "排队被人插队，你会", "TC", "直接怼回去", "算了算了", 2),
        Question(24, "游戏输了，你", "TC", " rage quit", "再来一局", 1),
        
        # 维度9: Y(享乐) vs P(规划)
        Question(25, "有钱到手，你会", "YP", "马上花掉，享受当下", "存起来，为未来打算", 2),
        Question(26, "对于生活，你认为", "YP", "及时行乐最重要", "要为将来做准备", 2),
        Question(27, "周末安排，你更喜欢", "YP", "随机应变，走到哪算哪", "提前计划好每一分钟", 1),
        
        # 混合维度题目
        Question(28, "如果世界末日，你会", "MX", "和爱的人在一起度过", "疯狂一把，想干啥干啥", 1),
        Question(29, "描述理想生活", "MX", "平淡安稳，岁月静好", "跌宕起伏，精彩纷呈", 1),
        Question(30, "你认为自己的本质是", "MX", "一个好人", "一个混蛋", 1),
        Question(31, "做完这个测试，你觉得自己", "MX", "被看穿了", "什么玩意儿", 1),
    ]
    
    # SBTI 人格类型定义
    PERSONALITY_TYPES = {
        "CTRL": SBTIType(
            "CTRL", "拿捏者", "The Controller",
            "你是一切尽在掌控的拿捏大师。无论是社交场合还是工作场景，你都能精准把握节奏，让事情按你的意愿发展。",
            ["控场能力强", "善于把握时机", "有领导气质", "让人又爱又怕"],
            85
        ),
        "SHIT": SBTIType(
            "SHIT", "愤世者", "The Cynic",
            "你对这个世界有着独特的见解（通常是负面的）。看什么都不顺眼，但骂得还挺有道理。",
            ["吐槽犀利", "眼光独到", "不随波逐流", "嘴硬心软"],
            78
        ),
        "LOVE": SBTIType(
            "LOVE", "恋爱脑", "The Romantic",
            "你的世界绕着爱情转。为爱痴狂，为爱哐哐撞大墙。理性是什么？能吃吗？",
            ["情感丰富", "为爱勇敢", "浪漫至上", "容易被感动"],
            72
        ),
        "FART": SBTIType(
            "FART", "屁王", "The Joker",
            "有你在的地方永远不会冷场。你的幽默感和胡说八道能力让你成为聚会焦点。",
            ["幽默风趣", "善于活跃气氛", "脑洞清奇", "不按套路出牌"],
            88
        ),
        "BOSS": SBTIType(
            "BOSS", "霸道总裁", "The Boss",
            "天生的领导者。目标明确，行动果断，让下属（朋友）既敬佩又畏惧。",
            ["气场强大", "执行力强", "目标导向", "说一不二"],
            90
        ),
        "LUCK": SBTIType(
            "LUCK", "欧皇", "The Lucky One",
            "运气就是你的超能力。做什么都顺风顺水，让人羡慕嫉妒恨。",
            ["运气爆棚", "乐观积极", "机会总是眷顾", "心态好"],
            75
        ),
        "WEAK": SBTIType(
            "WEAK", "废物", "The Underdog",
            "表面上看起来不太行，但其实...好吧，确实不太行。但废物也有废物的快乐！",
            ["心态平和", "知足常乐", "抗压能力强", "接受自己"],
            65
        ),
        "KING": SBTIType(
            "KING", "真命天子", "The Chosen One",
            "主角光环加身，走到哪都是焦点。自信、魅力、能力，你全都有。",
            ["自信爆棚", "魅力四射", "能力出众", "天生C位"],
            92
        ),
        "SEXY": SBTIType(
            "SEXY", "性感炸弹", "The Sexy Bomb",
            "你就是行走的荷尔蒙，走到哪都自带光环。不用刻意， naturally sexy。",
            ["魅力难挡", "自信从容", "吸引力max", "走路带风"],
            88
        ),
        "DADDY": SBTIType(
            "DADDY", "爹系伴侣", "The Daddy",
            "你有着超越年龄的成熟和掌控欲，喜欢照顾别人，但也喜欢被依赖。",
            ["成熟稳重", "保护欲强", "掌控欲max", "安全感爆棚"],
            82
        ),
        "MOMMY": SBTIType(
            "MOMMY", "妈系伴侣", "The Mommy",
            "你的母性光辉照耀四方，照顾人是你的本能，唠叨也是。",
            ["温柔体贴", "照顾欲强", "事无巨细", "让人又想逃又想依赖"],
            80
        ),
        "BABY": SBTIType(
            "BABY", "宝宝", "The Baby",
            "世界那么大，但你想当被宠坏的小孩。撒娇卖萌是你的武器。",
            ["天真烂漫", "依赖性强", "可爱即是正义", "让人想保护"],
            75
        ),
        "FOOD": SBTIType(
            "FOOD", "吃货", "The Foodie",
            "你的人生信条：没有什么是一顿美食解决不了的，如果有，就两顿。",
            ["味蕾敏感", "生活因美食而美好", "看到吃的就开心", "容易满足"],
            70
        ),
        "SLEEP": SBTIType(
            "SLEEP", "睡神", "The Sleep Master",
            "如果睡觉是 Olympic 项目，你一定能拿金牌。床才是你的真爱。",
            ["随时随地能睡", "起床困难户", "梦境比现实精彩", "充电模式长"],
            68
        ),
        "GAME": SBTIType(
            "GAME", "游戏宅", "The Gamer",
            "虚拟世界比现实更真实，游戏里的你才是完全体。",
            ["操作犀利", "反应神速", "团队配合好", "现实生活稍显社恐"],
            72
        ),
        "BOOK": SBTIType(
            "BOOK", "书呆子", "The Bookworm",
            "书中自有颜如玉，书中自有黄金屋。你比别人多活了几辈子。",
            ["知识渊博", "思考深邃", "独处也快乐", "偶尔显得不合群"],
            74
        ),
        "MUSIC": SBTIType(
            "MUSIC", "音乐精灵", "The Music Spirit",
            "音乐是你的灵魂语言，没有音乐的世界是黑白的。",
            ["节奏感强", "情感丰富", "艺术气质", "容易共情"],
            76
        ),
        "ART": SBTIType(
            "ART", "艺术家", "The Artist",
            "你看到的是别人看不到的美，你活在自己的审美世界里。",
            ["审美独特", "创意无限", "追求完美", "偶尔不切实际"],
            78
        ),
        "SPORT": SBTIType(
            "SPORT", "运动狂", "The Sportsman",
            "生命在于运动，多巴胺是你的快乐源泉，肌肉是你的勋章。",
            ["精力充沛", "自律严格", "挑战极限", "阳光积极"],
            81
        ),
        "MONEY": SBTIType(
            "MONEY", "财迷", "The Money Lover",
            "你的终极目标是财务自由，赚钱是你的游戏，数字是你的得分。",
            ["理财高手", "商业嗅觉敏锐", "数字敏感", "目标明确"],
            73
        ),
        "CAT": SBTIType(
            "CAT", "猫系", "The Cat",
            "高冷、独立、优雅，需要时粘人，不需要时勿扰。",
            ["独立自主", "优雅从容", "偶尔高冷", "需要自己的空间"],
            77
        ),
        "DOG": SBTIType(
            "DOG", "犬系", "The Dog",
            "忠诚、热情、粘人，你是最棒的伙伴，永远支持身边的人。",
            ["忠诚可靠", "热情开朗", "容易满足", "最佳伙伴"],
            79
        ),
        "BOBO": SBTIType(
            "BOBO", "摆烂王", "The Bobo",
            "你已经达到摆烂的最高境界：心安理得地躺平，还觉得自己挺对。",
            ["心态极佳", "压力免疫", "知足常乐", "活着就好"],
            66
        ),
    }
    
    def __init__(self):
        self.answers: Dict[int, str] = {}
        self.current_question: int = 0
    
    def get_current_question(self) -> Question:
        """获取当前题目"""
        if self.current_question < len(self.QUESTIONS):
            return self.QUESTIONS[self.current_question]
        return None
    
    def answer(self, choice: str) -> bool:
        """
        回答当前题目
        choice: 'A' 或 'B'
        返回: 是否还有下一题
        """
        if self.current_question < len(self.QUESTIONS):
            self.answers[self.current_question] = choice.upper()
            self.current_question += 1
            return self.current_question < len(self.QUESTIONS)
        return False
    
    def calculate_result(self) -> Tuple[SBTIType, Dict]:
        """计算测试结果"""
        # 统计各维度得分
        dimensions = {
            'S': 0, 'A': 0,  # 社恐 vs 社牛
            'F': 0, 'R': 0,  # 感性 vs 理性
            'I': 0, 'E': 0,  # 内向 vs 外向
            'P': 0, 'N': 0,  # 摆烂 vs 奋斗
            'T': 0, 'V': 0,  # 思考 vs 直觉
            'B': 0, 'H': 0,  # 正经 vs 胡扯
            'I2': 0, 'S2': 0,  # 自信 vs 自卑
            'T2': 0, 'C': 0,  # 暴躁 vs 冷静
            'Y': 0, 'P2': 0,  # 享乐 vs 规划
        }
        
        for qid, answer in self.answers.items():
            question = self.QUESTIONS[qid]
            dim = question.dimension
            weight = question.weight
            
            # 记录答案
            if dim == 'SA':
                if answer == 'A':
                    dimensions['S'] += weight
                else:
                    dimensions['A'] += weight
            elif dim == 'FR':
                if answer == 'A':
                    dimensions['F'] += weight
                else:
                    dimensions['R'] += weight
            elif dim == 'IE':
                if answer == 'A':
                    dimensions['I'] += weight
                else:
                    dimensions['E'] += weight
            elif dim == 'PN':
                if answer == 'A':
                    dimensions['P'] += weight
                else:
                    dimensions['N'] += weight
            elif dim == 'TV':
                if answer == 'A':
                    dimensions['T'] += weight
                else:
                    dimensions['V'] += weight
            elif dim == 'BH':
                if answer == 'A':
                    dimensions['B'] += weight
                else:
                    dimensions['H'] += weight
            elif dim == 'IS':
                if answer == 'A':
                    dimensions['I2'] += weight
                else:
                    dimensions['S2'] += weight
            elif dim == 'TC':
                if answer == 'A':
                    dimensions['T2'] += weight
                else:
                    dimensions['C'] += weight
            elif dim == 'YP':
                if answer == 'A':
                    dimensions['Y'] += weight
                else:
                    dimensions['P2'] += weight
        
        # 确定人格类型（简化版算法）
        # 根据得分模式匹配最接近的类型
        type_scores = {
            'CTRL': 0,
            'SHIT': 0,
            'LOVE': 0,
            'FART': 0,
            'BOSS': 0,
            'LUCK': 0,
            'WEAK': 0,
            'KING': 0,
            'SEXY': 0,
            'DADDY': 0,
            'MOMMY': 0,
            'BABY': 0,
            'FOOD': 0,
            'SLEEP': 0,
            'GAME': 0,
            'BOOK': 0,
            'MUSIC': 0,
            'ART': 0,
            'SPORT': 0,
            'MONEY': 0,
            'CAT': 0,
            'DOG': 0,
            'BOBO': 0,
        }
        
        # CTRL: 高社牛 + 高理性 + 高自信 + 高控制
        type_scores['CTRL'] = dimensions['A'] + dimensions['R'] + dimensions['I2'] + dimensions['C']
        
        # SHIT: 高胡扯 + 高愤世 + 混合
        type_scores['SHIT'] = dimensions['H'] + dimensions['T2'] + dimensions['S2']
        
        # LOVE: 高感性 + 高享乐 + 高外向
        type_scores['LOVE'] = dimensions['F'] + dimensions['Y'] + dimensions['E']
        
        # FART: 高胡扯 + 高享乐 + 低正经
        type_scores['FART'] = dimensions['H'] + dimensions['Y'] - dimensions['B']
        
        # BOSS: 高奋斗 + 高理性 + 高自信
        type_scores['BOSS'] = dimensions['N'] + dimensions['R'] + dimensions['I2']
        
        # LUCK: 高自信 + 高外向 + 高享乐
        type_scores['LUCK'] = dimensions['I2'] + dimensions['E'] + dimensions['Y']
        
        # WEAK: 高摆烂 + 低自信 + 低奋斗
        type_scores['WEAK'] = dimensions['P'] + dimensions['S2'] - dimensions['N']
        
        # KING: 高社牛 + 高自信 + 高外向 + 高奋斗
        type_scores['KING'] = dimensions['A'] + dimensions['I2'] + dimensions['E'] + dimensions['N']
        
        # SEXY: 高社牛 + 高自信 + 高外向 + 感性
        type_scores['SEXY'] = dimensions['A'] + dimensions['I2'] + dimensions['E'] + dimensions['F']
        
        # DADDY: 高理性 + 高控制 + 高自信 + 正经
        type_scores['DADDY'] = dimensions['R'] + dimensions['C'] + dimensions['I2'] + dimensions['B']
        
        # MOMMY: 高感性 + 高自信 + 正经 + 外向
        type_scores['MOMMY'] = dimensions['F'] + dimensions['I2'] + dimensions['B'] + dimensions['E']
        
        # BABY: 高感性 + 依赖 + 低自信 + 感性
        type_scores['BABY'] = dimensions['F'] + dimensions['S2'] * 2
        
        # FOOD: 高享乐 + 摆烂 + 感性
        type_scores['FOOD'] = dimensions['Y'] + dimensions['P'] + dimensions['F']
        
        # SLEEP: 高摆烂 + 内向 + 享乐
        type_scores['SLEEP'] = dimensions['P'] + dimensions['I'] + dimensions['Y']
        
        # GAME: 高内向 + 享乐 + 理性
        type_scores['GAME'] = dimensions['I'] + dimensions['Y'] + dimensions['R']
        
        # BOOK: 高内向 + 正经 + 理性
        type_scores['BOOK'] = dimensions['I'] + dimensions['B'] + dimensions['R']
        
        # MUSIC: 高感性 + 享乐 + 外向
        type_scores['MUSIC'] = dimensions['F'] + dimensions['Y'] + dimensions['E']
        
        # ART: 高感性 + 胡扯 + 内向
        type_scores['ART'] = dimensions['F'] + dimensions['H'] + dimensions['I']
        
        # SPORT: 高奋斗 + 外向 + 自信
        type_scores['SPORT'] = dimensions['N'] + dimensions['E'] + dimensions['I2']
        
        # MONEY: 高理性 + 奋斗 + 正经
        type_scores['MONEY'] = dimensions['R'] + dimensions['N'] + dimensions['B']
        
        # CAT: 高内向 + 独立(摆烂) + 冷静
        type_scores['CAT'] = dimensions['I'] + dimensions['P'] + dimensions['C']
        
        # DOG: 高外向 + 感性 + 依赖(低自信)
        type_scores['DOG'] = dimensions['E'] + dimensions['F'] + dimensions['S2']
        
        # BOBO: 高摆烂 + 低奋斗 + 享乐
        type_scores['BOBO'] = dimensions['P'] * 2 + dimensions['Y'] - dimensions['N']
        
        # 找到最高分类型
        result_type = max(type_scores, key=type_scores.get)
        match_score = min(95, 60 + type_scores[result_type] * 2)
        
        # 生成详细分析
        analysis = {
            "dimensions": {
                "社交倾向": f"{'社恐' if dimensions['S'] > dimensions['A'] else '社牛'} ({max(dimensions['S'], dimensions['A'])}分)",
                "情绪表达": f"{'感性' if dimensions['F'] > dimensions['R'] else '理性'} ({max(dimensions['F'], dimensions['R'])}分)",
                "能量来源": f"{'内向' if dimensions['I'] > dimensions['E'] else '外向'} ({max(dimensions['I'], dimensions['E'])}分)",
                "生活态度": f"{'摆烂' if dimensions['P'] > dimensions['N'] else '奋斗'} ({max(dimensions['P'], dimensions['N'])}分)",
                "胡说八道": f"{'正经' if dimensions['B'] > dimensions['H'] else '胡扯'} ({max(dimensions['B'], dimensions['H'])}分)",
                "自我认知": f"{'自信' if dimensions['I2'] > dimensions['S2'] else '自卑'} ({max(dimensions['I2'], dimensions['S2'])}分)",
            },
            "type_scores": type_scores,
            "match_percentage": match_score,
        }
        
        personality = self.PERSONALITY_TYPES[result_type]
        # 更新匹配度
        personality.match_percentage = match_score
        
        return personality, analysis
    
    def get_progress(self) -> str:
        """获取测试进度"""
        return f"{self.current_question} / {len(self.QUESTIONS)}"
    
    def is_complete(self) -> bool:
        """测试是否完成"""
        return self.current_question >= len(self.QUESTIONS)


def run_interactive_test():
    """交互式运行测试"""
    print("=" * 60)
    print("🧠 SBTI 人格测试")
    print("=" * 60)
    print("\nMBTI已经过时，SBTI来了！")
    print("共31道题，全选完才会放行。\n")
    
    test = SBTITest()
    
    while not test.is_complete():
        question = test.get_current_question()
        print(f"\n【{test.get_progress()}】{question.text}")
        print(f"  A. {question.option_a}")
        print(f"  B. {question.option_b}")
        
        while True:
            choice = input("\n你的选择 (A/B): ").strip().upper()
            if choice in ['A', 'B']:
                break
            print("请输入 A 或 B")
        
        test.answer(choice)
    
    # 显示结果
    print("\n" + "=" * 60)
    print("🎉 测试完成！")
    print("=" * 60)
    
    personality, analysis = test.calculate_result()
    
    print(f"\n你的 SBTI 类型: {personality.code}")
    print(f"名称: {personality.name}")
    print(f"英文名: {personality.nickname}")
    print(f"匹配度: {personality.match_percentage}%")
    
    print(f"\n📋 人格描述:")
    print(personality.description)
    
    print(f"\n✨ 主要特征:")
    for trait in personality.traits:
        print(f"  • {trait}")
    
    print(f"\n📊 维度分析:")
    for dim, value in analysis["dimensions"].items():
        print(f"  {dim}: {value}")
    
    print("\n" + "=" * 60)
    print("⚠️  友情提示：本测试仅供娱乐，别拿它当诊断、")
    print("    面试、相亲、分手、招魂、算命或人生判决书。")
    print("=" * 60)


if __name__ == "__main__":
    run_interactive_test()
