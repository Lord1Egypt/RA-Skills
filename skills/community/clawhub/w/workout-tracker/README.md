# Workout Tracker

个人健身跟踪器 — 通过文字记录健身训练数据，自动解析动作、组数、次数和重量，实时写入本地 MySQL 数据库。支持制定专属训练计划、查询历史记录、追踪进步曲线，以及球类和有氧运动记录。

## 主要功能

### 🏋️ 健身房训练模式
- **预排组模式**：一次性报完整动作计划，逐组完成
- **实时记录**：每完成一组说 "done"，自动标记完成
- **智能鼓励**：根据训练进度给予个性化鼓励语

### 🎾 球类/有氧运动模式
- **简化记录**：网球、羽毛球、游泳等运动直接记录时长
- **自动分类**：自动识别运动类型，归类为有氧/力量/柔韧

### 📊 训练计划与查询
- **智能计划生成**：根据本周训练历史和可用器械生成针对性计划
- **历史查询**：查看今日训练、本周训练天数、某动作历史记录
- **进度追踪**：记录重量、次数进步曲线

### 🗄️ 数据库管理
- **本地 MySQL**：所有数据存储在本地，不上传云端
- **安全设计**：参数化查询，防止 SQL 注入
- **多用户支持**：表结构支持多用户扩展

## 🚀 快速开始

### 1. 安装依赖
```bash
# 安装 Python MySQL 连接器
pip install mysql-connector-python

# 或使用系统包管理器
# Ubuntu/Debian: sudo apt-get install python3-mysql.connector
# macOS: brew install mysql-connector-python
```

### 2. 数据库准备
```sql
-- 创建数据库和用户
CREATE DATABASE IF NOT EXISTS workout_tracker;
CREATE USER IF NOT EXISTS 'workout_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT INSERT, SELECT, UPDATE, DELETE ON workout_tracker.* TO 'workout_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 安装技能
```bash
# 使用 skillhub 安装
skillhub install workout-tracker
```

### 4. 配置环境变量
```bash
# 必需的环境变量
export MYSQL_SOCKET="/tmp/mysql.sock"   # MySQL socket 路径
export MYSQL_USER="workout_user"        # MySQL 用户名
export MYSQL_PASSWORD="your_password"   # MySQL 密码
export MYSQL_DATABASE="workout_tracker" # 数据库名
```

## 使用示例

### 健身房训练
```
用户: 深蹲 60公斤 4组×8次
助手: 已预排4组，每完成一组说done

用户: done
助手: 第1组完成！还剩3组 💪

用户: done 加一组
助手: 第2组完成！已追加第5组 ⏳
```

### 球类运动
```
用户: 网球发球机一小时
助手: 🎾 网球发球机训练记录完成
     ───
     ⏱️ 时长：60 分钟
     🏃 类型：有氧
     ───
     状态评分 1-10？
```

### 训练计划
```
用户: 今天练背给我一个计划
助手: 📋 今日背部训练计划（智能生成）
     🗓️ 本周已练：胸部（昨天）
     🏋️ 可用器械：引体向上架、哑铃划船、高位下拉机
     
     ① 热身（5-10分钟）
     ② 主项：引体向上 [自重] 3组×8-12次
     ③ 辅助：哑铃划船 [哑铃] 3组×10-15次
     ④ 拉伸
```

## 安全特性

### 🔒 SQL 注入防护
- 所有查询使用参数化语句（?, %s 占位符）
- 禁止字符串拼接构建 SQL
- LIKE 查询完全参数化
- 输入验证和长度限制

### 🔐 权限管理
- 专用数据库用户，最小权限原则
- 仅授予 INSERT/SELECT/UPDATE/DELETE 权限
- 本地 socket 连接，不暴露到网络

## 数据库结构

```sql
-- 核心表：训练会话
workout_sessions (id, user_id, workout_date, sport_name, workout_type, duration_min, notes)

-- 训练项目
workout_items (id, session_id, exercise_type_id, set_order, reps, weight_kg, notes)

-- 动作类型
exercise_types (id, name, muscle_group, equipment, unit)

-- 器械清单
gym_equipment (id, name, category, muscle_main, muscle_sec)
```

## 贡献与支持

- **问题反馈**: GitHub Issues
- **功能建议**: GitHub Discussions
- **安全漏洞**: 私信联系

## 许可证

MIT License - 详见 LICENSE 文件