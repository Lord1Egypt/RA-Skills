# -*- coding: utf-8 -*-
"""
构建《主角》(陈彦) 人物 → 章节 倒排索引。

输入：TXT_DIR 下的 part0000.html ~ part0151.html（Calibre 导出，part0000 为目录）。
输出：
  data/chapters.json    每个 part 文件 → 部/章标签、字数
  data/characters.json  每个人物 → 规范名 / 别名 / 类别 / 简介 / 出现章节(html+标签)

人物表为人工校准：先用 jieba 词性标注(nr)做发现，再结合 grep 频率/上下文逐一核验，
剔除戏曲角色、历史人物与常用词误判，确认"同一人多名"的别名归属。
重跑：python3 build_index.py   （小说文本更新或人物表调整后执行）
"""
import re, os, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
DATA = os.path.join(SKILL, "data")
# 小说全文：优先环境变量，其次 skill 自带的 txt/（自包含），最后回退原路径
_BUNDLED = os.path.join(SKILL, "txt")
TXT_DIR = (os.environ.get("ZHUJUE_TXT")
           or (_BUNDLED if os.path.isdir(_BUNDLED) else "/home/jjw/zj/txt"))

# ---------------------------------------------------------------- 文本清洗
def clean_html(path):
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"(?is)<head.*?</head>", "", t)
    t = re.sub(r"(?is)<[^>]+>", "", t)
    t = (t.replace("&nbsp;", " ").replace("&amp;", "&")
           .replace("&lt;", "<").replace("&gt;", ">").replace("&#160;", " "))
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()

# ---------------------------------------------------------------- 部/章标签
def chapter_label(idx):
    """part 序号 → (部, 章序中文, 显示标签)。文件名顺序即正文顺序。"""
    cn = "零一二三四五六七八九十"
    def num(n):  # 1..55 → 中文
        if n <= 10: return cn[n]
        if n < 20:  return "十" + (cn[n % 10] if n % 10 else "")
        t = n // 10; r = n % 10
        return cn[t] + "十" + (cn[r] if r else "")
    if idx == 0:   return ("目录", "", "目录")
    if 1   <= idx <= 55:  n = idx;       return ("上部", num(n), f"上部·{num(n)}")
    if 56  <= idx <= 105: n = idx - 55;  return ("中部", num(n), f"中部·{num(n)}")
    if 106 <= idx <= 150: n = idx - 105; return ("下部", num(n), f"下部·{num(n)}")
    if idx == 151: return ("后记", "", "后记")
    return ("?", "", f"part{idx}")

# ================================================================ 人物表
# match: 用于"判定本章是否出现该人物"的子串（已核验：除主角/胡三元外，全名即足够覆盖，
#        短别名不增加章节）。aka: 供用户以任意名字检索的展示别名（含昵称/头衔/简称）。
CHARACTERS = [
 # ---- 主要人物 ----
 dict(id="yiqine", name="忆秦娥", cat="主要人物",
      aka=["易招弟","招弟","易青娥","青娥","秦娥","宁州第一","秦腔皇后","烧火丫头"],
      match=["忆秦娥","易青娥","易招弟","招弟","青娥","秦娥"],
      role="主角。本名易招弟，舅舅改名易青娥，成名后剧作家秦八娃改为忆秦娥。秦腔名伶，戏几乎贯穿全书。"),
 dict(id="husanyuan", name="胡三元", cat="主要人物", aka=["三元","胡老师"],
      match=["胡三元","三元"],
      role="忆秦娥的舅舅，县剧团鼓师，技艺高超而性格张扬，是把她带进剧团的人。"),
 dict(id="hucaixiang", name="胡彩香", cat="主要人物", aka=["彩香"], match=["胡彩香"],
      role="宁州县剧团旦角名角，忆秦娥早期的师傅式人物，与米兰是对手。"),
 dict(id="milan", name="米兰", cat="主要人物", aka=[], match=["米兰"],
      role="宁州县剧团旦角主演，与胡彩香争戏；后调离。"),
 dict(id="liaoyaohui", name="廖耀辉", cat="主要人物", aka=["廖师","廖师傅"], match=["廖耀辉","廖师"],
      role="县剧团灶上师傅，对少年易青娥有性骚扰行为，是她的童年阴影。"),
 dict(id="goucunzhong", name="苟存忠", cat="主要人物", aka=["老苟"], match=["苟存忠"],
      role="存字辈四位老艺人之一（忠）。传授忆秦娥吹火等绝技，《杀生》一折后病逝舞台。"),
 dict(id="gucunxiao", name="古存孝", cat="主要人物", aka=["老古","古老师"], match=["古存孝"],
      role="存字辈老艺人之一（孝），导戏的老把式，长期指点忆秦娥。"),
 dict(id="zhoucunren", name="周存仁", cat="主要人物", aka=["老周"], match=["周存仁"],
      role="存字辈老艺人之一（仁），擅武戏、把子功。"),
 dict(id="qiucunyi", name="裘存义", cat="主要人物", aka=["老裘"], match=["裘存义"],
      role="存字辈老艺人之一（义）。"),
 dict(id="fengxiaoxiao", name="封潇潇", cat="主要人物", aka=["潇潇"], match=["封潇潇"],
      role="县剧团小生演员，忆秦娥的初恋；后逐渐消沉。注意与导演'封子/封导'并非同一人。"),
 dict(id="chujiahe", name="楚嘉禾", cat="主要人物", aka=["嘉禾"], match=["楚嘉禾"],
      role="与忆秦娥同期入团的旦角，貌美而心气高，是贯穿全书的终身竞争对手。"),
 dict(id="liuhongbing", name="刘红兵", cat="主要人物", aka=[], match=["刘红兵"],
      role="地区官员之子，死缠烂打追到忆秦娥成为第一任丈夫，纨绔而痴情，终离婚。"),
 dict(id="qinbawa", name="秦八娃", cat="主要人物", aka=[], match=["秦八娃"],
      role="乡间杂货铺出身的剧作家，为忆秦娥改艺名、量身写《狐仙劫》等戏，是她的精神导师。"),
 dict(id="shihuaiyu", name="石怀玉", cat="主要人物", aka=["怀玉"], match=["石怀玉"],
      role="画家，为忆秦娥痴狂作画，成为她生命后期的伴侣，结局悲剧。"),
 dict(id="songyu", name="宋雨", cat="主要人物", aka=[], match=["宋雨"],
      role="忆秦娥培养、带在身边的后辈（娃娃生/徒弟式人物）。"),
 dict(id="liuyi", name="刘忆", cat="主要人物", aka=[], match=["刘忆"],
      role="忆秦娥与刘红兵之子，智力有障碍，是她沉重的牵挂。"),
 # ---- 次要人物 ----
 dict(id="huangzhengda", name="黄正大", cat="次要人物", aka=["黄主任","黄正"], match=["黄正大"],
      role="宁州县剧团主任/领导，作风官僚，曾整治胡三元；传与米兰有染。"),
 dict(id="zhujiru", name="朱继儒", cat="次要人物", aka=["老朱","朱团"], match=["朱继儒"],
      role="县剧团副主任/领导层，相对正派，后在剧团事务中多有出场。"),
 dict(id="shanyangping", name="单仰平", cat="次要人物", aka=["仰平"], match=["单仰平"],
      role="省秦腔团团长，把忆秦娥调入省团并予以支持。"),
 dict(id="xueguisheng", name="薛桂生", cat="次要人物", aka=["薛团","桂生"], match=["薛桂生"],
      role="省团小生演员，兰花指有名，后来当上团长。"),
 dict(id="fengzi", name="封子", cat="次要人物", aka=["封导"], match=["封子","封导"],
      role="省团导演（'封导'），有夫人，戏路上与忆秦娥多有交集。注意：并非小生封潇潇。"),
 dict(id="dingzhirou", name="丁至柔", cat="次要人物", aka=["丁团"], match=["丁至柔"],
      role="剧团中人，在名分与戏份上与忆秦娥一方有龃龉。"),
 dict(id="zhouyuzhi", name="周玉枝", cat="次要人物", aka=[], match=["周玉枝"],
      role="与忆秦娥、楚嘉禾同期的旦角学员，性子温和。"),
 dict(id="gonglili", name="龚丽丽", cat="次要人物", aka=["丽丽"], match=["龚丽丽"],
      role="与忆秦娥同期的女学员。"),
 dict(id="zhangguangrong", name="张光荣", cat="次要人物", aka=[], match=["张光荣"],
      role="县剧团乐队/演员，胡彩香的丈夫。"),
 dict(id="songguangzu", name="宋光祖", cat="次要人物", aka=["宋师","宋师傅"], match=["宋光祖","宋师"],
      role="县剧团灶上厨师（'宋师'），对易青娥较为照应。"),
 dict(id="yilaidi", name="易来弟", cat="次要人物", aka=["来弟"], match=["易来弟","来弟"],
      role="忆秦娥的姐姐。"),
 dict(id="liusituan", name="刘四团", cat="次要人物", aka=["四团"], match=["刘四团"],
      role="古存孝的年轻助手。"),
 dict(id="huifangling", name="惠芳龄", cat="次要人物", aka=[], match=["惠芳龄"],
      role="比忆秦娥年轻的后辈演员，性子大大咧咧。"),
 dict(id="liqinge", name="李青娥", cat="次要人物", aka=[], match=["李青娥"],
      role="省城名演员（与易青娥同'青娥'，曾有人据此造谣易青娥是其私生女）。注意：与主角易青娥并非同一人。"),
 # ---- 戏曲剧目与角色（忆秦娥所演，便于按角色/剧目检索）----
 dict(id="lihuiniang", name="李慧娘", cat="戏曲角色", aka=["鬼怨","杀生"], match=["李慧娘"],
      role="《游西湖》(含《鬼怨》《杀生》)中角色，忆秦娥的成名戏，吹火绝技所在。"),
 dict(id="baishe", name="白娘子", cat="戏曲角色", aka=["白蛇传","许仙","白素贞"], match=["白娘子","白蛇传"],
      role="《白蛇传》中角色（白娘子/许仙），忆秦娥的代表剧目之一。"),
 dict(id="hujiumei", name="胡九妹", cat="戏曲角色", aka=["狐仙","狐仙劫"], match=["胡九妹","狐仙劫"],
      role="秦八娃为忆秦娥量身创作的《狐仙劫》主角，狐仙九妹。"),
 dict(id="hufenglian", name="胡凤莲", cat="戏曲角色", aka=["游龟山"], match=["胡凤莲","游龟山"],
      role="《游龟山》中角色，忆秦娥早期所演。"),
 dict(id="yangjiajiang", name="杨家将", cat="戏曲角色", aka=["焦赞","孟良","穆桂英","打焦赞"],
      match=["杨家将","焦赞","孟良","穆桂英"],
      role="《杨家将》系列(含《打焦赞》)中角色，忆秦娥武戏剧目。"),
 dict(id="honghu", name="韩英", cat="戏曲角色", aka=["洪湖赤卫队","彭霸天"], match=["韩英","彭霸天"],
      role="《洪湖赤卫队》中角色，现代戏。"),
 dict(id="dujuanshan", name="柯湘", cat="戏曲角色", aka=["杜鹃山","雷刚"], match=["柯湘","杜鹃山"],
      role="《杜鹃山》中角色，现代样板戏。"),
]

# ================================================================ 构建
def main():
    files = sorted(glob.glob(os.path.join(TXT_DIR, "part*.html")))
    if not files:
        raise SystemExit(f"未找到小说文本：{TXT_DIR}/part*.html")

    chapters, texts = {}, {}
    for f in files:
        base = os.path.basename(f)
        idx = int(re.search(r"\d+", base).group())
        bu, zh, label = chapter_label(idx)
        txt = clean_html(f)
        texts[base] = txt
        chapters[base] = dict(idx=idx, part=bu, chap=zh, label=label, chars=len(txt))

    # 人物 → 章节
    out_chars = []
    for c in CHARACTERS:
        hit = []
        for base in sorted(texts):
            if base == "part0000.html":     # 跳过目录页
                continue
            if any(m in texts[base] for m in c["match"]):
                hit.append(base)
        rec = dict(id=c["id"], name=c["name"], cat=c["cat"], aka=c["aka"],
                   role=c["role"], match=c["match"],
                   chapters=[dict(file=b, label=chapters[b]["label"]) for b in hit],
                   chapter_count=len(hit))
        out_chars.append(rec)

    os.makedirs(DATA, exist_ok=True)
    json.dump(chapters, open(os.path.join(DATA, "chapters.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    json.dump(dict(txt_dir=TXT_DIR, characters=out_chars),
              open(os.path.join(DATA, "characters.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # 人类可读名册 references/characters.md（与索引同源，自动生成）
    refs = os.path.join(SKILL, "references")
    os.makedirs(refs, exist_ok=True)
    md = ["# 《主角》(陈彦) 人物名册",
          "",
          f"> 由 `scripts/build_index.py` 自动生成。正文 {len([b for b in chapters if b!='part0000.html'])} 章；"
          "「章数」= 该人物出现的章节数。同一人物多名已归并。",
          ""]
    for cat in ["主要人物", "次要人物", "戏曲角色"]:
        md.append(f"## {cat}\n")
        md.append("| 规范名 | 别名 | 章数 | 简介 |")
        md.append("| --- | --- | --: | --- |")
        for r in sorted([x for x in out_chars if x["cat"] == cat],
                        key=lambda x: -x["chapter_count"]):
            aka = "、".join(r["aka"]) if r["aka"] else "—"
            md.append(f"| {r['name']} | {aka} | {r['chapter_count']} | {r['role']} |")
        md.append("")
    open(os.path.join(refs, "characters.md"), "w", encoding="utf-8").write("\n".join(md))

    print(f"✓ 正文 {len([b for b in chapters if b!='part0000.html'])} 章，人物 {len(out_chars)} 条")
    print(f"✓ data/chapters.json, data/characters.json, references/characters.md 已写入")
    print("\n人物 / 类别 / 出现章节数：")
    for r in sorted(out_chars, key=lambda x: -x["chapter_count"]):
        print(f"  {r['name']:<5} [{r['cat']}] {r['chapter_count']:>3} 章"
              + (f"   别名: {'、'.join(r['aka'])}" if r['aka'] else ""))

if __name__ == "__main__":
    main()
