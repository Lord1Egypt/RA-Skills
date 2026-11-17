#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四库收录/存目判定（wenbo-research Step 3）

判定顺序：
  1. 命中预置索引 → 直接输出「收录 / 存目」＋置信度；
  2. 未命中 → 可选查百度百科 API 辅助（仅作线索，不代替《四库全书总目》定谳）。

用法:
    python3 siku_status.py 延绥镇志 九边图论 读史方舆纪要
    python3 siku_status.py 某某书 --web      # 未命中时查百科辅助
    python3 siku_status.py --list            # 列出预置索引全部条目

说明:
    - 「存目」→ 提示补源（存目丛书 / 续修四库 / 原刻方志）。
    - 权威判定最终以《四库全书总目》为准，本脚本输出附置信度，不冒充定谳。
"""
import json
import sys
import urllib.parse
import urllib.request

# 预置索引：书名 -> {status, category, confidence, note}
INDEX = {
    "读史方舆纪要": {"status": "收录", "category": "史部·地理类·总志之属", "confidence": "高",
                     "note": "四库本经删改、缺卷，须对勘"},
    "陕西通志": {"status": "收录", "category": "史部·地理类·都会郡县之属", "confidence": "高",
                 "note": "雍正敕修100卷；另有嘉靖赵廷瑞40卷本为存目"},
    "明史": {"status": "收录", "category": "史部·正史类", "confidence": "高", "note": ""},
    "史记": {"status": "收录", "category": "史部·正史类", "confidence": "高", "note": ""},
    "汉书": {"status": "收录", "category": "史部·正史类", "confidence": "高", "note": ""},
    "后汉书": {"status": "收录", "category": "史部·正史类", "confidence": "高", "note": ""},
    "水经注": {"status": "收录", "category": "史部·地理类·河渠之属", "confidence": "高",
               "note": "四库本为戴震校殿本，经删改"},
    "三辅黄图": {"status": "收录", "category": "史部·地理类", "confidence": "中",
                 "note": "需复核具体类属"},
    "九边图论": {"status": "存目", "category": "史部·地理类存目", "confidence": "中高",
                 "note": "明·许论；存世谢少南刻本等"},
    "皇明九边考": {"status": "存目", "category": "存目", "confidence": "中高",
                   "note": "明·魏焕，十卷"},
    "延绥镇志": {"status": "存目", "category": "史部·地理类存目", "confidence": "中高",
                 "note": "明郑汝璧1607/清谭吉璁1673续修，八卷；载成化十年三十六营堡"},
    "河套志": {"status": "存目", "category": "存目（或未收）", "confidence": "中",
               "note": "清·陈履中，六卷，乾隆年间"},
    "嘉靖陕西通志": {"status": "存目", "category": "存目", "confidence": "中",
                     "note": "明·赵廷瑞，40卷；与雍正本区分"},
    "太平寰宇记": {"status": "收录", "category": "史部·地理类·总志之属", "confidence": "高", "note": "宋·乐史"},
    "元和郡县图志": {"status": "收录", "category": "史部·地理类·总志之属", "confidence": "高", "note": "唐·李吉甫"},
    "元丰九域志": {"status": "收录", "category": "史部·地理类·总志之属", "confidence": "高", "note": "宋·王存；有武英殿聚珍本、四库本"},
    "大明一统志": {"status": "收录", "category": "史部·地理类·总志之属", "confidence": "高", "note": "明·李贤等；涉边塞处四库本可能删改"},
    "大清一统志": {"status": "收录", "category": "史部·地理类·总志之属", "confidence": "中", "note": "乾隆四十九年本在四库；道光续修本在四库之后"},
    "甘肃通志": {"status": "收录", "category": "史部·地理类·都会郡县之属", "confidence": "高", "note": "雍正十三年成书，抄入四库"},
    "山西通志": {"status": "收录", "category": "史部·地理类·都会郡县之属", "confidence": "高", "note": "雍正本收录"},
    "关中胜迹图志": {"status": "收录", "category": "史部·地理类", "confidence": "高", "note": "清·毕沅，乾隆四十一年；收录于四库"},
    "华阳国志": {"status": "收录", "category": "史部·载记类", "confidence": "高", "note": "东晋·常璩（西南，非九边）"},
    "九边图说": {"status": "存目", "category": "存目", "confidence": "中", "note": "明·隆庆三年兵部编；九边系列多存目"},
    "边政考": {"status": "存目", "category": "存目", "confidence": "中", "note": "明·张雨，十二卷"},
    "雍大记": {"status": "存目", "category": "存目", "confidence": "中", "note": "明·何景明，嘉靖元年"},
    "皇明经世文编": {"status": "禁毁", "category": "禁毁书目", "confidence": "中高", "note": "明末陈子龙等；涉清廷忌讳，四库不收且列禁毁"},
    "榆林府志": {"status": "未收", "category": "四库之后", "confidence": "高", "note": "清·李熙龄，道光二十一年（1841），晚于四库"},
    "延安府志": {"status": "未收", "category": "四库之后", "confidence": "高", "note": "清·洪蕙，嘉庆七年（1802）重修，晚于四库"},
    "绥德州志": {"status": "未收", "category": "四库之后/未收", "confidence": "中", "note": "清顺治/乾隆四十九年/光绪诸本；州县志四库多不收"},
    "米脂县志": {"status": "未收", "category": "现代", "confidence": "高", "note": "1993年本，与四库无关"},
}

SUPPLEMENT = "《四库全书存目丛书》/《续修四库全书》/《四库禁毁书丛刊》或原刻方志"


def baike_lookup(title):
    url = ("https://baike.baidu.com/api/openapi/BaikeLemmaCardApi"
           "?scope=103&format=json&appid=379020&bk_key="
           + urllib.parse.quote(title) + "&bk_length=600")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        d = json.load(urllib.request.urlopen(req, timeout=15))
        if not d.get("title"):
            return None
        import re
        import html as H
        ab = H.unescape(re.sub(r"<[^>]+>", "", d.get("abstract", "")))
        return {"title": d["title"], "abstract": ab[:300]}
    except Exception:
        return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    use_web = "--web" in sys.argv
    list_only = "--list" in sys.argv

    if list_only:
        for name, v in INDEX.items():
            print(f"  {name}  [{v['status']}] {v['category']}  ({v['confidence']})")
        return

    if not args:
        print(__doc__)
        return

    for title in args:
        v = INDEX.get(title)
        print(f"■ 《{title}》")
        if v:
            status_map = {
                "收录": "收录（正文有全文）",
                "存目": "存目（仅提要，正文无全文）",
                "禁毁": "禁毁（四库不收且列禁毁）",
                "未收": "未收（四库之后/未收）",
            }
            tag = status_map.get(v["status"], v["status"])
            print(f"  → {tag}  |  {v['category']}  |  置信度:{v['confidence']}")
            if v["note"]:
                print(f"    注: {v['note']}")
            if v["status"] == "存目":
                print(f"    ⚠️ 存目：四库正文无全文，补源 → {SUPPLEMENT}")
            elif v["status"] == "禁毁":
                print(f"    ⚠️ 禁毁书：查《四库禁毁书丛刊》")
            elif v["status"] == "未收":
                print(f"    ℹ️ 未收：查《续修四库全书》或原刻方志")
        else:
            print("  → 预置索引未命中（待核）")
            if use_web:
                b = baike_lookup(title)
                if b:
                    print(f"    [百科辅助] {b['title']}: {b['abstract']}")
                else:
                    print("    [百科辅助] 无结果")
            print(f"    ⚠️ 请回《四库全书总目》原书定谳")
        print()


if __name__ == "__main__":
    main()
