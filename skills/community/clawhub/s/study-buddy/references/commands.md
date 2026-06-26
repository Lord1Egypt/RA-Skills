# Study Buddy 命令参考

## 核心命令清单

| 命令 | 功能 | 优先级 | 状态 |
|------|------|--------|------|
| `start` | 初始化学习档案（家长视角） | P0 | ✅ 已实现 |
| `plan` | 查看学习计划 | P0 | ✅ 已实现 |
| `today` | 查看今日任务 | P0 | ✅ 已实现 |
| `checkin` | 学习打卡 | P0 | ✅ 已实现 |
| `progress` | 查看进度 | P0 | ✅ 已实现 |
| `report` | 生成学习报告 | P0 | ✅ 已实现 |
| `wrong` | 错题本管理 | P0 | ✅ 已实现 |
| `feedback` | 获取反馈建议 | P1 | ✅ 已实现 |
| `data` | 查看数据位置 | - | ✅ 已实现 |
| `help` | 显示详细帮助 | - | ✅ 已实现 |

---

## 详细说明

### `python3 scripts/study-buddy.py start`
交互式初始化学习档案，**专为家长设计**。

**收集的信息：**
- 孩子姓名（昵称也可）
- 当前学段（小学/初中/高中）
- 主要学习科目
- 基础水平（基础薄弱/中等/较好/优秀）
- 每日计划学习时间
- 偏好学习方式
- 学习目标类型
- 重要时间节点
- 家长备注（可选）

**输出：**
- 创建 `~/.study-buddy/profile.json`
- 自动生成三阶段学习计划（适应期→养成期→巩固期）

---

### `python3 scripts/study-buddy.py plan`
查看学习计划详情。

**显示内容：**
- 计划创建时间
- 学生姓名 + 学习科目
- 三阶段详情：
  - 阶段一：适应期（基础巩固）
  - 阶段二：养成期（稳步提升）
  - 阶段三：巩固期（拔高突破）

---

### `python3 scripts/study-buddy.py today`
查看今日学习任务和打卡状态。

---

### `python3 scripts/study-buddy.py checkin "内容" [--duration "时长"]`
记录学习情况。

**示例：**
```bash
python3 scripts/study-buddy.py checkin "完成数学作业第3章" --duration "45分钟"
```

---

### `python3 scripts/study-buddy.py progress`
查看学习进度统计。

**显示内容：**
- 累计学习天数
- 本周学习天数
- 连续打卡天数
- 最近学习记录

---

### `python3 scripts/study-buddy.py report`
生成学习报告。

---

### `python3 scripts/study-buddy.py wrong [action] [content]`
错题本管理。

**子命令：**
- `wrong add "内容" [--subject "学科"]` - 添加错题
- `wrong list` - 列出错题
- `wrong review "ID"` - 记录复习
- `wrong master "ID"` - 标记掌握

---

### `python3 scripts/study-buddy.py feedback`
获取反馈建议。

---

### `python3 scripts/study-buddy.py data`
查看数据存储位置。

---

### `python3 scripts/study-buddy.py help`
显示详细帮助信息，包括所有命令和示例。

---

## 数据文件结构

```
~/.study-buddy/
├── profile.json          # 学习档案
├── plans/                # 学习计划
├── logs/                 # 学习日志
├── wrong_questions/      # 错题本
└── report_YYYYMMDD.json  # 学习报告
```

### profile.json 结构
```json
{
  "student_name": "小明",
  "grade_level": "b",
  "subject": "数学",
  "level": "b",
  "daily_time": "1小时",
  "learning_style": "c",
  "goal_type": "b",
  "deadline": "2026-04-15",
  "parent_notes": "需要多鼓励",
  "created_at": "2026-03-09T11:00:00"
}
```
