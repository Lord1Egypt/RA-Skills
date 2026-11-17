# -*- coding: utf-8 -*-
"""rule_extractor：零依赖规则抽取层（散文 → EventNode）。

定位：白盒验收基线与降级兜底，不是生产级抽取。生产路径应为 llm_extractor。
本模块的存在价值：
  1) 全链路可复现——无 API key 也能跑通「抽取→校验→回原文核验」闭环；
  2) 每条产出可回原文——source 带章号与原文摘录；
  3) 词表可换——extraction/lexicons/*.json 决定识别哪些角色/地点/时间标记，
     架构与语料解耦（当前默认档案：红楼梦）。

判定原则（宁缺毋滥；以下规则全部来自白盒验收中回原文核验过的假阳性类）：
  - 只认词表内角色名（含别称），不猜人名；词表未收的角色整条不抽；
  - 引语按贪心配对保护切句；章内引语不配平（红楼梦语料 14/120 章）时
    未配对的引号按字面处理，不污染其余文本的切句；
  - 死亡标记只在**非引语叙事段**生效——口语「不如死了干淨」是反讽不是死亡；
  - 死亡归属四类确定性排除：
      代词主语（「他死了問誰」指代不明）、
      推测/误判（「邢夫人打量鳳姐死了」）、
      假设语气（「再真把寶玉死了」）、
      修辞与第三方（「哭得淚干氣絕」「雨村嫡配…下世」）；
  - state=生 只由**新发生的言语行为**证明（NAME+言语动词），
    回忆性叙述（「可卿在時」）不构成生存证据；
  - 地点就近归属：地点标记归给相距最近的角色提及，避免
    「自賈璉送黛玉往揚州去後」中的揚州被错归给同句的鳳姐；
  - 诗歌行（詩曰/正是：/有詩為證…）整句跳过——「三月雨」不是时间标记；
  - 坐标缺失的字段留空，由校验器按「空坐标不参与」处理，不臆造。
"""
import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

try:
    from .schema import EventNode
except ImportError:  # 允许独立运行调试
    from schema import EventNode  # type: ignore

_HERE = os.path.dirname(os.path.abspath(__file__))
LEXICON_DIR = os.path.join(_HERE, "lexicons")
DEFAULT_LEXICON = "example"

# 诗歌行标记：整句跳过（诗句中的数字/地名不是叙事坐标）
_VERSE_MARKERS = ("詩曰", "詞曰", "正是：", "有詩為證", "後人有詩", "詩云",
                  "偶成", "題曰", "只見題", "吟罷", "滿紙", "後人來詩",
                  "又詩曰", "口佔", "口占")
_SENT_END = "。！？；\n"
_QUOTE_OPEN, _QUOTE_CLOSE = "「", "」"
_BOM = "\ufeff"

# 言语行为判定：NAME + 0-2个副词性停顿 + 言语动词，动词前一字须不在阻塞表
# （排除「知道/通道/味道/學問/顧問」等非言语组合）
_SPEECH_ADV = "忙便又方遂即就也卻才連忙向還當自只"
_VERB_BLOCK_PREV = "知通覺味孝神話詢顧學訪議論"
_VERB_CHARS = "道問答說笑罵哭歎叫嚷喚斥"

# 死亡标记归属窗口：标记须出现在角色提及后 N 字内，否则视为无关
# （「這事便死了」中的「死了」是比喻，距最近角色提及十余字）
_DEATH_WINDOW = 8
# 死亡标记前的代词主语：「他死了問誰」指代不明，不归属任何词表角色
_PRONOUN_PRE = "他她其渠"
# 提及之前（6 字内）的推测/误判动词：「邢夫人打量鳳姐死了」是错判不是死亡
_SUPPOSED_PRE = ("以為", "只當", "打量", "想是", "想道", "只說", "料道",
                 "怕是", "疑心", "聽見", "聞得", "忽聽", "看見", "忽見",
                 "一見", "只見", "聽說")
# 提及之前（6 字内）的假设语气：「再真把寶玉死了」是假设不是事实
_HYPO_PRE = ("若", "倘若", "若是", "要是", "假如", "倘或", "只怕", "或者",
             "真把", "倘把", "若把", "直把")
# 标记与提及之间的修辞前缀：「哭得淚干氣絕」是修辞不是死亡
_FIGURATIVE_IN = ("哭", "淚", "笑", "嚇")
# 标记与提及之间的第三方主语描述：「雨村嫡配…下世」死的是嫡配不是雨村
_THIRDPARTY_IN = ("嫡配", "元配", "繼室", "嫡妻", "妻", "妾", "夫人", "奶奶",
                  "媳婦", "孫媳", "丫鬟", "僕", "母", "父", "兒", "女")
# 地点就近归属的最大距离
_PLACE_WINDOW = 30


def load_lexicon(name_or_path: str = DEFAULT_LEXICON) -> Dict[str, Any]:
    """载入词表：传档案名（不带路径/后缀）或完整 JSON 路径。"""
    if os.sep in name_or_path or name_or_path.endswith(".json"):
        path = name_or_path
    else:
        path = os.path.join(LEXICON_DIR, name_or_path + ".json")
    if not os.path.exists(path):
        raise FileNotFoundError(
            "词表不存在：%s（模板自带 example.json，实际档案请复制后替换内容）" % path)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_name_regex(lex: Dict[str, Any]) -> Tuple["re.Pattern", Dict[str, str]]:
    """角色名/别称 → 规范名的匹配正则。长名优先，避免「寶玉」截断「寶二爺」。"""
    alias2canon: Dict[str, str] = {}
    for canon, aliases in lex["characters"].items():
        alias2canon[canon] = canon
        for a in aliases or []:
            alias2canon[a] = canon
    names = sorted(alias2canon, key=len, reverse=True)
    if not names:
        raise ValueError("词表无角色名")
    return re.compile("|".join(re.escape(n) for n in names)), alias2canon


def build_marker_regex(markers: List[str], guard_prev: str = "") -> "re.Pattern":
    """词表标记匹配正则。guard_prev：前置阻塞字（防「十一月」误配「一月」）。"""
    ms = sorted(set(m for m in markers if m), key=len, reverse=True)
    if not ms:
        return re.compile(r"(?!x)x")  # 永不匹配
    lookbehind = "(?<![%s])" % guard_prev if guard_prev else ""
    return re.compile(lookbehind + "(?:%s)" % "|".join(re.escape(m) for m in ms))


def strip_quotes(text: str) -> str:
    """去掉「」引语段，只留叙事部分（说话人标签在引语外，不受影响）。"""
    return re.sub(_QUOTE_OPEN + r"[^" + _QUOTE_CLOSE + r"]*" + _QUOTE_CLOSE, "", text)


def _protected_mask(text: str) -> List[bool]:
    """引语区间掩码：贪心配对「」；未配对的引号按字面（容忍不配平语料）。"""
    mask = [False] * len(text)
    stack: List[int] = []
    for i, ch in enumerate(text):
        if ch == _QUOTE_OPEN:
            stack.append(i)
        elif ch == _QUOTE_CLOSE and stack:
            a = stack.pop()
            for j in range(a, i + 1):
                mask[j] = True
    return mask


def split_sentences(text: str) -> List[str]:
    """按句末标点切句，引语内部不切。

    古典小说的一段长篇对话常跨多个句号；在引语内切断会使引语剥离失效，
    引语内的「不如死了干淨」会被当成叙事死亡标记（白盒验收实测假阳性）。
    """
    mask = _protected_mask(text)
    sents: List[str] = []
    buf: List[str] = []
    for i, ch in enumerate(text):
        buf.append(ch)
        if ch in _SENT_END and not mask[i]:
            s = "".join(buf).strip()
            if s:
                sents.append(s)
            buf = []
    s = "".join(buf).strip()
    if s:
        sents.append(s)
    return sents


def _find_mentions(narrative: str, name_re) -> List[Tuple[int, str]]:
    """叙事段中的角色提及（按出现顺序）。"""
    return [(m.start(), m.group(0)) for m in name_re.finditer(narrative)]


def _speech_after(narrative: str, pos: int, name_len: int) -> bool:
    """提及位置之后是否紧跟言语动词（0-2 个副词间隔）。"""
    tail = narrative[pos + name_len: pos + name_len + 3]
    for i in range(0, min(2, len(tail)) + 1):
        if i >= len(tail):
            break
        v = tail[i]
        if v in _VERB_CHARS:
            prev = tail[i - 1] if i > 0 else ""
            if prev and prev in _VERB_BLOCK_PREV:
                continue
            return True
        if v not in _SPEECH_ADV:
            break
    return False


def _death_attribution(narrative: str, mentions: List[Tuple[int, str]],
                       death_hit, legal_re=None) -> Optional[Tuple[int, str]]:
    """死亡标记 → 角色提及。四类确定性排除，无法可靠归属返回 None。"""
    if not death_hit:
        return None
    # 0) 法律文书语境：判决/案卷中的死亡记述的是案情当事人，不是叙事死亡
    #    （薛蟠擬絞監候一案中「張三身死」不应归属同在句中的薛蟠）
    if legal_re is not None and legal_re.search(narrative):
        return None
    dpos = death_hit.start()
    # 1) 代词主语：「他死了問誰」指代不明
    pre = narrative[max(0, dpos - 2):dpos]
    if any(p in pre for p in _PRONOUN_PRE):
        return None
    best: Optional[Tuple[int, str]] = None
    for pos, name in mentions:
        if pos <= dpos and dpos - pos <= _DEATH_WINDOW:
            best = (pos, name)
    if best is None:
        return None
    pos, name = best
    # 2) 推测/误判与 3) 假设语气：提及之前 6 字内的语气/感知动词
    before = narrative[max(0, pos - 6):pos]
    if any(w in before for w in _SUPPOSED_PRE + _HYPO_PRE):
        return None
    # 4) 修辞与第三方主语：提及与标记之间的描述词
    window = narrative[pos + len(name):dpos]
    if any(w in window for w in _FIGURATIVE_IN + _THIRDPARTY_IN):
        return None
    return best


def _place_owners(narrative: str, mentions: List[Tuple[int, str]],
                  place_re) -> Dict[int, str]:
    """地点就近归属：每个地点标记归给相距最近的角色提及（≤30 字）。"""
    owners: Dict[int, str] = {}
    for pm in place_re.finditer(narrative):
        ppos = pm.start()
        best_idx, best_d = None, None
        for idx, (pos, _name) in enumerate(mentions):
            d = abs(pos - ppos)
            if best_d is None or d < best_d:
                best_idx, best_d = idx, d
        if best_idx is not None and best_d is not None and best_d <= _PLACE_WINDOW:
            owners.setdefault(best_idx, pm.group(0))
    return owners


def extract_nodes(chapter_text: str, chapter_no: int,
                  lex: Optional[Dict[str, Any]] = None) -> List[EventNode]:
    """从单章文本抽取 EventNode 列表（按行文顺序产出）。"""
    lex = lex or load_lexicon()
    name_re, alias2canon = build_name_regex(lex)
    place_re = build_marker_regex(lex.get("places", []))
    time_re = build_marker_regex(lex.get("time_markers", []),
                                 guard_prev="一二三四五六七八九十百")
    death_re = build_marker_regex(lex.get("death_markers", []))
    legal_re = build_marker_regex(lex.get("legal_context_markers", []))

    body = chapter_text.lstrip(_BOM).strip()
    nodes: List[EventNode] = []
    for sent in split_sentences(body):
        if any(mk in sent for mk in _VERSE_MARKERS):
            continue  # 诗歌行：无叙事坐标
        narrative = strip_quotes(sent)
        if not narrative:
            continue
        mentions = _find_mentions(narrative, name_re)
        if not mentions:
            continue
        # 章内时间标记：取叙事段中首个命中（确定性；缺则不赋值）
        tm = time_re.search(narrative)
        time_mark = tm.group(0) if tm else ""
        owners = _place_owners(narrative, mentions, place_re)
        death_hit = death_re.search(narrative)
        attribution = _death_attribution(narrative, mentions, death_hit, legal_re)
        for idx, (pos, name) in enumerate(mentions):
            seg_end = mentions[idx + 1][0] if idx + 1 < len(mentions) else len(narrative)
            action = narrative[pos:seg_end].strip(" ，。！？；：、")
            if not action:
                continue  # 无动作不构成事件
            state = ""
            if attribution and name == attribution[1] and pos == attribution[0]:
                state = "死"
            elif _speech_after(narrative, pos, len(name)):
                state = "生"  # 新发生的言语行为=生存证据（鬼魂显灵会误触，复核排除）
            nodes.append(EventNode(
                character=alias2canon.get(name, name),
                action=action[:80],
                time=time_mark,
                place=owners.get(idx, ""),
                state=state,
                source="第%03d回|%s" % (chapter_no, sent[:60]),
            ))
    return nodes


def extract_corpus(corpus_dir: str, lex: Optional[Dict[str, Any]] = None,
                   limit: int = 0) -> List[EventNode]:
    """按文件名顺序抽取整库（001..120），保证节点顺序=行文顺序。"""
    import glob
    lex = lex or load_lexicon()
    files = sorted(glob.glob(os.path.join(corpus_dir, "*.txt")))
    if limit:
        files = files[:limit]
    nodes: List[EventNode] = []
    for fp in files:
        m = re.match(r"(\d+)", os.path.basename(fp))
        if not m:
            continue
        with open(fp, encoding="utf-8") as f:
            nodes.extend(extract_nodes(f.read(), int(m.group(1)), lex))
    return nodes


def coverage_stats(nodes: List[EventNode]) -> Dict[str, Any]:
    """坐标覆盖率统计（白盒验收的输入质量指标）。"""
    n = len(nodes)
    if not n:
        return {"nodes": 0}
    return {
        "nodes": n,
        "characters": len({x.character for x in nodes}),
        "time": round(sum(1 for x in nodes if x.time) / n, 3),
        "place": round(sum(1 for x in nodes if x.place) / n, 3),
        "state": round(sum(1 for x in nodes if x.state) / n, 3),
        "state_dead": sum(1 for x in nodes if x.state == "死"),
        "state_alive": sum(1 for x in nodes if x.state == "生"),
        "full_coords": round(sum(1 for x in nodes if x.time and x.place) / n, 3),
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法：python extraction/rule_extractor.py <章节目录> [词表名或 json 路径]")
        print("示例：python extraction/rule_extractor.py ./corpus/示例 [example]")
        raise SystemExit(1)
    d = sys.argv[1]
    lex = load_lexicon(sys.argv[2]) if len(sys.argv) > 2 else None
    ns = extract_corpus(d, lex=lex)
    print(json.dumps(coverage_stats(ns), ensure_ascii=False, indent=1))
