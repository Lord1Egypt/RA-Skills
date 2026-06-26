# 🔒 Skill Security Scanner

自动扫描技能代码，识别安全风险（恶意模式、密钥泄露、危险函数），支持 VirusTotal API 集成。适用于ClawHub发布前的自动安全审查。

> **MVP in progress** - 预计 v0.1.0 即将发布

[![status](https://img.shields.io/badge/status-in%20development-yellow)](https://github.com/your-repo)

## ✨ 特性

- ✅ **静态代码分析** - 扫描 Python 代码文件，检测恶意模式
- ✅ **密钥泄露检测** - 发现硬编码的 API keys、passwords、tokens
- ✅ **危险函数识别** - 标记 eval、exec、subprocess shell=True 等危险用法
- ✅ **VirusTotal 集成** - 可选文件信誉检查（需要 API key）
- ✅ **多格式输出** - JSON（机器可读） + HTML（可视化仪表盘）
- ✅ **可配置严重程度** - low / medium / high / critical 阈值
- ✅ **零外部依赖** - 纯Python标准库，无需安装额外包

## 📦 安装

```bash
# ClawHub 自动安装（推荐）
clawhub install skill-secure-checker

# 或手动安装（待发布后可用）
# ./install.sh
```

## 🚀 快速开始

```bash
# 1. 扫描单个技能（JSON 报告）
skill-secure-checker skill_path="./skills/batch-renamer"

# 2. 生成 HTML 仪表盘（需要 frontend-design 美化）
skill-secure-checker skill_path="./skills/social-publisher" output_format=html

# 3. 包含 VirusTotal 文件扫描
export VT_API_KEY="your-virustotal-api-key"
skill-secure-checker skill_path="./skills/your-skill" virustotal_api_key="${VT_API_KEY}" output_format=both
```

## 🎯 命令参数

| 参数 | 类型 | 必填 | 默认值 | 描述 |
|------|------|------|--------|------|
| `skill_path` | string | ✅ | - | 要扫描的技能目录路径（绝对或相对） |
| `output_format` | string | ❌ | `json` | 输出格式：`json`、`html` 或 `both` |
| `virustotal_api_key` | string | ❌ | - | VirusTotal API key（可选，用于文件信誉扫描） |
| `severity_threshold` | string | ❌ | `low` | 最低严重程度报告：`low`、`medium`、`high`、`critical` |

## 📊 输出示例

```json
{
  "skill": "batch-renamer",
  "scan_time": "2026-03-28T06:30:00Z",
  "total_files": 12,
  "total_lines": 1456,
  "findings": 3,
  "risk_score": 45,
  "risk_level": "medium",
  "issues": [
    {
      "file": "source/renamer.py",
      "line": 123,
      "severity": "high",
      "type": "dangerous_function",
      "message": "Use of eval() detected - potential code injection",
      "snippet": "result = eval(user_input)"
    },
    {
      "file": "config.py",
      "line": 45,
      "severity": "critical",
      "type": "hardcoded_secret",
      "message": "Hardcoded API key found",
      "snippet": "API_KEY = \"sk-1234567890abcdef\""
    }
  ]
}
```

## 🔍 检测规则

### 危险函数
- `eval()`, `exec()`, `compile()`
- `__import__()` (动态导入)
- `subprocess.Popen(..., shell=True)`
- `os.system()` (外部命令执行)
- `pickle.loads()` (反序列化风险)

### 硬编码密钥
- 正则匹配类似 `api_key`, `secret`, `password`, `token`, `credentials` 的变量
- 检测常见格式：sk-, AIza, gh_, eyJ (JWT)
- 高熵字符串（随机字符序列）

### 网络操作
- 未验证的 URL 拼接
- HTTP 明文传输（应使用 HTTPS）
- 自签名证书禁用

### 文件操作
- 路径遍历风险（`../../../`）
- 临时文件不安全创建
- 日志文件敏感信息泄露

### VirusTotal（可选）
- 扫描技能包中的二进制文件和脚本
- 检查文件哈希信誉
- 需要 VT API key（免费版限频）

## 🎨 HTML 仪表盘

如果 `frontend-design` 技能已安装，HTML报告将包含美观的界面：
- 风险等级可视化
- 问题分布图表
- 可折叠的详细问题列表
- 响应式设计

```bash
skill-secure-checker skill_path="./your-skill" output_format=html
```

## 🔌 与 ClawHub 集成

作为 pre-publish hook 自动运行：

```bash
# 配置 pre-publish hook
clawhub config set hooks.pre_publish="skill-secure-checker skill_path=. output_format=json severity_threshold=medium"

# 发布时自动扫描
clawhub publish
# 如果 risk_level >= high，发布将被阻止（需要覆盖 --force）
```

## 🏗️ 开发状态

| 版本 | 状态 | 完成 |
|------|------|------|
| v0.1.0 (MVP) | 🚧 开发中 | ~60% |
| - 基础扫描引擎 | ✅ 完成 | |
| - 危险函数检测 | ✅ 完成 | |
| - 硬编码密钥检测 | 🚧 部分 | |
| - HTML报告生成 | 📝 待开始 | |
| - VirusTotal集成 | 📝 待开始 | |
| - ClawHub hook | 📝 待开始 | |

## 🧪 测试

```bash
# 运行单元测试（待创建）
pytest tests/

# 扫描测试样本
skill-secure-checker skill_path="./tests/sample-malicious-skill" severity_threshold=low
```

## 📝 故障排除

**Error: skill_path not found**
- 确认路径存在且可读
- 使用绝对路径避免相对路径问题

**VirusTotal API rate limit exceeded**
- 免费版限制 500 次/天
- 升级到 VT 高级版或等待限额重置

**Memory error on large skills**
- 增加系统内存或减少同时扫描的文件数
- 分目录多次扫描

**HTML report not beautified**
- 确保 frontend-design 技能已安装
- 或手动编辑 templates/report.html

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 👤 作者

**小叮当** - 智能体总体指挥中心

---

**注**: 本技能仍在开发中，建议仅在测试环境使用。生产环境请等待 v1.0.0 正式版。