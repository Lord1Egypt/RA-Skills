# FlyAI MCP集成配置报告

## 配置时间
2026-04-12 05:58-06:06

## 安装步骤

### 1. Skill安装
```bash
clawhub install flyai
# 结果: ✅ 成功 -> /home/admin/.openclaw/workspace/skills/flyai/
```

### 2. CLI安装
```bash
npm i @fly-ai/flyai-cli
# 结果: ✅ 成功 -> node_modules/@fly-ai/flyai-cli/
```

### 3. 调用方式
```bash
cd /home/admin/.openclaw/workspace
npx @fly-ai/flyai-cli search-flight --origin "北京" --destination "兰州" --dep-date "2026-05-01"
```

## 验证结果

| 命令 | 测试结果 | 返回数据 |
|------|----------|----------|
| search-flight | ✅ 成功 | 真实航班票价（¥1050-¥2390） |
| search-train | ✅ 成功 | 真实火车票价（¥189.5-¥608） |
| keyword-search | ✅ 成功 | 旅游产品搜索 |

## 返回数据格式

### 航班数据结构
```json
{
  "data": {
    "itemList": [{
      "journeys": [{
        "journeyType": "直达",
        "segments": [{
          "depCityName": "北京",
          "depStationName": "首都国际机场",
          "depDateTime": "2026-05-01 20:40:00",
          "arrCityName": "兰州",
          "arrStationName": "中川机场",
          "arrDateTime": "2026-05-01 23:05:00",
          "marketingTransportName": "海南航空",
          "marketingTransportNo": "HU7297",
          "seatClassName": "经济舱",
          "duration": "145"
        }],
        "totalDuration": "145"
      }],
      "jumpUrl": "https://a.feizhu.com/2odQgM",
      "ticketPrice": "1050.00"
    }]
  },
  "message": "success",
  "status": 0
}
```

### 火车数据结构
```json
{
  "data": {
    "itemList": [{
      "journeys": [{
        "journeyType": "直达",
        "segments": [{
          "depCityName": "北京",
          "depStationName": "北京西站",
          "depDateTime": "2026-05-01 19:49:00",
          "arrCityName": "兰州",
          "arrStationName": "兰州站",
          "arrDateTime": "2026-05-02 12:19:00",
          "marketingTransportName": "普快",
          "marketingTransportNo": "Z21",
          "seatClassName": "硬座"
        }],
        "totalDuration": "990"
      }],
      "jumpUrl": "https://a.feizhu.com/0GRuX2",
      "price": "189.50"
    }]
  },
  "message": "success",
  "status": 0
}
```

## 集成方案

### 后端调用
```python
import subprocess
import json

def call_flyai_flight(origin, destination, date):
    cmd = f'npx @fly-ai/flyai-cli search-flight --origin "{origin}" --destination "{destination}" --dep-date "{date}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='/home/admin/.openclaw/workspace')
    if result.returncode == 0:
        return json.loads(result.stdout)
    return None

def call_flyai_train(origin, destination, date):
    cmd = f'npx @fly-ai/flyai-cli search-train --origin "{origin}" --destination "{destination}" --dep-date "{date}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='/home/admin/.openclaw/workspace')
    if result.returncode == 0:
        return json.loads(result.stdout)
    return None
```

### 前端显示
- 表格展示航班/火车选项
- 真实票价高亮显示
- 预订链接可点击

## 永久规则

| 规则 | 说明 |
|------|------|
| P0原则 | 先查系统资源，再网上搜索skill+mcp |
| 禁止模拟 | 所有票价数据必须FlyAI真实调用 |
| 实话实说 | API不存在就实话实说 |
| 真实预订 | 预订链接必须飞猪真实链接 |

## 文件位置

| 文件 | 位置 |
|------|------|
| FlyAI Skill | /home/admin/.openclaw/workspace/skills/flyai/ |
| FlyAI CLI | /home/admin/.openclaw/workspace/node_modules/@fly-ai/flyai-cli/ |
| SKILL.md | /home/admin/.openclaw/workspace/skills/flyai/SKILL.md |
| references | /home/admin/.openclaw/workspace/skills/flyai/references/*.md |

## 下一步

1. 集成到7860端口后端
2. 更新前端UI显示真实票价
3. 修复之前BUG（歧义检测等）
4. 启动测试