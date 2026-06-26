---
name: task-director
description: Task Director — turn complex tasks into movie storyboards. Create a plan, review it, then execute step by step with fallback support. Pause, retry, skip anytime.
tags:
  - automation
  - planning
  - workflow
  - agent
requires:
  bins:
    - python
  env: []
---

# 任务导演 / Task Director

把复杂任务编排成电影剧本。**先看分镜，确认后再开机。**

No more "run and pray". Plan first, execute with confidence.

## 核心理念

普通 Agent 的工作方式：
```
用户：部署这个项目
Agent：冲！（5分钟后报错）啊... 从头再来...
```

用任务导演的 Agent：
```
用户：部署这个项目
Agent：我给你写了个分镜，你看看？
  🎬 第一幕：环境检查（预计 30s）
  🎬 第二幕：安装依赖（预计 2min）
  🎬 第三幕：构建部署（预计 5min）
     🎭 备选：先本地测试
  🎬 杀青：验证服务能访问
用户：第三幕的备选方案换成本地构建
Agent：好的，改了。开机？
用户：开机！
Agent：🎬 Action! 第一幕...
```

## 命令参考

DIRECTOR = python <skill_dir>/scripts/director.py

### 创建剧本

```bash
$DIRECTOR create --title "部署全栈项目" --scenes scenes.json
```

scenes.json 格式：
```json
[
  {
    "name": "环境准备",
    "description": "检查并配置运行环境",
    "estimated_time": "1 min",
    "shots": [
      {
        "action": "检查 Node.js 版本",
        "command": "node --version"
      },
      {
        "action": "安装项目依赖",
        "command": "npm install",
        "fallback": {
          "action": "使用 yarn 安装",
          "command": "yarn install"
        }
      }
    ]
  },
  {
    "name": "构建部署",
    "shots": [
      {
        "action": "执行构建",
        "command": "npm run build"
      }
    ]
  }
]
```

**Shot 的字段：**
- `action` (必填): 要做什么
- `command` (可选): 具体命令
- `fallback` (可选): 失败后的备选方案

### 查看剧本

```bash
$DIRECTOR show              # 显示当前活跃的剧本
$DIRECTOR show --id movie_xxx  # 按 ID 查看
```

### 批准剧本

```bash
$DIRECTOR approve
```

状态从 `draft` → `approved`，可以开始执行了。

### 开机拍摄（执行下一步）

```bash
$DIRECTOR action
```

输出下一个待执行的 shot 信息（JSON 格式），Agent 根据这个信息去实际执行。

指定某一幕某个镜头：
```bash
$DIRECTOR action --scene 2 --shot 1
```

### 记录结果

Agent 执行完后，回报结果：

```bash
# 成功
$DIRECTOR result --id movie_xxx --outcome done --output "v18.0.0"

# 失败
$DIRECTOR result --id movie_xxx --outcome ng --output "npm ERR! code ERESOLVE"

# 用备选方案成功
$DIRECTOR result --id movie_xxx --outcome done --fallback --output "yarn install success"
```

### 暂停 / 继续

```bash
$DIRECTOR cut     # 暂停（导演喊卡）
$DIRECTOR action  # 继续拍摄
```

### 跳过镜头

```bash
$DIRECTOR skip --scene 1 --shot 3 --reason "不需要这一步"
```

### 杀青

```bash
$DIRECTOR wrap
```

显示最终统计：耗时、完成率、失败数。

### 查看所有剧本

```bash
$DIRECTOR list
```

## Agent 工作流

### 创建剧本（Agent 自动生成）

```python
import json

scenes = [
    {
        "name": "环境检查",
        "estimated_time": "30s",
        "shots": [
            {"action": "检查 Python 版本", "command": "python --version"},
            {"action": "检查依赖是否安装", "command": "pip list | grep flask"},
        ]
    },
    {
        "name": "启动服务",
        "estimated_time": "10s",
        "shots": [
            {
                "action": "启动 Flask 服务",
                "command": "python app.py",
                "fallback": {
                    "action": "使用 gunicorn 启动",
                    "command": "gunicorn app:app"
                }
            },
        ]
    },
    {
        "name": "验证",
        "estimated_time": "5s",
        "shots": [
            {"action": "检查端口是否监听", "command": "curl http://localhost:5000/health"},
        ]
    },
]

with open("scenes.json", "w") as f:
    json.dump(scenes, f, ensure_ascii=False, indent=2)
```

### 执行循环

```
1. $DIRECTOR action          → 获取下一个 shot
2. Agent 执行 shot 中的 command
3. $DIRECTOR result --id xxx --outcome done --output "..."  → 记录结果
4. 如果有下一个，回到步骤 1
5. 全部完成后 $DIRECTOR wrap  → 杀青
```

### 失败处理

```
1. $DIRECTOR action          → 获取 shot
2. Agent 执行，失败了
3. $DIRECTOR result --id xxx --outcome ng --output "报错信息"
4. $DIRECTOR action          → 自动识别有 fallback，返回备选方案
5. Agent 执行备选方案
6. $DIRECTOR result --id xxx --outcome done --fallback --output "..."
```

## 状态流转

```
draft → approved → filming → wrapped
                ↘ cut → filming
```

Shot 状态：
```
pending → running → done / ng → fallback (if available) → done
                            ↘ skipped
```

## 目录结构

```
task-director/
├── SKILL.md              # 本文件
├── scripts/
│   └── director.py       # CLI 工具
└── templates/
    └── example-scenes.json  # 示例剧本
```

## 数据存储

剧本保存在 `~/.openclaw/memory/movies/`，每个剧本一个 JSON 文件。

## 设计哲学

- **电影隐喻**：用直觉化的概念降低理解成本
- **先规划后执行**：让用户有掌控感
- **备选方案**：不是只有一条路
- **随时喊卡**：可以暂停、跳过、重来
- **全程可视化**：进度条 + 状态图标一目了然
