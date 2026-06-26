---
name: xungu-huangli
description: 循古黄历 - 获取中国万年历信息，包括二十四节气、农历日期、宜忌、吉凶、黄道吉日等。当用户询问节气、农历、日子好坏、宜忌、黄历相关问题时使用此技能。
metadata:
  {
    "openclaw":
      {
        "config":
          [
            {
              "key": "HUANGLI_API_TOKEN",
              "description": "循古黄历API Bearer Token (从 https://xungufa.com 获取)",
              "required": true,
            },
          ],
      },
  }
---

# 循古黄历

> 基于 [循古排盘](https://xungufa.com) 提供的老黄历查询服务

## 循古排盘介绍

[循古排盘](https://xungufa.com) 是一个提供传统黄历查询的在线工具，支持：

- **万年历查询**：公历/农历转换、二十四节气
- **每日宜忌**：吉凶宜忌、黄道吉日
- **干支历法**：年月日时四柱八字
- **月相/道历/佛历**：传统历法参考

适用于择日选吉、历法研究、传统文化应用等场景。

## 使用场景

当用户询问以下内容时使用：
- 二十四节气相关问题
- 农历日期
- 今日/某日宜忌
- 吉凶查询
- 黄道吉日
- 每日指南
- 干支历/月相/道历/佛历

## 数据来源

使用 API 获取万年历数据：
```
https://xungufa.com/huangli/api/calendar
```

**认证方式**：标准 Bearer Token 认证

Token 通过 OpenClaw 配置注入，键名 `HUANGLI_API_TOKEN`。

**重要规则：**
- **查询今天**：`https://xungufa.com/huangli/api/calendar` （**不加 date 参数**）
- **查询特定日期**：`https://xungufa.com/huangli/api/calendar?date=YYYY-MM-DD` （加 date 参数）

## 配置

首次使用前，需设置环境变量 `HUANGLI_API_TOKEN`：

**方法 1：.env 文件（推荐）**

在 OpenClaw 工作目录下创建或编辑 `.env` 文件：
```
HUANGLI_API_TOKEN=your_token_here
```

**方法 2：环境变量**
```bash
export HUANGLI_API_TOKEN="your_token_here"
```

**获取 Token**：访问 [xungufa.com](https://xungufa.com) 注册获取 API Token

## 返回格式

调用 API 后，用以下 Python 格式化输出（不要省略任何内容）：

```python
import json
import urllib.request

import os
from pathlib import Path

def _load_env():
    """从 .env 文件加载环境变量（如果尚未注入）"""
    if os.environ.get('HUANGLI_API_TOKEN'):
        return
    env_paths = [
        Path.home() / '.openclaw' / '.env',
        Path.cwd() / '.env',
    ]
    for p in env_paths:
        if p.exists():
            for line in p.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    k, v = k.strip(), v.strip()
                    if k and k not in os.environ:
                        os.environ[k] = v
            break

def get_calendar(date=None):
    _load_env()
    token = os.environ.get('HUANGLI_API_TOKEN')
    if not token:
        return '❌ 未配置 HUANGLI_API_TOKEN 环境变量，请在 ~/.openclaw/.env 中设置'
    url = "https://xungufa.com/huangli/api/calendar"
    if date:
        url += f"?date={date}"
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Mozilla/5.0'
    }
    req = urllib.request.Request(url, headers=headers)
    data = json.loads(urllib.request.urlopen(req).read())

    s = data['solar']
    l = data['lunar']
    g = data['ganzhi']
    h = data['huangli']
    tao = data['tao']
    buddha = data['buddha']

    # 干支格式：丙午 辛巳 甲申（不要年日月日）
    ganzhi = f"{g['year']} {g['month']} {g['day']}"

    # 道历：取年
    tao_year = tao.get('year_chinese', '')

    # 佛历：加"年"字
    buddha_year = f"{buddha.get('year_chinese', '')}年{buddha.get('month_chinese', '')}{buddha.get('day_chinese', '')}"

    result = f"""📅 今日黄历
───────────────────────────────────
公历: {s['date']} {s['week']} {s.get('xingzuo', '')}
农历: {l['date']}
干支: {ganzhi}
───────────────────────────────────
🟢 宜: {h['yi']}

🔴 忌: {h['ji']}

⏰ 吉时: {h['good_hours']}
🐲 冲煞: {h['chong_sha']}
🌙 月相: {l.get('yue_xiang', '')}
📿 道历: {tao_year}
☸️ 佛历: {buddha_year}"""

    if data.get('jieqi'):
        result += f"\n❄️ 节气: {data['jieqi']}"

    return result
```

**注意**：
1. Token 使用占位符 `<HUANGLI_API_TOKEN>`，实际调用时需替换为用户配置的真实 Token
2. 干支格式必须是 `丙午 辛巳 甲申`，不要带"年/月/日"字样
3. 宜忌等信息必须完整输出，不要用"..."省略

## 使用示例

用户问："今天日子好吗"
-> 调用 get_calendar() 返回格式化后的黄历

用户问："明天黄历"
-> 调用 get_calendar("2026-03-12") 返回次日黄历

## 输出格式要求（重要）

黄历输出必须包含以下完整字段，不得省略：

```
📅 今日黄历
───────────────────────────────────
公历: YYYY-MM-DD 星期X 星座
农历: 二〇XX年X月XX
干支: XX XX XX（年月日三柱，如：丙午 辛卯 丁亥）
───────────────────────────────────
🟢 宜: xxx, xxx, xxx

🔴 忌: xxx, xxx, xxx

⏰ 吉时: XX (HH:MM - HH:MM), XX (HH:MM - HH:MM)...
🐲 冲煞: 冲(xx)X 煞X
🌙 月相: xxx
📿 道历: xxxx
☸️ 佛历: xxxx年Xxxx
```

**特别注意：干支历（年月日三柱）必须完整输出**，不可省略。
