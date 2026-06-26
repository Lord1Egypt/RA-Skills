---
name: "qsnctf-practice-dynamic"
version: "1.0.0"
description: "获取青少年CTF练习场的排行榜和解题动态。Invoke when user wants to check QSNCTF leaderboard or recent solve activities."
triggers:
  - "qsnctf-practice-dynamic"
  - "qsnctf leaderboard"
  - "qsnctf dynamic"
---

# 青少年CTF练习场动态查询

本技能用于获取青少年CTF练习场(www.qsnctf.com)的排行榜和解题动态信息。

## 功能说明

### 1. 排行榜查询
获取当前排行榜前20名用户信息，包括：
- 排名
- 用户名
- 积分
- 等级

```bash
python scripts/qsnctf_stats.py ranking
```

### 2. 解题动态查询
获取近期的解题动态，包括：
- 用户名
- 题目类别
- 解题时间

```bash
python scripts/qsnctf_stats.py dynamic
```


## 使用方法

### 命令格式

```bash
python scripts/qsnctf_stats.py <action> [options]
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `action` | 必填，可选值: `ranking`, `dynamic`, `all` |
| `-n, --number` | 可选，获取解题动态的数量(默认10条，0表示全部) |

### Action 说明

| Action | 功能 |
|--------|------|
| `ranking` | 获取排行榜TOP 20 |
| `dynamic` | 获取近期解题动态 |
| `all` | 同时获取排行榜和解题动态 |

## 使用示例

### 获取排行榜
```bash
python scripts/qsnctf_stats.py ranking
```

### 获取最近10条解题动态
```bash
python scripts/qsnctf_stats.py dynamic
```

### 获取最近20条解题动态
```bash
python scripts/qsnctf_stats.py dynamic -n 20
```

### 获取全部解题动态
```bash
python scripts/qsnctf_stats.py dynamic -n 0
```

### 同时获取排行榜和解题动态
```bash
python scripts/qsnctf_stats.py all
```

## 输出示例

### 排行榜输出
```
======================================================================
青少年CTF练习场 - 排行榜 TOP 20
======================================================================
排名     用户名                     积分        等级
----------------------------------------------------------------------
1       substkiller               892.0      Lv.2
2       huasan2508                836.0      Lv.2
3       qingquan12                627.0      Lv.2
...
======================================================================
```

### 解题动态输出
```
============================================================
青少年CTF练习场 - 近期解题动态
============================================================
用户名                题目类别                    时间
------------------------------------------------------------
zzawa                Base64                     2026-03-22 01:39:01
fenfenkaihuai        应急行动-1                  2026-03-21 23:45:51
...
============================================================
```

## 依赖

- Python 3.x
- requests 库

安装依赖：
```bash
pip install requests
```

## API 说明

本技能调用以下API：
- 排行榜: `GET https://www.qsnctf.com/api/5dboard/playlist`
- 解题动态: `GET https://www.qsnctf.com/api/5dboard/viewlist`
