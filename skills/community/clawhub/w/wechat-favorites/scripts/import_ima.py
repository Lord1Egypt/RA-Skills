# -*- coding: utf-8 -*-
"""
IMA 知识库批量导入
从 articles_final.csv 读取 URL，批量导入到 IMA 知识库
支持断点续传，自动限速

配置优先级：命令行参数 > 环境变量 > config.json

用法：
    python import_ima.py                              # 使用 config.json 配置
    python import_ima.py --kb-id YOUR_KB_ID           # 指定知识库
    python import_ima.py --csv path/to/articles.csv   # 指定 CSV 文件
    IMA_CLIENT_ID=xxx IMA_API_KEY=xxx python import_ima.py  # 环境变量
"""
import csv, json, urllib.request, time, os, sys, argparse

# ===== 安全模式：完全禁用网络功能 =====
SAFE_MODE = os.environ.get("SAFE_MODE", "").lower() in ("1", "true", "yes")
if SAFE_MODE:
    print("[SAFE_MODE] 网络功能已禁用，IMA 导入不可用")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "exported_favorites")

BATCH_SIZE = 10


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='批量导入微信收藏到IMA知识库')
    parser.add_argument('--csv', default='', help='CSV 文件路径（默认: exported_favorites/articles_final.csv）')
    parser.add_argument('--kb-id', default='', help='IMA 知识库 ID')
    parser.add_argument('--client-id', default='', help='IMA Client ID')
    parser.add_argument('--api-key', default='', help='IMA API Key')
    parser.add_argument('--state', default='', help='断点续传状态文件')
    parser.add_argument('--log', default='', help='日志文件路径')
    parser.add_argument('--batch-size', type=int, default=BATCH_SIZE, help='每批导入数量（默认: 10）')
    return parser.parse_args()


def load_config():
    """从 config.json 读取配置（最低优先级）"""
    cfg_path = os.path.join(SCRIPT_DIR, "config.json")
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_ima_credentials():
    """从 ~/.config/ima/ 读取 IMA 凭证"""
    client_id_path = os.path.expanduser("~/.config/ima/client_id")
    api_key_path = os.path.expanduser("~/.config/ima/api_key")
    
    client_id = ""
    api_key = ""
    
    if os.path.exists(client_id_path):
        client_id = open(client_id_path).read().strip()
    if os.path.exists(api_key_path):
        api_key = open(api_key_path).read().strip()
    
    return client_id, api_key


def resolve_config(args):
    """合并配置：命令行 > 环境变量 > config.json > ~/.config/ima/"""
    cfg = load_config()
    file_client_id, file_api_key = get_ima_credentials()
    
    # 按优先级合并
    client_id = (
        args.client_id or
        os.environ.get('IMA_CLIENT_ID', '') or
        file_client_id
    )
    
    api_key = (
        args.api_key or
        os.environ.get('IMA_API_KEY', '') or
        file_api_key
    )
    
    kb_id = (
        args.kb_id or
        os.environ.get('IMA_KB_ID', '') or
        cfg.get('ima_kb_id', '')
    )
    
    csv_path = args.csv or os.path.join(OUTPUT_DIR, 'articles_final.csv')
    state_file = args.state or os.path.join(SCRIPT_DIR, 'ima_import_state.json')
    log_file = args.log or os.path.join(SCRIPT_DIR, 'ima_import.log')
    batch_size = args.batch_size
    
    return {
        'client_id': client_id,
        'api_key': api_key,
        'kb_id': kb_id,
        'csv_path': csv_path,
        'state_file': state_file,
        'log_file': log_file,
        'batch_size': batch_size,
    }

def load_state(state_file):
    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"imported": 0, "failed": 0, "skipped": 0, "batch": 0, "errors": [], "last_url": ""}

def save_state(state_file, state):
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def log(log_file, msg):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def import_batch(kb_id, urls, client_id, api_key):
    """批量导入 URL 到 IMA 知识库"""
    if SAFE_MODE:
        print("[SAFE_MODE] 网络功能已禁用")
        return {"code": -1, "msg": "SAFE_MODE enabled"}
    
    body = json.dumps({"knowledge_base_id": kb_id, "urls": urls}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "https://ima.qq.com/openapi/wiki/v1/import_urls",
        data=body,
        headers={
            "ima-openapi-clientid": client_id,
            "ima-openapi-apikey": api_key,
            "Content-Type": "application/json; charset=utf-8"
        },
        method="POST"
    )
    resp = urllib.request.urlopen(req, timeout=120)
    return json.loads(resp.read())

def main():
    print("=" * 60)
    print("  IMA 知识库批量导入")
    print("=" * 60)

    args = parse_args()
    config = resolve_config(args)
    
    client_id = config['client_id']
    api_key = config['api_key']
    kb_id = config['kb_id']
    csv_path = config['csv_path']
    state_file = config['state_file']
    log_file = config['log_file']
    batch_size = config['batch_size']

    if not kb_id:
        print("[ERROR] 未配置 IMA 知识库 ID。使用 --kb-id 参数、IMA_KB_ID 环境变量或 config.json 中的 ima_kb_id")
        sys.exit(1)
    
    if not client_id or not api_key:
        print("[ERROR] 未配置 IMA 凭证。使用 --client-id/--api-key 参数、IMA_CLIENT_ID/IMA_API_KEY 环境变量或 ~/.config/ima/ 文件")
        sys.exit(1)

    if not os.path.exists(csv_path):
        print(f"[ERROR] CSV 文件不存在: {csv_path}")
        print("请先运行 classify_favorites.py 生成")
        sys.exit(1)

    state = load_state(state_file)
    log(log_file, f"=== Starting (resume from batch {state['batch']}) ===")
    log(log_file, f"Previous: imported={state['imported']}, failed={state['failed']}")
    log(log_file, f"Config: kb_id={kb_id[:8]}..., batch_size={batch_size}")

    # 收集所有 URL
    all_urls = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get("url", "").strip()
            if url.startswith("http"):
                all_urls.append(url)

    total = len(all_urls)
    log(log_file, f"Total URLs: {total}")

    start_idx = state["batch"] * batch_size
    if start_idx >= total:
        log(log_file, "All batches already processed!")
        return

    batch_urls = []

    for i in range(start_idx, total):
        batch_urls.append(all_urls[i])

        if len(batch_urls) == batch_size or i == total - 1:
            try:
                result = import_batch(kb_id, batch_urls, client_id, api_key)
                if result.get("code") == 0:
                    results = result.get("data", {}).get("results", {})
                    success = sum(1 for r in results.values() if r.get("ret_code") == 0)
                    fail = len(results) - success
                    state["imported"] += success
                    state["failed"] += fail
                    log(log_file, f"Batch {state['batch'] + 1}: +{success} ok, {fail} fail")
                else:
                    state["failed"] += len(batch_urls)
                    log(log_file, f"Batch {state['batch'] + 1}: API error - {result.get('msg', 'unknown')}")
            except Exception as e:
                state["failed"] += len(batch_urls)
                log(log_file, f"Batch {state['batch'] + 1}: Exception - {e}")
                if "403" in str(e) or "Forbidden" in str(e):
                    log(log_file, "Rate limited! Sleeping 60s...")
                    save_state(state_file, state)  # 限流前保存状态
                    time.sleep(60)

            state["batch"] += 1
            state["last_url"] = batch_urls[-1][:80]

            if batch_count % 10 == 0:
                save_state(state_file, state)

            batch_urls = []
            time.sleep(3.0)

    save_state(state_file, state)
    log(log_file, f"=== Complete: imported={state['imported']}, failed={state['failed']} ===")

if __name__ == "__main__":
    main()
