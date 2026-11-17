---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: 'b6368f92-6dc8-41a7-a16d-c4e9a8df4e9e'
  PropagateID: 'b6368f92-6dc8-41a7-a16d-c4e9a8df4e9e'
  ReservedCode1: '81c206f6-337e-4d68-8fc2-d6a127b0f355'
  ReservedCode2: '81c206f6-337e-4d68-8fc2-d6a127b0f355'
---

# Playwright 浏览器自动化：智学云字幕提取实战指南

## 适用场景

用于智学云 (zhixueyun.com) 等需要登录的在线学习平台。基于实战验证的 V12 成功方案。

## 核心策略：API 路由拦截

**关键经验**：不要在页面加载后用 `page.evaluate()` + `fetch` 调用 API（会丢失 session token 导致 401）。正确做法是在页面加载过程中用 `page.on("response")` 拦截自然触发的 API 响应。

## 完整工作流

### 第1步：启动浏览器（非 headless）

```python
import asyncio, json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--autoplay-policy=no-user-gesture-required"],
        )
        context = await browser.new_context()
        page = await context.new_page()
        # ... 后续步骤
```

### 第2步：设置 API 响应拦截器（在导航前）

```python
captured = {}

async def on_response(response):
    url = response.url
    try:
        if "course-info/front/find-by-ids" in url:
            captured["find_by_ids"] = await response.json()
        elif "course-info/front/find-by-id" in url and "find-by-ids" not in url:
            captured["course_info"] = await response.json()
        elif "guide-study/get-guide-study-info" in url:
            captured["guide_study_info"] = await response.json()
        elif "guide-study/get-guide-record" in url:
            captured["guide_record"] = await response.json()
    except:
        pass

page.on("response", on_response)
```

### 第3步：导航并等待用户登录

用户提供的短链（如 `detailInfo5748`）通常无效。两种处理方式：

```python
# 方式A：已知 UUID，直接导航
course_uuid = "7e98894b-..."
await page.goto(f"https://kc.zhixueyun.com/#/study/course/detail/{course_uuid}")

# 方式B：未知 UUID，先导航到首页拦截 find-by-ids API 解析 UUID
await page.goto("https://kc.zhixueyun.com/#/home-v")

# 等待用户手动登录（检测登录状态）
print("请在浏览器窗口中完成登录...")
# 轮询检查 localStorage token
while True:
    token_raw = await page.evaluate("localStorage.getItem('token')")
    if token_raw and "access_token" in token_raw:
        break
    await asyncio.sleep(2)
```

### 第4步：导航到课程详情页（触发关键 API）

```python
# 用 UUID 导航到课程详情页，API 会自动触发
course_uuid = captured.get("find_by_ids", {}).get("data", [{}])[0].get("id", course_uuid)
await page.goto(f"https://kc.zhixueyun.com/#/study/course/detail/{course_uuid}")

# 等待关键 API 数据到达
await page.wait_for_timeout(10000)  # 等待 API 响应完成
```

### 第5步：提取 DOM 字幕文本

```python
# 从页面 DOM 提取字幕文本（带时间戳）
body_text = await page.evaluate("document.body.innerText")

# 也可提取 video 元素信息
videos = await page.evaluate("""
    () => Array.from(document.querySelectorAll('video')).map(v => ({
        src: v.src,
        duration: v.duration,
        tracks: Array.from(v.textTracks).map(t => ({kind: t.kind, mode: t.mode, label: t.label}))
    }))
""")
```

### 第6步：Token 处理

```python
# localStorage token 是 JSON 字符串，需解析
token_raw = await page.evaluate("localStorage.getItem('token')")
if token_raw:
    token_data = json.loads(token_raw)
    access_token = token_data.get("access_token", "")
    # 如需用 token 调用 API：Authorization: Bearer {access_token}
```

### 第7步：保存提取的数据

```python
import json
from pathlib import Path

output = {
    "url": page.url,
    "body_text": body_text,
    "videos": videos,
    "guide_study_data": captured.get("guide_study_info", {}).get("data", []),
    "course_info_data": captured.get("course_info", {}).get("data", {}),
    "guide_record_data": captured.get("guide_record", {}).get("data", {}),
    "captured_apis": list(captured.keys()),
}

Path("output.json").write_text(
    json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
)
```

## 已验证的 API 端点

| API 端点 | 触发时机 | 用途 |
|---|---|---|
| `/api/v1/course-study/course-info/front/find-by-ids` | 首页加载 | 解析短链ID为课程UUID |
| `/api/v1/course-study/course-info/front/find-by-id?courseId={UUID}` | 课程详情页加载 | 课程元数据（名称/讲师/章节/时长） |
| `/api/v1/course-study/guide-study/get-guide-study-info` | 课程详情页加载 | **主要数据源**：20条AI知识点摘要（带毫秒时间戳） |
| `/api/v1/course-study/guide-study/get-guide-record` | 课程详情页加载 | 指导记录（含fileId） |

## 关键注意事项

1. **短链无效**：`detailInfo5748` 等短链 ID 无法直接导航，必须通过 `find-by-ids` API 解析出 UUID
2. **API 拦截时机**：必须在 `page.goto()` 之前设置 `page.on("response")`，否则会错过页面加载时自然触发的 API
3. **Token 401 问题**：页面加载后用 `fetch` 调用 API 会丢失 session（V11 实战验证），必须用 API 拦截方式
4. **Token 格式**：localStorage `token` 为 JSON 字串 `{"access_token":"...","token_type":"Bearer"}`，需 `JSON.parse()` 后使用
5. **视频源**：HLS m3u8 通过 blob URL 提供，不可直接下载
6. **页面路由**：Hash 路由 `/#/...`，导航时需包含完整 hash

## 完整脚本

`scripts/zhixueyun_extractor.py` 提供了完整的可执行脚本，封装了上述所有步骤。