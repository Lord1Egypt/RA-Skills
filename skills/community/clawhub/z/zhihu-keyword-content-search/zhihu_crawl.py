"""
知乎关键词问答爬虫
用法:
  python zhihu_crawl.py --cookie "你的Cookie" --keywords "关键词1" "关键词2" --top 100 --output ./output

依赖: pip install requests
"""
import argparse, requests, json, time, os, re
from urllib.parse import quote

TAG_RE = re.compile(r'<[^>]+>')

def strip_tags(s): return TAG_RE.sub('', s or '')

def html_to_text(html):
    text = TAG_RE.sub('', html or '')
    for o, n in [('&nbsp;',' '),('&amp;','&'),('&lt;','<'),('&gt;','>'),('&quot;','"'),('&#39;',"'")]:
        text = text.replace(o, n)
    return re.sub(r'\n{3,}', '\n\n', text).strip()

def get_json(url, params=None, headers=None, retry=3):
    for i in range(retry):
        try:
            r = requests.get(url, headers=headers, params=params, timeout=15)
            if r.status_code == 200: return r.json()
            print(f"  [HTTP {r.status_code}]", flush=True)
        except Exception as e:
            print(f"  [ERROR] {e}", flush=True)
        time.sleep(2 + i)
    return None

def make_headers(cookie, kw=""):
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Cookie": cookie,
        "Referer": "https://www.zhihu.com/search?type=question&q=" + quote(kw),
        "x-requested-with": "fetch",
    }

def search_keyword(keyword, cookie, all_kws, search_max):
    collected, offset = {}, 0
    headers = make_headers(cookie, keyword)
    while len(collected) < search_max:
        data = get_json("https://www.zhihu.com/api/v4/search_v3",
            params={"t":"question","q":keyword,"correction":1,"offset":offset,
                    "limit":20,"lc_idx":offset,"show_all_topics":0},
            headers=headers)
        if not data: break
        items = data.get("data") or []
        for item in items:
            obj = item.get("object", {})
            if obj.get("type") != "question": continue
            title = strip_tags(obj.get("title",""))
            matched = [kw for kw in all_kws if kw in title]
            if not matched: continue
            qid = str(obj.get("id",""))
            if not qid or qid in collected: continue
            collected[qid] = {
                "id": qid, "title": title,
                "answer_count": obj.get("answer_count", 0),
                "follower_count": obj.get("follower_count", 0),
                "url": f"https://www.zhihu.com/question/{qid}",
                "matched_kw": matched,
            }
        if data.get("paging",{}).get("is_end",True) or not items: break
        offset += 20
        time.sleep(0.8)
    return collected

def fetch_all_answers(qid, cookie, kw=""):
    answers, offset = [], 0
    headers = make_headers(cookie, kw)
    while True:
        data = get_json(
            f"https://www.zhihu.com/api/v4/questions/{qid}/answers"
            f"?include=content,excerpt,voteup_count,comment_count,author"
            f"&limit=20&offset={offset}&sort_by=default",
            headers=headers)
        if not data: break
        batch = data.get("data") or []
        for ans in batch:
            au = ans.get("author", {})
            answers.append({
                "author": au.get("name","匿名"),
                "author_url": f"https://www.zhihu.com/people/{au.get('url_token','')}",
                "voteup_count": ans.get("voteup_count", 0),
                "comment_count": ans.get("comment_count", 0),
                "content": ans.get("content",""),
                "excerpt": ans.get("excerpt",""),
            })
        if data.get("paging",{}).get("is_end",True) or not batch: break
        offset += 20
        time.sleep(0.8)
    return answers

def main():
    p = argparse.ArgumentParser(description="知乎关键词问答爬虫")
    p.add_argument("--cookie",      required=True,  help="知乎登录Cookie")
    p.add_argument("--keywords",    nargs="+",       default=["MyGO","Ave Mujica","丰川祥子"],
                   help="搜索关键词列表")
    p.add_argument("--top",         type=int,        default=100,
                   help="取回答数最多的前N个问题（默认100）")
    p.add_argument("--output",      default="zhihu_output",
                   help="输出目录（默认 zhihu_output）")
    p.add_argument("--search-max",  type=int,        default=200,
                   help="每个关键词最多搜索多少候选（默认200）")
    args = p.parse_args()

    os.makedirs(args.output, exist_ok=True)
    print(f"{'='*60}\n知乎爬虫  关键词: {args.keywords}  TOP {args.top}\n{'='*60}", flush=True)

    # 第一步：搜索
    print("\n【第一步】搜索候选问题...", flush=True)
    all_q = {}
    for kw in args.keywords:
        print(f"  搜索「{kw}」...", flush=True)
        found = search_keyword(kw, args.cookie, args.keywords, args.search_max)
        new = sum(1 for qid in found if qid not in all_q)
        all_q.update(found)
        print(f"  -> 本词 {len(found)} 条，新增 {new}，累计 {len(all_q)}", flush=True)
        time.sleep(1)

    if not all_q:
        print("未找到任何问题，请检查 Cookie 是否有效", flush=True)
        return

    ranked = sorted(all_q.values(), key=lambda x: x["answer_count"], reverse=True)
    top = ranked[:args.top]
    print(f"\n共 {len(all_q)} 个候选，取 TOP {len(top)}"
          f"（{top[0]['answer_count']} ~ {top[-1]['answer_count']} 条回答）", flush=True)
    with open(os.path.join(args.output, "_question_list.json"), "w", encoding="utf-8") as f:
        json.dump(top, f, ensure_ascii=False, indent=2)

    # 第二步：爬回答
    print(f"\n【第二步】爬取 {len(top)} 个问题的全部回答...", flush=True)
    all_results = []
    for i, q in enumerate(top, 1):
        kws = "/".join(q["matched_kw"])
        print(f"\n[{i}/{len(top)}] [{kws}] {q['title'][:55]}", flush=True)
        print(f"  API回答数={q['answer_count']}，抓取中...", flush=True)
        answers = fetch_all_answers(q["id"], args.cookie, q["matched_kw"][0])
        result = {**q, "fetched_count": len(answers), "answers": answers}
        fp = os.path.join(args.output, f"question_{q['id']}.json")
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"  [OK] {len(answers)} 条 -> {fp}", flush=True)
        all_results.append(result)
        time.sleep(2)

    # 第三步：合并纯文本
    print("\n【第三步】合并为纯文本...", flush=True)
    lines = [f"知乎「{'/ '.join(args.keywords)}」问题汇总", f"共 {len(all_results)} 题", "="*70]
    for r in all_results:
        lines += [
            f"\n{'='*70}",
            f"【问题】{r['title']}",
            f"关键词：{'|'.join(r['matched_kw'])}  链接：{r['url']}",
            f"共 {r['fetched_count']} 条回答",
            "="*70,
        ]
        for i, ans in enumerate(r["answers"], 1):
            lines.append(f"\n--- 回答{i} | 赞{ans['voteup_count']} | {ans['author']} ---")
            lines.append(html_to_text(ans["content"]) or ans["excerpt"])
    mp = os.path.join(args.output, "_merged_all.txt")
    with open(mp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"合并文本: {mp}  ({os.path.getsize(mp)//1024} KB)", flush=True)

    total = sum(r["fetched_count"] for r in all_results)
    print(f"\n完成！{len(all_results)} 个问题，{total} 条回答\n输出: {os.path.abspath(args.output)}", flush=True)

if __name__ == "__main__":
    main()
