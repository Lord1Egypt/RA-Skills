#!/usr/bin/env python3
"""自定义模型能力探测器 —— 加新模型后跑这一个就够。

用法（默认探测 ~/.workbuddy/models.json 里的全部模型）：
    python probe_model.py
    python probe_model.py --model deepseek-v4-flash
    python probe_model.py --model my-new-model --url https://.../chat/completions --key sk-xxx
    python probe_model.py --no-vision        # 跳过读图探测（纯文本模型，省一次大图请求）

探测四件事，输出可直接抄进 models.json 的结论：
  1. 读图      标准 image_url + 结构化提问（看 content 有没有真实描述，不是看 HTTP 200）
  2. 工具调用  发一个最小 tools 定义，看有没有标准 tool_calls
  3. 档位枚举  用非法值触发服务端报错，套出合法 effort 列表
  4. 档位可用  逐档实跑，确认哪些真的 200

关键坑（都在代码里处理了，别手动绕过）：
  · max_tokens 给太小会被 reasoning token 吃光 → content 为空，
    会被误判成「不支持读图」。这里统一用 MAX_TOKENS=900。
  · 不要只看 HTTP 200 判断多模态，必须看 content 里的实际描述。
  · 有些服务端拒非法值时只回一句笼统的 invalid_request_error，不列候选，
    此时自动退回逐档实跑。
  · 部分厂商要求带 User-Agent（Cloudflare 会挡裸 urllib），统一带上。

零依赖，只用标准库。
"""

import argparse
import base64
import json
import os
import sys
import time
import http.client
import ssl
import tempfile
from urllib.parse import urlparse

MODELS_PATH = os.path.expanduser("~/.workbuddy/models.json")

# 客户端 UI 内置枚举（读自 codebuddy-lite-wb.mjs）。配置里只写这些才选得到。
CLIENT_EFFORTS = ["off", "minimal", "low", "medium", "high", "xhigh", "max"]

# 探测读图/推理统一用这个值 —— 小于 800 会被 reasoning token 吃光
MAX_TOKENS = 900

# 默认测试图：脚本用标准库现画一张有明确视觉内容的 PNG（橙色圆 + 蓝色底）。
# 关键：不能用 8x8 纯色图 —— 部分厂商会拒（实测 Space Bunny 对纯色图直接 400）。
# ⚠ 必须落在**系统临时目录**，不能写在 skill 目录里：
#   1) skill 一旦发布就成公开内容，而 SkillHub / ClawHub 都**禁止打包 png**
#      （实测报「不允许的文件类型: _probe_image.png」）；
#   2) 缓存写进安装目录也会让 skill 目录永远多出一个非预期文件。
MIN_PROBE_PNG = os.path.join(
    tempfile.gettempdir(), "_wb_model_probe_image.png")


def make_probe_png(path, w=256, h=256):
    """零依赖生成测试图：蓝色背景 + 橙色实心圆。内容明确，便于模型描述。"""
    import struct
    import zlib

    cx, cy, r = w // 2, h // 2, min(w, h) // 3

    rows = bytearray()
    for y in range(h):
        rows.append(0)  # PNG 每行起始 filter byte 0
        for x in range(w):
            inside = (x - cx) ** 2 + (y - cy) ** 2 <= r * r
            rows += b"\xe0\x6a\x1e" if inside else b"\x1e\x5c\xa0"  # 橙 / 蓝

    def chunk(tag, data):
        c = tag + data
        return (struct.pack(">I", len(data)) + c
                + struct.pack(">I", zlib.crc32(c) & 0xffffffff))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(rows), 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    return path


def load_image_b64(image_arg):
    """返回 base64 字符串。image_arg 为空则现画一张测试图。"""
    path = image_arg
    if not path:
        if not os.path.exists(MIN_PROBE_PNG):
            make_probe_png(MIN_PROBE_PNG)
        path = MIN_PROBE_PNG
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def _png_size(b64):
    """从 PNG 头读真实宽高（IHDR 在第 16-24 字节）。"""
    raw = base64.b64decode(b64)
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a png")
    w = int.from_bytes(raw[16:20], "big")
    h = int.from_bytes(raw[20:24], "big")
    return w, h


def post(url, body, api_key, timeout=150, ua=True):
    """POST 一个 JSON，返回 (status, 响应文本)。"""
    u = urlparse(url)
    host = u.hostname
    port = u.port or (443 if u.scheme == "https" else 80)
    path = u.path or "/"
    if u.query:
        path += "?" + u.query

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    if ua:
        # 部分厂商（Cloudflare）在 User-Agent 缺失时返回 403 error code: 1010
        headers["User-Agent"] = "curl/8.0"

    cls = http.client.HTTPSConnection if u.scheme == "https" else http.client.HTTPConnection
    ctx = ssl.create_default_context() if u.scheme == "https" else None
    conn = cls(host, port, timeout=timeout, context=ctx) if ctx else cls(host, port, timeout=timeout)
    try:
        conn.request("POST", path, json.dumps(body), headers)
        r = conn.getresponse()
        return r.status, r.read().decode("utf-8", "replace")
    finally:
        conn.close()


def parse(raw):
    try:
        return json.loads(raw)
    except Exception:
        return {}


def err_text(d, raw):
    e = d.get("error")
    if isinstance(e, dict):
        return str(e.get("message") or e)
    if isinstance(e, str):
        return e
    return (raw or "")[:300]


def _text_of(d):
    """从各种可能的响应形状里取出文本内容。"""
    try:
        msg = d["choices"][0]["message"]
    except Exception:
        return "", ""
    content = msg.get("content")
    if isinstance(content, list):  # 少数端点返回 content 数组
        content = " ".join(
            c.get("text", "") for c in content if isinstance(c, dict)
        )
    reasoning = msg.get("reasoning_content") or msg.get("reasoning") or ""
    return (content or ""), reasoning


# ---------------------------------------------------------------- 1. 读图

VISION_PROMPT = (
    "Look at the image carefully, then answer exactly two things on "
    "separate lines:\n"
    "SHAPE: <the main shape you see>\n"
    "COLOR: <the main color of that shape>\n"
    "If the image contains an animal instead, write ANIMAL: <its name> "
    "on the first line."
)


def probe_vision(model, url, key, image_b64, retries=3):
    """探测读图。返回 (支持?, 详情, reasoning 片段)。

    判据不能只看 content —— reasoning 模型常把预算全花在思维链上，
    正文为空但 reasoning 里已经描述了图像内容（实测 DeepSeek 6/6 次如此）。
    因此只要 content 或 reasoning 里出现对图像的实际描述即算支持。
    """
    body = {
        "model": model,
        "max_tokens": MAX_TOKENS,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": VISION_PROMPT},
                {"type": "image_url",
                 "image_url": {"url": "data:image/png;base64," + image_b64}},
            ],
        }],
    }

    last = ("", "")
    for attempt in range(retries):
        st, raw = post(url, body, key)
        if st != 200:
            last = ("HTTP %s: %s" % (st, err_text(parse(raw), raw)[:160]), "")
            time.sleep(4)
            continue

        d = parse(raw)
        content, reasoning = _text_of(d)
        blob = (content + "\n" + reasoning).lower()
        # 图像描述的证据：模型说出了图里的具体内容（形状/颜色/物体）
        described = any(k in blob for k in (
            "orange", "blue", "circle", "round", "square", "cat", "dog",
            "animal", "fish", "goldfish", "image shows", "the image",
            "橘", "猫", "圆形", "方块"))
        # 结构化格式痕迹
        structured = ("shape" in blob and "color" in blob) or (
            "animal" in blob and "style" in blob)

        if content.strip() and (structured or described):
            return True, "content=%r" % content.strip()[:120], reasoning[:120]

        # 正文空但 reasoning 已描述图像 —— 仍然算支持（提高 max_tokens 往往就有正文）
        if described:
            return (True,
                    "content 为空但 reasoning 已描述图像（预算被推理吃光），"
                    "reasoning=%r" % reasoning.strip()[:110],
                    reasoning[:120])

        last = ("content=%r" % content.strip()[:100],
                reasoning[:120])
        time.sleep(4)

    ok, detail, reasoning = last
    return False, "重试 %d 次均未识别图像内容  %s" % (retries, detail), reasoning


# ------------------------------------------------------------ 2. 工具调用

TOOL_PROMPT = "What is the weather in Beijing right now? Use the tool."


def probe_tools(model, url, key):
    body = {
        "model": model,
        "max_tokens": MAX_TOKENS,
        "tools": [{
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather for a city",
                "parameters": {
                    "type": "object",
                    "properties": {"city": {"type": "string"}},
                    "required": ["city"],
                },
            },
        }],
        "tool_choice": "auto",
        "messages": [{"role": "user", "content": TOOL_PROMPT}],
    }
    st, raw = post(url, body, key)
    if st != 200:
        # 有些服务端不接受 tool_choice，但接受 tools
        body.pop("tool_choice", None)
        st, raw = post(url, body, key)
    if st != 200:
        return False, "HTTP %s: %s" % (st, err_text(parse(raw), raw)[:160])
    d = parse(raw)
    try:
        calls = d["choices"][0]["message"].get("tool_calls") or []
    except Exception:
        return False, "响应形状异常"
    if not calls:
        return False, "无 tool_calls"
    fn = calls[0].get("function", {})
    ok = fn.get("name") == "get_weather"
    return ok, "name=%r args=%r" % (fn.get("name"), str(fn.get("arguments"))[:80])


# ---------------------------------------------------------- 3-4. 档位枚举

EASY_Q = "What is 17*23? Answer with the number only."


def try_effort(model, url, key, eff):
    body = {"model": model, "max_tokens": 400, "messages": [
        {"role": "user", "content": EASY_Q}]}
    if eff is not None:
        body["reasoning_effort"] = eff
    st, raw = post(url, body, key)
    return st, raw


def probe_efforts(model, url, key, pause=3.0):
    """先试图非法值套枚举，失败则逐档实跑。返回 (accepted_list, notes)。"""
    notes = []
    st, raw = try_effort(model, url, key, "__probe__")
    enumerated = []
    if st != 200:
        msg = err_text(parse(raw), raw)
        notes.append("非法值报错: %s" % msg[:200])
        # 从报错里抠出候选词
        import re
        m = re.search(r"expected one of(.*)", msg, re.I)
        if m:
            enumerated = re.findall(r"`([a-z]+)`", m.group(1))

    accepted = []
    if enumerated:
        for eff in enumerated:
            st, raw = try_effort(model, url, key, eff)
            ok = st == 200
            if ok:
                accepted.append(eff)
            print("      %-9s %s" % (eff, "200" if ok else "HTTP %s" % st))
            time.sleep(pause)
    else:
        notes.append("服务端未列候选 → 逐档实跑")
        for eff in CLIENT_EFFORTS:
            if eff == "off":
                continue
            codes = []
            for _ in range(2):
                st, raw = try_effort(model, url, key, eff)
                codes.append(st)
                time.sleep(pause)
            ok = all(c == 200 for c in codes)
            if ok:
                accepted.append(eff)
            print("      %-9s %s" % (eff, "/".join(map(str, codes))))

    # 基线：不传档位，看是否仍然推理
    st, raw = try_effort(model, url, key, None)
    if st == 200:
        _, reasoning = _text_of(parse(raw))
        notes.append("不传档位: reasoning_content 长度=%d%s"
                     % (len(reasoning), "（会推理）" if reasoning else "（不推理）"))
    return accepted, notes


# ------------------------------------------------------------------ 主流程


def probe_one(entry, do_vision=True, pause=3.0, image_b64=None):
    model = entry["id"]
    url = entry["url"]
    key = entry.get("apiKey", "")
    name = entry.get("name", model)

    print("\n" + "=" * 66)
    print("%s  (%s)" % (name, model))
    print("  url  %s" % url)
    print("=" * 66)

    results = {}
    partial = False   # 是否有探测项因异常未得出结论

    if do_vision:
        print("  [1/4] 读图")
        try:
            ok, detail, _ = probe_vision(model, url, key, image_b64)
        except Exception as ex:
            ok, detail, partial = None, "探测异常: %r" % ex, True
        results["supportsImages"] = ok
        verdict = "支持" if ok else ("不支持" if ok is False else "未确定")
        print("      %s  %s" % (verdict, detail))
        time.sleep(pause)
    else:
        results["supportsImages"] = None

    print("  [2/4] 工具调用")
    try:
        ok, detail = probe_tools(model, url, key)
    except Exception as ex:
        ok, detail, partial = None, "探测异常: %r" % ex, True
    results["supportsToolCall"] = ok
    verdict = "支持" if ok else ("不支持" if ok is False else "未确定")
    print("      %s  %s" % (verdict, detail))
    time.sleep(pause)

    print("  [3/4] 思考强度档位")
    try:
        accepted, notes = probe_efforts(model, url, key, pause)
    except Exception as ex:
        accepted, notes, partial = [], ["探测异常: %r" % ex], True
    results["efforts"] = accepted
    for n in notes:
        print("      · %s" % n)

    usable = [e for e in accepted if e in CLIENT_EFFORTS and e != "off"]
    dropped = [e for e in accepted if e not in CLIENT_EFFORTS]
    results["usable"] = usable
    if dropped:
        print("      · 服务端支持但客户端选不到: %s" % "/".join(dropped))
    results["supportsReasoning"] = bool(usable)
    if not usable:
        partial = True   # 没探到任何可用档位，不能据此判定"不支持推理"

    results["_partial"] = partial
    return results


def main():
    ap = argparse.ArgumentParser(description="自定义模型能力探测器")
    ap.add_argument("--model", help="只探测指定 model id")
    ap.add_argument("--url", help="配合 --model 使用，覆盖 url")
    ap.add_argument("--key", help="配合 --model 使用，覆盖 apiKey")
    ap.add_argument("--image", help="读图探测用的图片路径（默认现画测试图）")
    ap.add_argument("--no-vision", action="store_true", help="跳过读图探测")
    ap.add_argument("--pause", type=float, default=3.0, help="每次请求间隔秒")
    ap.add_argument("--apply", action="store_true",
                    help="把探测结论直接写回 models.json（先自动备份）")
    ap.add_argument("--add", action="store_true",
                    help="配合 --url 把新模型追加进 models.json（先探测再写）")
    ap.add_argument("--name", help="配合 --add 指定的显示名")
    ap.add_argument("--vendor", help="配合 --add 指定的厂商名")
    ap.add_argument("--default-effort",
                    help="配合 --apply 指定默认档位（默认取 medium 或中位档）")
    ap.add_argument("--force", action="store_true",
                    help="配合 --apply：即使探测结果全部不完整也强制写入")
    args = ap.parse_args()

    if args.add and not args.url:
        sys.exit("--add 需要配合 --url（并用 --model 指定模型 id）")

    if args.url:
        if not args.model:
            sys.exit("--url 需要配合 --model")
        entries = [{"id": args.model, "url": args.url, "apiKey": args.key or "",
                    "name": args.model}]
    else:
        if not os.path.exists(MODELS_PATH):
            sys.exit("找不到 %s" % MODELS_PATH)
        entries = json.load(open(MODELS_PATH, encoding="utf-8"))
        if args.model:
            entries = [e for e in entries if e.get("id") == args.model]
            if not entries:
                sys.exit("models.json 里没有 id=%s" % args.model)

    image_b64 = None
    if not args.no_vision:
        image_b64 = load_image_b64(args.image)
        print("测试图: %s" % (args.image or "现画的橙圆蓝底图"))

    print("探测 %d 个模型（max_tokens=%d，间隔 %.1fs）"
          % (len(entries), MAX_TOKENS, args.pause))

    if args.add:
        append_entry(entries[0], args.name, args.vendor)

    out = {}
    for e in entries:
        try:
            out[e["id"]] = probe_one(e, not args.no_vision, args.pause, image_b64)
        except Exception as ex:
            print("  !! 探测失败: %r" % ex)
            out[e["id"]] = {"error": repr(ex)}

    print("\n" + "=" * 66)
    print("探测结论")
    print("=" * 66)
    print(json.dumps(out, ensure_ascii=False, indent=2))

    if args.apply or args.add:
        apply_results(out, entries, args.default_effort, args.force)
    else:
        print("\n（加 --apply 可直接把能力位写回 models.json）")


# ------------------------------------------------------------------ 写回

FIELD_ORDER = ["id", "name", "vendor", "url", "apiKey", "supportsImages",
               "supportsToolCall", "supportsReasoning", "reasoning"]


def append_entry(entry, name=None, vendor=None):
    """把新模型追加进 models.json（先备份）。能力位留空，等探测后填。"""
    before = json.load(open(MODELS_PATH, encoding="utf-8"))
    if any(m.get("id") == entry["id"] for m in before):
        print("\n%s 已存在于 models.json，跳过追加（可直接 --apply 更新能力位）"
              % entry["id"])
        return

    before.append({
        "id": entry["id"],
        "name": name or entry["id"],
        "vendor": vendor or "custom",
        "url": entry["url"],
        "apiKey": entry.get("apiKey", ""),
        "supportsImages": False,
        "supportsToolCall": False,
        "supportsReasoning": False,
    })

    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak_dir = os.path.join(os.path.dirname(MODELS_PATH), "backups")
    os.makedirs(bak_dir, exist_ok=True)
    bak = os.path.join(bak_dir, "models.json.bak-add-%s" % stamp)
    with open(MODELS_PATH, "r", encoding="utf-8") as src, \
            open(bak, "w", encoding="utf-8", newline="") as dst:
        dst.write(src.read())
    print("\n已备份 -> %s" % bak)

    normalized = [{k: m[k] for k in FIELD_ORDER if k in m} for m in before]
    with open(MODELS_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n")
    print("已追加条目 %s（能力位待探测后写入）" % entry["id"])


def pick_default_effort(usable, override=None, current=None):
    """挑默认档位。优先级：--default-effort > 现有配置里仍可用的档位 > medium/中位。

    关键：不要覆盖用户已有的 defaultEffort。上层调用会先把 current 传进来，
    只有当原值不在新档位列表里（服务端不再支持）时才重新挑。
    """
    if override:
        return override
    if current and current in usable:
        return current
    if not usable:
        return None
    if "medium" in usable:
        return "medium"
    return usable[len(usable) // 2]


def apply_results(results, entries, default_effort=None, force=False):
    """把探测结论写回 models.json。只改能力位，不碰 id/name/url/apiKey。"""
    clean = {k: v for k, v in results.items() if "error" not in v}
    if not clean:
        print("\n没有成功的探测结果，未改动配置。")
        return

    # 安全门槛一：全部探测都不完整时，拒绝写入（网络故障/限流会伪装成"全不支持"）
    all_partial = all(r.get("_partial") for r in clean.values())
    if all_partial and not force:
        print("\n⚠️ 所有模型的探测结果都不完整，很可能是网络/限流问题而非真实能力。")
        print("   为避免把已验证的能力位误降为 false，本次不写入。")
        print("   确认无误后可加 --force 强制写入。")
        return

    before = json.load(open(MODELS_PATH, encoding="utf-8"))
    changed = []

    for entry in entries:
        mid = entry.get("id")
        r = clean.get(mid)
        if not r:
            continue
        target = None
        for m in before:
            if m.get("id") == mid:
                target = m
                break
        if target is None:
            print("\n跳过 %s：不在 models.json 里（请先用 --add 加入条目）" % mid)
            continue

        eff = r.get("usable") or []
        new_reasoning = None
        if eff:
            # 保留用户已有的 defaultEffort（只要它还在新探测到的可用档位里）
            cur_eff = (target.get("reasoning") or {}).get("defaultEffort")
            new_reasoning = {
                "defaultEffort": pick_default_effort(eff, default_effort, cur_eff),
                "supportedEfforts": eff,
            }

        diffs = []
        for field in ("supportsImages", "supportsToolCall", "supportsReasoning"):
            val = r.get(field)
            if val is None:          # 该项没探测（如 --no-vision），保持原值
                continue
            # 关键防护：单个探测项失败/被跳过时，绝不能把已验证的 true 降级成 false。
            # 只有「探测明确说不支持」才允许置 false；探测异常时保持原值。
            if val is False and target.get(field) is True and r.get("_partial"):
                print("  ! %s.%s 探测不完整，保留原值 true（不降级）"
                      % (mid, field))
                continue
            if target.get(field) != val:
                diffs.append("%s: %s -> %s" % (field, target.get(field), val))
                target[field] = val
        if new_reasoning is not None and target.get("reasoning") != new_reasoning:
            diffs.append("reasoning: %s -> %s"
                         % (json.dumps(target.get("reasoning"), ensure_ascii=False),
                            json.dumps(new_reasoning, ensure_ascii=False)))
            target["reasoning"] = new_reasoning

        # 探测确认不支持推理时，必须清掉遗留的 reasoning 块，
        # 否则会留下「supportsReasoning=false 却带着档位」的自相矛盾配置。
        if (r.get("supportsReasoning") is False and not r.get("_partial")
                and target.get("reasoning") is not None):
            diffs.append("reasoning: %s -> （删除，不支持推理）"
                         % json.dumps(target["reasoning"], ensure_ascii=False))
            del target["reasoning"]

        changed.append((mid, diffs))

    # 字段顺序对齐，保持文件可读
    normalized = [{k: m[k] for k in FIELD_ORDER if k in m} for m in before]

    if not any(d for _, d in changed):
        print("\n配置已与探测结论一致，未改动文件。")
        return

    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak_dir = os.path.join(os.path.dirname(MODELS_PATH), "backups")
    os.makedirs(bak_dir, exist_ok=True)
    bak = os.path.join(bak_dir, "models.json.bak-probe-%s" % stamp)
    with open(MODELS_PATH, "r", encoding="utf-8") as src, \
            open(bak, "w", encoding="utf-8", newline="") as dst:
        dst.write(src.read())
    print("\n已备份 -> %s" % bak)

    with open(MODELS_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n")

    print("已写入 %s：\n" % MODELS_PATH)
    for mid, diffs in changed:
        if diffs:
            print("  %s" % mid)
            for d in diffs:
                print("      %s" % d)
        else:
            print("  %s  无变化" % mid)
    print("\n⚠️ 完全重启 WorkBuddy 后生效。")


if __name__ == "__main__":
    main()
