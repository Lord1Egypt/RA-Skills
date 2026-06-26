# Code Analyzer Skill

**版本**: 1.0.0  
**作者**: sohot-gdjinni  
**标签**: `code-review`, `python`, `security`, `optimization`

---

## 简介

一个专业的 Python 代码分析与优化 Skill，提供：
- 语法检查与结构分析
- 安全漏洞扫描
- 性能优化建议
- 重构后的可直接使用代码

---

## 功能特性

| 功能 | 说明 |
|------|------|
| 🔍 **语法检查** | Python 语法验证、AST 结构分析 |
| 🛡️ **安全扫描** | 检测硬编码密钥、裸 except、SQL 注入等 |
| ⚡ **性能分析** | 识别低效循环、冗余计算、缓存机会 |
| 📊 **代码质量** | 复杂度评估、重复代码检测 |
| ✅ **修复版本** | 提供可直接使用的优化后代码 |

---

## 使用方法

### 1. 直接分析代码

```bash
# 分析单个文件
python3 -m code_analyzer analyze /path/to/your/code.py

# 分析目录
python3 -m code_analyzer analyze /path/to/project/ --recursive
```

### 2. 在 Python 中使用

```python
from code_analyzer import CodeAnalyzer

analyzer = CodeAnalyzer()
results = analyzer.analyze_file('your_code.py')

# 查看问题列表
for issue in results.issues:
    print(f"[{issue.severity}] {issue.message}")

# 获取修复建议
fixed_code = results.get_fixed_code()
```

### 3. 作为 Agent Skill 使用

当你需要分析代码时，直接粘贴代码给我，我会：

1. **语法检查** - 验证代码能否正常运行
2. **问题检测** - 找出安全/性能/质量问题
3. **分级报告** - P0(必须修复) / P1(重要) / P2(建议) / P3(可选)
4. **提供修复** - 给出可直接使用的优化版本

---

## 示例输出

### 输入代码
```python
def api_get(path):
    import urllib.request
    try:
        req = urllib.request.Request('https://api.example.com' + path)
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except:
        return None
```

### 分析结果

```
📊 代码分析报告
==================================================
函数数量: 1
类数量: 0
导入语句: 1

🔍 发现的问题:
  ⚠️ [P0] 使用裸 except: 可能隐藏所有异常
  ⚠️ [P1] 硬编码 API 地址
  ⚠️ [P1] 缺少超时设置
  ⚠️ [P2] 导入语句在函数内

✅ 优化建议:
  1. 使用具体的异常类型 (HTTPError, URLError)
  2. 添加 timeout 参数
  3. 将 import 移到文件顶部
```

### 修复后代码
```python
import json
import urllib.request
import urllib.error
from typing import Optional, Dict

API_BASE_URL = 'https://api.example.com'
DEFAULT_TIMEOUT = 15

def api_get(path: str, timeout: int = DEFAULT_TIMEOUT) -> Optional[Dict]:
    """发送 GET 请求"""
    try:
        req = urllib.request.Request(API_BASE_URL + path)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"HTTP错误: {e.code}")
        return None
    except urllib.error.URLError as e:
        print(f"连接错误: {e.reason}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None
```

---

## 检查规则

### P0 - 必须修复 (安全/稳定性)
- [x] **hardcoded_secrets** - 硬编码 API 密钥/密码/令牌
- [x] **bare_except** - 裸 `except:` 捕获所有异常
- [x] **sql_injection** - SQL 注入风险（字符串拼接/format/f-string）
- [x] **command_injection** - 命令注入（os.system/subprocess 使用动态字符串）
- [x] **dangerous_functions** - 危险函数（eval/exec/pickle/yaml.load/marshal）

### P1 - 重要 (可靠性)
- [x] **missing_timeout** - HTTP 请求未设置 timeout
- [x] **resource_leaks** - 锁 acquire 没有对应 release
- [x] **unclosed_files** - 文件打开后未关闭
- [x] **debug_code** - 调试代码（pdb 导入）

### P2 - 建议 (质量)
- [x] **missing_type_hints** - 函数参数/返回值缺少类型提示
- [x] **long_functions** - 函数超过 50 行
- [x] **unused_variables** - 变量被赋值但从未使用
- [x] **inline_imports** - 函数内导入
- [x] **debug_code** - print 调试语句
- [x] **hardcoded_urls** - 硬编码 URL/IP 地址

### P3 - 可选 (风格)
- [ ] 命名规范
- [ ] 文档字符串缺失
- [ ] 注释质量

---

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/code-analyzer-skill.git
cd code-analyzer-skill

# 安装依赖
pip install -r requirements.txt

# 可选：安装为系统命令
pip install -e .
```

---

## 配置

创建 `.code_analyzer.yaml`：

```yaml
# 忽略的文件/目录
exclude:
  - "*/venv/*"
  - "*/__pycache__/*"
  - "*/tests/*"

# 自定义规则
rules:
  max_line_length: 120
  max_function_lines: 50
  max_complexity: 10

# 严重性覆盖
severity:
  bare_except: "error"      # 裸 except 升级为错误
  missing_timeout: "warning" # 缺少超时降级为警告
```

---

## 工作原理

```
┌─────────────────────────────────────────┐
│           代码输入                       │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  1. 语法检查 (AST解析)                   │
│     - Python 语法验证                   │
│     - 结构分析                          │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  2. 静态分析                             │
│     - 安全扫描                          │
│     - 性能检测                          │
│     - 代码异味                          │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  3. 问题分级                             │
│     - P0/P1/P2/P3                       │
│     - 影响评估                          │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  4. 生成修复                             │
│     - 代码重构                          │
│     - 类型提示                          │
│     - 文档生成                          │
└─────────────────────────────────────────┘
```

---

## 贡献

欢迎贡献！请遵循以下流程：

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 致谢

基于以下开源项目构建：
- Python AST 模块
- Bandit (安全扫描)
- Radon (复杂度分析)

---

## 更新日志

### v1.0.0 (2026-03-21)
- 🎉 初始版本发布
- ✅ 基础语法检查
- ✅ 安全漏洞扫描
- ✅ 性能优化建议
- ✅ 修复代码生成
