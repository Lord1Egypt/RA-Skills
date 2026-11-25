#!/usr/bin/env python3
"""Conservative text-plan checks; no inference from unprovided frames or identity."""
import json
import re
import sys
from pathlib import Path

KINDS = ('character', 'prop', 'lighting', 'space')
CN = dict(zip(KINDS, ('角色', '道具', '光线', '空间')))
COLORS = ('深蓝', '浅蓝', '蓝', '红', '黄', '白', '黑', '灰', '绿', '紫', '橙', '棕', '金', '银')
GARMENTS = ('外套', '大衣', '夹克', '衬衫', '裙', '裤', '围巾', '帽', '鞋')
# A name next to one of these predicates is an explicit on-screen participant,
# even when the sentence does not describe clothing.  Keep this list about
# identity-bearing actions/states rather than treating every Chinese noun as a
# person name.
# Do not use the generic verbs “在” or “出现” as person predicates.  They
# describe lights and scene objects just as often as people (for example
# “暖光在画面左侧” or “太阳出现在海平面”).  Location-plus-action is handled
# separately below for prose such as “林岚在卧室静坐”.
IDENTITY_PREDICATES = r'(?:身穿|穿着|穿|換上|换上|脱下|戴|拿|坐|站|走|看|跑|抱|提|举|推|拉|进入|未戴|不戴|停在|躺在|靠在|站在|坐在|正(?:在)?|正在|留在|望向|凝视|面对|回头|低头|抬头|微笑|笑|说话|说|皱眉|哭|点头|挥手|眨眼|睁眼|闭眼|沉思)'
LOCATION_ACTION_PREDICATES = r'在[^，。；;]{0,12}(?:静坐|坐着|站着|停留|等待|观察|看着|回头|低头|抬头|走动)'
NON_PERSON_NAMES = {'他', '她', '它', '他们', '她们', '人物', '角色', '路人', '男人', '女人', '老人', '孩子', '镜头', '房门', '房间', '汽车', '车辆', '车门', '摄像机', '相机', '杯子', '杯', '画面', '灯光', '道具', '纸袋', '手机', '盒子', '箱子', '门窗', '窗户', '书本', '右手', '左手', '双手', '门口', '左侧', '右侧', '窗帘', '暖光', '冷光', '太阳', '台灯', '海平面', '画面', '床头', '太阳出现', '花瓶'}
NON_PERSON_SCENE_LEADS = ('白墙', '灰墙', '红墙', '砖墙', '墙面', '朱门', '木门', '铁门', '林木', '林间', '林中', '白云', '山间', '海面', '水面', '高楼', '窗外', '窗边', '屋顶', '天花板', '地面', '桌面', '雾气', '晨雾', '灯火', '街灯', '沙发上', '桌边', '桌旁', '床边', '床上', '椅子上', '地毯上')
# When an unfamiliar action follows a conventional Chinese personal name, the
# name is still explicit identity evidence.  This avoids making required
# character references depend on a closed list of verbs (for example, 沉思).
SURNAMES = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗丁宣邓郁单杭洪包诸左石崔吉龚程邢滑裴陆荣翁荀羊於惠甄曲封储仲伊宁仇甘武符刘景詹龙叶幸司黎薄印白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴郜胥能苍双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍郤璩桑桂濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎慕连茹习宦艾鱼容向古易慎戈廖庾终居衡步都耿满弘匡国文寇广禄阙东欧殳沃利蔚越夔隆师巩聂晁勾敖融冷訾辛阚那简饶空曾毋沙乜养鞠须丰关蒯相查后荆红游竺权逯盖益桓公'
LOCATIONS = ('书店', '咖啡店', '书房', '教室', '房间', '卧室', '客厅', '厨房', '街道', '车内', '办公室', '公园', '海滩', '码头', '车站', '学校', '医院', '商场', '餐厅', '酒店', '山顶', '森林', '广场', '仓库', '天台', '地下室', '阁楼', '阳台', '走廊', '电梯', '停车场', '楼梯间')
# These are venue-noun endings, rather than a list of named places.  Keeping
# the full phrase is important: “古堡大厅” and “废弃工厂大厅” are separately
# stated locations even though neither venue is in LOCATIONS.
PLACE_NOUN_SUFFIX = r'(?:大厅|花园|庭院|露台|广场|剧院|展厅|影棚|摄影棚|片场|村|镇|岛|街|巷|路|桥|湖|河|楼|院|站|港|湾|谷|洞|塔|寺|馆)'
MARKERS = {
    'character': ('换上', '脱下', '穿上', '更衣', '换装', '更换外套', '换成', '摘下', '取下'),
    'prop': ('放下', '递给', '交给', '拿起', '收起', '丢下', '装进', '取出', '换手'),
    'lighting': ('开灯', '关灯', '日落', '日出', '入夜', '灯光转', '光线转', '切到夜', '切到白天', '重新布光'),
    'space': ('走到', '走向', '进入', '走进', '走入', '离开', '移动到', '来到', '转身', '切换场景', '换景'),
}

def scene_like_phrase(value, start, candidate):
    """Whether a short candidate is part of a scene/object phrase, not a name.

    The name matcher intentionally accepts ordinary two-character Chinese names.
    That must not promote compact shot-list descriptions such as ``白墙反光``
    or ``高楼灯火通明`` into characters merely because their first character can
    also be a surname.
    """
    if any(value.startswith(lead, start) for lead in NON_PERSON_SCENE_LEADS):
        return True
    # This narrow fallback catches a new compound scene noun without treating
    # a person's later activity (for example “林岚坐在卧室”) as scene evidence.
    return bool(re.search(r'(?:墙|门|窗|楼|林|间|雾|灯|火|天|地|桌|床)$', candidate))

def text(value):
    return value.strip() if isinstance(value, str) else ''

def state(shot, kind):
    # Explicit fields and generic picture text both contain evidence.
    return '，'.join(filter(None, (text(shot.get(kind)), text(shot.get('description')), text(shot.get('visual')))))

def named_reference(value):
    match = re.match(r'\s*([^：:，,。；;]+)\s*[：:]', text(value))
    return match.group(1).strip() if match else ''

def character_references(references):
    value = references.get('character')
    if isinstance(value, dict):
        return {str(name): text(description) for name, description in value.items() if text(description)}
    value = text(value)
    if not value:
        return {}
    parts = [p.strip() for p in re.split(r'[；;\n]', value) if p.strip()]
    mapping = {named_reference(p): p for p in parts if named_reference(p)}
    return mapping if mapping else {'': value}

def named_actors(value):
    """Return explicit person-like names in prose; never infer pronouns."""
    if re.search(r'(?:无人出镜|没有人出镜|空镜|静物镜头)', value):
        return []
    names = [match.group(1) for match in re.finditer(
        r'(?<![\u4e00-\u9fff])([\u4e00-\u9fff]{2,4})(?<![不未])(?=' + IDENTITY_PREDICATES + r')', value)
        if match.group(1) not in NON_PERSON_NAMES and not scene_like_phrase(value, match.start(1), match.group(1))]
    names.extend(match.group(1) for match in re.finditer(
        r'(?<![\u4e00-\u9fff])([\u4e00-\u9fff]{2,4}?)(?=' + LOCATION_ACTION_PREDICATES + r')', value)
        if match.group(1) not in NON_PERSON_NAMES)
    names.extend(match.group(1) for match in re.finditer(
        r'(?:^|[，,。；;\s])(?:镜头中|画面中|镜头里|画面里)?([' + SURNAMES + r'][\u4e00-\u9fff])(?=' + IDENTITY_PREDICATES + r')', value)
        if match.group(1) not in NON_PERSON_NAMES)
    # A coordinated subject such as “林岚、陈默穿……” has only one predicate.
    # Keep both explicitly named people, including the name before the connector.
    coordinated = re.compile(
        r'([\u4e00-\u9fff]{2,4}(?:[、和及与][\u4e00-\u9fff]{2,4})+)'
        r'(?=(?:同时|一起|均|都)?' + IDENTITY_PREDICATES + r')')
    for match in coordinated.finditer(value):
        names.extend(name for name in re.split(r'[、和及与]', match.group(1)) if name not in NON_PERSON_NAMES)
    # Explicitly named people remain identifiable in group-presence wording,
    # even when the sentence gives no action verb (e.g. “林岚和陈默同框” or
    # “林岚与陈默出现在书店”). Restrict this matcher to surname-led names so
    # scene nouns and objects are not promoted to characters.
    group_presence = re.compile(
        r'([' + SURNAMES + r'][\u4e00-\u9fff]{1,2}(?:[、和及与][' + SURNAMES + r'][\u4e00-\u9fff]{1,2})+)'
        r'(?=同框|同场|入镜|一同出现|一起出现|出现在)')
    for match in group_presence.finditer(value):
        names.extend(name for name in re.split(r'[、和及与]', match.group(1)) if name not in NON_PERSON_NAMES)
    # Do not require an action dictionary for a sentence headed by a
    # conventional name.  The short predicate is deliberately bounded by a
    # clause boundary so locations such as “卧室床边，清晨” are not parsed as
    # people.  Existing explicit predicates remain the preferred evidence.
    first_clause = re.split(r'[，,。；;]', value, maxsplit=1)[0].strip()
    # A bare scene phrase can begin with a surname character (“古堡大厅”,
    # “林间小路”); do not turn that location into a person name.
    # Besides an exact scene mention, reject a scene-led clause with a
    # descriptive suffix (for example “古堡大厅内景”).  Such phrases can
    # start with a surname character, but have no person identity evidence.
    scene_lead = explicit_scene_mention(first_clause) or bool(re.match(
        r'^[\u4e00-\u9fff]{1,10}(?:大厅|花园|庭院|露台|广场|剧院|展厅|影棚|摄影棚|片场|村|镇|岛|街|巷|路|桥|湖|河|楼|院|站|港|湾|谷|洞|塔|寺|馆)(?:内景|外景|全景|远景|近景)?$',
        first_clause))
    if not scene_lead:
        for match in re.finditer(
            r'^([' + SURNAMES + r'][\u4e00-\u9fff])(?:正在|正|已)?[\u4e00-\u9fff]{1,6}(?=[，。；;]|$)', value):
            if match.group(1) not in NON_PERSON_NAMES and not scene_like_phrase(value, match.start(1), match.group(1)):
                names.append(match.group(1))
    # The simple predicate matcher may include a coordinating adverb in its
    # maximum four-character name span (for example “陈默同时穿”).
    names = [name[:-2] if name.endswith(('同时', '一起')) else name for name in names]
    names = [name[:-2] if name.endswith(('即将', '正在', '准备', '打算', '将要')) else name for name in names]
    # A greedy prose match must never make a negation particle part of a
    # person's name (for example ``林岚未戴围巾`` or ``林岚不戴眼镜``).
    # Keep this normalization after all matchers so it also protects future
    # predicate additions.
    names = [name[:-1] if name.endswith(('未', '不')) else name for name in names]
    names = [re.sub(r'(?:右手|左手|双手)$', '', name) for name in names]
    names = [name for name in names if len(name) >= 2]
    # A short surname-led match must not truncate an adjacent three-character
    # name captured by the specific surname matcher (e.g. 张晓明 -> 张晓).
    names = [name for name in names if not any(
        other != name and len(other) > len(name) and other.startswith(name)
        for other in names)]
    # The bounded name regex can otherwise absorb a colored object immediately
    # before an action (e.g. “黄色纸袋拿在手中” -> “黄色纸袋”).
    non_person_fragments = (*NON_PERSON_NAMES, '色', '衣服', '纸袋', '背包', '手机壳')
    names = [name for name in names if not any(fragment in name for fragment in non_person_fragments)]
    names = [name for name in names if not scene_like_phrase(value, value.find(name), name)]
    return list(dict.fromkeys(names))

def named_actor(value):
    actors = named_actors(value)
    return actors[0] if len(actors) == 1 else ''

def subjects(shot, references):
    explicit = text(shot.get('character_id'))
    # A holder label in the prop field ("林岚：右手持…") is also explicit
    # identity evidence.  Without it, a shot whose character column merely
    # says "两人同框" loses the safe per-holder alignment below and can fall
    # back to comparing one person's prop with another person's prop.
    value = '，'.join(filter(None, (state(shot, 'character'), state(shot, 'prop'))))
    refs = character_references(references)
    present = [name for name in refs if name and name in value]
    candidates = named_actors(value)
    return list(dict.fromkeys(([explicit] if explicit else []) + present + candidates))

def subject(shot, references):
    people = subjects(shot, references)
    return people[0] if len(people) == 1 else ''

def has_anonymous_person(shot):
    value = '，'.join(text(shot.get(key)) for key in ('character', 'description', 'visual'))
    return bool(re.search(r'(?<!其)(?:他|她|他们|她们|一位|一个人|男人|女人|男孩|女孩|人物|角色)', value))

def positive_action(value, markers):
    """Return whether a marker describes an action that actually occurred.

    A transition is evidence only when it asserts the action happened.  In
    particular, refusal, intent, an attempt, and an unsuccessful outcome must
    not waive a continuity finding (``拒绝放下纸袋`` and ``试图走进…但失败``).
    """
    for marker in markers:
        for match in re.finditer(re.escape(marker), value):
            # Restrict both sides to the same clause.  This preserves an
            # actual later action in a new clause while rejecting negated or
            # merely intended actions in the marker's own clause.
            clause_start = max(value.rfind(separator, 0, match.start()) for separator in '，。；;') + 1
            clause_end_candidates = [pos for separator in '，。；;' if (pos := value.find(separator, match.end())) != -1]
            clause_end = min(clause_end_candidates) if clause_end_candidates else len(value)
            before = value[clause_start:match.start()]
            after = value[match.end():clause_end]
            negated = re.search(
                r'(?:没有|并未|尚未|不曾|无需|未|没|不|无|拒绝|避免|不愿|阻止)'
                r'(?:把|将|对|进行|任何|明确|交代)?[^，。；;]{0,16}$', before)
            intended = re.search(r'(?:准备|打算|计划|即将|将要|想要|快要|拟于|拟定|试图|尝试|试着).{0,12}$', before)
            failed = re.search(r'(?:但|却|最终|仍)?(?:未能|没有成功|未成功|失败|没能|没成功)', after)
            if not negated and not intended and not failed:
                return True
    return False

def has_explanation(shot, kind, aspect=''):
    transition = shot.get('transition')
    if isinstance(transition, dict):
        relevant = text(transition.get(kind))
    else:
        relevant = text(transition)
    # Require the action to name the changed object/property. A generic action cannot waive a category.
    value = relevant + '，' + state(shot, kind)
    verbs = MARKERS[kind]
    clauses = [piece for piece in re.split(r'[，。；;]', value) if piece]
    if kind == 'character':
        for clause in clauses:
            if not aspect or not positive_action(clause, verbs):
                continue
            if (re.search(r'(?:换上|穿上|更换|换装|更衣|摘下|取下|脱下)[^，。；;]{0,12}' + re.escape(aspect), clause)
                    or re.search(re.escape(aspect) + r'[^，。；;]{0,8}换成|换成[^，。；;]{0,8}' + re.escape(aspect), clause)):
                return True
        return False
    if kind == 'prop':
        return any(positive_action(clause, (verb,)) and re.search(r'(?:纸袋|手机|杯|书|包|伞|钥匙|花|盒子|箱子|门|抽屉|瓶子)', clause) for clause in clauses for verb in (*verbs, '打开', '关闭', '合上', '盖上', '关上'))
    if kind == 'lighting':
        return any(positive_action(clause, (verb,)) and re.search(r'(?:灯|光|日落|日出|入夜|白天|夜)', clause) for clause in clauses for verb in verbs)
    return any(positive_action(clause, (verb,)) and re.search(r'(?:到|向|入|离开|场景|换景|转身)', clause) for clause in clauses for verb in verbs)

def explains_space_change(shot, before, after):
    transition = shot.get('transition')
    change_text = (text(transition.get('space')) if isinstance(transition, dict) else text(transition)) + '，' + state(shot, 'space')
    if not change_text:
        return False
    new_places = locations(after)
    old_places = locations(before)
    # A turn can explain facing, but it cannot explain a move to another place.
    movement_markers = ('走到', '走向', '进入', '走进', '走入', '离开', '移动到', '来到', '切换场景', '换景')
    clauses = re.split(r'[，。；;]', change_text)
    if not any(positive_action(clause, movement_markers) for clause in clauses):
        return False
    return bool(new_places) and all(place in change_text for place in new_places)

def explains_prop_state_change(shot, item, actor='', references=None):
    transition = shot.get('transition')
    transition_text = text(transition.get('prop')) if isinstance(transition, dict) else text(transition)
    value = '，'.join(filter(None, (transition_text, text(shot.get('prop')), text(shot.get('description')), text(shot.get('visual')))))
    if actor and references:
        value = actor_scoped_text(value, shot, actor, references)
    action_order = re.compile(r'(?:打开|关上|合上|盖上|掀开).{0,8}' + re.escape(item))
    natural_order = re.compile(re.escape(item) + r'.{0,8}(?:打开|关上|合上|盖上|掀开)')
    passive_order = re.compile(re.escape(item) + r'.{0,8}(?:被|已)(?:打开|关上|合上|盖上|掀开)')
    return any(item in clause and positive_action(clause, ('打开', '关上', '合上', '盖上', '掀开'))
               and (action_order.search(clause) or natural_order.search(clause) or passive_order.search(clause))
               for clause in re.split(r'[，。；;]', value))

def explains_prop_position_change(shot, item, actor='', references=None):
    transition = shot.get('transition')
    transition_text = text(transition.get('prop')) if isinstance(transition, dict) else text(transition)
    value = '，'.join(filter(None, (transition_text, text(shot.get('prop')), text(shot.get('description')), text(shot.get('visual')))))
    if actor and references:
        value = actor_scoped_text(value, shot, actor, references)
    position_markers = ('放下', '拿起', '收起', '丢下', '装进', '取出', '递给', '交给', '换手', '移动到', '放到', '放在')
    return any(item in clause and positive_action(clause, position_markers)
               and any(marker in clause for marker in position_markers)
               for clause in re.split(r'[，。；;]', value))

def prop_states(value):
    found = {}
    for item in ('盒子', '箱子', '门', '抽屉', '瓶子', '包', '书'):
        if re.search(re.escape(item) + r'[^，。；;]{0,8}(?:打开|敞开|开着)', value): found[item] = '打开'
        if re.search(re.escape(item) + r'[^，。；;]{0,8}(?:关闭|关上|合上|闭着)', value): found[item] = '关闭'
    return found

def colors_before(value, item):
    """Return explicit colours immediately attached to one item.

    Match the colour vocabulary as one longest-first alternative.  Searching
    for every colour separately makes ``深蓝色手机`` also match the shorter
    ``蓝色手机`` token, which can make a real prop change look ambiguous.
    """
    color_pattern = '|'.join(map(re.escape, COLORS))
    return list(dict.fromkeys(re.findall(
        r'(' + color_pattern + r')(?:色)?' + re.escape(item), text(value)
    )))

def colors_for(value, garment):
    removed = (r'(?:没有\s*(?:深蓝|浅蓝|红|黄|白|黑|灰|蓝|绿|紫|橙|棕|金|银)?色?|'
               r'未戴|不戴|脱下|取下|摘下)\s*' + re.escape(garment))
    if re.search(removed, text(value)):
        return []
    return colors_before(value, garment)

def color_family(value):
    return re.sub(r'^(?:深|浅)', '', text(value))

def same_color(left, right):
    if left == right:
        return True
    if color_family(left) != color_family(right):
        return False
    # A broad color description is compatible with either explicit shade;
    # two distinct explicit shades are a material continuity change.
    return left == color_family(left) or right == color_family(right)

def appearance_tokens(value):
    return [(colors[0], garment) for garment in GARMENTS if len(colors := colors_for(value, garment)) == 1]

def personal_features(value):
    value = text(value)
    features, hair = {}, []
    if re.search(r'中长发', value): hair.append('中长发')
    elif re.search(r'长发|长头发', value): hair.append('长发')
    if re.search(r'短发|短头发', value): hair.append('短发')
    if len(set(hair)) == 1: features['头发'] = hair[0]
    if re.search(r'(?:未戴|不戴|没有戴)(?:黑框|细框|粗框|圆框)?眼镜', value):
        features['眼镜'] = '未佩戴'
    else:
        colored_glasses = re.findall(r'(?:戴|佩戴)?(深蓝|浅蓝|蓝|红|黄|白|黑|灰|绿|紫|橙|棕|金|银)(?:色)?眼镜', value)
        glasses = re.findall(r'戴((?:黑框|细框|粗框|圆框)?眼镜)', value)
        if len(set(colored_glasses)) == 1 and colored_glasses:
            features['眼镜'] = colored_glasses[0] + '色眼镜'
        elif len(set(glasses)) == 1 and glasses: features['眼镜'] = glasses[0]
    return features

def visual_appearance_tokens(value):
    return appearance_tokens(value) + [(state_value, feature) for feature, state_value in personal_features(value).items()]

def explained_new_color(value, garment):
    value = text(value)
    match = re.search(r'(?:换成|换为)(深蓝|浅蓝|蓝|红|黄|白|黑|灰|绿|紫|橙|棕|金|银)(?:色)?', value)
    return match.group(1) if match and re.search(re.escape(garment), value) else ''

def light_direction(value):
    directions = []
    # Isolate light direction, not a person's facing direction in the same description.
    patterns = (r'(?:暖光|冷光|阳光|灯光|来光|光线|光)[^，。；;]{0,8}?(?:从|来自|由|在)(左|右)(?:侧|边|方)?',
                r'(左|右)(?:侧|边|方)[^，。；;]{0,3}?(?:来光|照入|照射|灯光)')
    for pattern in patterns:
        directions.extend(re.findall(pattern, value))
    unique = set(directions)
    return next(iter(unique)) if len(unique) == 1 else ''

def explicit_light_directions(value):
    """Return every explicit light direction, preserving conflicts for QA."""
    directions = []
    patterns = (r'(?:暖光|冷光|阳光|灯光|来光|光线|光)[^，。；;]{0,8}?(?:从|来自|由|在)(左|右)(?:侧|边|方)?',
                r'(左|右)(?:侧|边|方)[^，。；;]{0,3}?(?:来光|照入|照射|灯光)')
    for pattern in patterns:
        directions.extend(re.findall(pattern, text(value)))
    return list(dict.fromkeys(directions))

def light_description(value):
    """Whether the text describes a scene light, even without a direction."""
    return bool(re.search(r'(?:暖光|冷光|阳光|日光|灯光|来光|光线|光照|色温|逆光|侧光|顶光|背光)', text(value)))

def prop_appearances(value):
    found = {}
    value = text(value)
    items = ('纸袋', '手机', '杯子', '杯', '书', '包', '伞', '钥匙', '花', '盒子', '箱子', '瓶子')
    for item in items:
        colors = colors_before(value, item)
        if len(colors) == 1:
            found[item] = colors[0]
    if found.get('杯子') == found.get('杯'):
        found.pop('杯', None)
    return found

def explains_prop_appearance_change(shot, item, actor='', references=None):
    transition = shot.get('transition')
    value = (text(transition.get('prop')) if isinstance(transition, dict) else text(transition)) + '，' + state(shot, 'prop')
    if actor and references:
        value = actor_scoped_text(value, shot, actor, references)
    return any(positive_action(clause, ('更换', '换成', '换为', '拿起', '取出', '递给')) and item in clause
               for clause in re.split(r'[，。；;]', value))

def explains_hand_change(shot, item, actor='', references=None):
    """A hand-side change needs an explicit, item-specific handoff action."""
    transition = shot.get('transition')
    transition_text = text(transition.get('prop')) if isinstance(transition, dict) else text(transition)
    value = '，'.join(filter(None, (transition_text, state(shot, 'prop'))))
    if actor and references:
        value = actor_scoped_text(value, shot, actor, references)
    return any(item in clause and positive_action(clause, ('换手',))
               for clause in re.split(r'[，。；;]', value))

def light_temperature(value):
    value = text(value)
    warm = bool(re.search(r'暖光|暖色光|偏暖|暖色温', value))
    cool = bool(re.search(r'冷光|冷色光|偏冷|冷色温', value))
    return '暖' if warm and not cool else '冷' if cool and not warm else ''

def light_intensity(value):
    value = text(value)
    bright = bool(re.search(r'明亮|明快|强光|光线充足|亮堂', value))
    dim = bool(re.search(r'昏暗|暗淡|微弱光|光线很暗|偏暗', value))
    return '明亮' if bright and not dim else '昏暗' if dim and not bright else ''

def prop_positions(value):
    positions = {}
    for item in ('纸袋', '手机', '杯子', '书', '包', '伞', '钥匙', '花'):
        if re.search(r'(?:桌上|桌面上|放在桌面|摆在桌面)[^，。；;]{0,8}' + item + r'|' + item + r'[^，。；;]{0,8}(?:在桌上|放在桌面)', value):
            positions[item] = '桌面'
        elif re.search(r'(?:拿|持|握|提|捧|拎|抱)[^，。；;]{0,8}' + item, value):
            positions[item] = '手持'
    return positions

def explains_light_change(shot):
    transition = shot.get('transition')
    value = (text(transition.get('lighting')) if isinstance(transition, dict) else text(transition)) + '，' + state(shot, 'lighting')
    states_an_actual_change = bool(re.search(r'(?:暖|冷|色温|从左|从右|左侧|右侧)', value)) or bool(
        re.search(r'(?:开灯|关灯)', value) and light_intensity(value))
    return positive_action(value, MARKERS['lighting']) and states_an_actual_change

def locations(value):
    # Keep the most specific place phrase, so “书店门口” is not also read as
    # a separate “书店” location. Explicit unknown places can still compare.
    value = text(value)
    # Holding/hand placement (for example “杯子拿在左手”) is prop identity
    # evidence, not a location that calls for references.scene.
    value = re.sub(r'(?:拿|持|握|拎|提|抓)?(?:在|于)?(?:左手|右手|双手|手中)', '', value)
    value = re.sub(r'(?:左手|右手|双手|手中)(?:拿|持|握|拎|提|抓)?', '', value)
    # Keep known locations separate from prose captures.  A known place is
    # stronger evidence than a greedy prose tail: in “在卧室发呆”, “卧室” is
    # the location and “发呆” is activity, even though it is not in a fixed
    # list of action verbs.
    known = {location for location in LOCATIONS if location in value}
    found = set(known)
    # References are often terse ("书店门口") and have no preceding 在/到.
    # Promote a listed base place plus its qualifier to the same specific form
    # used for prose such as "林岚在书店门口".
    found.update(
        match.group(0)
        for location in LOCATIONS
        for match in re.finditer(re.escape(location) + r'(?:边|旁|内|外|门口|入口|岸|上|下|床边|床头)', value)
    )
    # Keep the qualifier inside the captured name.  The former expression
    # captured only "书店" from "书店门口", which both lost specificity and
    # made one textual place look like two different places downstream.
    found.update(re.findall(r'(?:在|到|向|进入|离开|来到|位于)((?:[^，。；;\s]{1,8}(?:边|旁|内|外|门口|入口|岸|上|下)))', value))
    prose_places = set(re.findall(r'(?:在|到|进入|离开|来到|位于|走到|走向|移动到)([^，。；;\s]{1,12}?)(?=面向|朝|拍摄|停留|固定|静置|静坐|坐着|站着|等待|看书|阅读|休息|工作|观察|交谈|说话|出现|保持|走|移动|$)', value))
    qualifiers = r'(?:边|旁|内|外|门口|入口|岸|上|下|床边|床头)$'
    # Do not let an unrecognised action fused to a known location manufacture
    # a new place.  Explicit place qualifiers remain useful and are already
    # collected above (e.g. “书店门口”).
    prose_places = {
        place for place in prose_places
        if not any(location in place and place != location and not re.search(qualifiers, place)
                   for location in known)
    }
    found.update(prose_places)
    # Retain a clearly named short place even when it is not in LOCATIONS;
    # the suffix identifies a venue noun while the complete phrase preserves
    # the distinguishing prefix (e.g. “古堡大厅” vs “废弃工厂大厅”).
    found.update(re.findall(
        r'(?:^|[，。；;\s])([^，。；;\s]{1,14}' + PLACE_NOUN_SUFFIX + r')(?:内景|外景|全景|远景|近景)?(?=[，。；;\s]|$)', value))
    canonical = {'卧室内':'卧室', '办公室内':'办公室', '客厅内':'客厅', '厨房内':'厨房', '房间内':'房间'}
    normalized = {canonical.get(place, place) for place in found}
    non_location_anchors = {'桌上', '桌面', '地上', '地面', '台面', '手中', '画面中', '镜头中'}
    return {place for place in normalized if place not in non_location_anchors
            and not re.fullmatch(r'(?:左|右|双)?手(?:中|上|边)', place)
            and not re.match(r'(?:画面|镜头|构图)(?:左|右|中|前|后|上|下)', place)
            and not any(place != other and place in other for other in normalized)}

def location_identity(place):
    """Normalize a within-place qualifier while preserving the named venue."""
    place = text(place)
    # Prose may qualify a venue ("安静的书店门口") without changing its
    # identity.  Retain the venue and its entrance qualifier, while dropping
    # only the descriptive lead-in; this is not evidence of a location move.
    for location in sorted(LOCATIONS, key=len, reverse=True):
        match = re.search(re.escape(location) + r'(?:边|旁|内|外|门口|入口|岸|上|下|床边|床头)?$', place)
        if match and match.start() and place[:match.start()].endswith('的'):
            return match.group(0)
    # Positions such as “卧室窗边” and “卧室床边” describe a point inside the
    # same room; venue entrances such as “书店门口” keep the venue identity.
    for location in sorted(LOCATIONS, key=len, reverse=True):
        if place.startswith(location) and place[len(location):] in ('窗边', '床边', '床头', '桌边', '门内', '门外', '角落', '中央', '里面', '内部'):
            return location
        if place.endswith(location) and place[:-len(location)] in ('室内的', '房间里的', '房间内的'):
            return location
    return place

def same_location(old, new):
    old_ids = {location_identity(place) for place in old}
    new_ids = {location_identity(place) for place in new}
    if old_ids == new_ids:
        return True
    # A scene reference may explicitly establish several allowed spaces in
    # one location set (for example, a sequence covering bedroom and balcony).
    # Any single shot inside that set belongs to the same baseline.
    if new_ids and new_ids.issubset(old_ids):
        return True
    room_places = {'卧室', '客厅', '厨房', '房间', '室内', '办公室'}
    if len(old_ids) == len(new_ids) == 1:
        left, right = next(iter(old_ids)), next(iter(new_ids))
        if left == '房间' and right in room_places or right == '房间' and left in room_places:
            return True
    return False

def explicit_scene_mention(value):
    """Recognize a clearly written place even when it is outside LOCATIONS."""
    value = text(value)
    if locations(value):
        return True
    # Terse shot lists often start with a place noun (“古堡大厅，清晨”) rather
    # than “在古堡大厅”.  These endings name a location, unlike a bare object
    # or frame-position phrase.
    return bool(re.search(
        r'(?:^|[，。；;])[^，。；;\s]{1,10}(?:大厅|花园|庭院|露台|广场|剧院|展厅|影棚|摄影棚|片场|村|镇|岛|街|巷|路|桥|湖|河|楼|院|站|港|湾|谷|洞|塔|寺|馆)(?=[，。；;\s]|$)', value))

def spatial_tokens(value):
    text_value = text(value)
    facing = re.findall(r'面向(左|右|前|后|北|南|东|西)', text_value)
    movement = re.findall(r'(?<!面)(?:朝|向)(左|右|前|后|北|南|东|西)(?:走|移动|前进|离开|看)?', text_value)
    return ('|'.join(dict.fromkeys(facing)) if len(set(facing)) == 1 else '',
            '|'.join(dict.fromkeys(movement)) if len(set(movement)) == 1 else '')

def missing_material(data):
    if not isinstance(data, dict):
        return ['input（JSON对象）']
    shots = data.get('shots')
    references = data.get('references', {})
    missing = []
    if not isinstance(shots, list) or not shots:
        return ['shots（非空镜头表）']
    if len(shots) > 100:
        missing.append('镜头表超过100行，请按章节或场景分批')
    if not isinstance(references, dict):
        missing.append('references（JSON对象）')
        references = {}
    known_names = [name for name in character_references(references) if name]
    ids = []
    for index, shot in enumerate(shots, 1):
        prefix = f'shots[{index}]'
        if not isinstance(shot, dict):
            missing.append(f'{prefix}（镜头对象）')
            continue
        raw_identifier = shot.get('id')
        identifier = text(raw_identifier) if isinstance(raw_identifier, str) else (str(raw_identifier) if isinstance(raw_identifier, (int, float)) and not isinstance(raw_identifier, bool) else '')
        if not identifier:
            missing.append(f'{prefix}.id（镜头编号）')
        elif identifier in ids:
            missing.append(f'{prefix}.id（重复镜头编号{identifier}，请提供唯一编号）')
        else:
            ids.append(identifier)
        if not any(text(shot.get(key)) for key in (*KINDS, 'description', 'visual')):
            missing.append(f'{prefix}（画面信息：character/prop/lighting/space/description/visual）')
        description = '，'.join(text(shot.get(key)) for key in ('character','description','visual','space','prop') if text(shot.get(key)))
        prose_actors = named_actors(description)
        prose_actor = prose_actors[0] if len(prose_actors) == 1 else ''
        # An explicit empty-frame statement is stronger than broad words such
        # as “人物” or “角色” elsewhere in the same shot.  It therefore must
        # not trigger a character-reference request for a scene-only image.
        explicit_empty_frame = bool(re.search(
            r'(?:无人出镜|没有人出镜|(?:人物|角色)(?:均)?(?:未|没有|不)出镜|'
            r'没有(?:人物|角色)出镜|无人物|无角色|空镜|静物镜头)', description))
        involves_character = not explicit_empty_frame and bool(text(shot.get('character')) or text(shot.get('character_id')) or appearance_tokens(description) or any(name in description for name in known_names) or prose_actor or re.search(r'(?:人物|角色|老人|老年人|男人|女人|男孩|女孩|孩子|青年|女子|男子|路人|(?<!其)他|她|一位|一个人)', description))
        actor = subject(shot, references)
        char_refs = character_references(references)
        described_known_names = [name for name in char_refs if name and name in description]
        # Report every explicitly named person whose own reference is absent.
        # In particular, a valid reference for 林岚 must not make “林岚和陈默
        # 同框” look complete: 陈默 still needs a separately usable reference.
        # Keeping the name in the missing item gives the editor an actionable
        # request instead of an ambiguous, generic references.character error.
        unresolved_named_actors = [name for name in prose_actors if name not in char_refs]
        if unresolved_named_actors:
            for name in unresolved_named_actors:
                missing.append(f'references.character（{name}，{prefix}涉及人物）')
        elif involves_character and (not char_refs or (actor and actor not in char_refs) or (not actor and not described_known_names and '' not in char_refs)):
            missing.append(f'references.character（{prefix}涉及人物）')
        scene_text = '，'.join(text(shot.get(key)) for key in ('space','lighting','description','visual') if text(shot.get(key)))
        involves_scene = bool(text(shot.get('space')) or text(shot.get('lighting')) or explicit_scene_mention(scene_text) or light_direction(scene_text) or light_description(scene_text) or re.search(r'(?:海滩|海边|码头|门口|室内|室外|背景|街边|山上|岸边|床边|床头|场景)', scene_text))
        if involves_scene and not text(references.get('scene')):
            missing.append(f'references.scene（{prefix}涉及场景）')
        prop_text = state(shot, 'prop')
        actors = subjects(shot, references)
        if len(actors) > 1:
            # A coloured prop, a hand-side phrase, or a holding verb makes
            # identity material: it cannot safely belong to every person in
            # a shared frame.  This also covers natural orders such as
            # “手机在右手”, which do not use “拿/持”.
            prop_items = r'(?:纸袋|手机|杯子|杯|书|包|伞|钥匙|花|盒子|箱子|瓶子)'
            identity_sensitive = re.compile(
                r'(?:左手|右手|双手|手中|拿|持|握|提|捧|抱|拎)' 
                r'|(?:深|浅)?(?:红|黄|白|黑|灰|蓝|绿|紫|橙|棕|金|银)色?' + prop_items)
            phone_colors = set(re.findall(r'(?:深|浅)?(?:红|黄|白|黑|灰|蓝|绿|紫|橙|棕|金|银)色?手机', prop_text))
            needs_hand_attribution = len(phone_colors) > 1 or bool(re.search(r'左手', prop_text) and re.search(r'右手', prop_text))
            for clause in re.split(r'[，,。；;\n]', prop_text):
                if identity_sensitive.search(clause) and re.search(prop_items, clause) and sum(name in clause for name in actors) != 1:
                    detail = ('请标注各道具持有人及左右手，或人工确认归属'
                              if needs_hand_attribution else
                              '请标注道具持有人，每件道具须有唯一持有人，或人工确认归属')
                    missing.append(f'{prefix}.prop（多人同框时{detail}）')
                    break
            # “红色手机、蓝色手机；左手、右手” puts hand sides in a
            # separate clause. It is still an incomplete ownership record.
            if needs_hand_attribution and any(re.search(prop_items, clause) and sum(name in clause for name in actors) != 1
                                              for clause in re.split(r'[，,。；;\n]', prop_text)):
                missing.append(f'{prefix}.prop（多人同框时请标注各道具持有人及左右手，或人工确认归属）')
    return list(dict.fromkeys(missing))

def inferred_severity(kind, aspect):
    """Rank evidence by how much the mismatch can change a viewer's story reading."""
    # Keep this classification at the reporting boundary so every issue path
    # (reference checks, adjacent-shot checks, and carried baselines) uses the
    # same visible severity rule.  Do not make callers remember a default.
    if kind == 'character':
        return 'high'
    if kind == 'space':
        # A location jump changes where the action is happening.  Facing,
        # movement, and an in-scene anchor are still visible discontinuities,
        # but normally do not change the story location.
        return 'high' if aspect == '地点' else 'medium'
    if kind == 'prop':
        # A prop appearing, disappearing, changing colour, or changing state
        # can alter what a character has done.  Its exact placement/hand is a
        # lower-impact screen-direction continuity issue.
        return 'medium' if re.search(r'(?:位置|手侧)', aspect) else 'high'
    if kind == 'lighting':
        # Exposure/brightness alone is a polish issue; light direction and
        # colour temperature can break a cut's perceived setup.
        return 'low' if re.search(r'(?:明暗|亮度)', aspect) else 'medium'
    return 'medium'

def issue(kind, ids, aspect, evidence, suggestion, severity=None):
    severity = severity or inferred_severity(kind, aspect)
    return {'category': CN[kind], 'severity': severity, 'shots': ids, 'aspect': aspect,
            'evidence': evidence, 'minimal_change': suggestion}

def actor_state(shot, actor, references):
    value = state(shot, 'character')
    refs = character_references(references)
    if (len(refs) == 1 or text(shot.get('character')) == actor
            or (text(shot.get('character_id')) == actor and actor not in value)):
        return value
    start = value.find(actor)
    if start < 0:
        return ''
    end = len(value)
    for boundary in re.finditer(r'[，。；;]', value[start:]):
        end = min(end, start + boundary.start())
    for other in character_references(references):
        if other and other != actor:
            other_start = value.find(other, start + len(actor))
            if other_start >= 0:
                # “林岚、陈默穿黑色外套” is one coordinated predicate: the
                # apparel after the second name applies to both people.
                connector = value[start + len(actor):other_start]
                if not re.fullmatch(r'[、和及与]', connector):
                    end = min(end, other_start)
    return value[start:end]

def actor_scoped_prop(shot, actor, references):
    """Return prop clauses explicitly attached to this person in a multi-person shot."""
    return actor_scoped_text(state(shot, 'prop'), shot, actor, references)

def actor_scoped_text(value, shot, actor, references):
    """Keep only prose that is explicitly attributable to ``actor``.

    In a multi-person shot an unqualified action is deliberately not borrowed
    from another person's clause.  That keeps, for example, “陈默放下纸袋”
    from explaining 林岚's missing paper bag.
    """
    refs = [name for name in character_references(references) if name]
    if len(subjects(shot, references)) <= 1:
        return value
    clauses = re.split(r'[，,。；;\n]', value)
    # Attribution is per clause, never stateful.  In particular, do not let
    # “林岚拿手机；右手拿纸袋” silently assign the second clause to 林岚.
    return '，'.join(
        clause for clause in clauses
        if actor in clause and not any(name != actor and name in clause for name in refs)
    )

def actor_has_explanation(shot, actor, references, aspect=''):
    transition = shot.get('transition')
    transition_value = text(transition.get('character')) if isinstance(transition, dict) else text(transition)
    scoped = {
        'character': actor_state(shot, actor, references),
        'transition': {'character': actor_scoped_text(transition_value, shot, actor, references)},
    }
    return has_explanation(scoped, 'character', aspect)

def prop_change_issues(before, after, current, ids, actor='', references=None):
    before_states, after_states = prop_states(before), prop_states(after)
    before_looks, after_looks = prop_appearances(before), prop_appearances(after)
    found = []
    for item in sorted(set(before_looks) & set(after_looks)):
        if before_looks[item] != after_looks[item] and not explains_prop_appearance_change(current, item, actor, references):
            label = f'{actor}的{item}' if actor else item
            found.append(issue('prop', ids, f'{label}外观颜色', f'{label}：{before_looks[item]}色 → {after_looks[item]}色', '核对同一人物持有的道具；确有更换则补真实过渡，否则保持颜色一致。'))
    for item in sorted(set(before_states) & set(after_states)):
        if before_states[item] != after_states[item] and not explains_prop_state_change(current, item, actor, references):
            label = f'{actor}的{item}' if actor else item
            found.append(issue('prop', ids, f'{label}开合状态', f'{label}{before_states[item]} → {label}{after_states[item]}', f'核对{label}状态；如有真实开合动作，在过渡中说明。'))
    return found

def prop_hand_issues(previous, current, references, actors, ids):
    items = ('纸袋', '手机', '杯', '书', '包', '伞', '钥匙', '花', '相机')
    found = []
    transition = current.get('transition')
    transition_text = text(transition.get('prop')) if isinstance(transition, dict) else text(transition)
    all_current = state(current, 'prop') + '，' + transition_text
    for actor in actors:
        before = actor_scoped_prop(previous, actor, references) if actor else state(previous, 'prop')
        after = actor_scoped_prop(current, actor, references) if actor else state(current, 'prop')
        if not before or not after:
            continue
        action_text = all_current
        if actor and len(subjects(current, references)) > 1:
            # Apply a drop/handoff only to the named holder's prose.  A
            # generic action stays ambiguous rather than being assigned to
            # every person in the frame.
            action_text = '，'.join(filter(None, (
                actor_scoped_prop(current, actor, references),
                actor_scoped_text(transition_text, current, actor, references),
            )))
        for item in items:
            not_bookplace = r'(?!店|架)' if item == '书' else ''
            def hand_present(value, hand):
                forward = re.escape(hand) + r'[^，。；;]{0,4}(?:拿|持|握|提|捧|拎|抱)[^，。；;]{0,6}' + re.escape(item) + not_bookplace
                reverse = re.escape(item) + r'[^，。；;]{0,5}(?:在|放在|位于)?' + re.escape(hand)
                return bool(re.search(forward, value) or re.search(reverse, value))
            old_hand = next((hand for hand in ('左手', '右手') if hand_present(before, hand)), '')
            new_hand = next((hand for hand in ('左手', '右手') if hand_present(after, hand)), '')
            if old_hand and new_hand and old_hand != new_hand and not explains_hand_change(current, item, actor, references):
                label = f'{actor}的{item}' if actor and len(actors) > 1 else item
                found.append(issue('prop', ids, f'{label}持有手侧', f'{label}：{old_hand}持有 → {new_hand}持有', '核对同一人物持有道具的手侧；如确有换手，在过渡中写明换手。'))
        held = [item for item in items if re.search(r'(?:拿|持|握|提|捧|抱|拎)[^，。；;]{0,8}' + re.escape(item) + (r'(?!店|架)' if item == '书' else ''), before)
                or re.search(re.escape(item) + r'[^，。；;]{0,5}(?:在|放在|位于)?(?:左手|右手)', before)]
        before_empty_hands = bool(re.search(r'(?:双手|两手|手中)(?:都)?空(?:着|无物)?', before))
        if before_empty_hands:
            for item in items:
                present_after = (re.search(r'(?:拿|持|握|提|捧|抱|拎)[^，。；;]{0,8}' + re.escape(item) + (r'(?!店|架)' if item == '书' else ''), after)
                    or re.search(re.escape(item) + r'[^，。；;]{0,5}(?:在|放在|位于)?(?:左手|右手)', after))
                acquired = any(item in clause and positive_action(clause, ('拿起', '拾起', '捡起', '接过', '收到', '递给', '交给'))
                    for clause in re.split(r'[，。；;]', action_text))
                if present_after and not acquired:
                    label = f'{actor}：' if actor else ''
                    found.append(issue('prop', ids, item, f'{label}{before} → {after}', '核对该人物的道具持有状态；如确有拿起或交接，在过渡中说明。'))
        empty_hands = bool(re.search(r'双手空|手中空', after))
        for item in held:
            absent = empty_hands or bool(re.search(r'(?:没有|未)(?:拿|持|握)?(?:着)?[^，。；;]{0,2}' + re.escape(item), after))
            action = any(positive_action(clause, MARKERS['prop']) and item in clause
                         and re.search(r'(?:放下|递给|交给|收起|丢下|装进|取出|换手)', clause)
                         for clause in re.split(r'[，。；;]', action_text))
            if absent and not action:
                label = f'{actor}：' if actor else ''
                found.append(issue('prop', ids, item, f'{label}{before} → {after}', '核对该人物的道具持有状态；有已确定放下/交接则补真实说明，没有则保持原状态。'))
    return found

def reference_issues(shot, references):
    found, identifier = [], shot['id']
    refs = character_references(references)
    documented_changes = establishes_baseline(shot, references)
    for actor in subjects(shot, references):
        ref = refs.get(actor, '')
        if not ref:
            continue
        person_state = actor_state(shot, actor, references)
        for color, garment in appearance_tokens(ref):
            actual = colors_for(person_state, garment)
            if len(actual) == 1 and not same_color(actual[0], color) and not actor_has_explanation(shot, actor, references, garment):
                found.append(issue('character', [identifier], garment,
                    f'人物参考要求“{color}{garment}”，镜头{identifier}明确写为“{actual[0]}{garment}”。',
                    f'核对{actor}的{garment}；无已确定换装时保留{color}，如确有换装则补真实过渡。'))
            elif not actual and re.search(r'(?:没有|未戴|不戴|脱下|取下|摘下)[^，。；;]{0,6}' + re.escape(garment), person_state) and not actor_has_explanation(shot, actor, references, garment):
                found.append(issue('character', [identifier], garment,
                    f'人物参考要求“{color}{garment}”，镜头{identifier}明确写为服饰缺失。',
                    f'核对{actor}的{garment}；无已确定换装时保留{color}，如确有换装则补真实过渡。'))
        for feature, expected in personal_features(ref).items():
            actual = personal_features(person_state).get(feature)
            if actual and actual != expected and not actor_has_explanation(shot, actor, references, feature):
                found.append(issue('character', [identifier], feature,
                    f'人物参考要求“{expected}{feature}”，镜头{identifier}明确写为“{actual}{feature}”。',
                    f'核对{actor}的{feature}；未明确变化时保持参考状态，真实变化需补过渡。'))
    scene_ref = text(references.get('scene'))
    for kind in ('space', 'lighting'):
        value = state(shot, kind)
        if not value or not scene_ref or (kind == 'lighting' and has_explanation(shot, kind)):
            continue
        if kind == 'space':
            old, new = locations(scene_ref), locations(value)
            if old and new and not same_location(old, new) and not explains_space_change(shot, scene_ref, value):
                reference_places = '、'.join(sorted(old))
                shot_places = '、'.join(sorted(new))
                found.append(issue(kind, [identifier], '地点', f'场景参考为“{reference_places}”，镜头{identifier}为“{shot_places}”。',
                    '核对场景地点；若有已确定换景，补相应过渡，不新增移动剧情。'))
            # Do not turn differing light, framing, or other scene detail into
            # a guessed location conflict.  locations() only returns explicit
            # known venues or explicit venue-noun phrases.
            old_facing, old_move = spatial_tokens(scene_ref)
            new_facing, new_move = spatial_tokens(value)
            if old_facing and new_facing and old_facing != new_facing and not has_explanation(shot, 'space'):
                found.append(issue(kind, [identifier], '面向方向', f'场景参考面向{old_facing}，镜头{identifier}面向{new_facing}。', '核对人物朝向；若有真实转身，补明转身过渡。'))
            if old_move and new_move and old_move != new_move and not has_explanation(shot, 'space'):
                found.append(issue(kind, [identifier], '运动方向', f'场景参考运动方向为{old_move}，镜头{identifier}为{new_move}。', '核对运动方向；若有真实转向，补明方向变化。'))
            old_positions, new_positions = anchor_positions(scene_ref), anchor_positions(value)
            for anchor in set(old_positions) & set(new_positions):
                if old_positions[anchor] != new_positions[anchor] and not has_explanation(shot, 'space'):
                    found.append(issue(kind, [identifier], f'{anchor}位置', f'场景参考在{anchor}{old_positions[anchor]}，镜头{identifier}在{anchor}{new_positions[anchor]}。', '核对场景内相对位置；若有真实移动或换位，补明过渡。'))
        else:
            old, new = light_direction(scene_ref), light_direction(value)
            if old and new and old != new and ('光线', '', '来光方向') not in documented_changes:
                found.append(issue(kind, [identifier], '来光方向', f'场景参考来光为{old}侧，镜头{identifier}明确为{new}侧。', '核对来光方向；若确有布光变化，补真实变化说明。'))
            old_temp, new_temp = light_temperature(scene_ref), light_temperature(value)
            if old_temp and new_temp and old_temp != new_temp and not explains_light_change(shot) and ('光线', '', '光线色温') not in documented_changes:
                found.append(issue(kind, [identifier], '光线色温', f'场景参考为{old_temp}光，镜头{identifier}明确为{new_temp}光。', '核对色温；若确有布光变化，补真实变化说明。'))
            old_level, new_level = light_intensity(scene_ref), light_intensity(value)
            if old_level and new_level and old_level != new_level and not explains_light_change(shot):
                found.append(issue(kind, [identifier], '光线明暗', f'场景参考为{old_level}，镜头{identifier}明确为{new_level}。', '核对光线明暗；若确有布光变化，补真实变化说明。'))
    return found

def establishes_baseline(shot, references):
    """Return explicitly changed reference aspects that later shots may inherit."""
    changes = set()
    for actor in subjects(shot, references):
        person_state = actor_state(shot, actor, references)
        for garment in GARMENTS:
            has_state = bool(colors_for(person_state, garment) or re.search(
                r'(?:没有|未戴|不戴|脱下|取下|摘下)[^，。；;]{0,6}' + re.escape(garment), person_state))
            if has_state and actor_has_explanation(shot, actor, references, garment):
                changes.add(('角色', actor, garment))

    scene_text = state(shot, 'space')
    scene_ref = text(references.get('scene'))
    if scene_text and scene_ref and explains_space_change(shot, scene_ref, scene_text):
        changes.add(('空间', '', '地点'))

    light_text = state(shot, 'lighting')
    transition = shot.get('transition')
    light_transition = text(transition.get('lighting')) if isinstance(transition, dict) else text(transition)
    all_light_text = light_transition + '，' + light_text
    explicit_relight = explains_light_change(shot) or (
        positive_action(all_light_text, ('调整布光', '调整光线', '改变布光', '改变光线', '重新打光'))
        and (light_direction(all_light_text) or light_temperature(all_light_text) or light_intensity(all_light_text)))
    if explicit_relight:
        if light_direction(light_text):
            changes.add(('光线', '', '来光方向'))
        if light_temperature(light_text):
            changes.add(('光线', '', '光线色温'))
    return changes

def anchor_positions(value):
    value = text(value)
    found = {}
    for anchor in ('办公桌', '书桌', '桌子', '床', '沙发', '门', '窗'):
        match = re.search(re.escape(anchor) + r'(?:的)?(左|右)(?:侧|边)', value)
        if match:
            found[anchor] = match.group(1)
    return found

def reference_issue_key(item):
    category, aspect = item['category'], item['aspect']
    if category == '角色':
        match = re.search(r'核对(.+?)的' + re.escape(aspect), item['minimal_change'])
        return (category, match.group(1) if match else '', aspect)
    return (category, '', aspect)

def adjacent_issues(previous, current, references, inherited_changes=frozenset()):
    found = []
    before_actor, after_actor = subject(previous, references), subject(current, references)
    shared_actors = sorted(set(subjects(previous, references)) & set(subjects(current, references)))
    same_actor = bool(shared_actors) or bool(before_actor and before_actor == after_actor)
    for kind in KINDS:
        before, after = state(previous, kind), state(current, kind)
        if not before or not after:
            continue
        ids = [previous['id'], current['id']]
        if kind == 'character' and same_actor:
            actors = shared_actors or [before_actor]
            for actor in actors:
                before_person = actor_state(previous, actor, references) if actor else before
                after_person = actor_state(current, actor, references) if actor else after
                for old, garment in appearance_tokens(before_person):
                    # A transition can name the garment being removed rather
                    # than repeat the final colour beside it ("把深蓝外套换成
                    # 白色").  Once that real change is documented, the next
                    # shot inherits its result instead of being compared with
                    # the pre-change wording in this transition shot.
                    if ('角色', actor, garment) in inherited_changes:
                        continue
                    new = colors_for(after_person, garment)
                    if len(new) == 1 and not same_color(old, new[0]) and not actor_has_explanation(current, actor, references, garment):
                        found.append(issue(kind, ids, garment, f'{actor}：{old}{garment} → {new[0]}{garment}',
                            f'核对{actor}的{garment}；无已确定换装时保持基线，有则补真实换装说明。'))
                    elif not new and re.search(r'(?:没有|未戴|不戴|脱下|取下|摘下)[^，。；;]{0,6}' + re.escape(garment), after_person) and not actor_has_explanation(current, actor, references, garment):
                        found.append(issue(kind, ids, garment, f'{actor}：{old}{garment} → 明确写为服饰缺失',
                            f'核对{actor}的{garment}；无已确定换装时保持基线，有则补真实换装说明。'))
                before_features, after_features = personal_features(before_person), personal_features(after_person)
                for feature in set(before_features) & set(after_features):
                    if before_features[feature] != after_features[feature] and not actor_has_explanation(current, actor, references, feature):
                        found.append(issue(kind, ids, feature, f'{actor}：{before_features[feature]}{feature} → {after_features[feature]}{feature}', f'核对{actor}的{feature}；未明确变化时保持一致，真实变化需补过渡。'))
        elif kind == 'prop':
            anonymous_cross_shot = has_anonymous_person(previous) or has_anonymous_person(current)
            comparable_prop_identity = (not anonymous_cross_shot and not (subjects(previous, references) or subjects(current, references))) or bool(shared_actors)
            reference_names = [name for name in character_references(references) if name]
            has_person_attribution = any(name in value for name in reference_names for value in (before, after))
            if comparable_prop_identity and shared_actors and has_person_attribution:
                for actor in shared_actors:
                    before_person_prop = actor_scoped_prop(previous, actor, references)
                    after_person_prop = actor_scoped_prop(current, actor, references)
                    if before_person_prop and after_person_prop:
                        found.extend(prop_change_issues(before_person_prop, after_person_prop, current, ids, actor, references))
            elif comparable_prop_identity:
                found.extend(prop_change_issues(before, after, current, ids))
            if comparable_prop_identity:
                position_pairs = []
                if shared_actors and has_person_attribution:
                    position_pairs = [(actor_scoped_prop(previous, actor, references), actor_scoped_prop(current, actor, references)) for actor in shared_actors]
                else:
                    position_pairs = [(before, after)]
                for before_position_text, after_position_text in position_pairs:
                    before_positions, after_positions = prop_positions(before_position_text), prop_positions(after_position_text)
                    for item in set(before_positions) & set(after_positions):
                        actor = ''
                        if shared_actors and has_person_attribution:
                            actor = next((name for name in shared_actors if name in before_position_text or name in after_position_text), '')
                        if before_positions[item] != after_positions[item] and not explains_prop_position_change(current, item, actor, references):
                            found.append(issue('prop', ids, f'{item}位置', f'{item}：{before_positions[item]} → {after_positions[item]}', '核对道具位置；若真实放下或拿起，在过渡中写明。'))
        if kind == 'prop' and same_actor:
            found.extend(prop_hand_issues(previous, current, references, shared_actors or [before_actor], ids))
        elif kind == 'prop' and comparable_prop_identity:
            # A prop-only pair has no person name to align, but it also has
            # no competing holder.  Its explicit hand state is therefore a
            # safe continuity fact: "双手空着" followed by "右手拿纸袋"
            # must not let a prop appear without a documented pickup or
            # handoff.  Anonymous people remain excluded above so pronouns
            # are never silently treated as the same person.
            found.extend(prop_hand_issues(previous, current, references, [''], ids))
        elif kind == 'lighting':
            old, new = light_direction(before), light_direction(after)
            if old and new and old != new and not has_explanation(current, kind):
                found.append(issue(kind, ids, '来光方向', f'来光{old}侧 → {new}侧', '核对布光；有真实变化则补说明，否则保持来光方向。'))
            old_temp, new_temp = light_temperature(before), light_temperature(after)
            if old_temp and new_temp and old_temp != new_temp and not explains_light_change(current):
                found.append(issue(kind, ids, '光线色温', f'{old_temp}光 → {new_temp}光', '核对色温；有真实布光变化则补说明，否则保持色温一致。'))
            old_level, new_level = light_intensity(before), light_intensity(after)
            if old_level and new_level and old_level != new_level and not explains_light_change(current):
                found.append(issue(kind, ids, '光线明暗', f'{old_level} → {new_level}', '核对光线明暗；有真实布光变化则补说明，否则保持一致。'))
        elif kind == 'space':
            old, new = locations(before), locations(after)
            if len(old) == len(new) == 1 and not same_location(old, new) and not explains_space_change(current, before, after):
                    found.append(issue(kind, ids, '地点', f'地点{next(iter(old))} → {next(iter(new))}', '核对地点；有真实换景则补说明，不凭空新增移动。'))
            # See the reference check above: only explicit venue wording can
            # establish that two locations differ.
            old_facing, old_move = spatial_tokens(before)
            new_facing, new_move = spatial_tokens(after)
            if old_facing and new_facing and old_facing != new_facing and not has_explanation(current, kind):
                found.append(issue(kind, ids, '面向方向', f'面向{old_facing} → {new_facing}', '核对人物朝向；有真实转身则补明过渡，否则保持方向。'))
            if old_move and new_move and old_move != new_move and not has_explanation(current, kind):
                found.append(issue(kind, ids, '运动方向', f'运动方向{old_move} → {new_move}', '核对运动方向；有真实转向则补明过渡，否则保持方向。'))
            before_positions, after_positions = anchor_positions(before), anchor_positions(after)
            for anchor in set(before_positions) & set(after_positions):
                if before_positions[anchor] != after_positions[anchor] and not has_explanation(current, kind):
                    found.append(issue(kind, ids, f'{anchor}位置', f'{anchor}：{before_positions[anchor]}侧 → {after_positions[anchor]}侧', '核对场景内相对位置；有真实换位则补明过渡。'))
    return found

def check(data):
    missing = missing_material(data)
    if missing:
        return {'status': 'needs_material', 'missing': missing, 'issues': []}
    shots, references = data['shots'], data.get('references', {})
    raw = []
    for shot in shots:
        if not isinstance(shot, dict):
            continue
        raw.extend(intra_shot_field_issues(shot, references))
    established = set()
    for shot in shots:
        for item in reference_issues(shot, references):
            if reference_issue_key(item) not in established:
                raw.append(item)
        established.update(establishes_baseline(shot, references))
    # A documented reference change remains the current baseline across shots
    # that omit the attribute, but a later explicit contradiction must still
    # be reported. The older dedupe set alone hid such contradictions forever.
    carried = {}
    for shot in shots:
        for actor, ref in character_references(references).items():
            if not actor:
                continue
            actual_state = actor_state(shot, actor, references)
            transition = shot.get('transition')
            transition_text = text(transition.get('character')) if isinstance(transition, dict) else text(transition)
            for expected, garment in appearance_tokens(ref):
                actual = colors_for(actual_state, garment)
                transition_value = text(transition.get('character')) if isinstance(transition, dict) else text(transition)
                changed_to = explained_new_color(actual_state + '，' + transition_value, garment) or (actual[0] if len(actual) == 1 else '')
                removed = not actual and bool(re.search(r'(?:没有|未戴|不戴|脱下|取下|摘下)[^，。；;]{0,6}' + re.escape(garment), actual_state))
                if actor_has_explanation(shot, actor, references, garment) and (changed_to or removed):
                    carried[(actor, garment)] = (changed_to or '未佩戴', shot['id'])
                elif (actor, garment) in carried and ((len(actual) == 1 and actual[0] != carried[(actor, garment)][0])
                        or (carried[(actor, garment)][0] == '未佩戴' and bool(actual))):
                    old, old_id = carried[(actor, garment)]
                    new_state = actual[0] + garment if actual else '明确写为未佩戴'
                    raw.append(issue('character', [old_id, shot['id']], garment, f'{actor}：已说明基线为{old}{garment if old != "未佩戴" else ""}，镜头{shot["id"]}又写为{new_state}。', f'核对{actor}的{garment}；保持已建立基线，或补充真实再次变化的过渡。'))
    scene_ref = text(references.get('scene'))
    # A reference can name several permitted places (for example “卧室、阳台
    # 均为本场景”).  It is an allowed-location set, not the state of the first
    # shot.  Establish the rolling baseline only from an actual shot so a
    # reference never creates a fabricated ["01", "01"] comparison.
    scene_baseline = (set(), '')
    light_baseline = {
        '来光方向': (light_direction(scene_ref), shots[0]['id'] if shots else ''),
        '光线色温': (light_temperature(scene_ref), shots[0]['id'] if shots else ''),
        '光线明暗': (light_intensity(scene_ref), shots[0]['id'] if shots else ''),
    }
    for shot in shots:
        space_text = state(shot, 'space')
        current_places = locations(space_text)
        explained_space = bool(space_text and scene_ref and explains_space_change(shot, scene_ref, space_text))
        if explained_space and current_places:
            scene_baseline = (current_places, shot['id'])
        elif current_places:
            previous_places, previous_id = scene_baseline
            if previous_places and not same_location(previous_places, current_places):
                previous_label = '、'.join(sorted(previous_places))
                current_label = '、'.join(sorted(current_places))
                raw.append(issue('space', [previous_id, shot['id']], '地点', f'已说明场景为“{previous_label}”，镜头{shot["id"]}又写为“{current_label}”。', '核对地点；保持最近一次已说明的场景基线，或补充真实换景过渡。'))
            # An explicit current location is the only defensible baseline for
            # the next cut, whether it agrees with the scene reference or not.
            scene_baseline = (current_places, shot['id'])

        light_text = state(shot, 'lighting')
        transition = shot.get('transition')
        transition_light = text(transition.get('lighting')) if isinstance(transition, dict) else text(transition)
        combined_light = '，'.join(filter(None, (transition_light, light_text)))
        light_values = {
            '来光方向': light_direction(light_text),
            '光线色温': light_temperature(light_text),
            '光线明暗': light_intensity(light_text),
        }
        if explains_light_change(shot):
            for aspect, value in light_values.items():
                if value:
                    light_baseline[aspect] = (value, shot['id'])
        else:
            for aspect, value in light_values.items():
                old, old_id = light_baseline[aspect]
                if value and old and value != old:
                    raw.append(issue('lighting', [old_id, shot['id']], aspect, f'已说明光线基线为{old}，镜头{shot["id"]}又写为{value}。', '核对光线；保持最近一次已说明的布光基线，或补充真实变化说明。'))
    inherited_changes = set()
    for previous, current in zip(shots, shots[1:]):
        raw.extend(adjacent_issues(previous, current, references, inherited_changes))
        # Only carry a documented baseline across its immediate textual
        # successor.  Later contradictions are still compared with the
        # successor's explicit state rather than being permanently waived.
        inherited_changes = establishes_baseline(current, references)
    order = {shot['id']: index for index, shot in enumerate(shots)}
    unique = {}
    for item in raw:
        actor_match = re.search(r'核对(.+?)的', item['minimal_change']) if item['category'] == '角色' else None
        key = (item['category'], item['shots'][-1], item['aspect'], actor_match.group(1) if actor_match else '')
        if key not in unique:
            unique[key] = item
        else:
            old = unique[key]
            old['shots'] = sorted(set(old['shots'] + item['shots']), key=order.get)
            old['evidence'] += '；相邻证据：' + item['evidence']
    result = {'status': 'ok', 'scope': f'{len(shots)}个镜头', 'missing': [], 'issues': list(unique.values())}
    severity_rank = {'high': 0, 'medium': 1, 'low': 2}
    result['issues'].sort(key=lambda item: (severity_rank.get(item['severity'], 9), order[item['shots'][0]], order[item['shots'][-1]], KINDS[tuple(CN.values()).index(item['category'])]))
    unattributed = [shot['id'] for shot in shots if appearance_tokens(state(shot, 'character')) and not subject(shot, references)]
    if unattributed:
        result['notes'] = ['人物身份不能安全对齐的镜头：' + '、'.join(map(str, unattributed)) + '；未猜测同一人物，需补character_id或人工核对。']
    uncertain_props = []
    for previous, current in zip(shots, shots[1:]):
        before_identity, after_identity = subject(previous, references), subject(current, references)
        before_character = state(previous, 'character') + '，' + state(previous, 'description') + '，' + state(previous, 'visual')
        after_character = state(current, 'character') + '，' + state(current, 'description') + '，' + state(current, 'visual')
        anonymous = r'(?:他|她|他们|她们|人物|角色|一位|一个人|男人|女人|男孩|女孩)'
        if (not before_identity and not after_identity
                and re.search(anonymous, before_character) and re.search(anonymous, after_character)):
            before_prop, after_prop = state(previous, 'prop'), state(current, 'prop')
            has_handoff_risk = bool(re.search(r'(?:拿|持|握|提|捧|抱|拎).{0,8}(?:纸袋|手机|杯|书|包|伞|钥匙|花)', before_prop)
                and (re.search(r'双手空|手中空', after_prop) or re.search(r'(?:没有|未)(?:拿|持|握)?(?:着)?.{0,2}(?:纸袋|手机|杯|书|包|伞|钥匙|花)', after_prop)))
            if has_handoff_risk:
                uncertain_props.append(f"{previous['id']}→{current['id']}")
    if uncertain_props:
        result.setdefault('notes', []).append('人物身份不能安全对齐的道具变化：' + '、'.join(uncertain_props) + '；未将两镜头合并为同一人物，需补character_id或人工核对持有关系。')
    return result

def intra_shot_field_issues(shot, references):
    """Catch contradictory explicit states across fields of one shot."""
    found = []
    identifier = str(shot.get('id', '?'))
    refs = character_references(references)
    names = [name for name in refs if name]
    text_fields = ('character', 'description', 'visual')
    if not names:
        names = list(dict.fromkeys(name for key in text_fields for name in named_actors(text(shot.get(key)))))
    garments = set(GARMENTS)
    for ref in refs.values():
        garments.update(garment for garment in GARMENTS if garment in ref)
    for actor in names or ['人物']:
        values_by_garment = {}
        for key in text_fields:
            value = text(shot.get(key))
            if not value:
                continue
            if actor != '人物' and len(names) > 1:
                value = actor_scoped_text(value, shot, actor, references)
            elif actor != '人物' and refs and actor not in value and len(names) == 1:
                # The single referenced character may be described in another
                # field without repeating their name.
                pass
            for garment in garments:
                colors = colors_for(value, garment)
                for color in colors:
                    values_by_garment.setdefault(garment, []).append((key, color))
        for garment, values in values_by_garment.items():
            distinct = list(dict.fromkeys(color for _, color in values))
            if len(distinct) > 1:
                evidence = '；'.join(f'{key}写为{color}{garment}' for key, color in values)
                label = f'{actor}的{garment}' if actor != '人物' else garment
                found.append(issue('character', [identifier], garment, evidence,
                    f'核对同一镜头中{label}的字段描述，保留一个真实状态。'))
    # A multi-value result intentionally becomes empty in light_direction()
    # so a cross-shot comparison cannot guess a baseline.  Within one shot,
    # however, the explicit conflict must be reported, including prose fields.
    direction_values = []
    for key in ('lighting', 'description', 'visual'):
        for direction in explicit_light_directions(text(shot.get(key))):
            direction_values.append((key, direction))
    directions = list(dict.fromkeys(direction for _, direction in direction_values))
    if len(directions) > 1:
        evidence = '；'.join(f'{key}写为来自{direction}侧' for key, direction in direction_values)
        found.append(issue('lighting', [identifier], '来光方向', evidence,
            '核对本镜头的来光方向，只保留一个实际布光状态。'))
    return found

def main(path):
    print(json.dumps(check(json.loads(Path(path).read_text(encoding='utf-8'))), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: check_continuity.py INPUT.json')
    main(sys.argv[1])
