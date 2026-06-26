#!/usr/bin/env python3
import argparse
import csv
import json
import mimetypes
import os
import sys
import urllib.request
import urllib.error
import uuid

API_URL = "https://www.receiptextract.com/api/receipt/upload"
TOKEN_ENV_VAR = "RECEIPTEXTRACT_API_TOKEN"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".pdf"}


def read_token_from_env() -> str:
    return os.getenv(TOKEN_ENV_VAR, "").strip()


def is_supported_receipt_file(file_path: str) -> bool:
    return os.path.splitext(file_path)[1].lower() in SUPPORTED_EXTENSIONS


def collect_receipt_files(input_dir: str, recursive: bool) -> list:
    files = []
    if recursive:
        for root, _, names in os.walk(input_dir):
            for name in names:
                path = os.path.join(root, name)
                if os.path.isfile(path) and is_supported_receipt_file(path):
                    files.append(path)
    else:
        for name in os.listdir(input_dir):
            path = os.path.join(input_dir, name)
            if os.path.isfile(path) and is_supported_receipt_file(path):
                files.append(path)
    return sorted(files)


def build_multipart(field_name: str, file_path: str):
    boundary = f"----OpenClawBoundary{uuid.uuid4().hex}"
    filename = os.path.basename(file_path)
    content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    parts = []
    parts.append(f"--{boundary}\r\n".encode())
    parts.append(
        (
            f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode()
    )
    parts.append(file_bytes)
    parts.append("\r\n".encode())
    parts.append(f"--{boundary}--\r\n".encode())

    return boundary, b"".join(parts)


def upload_receipt(file_path: str, token: str):
    boundary, body = build_multipart("file", file_path)
    req = urllib.request.Request(API_URL, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("Content-Length", str(len(body)))

    try:
        with urllib.request.urlopen(req, data=body) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {"success": False, "error": raw}
        return e.code, payload


def print_summary(payload: dict):
    data = payload.get("data", {}) or {}
    print(f"Merchant: {data.get('merchant', '')}")
    print(f"Date: {data.get('date', '')}")
    print(f"Total: {data.get('total', '')}")
    print(f"Tax: {data.get('tax', '')}")
    print(f"Correctness: {data.get('correctnessCheck', '')}")
    saved_id = payload.get("savedReceiptId", "")
    if saved_id:
        print(f"SavedReceiptId: {saved_id}")
    items = data.get("items", []) or []
    if items:
        print("Items:")
        for item in items:
            desc = item.get("description", "")
            qty = item.get("quantity", "")
            price = item.get("total_price", "")
            sku = item.get("sku", "")
            line = f"- {desc}"
            if qty != "":
                line += f" | qty={qty}"
            if price != "":
                line += f" | total_price={price}"
            if sku:
                line += f" | sku={sku}"
            print(line)


def print_csv(payload: dict):
    data = payload.get("data", {}) or {}
    items = data.get("items", []) or []
    writer = csv.writer(sys.stdout)
    writer.writerow([
        "merchant",
        "date",
        "description",
        "quantity",
        "total_price",
        "item_tax",
        "sku",
        "receipt_tax",
        "receipt_total",
        "saved_receipt_id",
    ])
    for item in items:
        writer.writerow([
            data.get("merchant", ""),
            data.get("date", ""),
            item.get("description", ""),
            item.get("quantity", ""),
            item.get("total_price", ""),
            item.get("tax", ""),
            item.get("sku", ""),
            data.get("tax", ""),
            data.get("total", ""),
            payload.get("savedReceiptId", ""),
        ])


def print_batch_summary(results: list):
    for result in results:
        status = "OK" if result.get("success") else "FAIL"
        file_path = result.get("filePath", "")
        http_status = result.get("httpStatus", "")
        error = result.get("error", "")
        line = f"[{status}] {file_path} (http={http_status})"
        if error:
            line += f" error={error}"
        print(line)

    total = len(results)
    succeeded = sum(1 for r in results if r.get("success") is True)
    failed = total - succeeded
    print(f"Processed: {total}")
    print(f"Succeeded: {succeeded}")
    print(f"Failed: {failed}")


def print_batch_csv(results: list):
    writer = csv.writer(sys.stdout)
    writer.writerow([
        "source_file",
        "merchant",
        "date",
        "description",
        "quantity",
        "total_price",
        "item_tax",
        "sku",
        "receipt_tax",
        "receipt_total",
        "saved_receipt_id",
        "http_status",
        "success",
        "error",
    ])

    for result in results:
        payload = result.get("payload", {}) or {}
        data = payload.get("data", {}) or {}
        items = data.get("items", []) or []
        source_file = result.get("filePath", "")
        http_status = result.get("httpStatus", "")
        success = payload.get("success") is True
        error = payload.get("error", "")
        saved_receipt_id = payload.get("savedReceiptId", "")

        if not success:
            writer.writerow([
                source_file,
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                saved_receipt_id,
                http_status,
                success,
                error,
            ])
            continue

        if not items:
            writer.writerow([
                source_file,
                data.get("merchant", ""),
                data.get("date", ""),
                "",
                "",
                "",
                "",
                "",
                data.get("tax", ""),
                data.get("total", ""),
                saved_receipt_id,
                http_status,
                success,
                "",
            ])
            continue

        for item in items:
            writer.writerow([
                source_file,
                data.get("merchant", ""),
                data.get("date", ""),
                item.get("description", ""),
                item.get("quantity", ""),
                item.get("total_price", ""),
                item.get("tax", ""),
                item.get("sku", ""),
                data.get("tax", ""),
                data.get("total", ""),
                saved_receipt_id,
                http_status,
                success,
                "",
            ])


def main():
    parser = argparse.ArgumentParser(description="Extract receipt data using ReceiptExtract API")
    parser.add_argument("file", nargs="?", help="Path to receipt image or PDF")
    parser.add_argument("--input-dir", help="Directory containing receipt images or PDFs")
    parser.add_argument("--recursive", action="store_true", help="Recursively scan --input-dir")
    parser.add_argument("--format", choices=["json", "summary", "csv"], default="json")
    args = parser.parse_args()

    has_file = bool(args.file)
    has_input_dir = bool(args.input_dir)
    if has_file == has_input_dir:
        print("Provide exactly one input: either a file path or --input-dir", file=sys.stderr)
        sys.exit(2)

    if args.recursive and not has_input_dir:
        print("--recursive can only be used with --input-dir", file=sys.stderr)
        sys.exit(2)

    file_paths = []
    if has_file:
        file_path = os.path.expanduser(args.file)
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}", file=sys.stderr)
            sys.exit(2)
        if not is_supported_receipt_file(file_path):
            print(f"Unsupported file type: {file_path}", file=sys.stderr)
            sys.exit(2)
        file_paths = [file_path]
    else:
        input_dir = os.path.expanduser(args.input_dir)
        if not os.path.isdir(input_dir):
            print(f"Directory not found: {input_dir}", file=sys.stderr)
            sys.exit(2)
        file_paths = collect_receipt_files(input_dir, args.recursive)
        if not file_paths:
            print(f"No supported receipt files found in: {input_dir}", file=sys.stderr)
            sys.exit(2)

    token = read_token_from_env()
    if not token:
        print(f"Missing or empty {TOKEN_ENV_VAR}", file=sys.stderr)
        sys.exit(2)

    is_batch = len(file_paths) > 1 or has_input_dir

    if not is_batch:
        file_path = file_paths[0]
        status, payload = upload_receipt(file_path, token)

        if args.format == "json":
            print(json.dumps({"httpStatus": status, **payload}, indent=2, ensure_ascii=False))
        elif args.format == "summary":
            print_summary(payload)
        elif args.format == "csv":
            print_csv(payload)

        success = payload.get("success") is True
        if not success:
            sys.exit(1)
        return

    results = []
    for file_path in file_paths:
        status, payload = upload_receipt(file_path, token)
        results.append({
            "filePath": file_path,
            "httpStatus": status,
            "success": payload.get("success") is True,
            "error": payload.get("error", ""),
            "payload": payload,
        })

    processed = len(results)
    succeeded = sum(1 for r in results if r.get("success") is True)
    failed = processed - succeeded

    if args.format == "json":
        output = {
            "success": failed == 0,
            "processed": processed,
            "succeeded": succeeded,
            "failed": failed,
            "results": [
                {
                    "filePath": r.get("filePath"),
                    "httpStatus": r.get("httpStatus"),
                    **(r.get("payload") or {}),
                }
                for r in results
            ],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    elif args.format == "summary":
        print_batch_summary(results)
    elif args.format == "csv":
        print_batch_csv(results)

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
