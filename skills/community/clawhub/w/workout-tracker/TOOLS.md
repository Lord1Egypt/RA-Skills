# TOOLS.md - 本地配置模板（不随技能发布）

## 📦 依赖说明

**运行时依赖：**
- `mysql-connector-python` (Python MySQL 连接器)
- 本地 MySQL 数据库服务

**安装依赖（一次性的）：**
```bash
# 安装 Python 依赖
pip install mysql-connector-python

# 或使用系统包管理器
# Ubuntu/Debian: sudo apt-get install python3-mysql.connector
# macOS: brew install mysql-connector-python
```

## 数据库连接

本技能**仅连接本地 MySQL**，不连接任何远程数据库。

### 安全配置指南

#### ⚠️ 重要安全警告
- **永远不要**将密码提交到版本控制（Git 等）
- **永远不要**将密码存储在 ~/.bashrc、~/.zshrc 等 shell 配置文件中
- **永远不要**在代码中硬编码密码
- 使用强密码（12位以上，包含大小写字母、数字、符号）
- 定期更换密码

#### 推荐配置方法（安全性从高到低）

**方法 A：.env 文件（最安全）**
```bash
# 创建 .env 文件（不上传至版本控制）
cat > ~/.workout-tracker.env << 'EOF'
MYSQL_SOCKET="/tmp/mysql.sock"
MYSQL_USER="workout_user"
MYSQL_PASSWORD="your_secure_password_here"  # ⬅️ 在此填写实际密码
MYSQL_DATABASE="workout_tracker"
EOF

# 设置文件权限（仅当前用户可读）
chmod 600 ~/.workout-tracker.env

# 加载配置
source ~/.workout-tracker.env
```

**方法 B：交互式输入（无痕迹）**
```python
# 使用 Python 脚本安全输入密码
import getpass
import os

password = getpass.getpass("请输入 MySQL 密码: ")
os.environ['MYSQL_PASSWORD'] = password
```

**方法 C：会话环境变量（临时）**
```bash
# 仅在当前终端会话有效（密码会出现在 shell 历史中）
export MYSQL_SOCKET="/tmp/mysql.sock"
export MYSQL_USER="workout_user"
export MYSQL_PASSWORD="temporary_password"  # 注意安全
export MYSQL_DATABASE="workout_tracker"
```

### 配置验证脚本
```bash
# 验证环境变量是否设置
if [ -z "$MYSQL_USER" ] || [ -z "$MYSQL_PASSWORD" ]; then
    echo "错误：请先设置 MYSQL_USER 和 MYSQL_PASSWORD 环境变量"
    exit 1
fi

# 验证 MySQL 连接
python3 -c "
import mysql.connector
import os
try:
    conn = mysql.connector.connect(
        unix_socket=os.getenv('MYSQL_SOCKET', '/tmp/mysql.sock'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE', 'workout_tracker')
    )
    print('✅ MySQL 连接成功')
    conn.close()
except Exception as e:
    print(f'❌ MySQL 连接失败: {e}')
    exit(1)
"
```

**注意：不支持 MYSQL_HOST（远程连接），仅支持本地 socket 或 localhost:3306。**

## 初始化数据库

```bash
# 创建专用数据库用户（最小权限原则）
mysql -u root -p -S /tmp/mysql.sock -e "
CREATE USER IF NOT EXISTS 'workout_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT INSERT, SELECT, UPDATE, DELETE ON workout_tracker.* TO 'workout_user'@'localhost';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS workout_tracker;
"
```

## 创建表结构

```sql
CREATE TABLE exercise_types (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL UNIQUE,
  muscle_group VARCHAR(50),
  equipment VARCHAR(50),
  unit VARCHAR(10) DEFAULT '次'
);

CREATE TABLE gym_equipment (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL UNIQUE,
  category VARCHAR(30),
  muscle_main VARCHAR(50),
  muscle_sec VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workout_sessions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL DEFAULT 1,
  workout_date DATE NOT NULL,
  duration_min INT,
  workout_type VARCHAR(30),
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workout_items (
  id INT PRIMARY KEY AUTO_INCREMENT,
  session_id INT NOT NULL,
  exercise_type_id INT NOT NULL,
  set_order INT DEFAULT 1,
  reps INT,
  weight_kg DECIMAL(6,2),
  notes VARCHAR(100),
  FOREIGN KEY (session_id) REFERENCES workout_sessions(id) ON DELETE CASCADE,
  FOREIGN KEY (exercise_type_id) REFERENCES exercise_types(id)
);
```

## 注意事项

- **仅限本地连接**：不暴露数据库到外部网络
- **最小权限用户**：数据库用户仅授予 INSERT/SELECT/UPDATE/DELETE，不授予 DROP 或 ADMIN 权限
- **用户 ID**：默认为 1，可在安装后自行修改
- **数据存储**：所有训练数据仅存储在本地，不上传任何外部服务
