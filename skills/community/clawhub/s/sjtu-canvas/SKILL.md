---
name: sjtu-canvas
description: |
  SJTU Canvas LMS 课程助手。管理上海交通大学 Canvas (oc.sjtu.edu.cn) 课程数据。
  也适用于其他基于 Canvas LMS 的高校，修改 base_url 即可。
  触发场景:
  (1) 查看/下载课程文件(PPT/PDF)、批量下载课件
  (2) 查看作业列表、DDL、提交状态、提交作业
  (3) 同步作业DDL到Apple日历(Mac+iPhone)
  (4) PPT/PDF内容提取和AI总结、课件学习
  (5) 作业辅导(提取作业要求+课件内容→给思路)
  (6) 查看成绩、计算均分
  (7) 课程讨论区摘要
  (8) DDL预警提醒
  (9) 期末复习包生成(所有课件→Markdown)
  (10) 一键提交作业
  触发词: Canvas, 课程, 作业, DDL, 截止, 成绩, 课件, PPT, 总结, 复习, 提交作业, 讨论区, course, assignment, grade
---

# SJTU Canvas 课程助手

Canvas LMS 课程管理技能，默认配置为上海交通大学 (oc.sjtu.edu.cn)，也兼容其他 Canvas LMS 实例。

## 首次配置

1. 复制配置模板并填入你的 Canvas API Token：

```bash
cp skills/sjtu-canvas/config.example.json skills/sjtu-canvas/config.json
```

2. 编辑 `config.json`，填入：
   - `canvas_token`: 从 Canvas → 设置 → 新建访问令牌 获取
   - `base_url`: 你的 Canvas 地址（默认 `https://oc.sjtu.edu.cn`）
   - `save_dir`: 课件下载目录（默认 `~/Downloads/Canvas课件`）
   - `calendar_name`: Apple 日历分类名（默认 `Canvas作业`）

3. 安装依赖：

```bash
pip3 install python-pptx pdfplumber requests
```

## 核心脚本

所有脚本位于 `skills/sjtu-canvas/scripts/`，用 python3 执行。

### canvas_api.py — Canvas API 交互

```bash
# 列出课程
python3 scripts/canvas_api.py courses

# 查看所有未来DDL
python3 scripts/canvas_api.py ddls

# 查看已出成绩
python3 scripts/canvas_api.py grades
```

Python 中调用:
```python
import sys; sys.path.insert(0, "skills/sjtu-canvas/scripts")
from canvas_api import *

list_courses()                          # 课程列表
list_assignments(course_id)             # 作业列表
get_all_upcoming_ddls()                 # 所有未来DDL
get_course_grades(course_id)            # 成绩
list_course_files(course_id)            # 课程文件
download_course_files(cid, name, dir)   # 批量下载
list_discussions(course_id)             # 讨论区
get_full_discussion(cid, topic_id)      # 讨论详情
submit_assignment(cid, aid, [paths])    # 提交作业
```

### file_extractor.py — 课件内容提取

```bash
# 提取单个文件
python3 scripts/file_extractor.py path/to/file.pptx

# 批量提取目录 → Markdown
python3 scripts/file_extractor.py ~/Downloads/Canvas课件/传热学 ~/Downloads/Canvas课件/传热学_md
```

支持格式: `.pptx` `.pdf` `.docx` `.txt` `.md`

### calendar_sync.py — DDL → Apple 日历 (macOS)

```bash
cd skills/sjtu-canvas && python3 scripts/calendar_sync.py
```

自动创建日历分类，已存在的事件不会重复创建。通过 iCloud 同步到 iPhone。

## 工作流

### 1. 课件下载 + 总结

1. `canvas_api.download_course_files()` 下载课程 PPT/PDF
2. `file_extractor.extract_file()` 提取文本
3. 用 LLM 总结要点

### 2. 作业辅导

1. `canvas_api.get_assignment()` 获取作业要求
2. 下载相关课件并提取内容
3. 结合作业要求和课件，给出解题思路

### 3. DDL 管理

1. `canvas_api.get_all_upcoming_ddls()` 获取所有未来 DDL
2. `calendar_sync.sync_ddls()` 同步到 Apple 日历
3. 可设置 cron 定时巡检

### 4. 成绩追踪

1. `canvas_api.get_course_grades()` 获取各科成绩
2. 计算加权均分

### 5. 期末复习包

1. `canvas_api.download_course_files()` 批量下载课件
2. `file_extractor.batch_extract()` 批量提取为 Markdown
3. 导入 NotebookLM 或其他工具复习

### 6. 提交作业

1. 确认课程 ID、作业 ID、本地文件
2. `canvas_api.submit_assignment()` 提交
3. **提交前必须向用户确认**

## 注意事项

- 提交作业前**必须**向用户确认
- Canvas Token 有效期可能有限，失效时需重新生成
- Apple 日历同步仅支持 macOS
- 非 SJTU 用户需修改 `config.json` 中的 `base_url`
