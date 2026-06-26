import os
import sys
import json
import base64
import mimetypes
import argparse
import traceback
from datetime import datetime
import requests

# Sudocode currently exposes nano-banana2 through this upstream model identifier.
MODEL = "gemini-3.1-flash-image-preview"


def init_logger(output_path):
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(output_path)), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    log_path = os.path.join(logs_dir, f"run-{ts}.log")
    log_fp = open(log_path, "w", encoding="utf-8")
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr

    class Tee:
        def __init__(self, *streams):
            self.streams = list(streams)

        def write(self, data):
            for s in self.streams:
                try:
                    s.write(data)
                    s.flush()
                except Exception:
                    pass
            return len(data)

        def flush(self):
            for s in self.streams:
                try:
                    s.flush()
                except Exception:
                    pass

        def remove(self, stream):
            self.streams = [s for s in self.streams if s is not stream]

    tee_out = Tee(sys.__stdout__, log_fp)
    tee_err = Tee(sys.__stderr__, log_fp)
    sys.stdout = tee_out
    sys.stderr = tee_err
    print(f"📝 日志文件: {log_path}")
    return log_fp, log_path, orig_stdout, orig_stderr, tee_out, tee_err

def read_image_as_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def guess_mime(path):
    mime, _ = mimetypes.guess_type(path)
    return mime or "image/png"

def save_image_from_response(data, output_path):
    candidates = data.get("candidates", [])
    for candidate in candidates:
        parts = candidate.get("content", {}).get("parts", [])
        for part in parts:
            inline_data = part.get("inlineData") or part.get("inline_data")
            if inline_data and inline_data.get("data"):
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(inline_data["data"]))
                return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--input_image", default=None)
    parser.add_argument("--output", default="output.png")
    args = parser.parse_args()

    abs_output = os.path.abspath(args.output)
    log_fp, log_path, orig_stdout, orig_stderr, tee_out, tee_err = init_logger(abs_output)

    try:
        api_key = os.getenv("SUDOCODE_IMAGE_API_KEY")
        base_url = os.getenv("SUDOCODE_BASE_URL", "https://sudocode.run")

        if not api_key:
            print("缺少 SUDOCODE_IMAGE_API_KEY 环境变量")
            print("请先前往 https://sudocode.us 注册并申请 API Key。")
            print("然后运行 init_env.py 写入 ~/.openclaw/.env 后再重试。")
            sys.exit(1)

        url = f"{base_url.rstrip('/')}/v1beta/models/{MODEL}:generateContent"

        parts = [{"text": args.prompt}]

        if args.input_image:
            if not os.path.exists(args.input_image):
                print(f"输入图片不存在: {args.input_image}")
                sys.exit(1)

            parts.append({
                "inline_data": {
                    "mime_type": guess_mime(args.input_image),
                    "data": read_image_as_base64(args.input_image)
                }
            })

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": parts
                }
            ],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"]
            }
        }

        headers = {
            "x-goog-api-key": api_key,
            "Content-Type": "application/json"
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=300)
        except Exception as e:
            print(f"请求失败: {e}")
            sys.exit(1)

        text = resp.text.lower()

        if resp.status_code >= 400:
            if resp.status_code in (402, 403, 429) or any(kw in text for kw in [
                "quota", "insufficient", "balance", "exceeded", "limit",
                "rate", "billing", "payment", "credit", "exhausted",
                "too many", "resource_exhausted", "429",
                "预扣费", "额度", "剩余", "余额", "充值", "sudocode_error"
            ]):
                print("❌ 额度不足或请求过于频繁！")
                print("👉 请前往 https://sudocode.us 登录并充值后重试。")
                sys.exit(2)

            print(f"❌ API 错误 (HTTP {resp.status_code})：")
            print(resp.text[:1000])
            sys.exit(1)

        try:
            data = resp.json()
        except json.JSONDecodeError:
            print("❌ 返回内容不是有效 JSON：")
            print(resp.text[:500])
            sys.exit(1)

        if save_image_from_response(data, abs_output):
            print(f"✅ 生成成功: {abs_output}")
            return

        # 检查是否返回了纯文本（模型拒绝生成图片的情况）
        text_parts = []
        for c in data.get("candidates", []):
            for p in c.get("content", {}).get("parts", []):
                if "text" in p:
                    text_parts.append(p["text"])
        if text_parts:
            print("⚠️ 模型返回了文本而非图片：")
            print("\n".join(text_parts))
            sys.exit(1)

        print("❌ 没有解析到图片，原始返回如下：")
        print(json.dumps(data, ensure_ascii=False, indent=2)[:1000])
        sys.exit(1)
    except SystemExit:
        raise
    except Exception:
        print("❌ 未捕获异常：")
        print(traceback.format_exc())
        sys.exit(1)
    finally:
        print(f"📍 本次日志: {log_path}")
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr
        tee_out.remove(log_fp)
        tee_err.remove(log_fp)
        log_fp.close()

if __name__ == "__main__":
    main()
