# Skill Tracker 📊

**通用技能使用统计追踪器** - 为 OpenClaw 技能提供使用情况统计和追踪功能

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/openclaw/skill-tracker)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://openclaw.ai)

---

## ✨ 特性

- **⚡ 非阻塞异步** - 调用延迟 <0.5ms，不影响技能执行
- **🔒 异常隔离** - 追踪失败不影响主流程
- **🔄 重试机制** - 3 次重试，抗瞬时故障
- **📈 耗时统计** - 记录执行时间，分析性能
- **🔐 并发安全** - 文件锁 + 原子写入
- **⚙️ 灵活配置** - 数据目录、重试次数、日志级别
- **📊 统计报告** - 调用次数、成功率、排行
- **🌐 双语言** - Python + Node.js 支持

---

## 📦 安装

### Python 版

**方式 1：直接复制（推荐）**
```bash
# 复制 skill_tracker.py 到项目
cp skill_tracker.py /path/to/your/project/
```

**方式 2：pip 安装（即将发布）**
```bash
pip install skill-tracker
```

### Node.js 版

**方式 1：直接复制（推荐）**
```bash
# 复制 index.js 到项目
cp index.js /path/to/your/project/
```

**方式 2：npm 安装（即将发布）**
```bash
npm install skill-tracker
```

---

## 🚀 快速开始

### Python 示例

```python
from skill_tracker import track
import time

start_time = time.time()

# 记录调用（非阻塞，立即返回）
track('my-skill', 'call', {
    'user': '韩先生',
    'start_time': start_time
})

try:
    # 执行技能逻辑
    result = execute_skill()
    
    # 记录成功
    track('my-skill', 'success', {
        'duration': int((time.time() - start_time) * 1000)
    })
    
except Exception as e:
    # 记录失败
    track('my-skill', 'fail', {
        'error': str(e),
        'duration': int((time.time() - start_time) * 1000)
    })
    raise
```

### Node.js 示例

```javascript
const tracker = require('skill-tracker');

const startTime = Date.now();

// 记录调用（非阻塞）
tracker.track('my-skill', 'call', {
    user: '韩先生',
    startTime: startTime
});

try {
    const result = await executeSkill();
    
    // 记录成功
    tracker.track('my-skill', 'success', {
        duration: Date.now() - startTime
    });
    
} catch (err) {
    // 记录失败
    tracker.track('my-skill', 'fail', {
        error: err.message,
        duration: Date.now() - startTime
    });
    throw err;
}
```

### 查看报告

**命令行：**
```bash
# Python
python skill_tracker.py report

# Node.js
node -e "const t=require('./index.js'); t.getReport().then(console.log)"
```

**OpenClaw 指令：**
```
技能统计
调用统计
skill 排行
使用报告
```

---

## 📖 API 参考

### `track(skillName, action, context)`

记录技能调用

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `skillName` | string | ✅ | 技能名称 |
| `action` | string | ❌ | 动作类型：`call` / `success` / `fail`，默认 `call` |
| `context` | object | ❌ | 上下文信息 |

**context 对象：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `user` | string | 用户标识，默认 "韩先生" |
| `channel` | string | 渠道，默认 "feishu" |
| `session_id` | string | 会话 ID |
| `start_time` | datetime | 开始时间（用于计算耗时） |
| `duration` | int | 执行耗时（毫秒） |
| `success` | boolean | 是否成功 |
| `error` | string | 错误信息 |

**返回值：** `None`（非阻塞，立即返回）

**注意事项：**
- 调用立即返回，不阻塞主流程
- 数据在后台线程写入
- 异常已隔离，不影响技能执行

---

## ⚙️ 配置

### Python

```python
from skill_tracker import configure

configure(
    data_dir='/var/log/skill-tracker',  # 数据目录
    max_retries=5,                       # 最大重试次数
    retry_delay=0.2,                     # 重试延迟（秒）
    log_level='DEBUG',                   # 日志级别
    enable_logging=True                  # 是否启用日志
)
```

### Node.js

```javascript
const tracker = require('skill-tracker');

tracker.configure({
  dataDir: '/var/log/skill-tracker',
  maxRetries: 5,
  retryDelay: 200,
  logLevel: 'debug',
  enableLogging: true
});
```

### 配置项说明

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `data_dir` | `data/` | 数据文件存储目录 |
| `max_retries` | `3` | 写入失败时的重试次数 |
| `retry_delay` | `0.1s` | 重试间隔 |
| `log_level` | `INFO` | 日志级别：DEBUG/INFO/WARNING/ERROR |
| `enable_logging` | `true` | 是否启用日志输出 |

---

## 📊 数据格式

### skill-stats.json

聚合统计数据：
```json
{
  "totalCalls": 156,
  "skills": {
    "nano-banana-pro": {
      "calls": 45,
      "success": 44,
      "fail": 1,
      "totalDuration": 56250,
      "avgDuration": 1250,
      "firstUsed": "2026-03-18T10:00:00",
      "lastUsed": "2026-03-18T13:48:00"
    }
  },
  "lastUpdated": "2026-03-18T13:48:00"
}
```

### usage-log.jsonl

原始调用日志（每行一条）：
```json
{"timestamp":"2026-03-18T13:48:11","date":"2026-03-18","skill":"nano-banana-pro","action":"success","duration_ms":1250,"context":{"user":"韩先生","channel":"feishu","success":true,"error":null}}
```

---

## 🧪 测试

### Python

```bash
# 运行测试
python -m pytest tests/

# 或手动测试
python skill_tracker.py test
```

### Node.js

```bash
# 运行测试
npm test

# 或手动测试
node test.js
```

---

## 📁 项目结构

```
skill-tracker/
├── README.md               # 本文档
├── LICENSE                 # MIT 许可证
├── CHANGELOG.md            # 更新日志
├── skill_tracker.py        # Python 版追踪器
├── index.js                # Node.js 版追踪器
├── setup.py                # Python 打包配置
├── package.json            # Node.js 打包配置
├── config.yaml             # 配置文件示例
├── tests/
│   ├── test_python.py      # Python 测试
│   └── test_node.js        # Node.js 测试
└── data/
    ├── skill-stats.json    # 统计数据
    └── usage-log.jsonl     # 原始日志
```

---

## 🔒 隐私与安全

- ✅ **本地存储** - 所有数据存储在本地
- ✅ **不上传** - 不会发送到外部服务器
- ✅ **无外部依赖** - 纯本地运行
- ✅ **开源透明** - 代码完全开源

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/openclaw/skill-tracker.git
cd skill-tracker

# Python 测试
pip install pytest
pytest tests/

# Node.js 测试
npm install
npm test
```

---

## 📞 联系

- **作者：** aiyst (@aiyst1982)
- **邮箱：** aiyst@qq.com
- **GitHub：** https://github.com/aiyst1982
- **Issue：** https://github.com/openclaw/skill-tracker/issues
- **讨论：** https://github.com/openclaw/skill-tracker/discussions

---

**📊 让数据驱动您的技能优化决策！**
