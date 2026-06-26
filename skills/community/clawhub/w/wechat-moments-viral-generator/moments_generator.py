# 微信朋友圈爆款文案生成器 - 核心生成逻辑
import json
import random

STYLES = {
    "reseller": {
        "name": "微商出货",
        "emoji_set": ["💰", "📈", "🔥", "✨", "👇", "👏", "🤝", "💯", "🎁", "⚡"],
        "hook_type": "晒收入/制造稀缺/代理裂变",
        "suitable": ["产品推广", "招商加盟", "出货喜报"]
    },
    "promote": {
        "name": "种草安利",
        "emoji_set": ["💄", "✨", "👀", "🔥", "👍", "💕", "🎀", "😍", "💯", "👏"],
        "hook_type": "真实体验/对比反差/场景代入",
        "suitable": ["美妆护肤", "数码产品", "生活好物"]
    },
    "personal_ip": {
        "name": "个人IP",
        "emoji_set": ["🌟", "💪", "📚", "🎯", "✨", "💡", "🚀", "🔥", "👇", "🤝"],
        "hook_type": "个人成长/价值观输出/身份认同",
        "suitable": ["个人品牌", "知识博主", "创业者"]
    },
    "motivational": {
        "name": "励志鸡血",
        "emoji_set": ["💪", "🔥", "🚀", "🌟", "⚡", "✨", "💯", "🎯", "🏆", "👊"],
        "hook_type": "逆境反转/成就晒单/赋能激励",
        "suitable": ["早安打卡", "目标宣言", "成就庆祝"]
    },
    "flash_sale": {
        "name": "限时促销",
        "emoji_set": ["⏰", "🔥", "💥", "📢", "⚡", "🎁", "👇", "💰", "🚨", "✨"],
        "hook_type": "倒计时/名额有限/价格锚点",
        "suitable": ["促销活动", "清仓甩卖", "新品首发"]
    }
}

RESELLER_TEMPLATES = [
    "恭喜团队小伙伴🎉 又出单了！\n\nXX姐加入第XX天，终于是小老板了👍\n\n她说：'以前总觉得微商丢人，现在发现穷人还端着才丢人'💰\n\n想改变现状的姐妹，评论区扣'想赚钱'👇",
    "昨晚2点还在打包📦\n\n今天发出XX单，每一单都是信任💕\n\n我做微商5年，最深的感悟：\n👉不是刷屏就能赚钱\n👉是用心才能留住人\n\n想学习的加我，纯分享不收费🤝",
    "新代理第一周战绩出炉🔥\n\nXX元首单开门红💰\n\n她说：本来只想试试，没想到这么快回本\n\n机会面前犹豫的人，永远在观望👀\n\n想改变现状的，私信我👇"
]

PROMOTE_TEMPLATES = [
    "用了XX个月，彻底爱上了这款💕\n\n之前试过XX款都不行，这款直接封神✨\n\n最惊艳的是XX，真的绝绝子👍\n\n[配图：使用前后对比]\n\n想买的姐妹评论区扣'想要'，我私信你🔗",
    "说真的，以前觉得XX是智商税😤\n\n直到我自己用了XX个月，才知道真香🔥\n\nXX效果肉眼可见，皮肤状态好到化妆师都问我用了什么💄\n\n真心推荐给所有姐妹👯‍♀️\n\n冲！冲冲！冲！🔥🔥🔥",
    "XX品牌真的太懂女生了💯\n\n包装高级到舍不得送人🎀\n\n使用感满分，完全不输XX大牌✨\n\n性价比之王，学生党也能轻松入👛\n\n闭眼入系列，绝对不踩雷👍"
]

PERSONAL_IP_TEMPLATES = [
    "35岁，我终于想明白了：\n\n人这辈子最大的风险，是不敢冒险。\n\n📍从月薪3000到年入百万\n📍从朝九晚五到自由职业\n📍从害怕变化到拥抱不确定性\n\n我的改变，都在这三年里发生。\n\n如果你也处在人生迷茫期，评论区说说你的困惑👇",
    "停止无效社交的第365天。\n\n很多人问我：不社交不会错过机会吗？\n\n我的答案是：当你自己不牛的时候，认识谁都没用。\n\n与其混圈子，不如让自己成为圈子。\n\n今天比昨天好，这就是我希望的人生状态。\n\n——与同在路上的人共勉🌟",
    "做IP这3年，踩过的坑价值100万。\n\n💥坑1：什么都想做，结果什么都没做成\n💥坑2：追求完美，永远在准备\n💥坑3：数据焦虑，忘了初心\n\n现在回头看，最庆幸的是：没放弃。\n\n想做好个人品牌的，评论区扣'666'，下期分享具体方法👇"
]

MOTIVATIONAL_TEMPLATES = [
    "早安☀️\n\n新的一天，从对自己说这句话开始：\n\n'我值得更好的生活'💪\n\n别让任何人告诉你，你不行。\n\n今天目标：完成XX，赚到XX钱🚀\n\n有一起打卡的吗？评论区集合👇\n\n#早安打卡 #自我提升 #正能量",
    "从负债XX万到月入XX万💰\n\n我用了2年时间还清债务\n\n中间无数次想放弃\n但最后还是选择了咬牙坚持\n\n这就是普通人的翻身之路：\n没有捷径，只有持续努力💪\n\n看到这里的你，点个赞👍\n我们一起变强🔥",
    "停止抱怨的第30天。\n\n抱怨会偷走你的能量，让你越来越丧。\n\n从今天起，我只做3件事：\n✅修炼硬技能\n✅扩大影响力\n✅创造实际价值\n\n你把时间花在哪里，成绩就在哪里。\n\n与君共勉💪 #成长# #赚钱#"
]

FLASH_SALE_TEMPLATES = [
    "⚠️紧急通知⚠️\n\nXX产品限时XX小时大放价💥\n\n原价XX元，现在只要XX元❗️\n\n名额仅剩XX个，抢完即止⏰\n\n[配图：价格对比]\n\n识别下图二维码立即抢购👇\n\n手慢无！手慢无！手慢无！🚨",
    "🎁品牌方给了我XX个内部价名额\n\n不是直播价，不是店庆价\n是成本价💰\n\nXX元到手XX件，正品保证📦\n\n需要的速度，评论扣'要'👇\n\n不废话，直接抢🔥",
    "清仓大甩卖❗️❗️❗️\n\nXX元/件，XX元/3件\n\n质量保证，售后无忧👍\n\n仅限今天，过时不候⏰\n\n评论扣'买'，我私你下单方式👇\n\n先到先得，抢到就是赚到💰"
]

PUBLISH_TIME_TIPS = {
    "morning": "07:30-08:30（上班族刷手机高峰）",
    "noon": "12:00-13:30（午休时间，浏览量大）",
    "evening": "19:30-21:00（黄金时段，转化最高）",
    "late_night": "22:00-23:00（适合情感/深度内容）"
}

def generate_moments_content(product_scene: str, style: str = "reseller", count: int = 5):
    """生成朋友圈爆款文案"""
    
    style_info = STYLES.get(style, STYLES["reseller"])
    template_pool = {
        "reseller": RESELLER_TEMPLATES,
        "promote": PROMOTE_TEMPLATES,
        "personal_ip": PERSONAL_IP_TEMPLATES,
        "motivational": MOTIVATIONAL_TEMPLATES,
        "flash_sale": FLASH_SALE_TEMPLATES
    }.get(style, RESELLER_TEMPLATES)
    
    results = []
    used_templates = []
    
    for i in range(count):
        # 避免重复使用模板
        available = [t for t in template_pool if t not in used_templates]
        if not available:
            available = template_pool
        template = random.choice(available)
        used_templates.append(template)
        
        # 生成配套emoji和发布时间
        emoji_set = random.sample(style_info["emoji_set"], min(6, len(style_info["emoji_set"])))
        best_time = random.choice(list(PUBLISH_TIME_TIPS.keys()))
        
        results.append({
            "index": i + 1,
            "main_text": template,
            "emoji_combination": " ".join(emoji_set),
            "image_suggestion": f"建议配图：产品实拍图 + 文字包装（增加可信度）",
            "publish_time": PUBLISH_TIME_TIPS[best_time],
            "interaction_guide": random.choice([
                "评论区扣'想要'，私信你优惠链接👇",
                "有需要的评论区举手，我一个个回🤝",
                "觉得有用的点赞，收藏起来慢慢看👍",
                "想了解更多的评论区扣'1'👇",
                "你们遇到过XX问题吗？评论区聊聊💬"
            ])
        })
    
    return {
        "status": "success",
        "product_scene": product_scene,
        "style": style_info,
        "count": count,
        "contents": results,
        "tips": {
            "best_frequency": "每天3-5条为宜，过多会被屏蔽",
            "golden_rule": "1条产品 + 2条生活 + 1条反馈 + 1条价值观",
            "avoid": "避免刷屏、避免硬广、避免负能量"
        }
    }

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    result = generate_moments_content(
        product_scene="减肥代餐产品",
        style="flash_sale",
        count=5
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
