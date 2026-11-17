#!/usr/bin/env python3
"""电商广告合规护栏 - 违规用语规则包 (terms)。

覆盖《中华人民共和国广告法》《反不正当竞争法》《价格法》《消费者权益保护法》
等语境下，电商商品标题、详情页、直播话术、促销文案里的高频违规用语。
纯数据定义，无副作用、无网络、无动态执行。

每条术语字段：
    term        违规用语（子串匹配，大小写不敏感）
    category    违规类别
    severity    风险等级 high / medium / low
    suggestion  整改建议（可选，缺省时使用类别默认建议）

设计原则：
  - 只收录"红线清晰、可编码"的高频违规词，降低误报。
  - 绝对化用语（广告法第九条）风险最高，罚款 20 万元起，单独成类。
  - 普通商品（尤其化妆品/食品/保健品）宣称医疗功效属广告法第十七条明令禁止。
  - 规则可扩展：直接在 TERMS 中追加即可，内核无需改动。
"""

PROFILE = {
    "id": "ecom_ad",
    "name": "电商广告合规护栏规则",
    "version": "1.0.0",
    "basis": "《中华人民共和国广告法》第九条、第十七条、第十三条；《反不正当竞争法》；《价格法》；《消费者权益保护法》",
}

# ============ 类别默认建议 ============
CATEGORY_DEFAULT = {
    "absolute": "广告法第九条禁止使用绝对化用语（如'国家级''最高级''最佳'等），建议删除或替换为客观、可证实的描述。",
    "medical_claim": "广告法第十七条禁止非医疗产品宣称医疗功效，普通商品、化妆品、食品不得涉及疾病治疗功能或医疗用语，建议删除。",
    "false_exaggerate": "涉嫌虚假或夸大宣传，若无法提供可验证依据，建议删除或改写。",
    "false_promo": "促销用语须真实有据；虚构原价、'最低价''亏本'等涉嫌价格欺诈或虚假宣传，建议核实后修改。",
    "comparative": "比较广告须真实且不得贬低竞争对手，建议删除无法证实或贬低性的比较表述。",
    "superstition": "涉嫌迷信或诱导，不符合广告法'文明、健康'导向，建议删除。",
}

CATEGORY_LABEL = {
    "absolute": "绝对化用语",
    "medical_claim": "医疗功效违规宣称",
    "false_exaggerate": "虚假/夸大宣传",
    "false_promo": "虚假促销用语",
    "comparative": "比较/贬低用语",
    "superstition": "迷信/诱导用语",
}

# ============ 违规用语表 ============
# (term, category, severity, suggestion?)
TERMS = [
    # —— 绝对化用语（广告法第九条，罚款 20 万起）——
    ("国家级", "absolute", "high", None),
    ("国家免检", "absolute", "high", None),
    ("最高级", "absolute", "high", None),
    ("最佳", "absolute", "high", None),
    ("最好", "absolute", "high", None),
    ("最大", "absolute", "high", None),
    ("最强", "absolute", "high", None),
    ("最优", "absolute", "high", None),
    ("顶级", "absolute", "high", None),
    ("顶尖", "absolute", "high", None),
    ("极致", "absolute", "high", None),
    ("极品", "absolute", "high", None),
    ("第一", "absolute", "high", None),
    ("唯一", "absolute", "high", None),
    ("独家", "absolute", "high", None),
    ("首发", "absolute", "high", None),
    ("首创", "absolute", "high", None),
    ("首款", "absolute", "high", None),
    ("王牌", "absolute", "high", None),
    ("金牌", "absolute", "high", None),
    ("销量第一", "absolute", "high", None),
    ("排名第一", "absolute", "high", None),
    ("领导品牌", "absolute", "high", None),
    ("领导者", "absolute", "high", None),
    ("领袖", "absolute", "high", None),
    ("缔造者", "absolute", "high", None),
    ("创始者", "absolute", "high", None),
    ("开创者", "absolute", "high", None),
    ("世界领先", "absolute", "high", None),
    ("全国领先", "absolute", "high", None),
    ("行业领先", "absolute", "high", None),
    ("遥遥领先", "absolute", "high", None),
    ("举世无双", "absolute", "high", None),
    ("独一无二", "absolute", "high", None),
    ("绝无仅有", "absolute", "high", None),
    ("空前绝后", "absolute", "high", None),
    ("百分百", "absolute", "high", None),
    ("百分之百", "absolute", "high", None),
    ("100%", "absolute", "high", None),
    ("万能", "absolute", "high", None),
    ("绝对", "absolute", "high", "广告法第九条禁止'绝对化'表述，建议删除或改为有条件、可证实的描述。"),
    ("永久", "absolute", "high", "耐用/有效类宣称'永久'通常无法证实，涉嫌夸大，建议删除或限定具体期限。"),
    ("永久有效", "absolute", "high", None),
    ("终身", "absolute", "high", "承诺'终身'类表述难以履行且易构成虚假宣传，建议删除或明确范围。"),
    ("至尊", "absolute", "high", None),
    ("巅峰", "absolute", "high", None),
    ("之王", "absolute", "high", None),
    ("鼻祖", "absolute", "high", None),
    ("始祖", "absolute", "high", None),

    # —— 医疗功效违规宣称（广告法第十七条，非医疗产品禁宣医疗功效）——
    ("治疗", "medical_claim", "high", None),
    ("医治", "medical_claim", "high", None),
    ("医疗", "medical_claim", "high", None),
    ("药用", "medical_claim", "high", None),
    ("药方", "medical_claim", "high", None),
    ("药品", "medical_claim", "high", None),
    ("消炎", "medical_claim", "high", None),
    ("抗炎", "medical_claim", "high", None),
    ("杀菌", "medical_claim", "high", None),
    ("抗菌", "medical_claim", "high", None),
    ("抗感染", "medical_claim", "high", None),
    ("抗癌", "medical_claim", "high", None),
    ("防癌", "medical_claim", "high", None),
    ("抗肿瘤", "medical_claim", "high", None),
    ("解毒", "medical_claim", "high", None),
    ("排毒", "medical_claim", "high", None),
    ("活血", "medical_claim", "high", None),
    ("化瘀", "medical_claim", "high", None),
    ("降脂", "medical_claim", "high", None),
    ("降压", "medical_claim", "high", None),
    ("降糖", "medical_claim", "high", None),
    ("镇痛", "medical_claim", "high", None),
    ("安眠", "medical_claim", "high", None),
    ("安神", "medical_claim", "high", None),
    ("助眠", "medical_claim", "high", None),
    ("催眠", "medical_claim", "high", None),
    ("丰胸", "medical_claim", "high", None),
    ("丰乳", "medical_claim", "high", None),
    ("减肥", "medical_claim", "high", None),
    ("瘦身", "medical_claim", "high", None),
    ("塑身", "medical_claim", "high", None),
    ("壮阳", "medical_claim", "high", None),
    ("补肾", "medical_claim", "high", None),
    ("提高免疫", "medical_claim", "high", None),
    ("修复受损", "medical_claim", "high", None),
    ("干细胞", "medical_claim", "high", None),
    ("药到病除", "medical_claim", "high", None),
    ("包治", "medical_claim", "high", None),
    ("根治", "medical_claim", "high", None),
    ("治愈", "medical_claim", "high", None),
    ("痊愈", "medical_claim", "high", None),
    ("速效", "medical_claim", "high", None),

    # —— 虚假 / 夸大宣传（medium）——
    ("纯天然", "false_exaggerate", "medium", None),
    ("100%有效", "false_exaggerate", "medium", None),
    ("百分百有效", "false_exaggerate", "medium", None),
    ("立竿见影", "false_exaggerate", "medium", None),
    ("立即见效", "false_exaggerate", "medium", None),
    ("瞬间", "false_exaggerate", "medium", "若宣称'瞬间'见效通常无法证实，建议删除或限定真实场景。"),
    ("神奇", "false_exaggerate", "medium", None),
    ("特效", "false_exaggerate", "medium", None),
    ("神效", "false_exaggerate", "medium", None),
    ("奇效", "false_exaggerate", "medium", None),
    ("无效退款", "false_exaggerate", "medium", "承诺'无效退款'须有真实可执行机制，否则涉嫌虚假，建议补充依据或删除。"),
    ("三天见效", "false_exaggerate", "medium", None),
    ("永久不反弹", "false_exaggerate", "medium", None),
    ("一用就好", "false_exaggerate", "medium", None),
    ("彻底清除", "false_exaggerate", "medium", None),
    ("零风险", "false_exaggerate", "medium", "投资/效果类'零风险'表述通常无法保证，建议删除。"),
    (" guaranteed", "false_exaggerate", "medium", "外文'保证'类绝对承诺需有依据，建议删除或本地化改写。"),

    # —— 虚假促销用语（价格法 / 反不正当竞争法，medium）——
    ("全网最低", "false_promo", "medium", None),
    ("全网最低价", "false_promo", "medium", None),
    ("最低价", "false_promo", "medium", None),
    ("史上最低", "false_promo", "medium", None),
    ("史上最优惠", "false_promo", "medium", None),
    ("亏本甩卖", "false_promo", "medium", None),
    ("亏本", "false_promo", "medium", "宣称'亏本'须真实，虚构亏损促销涉嫌虚假宣传，建议核实。"),
    ("跳楼价", "false_promo", "medium", None),
    ("血本", "false_promo", "medium", None),
    ("清仓甩卖", "false_promo", "medium", None),
    ("免单", "false_promo", "medium", "抽奖式'免单'须遵守有奖销售最高奖金额限制（不超过五万元），建议合规设计。"),
    ("最后一天", "false_promo", "medium", "限时限量须真实，反复使用'最后一天'涉嫌虚假，建议据实标注。"),
    ("限时特惠", "false_promo", "medium", "限时促销须有明确且真实的起止时间，建议补充具体时段。"),

    # —— 比较 / 贬低用语（广告法第十三条，medium）——
    ("优于", "comparative", "medium", None),
    ("胜过", "comparative", "medium", None),
    ("压倒", "comparative", "medium", None),
    ("打败", "comparative", "medium", None),
    ("颠覆", "comparative", "medium", None),
    ("取代", "comparative", "medium", None),
    ("代替", "comparative", "medium", None),
    ("完胜", "comparative", "medium", None),

    # —— 迷信 / 诱导用语（low）——
    ("招财", "superstition", "low", None),
    ("发财", "superstition", "low", None),
    ("风水", "superstition", "low", None),
    ("转运", "superstition", "low", None),
    ("辟邪", "superstition", "low", None),
    ("化解", "superstition", "low", None),
    ("改运", "superstition", "low", None),
    ("助运", "superstition", "low", None),
    ("开光", "superstition", "low", None),
    ("旺", "superstition", "low", "单字'旺'在招财语境下易踩迷信/诱导红线，建议结合上下文删除或替换。"),
]
