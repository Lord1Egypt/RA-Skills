# xhscosmoskill — 小红书数据抓取工具

> Agent 可直接调用的小红书内容抓取客户端。
> 基于 SeleniumBase UC Mode + XHR 拦截，绕过反爬检测，无需逆向签名算法。

---

## 核心原理

```
用户登录一次 → 保存 Cookie
↓
SeleniumBase UC Mode 打开浏览器（绕过 headless 检测）
↓
注入 JS 拦截器（劫持 fetch/XHR）
↓
浏览器自动带签名请求小红书 API
↓
拦截器捕获 API 响应 JSON → 返回结构化数据
```

不需要逆向 X-s/X-t 签名，因为我们让浏览器自己完成签名，然后从内存中读取响应。

---

## 前置步骤（只需一次）

```bash
# 1. 安装依赖
pip install seleniumbase

# 2. 登录小红书，保存 cookie
cd /Users/zezedabaobei/Desktop/cosmocloud/Deeplumen/cosmowork/xiaohongshu_new
python3 xhs_login.py
# → 浏览器弹出，手动登录，按 Enter 保存
# → 生成 xhs_cookies.json（有效期约 30 天）
```

---

## 快速使用

```python
import sys
sys.path.insert(0, "/Users/zezedabaobei/Desktop/cosmocloud/Deeplumen/cosmowork/xiaohongshu_new")

from xhscosmoskill import XhsClient

with XhsClient() as xhs:
    # 搜索关键词
    notes = xhs.search("咖啡", limit=20)

    # 获取用户所有笔记
    notes = xhs.get_user_notes("USER_ID_HEX_HERE", limit=50)

    # 获取单篇详情（正文 + 评论）
    note = xhs.get_note_detail("https://www.xiaohongshu.com/explore/xxx")

    # 批量补充详情
    notes = xhs.batch_get_details(notes, delay=2.0)

    # 保存
    xhs.save(notes, "output.json")
```

---

## API 文档

### `XhsClient(cookies_file, headless, scroll_times)`

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| cookies_file | str | `../xhs_cookies.json` | Cookie 文件路径 |
| headless | bool | False | 无头模式（稳定后可开启） |
| scroll_times | int | 5 | 默认滚动次数（影响加载量） |

---

### `xhs.search(keyword, limit, scroll_times) → List[Note]`

搜索笔记。

```python
notes = xhs.search("咖啡", limit=30)
# notes[0].title, notes[0].likes, notes[0].url, notes[0].type
```

---

### `xhs.get_user_notes(user_id, limit, scroll_times) → List[Note]`

获取用户主页所有笔记。`user_id` 是 URL 中的 hex 字符串。

```python
# URL: xiaohongshu.com/user/profile/USER_ID_HEX_HERE
notes = xhs.get_user_notes("USER_ID_HEX_HERE", limit=100)
```

---

### `xhs.get_note_detail(note_url) → Note | None`

获取单篇笔记详情，包含正文、评论、互动数据。

```python
note = xhs.get_note_detail("https://www.xiaohongshu.com/explore/xxx")
print(note.content)   # 正文全文
print(note.comments)  # List[Comment]
```

---

### `xhs.batch_get_details(notes, delay) → List[Note]`

在搜索/列表结果基础上批量补充正文和评论。

```python
notes = xhs.search("咖啡", limit=20)
notes = xhs.batch_get_details(notes, delay=2.0)  # delay 建议 1.5~3 秒
```

---

### `xhs.save(notes, filepath)`

保存为 JSON 文件。

---

## 数据模型

### `Note`
```
id            str   笔记 ID
title         str   标题
content       str   正文全文
url           str   完整 URL
author        str   作者昵称
author_id     str   作者 ID
likes         str   点赞数（字符串，如 "3万"）
collects      str   收藏数
comments_count str  评论数
type          str   "video" | "normal"
images        list  图片 URL 列表
tags          list  话题标签列表
comments      list  List[Comment]
```

### `Comment`
```
user    str   评论者昵称
text    str   评论内容
likes   str   评论点赞数
time    str   评论时间
```

---

## 稳定性说明

| 场景 | 稳定性 | 说明 |
|------|--------|------|
| 搜索列表 | ✅ 稳定 | DOM 兜底，基本必成 |
| 用户主页列表 | ✅ 稳定 | 同上 |
| 笔记详情正文 | ⚠️ 较好 | API 拦截优先，DOM 兜底 |
| 评论数据 | ⚠️ 较好 | 依赖 API 拦截成功 |

- Cookie 有效期约 30 天，过期后重跑 `xhs_login.py`
- 建议单账号每次请求间隔 1.5 秒以上，避免风控
- 首次使用建议 `headless=False` 观察浏览器行为

---

## 文件结构

```
xhscosmoskill/
├── __init__.py       入口，导出 XhsClient
├── client.py         主客户端类（对外 API）
├── browser.py        浏览器会话 + XHR 拦截器
├── parser.py         API JSON / DOM 解析器
├── models.py         数据模型（Note / Comment / UserProfile）
├── README.md         本文件
└── examples/
    ├── search_notes.py    搜索示例
    ├── user_profile.py    用户主页示例
    └── note_detail.py     单篇详情示例
```

---

## 常见问题

**Q: `Cookie 文件不存在` 报错**
A: 运行 `python3 xhs_login.py` 先登录一次。

**Q: content 字段为空**
A: 该笔记的详情页 API 未被拦截到。可尝试增加 `wait` 时间，或该笔记需要登录才可见。

**Q: 运行很慢**
A: 正常，每次操作需要等待页面渲染。可在稳定后开启 `headless=True`。

**Q: 被封号怎么办**
A: 降低频率（`delay=3`），换账号重新 `xhs_login.py`。
