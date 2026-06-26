# skill-secure-checker - 技能安全扫描器🔒

自动扫描技能代码，识别安全风险（恶意模式、密钥泄露、危险函数），支持 VirusTotal API 集成。适用于ClawHub发布前的自动安全审查。

## 功能特性

✅ **静态代码分析** - 扫描 Python 代码文件，检测恶意模式
✅ **密钥泄露检测** - 发现硬编码的 API keys、passwords、tokens
✅ **危险函数识别** - 标记 eval、exec、subprocess shell=True 等危险用法
✅ **VirusTotal 集成** - 可选文件信誉检查（需要 API key）
✅ **多格式输出** - JSON（机器可读） + HTML（可视化仪表盘）
✅ **可配置严重程度** - low / medium / high / critical 阈值
✅ **零外部依赖** - 纯Python标准库，无需安装额外包

## 安装

```bash
# ClawHub 自动安装（推荐）
clawhub install skill-secure-checker

# 或手动安装
git clone <skill-repo>
cd skill-secure-checker
./install.sh
```

## 使用方法

### 基础扫描（JSON报告）

```bash
skill-secure-checker skill_path="./skills/batch-renamer"
```

### 生成HTML仪表盘

```bash
skill-secure-checker skill_path="./skills/social-publisher" output_format=html
```

### 同时生成两种格式

```bash
skill-secure-checker skill_path="./skills/xiaohongshu-proxy-manager" output_format=both
```

### 启用VirusTotal文件扫描

```bash
export VT_API_KEY="your-virustotal-api-key"
skill-secure-checker skill_path="./skills/your-skill" virustotal_api_key="${VT_API_KEY}" output_format=html
```

### 设置严重程度阈值（只报告 medium 及以上）

```bash
skill-secure-checker skill_path="./skills/your-skill" severity_threshold="medium"
```

## 输出示例

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

## 风险等级计算

- **risk_score** = 基于发现的问题数量和严重程度的加权分数
- **risk_level**：low (0-20) | medium (21-50) | high (51-80) | critical (81-100)

| 严重程度 | 权重 |
|---------|------|
| low     | 1    |
| medium  | 5    |
| high    | 20   |
| critical| 50   |

## 检测规则

### 1. 危险函数
- `eval()`, `exec()`, `compile()`
- `__import__()` (动态导入)
- `subprocess.Popen(..., shell=True)`
- `os.system()` (外部命令执行)
- `pickle.loads()` (反序列化风险)

### 2. 硬编码密钥
- 正则匹配类似 `api_key`, `secret`, `password`, `token`, `credentials` 的变量
- 检测常见格式：sk-, AIza, gh_, eyJ (JWT)
- 高熵字符串（随机字符序列）

### 3. 网络操作
- 未验证的 URL 拼接
- HTTP 明文传输（应使用 HTTPS）
- 自签名证书禁用

### 4. 文件操作
- 路径遍历风险（`../../../`）
- 临时文件不安全创建
- 日志文件敏感信息泄露

### 5. VirusTotal（可选）
- 扫描技能包中的二进制文件和脚本
- 检查文件哈希信誉
- 需要 VT API key（免费版限频）

## 与 ClawHub 集成

该技能可以作为 `clawhub publish` 的 pre-publish hook 自动运行：

```bash
# 配置 pre-publish hook（示例）
clawhub config set hooks.pre_publish="skill-secure-checker skill_path=. output_format=json severity_threshold=medium"

# 发布时自动扫描
clawhub publish
# 如果风险等级 >= high，发布将被阻止
```

## 生产环境建议

1. **所有技能发布前必须扫描** - 作为持续集成的一部分
2. **HTML仪表盘存档** - 每次发布保留扫描报告
3. **定期扫描已发布技能** - 检测新发现的安全问题
4. **设置团队安全政策** - 定义可接受的风险等级
5. **结合 skill-validator** - 先保证代码规范，再检查安全

## 技术实现

- 纯Python标准库（`ast`, `re`, `json`, `os`, `pathlib`）
- AST 遍历分析（比正则更安全准确）
- 多线程扫描（大项目性能优化）
- HTML报告使用 frontend-design 美学（可选）

## 限制

- 仅扫描 Python 代码（其他语言暂不支持）
- VirusTotal API 有请求频率限制（免费版 500次/天）
- 无法检测运行时行为（仅静态分析）

## 下一步计划

- [ ] 支持 JavaScript/TypeScript 扫描
- [ ] 集成 OWASP Dependency-Check（第三方包漏洞）
- [ ] 自动修复建议（如替换 eval 为 ast.literal_eval）
- [ ] Diff 模式（对比两次扫描的差异）
- [ ] Slack/Discord 通知集成

## 故障排除

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

---

**License**: MIT
**Author**: 小叮当
**Version**: 0.1.0 (MVP in development)