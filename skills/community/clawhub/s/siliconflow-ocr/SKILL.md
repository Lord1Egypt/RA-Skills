---
name: siliconflow-ocr
description: 使用 SiliconFlow API（OpenAI 兼容接口）做图片/PDF 文字识别。默认走 PaddleOCR-VL-1.5（文档 OCR SOTA，速度比 Qwen3-VL 快 40%、表格公式更强）。支持本地路径或 URL、单页/批量并发、坐标 token 清洗。密钥通过 OpenClaw secret-egress-proxy 注入，需保留 `requests`+网关 proxy。
---

# SiliconFlow OCR 技能

## 环境变量

`SILICONFLOW_API_KEY` 由 OpenClaw gateway 注入（sentinel token），本地调 outbound API 时**必须**走 `requests`+gateway proxy——不要用 `urllib.request.ProxyHandler({})` 旁路，否则 sentinel 不被替换、upstream 返回 401。

## 单页 OCR

```python
import os, base64, re, requests

LOC_RE = re.compile(r"<\|LOC_\d+\|>")

def ocr_image(
    image_path: str = None,
    image_url: str = None,
    api_key: str = None,
    model: str = "PaddlePaddle/PaddleOCR-VL-1.5",
    timeout: int = 180,
) -> str:
    """单页 OCR。返回清洗过坐标 token 的纯文本。"""
    api_key = api_key or os.environ["SILICONFLOW_API_KEY"]

    if image_path:
        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("ascii")
        img_data = f"data:image/png;base64,{img_b64}"
    else:
        img_data = image_url

    payload = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "请逐字识别图片中所有文字内容,包括正文、表格、公式、脚注。按原文输出,不要总结,不要省略,标点和换行尽量保留原版式。"},
                {"type": "image_url", "image_url": {"url": img_data}},
            ],
        }],
        "temperature": 0.1,
        "max_tokens": 8000,
    }
    resp = requests.post(
        "https://api.siliconflow.cn/v1/chat/completions",
        json=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        timeout=timeout,
    )
    resp.raise_for_status()
    raw = resp.json()["choices"][0]["message"]["content"]
    return LOC_RE.sub("", raw).strip()
```

## 批量并发 + 重试

`ThreadPoolExecutor` 跑多页 PDF。SiliconFlow 对并发敏感：8 路会撞 rate limit（timeout 失败率 >60%），**默认 4 路**稳定。

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import json, time

def ocr_one(api_key, page_num, image_bytes, max_attempts=3, timeout=180):
    last_err = None
    t0 = time.time()
    for attempt in range(1, max_attempts + 1):
        try:
            text = ocr_image_bytes(api_key, image_bytes, timeout=timeout)
            return {"page": page_num, "ok": True, "chars": len(text),
                    "seconds": round(time.time()-t0, 2), "attempt": attempt}
        except Exception as e:
            last_err = str(e)
            time.sleep(2 * attempt)
    return {"page": page_num, "ok": False, "error": last_err,
            "seconds": round(time.time()-t0, 2)}

# todo: list[int]，pages: list[bytes]（已渲染好的 PNG）
with ThreadPoolExecutor(max_workers=4) as exe:
    futures = {exe.submit(ocr_one, api_key, p, pages[p-1]): p for p in todo}
    for fut in as_completed(futures):
        rec = fut.result()
        # 写 progress.jsonl 增量落盘，崩了不丢成果
```

## PDF 多页

PDF 用 `pymupdf` 渲成 2x PNG 再喂 API：

```python
import pymupdf

def render_page(pdf_path, page_num_1based, zoom=2.0):
    doc = pymupdf.open(pdf_path)
    try:
        page = doc[page_num_1based - 1]
        return page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False).tobytes("png")
    finally:
        doc.close()
```

`pymupdf` 在 base 环境已经装过。

## 模型选择

| 模型 | 单页 | 4 路并发 | 文档 OCR | 备注 |
|---|---|---|---|---|
| `PaddlePaddle/PaddleOCR-VL-1.5` | ~80-110s | 稳定 0 fail | **SOTA (OmniDocBench 96.87)** | **首选**——表格、公式、术语表 |
| `Qwen/Qwen3-VL-8B-Instruct` | ~130s | 高 fail 撞限流 | 一般 89.0 | 通用 VLM，看图说话 OK |
| `deepseek-ai/DeepSeek-OCR` | 波动大 | 不稳定 | — | 慎用 |

**何时选 Qwen-VL**：图里有自然场景 + 文字混合（路牌、产品图），需要 VLM 通用理解。
**何时选 PaddleOCR-VL**：印刷体文档、表格、公式、密集中英文术语——所有"扫书"场景。

## 错误处理

- **超时（默认 180s）**：单页偶发，重试 3 次（指数 backoff）即可
- **407 Proxy Auth**：OpenClaw secret proxy 认证失败，检查 `HTTPS_PROXY`/`HTTP_PROXY` 是否被脚本意外清掉
- **401 Unauthorized**：用了 `urllib.request.ProxyHandler({})` 旁路了 proxy，sentinel 没替换。改回 `requests` 走默认 proxy
- **识别为空**：先看 raw 输出有没有 `<|LOC_xxx|>`（已清洗）或其他奇怪结构，调 prompt 重试