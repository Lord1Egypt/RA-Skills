# system-healthcheck 快速安装指南

## 1. 安装

### 方式 A: 通过 ClawHub（推荐）

```bash
clawhub install system-healthcheck
```

### 方式 B: 手动安装

```bash
# 克隆或复制到 OpenClaw skills 目录
cp -r /path/to/system-healthcheck ~/.openclaw/skills/

# 或从 Git 克隆
git clone https://github.com/your-username/system-healthcheck.git ~/.openclaw/skills/system-healthcheck
```

---

## 2. 验证安装

```bash
cd ~/.openclaw/skills/system-healthcheck

# 运行测试脚本
./scripts/test.sh

# 或手动测试
python scripts/l1_fast_check.py
python scripts/l2_hourly_check.py
```

---

## 3. 配置 Crontab

### 3.1 查看示例配置

```bash
cat templates/crontab_example.txt
```

### 3.2 编辑 Crontab

```bash
crontab -e
```

### 3.3 添加以下配置（修改路径）

```bash
# 环境变量
PYTHON=/usr/bin/python3
HEALTHCHECK_DIR=$HOME/.openclaw/skills/system-healthcheck
WORKSPACE=$HOME/.openclaw/workspace

# L2 小时级检查（每小时）
0 * * * * cd $HEALTHCHECK_DIR && $PYTHON scripts/l2_hourly_check.py >> $WORKSPACE/logs/healthcheck.log 2>&1

# 心跳检查（每 30 分钟）
*/30 * * * * cd $HEALTHCHECK_DIR && $PYTHON scripts/heartbeat.py >> $WORKSPACE/logs/heartbeat.log 2>&1
```

### 3.4 验证 Crontab

```bash
# 查看已配置的任务
crontab -l

# 查看系统 Cron 服务状态
systemctl status cron  # Linux
# 或
launchctl list | grep cron  # macOS
```

---

## 4. 自定义配置

编辑 `config/default_config.yaml`：

```yaml
# 修改语言
i18n:
  locale: zh-CN  # 或 en, zh-TW, ja, ko

# 修改阈值
thresholds:
  disk_warning: 85      # 85% 警告
  memory_warning_mb: 256  # 256MB 警告
```

---

## 5. 集成到 OpenClaw

### 5.1 自动 L1 检查（对话前）

在 OpenClaw 的会话初始化脚本中添加：

```python
import subprocess
from pathlib import Path

healthcheck_dir = Path.home() / ".openclaw" / "skills" / "system-healthcheck"
result = subprocess.run(
    ["python", str(healthcheck_dir / "scripts" / "l1_fast_check.py")],
    capture_output=True, text=True, timeout=1
)

if result.returncode != 0:
    print(f"⚠️ Warning: {result.stdout}")
```

### 5.2 心跳机制

心跳检查已设计为智能输出：
- 工作时间（9-18 点）：有问题时输出，正常时输出 `HEARTBEAT_OK`
- 非工作时间：静默

---

## 6. 常见问题

### Q: 提示找不到 Python
A: 修改 crontab 中的 `PYTHON` 路径：
```bash
which python3  # 查看 Python 路径
```

### Q: Cron 服务未运行
A: 启动 Cron 服务：
```bash
# Linux
sudo systemctl start cron
sudo systemctl enable cron

# macOS
sudo launchctl load -w /System/Library/LaunchDaemons/com.vix.cron.plist
```

### Q: 输出乱码
A: 确保终端支持 UTF-8：
```bash
export LANG=en_US.UTF-8  # 或 zh_CN.UTF-8
```

### Q: 如何禁用某项检查？
A: 编辑 `config/default_config.yaml`，设置 `enabled: false`

---

## 7. 卸载

```bash
# 删除技能目录
rm -rf ~/.openclaw/skills/system-healthcheck

# 移除 crontab 配置
crontab -e
# 删除相关行

# 清理日志（可选）
rm ~/.openclaw/workspace/logs/healthcheck*.log
```

---

## 8. 更新

```bash
# ClawHub 安装
clawhub update system-healthcheck

# 或手动更新
cd ~/.openclaw/skills/system-healthcheck
git pull  # 如果是 Git 安装
```

---

## 9. 获取帮助

```bash
# 查看脚本帮助
python scripts/l2_hourly_check.py --help

# 查看文档
cat README.md
cat README.zh-CN.md
```

---

## 10. 下一步

- ✅ 完成安装和基础测试
- 📅 配置 Crontab 定时检查
- 🔧 根据需求调整阈值
- 🌍 添加更多语言支持
- 🔌 开发自定义检查插件

---

**祝使用愉快！** 🦞
