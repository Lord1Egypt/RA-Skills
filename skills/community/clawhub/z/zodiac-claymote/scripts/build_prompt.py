#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提示词装配器 —— 十二生肖黏土软萌风表情包

用法:
  python build_prompt.py --list
  python build_prompt.py --zodiac 龙 --job 工程师 --emotion 崩溃 --scene 线上出Bug
  python build_prompt.py --zodiac dragon --job teacher --emotion 抓狂 --text 改不完
  python build_prompt.py --set 16 --zodiac 猪 --job 学生 --out out/prompts.md
  python build_prompt.py --set 24 --mix --out out/full24.md

中英文均可作为生肖/职业/情绪参数（避免终端编码问题）。
"""
import argparse
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ---------------------------------------------------------------- 数据区

# 生肖角色（原创设定，取自 references/zodiac-characters.md）
ZODIAC = {
    "鼠": dict(
        en="mouse", aliases=["rat", "shu", "mouse"],
        body="teardrop-shaped body, two oversized thin leaf-like round ears, two prominent front teeth, thin curled tail with a small curl at the tip",
        main="misty blue-grey #A9BACB", accent="milky white belly #FBF7F0 and pink ears #FFC2CE",
        face="big glossy bean eyes with highlight dots, low-set eyes",
        jobs=["财务", "行政", "科研"],
    ),
    "牛": dict(
        en="baby bull", aliases=["ox", "cow", "niu", "bull"],
        body="stocky body with shoulders wider than head, two stubby sprouting horns, pink oval nose, four short legs",
        main="creamy white #F7F1E8", accent="caramel horns #C98F4E",
        face="gentle bean eyes, small blush cheeks",
        jobs=["工程师", "建筑", "外卖", "安保"],
    ),
    "虎": dict(
        en="tiger cub", aliases=["tiger", "hu", "tiger cub"],
        body="round face with wide puffy cheeks, two small semicircle ears flat on head sides, short tail pointing up",
        main="warm orange #F2A03D", accent="three dark brown stripes #8A5A2B (two on forehead, one on side) and creamy white chest",
        face="big rounded eyes, wide expressive eyebrows",
        jobs=["销售", "老板", "安保", "教师"],
    ),
    "兔": dict(
        en="lop-eared rabbit", aliases=["rabbit", "tu", "bunny"],
        body="rice-dumpling shaped body, long ears drooping below the shoulders, cotton-ball tail, three-lobed mouth",
        main="milky pink-white #FBEFEA", accent="peach inner ears #FFAFBC",
        face="soft shiny eyes, tiny blush",
        jobs=["教师", "护士", "客服", "HR", "学生"],
    ),
    "龙": dict(
        en="baby dragon", aliases=["dragon", "long", "loong"],
        body="barrel-shaped body, two tiny sprout-like horns, three soft rounded fins on the back, tiny wings too short to fly, belly scale pattern",
        main="moss green #7FB77E", accent="golden belly #F5C542 and pale gold horns #E8D6A0",
        face="big bright eyes, confident brows",
        jobs=["产品", "运营", "设计师"],
    ),
    "蛇": dict(
        en="snake", aliases=["snake", "she"],
        body="lower body coiled into a spring spiral on the ground, upper body standing upright, no limbs, tail tip used as a hand, small forked tongue tip",
        main="mint green #9FD8CB", accent="creamy yellow belly #F7E9A0",
        face="vertical oval eyes, calm half-lidded look",
        jobs=["法务", "工程师", "财务", "科研"],
    ),
    "马": dict(
        en="pony", aliases=["horse", "ma", "pony"],
        body="short thick neck, mane as three round puffballs, brush-like short tail, four small round hooves",
        main="chestnut brown #B07D56", accent="cream mane #EFDCC3",
        face="wide eager eyes, flared nostrils",
        jobs=["外卖", "销售", "运营"],
    ),
    "羊": dict(
        en="sheep", aliases=["sheep", "yang", "lamb"],
        body="whole body a cloud-like wool ball made of stacked spheres, face peeking out of the fluff, thin short legs, two spiral horns",
        main="cream white #F6F1E4", accent="light brown face and ears #C9A88C",
        face="sleepy gentle eyes, small smile",
        jobs=["行政", "通用"],
    ),
    "猴": dict(
        en="monkey", aliases=["monkey", "hou"],
        body="large heart-shaped face, two small round fan-like ears on the sides, long thin tail curled into a question mark",
        main="honey-brown #C98A5E", accent="light pink face #FFC9AE",
        face="big playful eyes, mischievous brows",
        jobs=["运营", "产品", "设计师", "工程师"],
    ),
    "鸡": dict(
        en="rooster chick", aliases=["rooster", "chick", "ji", "chicken"],
        body="egg-drop shaped body, three-lobed soft crown on head, small triangular beak, two small round wings close to body, three upright tail feathers",
        main="goose-yellow #F8D35C", accent="orange-red comb #F26B4E",
        face="round alert eyes, high-energy brows",
        jobs=["教师", "客服", "销售"],
    ),
    "狗": dict(
        en="puppy", aliases=["dog", "gou", "puppy"],
        body="two big floppy ears reaching the chin, shiny black round nose, short stick-like wagging tail, white chest patch",
        main="milk-coffee #D9B08C", accent="dark coffee drooping ears #8C6A4F and white chest #FDF8F0",
        face="big loyal eyes with lower eyelid line",
        jobs=["行政", "客服", "护士", "学生"],
    ),
    "猪": dict(
        en="piglet", aliases=["pig", "zhu", "piglet"],
        body="nearly spherical body, flat round snout with two nostrils, two triangle flag-like ears, tail curled into a ring, four small round hooves",
        main="peach-pink #FFB7B2", accent="deeper pink ears and hooves #F08A8A",
        face="small content eyes, permanent rosy cheeks",
        jobs=["学生", "自由职业", "厨师", "设计师"],
    ),
}

# 职业（取自 references/professions.md）
JOBS = {
    "教师": dict(aliases=["teacher", "老师"], outfit="a navy knit vest over a white shirt with a red pen clipped at the collar",
                 prop="a stack of exercise books", scene="in front of a small chalkboard covered in neat writing"),
    "学生": dict(aliases=["student"], outfit="a school uniform with a backpack",
                 prop="a pencil", scene="at a small classroom desk with a tower of textbooks"),
    "工程师": dict(aliases=["engineer", "programmer", "coder", "程序员"],
                   outfit="a grey-blue plaid shirt with a lanyard badge and round glasses",
                   prop="a mechanical keyboard", scene="at a desk with two monitors covered in sticky notes, a red error popup on screen"),
    "护士": dict(aliases=["nurse"], outfit="a light blue nurse uniform with a small cap and a mask pulled down to the chin",
                 prop="a medical chart", scene="in a quiet hospital corridor at night"),
    "医生": dict(aliases=["doctor"], outfit="a white coat with a stethoscope",
                 prop="a clipboard", scene="in a small clinic room"),
    "产品": dict(aliases=["pm", "产品经理"], outfit="a simple knit sweater over a shirt",
                 prop="a slim laptop", scene="beside a whiteboard covered in sticky notes"),
    "设计师": dict(aliases=["designer"], outfit="a black tee with round glasses",
                   prop="a drawing tablet pen", scene="at a monitor showing a design draft"),
    "运营": dict(aliases=["ops", "operator"], outfit="a casual hoodie with a lanyard",
                 prop="a phone showing a data dashboard", scene="at a workstation with charts on screen"),
    "销售": dict(aliases=["sales"], outfit="a slightly tight dark suit with a tie",
                 prop="a phone with a message bubble", scene="standing in a plain office corner"),
    "财务": dict(aliases=["finance", "会计"], outfit="a plain shirt with sleeve covers and a visor",
                 prop="a calculator", scene="buried under a mountain of invoices and receipts"),
    "老板": dict(aliases=["boss", "领导"], outfit="a dark suit with a tie",
                 prop="a teacup", scene="at the head of a tiny meeting table"),
    "客服": dict(aliases=["service"], outfit="a work uniform with a headset mic",
                 prop="a phone handset", scene="at a customer service desk"),
    "外卖": dict(aliases=["delivery", "快递"], outfit="a plain windbreaker with a plain helmet without any logo",
                 prop="an insulated delivery box", scene="on a street corner in a hurry"),
    "科研": dict(aliases=["researcher", "研究生"], outfit="a white lab coat with safety goggles",
                 prop="a test tube", scene="in a small laboratory"),
    "行政": dict(aliases=["admin"], outfit="a tidy office vest with a badge",
                 prop="a folder", scene="at a tidy office desk"),
    "厨师": dict(aliases=["chef", "餐饮"], outfit="a white chef jacket with a small tall hat",
                 prop="a frying pan", scene="in a small kitchen"),
    "安保": dict(aliases=["guard", "保安"], outfit="a dark blue uniform with a cap",
                 prop="a walkie-talkie", scene="in a small guard booth"),
    "建筑": dict(aliases=["builder", "工人"], outfit="a plain reflective vest with a plain safety helmet",
                 prop="a measuring tape", scene="on a simple construction site"),
    "HR": dict(aliases=["hr"], outfit="a professional suit",
               prop="a stack of resumes", scene="in a small interview room"),
    "法务": dict(aliases=["legal", "lawyer"], outfit="a formal suit with thin-rimmed glasses",
                 prop="a contract with red annotations", scene="at a desk piled with documents"),
    "自由职业": dict(aliases=["freelancer"], outfit="loose comfortable home clothes",
                     prop="a laptop", scene="on a cozy sofa at home"),
    "通用": dict(aliases=["none", "general", "无"], outfit="simple everyday casual clothes",
                 prop="a phone", scene="in a plain everyday setting"),
}

# 情绪（取自 references/scenes-emotions.md）
EMOTIONS = {
    "开心": dict(aliases=["happy"], en="happy expression: crescent moon eyes, big open smile, both arms raised",
                 symbol="small sparkles and stars around", text="好耶"),
    "狂喜": dict(aliases=["ecstatic"], en="ecstatic expression: eyes glowing, mouth wide open laughing, jumping up",
                 symbol="confetti and gold sparkles", text="太好了"),
    "害羞": dict(aliases=["shy"], en="shy expression: curved shy eyes, both paws covering the face, heavy blush",
                 symbol="small floating hearts", text="害羞"),
    "撒娇": dict(aliases=["cute"], en="acting-cute expression: huge glossy eyes, body swaying, both paws together pleading",
                 symbol="heart bubbles", text="求放过"),
    "期待": dict(aliases=["eager"], en="expectant expression: bright shiny eyes, leaning forward, rubbing paws together",
                 symbol="glossy highlight sparkles", text="期待"),
    "得意": dict(aliases=["smug"], en="smug expression: narrow eyes curving up, crooked smirk, chest puffed out",
                 symbol="a tiny crown and upward arrows", text="稳了"),
    "骄傲": dict(aliases=["proud"], en="proud expression: closed satisfied eyes, nodding, one paw giving a thumbs-up",
                 symbol="a bright shine flash", text="可以"),
    "疑惑": dict(aliases=["confused"], en="confused expression: one eye wide one eye squinted, head tilted, mouth in a small o",
                 symbol="a floating question mark", text="？？？"),
    "震惊": dict(aliases=["shocked"], en="shocked expression: eyes bulging round, mouth a big o, body leaning back",
                 symbol="lightning bolts", text="什么！"),
    "惊恐": dict(aliases=["terrified"], en="terrified expression: eyes shrunk to tiny dots, sweat spraying, mouth agape",
                 symbol="cold sweat droplets and panic lines", text="救命"),
    "委屈": dict(aliases=["wronged"], en="wronged expression: downturned八字 eyebrows, teary shining eyes, mouth corners pulled down",
                 symbol="a few teardrops", text="委屈"),
    "大哭": dict(aliases=["crying"], en="crying hard expression: eyes squeezed shut, mouth wide open wailing, paws rubbing eyes",
                 symbol="a waterfall of tears", text="呜呜"),
    "心碎": dict(aliases=["heartbroken"], en="heartbroken expression: half-closed sad eyes, paws clutching the chest, body curling forward",
                 symbol="a cracked heart", text="心碎"),
    "生气": dict(aliases=["angry"], en="angry expression: inverted-V eyebrows, puffed cheeks, pouting mouth, paws on hips",
                 symbol="anger cross marks", text="生气"),
    "崩溃": dict(aliases=["crash", "抓狂", "freaking"], en="freaking-out expression: eyebrows knitted, eyes squeezed into wrinkled crescents, mouth wide open shouting, both paws clutching the head",
                 symbol="radiating anger lines and sweat", text="我裂开"),
    "无语": dict(aliases=["speechless"], en="speechless expression: two vertical line eyes, a single straight-line mouth, head slightly turned away",
                 symbol="a black line and a tiny crow", text="无语"),
    "不屑": dict(aliases=["disdain"], en="disdainful expression: half-open eyes rolled up, mouth corner pulled down",
                 symbol="a small floating cloud", text="就这？"),
    "阴阳怪气": dict(aliases=["passive"], en="passive-aggressive expression: fake curved smile with cold half-lidded eyes",
                     symbol="a pair of quotation marks", text="谢谢你"),
    "摆烂": dict(aliases=["giveup"], en="giving-up expression: flat lined eyes, both paws spread open in a shrug, body collapsed down",
                 symbol="ZZZ and a dried-fish prop", text="摆了"),
    "摸鱼": dict(aliases=["slack"], en="slacking-off expression: squinting eyes, pretending to be serious while hiding a phone",
                 symbol="a small fish symbol", text="摸了"),
    "困倦": dict(aliases=["sleepy"], en="sleepy expression: half-closed droopy eyes, visible dark eye circles, small yawn",
                 symbol="three floating ZZZ", text="困"),
    "饥饿": dict(aliases=["hungry"], en="hungry expression: starry eyes, mouth wide open, paws holding the belly",
                 symbol="a small fork and knife", text="饿了"),
    "社恐": dict(aliases=["anxious"], en="socially-anxious expression: curled into a ball, eyes darting away, sweat drop",
                 symbol="sweat droplets", text="社恐"),
    "佛系": dict(aliases=["zen"], en="zen expression: closed smiling eyes, sitting cross-legged, both paws together",
                 symbol="a soft halo glow", text="随缘"),
}

# 场景（可选，覆盖职业默认场景）
SCENES = {
    "线上出Bug": "at a desk with two monitors, a glowing red error popup, paws frozen mid-air above the keyboard",
    "改需求": "surrounded by piles of revised documents and sticky notes everywhere",
    "加班深夜": "alone in an office at night with only one desk lamp on, city lights outside the window",
    "汇报": "standing before a projected slide, pointing with a tiny stick",
    "发工资": "holding a tiny pay slip, squinting closely at the number",
    "下班": "standing at a doorway with a small bag, a wall clock showing 18:00",
    "早八": "sitting at a classroom desk in early morning light, head nodding off",
    "考试": "at an exam desk with a test paper, pencil in paw",
    "午休": "lying face down on a desk, cheek squished flat, a tiny drool bubble",
    "摸鱼中": "at a desk pretending to work, a phone hidden under the desk",
    "会议": "sitting at a small meeting table with a blank stare",
    "沙发刷手机": "sunk deep into a cozy sofa, phone in paw, screen glow on the face",
    "奶茶": "hugging an oversized cup of milk tea with both arms",
    "逢年过节": "wearing a tiny festive hat, holding an oversized red envelope",
    "通勤": "squeezed in a tiny metro cart, hanging on a handrail",
    "日常": "in a plain everyday setting",
}

# 固定段（整套锁定，见 references/style-bible.md）
STYLE = ("soft polymer clay material, smooth matte surface with subtle fingerprint marks, "
         "rounded beveled edges, no sharp corners, chibi proportions with head-body ratio 1:1, "
         "round ball body, short stubby limbs, round mitten hands without visible fingers, "
         "solid handmade clay texture, soft subsurface scattering on edges, blind-box toy aesthetic")
CAMERA = ("three-quarter front view, slight 15-degree high angle, centered composition, "
          "subject fills 75% of frame, warm studio three-point lighting, soft contact shadow beneath")
TECH = "square 1:1, high detail, clean isolated subject easy to cut out, sticker-friendly, 8k"
NEGATIVE = ("realistic photography, photorealistic, human face, human skin, horror, creepy, gore, "
            "extra limbs, extra fingers, deformed hands, mutated body, asymmetric eyes, cross-eyed, "
            "text, letters, watermark, logo, signature, artist name, brand mark, "
            "blurry, lowres, jpeg artifacts, noise, oversaturated, dark background, busy background, "
            "sharp spikes, metallic gloss, fur texture, ceramic glaze, multiple characters, split panel, comic frame")

BG_COLOR = "cream #F5EFE6"

# 16 张一套的情绪配比（顺序即展示顺序）
SET16 = ["开心", "无语", "崩溃", "摸鱼", "委屈", "得意", "困倦", "惊恐",
         "撒娇", "心碎", "摆烂", "震惊", "生气", "期待", "阴阳怪气", "狂喜"]
SET24 = SET16 + ["害羞", "社恐", "佛系", "骄傲", "疑惑", "饥饿", "不屑", "大哭"]


# ---------------------------------------------------------------- 工具函数

def _resolve(value, table, kind):
    """按中文名或英文名别名解析键"""
    if not value:
        return None
    if value in table:
        return value
    low = value.strip().lower()
    for key, item in table.items():
        if low in [a.lower() for a in item.get("aliases", [])] or low == item.get("en", "").lower():
            return key
    raise SystemExit(f"[错误] 找不到{kind}: {value}\n可用: {', '.join(table.keys())}\n"
                     f"（也可用英文别名，如 dragon / teacher / angry；用 --list 查看全部）")


def _resolve_soft(value, table, default):
    """解析失败时回退到默认值，不抛错（成套批量生成时用）"""
    try:
        return _resolve(value, table, "")
    except SystemExit:
        return default


def build(zodiac, job, emotion, scene=None, text=None, bg=BG_COLOR):
    z = ZODIAC[zodiac]
    j = JOBS[job]
    e = EMOTIONS[emotion]
    scene_en = SCENES.get(scene) if scene else j["scene"]
    scene_name = scene or "职业默认场景"

    en = (
        f"A chubby round {z['en']}, {z['body']}, colored in {z['main']} with {z['accent']} accents, "
        f"{z['face']}, wearing {j['outfit']}, holding {j['prop']}, {scene_en}, {e['en']}, {e['symbol']}, "
        f"simple clean {bg} background, subtle depth of field. "
        f"{STYLE}. {CAMERA}. {TECH}."
    )
    caption = text or e["text"]
    return {"zodiac": zodiac, "creature_en": z["en"], "job": job, "emotion": emotion,
            "scene": scene_name, "caption": caption, "en": en,
            "colors": f"{z['main']} ＋ {z['accent']}",
            "outfit": j["outfit"], "prop": j["prop"], "scene_en": scene_en,
            "negative": NEGATIVE}


def render(items, title="表情包提示词"):
    lines = [f"# {title}", "",
             "> 画风固定段（整套不可改）：黏土软胶材质 + chibi 1:1 + 暖色三点光 + 1:1 正方形",
             "> 负向提示词统一使用文末 [NEGATIVE]，每张一致。", ""]
    for i, it in enumerate(items, 1):
        lines += [
            f"## {i:02d} · {it['zodiac']} × {it['job']} · {it['emotion']}",
            "",
            f"- **场景**：{it['scene']}",
            f"- **配色**：{it['colors']}",
            f"- **服装**：{it['outfit']}",
            f"- **道具**：{it['prop']}",
            f"- **文案**（后期叠加，不进提示词）：**{it['caption']}**",
            "",
            "**英文提示词（复制这段）**",
            "```",
            it["en"],
            "```",
            "",
        ]
    lines += ["---", "", "**负向提示词（每张都带）**", "```", NEGATIVE, "```", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------- CLI

def main():
    ap = argparse.ArgumentParser(description="十二生肖黏土软萌风表情包提示词装配器")
    ap.add_argument("--zodiac", "-z", help="生肖：中文（龙）或英文（dragon）")
    ap.add_argument("--job", "-j", help="职业：中文（工程师）或英文（engineer）")
    ap.add_argument("--emotion", "-e", help="情绪：中文（崩溃）或英文（crash）")
    ap.add_argument("--scene", "-s", help="场景：如 线上出Bug / 加班深夜（可选，默认用职业场景）")
    ap.add_argument("--text", "-t", help="表情包中文文案（不进提示词，后期叠加）")
    ap.add_argument("--bg", default=BG_COLOR, help="背景色")
    ap.add_argument("--set", type=int, choices=[16, 24], help="生成成套：16 或 24 张")
    ap.add_argument("--mix", action="store_true", help="配合 --set：12 生肖轮换（默认单一生肖）")
    ap.add_argument("--out", "-o", help="输出 markdown 文件路径")
    ap.add_argument("--json", action="store_true", help="输出 JSON 而非 Markdown")
    ap.add_argument("--list", action="store_true", help="列出所有可选项")
    args = ap.parse_args()

    if args.list:
        print("生肖：", " / ".join(ZODIAC.keys()))
        print("职业：", " / ".join(JOBS.keys()))
        print("情绪：", " / ".join(EMOTIONS.keys()))
        print("场景：", " / ".join(SCENES.keys()))
        print("\n推荐搭配：")
        for k, z in ZODIAC.items():
            print(f"  {k} → {' / '.join(z['jobs'])}")
        return

    if args.set:
        emotions = SET16 if args.set == 16 else SET24
        zodiacs = (list(ZODIAC.keys()) if args.mix
                   else [_resolve(args.zodiac, ZODIAC, "生肖") if args.zodiac else "猪"])
        if args.mix:
            zodiac = _resolve(args.zodiac, ZODIAC, "生肖") if args.zodiac else None
        items = []
        for i, emo in enumerate(emotions):
            z = zodiacs[i % len(zodiacs)]
            j = args.job or ZODIAC[z]["jobs"][0]
            job_key = args.job or ZODIAC[z]["jobs"][i % len(ZODIAC[z]["jobs"])]
            job_key = _resolve_soft(job_key, JOBS, "通用")
            items.append(build(z, job_key, emo, args.scene, bg=args.bg))
        title = f"{args.set} 张成套表情包提示词（{'12生肖轮换' if args.mix else zodiacs[0]} × {args.job or '推荐职业轮换'}）"
    else:
        if not (args.zodiac and args.job and args.emotion):
            ap.error("单张模式需要 --zodiac --job --emotion（或用 --set 成套生成 / --list 查看选项）")
        z = _resolve(args.zodiac, ZODIAC, "生肖")
        j = _resolve(args.job, JOBS, "职业")
        e = _resolve(args.emotion, EMOTIONS, "情绪")
        items = [build(z, j, e, args.scene, args.text, args.bg)]
        title = f"{z} × {j} · {e}"

    if args.json:
        import json
        out = json.dumps(items, ensure_ascii=False, indent=2)
    else:
        out = render(items, title)

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"[完成] 已写入 {os.path.abspath(args.out)}  （共 {len(items)} 条）")
    else:
        print(out)


if __name__ == "__main__":
    main()
