"""便携版真题转题库：任何能跑 Python + 有 deepseek key 的 AI/客户端都能一键跑（与 OpenClaw 解耦）。
Version: 1.2.0 (2026-09-09)  ——年份列填 XXXX年XX月；解析列必填
流程: OCR(exam-ocr) -> deepseek 抽取(含题号) -> 写xlsx -> 漏题自检 -> 自动补题(最多3轮)。
用法:
  python auto_run.py <pdf> <out.xlsx> --course 马克思主义基本原理 --year 2026 [--month 4] \
        [--url http://exam-ocr:8000] [--api-key sk-...] [--ocr-md out.md]
- 年份列写"2026年4月"格式：给了 --month 则拼成 2026年4月，不给则只写 2026（同课程同年多考期务必给 --month）。
- OCR/写表依赖内网 exam-ocr 服务（EXAM_OCR_URL 或 --url）。
- 抽取用 deepseek API，key 来自 --api-key 或环境变量 DEEPSEEK_API_KEY（用调用方自己的 key，不要共用 OpenClaw 的）。
"""
import sys, os, re, json, argparse, requests

DEFAULT_URL = os.environ.get("EXAM_OCR_URL", "http://exam-ocr:8000")
API_URL = "https://api.deepseek.com/chat/completions"
SCHEMA = ["课程", "知识点", "题型", "题目内容", "选项A", "选项B", "选项C", "选项D", "选项E",
          "正确答案", "难度", "状态", "是否真题", "是否模拟试卷", "是否考前押题", "年份", "解析"]

PROMPT = """你是自考题库整理助手。下面是一份真题 OCR 文本。请按以下字段把每道题抽成一条 JSON 记录，
并额外给每条加一个整数 题号（全局连续编号：单选从1起、简答续编、论述续编；若原卷分节编号也请按阅读顺序编成全局连续号）。
输出 JSON 数组，每条字段顺序：
["题号","课程","知识点","题型","题目内容","选项A","选项B","选项C","选项D","选项E","正确答案","难度","状态","是否真题","是否模拟试卷","是否考前押题","年份","解析"]
规则：
- 选择题答案通常在试卷末尾"参考答案"区，请把正确选项字母关联到对应题目；找不到答案填 ""。
- 选项只填 A~E 有内容的；无则空字符串。
- 题型从"单选/多选/判断/填空/简答/计算/论述"中归类。
- 年份列填消息里给出的考期值（如 2026年4月），逐字照抄、不要改写格式；是否真题=是；状态=启用；是否模拟试卷/是否考前押题=否。
- 题目内容保留完整题干（含题号文字），去掉页码/页眉页脚噪点。
- 解析列必填（重点）：客观题写 1~3 句，讲清正确项成立的依据，并点明主要干扰项为什么错；主观题写 3~5 条得分要点；判断题说明正确的表述应该是什么。禁止留空、禁止只写"略"、禁止照抄题干。
只输出 JSON 数组，不要任何解释文字。"""


def ocr(url, pdf):
    with open(pdf, "rb") as f:
        r = requests.post(f"{url}/parse",
                          files={"file": (os.path.basename(pdf), f, "application/octet-stream")},
                          timeout=600)
    r.raise_for_status()
    return r.json()


def extract(api_key, md_text, course, period, focus=None):
    user = f"课程：{course}\n年份：{period}\n"
    if focus:
        user += f"\n⚠ 以下题号上次漏抽，请重点补全（题型+题号）：{focus}\n"
    user += f"\nOCR文本：\n{md_text}"
    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": user},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    h = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    r = requests.post(API_URL, json=body, headers=h, timeout=300)
    r.raise_for_status()
    content = r.json()["choices"][0]["message"]["content"]
    data = json.loads(content)
    if isinstance(data, dict):
        data = data.get("records", [])
    return data


def write_excel(url, records, out):
    r = requests.post(f"{url}/write-excel", json={"schema": SCHEMA, "records": records}, timeout=120)
    r.raise_for_status()
    with open(out, "wb") as f:
        f.write(r.content)
    return out


def check(recs):
    groups = {}
    for r in recs:
        g = r.get("题型", "未知")
        q = r.get("题号")
        if q is None:
            m = re.match(r"\s*(\d+)\s*[.、．]", r.get("题目内容", "") or "")
            q = int(m.group(1)) if m else None
        groups.setdefault(g, []).append(q)
    missing = []
    for g, nums in groups.items():
        nums = [n for n in nums if n is not None]
        if not nums:
            continue
        lo, hi = min(nums), max(nums)
        for n in range(lo, hi + 1):
            if n not in nums:
                missing.append((g, n))
    return missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("out")
    ap.add_argument("--course", required=True)
    ap.add_argument("--year", required=True)
    ap.add_argument("--month", default="")
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--api-key", default=os.environ.get("DEEPSEEK_API_KEY"))
    ap.add_argument("--ocr-md", default=None)
    a = ap.parse_args()

    if not a.api_key:
        raise SystemExit("需要 deepseek key：--api-key 或环境变量 DEEPSEEK_API_KEY")

    print("① OCR 解析中...", flush=True)
    data = ocr(a.url, a.pdf)
    md = data.get("markdown", "")
    if a.ocr_md:
        open(a.ocr_md, "w", encoding="utf-8").write(md)

    print("② deepseek 抽取中...", flush=True)
    period = f"{a.year}年{int(a.month)}月" if a.month else str(a.year)
    recs = extract(a.api_key, md, a.course, period)

    for attempt in range(3):
        miss = check(recs)
        if not miss:
            break
        focus = ",".join(f"{g}{n}" for g, n in miss[:40])
        print(f"③ 第{attempt + 1}次补题，缺：{focus}", flush=True)
        extra = extract(a.api_key, md, a.course, period, focus=focus)
        seen = {(r.get("题型"), r.get("题号")): r for r in recs}
        for r in extra:
            seen[(r.get("题型"), r.get("题号"))] = r
        recs = list(seen.values())

    miss = check(recs)
    print(f"抽取 {len(recs)} 题，自检缺题 {len(miss)}：{miss}", flush=True)

    print(f"④ 写 Excel -> {a.out}", flush=True)
    write_excel(a.url, recs, a.out)
    print("✅ 完成。")


if __name__ == "__main__":
    main()
