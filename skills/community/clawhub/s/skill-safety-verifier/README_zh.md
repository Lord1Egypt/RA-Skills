# Skill Safety Verifier

**[English](README.md) | [中文](README_zh.md)**

> AI Agent 安全审查工具。在安装任何来自 ClawdHub、GitHub 或其他来源的 Skill 前进行安全检查。

## 为什么重要

AI Agent 以高级权限运行，可以：
- 执行任意命令
- 访问文件系统
- 发起网络请求
- 读取环境变量

**未经审查的 Skill = 安全风险**

## 功能特性

- 代码模式扫描 - 检测危险代码 (exec/eval/subprocess)
- GitHub Advisory API - 检查依赖项已知 CVE
- 权限分析 - 从配置文件分析所需权限
- 风险分类 - 将 Skill 分类为 Safe/Low/Medium/High
- Risk Radar 可视化 - 进度条 + 颜色评分

---

## 前置依赖

### Python 版本
- Python 3.8 或更高

### 必需依赖
```bash
# 方式 1: 通过 pip 安装
pip install -r requirements.txt

# 方式 2: 通过 setup.py 安装
pip install -e .

# 方式 3: 手动安装
pip install requests>=2.28.0
```

### 可选依赖（开发用）
```bash
pip install pytest pytest-cov
```

---

## 快速开始

### 安装

#### 方式 1: 克隆并安装
```bash
git clone https://github.com/ttttstc/skill-safety-verifier.git
cd skill-safety-verifier
pip install -e .
```

#### 方式 2: 通过 ClawdHub
```bash
npx skills add ttttstc/skill-safety-verifier
```

#### 方式 3: 直接下载使用
```bash
# 仅下载并使用
wget https://raw.githubusercontent.com/ttttstc/skill-safety-verifier/main/analyzer.py
wget https://raw.githubusercontent.com/ttttstc/skill-safety-verifier/main/risk_radar.py
```

### 使用

```bash
# 方式 1: 安装后使用
skill-safety-check /path/to/skill

# 方式 2: 直接 Python 运行
python analyzer.py /path/to/skill
python3 analyzer.py /path/to/skill

# 输出 JSON
python analyzer.py /path/to/skill --json

# 帮助
python analyzer.py --help
```

---

## 项目结构

```
skill-safety-verifier/
├── bin/                      # 入口脚本
│   └── skill-safety-check   # CLI 启动器
├── analyzer.py               # 主分析器
├── risk_radar.py             # Risk Radar 渲染器
├── requirements.txt           # Python 依赖
├── setup.py                  # 包配置
├── SKILL.md                  # OpenClaw skill 定义
├── README.md                 # 英文文档
├── README_zh.md              # 中文文档
└── LICENSE                  # MIT 许可证
```

---

## 工作流程

```
用户触发安装
    |
    v
1. 克隆 Skill 仓库
    |
    v
2. 并行扫描:
   - 扫描代码模式 (exec/eval/subprocess)
   - 检查 GitHub Advisory API
   - 分析权限
    |
    v
3. 计算风险评分
    |
    v
4. 渲染 Risk Radar
    |
    v
用户决定
```

---

## 风险分类

| 等级 | 分数 | 颜色 | 操作 |
|------|------|------|------|
| Safe | 0-10 | 绿色 | 自由安装使用 |
| Low | 11-30 | 黄色 | 谨慎安装 |
| Medium | 31-60 | 橙色 | 先审查代码 |
| High | 61-100 | 红色 | 禁止安装 |

---

## 输出示例

### 安全 Skill

```
skill-name - 风险评估

风险雷达:
  网络风险    0/50  绿色
  漏洞风险    0/25  绿色
  权限风险    0/50  绿色
  总分        0/100 绿色

建议: 安全，可安装
```

### 中风险 Skill

```
skill-name - 风险评估

风险雷达:
  网络风险    20/50 黄色
  漏洞风险    5/25  绿色
  权限风险    25/50 橙色
  总分        50/100 橙色

警告: 检测到网络调用
建议: 安装前先审查代码
```

---

## 配置

### 缓存目录
默认: `~/.cache/skill-safety/`

### 缓存 TTL
- Advisory 数据: 24 小时
- Skill 依赖: 6 小时

### GitHub API
- 无需认证（60 次/小时）
- 有认证: 5000 次/小时

---

## 集成

### 与 ClawdHub 集成

```bash
# 安装时自动验证
npx skills add <owner/repo> --verify
```

### 在你自己的流水线中

```python
from analyzer import analyze_skill

result = analyze_skill('/path/to/skill')
print(result['scores'])
# {'network': 0, 'vuln': 0, 'permission': 25, 'total': 25}
```

---

## 最佳实践

1. 始终验证 - 永远不要安装未经审查的 Skill
2. 阅读代码 - 自动检查不够，需要人工审查
3. 最小权限 - 只授予必要的权限
4. 隔离运行 - 在容器中运行高风险 Skill
5. 监控日志 - 记录所有 Skill 活动

---

## 常见问题

### "No module named 'requests'"
```bash
pip install requests
```

### "SSL certificate verify failed"
默认使用 SSL 验证。如果遇到问题，可以禁用 SSL 验证（生产环境不推荐）。

### "API rate limit exceeded"
等待一小时或使用 GitHub Token 提高速率限制。

---

## 相关链接

- ClawdHub (https://clawhub.com) - Skill 市场
- GitHub Advisory API (https://api.github.com/advisories)
- OpenClaw 文档 (https://docs.openclaw.ai)

---

## License

MIT License - see LICENSE file for details.
