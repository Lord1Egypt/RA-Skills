#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xuan-Ping Domain Divination (I-Ching) - Easter egg for Universal Domain Risk &
Xuan-Ping Review.

Normalizes the domain + SHA256 -> deterministically maps to one of the 64 King
Wen hexagrams + a moving line. Pure entertainment, reproducible (same domain
always gives the same hexagram), non-random, never a risk conclusion, never part
of the formal assessment.
"""
import sys, json, hashlib

# King Wen order: number | Chinese name | English name | short hexagram text
HEXAGRAMS = [
    (1,"乾为天","The Creative / Heaven","Yuan, heng, li, zhen. The movement of heaven is full of power; the superior person makes himself strong and untiring."),
    (2,"坤为地","The Receptive / Earth","Yuan, heng. The superior person, with the breadth of earth, carries all things with virtue."),
    (3,"水雷屯","Difficulty at the Beginning","Great progress and perseverance; do not undertake a journey, but establish a helper."),
    (4,"山水蒙","Youthful Folly","Success. It is not I who seek the young fool; the young fool seeks me."),
    (5,"水天需","Waiting (Nourishment)","With sincerity, light and success; perseverance brings good fortune; it furthers one to cross the great water."),
    (6,"天水讼","Conflict","Sincerity is obstructed; a halt midway brings good fortune, the end brings misfortune."),
    (7,"地水师","The Army","Perseverance; an experienced leader brings good fortune, no blame."),
    (8,"水地比","Holding Together","Good fortune. Re-examine with the oracle; if there is sublime perseverance, no blame."),
    (9,"风天小畜","Small Taming","Success. Dense clouds, no rain from our western suburbs."),
    (10,"天泽履","Treading (Conduct)","Treading on the tail of the tiger; it does not bite. Success."),
    (11,"地天泰","Peace","The small departs, the great arrives; good fortune and success."),
    (12,"天地否","Stagnation / Standstill","The great departs, the small arrives; no enterprise is furthered now."),
    (13,"天火同人","Fellowship with Others","Fellowship in the open; success. It furthers one to cross the great water."),
    (14,"火天大有","Great Possession","Great progress and success through the great yielding in a high place."),
    (15,"地山谦","Modesty","Success; the superior person carries things through to the end."),
    (16,"雷地豫","Enthusiasm","It furthers one to install helpers and set the armies marching."),
    (17,"泽雷随","Following","Great progress and perseverance; no blame."),
    (18,"山风蛊","Work on the Decayed","Great success; it furthers one to cross the great water. Consider three days before and after the turning point."),
    (19,"地泽临","Approach","Great progress and perseverance; in the eighth month there will be misfortune."),
    (20,"风地观","Contemplation (View)","The ablution has been made, but not yet the offering; sincerity and a dignified bearing."),
    (21,"火雷噬嗑","Biting Through","Success; it furthers one to let the law take its course."),
    (22,"山火贲","Grace","Success; in small matters it furthers one to undertake something."),
    (23,"山地剥","Splitting Apart","It does not further one to undertake anything now."),
    (24,"地雷复","Return (The Turning Point)","Success; going out and coming in without harm; friends come without blame."),
    (25,"天雷无妄","Innocence (The Unexpected)","Great progress and perseverance; if one is not as one should be, there is misfortune."),
    (26,"山天大畜","Great Taming","Perseverance furthers; not eating at home brings good fortune; it furthers to cross the great water."),
    (27,"山雷颐","The Corners of the Mouth (Nourishment)","Perseverance brings good fortune; observe how nourishment is sought and provided."),
    (28,"泽风大过","Great Preponderance","The ridgepole sags; it furthers one to have somewhere to go. Success."),
    (29,"坎为水","The Abysmal (Water)","Repetition of the abyss; if you are sincere, you have success in your heart."),
    (30,"离为火","The Clinging (Fire)","Perseverance furthers; it brings success; care of the cow brings good fortune."),
    (31,"泽山咸","Influence (Wooing)","Success; perseverance furthers; taking a maiden to wife brings good fortune."),
    (32,"雷风恒","Duration","Success, no blame; perseverance furthers; it furthers one to have somewhere to go."),
    (33,"天山遁","Retreat","Success; in what is small, perseverance furthers."),
    (34,"雷天大壮","Great Power","Perseverance furthers."),
    (35,"火地晋","Progress","The marquis is honored with many horses; received three times in a single day."),
    (36,"地火明夷","Darkening of the Light","In adversity it furthers one to be persevering."),
    (37,"风火家人","The Family (The Clan)","The perseverance of the woman furthers."),
    (38,"火泽睽","Opposition","In small matters, good fortune."),
    (39,"水山蹇","Obstruction","The southwest furthers; the northeast does not. It furthers one to see the great person; perseverance brings good fortune."),
    (40,"雷水解","Deliverance","The southwest furthers; if there is nowhere to go, returning brings good fortune."),
    (41,"山泽损","Decrease","With sincerity, great good fortune, no blame; constancy furthers."),
    (42,"风雷益","Increase","It furthers one to undertake something; it furthers to cross the great water."),
    (43,"泽天夬","Breakthrough (Resoluteness)","One must resolutely make the matter known at the court; it is not furthered by resorting to arms."),
    (44,"天风姤","Coming to Meet","The maiden is powerful; one should not marry such a maiden."),
    (45,"泽地萃","Gathering Together","Success; the king approaches his temple; it furthers one to see the great person."),
    (46,"地风升","Pushing Upward","Great success; one sees the great person; do not worry; a journey to the south brings good fortune."),
    (47,"泽水困","Oppression (Exhaustion)","Success; the great person brings good fortune, no blame."),
    (48,"水风井","The Well","The town may be changed, but the well cannot; nothing lost, nothing gained."),
    (49,"泽火革","Revolution (Molting)","On one's own day one is believed; great progress, success, furthering through perseverance; remorse disappears."),
    (50,"火风鼎","The Cauldron","Supreme good fortune; success."),
    (51,"震为雷","The Arousing (Thunder)","Success; thunder comes terrifying, then laughing words and rejoicing."),
    (52,"艮为山","Keeping Still (Mountain)","Keeping still; rest when it is time to rest, act when it is time to act."),
    (53,"风山渐","Development (Gradual Progress)","The maiden's marriage brings good fortune; perseverance furthers."),
    (54,"雷泽归妹","The Marrying Maiden","Undertakings bring misfortune; nothing that might further."),
    (55,"雷火丰","Abundance (Fullness)","Success; the king attains abundance; be not sad, be like the sun at midday."),
    (56,"火山旅","The Wanderer","Small success; the wanderer's perseverance furthers."),
    (57,"巽为风","The Gentle (Penetrating Wind)","Small success; it furthers one to have somewhere to go and to see the great person."),
    (58,"兑为泽","The Joyous (Lake)","Success; perseverance furthers."),
    (59,"风水涣","Dispersion (Dissolution)","Success; the king approaches his temple; it furthers to cross the great water; perseverance furthers."),
    (60,"水泽节","Limitation","Success; bitter limitation must not be persevered in."),
    (61,"风泽中孚","Inner Truth","Pigs and fishes bring good fortune; it furthers to cross the great water; perseverance furthers."),
    (62,"雷山小过","Small Preponderance","Success; perseverance furthers; small things may be done, great things should not."),
    (63,"水火既济","After Completion","Success in small matters; perseverance furthers; at the beginning good fortune, at the end disorder."),
    (64,"火水未济","Before Completion","Success; the little fox, having nearly crossed, gets its tail wet; nothing furthers."),
]

# Playful one-line readings (entertainment only, never a decision basis)
FORTUNES = [
    "An upright hexagram - stay on the straight path and keep operations steady.",
    "Read the small signs: a few details can still be polished; fixing them makes things steadier.",
    "Deviations retreat before clarity; defenses are sound without, keep diligence within.",
    "Crouching and gathering strength; the foundation holds, and slow progress is still progress.",
    "Set yourself straight before setting others straight; a domain's outward face rests on its inward credit.",
    "Take the hexagram as a mirror, spotting hidden gaps before they form; mend today, ease tomorrow.",
    "Motion and stillness both fit; consolidation is ample, but choose the moment for expansion.",
]

def normalize(d):
    import re
    d = d.strip().lower()
    d = re.sub(r'^https?://', '', d)
    d = re.sub(r'^www\.', '', d)
    return d.split('/')[0]

def divine(domain):
    d = normalize(domain)
    h = hashlib.sha256(d.encode('utf-8')).hexdigest()
    n = int(h[:8], 16)
    gua = HEXAGRAMS[n % 64]
    yao = (n >> 8) % 6 + 1          # moving line 1-6 (from bottom up)
    fortune = FORTUNES[(n >> 12) % len(FORTUNES)]
    yao_ord = ["first", "second", "third", "fourth", "fifth", "top"][yao-1]
    return {
        "domain": d,
        "method": "Normalize domain -> SHA256 -> King Wen hexagram order + moving line (deterministic; same domain always same hexagram)",
        "gua_number": gua[0],
        "gua_name": gua[1],
        "gua_name_en": gua[2],
        "gua_ci": gua[3],
        "moving_yao": yao,
        "yao_label": yao_ord + " line",
        "fortune": fortune,
        "signature": f"Hexagram {gua[0]:02d} | {gua[2]} | moving {yao_ord} line",
        "disclaimer": "Xuan-Ping divination is a pure entertainment Easter egg; it is not a risk conclusion and not a decision basis. Rely on the red/amber/green evidence above.",
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"error":"Usage: divination.py <domain>"}, ensure_ascii=False)); sys.exit(1)
    print(json.dumps(divine(sys.argv[1]), ensure_ascii=False, indent=2))
