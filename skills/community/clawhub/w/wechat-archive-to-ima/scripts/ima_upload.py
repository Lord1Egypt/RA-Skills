#!/usr/bin/env python3
"""
ima_upload.py — 批量上传本地文件到腾讯 ima 知识库
用法：
    python ima_upload.py \
        --dir "<要上传的目录>" \
        --client-id "<ClientID>" \
        --api-key "<APIKey>" \
        --kb-id "<knowledge_base_id>" \
        [--folder-id "<folder_id>"] \
        [--limit 50]   # 单文件 MB 上限，默认 50
"""
import argparse
import csv
import json
import mimetypes
import os
import time
from pathlib import Path
from urllib import request, error


CREATE_MEDIA_URL = "https://ima.qq.com/openapi/wiki/v1/create_media"
ADD_KNOWLEDGE_URL = "https://ima.qq.com/openapi/wiki/v1/add_knowledge"


def http_post(url: str, headers: dict, body: dict) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = request.Request(url, data=data, method="POST")
    for k, v in headers.items():
        req.add_header(k, v)
    req.add_header("Content-Type", "application/json")
    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as e:
        return {"_error": e.code, "_body": e.read().decode("utf-8", errors="replace")}


def upload_one(file_path: Path, headers: dict, kb_id: str, folder_id: str) -> tuple[bool, str]:
    """
    简化版上传：只调 create_media + add_knowledge，
    COS 上传凭证在返回体里（实际接入时需根据返回字段用 POST 表单上传文件）。
    """
    size = file_path.stat().st_size
    if size > 50 * 1024 * 1024:
        return False, "文件超过 50MB"

    mime, _ = mimetypes.guess_type(str(file_path))
    mime = mime or "application/octet-stream"

    # Step 1: create_media
    body1 = {
        "file_name": file_path.name,
        "file_size": size,
        "content_type": mime,
        "knowledge_base_id": kb_id,
        "file_ext": file_path.suffix.lstrip("."),
    }
    r1 = http_post(CREATE_MEDIA_URL, headers, body1)
    if "_error" in r1:
        return False, f"create_media {r1['_error']}: {r1['_body'][:200]}"

    media_id = r1.get("media_id") or r1.get("data", {}).get("media_id")
    if not media_id:
        return False, f"create_media 返回缺 media_id: {json.dumps(r1)[:200]}"

    # Step 2: 实际上传文件到 COS（这里需要根据 create_media 返回的凭证字段做 multipart POST）
    # 由于不同时期 ima 返回的 COS 字段可能不同，这里只做占位说明：
    # >>> 实际部署时，从 r1 中取出临时凭证字段（cos_key / cos_secret / cos_token / upload_url），
    # >>> 用 requests.post(upload_url, files={file}, data={凭证字段}) 上传。
    # >>> 本脚本为通用占位版本，提示用户此步骤需要根据实测返回补全。

    # Step 3: add_knowledge
    body3 = {
        "media_type": 11,
        "title": file_path.stem,
        "knowledge_base_id": kb_id,
        "media_id": media_id,
    }
    if folder_id:
        body3["folder_id"] = folder_id
    body3["note_info"] = {
        "source": "微信归档",
        "original_name": file_path.name,
    }

    r3 = http_post(ADD_KNOWLEDGE_URL, headers, body3)
    if "_error" in r3:
        return False, f"add_knowledge {r3['_error']}: {r3['_body'][:200]}"

    return True, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--client-id", required=True)
    ap.add_argument("--api-key", required=True)
    ap.add_argument("--kb-id", required=True)
    ap.add_argument("--folder-id", default="")
    ap.add_argument("--limit", type=int, default=50, help="单文件 MB 上限")
    ap.add_argument("--sleep", type=float, default=1.0, help="请求间隔秒")
    args = ap.parse_args()

    headers = {
        "ima-openapi-clientid": args.client_id,
        "ima-openapi-apikey": args.api_key,
    }

    src_dir = Path(args.dir)
    files = [p for p in src_dir.rglob("*") if p.is_file() and
             p.stat().st_size < args.limit * 1024 * 1024]

    print(f"[*] 待上传: {len(files)} 个文件")
    results = []
    for i, fp in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {fp.name} ...", end=" ", flush=True)
        ok, msg = upload_one(fp, headers, args.kb_id, args.folder_id)
        print("✓" if ok else f"✗ {msg}")
        results.append({"文件": str(fp), "成功": ok, "备注": msg})
        time.sleep(args.sleep)

    # 失败清单
    fail_path = src_dir / "upload_failed.csv"
    with open(fail_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["文件", "成功", "备注"])
        w.writeheader()
        for r in results:
            if not r["成功"]:
                w.writerow(r)

    ok_cnt = sum(1 for r in results if r["成功"])
    print(f"\n[✓] 完成: {ok_cnt}/{len(results)} 成功")
    print(f"    失败清单: {fail_path}")
    print("\n[!] 注意: 本脚本的 COS 上传步骤为占位实现。")
    print("    首次真实调用时，需根据 create_media 返回的实际字段补全 Step 2 的 multipart 上传。")


if __name__ == "__main__":
    main()
