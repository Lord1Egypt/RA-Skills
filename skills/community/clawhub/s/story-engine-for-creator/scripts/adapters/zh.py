# -*- coding: utf-8 -*-
"""中文语言适配器（ChineseAdapter / lang=zh）。

由 `extract_adapter.py` 从 Story Engine **AST 精确提取**生成；常量值与引擎原定义逐字一致，
已通过值等价校验。引擎经 `_LZ.<NAME>` 引用本文件。

协议：见 adapters/spec.md（六方法 + 常量包）。新增语言 = 新建 adapters/<lang>.py。
边界：本文件不含语义层（认知越界 / 谶语应验 / 伏笔回收需外部知识）。
"""
import re

# ============================================================================
# 语言相关常量（引擎原样外置；跨类同名者已分名）
# ============================================================================

# [NarrativeStripper.] 原行 267-269
_PUNCT_RE = re.compile(
        r"[，。！？；：、,.!?;:()（）【】\[\]《》〈〉“”‘’\"'…—\s]+"
    )

# [NarrativeStripper.] 原行 272-343
_ACTION_WORDS = (
        "留在原地",
        "追上去",
        "拉黑",
        "离开",
        "生气",
        "难过",
        "说道",
        "笑道",
        "哭道",
        "怒道",
        "喝道",
        "骂道",
        "叹道",
        "看见",
        "听到",
        "听见",
        "追赶",
        "走进",
        "走出",
        "走来",
        "走去",
        "起身",
        "落座",
        "拱手",
        "作揖",
        "下拜",
        "拜见",
        "拍案",
        "回头",
        "转身",
        "开口",
        "沉默",
        "点头",
        "摇头",
        "打",
        "跑",
        "走",
        "看",
        "说",
        "哭",
        "笑",
        "喊",
        "叫",
        "坐",
        "立",
        "站",
        "跪",
        "拜",
        "喝",
        "骂",
        "叹",
        "提",
        "拿",
        "取",
        "放",
        "掷",
        "砍",
        "杀",
        "斗",
        "战",
        "退",
        "进",
        "追",
        "寻",
        "送",
        "迎",
        "辞",
        "别",
        "归",
        "回",
    )

# [NarrativeStripper.] 原行 344-346
_ACTION_RE = re.compile(
        r"([\u4e00-\u9fa5]{1,4})(" + "|".join(map(re.escape, _ACTION_WORDS)) + r")"
    )

# [AutomaticRepairEngine.→_JUMP_WORDS_ARE] 原行 504-525
_JUMP_WORDS_ARE = (
        "突然之间",
        "突然间",
        "突然地",
        "突然",
        "莫名地",
        "莫名的",
        "莫名其妙地",
        "莫名其妙",
        "莫名",
        "毫无理由地",
        "毫无理由",
        "不知怎么地",
        "不知怎么",
        "鬼使神差地",
        "鬼使神差",
        "无缘无故地",
        "无缘无故",
        "毫无征兆地",
        "毫无征兆",
        "说变就变",
    )

# [AutomaticRepairEngine.] 原行 526-526
_JUMP_PATTERN = re.compile("|".join(re.escape(w) for w in _JUMP_WORDS_ARE))

# [AutomaticRepairEngine.] 原行 527-527
_TRANSITION = "伴随着情绪的沉淀，顺理成章地"

# [AutomaticRepairEngine.] 原行 529-529
_DUP_TRANSITION = re.compile(re.escape(_TRANSITION) + r"{2,}")

# [模块级] 原行 640-657
_NAME_PRONOUN_HEADS = (
    "他",
    "她",
    "它",
    "我",
    "你",
    "咱",
    "吾",
    "汝",
    "其",
    "这",
    "那",
    "我们",
    "你们",
    "他们",
    "她们",
    "它们",
)

# [模块级] 原行 659-674
_NAME_PRONOUN_HEADS = _NAME_PRONOUN_HEADS + (
    "某",
    "彼",
    "此",
    "俺",
    "妾",
    "奴",
    "臣",
    "朕",
    "孤",
    "寡人",
    "尔等",
    "汝等",
    "我等",
    "你等",
)

# [模块级] 原行 675-737
_NAME_VERB_HEADS = (
    "说",
    "道",
    "问",
    "答",
    "喊",
    "叫",
    "想",
    "看",
    "听",
    "走",
    "跑",
    "来",
    "去",
    "是",
    "有",
    "在",
    "坚持",
    "认为",
    "觉得",
    "决定",
    "意识",
    "同意",
    "评估",
    "梳理",
    "分析",
    "理解",
    "发现",
    "感到",
    "知道",
    "离开",
    "来到",
    "回到",
    "前往",
    "看见",
    "听到",
    "想起",
    "望着",
    "看着",
    "听见",
    "点头",
    "摇头",
    "沉默",
    "开口",
    "转身",
    "回头",
    "抬头",
    "低头",
    "坐下",
    "起身",
    "推开",
    "关上",
    "拿起",
    "放下",
    "掏出",
    "停下",
    "愣住",
    "怔住",
    "惊醒",
    "醒来",
    "出门",
    "进屋",
)

# [模块级] 原行 739-784
_NAME_VERB_HEADS = _NAME_VERB_HEADS + (
    "且",
    "请",
    "若",
    "既",
    "但",
    "莫",
    "休",
    "须",
    "待",
    "不",
    "无",
    "有",
    "日",
    "月",
    "天",
    "地",
    "风",
    "雨",
    "雪",
    "云",
    "却",
    "遂",
    "乃",
    "便",
    "即",
    "又",
    "也",
    "都",
    "只",
    "就",
    "正",
    "先",
    "忙",
    "急",
    "再",
    "亦",
    "皆",
    "俱",
    "莫",
    "休",
    "须",
    "待",
    "不",
    "无",
)

# [模块级] 原行 785-833
_NAME_TAIL_NOISE = (
    "在",
    "去",
    "来",
    "说",
    "道",
    "了",
    "着",
    "过",
    "和",
    "与",
    "跟",
    "吧",
    "呢",
    "吗",
    "啊",
    "呀",
    "么",
    "哈",
    "哦",
    "走",
    "问",
    "答",
    "喊",
    "叫",
    "想",
    "看",
    "听",
    "见",
    "一起",
    "前往",
    "来到",
    "回到",
    "离开",
    "看着",
    "梳理",
    "理",
    "梳",
    "意识",
    "同意",
    "评估",
    "决定",
    "认为",
    "觉得",
    "意识到",
    "发现",
    "感到",
    "知道",
)

# [模块级] 原行 835-880
_NAME_TAIL_NOISE = _NAME_TAIL_NOISE + (
    "便",
    "即",
    "遂",
    "乃",
    "却",
    "又",
    "也",
    "都",
    "只",
    "方",
    "才",
    "就",
    "正",
    "先",
    "忙",
    "急",
    "再",
    "亦",
    "皆",
    "俱",
    "喝",
    "骂",
    "笑",
    "哭",
    "怒",
    "喜",
    "叹",
    "惊",
    "惧",
    "骇",
    "慌",
    "拜",
    "揖",
    "跪",
    "禀",
    "报",
    "应",
    "回",
    "唤",
    "劝",
    "谏",
    "扶",
    "扯",
    "拱",
)

# [模块级] 原行 1261-1271
_FORESHADOW_SET_HINTS = (
    "埋下伏笔",
    "埋下",
    "埋伏笔",
    "留下一句",
    "留下线索",
    "暗暗留下",
    "留下伏笔",
    "铺下伏笔",
    "埋线",
)

# [模块级] 原行 1272-1282
_FORESHADOW_PAY_HINTS = (
    "回收伏笔",
    "呼应",
    "揭开",
    "真相大白",
    "兑现",
    "解释前文",
    "收回伏笔",
    "揭开谜底",
    "原来如此",
)

# [模块级] 原行 1284-1286
_FORESHADOW_TOPIC_SPLIT = re.compile(
    r"[：:，,。；;！!？?\s]|(?:关于|指向|关于的|就是|在于)"
)

# [SecondPerspectiveCausalEngine.] 原行 2631-2642
_COLOCATION_HINTS = [
        "车站",
        "站台",
        "电车",
        "街道",
        "房间",
        "同处",
        "见面",
        "相遇",
        "战场",
        "广场",
    ]

# [SecondPerspectiveCausalEngine.] 原行 2643-2643
_MOTION_HINTS = ["追", "跑", "走", "离开", "去", "赶到", "赶来", "冲", "奔"]

# [SecondPerspectiveCausalEngine.] 原行 2644-2644
_COMMS_HINTS = ["发消息", "打电话", "拉黑", "联系", "回复", "微信", "短信", "传讯"]

# [SecondPerspectiveCausalEngine.] 原行 2645-2645
_JUMP_HINTS = ["突然", "莫名", "毫无理由", "不知怎么", "鬼使神差", "突然之间"]

# [模块级] 原行 2866-2869
_NARRATION_CHRONICLER_KW = [
    "悬疑", "推理", "侦探", "探案", "刑侦", "罪案", "命案", "凶案", "调查", "审讯", "证词",
    "档案", "卷宗", "正史", "传记", "纪事", "实录", "编年", "口述", "笔录",
]

# [模块级] 原行 2870-2870
_NARRATION_LIMITED_KW = ["回忆录", "自传", "成长", "蜕变", "囚徒", "流放", "第一人称", "日记", "书信体"]

# [模块级] 原行 2871-2874
_NARRATION_OMNISCIENT_KW = [
    "史诗", "神话", "演义", "传奇", "传说", "评书", "说书", "话本", "唱本",
    "民间故事", "寓言", "童话", "志怪", "神魔",
]

# [模块级] 原行 2877-2881
_OMNISCIENT_PATTERNS = [
    "殊不知", "原来", "事实上", "实际上", "其实他", "其实她", "要知道", "说白了",
    "说到底", "换句话说", "众所周知", "值得注意的是",
    "其深层原因", "背后真正的原因是", "不为人知的是", "读者应当知道",
]

# [模块级] 原行 2882-2891
_EXPLAIN_MOTIVE_PATTERNS = [
    re.compile(r"他之所以[^，。；]*?是因为"),
    re.compile(r"她之所以[^，。；]*?是因为"),
    re.compile(r"他内心真正[^，。；]*?是"),
    re.compile(r"她内心真正[^，。；]*?是"),
    re.compile(r"[^，。；]{0,6}做这一切，?是因为"),
    re.compile(r"[^，。；]{0,6}做这一切，?源于"),
    re.compile(r"他这么做\s*是\s*因为"),
    re.compile(r"她这么做\s*是\s*因为"),
]

# [模块级] 原行 2893-2893
_ALLOWED_PSYCH = ["心想", "感到", "觉得", "意识到", "明白", "恍然", "暗自"]

# [模块级] 原行 2897-2901
_ERA_FORBIDDEN_DEFAULT = [
    "系统", "手机", "电话", "网络", "数据", "系统提示", "心理素质", "效率低", "标准化",
    "资源整合", "竞争力", "供应链", "互联网", "智能设备", "APP", "公众号",
    "刷屏", "流量", "直播间", "外卖", "共享单车", "充电宝",
]

# [模块级] 原行 2904-2908
_DIALOGUE_RES = [
    re.compile(r"“([^”]{1,120})”"),
    re.compile(r"「([^」]{1,120})」"),
    re.compile(r'"([^"]{1,120})"'),
]

# [ProseStyleAuditor.→_CLASSICAL_CHARS_PSA] 原行 3176-3176
_CLASSICAL_CHARS_PSA = "之乎者也矣焉哉夫其而于所与及以若者乃遂辄弗尝兮"

# [ProseStyleAuditor.] 原行 3177-3180
_EASTERN_WORDS = [
        "遂", "乃", "吾", "汝", "妾", "卿", "陛下", "公子", "娘子", "阁下",
        "府上", "在下", "贫道", "贫僧", "施主", "道友", "仙尊", "圣上",
    ]

# [ProseStyleAuditor.] 原行 3181-3183
_MODERN_NETSLANG = [  # 纯网语/口语化过度词：在正常叙事（古今）均属文风漂移
        "绝了", "yyds", "破防", "栓Q", "家人们", "属实", "简直了", "我裂开", "好吧",
    ]

# [ProseStyleAuditor.] 原行 3184-3184
_MODERN_OBJECTS = ["手机", "微信", "电脑", "老板", "公司", "OK", "WiFi", "视频"]

# [ProseStyleAuditor.] 原行 3185-3188
_PERCEPTION_VB = [
        "想", "心想", "暗自", "觉得", "感到", "意识到", "看见", "听到",
        "猜测", "以为", "知道", "希望", "害怕", "明白",
    ]

# [ProseStyleAuditor.] 原行 3189-3192
_ABSTRACT_TELL = [
        "感到", "觉得", "似乎", "仿佛", "好像", "意识到", "认为", "知道",
        "显得", "看起来", "让人", "令人",
    ]

# [ProseStyleAuditor.] 原行 3198-3198
_REDUNDANT_PAIRS_MODERN = ("的的", "了了", "着呢", "是在", "的了", "着的")

# [ProseStyleAuditor.] 原行 3199-3199
_VIRTUAL_CHARS = "的了着在是于把被给"

# [ProseStyleAuditor.] 原行 3201-3225
_THRESHOLDS = {
        "eastern_ancient": {"virtual_density": 0.30, "fourchar_density": 0.06,
                            "rhythm_cv": 0.30, "tell_density": 0.32, "repeat_window": 6},
        "western_plain":   {"virtual_density": 0.22, "fourchar_density": 0.02,
                            "rhythm_cv": 0.40, "tell_density": 0.35, "repeat_window": 5},
        "unknown":         {"virtual_density": 0.25, "fourchar_density": 0.04,
                            "rhythm_cv": 0.35, "tell_density": 0.33, "repeat_window": 5},
        # —— 扩展审查族（A：支持更多文风校验）——
        "wuxia":           {"virtual_density": 0.32, "fourchar_density": 0.08,
                            "rhythm_cv": 0.30, "tell_density": 0.30, "repeat_window": 6},
        "xianxia":         {"virtual_density": 0.33, "fourchar_density": 0.09,
                            "rhythm_cv": 0.28, "tell_density": 0.28, "repeat_window": 6},
        "classical_poetry": {"virtual_density": 0.38, "fourchar_density": 0.14,
                            "rhythm_cv": 0.25, "tell_density": 0.22, "repeat_window": 5},
        "scifi":           {"virtual_density": 0.22, "fourchar_density": 0.02,
                            "rhythm_cv": 0.42, "tell_density": 0.35, "repeat_window": 5},
        "webnovel":        {"virtual_density": 0.24, "fourchar_density": 0.03,
                            "rhythm_cv": 0.38, "tell_density": 0.40, "repeat_window": 5},
        "hardboiled":      {"virtual_density": 0.18, "fourchar_density": 0.01,
                            "rhythm_cv": 0.45, "tell_density": 0.30, "repeat_window": 4},
        "epic_fantasy":    {"virtual_density": 0.30, "fourchar_density": 0.07,
                            "rhythm_cv": 0.30, "tell_density": 0.30, "repeat_window": 6},
        "urban":           {"virtual_density": 0.20, "fourchar_density": 0.02,
                            "rhythm_cv": 0.42, "tell_density": 0.38, "repeat_window": 5},
    }

# [ProseStyleAuditor.] 原行 3285-3285
_QUOTE_SPAN_RE = re.compile(r"[\u300c\u201c][^\u300d\u201d]{0,300}[\u300d\u201d]")

# [ProseStyleAuditor.] 原行 3351-3351
_REPEAT_MIN_FRAG = 4

# [ProseStyleAuditor.] 原行 3352-3352
_REPEAT_CHUNK_SENTS = 120

# [ProseStyleAuditor.] 原行 3355-3355
_SPEECH_TAIL_CHARS = "道說曰問答云謂言罵嘆喝哭"

# [ProseStyleAuditor.] 原行 3356-3360
_SPEECH_TAIL_PHRASES = (
        "聽了", "看了", "聽見", "聽說", "心想", "說道", "笑道", "哭道",
        "問道", "答道", "罵道", "嘆道", "喝道", "怒道", "便道", "乃道",
        "遂道", "忙道", "急道", "低聲", "高聲", "出來", "進去",
    )

# [模块级] 原行 3468-3541
STYLE_PRESETS = {
    "wuxia": {
        "label_zh": "武侠", "label_en": "Wuxia", "family": "wuxia",
        "encourage": ["剑", "掌", "内力", "抱拳", "纵身", "纵马", "江湖", "门派", "掌门", "侠", "招式", "轻功"],
        "forbidden": ["手机", "微信", "电脑", "OK", "WiFi", "视频", "绝了", "yyds", "破防"],
        "sentence": "多用四字格与利落短句，动作描写干净；允许半文半白。",
        "rhetoric": "重白描与动作，少心理独白；对话干脆有江湖气。",
        "pov": "第三人称限知 / 史官旁观",
        "sample": "他抱拳一礼，纵身跃上墙头，剑光在月下划出一道冷弧。",
    },
    "xianxia": {
        "label_zh": "仙侠", "label_en": "Xianxia", "family": "xianxia",
        "encourage": ["仙", "灵", "气", "渡劫", "飞升", "宗门", "道友", "法宝", "灵根", "洞府"],
        "forbidden": ["手机", "微信", "电脑", "OK", "WiFi", "视频", "绝了", "yyds"],
        "sentence": "半文半白，长句铺陈天地灵气；可用对仗与虚字。",
        "rhetoric": "重意境与气象描写，修辞偏瑰丽；对话清冷有仙风。",
        "pov": "第三人称全知 / 史官旁观",
        "sample": "灵气自洞府涌出，他闭目引气入体，恍若听见万物呼吸。",
    },
    "classical_poetry": {
        "label_zh": "古风诗词", "label_en": "Classical poetry", "family": "classical_poetry",
        "encourage": ["之", "乎", "者", "也", "兮", "风", "月", "江", "愁", "梦", "孤", "落"],
        "forbidden": ["手机", "微信", "电脑", "OK", "WiFi", "视频", "绝了", "yyds", "破防"],
        "sentence": "句式长短错落，重对仗与韵律；四字格与文言虚字密集。",
        "rhetoric": "重意象与比兴，忌直白叙述；语域统一古雅。",
        "pov": "抒情第一人称 / 第三人称限知",
        "sample": "江风起兮波浩渺，孤舟独往梦迢遥。",
    },
    "scifi": {
        "label_zh": "科幻", "label_en": "Sci-Fi", "family": "scifi",
        "encourage": ["星", "舰", "量子", "文明", "轨道", "数据", "算法", "曲率", "维度", "信号"],
        "forbidden": ["绝了", "yyds", "破防", "栓Q", "家人们"],
        "sentence": "以白描与术语构建冷峻未来感；句长中等，逻辑清晰。",
        "rhetoric": "重概念与机理，少用滥情比喻；对话精炼。",
        "pov": "第三人称限知 / 史官旁观",
        "sample": "曲率引擎点燃的瞬间，舰体在星图上拉出一道蓝色的痕。",
    },
    "webnovel": {
        "label_zh": "网文", "label_en": "Web novel", "family": "webnovel",
        "encourage": ["他", "她", "眼神", "心中", "气氛", "瞬间", "却在", "然而"],
        "forbidden": ["绝了", "yyds", "破防", "栓Q", "家人们", "我裂开"],
        "sentence": "快节奏，短中句交替；多用转折词维持爽感。",
        "rhetoric": "重情绪钩子与节奏，可接受适度 tell；对话口语化。",
        "pov": "第三人称限知",
        "sample": "他却在下一瞬笑了，眼中寒意比刀更利。",
    },
    "hardboiled": {
        "label_zh": "冷硬派", "label_en": "Hardboiled", "family": "hardboiled",
        "encourage": ["烟", "街", "雨", "枪", "酒", "影子", "沉默", "血"],
        "forbidden": ["绝了", "yyds", "破防", "栓Q", "家人们"],
        "sentence": "极短句、硬冷白描；几乎不用形容词与比喻。",
        "rhetoric": "重动作与环境，极少心理；对话 terse。",
        "pov": "第一人称限知",
        "sample": "雨还在下。我点燃最后一支烟，等电话响。",
    },
    "epic_fantasy": {
        "label_zh": "史诗奇幻", "label_en": "Epic fantasy", "family": "epic_fantasy",
        "encourage": ["王", "剑", "誓", "远征", "古老", "预言", "城邦", "龙", "命运"],
        "forbidden": ["手机", "微信", "电脑", "OK", "WiFi", "视频", "绝了", "yyds"],
        "sentence": "庄重长句铺陈，重场面与史诗感；可半文半白。",
        "rhetoric": "重象征与宿命，修辞恢弘；对话有古韵。",
        "pov": "第三人称全知 / 史官旁观",
        "sample": "古老预言在风中复苏，王举起碎裂的剑，誓言仍未冷却。",
    },
    "urban": {
        "label_zh": "都市", "label_en": "Urban", "family": "urban",
        "encourage": ["公司", "地铁", "咖啡", "手机", "会议", "夜晚", "街角"],
        "forbidden": ["绝了", "yyds", "破防", "栓Q", "家人们"],
        "sentence": "现代白话，中等句长；允许现代物象。",
        "rhetoric": "重生活质感与对话，自然口语；忌文言堆砌。",
        "pov": "第一人称 / 第三人称限知",
        "sample": "地铁进站的风卷起她的衣角，手机在掌心震了一下。",
    },
}

# [StyleRecognizer.→_CLASSICAL_CHARS_SR] 原行 3951-3951
_CLASSICAL_CHARS_SR = "之乎者也矣焉哉夫其而于所与及以若者乃遂辄弗尝"

# [IncrementalAuditor.→_JUMP_WORDS_IA] 原行 4178-4183
_JUMP_WORDS_IA = (
        "突然之间", "突然间", "突然地", "突然", "莫名地", "莫名的", "莫名其妙地",
        "莫名其妙", "莫名", "毫无理由地", "毫无理由", "不知怎么地", "不知怎么",
        "鬼使神差地", "鬼使神差", "无缘无故地", "无缘无故", "毫无征兆地",
        "毫无征兆", "说变就变",
    )


# ============================================================================
# 六方法协议实现（见 adapters/spec.md）
# 说明：本轮为「协议就绪」，引擎尚未经此六方法调用（保持零行为变化）；
#       新增语言时以本文件为模板实现同名六方法即可。
# ============================================================================
def split_sentences(text):
    """切句：返回句子列表（去除空串）。"""
    return [s.strip() for s in re.split(r"[。！？!?；;]", text or "") if s.strip()]


def tokenize(text):
    """分词/动作抽提：返回 [(施动片段, 动作词), ...]。"""
    return _ACTION_RE.findall(text or "")


def extract_names(sentence, known=None):
    """人名识别：优先已知名表精确匹配，否则按中文姓名启发式返回至多一个候选。"""
    if not sentence:
        return []
    if known:
        return [x for x in known if x and x in sentence]
    cand = []
    for m in re.finditer(r"[\u4e00-\u9fa5]{2,3}", sentence):
        c = m.group(0)
        if c[0] in _NAME_PRONOUN_HEADS or c[0] in _NAME_VERB_HEADS:
            continue
        if c[-1] in _NAME_TAIL_NOISE:
            continue
        cand.append(c)
    return cand[:1]


def era_forbidden(extra=None):
    """时代禁用词表：默认表 + 调用方追加。"""
    out = list(_ERA_FORBIDDEN_DEFAULT)
    if extra:
        out.extend(extra)
    return out


def style_features(text):
    """文风特征：句数、汉字数、均句长、古典字计数（供风格族判定与阈值校准）。"""
    sents = split_sentences(text)
    han = length_unit(text)
    return {
        "sentences": len(sents),
        "han_chars": han,
        "avg_sentence_len": round(han / max(1, len(sents)), 2),
        "classical_chars": sum(1 for c in (text or "") if c in _CLASSICAL_CHARS),
    }


def length_unit(text):
    """长度度量：中文按汉字计。"""
    return sum(1 for c in (text or "") if "\u4e00" <= c <= "\u9fa5")

