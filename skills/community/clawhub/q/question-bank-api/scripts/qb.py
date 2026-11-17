#!/usr/bin/env python3
"""Question-bank API client/CLI (stdlib only, no pip install needed).

Auth: X-API-Key header. Base URL + key from env (QB_API_BASE / QB_API_KEY) or
CLI flags (--base / --key). All endpoints are POST JSON.

Subcommands map 1:1 to the vendor API:
  catalog          POST /api/v1/subjectEditionApi
  dict             POST /api/v1/getOtherBasic
  knowledge-tree   POST /api/v1/knowledgeApi
  chapter-tree     POST /api/v1/chapterApi
  chapter-leaves   POST /api/v1/chapterApi + 本地遍历 (列出叶子节点 32 位 oldId)
  by-knowledge     POST /api/v1/getQuestions        (核心：按知识点取题)
  by-chapter       POST /api/v1/getQidByChapterId  (语文/英语按章节取题)
  by-chapter-knowledge POST /api/v1/chapterApi + getQuestions
                  (其他科目按章节取题：遍历叶子 → 取 32 位 oldId → 按知识点取题)
  search           POST /api/v1/search
  answer           POST /api/v1/getAnswer
  papers           POST /api/v1/getPaperList
  paper            POST /api/v1/getPaperQues        (核心：按试卷取题)
  paper-search     POST /api/v1/paperSearch
  report           POST /api/v1/quesErrorReport
  to-word          POST /api/v1/json2word           (返回 docx 二进制流)
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

DEFAULT_BASE = "https://api.xuekubao.com"
# 用户在哪注册账号、申请/购买 API key。发布前若换了域名，改这里即可。
DEFAULT_SIGNUP_URL = "https://api.xuekubao.com"
TAG_RE = re.compile(r"<[^>]+>")
DRY = False  # global dry-run flag, set from --dry-run


def cfg(args):
    base = (getattr(args, "base", None) or os.environ.get("QB_API_BASE") or DEFAULT_BASE).rstrip("/")
    key = getattr(args, "key", None) or os.environ.get("QB_API_KEY") or ""
    timeout = getattr(args, "timeout", None) or int(os.environ.get("QB_TIMEOUT", "30"))
    return base, key, timeout


def post(base, key, timeout, path, payload=None, raw=False, out_path=None, dry_run=False):
    url = base + path
    body = json.dumps(payload or {}).encode("utf-8")
    if dry_run or DRY:
        print(f"[dry-run] POST {url}\n          body={payload}", file=sys.stderr)
        return None
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    if key:
        req.add_header("X-API-Key", key)
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                if raw or out_path:
                    data = r.read()
                    if out_path:
                        with open(out_path, "wb") as f:
                            f.write(data)
                        return {"saved": out_path, "bytes": len(data)}
                    return data
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            txt = e.read().decode("utf-8", "replace")
            if e.code in (429, 500, 503) and attempt < 2:
                time.sleep(2 ** attempt)
                last = f"HTTP {e.code}: {txt}"
                continue
            return {"errorCode": str(e.code), "_raw": txt}
        except Exception as e:  # noqa: BLE001
            if attempt < 2:
                time.sleep(2 ** attempt)
                last = str(e)
                continue
            return {"error": "request_failed", "message": last or str(e)}
    return {"error": "request_failed", "message": last or "retries exhausted"}


def strip_html(s):
    if not s:
        return ""
    return TAG_RE.sub("", s).replace("&nbsp;", " ").strip()


def shorten(s, n=60):
    s = strip_html(s)
    return s[:n] + ("…" if len(s) > n else "")


def fmt_questions(items):
    if not isinstance(items, list) or not items:
        print("(无题目)")
        return
    for i, q in enumerate(items, 1):
        opts = " ".join(o for o in (q.get(f"option_{c}") for c in "abcde") if o)
        meta = " · ".join(filter(None, [
            q.get("qtpye", ""),
            (q.get("subjectName", "") + "/" + q.get("gradeName", "")) if q.get("subjectName") else "",
            q.get("paperName", ""),
            ("难度" + str(q.get("diff"))) if q.get("diff") else "",
        ]))
        print(f"{i}. {meta}")
        print(f"   {shorten(q.get('title') or q.get('timu') or '', 70)}")
        if opts:
            print(f"   选项: {shorten(opts, 90)}")
        if q.get("md52"):
            print(f"   md52: {q['md52']}  | id: {q.get('id','')}")


def maybe_json(args, data):
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    return data


def collect_chapter_leaves(nodes, path=None, out=None):
    """遍历章节树，收集「叶子节点且 oldId 为 32 位」的章节。

    其他科目按章节取题的逻辑：按 科目/年级/版本 取到章节树后，循环遍历到最后一个
    叶子节点，取叶子节点的 oldId（32 位十六进制）作为 knowledgeId，再按知识点取题。
    返回 [{'oldId','name','path','id'}, ...]，path 为从根到该叶子的名称路径。
    """
    if out is None:
        out = []
    for n in nodes or []:
        name = n.get("name", "")
        cur = (path or []) + [name]
        children = n.get("child") or []
        if not children:
            oid = n.get("oldId", "")
            if oid and len(oid) == 32:
                out.append({"oldId": oid, "name": name, "path": " / ".join(cur), "id": n.get("id")})
        else:
            collect_chapter_leaves(children, cur, out)
    return out


def find_node(nodes, target):
    """在章节树中按 id 递归查找节点（用于把范围限定到某个章节子树）。"""
    for n in nodes or []:
        if str(n.get("id")) == str(target):
            return n
        r = find_node(n.get("child") or [], target)
        if r:
            return r
    return None


def build_knowledge_payload(knowledgeId, args, page):
    p = {"knowledgeId": knowledgeId, "page": page or 1}
    for k in ("qtypeId", "paperType", "diff", "gradeId", "year"):
        v = getattr(args, k, None)
        if v is not None:
            p[k] = v
    return p


def cmd_catalog(args, c):
    d = post(*c, "/api/v1/subjectEditionApi", {})
    if d is None:
        return
    if args.json:
        maybe_json(args, d)
    else:
        tree = d.get("data", d) if isinstance(d, dict) else d
        print(f"学段/年级/学科/版本树（顶层 {len(tree) if isinstance(tree, list) else '?'} 项）。"
              "用 --json 看完整结构；取 code 作为 pharseId/subjectId/gradeId/editionId。")


def cmd_dict(args, c):
    d = post(*c, "/api/v1/getOtherBasic", {})
    if d is None:
        return
    if args.json:
        maybe_json(args, d)
        return
    for key, label in (("qtypes", "题型"), ("paperTypes", "试卷类型"), ("diffTypes", "难易度")):
        items = d.get(key, [])
        print(f"{label}（{len(items)}）:")
        for it in items[:30]:
            print(f"  {it.get('id')}: {it.get('typeName', it.get('name',''))}")


def cmd_knowledge_tree(args, c):
    p = {"pharseId": args.pharseId}
    if args.subjectId:
        p["subjectId"] = args.subjectId
    d = post(*c, "/api/v1/knowledgeApi", p)
    if d is None:
        return
    if args.json:
        maybe_json(args, d)
    else:
        print("知识点树已返回。遍历到第三级，取 oldId 作为 by-knowledge 的 --knowledgeId。"
              "用 --json 查看完整树。")


def cmd_chapter_tree(args, c):
    p = {"pharseId": args.pharseId}
    for k in ("subjectId", "editionId", "gradeId"):
        v = getattr(args, k)
        if v:
            p[k] = v
    d = post(*c, "/api/v1/chapterApi", p)
    if d is None:
        return
    if args.json:
        maybe_json(args, d)
    else:
        print("章节树已返回。取目标章节的 id 作为 by-chapter 的 --chapterId。用 --json 查看完整树。")


def cmd_by_knowledge(args, c):
    p = {"knowledgeId": args.knowledgeId, "page": args.page or 1}
    for k in ("qtypeId", "paperType", "diff", "gradeId", "year"):
        v = getattr(args, k)
        if v:
            p[k] = v
    d = post(*c, "/api/v1/getQuestions", p)
    if d is None:
        return
    if args.json:
        maybe_json(args, d)
    else:
        fmt_questions(d.get("data", []))
        print(f"\n本页 {len(d.get('data', []))} 题，总计 {d.get('dataCount', '?')} 题；"
              "翻页加 --page。需要答案用 answer --md52 <md52>。")


def cmd_by_chapter(args, c):
    p = {"chapterId": args.chapterId, "page": args.page or 1}
    for k in ("qtypeId", "paperType", "diff", "year"):
        v = getattr(args, k)
        if v:
            p[k] = v
    d = post(*c, "/api/v1/getQidByChapterId", p)
    if d is None:
        return
    if args.json:
        maybe_json(args, d)
    else:
        fmt_questions(d.get("data", []))
        print(f"\n本页 {len(d.get('data', []))} 题；翻页加 --page。需要答案用 answer --md52 <md52>。")


def cmd_chapter_leaves(args, c):
    p = {"pharseId": args.pharseId}
    for k in ("subjectId", "editionId", "gradeId"):
        v = getattr(args, k)
        if v:
            p[k] = v
    tree = post(*c, "/api/v1/chapterApi", p)
    if tree is None:
        return
    if args.json:
        maybe_json(args, tree)
        return
    nodes = tree.get("data", []) if isinstance(tree, dict) else tree
    leaves = collect_chapter_leaves(nodes)
    if not leaves:
        print("(未找到带 32 位 oldId 的叶子章节)")
        return
    print(f"叶子章节（共 {len(leaves)} 个；oldId 可作 by-knowledge / by-chapter-knowledge 的 knowledgeId）：")
    for i, lf in enumerate(leaves, 1):
        print(f"{i}. {lf['path']}  oldId={lf['oldId']}")


def cmd_by_chapter_knowledge(args, c):
    p = {"pharseId": args.pharseId}
    for k in ("subjectId", "editionId", "gradeId"):
        v = getattr(args, k)
        if v:
            p[k] = v
    tree = post(*c, "/api/v1/chapterApi", p)
    if tree is None:
        return
    nodes = tree.get("data", []) if isinstance(tree, dict) else tree
    if getattr(args, "chapterId", None):
        node = find_node(nodes, args.chapterId)
        if not node:
            print(f"[error] 未找到 chapterId={args.chapterId}", file=sys.stderr)
            sys.exit(2)
        roots = [node]
    else:
        roots = nodes
    leaves = collect_chapter_leaves(roots)
    if not leaves:
        print("(该章节范围内未找到带 32 位 oldId 的叶子节点)")
        return
    max_leaves = args.max_leaves or 0
    if max_leaves and len(leaves) > max_leaves:
        print(f"[info] 共 {len(leaves)} 个叶子章节，受 --max-leaves {max_leaves} 限制，仅取前 {max_leaves} 个。")
        leaves = leaves[:max_leaves]
    if args.json:
        maybe_json(args, {"leaves": leaves})
        return
    all_items = []
    total_cap = args.limit or 0
    for lf in leaves:
        if total_cap and len(all_items) >= total_cap:
            break
        d = post(*c, "/api/v1/getQuestions", build_knowledge_payload(lf["oldId"], args, args.page or 1))
        if d is None:
            continue
        items = d.get("data", []) if isinstance(d, dict) else []
        budget = (total_cap - len(all_items)) if total_cap else len(items)
        items = items[:budget]
        print(f"\n=== 章节: {lf['path']}  (oldId={lf['oldId']}, {len(items)} 题) ===")
        fmt_questions(items)
        all_items.extend(items)
    print(f"\n共取 {len(all_items)} 题，来自 {len(leaves)} 个叶子章节。需要答案用 answer --md52 <md52>。")


def cmd_search(args, c):
    p = {"keyword": args.keyword, "gradeId": args.gradeId}
    if args.subjectId:
        p["subjectId"] = args.subjectId
    d = post(*c, "/api/v1/search", p)
    if d is None:
        return
    if args.json:
        maybe_json(args, d)
    else:
        fmt_questions(d.get("data", []))


def cmd_answer(args, c):
    d = post(*c, "/api/v1/getAnswer", {"qid": args.md52})
    if d is None:
        return
    if args.json:
        maybe_json(args, d)
        return
    items = d.get("data", d) if isinstance(d, dict) else d
    if not isinstance(items, list):
        items = [items]
    for i, q in enumerate(items, 1):
        print(f"{i}. {q.get('qtpye','')}  md52={q.get('md52','')}")
        print(f"   题干: {shorten(q.get('title',''), 80)}")
        print(f"   答案: {q.get('answer1','') or q.get('answer2','')}")
        if q.get("parse"):
            print(f"   解析: {shorten(q.get('parse'), 120)}")
        for ch in q.get("children", []):
            print(f"   - {shorten(ch.get('title',''),60)} 答案={ch.get('answer1', ch.get('answer2',''))}")


def cmd_papers(args, c):
    p = {"gradeId": args.gradeId}
    for k in ("subjectId", "paperTypeId", "term", "areaId"):
        v = getattr(args, k)
        if v:
            p[k] = v
    d = post(*c, "/api/v1/getPaperList", p)
    if d is None:
        return
    if args.json:
        maybe_json(args, d)
        return
    items = d.get("data", [])
    print(f"试卷列表（{len(items)} 条，总计 {d.get('dataCount','?')}）：")
    for i, it in enumerate(items, 1):
        print(f"{i}. [{it.get('id')}] {it.get('paperName','')}  "
              f"({it.get('subjectName','')}/{it.get('gradeName','')}/{it.get('paperType','')}/{it.get('year','')})")


def cmd_paper(args, c):
    d = post(*c, "/api/v1/getPaperQues", {"paperId": args.paperId})
    if d is None:
        return
    if args.json:
        maybe_json(args, d)
    else:
        fmt_questions(d.get("data", []))


def cmd_paper_search(args, c):
    d = post(*c, "/api/v1/paperSearch", {"keyword": args.keyword})
    if d is None:
        return
    if args.json:
        maybe_json(args, d)
        return
    items = d.get("data", [])
    print(f"试卷搜索（{d.get('dataCount', len(items))} 条）：")
    for i, it in enumerate(items, 1):
        print(f"{i}. [{it.get('id')}] {it.get('paperName','')}  "
              f"({it.get('subjectName','')}/{it.get('gradeName','')}/{it.get('paperType','')}/{it.get('year','')})")


def cmd_report(args, c):
    p = {"qid": args.qid}
    if args.content:
        p["content"] = args.content
    d = post(*c, "/api/v1/quesErrorReport", p)
    if d is None:
        return
    maybe_json(args, d) if args.json else print(f"提交结果: {d}")


def cmd_to_word(args, c):
    try:
        payload = json.loads(args.data)
    except Exception as e:  # noqa: BLE001
        print(f"[error] --data 不是合法 JSON: {e}", file=sys.stderr)
        sys.exit(2)
    out = args.out or "paper.docx"
    d = post(*c, "/api/v1/json2word", payload, raw=True, out_path=out)
    if d is None:
        return
    if isinstance(d, dict) and d.get("saved"):
        print(f"已保存 Word 文档: {out} ({d['bytes']} bytes)")
    else:
        print(f"[warn] 响应非预期: {d}")


def build_parser():
    ap = argparse.ArgumentParser(description="题库 API 客户端")
    sub = ap.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--base")
    common.add_argument("--key")
    common.add_argument("--timeout", type=int)
    common.add_argument("--json", action="store_true", help="输出原始 JSON")
    common.add_argument("--dry-run", action="store_true", help="仅打印请求，不真正调用")

    sub.add_parser("catalog", parents=[common], help="学段/年级/学科/版本树").set_defaults(fn=cmd_catalog)
    sub.add_parser("dict", parents=[common], help="题型/试卷类型/难易度字典").set_defaults(fn=cmd_dict)

    kt = sub.add_parser("knowledge-tree", parents=[common], help="知识点树")
    kt.add_argument("--pharseId", required=True)
    kt.add_argument("--subjectId")
    kt.set_defaults(fn=cmd_knowledge_tree)

    ct = sub.add_parser("chapter-tree", parents=[common], help="章节树")
    ct.add_argument("--pharseId", required=True)
    ct.add_argument("--subjectId")
    ct.add_argument("--editionId")
    ct.add_argument("--gradeId")
    ct.set_defaults(fn=cmd_chapter_tree)

    bk = sub.add_parser("by-knowledge", parents=[common], help="按知识点取题")
    bk.add_argument("--knowledgeId", required=True)
    bk.add_argument("--qtypeId")
    bk.add_argument("--paperType")
    bk.add_argument("--diff")
    bk.add_argument("--gradeId")
    bk.add_argument("--year")
    bk.add_argument("--page", type=int)
    bk.set_defaults(fn=cmd_by_knowledge)

    bc = sub.add_parser("by-chapter", parents=[common], help="语文/英语按章节取题")
    bc.add_argument("--chapterId", required=True)
    bc.add_argument("--qtypeId")
    bc.add_argument("--paperType")
    bc.add_argument("--diff")
    bc.add_argument("--year")
    bc.add_argument("--page", type=int)
    bc.set_defaults(fn=cmd_by_chapter)

    cl = sub.add_parser("chapter-leaves", parents=[common],
                        help="列出章节树的叶子节点 32 位 oldId（供按章节取题用）")
    cl.add_argument("--pharseId", required=True)
    cl.add_argument("--subjectId")
    cl.add_argument("--editionId")
    cl.add_argument("--gradeId")
    cl.set_defaults(fn=cmd_chapter_leaves)

    bck = sub.add_parser("by-chapter-knowledge", parents=[common],
                         help="其他科目按章节取题：遍历叶子→取32位oldId→按知识点取题")
    bck.add_argument("--pharseId", required=True)
    bck.add_argument("--subjectId")
    bck.add_argument("--editionId")
    bck.add_argument("--gradeId")
    bck.add_argument("--chapterId", help="可选：把范围限定到某个章节子树")
    bck.add_argument("--qtypeId")
    bck.add_argument("--paperType")
    bck.add_argument("--diff")
    bck.add_argument("--year")
    bck.add_argument("--page", type=int)
    bck.add_argument("--max-leaves", type=int, default=20,
                     help="最多查询的叶子章节数，防止一次消耗过多额度（默认 20）")
    bck.add_argument("--limit", type=int, help="最多返回的试题总数")
    bck.set_defaults(fn=cmd_by_chapter_knowledge)

    se = sub.add_parser("search", parents=[common], help="全文检索试题")
    se.add_argument("--keyword", required=True)
    se.add_argument("--gradeId", required=True)
    se.add_argument("--subjectId")
    se.set_defaults(fn=cmd_search)

    an = sub.add_parser("answer", parents=[common], help="按 md52 取答案")
    an.add_argument("--md52", required=True)
    an.set_defaults(fn=cmd_answer)

    pp = sub.add_parser("papers", parents=[common], help="试卷列表")
    pp.add_argument("--gradeId", required=True)
    pp.add_argument("--subjectId")
    pp.add_argument("--paperTypeId")
    pp.add_argument("--term")
    pp.add_argument("--areaId")
    pp.set_defaults(fn=cmd_papers)

    pq = sub.add_parser("paper", parents=[common], help="试卷详情（含全部试题）")
    pq.add_argument("--paperId", required=True)
    pq.set_defaults(fn=cmd_paper)

    ps = sub.add_parser("paper-search", parents=[common], help="试卷搜索")
    ps.add_argument("--keyword", required=True)
    ps.set_defaults(fn=cmd_paper_search)

    rp = sub.add_parser("report", parents=[common], help="提交试题报错")
    rp.add_argument("--qid", required=True)
    rp.add_argument("--content")
    rp.set_defaults(fn=cmd_report)

    tw = sub.add_parser("to-word", parents=[common], help="结构化题目 → docx")
    tw.add_argument("--data", required=True, help="paperData JSON 字符串")
    tw.add_argument("--out", help="输出文件路径，默认 paper.docx")
    tw.set_defaults(fn=cmd_to_word)
    return ap


def main():
    global DRY
    args = build_parser().parse_args()
    DRY = args.dry_run
    c = cfg(args)
    if not c[1] and not args.dry_run:
        print(
            "[warn] 未配置 API key。请先到学库宝注册并申请访问 key：\n"
            f"        {DEFAULT_SIGNUP_URL}  →  注册账号 → API 管理 → 申请访问 key\n"
            "        购买 ¥9.9 测试套餐即可试用；有疑问联系微信客服：569212182\n"
            "        拿到 key 后设为 QB_API_KEY 环境变量，或每次调用加 --key <你的key>。",
            file=sys.stderr)
    args.fn(args, c)


if __name__ == "__main__":
    main()
