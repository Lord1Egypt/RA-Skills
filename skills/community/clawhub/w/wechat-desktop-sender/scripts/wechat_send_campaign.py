import argparse
import csv
import json
import logging
import time
from datetime import datetime
from pathlib import Path

from wechat_send_hello import (
    DEFAULT_LOG_DIR,
    connect_wechat_window,
    ensure_wechat,
    open_chat,
    send_message,
    setup_logging,
)


def parse_args():
    parser = argparse.ArgumentParser(description="微信个性化串行发送")
    parser.add_argument("--csv", help="CSV 文件路径，至少包含 contact,message 两列")
    parser.add_argument("--json", dest="json_file", help="JSON 文件路径，内容为 [{contact, message}] 列表")
    parser.add_argument("--delay", type=float, default=1.5, help="每步 UI 操作后的等待秒数")
    parser.add_argument("--between", type=float, default=1.0, help="联系人之间等待秒数")
    parser.add_argument("--log-dir", default=str(DEFAULT_LOG_DIR), help="日志与结果输出目录")
    parser.add_argument("--verify-title", action="store_true", help="校验窗口标题里是否包含聊天名")
    parser.add_argument("--stop-on-error", action="store_true", help="遇到失败立即停止")
    return parser.parse_args()



def load_rows(args):
    rows = []
    if args.csv:
        path = Path(args.csv)
        if not path.exists():
            raise FileNotFoundError(f"CSV 文件不存在: {path}")
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=1):
                contact = (row.get("contact") or row.get("to") or "").strip()
                message = (row.get("message") or row.get("text") or "").strip()
                if not contact or not message:
                    continue
                rows.append({"contact": contact, "message": message, "row": idx})

    if args.json_file:
        path = Path(args.json_file)
        if not path.exists():
            raise FileNotFoundError(f"JSON 文件不存在: {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        for idx, item in enumerate(data, start=1):
            contact = (item.get("contact") or item.get("to") or "").strip()
            message = (item.get("message") or item.get("text") or "").strip()
            if not contact or not message:
                continue
            rows.append({"contact": contact, "message": message, "row": idx})

    if not rows:
        raise ValueError("没有可发送的数据，请提供 --csv 或 --json")
    return rows



def classify_retry(error):
    if not error:
        return False
    text = str(error).lower()
    retry_keywords = ["没找到", "超时", "timeout", "焦点", "窗口", "搜索框", "输入框"]
    return any(k in text for k in retry_keywords)



def build_summary_payload(results):
    total = len(results)
    success = sum(1 for x in results if x.get("success"))
    verified = sum(1 for x in results if x.get("verified"))
    failed = total - success
    retryable = sum(1 for x in results if x.get("retry_recommended"))
    return {
        "summary": {
            "total": total,
            "success": success,
            "failed": failed,
            "verified": verified,
            "retry_recommended": retryable,
        },
        "results": results,
    }



def save_summary(log_dir: Path, results):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = log_dir / f"wechat-campaign-summary-{ts}.json"
    payload = build_summary_payload(results)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    logging.info("个性化发送结果已保存: %s", out)
    return out



def main():
    args = parse_args()
    log_dir = Path(args.log_dir)
    log_file = setup_logging(log_dir)
    rows = load_rows(args)

    logging.info("日志文件: %s", log_file)
    logging.info("个性化发送启动，条目数量: %s", len(rows))

    ensure_wechat()
    win = connect_wechat_window()

    results = []
    for idx, item in enumerate(rows, start=1):
        result = {
            "index": idx,
            "row": item.get("row", idx),
            "contact": item["contact"],
            "message": item["message"],
            "success": False,
            "verified": False,
            "error": None,
            "status": "pending",
            "retry_recommended": False,
            "sent_at": None,
        }
        try:
            logging.info("[%s/%s] 开始发送给: %s", idx, len(rows), item["contact"])
            open_chat(win, item["contact"], args.delay, args.verify_title)
            verified, _texts = send_message(win, item["message"], args.delay)
            result["success"] = True
            result["verified"] = bool(verified)
            result["status"] = "sent_verified" if verified else "sent_unverified"
            result["sent_at"] = datetime.now().isoformat(timespec="seconds")
            logging.info("[%s/%s] 完成: %s | verified=%s", idx, len(rows), item["contact"], verified)
        except Exception as e:
            result["error"] = str(e)
            result["status"] = "failed"
            result["retry_recommended"] = classify_retry(e)
            logging.exception("[%s/%s] 发送失败: %s", idx, len(rows), item["contact"])
            results.append(result)
            if args.stop_on_error:
                save_summary(log_dir, results)
                raise
            time.sleep(args.between)
            continue

        results.append(result)
        if idx < len(rows):
            time.sleep(args.between)

    success_count = sum(1 for x in results if x["success"])
    verified_count = sum(1 for x in results if x["verified"])
    retry_count = sum(1 for x in results if x.get("retry_recommended"))
    logging.info("个性化发送完成: success=%s/%s, verified=%s/%s, retry_recommended=%s", success_count, len(results), verified_count, len(results), retry_count)
    save_summary(log_dir, results)


if __name__ == "__main__":
    main()
