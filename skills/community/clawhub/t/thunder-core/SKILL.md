---
name: thunder-core
description: Windows Thunder download client via COM interface — add, commit, cancel, and manage download tasks programmatically.
version: 1.0.0
tags:
  - download
  - thunder
  - xunlei
  - windows
  - com
  - automation
category: "Automation"
os:
  - windows
metadata:
  openclaw:
    requires:
      bins:
        - python
    emoji: ⚡
---

# Thunder Download Core

Control the [Thunder (迅雷)](https://www.xunlei.com/) download engine on Windows via COM interface. Add download tasks, set custom headers (Referer, User-Agent, Cookie), commit tasks, cancel all, and query task list.

**Prerequisites**: Windows OS with Thunder client installed. Python packages: `pywin32` (`pip install pywin32`).

## Quick Start

```python
from thunder_core import ThunderCore, download

# Quick one-shot download
download("https://example.com/file.zip", "C:\\Downloads\\file.zip")

# Full control
tc = ThunderCore()
if tc.initialize():
    tc.add_task("https://example.com/file.zip", "C:\\Downloads\\file.zip",
                refer_url="https://example.com",
                user_agent="Mozilla/5.0")
    tc.commit_tasks()
    tasks = tc.get_tasks()
    tc.close()
```

## API

### ThunderCore

| Method | Description |
|--------|-------------|
| `initialize()` | Initialize Thunder COM component |
| `add_task(url, save_path, ...)` | Add a download task with custom headers |
| `commit_tasks()` | Submit all queued tasks |
| `add_and_commit(url, save_path, ...)` | Add task and immediately commit |
| `cancel_all()` | Cancel all active tasks |
| `get_tasks()` | Get current task list |
| `close()` | Release COM resources |

### Utility

| Function | Description |
|----------|-------------|
| `download(url, save_path, ...)` | Convenience: create, add, commit in one call |

## Notes

- Windows-only (uses COM interface `ThunderAgent.ThunderAgent`)
- Thunder must be installed at default path or custom `_install_path`
- Run as administrator if COM registration fails

## Source

`thunder_core.py` (155 lines) in this skill directory.

## 触发场景
- 用户说"下载"、"迅雷下载"、"加下载任务"
- 用户说"迅雷"、"thunder"、"xunlei"
- 用户说"管理下载"、"查看下载进度"


## B站学习
> 学习时间: 2026-06-01 20:58

- **大明子1014**: 【大明子】地心护核者CORE KEEPER 第四BOSS天空泰坦埃齐欧斯讨伐攻略！！！【手残党福音】
  - 关键词: 大明子, 地心护核者CORE, KEEPER, 第四BOSS天空泰坦埃齐欧斯讨伐攻略, 手残党福音
- **AhiruMochi**: 【搬運】DJ Myosuke - Joe Thunder 原版MV
  - 关键词: 搬運, DJ, Myosuke, Joe, Thunder

## B站学习
> 学习时间: 2026-06-01 21:02

- **大明子1014**: 【大明子】地心护核者CORE KEEPER 第四BOSS天空泰坦埃齐欧斯讨伐攻略！！！【手残党福音】
- **AhiruMochi**: 【搬運】DJ Myosuke - Joe Thunder 原版MV
- **台绒-_-**: Dream-Core&amp;连接 实机预告

## B站学习 (第1轮)
> 学习时间: 2026-06-02 09:22

- **健身让我勇敢**: 2026年二季度lesmills莱美core核心提升62期
  https://www.bilibili.com/video/BV1kRVn6AEwb
- **AhiruMochi**: 【搬運】DJ Myosuke - Joe Thunder 原版MV
  https://www.bilibili.com/video/BV1pN411G7tm
- **台绒-_-**: Dream-Core&amp;连接 实机预告
  https://www.bilibili.com/video/BV1tnVJ6qEK2

## B站学习 (第2轮)
> 学习时间: 2026-06-02 09:35

- **健身让我勇敢**: 2026年二季度lesmills莱美core核心提升62期
  https://www.bilibili.com/video/BV1kRVn6AEwb
- **AhiruMochi**: 【搬運】DJ Myosuke - Joe Thunder 原版MV
  https://www.bilibili.com/video/BV1pN411G7tm
- **台绒-_-**: Dream-Core&amp;连接 实机预告
  https://www.bilibili.com/video/BV1tnVJ6qEK2
