# 上下文压缩技能安装指南

## 📦 安装方法

### 方法一：直接复制（推荐）
```bash
# 复制到OpenClaw技能目录
cp -r context-compactor ~/.openclaw/workspace/skills/

# 或者复制到全局技能目录
cp -r context-compactor ~/.agents/skills/
```

### 方法二：使用ClawHub（如果发布）
```bash
# 搜索技能
clawhub search context-compactor

# 安装技能
clawhub install context-compactor
```

## 🔧 依赖安装

### Python依赖
```bash
# 安装Python依赖
pip install -r requirements.txt

# 或者使用pip3
pip3 install -r requirements.txt
```

### 系统依赖
确保系统已安装：
- Python 3.8+
- SQLite3
- Bash shell

## 🚀 快速配置

### 1. 基本配置
```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/context-compactor

# 修改配置文件（可选）
nano config.json

# 启动系统
./start_system.sh
```

### 2. 集成到OpenClaw

#### 添加到心跳检查
编辑 `~/.openclaw/workspace/HEARTBEAT.md`：
```markdown
# 上下文压缩检查
- 检查压缩系统状态：cd ~/.openclaw/workspace/skills/context-compactor && ./check_status.sh
- 查看最近压缩报告：python3 integration.py --report
- 优化配置参数：python3 integration.py --config --optimize
```

#### 创建定时任务
```bash
# 每小时检查一次
(crontab -l 2>/dev/null; echo "0 * * * * cd ~/.openclaw/workspace/skills/context-compactor && python3 integration.py --check") | crontab -

# 每天清理旧日志
(crontab -l 2>/dev/null; echo "0 2 * * * cd ~/.openclaw/workspace/skills/context-compactor && find logs -name '*.log' -mtime +7 -delete") | crontab -
```

## 📊 验证安装

### 1. 检查系统状态
```bash
./check_status.sh
```

### 2. 运行测试
```bash
python3 test_compaction.py
```

### 3. 查看日志
```bash
tail -f logs/system.log
```

## 🔍 故障排除

### 常见问题

**问题1：Python依赖安装失败**
```bash
# 使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**问题2：权限不足**
```bash
# 给脚本执行权限
chmod +x *.sh

# 给Python脚本执行权限
chmod +x *.py
```

**问题3：端口冲突**
```bash
# 修改API端口
sed -i 's/"port": 8080/"port": 8081/' config.json
```

**问题4：数据库问题**
```bash
# 重新初始化数据库
rm -f context_compactor.db
python3 integration.py --init
```

## 🎯 使用示例

### 示例1：手动压缩
```bash
# 查看当前状态
python3 integration.py --status

# 手动触发压缩
python3 integration.py --compress

# 查看压缩报告
python3 integration.py --report
```

### 示例2：监控模式
```bash
# 启动监控
./start_monitor.sh

# 查看监控日志
tail -f logs/monitor.log

# 停止监控
./stop_monitor.sh
```

### 示例3：API访问
```bash
# 启动API服务器
python3 api_server.py &

# 查询状态
curl http://localhost:8080/status

# 触发压缩
curl -X POST http://localhost:8080/compress
```

## 📈 性能调优

### 调整压缩策略
```bash
# 更积极的压缩
python3 integration.py --config --memory-threshold 0.6 --strategy aggressive

# 更保守的压缩
python3 integration.py --config --memory-threshold 0.8 --strategy conservative
```

### 优化监控间隔
```bash
# 增加监控间隔（秒）
python3 integration.py --config --monitor-interval 300

# 减少压缩频率
python3 integration.py --config --max-daily-compactions 5
```

## 🔄 更新和维护

### 更新技能
```bash
# 备份当前配置
cp config.json config.json.backup

# 更新文件
git pull origin main  # 如果使用git
# 或者手动复制新版本

# 恢复配置
cp config.json.backup config.json
```

### 定期维护
```bash
# 清理旧日志（每周）
find logs -name "*.log" -mtime +7 -delete

# 备份数据库（每月）
cp context_compactor.db "backup/context_compactor_$(date +%Y%m%d).db"

# 优化数据库
sqlite3 context_compactor.db "VACUUM;"
```

## 🆘 获取帮助

### 查看文档
```bash
# 查看详细文档
cat README.md

# 查看部署指南
cat DEPLOYMENT.md

# 查看集成指南
cat OPENCLAW_INTEGRATION.md
```

### 查看测试报告
```bash
cat TEST_REPORT.md
```

### 查看日志
```bash
# 系统日志
tail -f logs/system.log

# 错误日志
tail -f logs/error.log

# 压缩日志
tail -f logs/compaction.log
```

## 🎉 安装完成！

恭喜！上下文压缩技能已成功安装。现在您可以：

1. **启动系统**：`./start_system.sh`
2. **检查状态**：`./check_status.sh`
3. **开始使用**：系统会自动监控和优化您的对话上下文

享受高效的上下文管理吧！