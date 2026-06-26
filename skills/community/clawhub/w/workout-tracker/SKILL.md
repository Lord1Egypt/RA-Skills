---
name: workout-tracker
description: 个人健身跟踪器 — 通过文字记录健身训练数据，自动解析动作、组数、次数和重量，实时写入本地 MySQL 数据库。支持制定专属训练计划、查询历史记录、追踪进步曲线，以及球类和有氧运动记录。
metadata: {"clawdbot":{"emoji":"🏋️","requires":{"bins":["python3","mysql"],"env":["MYSQL_USER","MYSQL_PASSWORD","MYSQL_DATABASE","MYSQL_SOCKET"]},"primaryEnv":"MYSQL_PASSWORD"}}
---

# Workout Tracker

记录健身数据，自动解析训练内容并写入数据库。

## 🚀 完整安装指南

### 1. 安装依赖
```bash
# 安装 Python MySQL 连接器
pip install mysql-connector-python

# 验证安装
python3 -c "import mysql.connector; print('✅ mysql-connector-python 已安装')"
```

### 2. 安全配置环境变量（推荐方法）

#### 方法 A：使用 .env 文件（最安全）
```bash
# 创建 .env 配置文件
cat > .workout-tracker.env << 'EOF'
MYSQL_SOCKET="/tmp/mysql.sock"
MYSQL_USER="workout_user"
MYSQL_PASSWORD="your_secure_password"  # 替换为实际密码
MYSQL_DATABASE="workout_tracker"
EOF

# 设置文件权限（仅当前用户可读）
chmod 600 .workout-tracker.env

# 加载配置
source .workout-tracker.env
```

#### 方法 B：临时环境变量（会话有效）
```bash
# 仅在当前终端会话中有效
export MYSQL_SOCKET="/tmp/mysql.sock"
export MYSQL_USER="workout_user"
export MYSQL_PASSWORD="your_password"  # 注意：密码会出现在 shell 历史中
export MYSQL_DATABASE="workout_tracker"
```

#### 方法 C：交互式输入（最安全，无痕迹）
```python
# 使用脚本提示输入密码，不存储在任何地方
import getpass
import os

password = getpass.getpass("请输入 MySQL 密码: ")
os.environ['MYSQL_PASSWORD'] = password
```

**⚠️ 安全警告**：避免将密码存储在 ~/.bashrc、~/.zshrc 或版本控制的文件中。

### 3. 数据库用户创建
```sql
-- 在 MySQL 中执行
CREATE USER IF NOT EXISTS 'workout_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT INSERT, SELECT, UPDATE, DELETE ON workout_tracker.* TO 'workout_user'@'localhost';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS workout_tracker;
```

### 4. 初始化数据库（一键脚本）
```bash
# 运行初始化脚本
python3 /path/to/workout-tracker/scripts/init_database.py
```

### 5. 验证安装
```bash
# 运行验证脚本
python3 /path/to/workout-tracker/scripts/verify_setup.py
```

### 安全配置（推荐使用 .env 文件）
```bash
# 创建安全的 .env 配置文件（不上传至版本控制）
cat > ~/.workout-tracker.env << 'EOF'
# Workout Tracker 数据库配置
# ⚠️ 警告：此文件包含敏感信息，不要上传到版本控制
MYSQL_SOCKET="/tmp/mysql.sock"
MYSQL_USER="workout_user"
MYSQL_PASSWORD="your_secure_password_here"  # 替换为你的实际密码
MYSQL_DATABASE="workout_tracker"
EOF

# 设置文件权限（仅当前用户可读）
chmod 600 ~/.workout-tracker.env

# 在 shell 中加载配置
source ~/.workout-tracker.env
```

### 自动化安装脚本（安全版本）
```bash
#!/bin/bash
# workout-tracker-setup-secure.sh

echo "🏋️ Workout Tracker 安全安装"

# 安装 Python 依赖
echo "📦 安装 Python 依赖..."
pip install mysql-connector-python

# 创建安全的配置模板
echo "🔐 创建安全配置模板..."
cat > workout-tracker-config-template.env << 'EOF'
# Workout Tracker 配置模板
# 1. 将此文件复制为 .workout-tracker.env
# 2. 填写实际的数据库密码
# 3. 设置文件权限: chmod 600 .workout-tracker.env

MYSQL_SOCKET="/tmp/mysql.sock"
MYSQL_USER="workout_user"
MYSQL_PASSWORD=""  # ⬅️ 在此处填写你的 MySQL 密码
MYSQL_DATABASE="workout_tracker"
EOF

echo "✅ 安装完成！"
echo ""
echo "📋 后续步骤："
echo "1. 填写数据库密码: cp workout-tracker-config-template.env ~/.workout-tracker.env"
echo "2. 编辑 ~/.workout-tracker.env 设置密码"
echo "3. 设置文件权限: chmod 600 ~/.workout-tracker.env"
echo "4. 加载配置: source ~/.workout-tracker.env"
echo "5. 验证安装: python3 scripts/verify_setup.py"
echo ""
echo "🔒 安全提示："
echo "- 永远不要在版本控制中包含 .env 文件"
echo "- 使用强密码并定期更换"
echo "- 数据库用户仅授予最小必要权限"
```

## 本地配置说明

本技能专为单用户本地部署设计（用户无需公开任何凭据）。数据库配置通过本地环境变量或配置文件管理，不随技能发布。

**默认单用户 ID 说明：**
- 本技能设计为单用户工具（user_id = 1 是默认值，适用于个人本地使用）
- 安装后用户可自行修改 `workout_sessions` 和 `workout_items` 中的 `user_id` 以匹配自己的设置
- 数据库表结构兼容多用户扩展（只需在查询时指定对应 user_id）

## 数据库结构

```sql
exercise_types (id, name, muscle_group, equipment, unit)
  -- id: 自增主键
  -- name: 动作名称，如"杠铃深蹲"、"腿举机"
  -- muscle_group: 主要肌群（胸/背/腿/肩/臂/腹/全身/下背）
  -- equipment: 器械类型（杠铃/哑铃/器械/自重/有氧）
  -- unit: 计量单位（次/分钟/米）

gym_equipment (id, name, category, muscle_main, muscle_sec, created_at)
  -- id: 自增主键
  -- name: 器械名称
  -- category: 类别（哑铃/杠铃/器械/有氧/自由重量/辅助）
  -- muscle_main/muscle_sec: 主要/次要肌群

workout_sessions (id, user_id, workout_date, start_time, end_time, duration_min, workout_type, notes)
  -- id: 自增主键
  -- user_id: 用户ID（默认1，单用户本地部署）
  -- workout_date: 训练日期
  -- duration_min: 总时长（分钟）
  -- workout_type: 训练类型（力量/有氧/柔韧）
  -- notes: 备注（如状态评分"状态评分: 9/10 | 非常爽"）

workout_items (id, session_id, exercise_type_id, set_order, reps, weight_kg, distance_km, rpe, notes)
  -- id: 自增主键
  -- session_id: 关联 workout_sessions.id
  -- exercise_type_id: 关联 exercise_types.id
  -- set_order: 第几组（1, 2, 3...）
  -- reps: 重复次数
  -- weight_kg: 重量（公斤）
  -- notes: 备注（如"杠铃深蹲第1组"）
```

## 核心流程

### 标准预排模式（默认）

用户一次性报完整动作计划 → 我预排所有组 → 用户每完成一组说 done → 我逐条标记完成

**用户命令示例：**
- 说`"深蹲 60公斤 4组×8次"` → 预排所有组，记录为待完成状态，回复"已预排4组，每完成一组说done"
- 说`"done"` → 标记当前训练最新一组为完成状态，回复"第1组完成！还剩3组"
- 说`"done 这组是10次"` → 同上，并更新该组次数为10次
- 说`"done 加一组"` → 完成当前组，并追加一组相同训练
- 说`"卧推 40公斤 3组×10次"` → 切换到新动作，重新预排
- 说`"结束了"` → 训练完成，自动计算时长，询问状态评分

**操作流程（预排模式）：**
```
1. 用户说"动作 + 重量 + X组×Y次"
   → 若当日尚无 workout_session，先创建（start_time=NOW()）
   → 解析动作名、重量、组数、次数
   → 匹配 exercise_types.id，不存在则插入
   → 一次性插入 N 条 workout_items，notes 标"⏳待完成"
   → 回复"已预排X组，每完成一组说done"
   → 随机（30%概率）附一句简短鼓励（如"这个重量稳的！"）

2. 用户说 "done"（或"done 这组是X次"）
   → 找到当前 session 最新未标记 ✓ 的记录
   → 更新 notes 追加" ✓"（若用户报了次数，同时更新 reps）
   → 回复"第N组完成！还剩X组"（若还有未完成的）
   → 若动作全部完成 → 回复"XX动作完成！下一个动作是什么？"
   → 随机（30%概率）附一句简短鼓励

3. 用户说 "done 加一组"
   → 执行步骤2的标记完成逻辑
   → 在当前动作下追加一条新的"⏳待完成"记录（reps/weight 继承上一组）
   → 回复"已追加第N+1组 ⏳"

4. 用户说 "动作名 重量 X组×Y次"
   → 切换到新动作，重复步骤1

5. 用户说 "结束了"
   → 自动计算：TIMESTAMPDIFF(MINUTE, start_time, NOW())，start_time 来自 workout_sessions
   → UPDATE workout_sessions SET duration_min=? WHERE id=current_session
   → 查询汇总数据，回复训练完成汇总
   → 主动询问："今天状态怎么样？状态评分1-10"
```

**情绪价值 — 鼓励语料库（随机选取）：**

每完成一组时，随机附上以下类型的鼓励语：
- 🔥 进度类：`"又完成一组，腿部在燃烧！"`、`"离目标又近了一步！"`、`"感觉怎么样？这组有没有更稳？"`
- 💪 力量类：`"这重量稳的！"`、`"继续保持这个节奏"`、`"你的深蹲越来越扎实了"`
- 🌟 夸赞类：`"不错不错！"`、`"这组完成得很干净"`、`"看得出状态很好！"`
- 😅 幽默类：`"腿已经软了？坚持住！"`、`"疼痛是成长的象征 😄"`、`"汗水不会骗人 💦"`
- 🏆 完成类（动作全部完成）：`"这个动作拿捏了！"`、`"太强了，下一个！"`、`"肌肉在尖叫，继续！"`

**鼓励触发规则：**
- 开始新动作时：30%概率附一句（针对该动作的简短鼓励）
- 每完成一组 "done" 时：50%概率附一句（简短、自然，不要每组都说）
- 动作全部4组完成时：80%概率附一句夸奖
- 用户感到吃力或犹豫时：主动降低语气，给予安慰而非催促
- 不要过度鼓励，保持自然节奏，避免刷屏感

**SQL模板（参数化查询）：**
```sql
-- 创建新训练 session（如尚无今日 session，start_time 自动为 NOW()）
INSERT INTO workout_sessions (user_id, workout_date, workout_type, start_time)
VALUES (?, CURDATE(), ?, NOW());  -- user_id, workout_type

-- 获取当前 session_id
SELECT id FROM workout_sessions WHERE user_id=? ORDER BY id DESC LIMIT 1;  -- user_id

-- 预排 N 组（用户说"动作 重量 X组×Y次"）
INSERT INTO workout_items (session_id, exercise_type_id, set_order, reps, weight_kg, notes) VALUES
(?, ?, 1, ?, ?, CONCAT(?, ' 第1组 ⏳')),
(?, ?, 2, ?, ?, CONCAT(?, ' 第2组 ⏳')),
...
(?, ?, N, ?, ?, CONCAT(?, ' 第N组 ⏳'));  -- sid, eid, reps, weight, exercise_name

-- 标记第N组完成（用户说 done 时）
UPDATE workout_items
SET notes = CONCAT(?, ' 第', ?, '组 ✓'),  -- exercise_name, set_order
    reps = ?  -- 如用户报了次数
WHERE session_id=? AND set_order=?;  -- sid, set_order

-- 追加一组（用户说 done 加一组 时）
INSERT INTO workout_items (session_id, exercise_type_id, set_order, reps, weight_kg, notes)
VALUES (?, ?, (SELECT IFNULL(MAX(set_order),0)+1 FROM workout_items WHERE session_id=?), ?, ?, CONCAT(?, ' 第N组 ⏳'));
-- sid, eid, sid, reps, weight, exercise_name

-- 完成训练（duration_min = NOW() - start_time）
SELECT TIMESTAMPDIFF(MINUTE, start_time, NOW()) as duration_min
FROM workout_sessions WHERE id=?;  -- sid
UPDATE workout_sessions SET duration_min=? WHERE id=?;  -- minutes, sid

-- 状态评分更新（后续用户说"X分"时）
UPDATE workout_sessions SET notes=? WHERE id=?;  -- score_note, sid
```

### 模式二：一次性记录（训练后补录）

用户一次性报完整训练内容：
```
今天练了深蹲 4组×10次×30公斤，腿举 3组×8次×72公斤
```

**操作流程：**
1. 解析所有动作及每组数据
2. 创建 session
3. 批量插入 workout_items
4. 回复汇总

### 模式三：制定训练计划（基础版）

用户说"今天练腿给我一个计划"
→ 根据 gym_equipment 中的器械，生成针对性的训练计划
→ 回复格式：热身 → 主项 → 辅助项 → 拉伸

### 模式四：智能生成训练计划（增强版）

当用户说"今天练X"、"我要练X"、"给我一个X训练计划"时，自动执行：

**第一步：查询本周已训练过的肌群（避免重复）**
```sql
-- 查询本周（近7天）训练过的肌群及动作
SELECT DISTINCT ws.workout_date, ws.workout_type,
  et.muscle_group, et.name as exercise_name,
  wi.weight_kg, wi.reps, wi.set_order
FROM workout_sessions ws
JOIN workout_items wi ON wi.session_id = ws.id
JOIN exercise_types et ON et.id = wi.exercise_type_id
WHERE ws.user_id=1 AND ws.workout_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
ORDER BY ws.workout_date DESC, et.muscle_group;
```

**第二步：查询用户器械（确保计划可执行）**
```sql
SELECT id, name, category, muscle_main, muscle_sec
FROM gym_equipment
WHERE muscle_main LIKE '%背%'   -- 动态替换目标肌群关键词
   OR muscle_sec LIKE '%背%'
ORDER BY category;
```

**第三步：分析后生成计划**
- 目标肌群本周已练过 → 计划注明"上次练过此肌群，可适当降低强度"
- 目标肌群本周未练 → 正常强度
- 计划必须全部来自已有器械，无器械可用时标注"需新增器械"
- 回复格式：热身 → 主项（含建议重量参考）→ 辅助项 → 拉伸

**回复模板：**
```
📋 今日{肌群}训练计划（智能生成）
🗓️ 本周已练：{已训练肌群及日期}
🏋️ 可用器械：{器械列表}

① 热身（5-10分钟）
② 主项（3-4组×8-12次）— 标注动作名 [器械名]
③ 辅助项（2-3组×10-15次）— 标注动作名 [器械名]
④ 拉伸

💡备注：{上次训练情况及建议}
```

### 模式五：查询记录

用户问"今天练了什么"、"上周训练几次"等
→ 执行查询SQL → 整理成表格回复

## 查询示例

### 训练完成汇总
```sql
SELECT ws.workout_date, ws.duration_min, ws.workout_type, ws.notes,
  et.name, COUNT(*) as sets, SUM(wi.reps) as total_reps, wi.weight_kg
FROM workout_items wi
JOIN workout_sessions ws ON ws.id = wi.session_id
JOIN exercise_types et ON et.id = wi.exercise_type_id
WHERE wi.session_id = ?
GROUP BY et.name, wi.weight_kg
ORDER BY et.name;
```

### 查今日训练
```sql
SELECT ws.workout_date, ws.duration_min, ws.workout_type,
  et.name, wi.set_order, wi.reps, wi.weight_kg
FROM workout_sessions ws
JOIN workout_items wi ON wi.session_id = ws.id
JOIN exercise_types et ON et.id = wi.exercise_type_id
WHERE ws.user_id=1 AND ws.workout_date=CURDATE()
ORDER BY ws.id, wi.set_order;
```

### 查本周训练天数
```sql
SELECT COUNT(DISTINCT workout_date) as days,
  SUM(duration_min) as total_min
FROM workout_sessions
WHERE user_id=1 AND workout_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY);
```

### 查某动作历史
```sql
SELECT ws.workout_date, et.name, wi.reps, wi.weight_kg
FROM workout_items wi
JOIN workout_sessions ws ON ws.id = wi.session_id
JOIN exercise_types et ON et.id = wi.exercise_type_id
WHERE ws.user_id=1 AND et.name LIKE '%深蹲%'
ORDER BY ws.workout_date DESC LIMIT 10;
```

## 动作识别优先级

用户输入动作简称时，自动识别对应 exercise_types：
- "山羊挺身" → 45度背部挺身机
- "腿举" → 腿举机/倒蹬机
- "罗马凳" → 罗马凳/背肌伸展架
- "深蹲" → 杠铃深蹲
- "卧推" → 杠铃卧推
- 等等（模糊匹配）

如果完全匹配不到，先插入新动作。

## 训练完成后的反馈询问

训练结束汇总回复后，必须主动询问：
```
"今天状态怎么样？状态评分1-10"
```

用户回复后，更新 workout_sessions.notes：
```sql
UPDATE workout_sessions SET notes = CONCAT('状态评分: ', ?, '/10 | ', ?) WHERE id = ?;  -- score, feeling, sid
```

## 常见动作类型判断

根据关键词判断 workout_type：
- "跑"、"快走"、"椭圆机"、"有氧" → `有氧`
- "瑜伽"、"拉伸"、"普拉提" → `柔韧`
- 其他（卧推、深蹲、硬拉、引体等） → `力量`

## 模式六：球类/有氧运动记录（简化流程）

用户说"网球一小时"、"游泳半小时"等，直接创建 session，不走预排组流程。

**识别规则：**
- 运动名 + 时长（网球/羽毛球/乒乓球/篮球/足球/游泳/跑步/骑行/椭圆机 等）
- 时长单位：小时/分钟/小时半（1.5小时）

**操作流程：**
1. 匹配 `exercise_types.name`（模糊匹配 sport_name）
2. 创建 session，`sport_name` 字段写入运动名，`workout_type` 设为 `有氧`
3. `duration_min` 写入实际时长（分钟）
4. 不创建 `workout_items`（这类运动不需要组数记录）
5. 回复汇总即可

**SQL：**
```sql
-- 创建运动记录
INSERT INTO workout_sessions (user_id, workout_date, sport_name, workout_type, duration_min, start_time)
VALUES (1, CURDATE(), '网球发球机', '有氧', 60, NOW());
```

**回复模板：**
```
🎾 网球发球机训练记录完成
───
⏱️ 时长：60 分钟
🏃 类型：有氧
───
状态评分 1-10？
```

## SQL 安全规范（严格禁止 SQL 注入）

**所有用户输入必须经过参数化查询，禁止任何形式的字符串拼接 SQL。**

### ✅ 正确做法（参数化查询）
```python
# Python + MySQL Connector 示例
import mysql.connector

# 使用参数化查询
cursor.execute(
    "INSERT INTO workout_items (session_id, exercise_type_id, set_order, reps, weight_kg) VALUES (%s, %s, %s, %s, %s)",
    (session_id, exercise_type_id, set_order, reps, weight_kg)
)

# LIKE 查询也必须参数化
search_term = "深蹲"
cursor.execute(
    "SELECT * FROM exercise_types WHERE name LIKE %s",
    (f"%{search_term}%",)  # 参数化，安全
)
```

### ❌ 绝对禁止的做法
```python
# ❌ 危险：字符串拼接（极易 SQL 注入）
cursor.execute(f"INSERT INTO ... VALUES ({session_id}, {exercise_type_id}, ...)")

# ❌ 危险：使用 .format() 或 %
cursor.execute("SELECT * FROM exercise_types WHERE name LIKE '%{}%'".format(user_input))

# ❌ 危险：直接拼接用户输入到 SQL
sql = "SELECT * FROM exercise_types WHERE name LIKE '%" + user_input + "%'"
cursor.execute(sql)
```

### ⚠️ 特别注意
1. **LIKE 子句**：必须参数化整个模式，不能只参数化搜索词
2. **表名/列名**：不能参数化，必须白名单验证
3. **整数/浮点数**：同样需要参数化，不要以为数字就安全
4. **Python f-string**：绝对禁止用于 SQL 语句构建

### 🔒 额外防护措施
1. 数据库用户使用最小权限原则（仅 GRANT INSERT/SELECT/UPDATE/DELETE）
2. 所有查询记录日志（用于审计异常）
3. 输入验证：动作名称长度限制、数字范围检查
4. 错误消息不泄露数据库结构

## 安全审计清单（部署前必须检查）

### 🔍 SQL 注入防护
- [ ] 所有 SQL 查询使用参数化语句（?, %s 等占位符）
- [ ] 绝对禁止字符串拼接构建 SQL
- [ ] LIKE 查询完全参数化（包括通配符 % 和 _）
- [ ] 整数/浮点数值也使用参数化查询

### 🔐 数据库权限
- [ ] 创建专用数据库用户（非 root）
- [ ] 仅授予最小权限：INSERT/SELECT/UPDATE/DELETE
- [ ] 禁止 DROP、CREATE、ALTER 权限
- [ ] 定期审计数据库用户权限

### 🛡️ 输入验证
- [ ] 动作名称长度限制（例如 50 字符）
- [ ] 数字范围验证（reps: 1-100, weight: 0-500kg）
- [ ] 时间/日期格式验证
- [ ] 特殊字符过滤或转义

### 📝 安全配置
- [ ] 数据库连接使用本地 socket（非 TCP）
- [ ] 错误消息不泄露数据库结构
- [ ] 查询日志记录（用于审计异常）
- [ ] 定期备份数据库

### 🚨 应急响应
- [ ] 监控异常查询模式
- [ ] 记录失败登录尝试
- [ ] 准备数据库恢复方案
- [ ] 定期安全更新 MySQL

---

## 注意事项

- 用户 ID 默认为 1（单用户本地部署）
- 所有 SQL 必须使用参数化查询，防止 SQL 注入
- 数据库用户建议创建专用账户，仅授予 INSERT/SELECT/UPDATE/DELETE 权限
- duration_min 单位为分钟
- weight_kg 单位为公斤，保留2位小数
- reps 为整数（次数）
- set_order 从1开始，每组递增
- 训练结束后必须询问状态评分
- 解析时支持"4组×8次"、"4x8"、"四组八次"、"每组12次"等多种格式
- 用户说"done"时，记录的是当前 session 最新插入的未完成组
