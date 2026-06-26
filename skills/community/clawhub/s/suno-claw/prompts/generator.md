# prompts/generator.md — Suno API 调用指南（kie.ai）

## API 基础信息

**Base URL：** `https://api.kie.ai`

**认证：**
```bash
Authorization: Bearer YOUR_API_KEY
```

**环境变量：**
```bash
KIEAI_API_KEY=your-key-here   # 从 https://kie.ai/api-key 获取
```

---

## 生成音乐 — `POST /api/v1/generate`

### 完整请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `prompt` | string | instrumental=false 时必填 | 歌词内容，Non-custom Mode 最大500字符；instrumental=true 时传空字符串 `""` |
| `style` | string | Custom Mode 必填 | 风格标签；Non-custom Mode 不填 |
| `title` | string | Custom Mode 必填 | 歌曲标题，最大80字；Non-custom Mode 不填 |
| `customMode` | boolean | 必填 | `true`=自定义模式；`false`=Non-custom Mode（**推荐，新用户从这开始**） |
| `instrumental` | boolean | 必填 | `true`=纯音乐，`false`=有人声 |
| `model` | string | 必填 | V4 / V4_5 / V4_5PLUS / V5 / V5_5 |
| `callBackUrl` | string | 必填 | 回调通知 URL，默认 `https://example.com/callback`，可通过 `CALLBACK_URL` 环境变量覆盖 |

### Non-custom Mode vs Custom Mode

**推荐使用 Non-custom Mode（`customMode: false`）**，参数最简：
- 仅 `prompt` 必填，其他参数可选
- V4/V4_5 prompt 最大500字符
- 系统自动生成歌词（instrumental=false 时）

**Custom Mode（`customMode: true`）**：
- instrumental=false：`prompt`（歌词）+ `style` + `title` 必填
- instrumental=true：`style` + `title` 必填
- V4: prompt≤3000字符，style≤200字符；V4.5+: prompt≤5000，style≤1000字符

### 模型选择

| 模型 | 特点 | 最大时长 |
|------|------|---------|
| `V4` | 基础版 | 4分钟 |
| `V4_5` | 更智能提示，更快生成 | 8分钟 |
| `V4_5PLUS` | 更丰富音色，更多创作方式 | 8分钟 |
| `V5` | superior musical expression | - |
| `V5_5` | 定制化模型，符合个人口味 | - |

**默认选择：`V5`**

---

## 查询任务 — `GET /api/v1/generate/record-info?taskId={taskId}`

**注意：不是 `/api/v1/task/{id}`，是 `/api/v1/generate/record-info?taskId=`**

### 响应结构

```json
{
  "code": 200,
  "data": {
    "status": "SUCCESS | FIRST_SUCCESS | TEXT_SUCCESS | PENDING | ... |",
    "response": {
      "sunoData": [
        {
          "audioUrl": "https://tempfile.aiquickdraw.com/r/xxx.mp3",
          "videoUrl": "N/A",
          "title": "歌曲标题"
        }
      ]
    }
  }
}
```

### 状态流转

```
PENDING
  ↓
TEXT_SUCCESS（歌词生成完成）
  ↓
FIRST_SUCCESS（第1个音频生成完成）
  ↓
SUCCESS（全部音频生成完成） ← 终止状态
```

**其他终止状态：**
| status | 含义 |
|--------|------|
| `SUCCESS` | 全部成功 |
| `CREATE_TASK_FAILED` | 任务创建失败 |
| `GENERATE_AUDIO_FAILED` | 音频生成失败 |
| `CALLBACK_EXCEPTION` | 回调处理异常 |
| `SENSITIVE_WORD_ERROR` | 内容敏感词过滤 |

---

## Python 调用示例

```python
import os, requests, time, json

API_KEY = os.environ.get("KIEAI_API_KEY")
# CALLBACK_URL: 设为空字符串则不传给 API; 留空则使用内部轮询
CALLBACK_URL = os.environ.get("CALLBACK_URL", "")
BASE = "https://api.kie.ai"

s = requests.Session()
s.headers.update({"Authorization": f"Bearer {API_KEY}"})
s.verify = True  # 始终验证 SSL 证书


def generate(prompt, instrumental=False, model="V4_5", callback_url=""):
    """
    Non-custom Mode 生成音乐
    prompt: 音乐描述（英文推荐，instrumental=true 时为音乐风格描述）
    callback_url: 回调地址；空字符串则不传给 API（推荐，默认用轮询）
    """
    payload = {
        "prompt": prompt,
        "customMode": False,
        "instrumental": instrumental,
        "model": model,
    }
    if callback_url:
        payload["callBackUrl"] = callback_url
    resp = s.post(f"{BASE}/api/v1/generate", json=payload, timeout=30)
    data = resp.json()
    if data.get("code") != 200:
        raise Exception(f"生成失败: {data.get('msg')}")
    return data["data"]["taskId"]


def check_task(task_id):
    """
    查询任务状态，返回 data 或 None（查询失败）
    """
    url = f"{BASE}/api/v1/generate/record-info?taskId={task_id}"
    resp = s.get(url, timeout=20)
    data = resp.json()
    if data.get("code") != 200:
        return None
    return data["data"]


def poll_task(task_id, timeout=300, interval=15):
    """
    轮询直到任务完成或失败
    返回: { status, songs: [{audioUrl, title}] }
    """
    end = time.time() + timeout
    while time.time() < end:
        result = check_task(task_id)
        if result is None:
            raise Exception("查询失败")
        status = result.get("status")
        if status in ("SUCCESS", "FIRST_SUCCESS"):
            songs = (result.get("response") or {}).get("sunoData") or []
            return {"status": status, "songs": songs}
        elif status in ("CREATE_TASK_FAILED", "GENERATE_AUDIO_FAILED",
                       "CALLBACK_EXCEPTION", "SENSITIVE_WORD_ERROR"):
            em = result.get("errorMessage") or ""
            raise Exception(f"生成失败 [{status}]: {em}")
        # PENDING / TEXT_SUCCESS: 继续轮询
        time.sleep(interval)
    raise TimeoutError(f"任务 {task_id} 轮询超时")


def generate_and_wait(prompt, instrumental=False, model="V5"):
    """一步到位：生成 + 轮询"""
    task_id = generate(prompt, instrumental, model)
    result = poll_task(task_id)
    return result
```

---

## 使用示例

### Non-custom Mode — 纯音乐

```python
result = generate_and_wait(
    prompt="A calm and relaxing piano track with soft melodies",
    instrumental=True
)
for song in result["songs"]:
    print(f"🎵 {song['title']}: {song['audioUrl']}")
```

### Non-custom Mode — 有歌词（英文）

```python
result = generate_and_wait(
    prompt="An upbeat K-pop song about breaking free",
    instrumental=False
)
```

### Custom Mode — 有歌词 + 风格标签

```python
result = generate_and_wait(
    prompt="[Verse 1]\nWalking through the night\n[Chorus]\nThis is my moment",
    instrumental=False
)
# Custom Mode 需要 style 和 title 时：
payload = {
    "prompt": "...",
    "style": "pop, female vocals, upbeat, synth",
    "title": "My Song",
    "customMode": True,
    "instrumental": False,
    "model": "V5",
    # "callBackUrl": "你的回调地址"  # 空字符串或不传则使用内部轮询
}
```

---

## 渐进生成流程

```python
def progressive_generate(suno_prompts: list, is_instrumental: bool = False):
    """
    suno_prompts: 3个封包后的 prompt 对象（按 relevance 1.0→0.7→0.5 排序）
    is_instrumental: 是否纯音乐

    每步完成后暂停，返回结果给主代理展示给用户，
    等待用户确认后再跑下一步（节约 API 用量）
    """
    for i, p in enumerate(suno_prompts):
        print(f"\n[Step {i+1}/3] Relevance: {p.get('relevance')} ...")

        # 生成 + 轮询
        result = generate_and_wait(
            prompt=p["lyrics"] if not is_instrumental else p["style_tags"],
            instrumental=is_instrumental
        )

        songs = result["songs"]
        audio_url = songs[0]["audioUrl"] if songs else ""

        yield {
            "version": i + 1,
            "relevance": p.get("relevance"),
            "audio_url": audio_url,
            "title": songs[0].get("title") if songs else "",
            "lyrics": p.get("lyrics", ""),
            "style_tags": p.get("style_tags", ""),
            "theme_summary": p.get("theme_summary", "")
        }
        # 【暂停】等待用户反馈
```

---

## 错误处理

| 错误 | 原因 | 处理方式 |
|------|------|---------|
| `code=422` | 参数缺失（如 callBackUrl 为空） | 确保所有必填字段 |
| `code=401` | API Key 无效 | 检查 `KIEAI_API_KEY` |
| `429` | 超速限制 | 等待后重试 |
| 查询返回 404 | taskId 不存在或已过期 | 重新提交生成任务 |
| `SENSITIVE_WORD_ERROR` | 内容含敏感词 | 更换 prompt |
| `CREATE_TASK_FAILED` | 任务创建失败 | 更换 prompt 或模型 |
| SSL EOF Error | 代理/防火墙拦截 | 关闭代理或配置系统证书链 |
