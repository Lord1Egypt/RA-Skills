---
name: wangcut
description: |
  秦丝智能视频剪辑APP的API集成，用于创建和管理AI视频剪辑任务。
  TRIGGER when: 用户请求创建视频、生成视频剪辑、查看视频任务列表、下载剪辑结果、等待任务完成、配置旺剪账号。
  触发词: "创建视频"、"视频剪辑"、"生成视频"、"查看任务"、"下载视频"、"等待视频"、"配置旺剪"、"旺剪账号"、"wangcut"。
  支持功能: (1) 根据文案创建视频剪辑任务，自动随机选择7个素材 (2) 查看任务列表和详情 (3) 等待任务完成并下载视频到本地 (4) 自动检测配置状态并引导用户配置账号密码
---

# 秦丝智能视频剪辑

通过API操作秦丝智能视频剪辑APP。

## 首次使用

首次使用会自动检测配置，如果未配置账号密码会提示：

```
⚠️ 旺剪配置异常: 账号密码未配置
请提供账号密码进行配置，格式：账号 158xxx 密码 xxx
```

### 配置账号密码

用户说：**"配置旺剪账号，账号 158xxx 密码 xxx"**

```python
import sys
sys.path.insert(0, '.claude/skills/wangcut/scripts')
from wangcut_api import setup_config

# 配置账号密码（自动创建或更新 config.ini）
config_path = setup_config(
    username="15812345678",
    password="your_password"
)
print(f"配置已保存到: {config_path}")
```

### 检查配置状态

```python
import sys
sys.path.insert(0, '.claude/skills/wangcut/scripts')
from wangcut_api import check_config, get_config_status_message

status, message, path = check_config()
print(f"状态: {status}, 消息: {message}")

# 或获取友好提示
print(get_config_status_message())
```

## 核心功能

### 创建视频任务

自动从最近100个素材中随机选择7个：

```python
import sys
sys.path.insert(0, '.claude/skills/wangcut/scripts')
from wangcut_api import create_video_task

task_id = create_video_task("你的视频文案内容")
print(f"任务ID: {task_id}")
```

### 查看任务列表

```python
import sys
sys.path.insert(0, '.claude/skills/wangcut/scripts')
from wangcut_api import list_recent_tasks

tasks = list_recent_tasks(count=10, with_details=True)
status_map = {0: '待处理', 1: '处理中', 2: '处理中', 3: '处理中', 4: '已完成', 5: '失败'}
for t in tasks:
    print(f"ID:{t['id']} 状态:{status_map.get(t.get('status'),'未知')}")
    print(f"   文案:{(t.get('script_content') or '')[:30]}...")
    print(f"   时长:{t.get('duration')}秒 分辨率:{t.get('resolution')}")
    print(f"   封面:{t.get('cover_title')} 语音:{t.get('voice_name')}")
    print(f"   播放地址:{t.get('play_url')}")
    print(f"   下载地址:{t.get('video_url')}")
```

### 等待完成并下载

```python
import sys
sys.path.insert(0, '.claude/skills/wangcut/scripts')
from wangcut_api import wait_and_download

filepath = wait_and_download(task_id=12575, timeout=600, save_dir="./downloads")
print(f"视频已下载: {filepath}")
```

## 任务状态码

| 码 | 状态 |
|----|------|
| 0 | 待处理 |
| 1-3 | 处理中 |
| 4 | 已完成 |
| 5 | 失败 |

## 高级用法

### 指定素材ID

```python
import sys
sys.path.insert(0, '.claude/skills/wangcut/scripts')
from wangcut_api import WangcutAPI

api = WangcutAPI()
result = api.create_task(
    script_content="视频文案",
    material_ids=[54131, 54130, 54129],
    voice_speed=1.5,
    subtitle_font_color="white"
)
```

### 查看任务详情

```python
import sys
sys.path.insert(0, '.claude/skills/wangcut/scripts')
from wangcut_api import WangcutAPI

api = WangcutAPI()
detail = api.get_task_detail(task_id=12575)
info = api.extract_task_info(detail)
print(f"文案: {info['script_content'][:50]}...")
print(f"时长: {info['duration']}秒, 分辨率: {info['resolution']}")
print(f"封面: {info['cover_title']}, 语音: {info['voice_name']}")
print(f"播放地址: {info['play_url']}")  # 用于浏览器预览
print(f"下载地址: {info['video_url']}")  # 用于下载到本地
```
