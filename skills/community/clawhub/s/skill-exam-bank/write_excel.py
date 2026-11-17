"""调用内网 exam-ocr 服务，把 17 列表头的 JSON 记录写成题库 .xlsx。
用法: python write_excel.py <抽取结果.json> [输出.xlsx] [--url http://exam-ocr:8000]
服务地址：环境变量 EXAM_OCR_URL 或 --url，默认 http://exam-ocr:8000
说明：JSON 每条可含内部字段 题号（供漏题自检用），写表时只取下方 17 列表头，题号不写入 xlsx。
"""
import sys, os, json, argparse, requests

URL = os.environ.get("EXAM_OCR_URL", "http://exam-ocr:8000")

SCHEMA = [
    "课程", "知识点", "题型", "题目内容", "选项A", "选项B", "选项C", "选项D", "选项E",
    "正确答案", "难度", "状态", "是否真题", "是否模拟试卷", "是否考前押题", "年份", "解析",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("out", nargs="?", default=None)
    ap.add_argument("--url", default=os.environ.get("EXAM_OCR_URL", "http://exam-ocr:8000"))
    a = ap.parse_args()

    with open(a.json_path, encoding="utf-8") as f:
        records = json.load(f)
    if isinstance(records, dict):
        records = records.get("records", [])
    payload = {"schema": SCHEMA, "records": records}
    r = requests.post(f"{a.url}/write-excel", json=payload, timeout=120)
    r.raise_for_status()
    out = a.out or (a.json_path + ".xlsx")
    with open(out, "wb") as f:
        f.write(r.content)
    print(json.dumps({"ok": True, "saved": out, "records": len(records)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
