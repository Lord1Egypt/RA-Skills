# Code Analyzer Skill 🔍

专业的 Python 代码分析与优化工具，为你的代码提供安全检查、性能优化建议和自动化重构。

## ✨ 特性

- **语法检查** - Python AST 解析，精准定位语法错误
- **安全扫描** - 检测硬编码密钥、裸 except、注入漏洞等安全隐患
- **性能分析** - 识别低效代码、冗余计算、缓存机会
- **代码质量** - 复杂度评估、重复代码检测、类型提示检查
- **自动修复** - 生成可直接使用的优化后代码

## 🚀 快速开始

### 作为 OpenClaw Skill 使用

直接粘贴代码给我，我会：
1. 语法检查
2. 问题检测（分级 P0/P1/P2/P3）
3. 生成修复版本

### 命令行使用

```bash
# 分析单个文件
python3 analyzer.py your_code.py

# JSON 格式输出
python3 analyzer.py your_code.py --format json
```

### 在 Python 中使用

```python
from analyzer import CodeAnalyzer

analyzer = CodeAnalyzer()
result = analyzer.analyze_file('your_code.py')

# 查看 P0 级别问题
from analyzer import Severity
p0_issues = result.get_by_severity(Severity.P0)

# 生成报告
print(analyzer.generate_report(result))
```

## 📊 示例输出

```
📊 代码分析报告
==================================================
文件: /workspace/caishen_v5_detector.py

📈 统计信息:
  函数数量: 13
  类数量: 0
  导入数量: 8

🔍 发现的问题:
  [P0] 第15行: 发现硬编码 API_KEY，存在安全风险
      💡 建议: 使用环境变量: API_KEY = os.getenv('API_KEY')
  [P0] 第89行: 使用裸 'except:' 会捕获所有异常
      💡 建议: 使用具体的异常类型
  [P1] 第156行: urllib.request.urlopen 缺少 timeout 参数
      💡 建议: 添加 timeout 参数，如 timeout=15
```

## 📋 检查规则

### P0 - 必须修复 (安全/稳定性)

| 规则 | 说明 | 示例 |
|------|------|------|
| **hardcoded_secrets** | 硬编码 API_KEY/SECRET/PASSWORD | `API_KEY = "sk-xxx"` |
| **bare_except** | 裸 `except:` 捕获所有异常 | `except:` |
| **sql_injection** | SQL 注入风险（字符串拼接） | `cursor.execute(f"SELECT * FROM t WHERE id = {user_id}")` |
| **command_injection** | 命令注入风险 | `os.system(f"ls {user_input}")` |
| **dangerous_functions** | 危险函数（eval/exec/pickle） | `eval(user_input)` |

### P1 - 重要 (可靠性)

| 规则 | 说明 | 示例 |
|------|------|------|
| **missing_timeout** | HTTP 请求未设置 timeout | `urllib.request.urlopen(url)` |
| **resource_leaks** | 锁 acquire 没有 release | `lock.acquire()` |
| **unclosed_files** | 文件打开后未关闭 | `f = open("file.txt")` |
| **debug_code** | 调试代码（pdb 导入） | `import pdb` |

### P2 - 建议 (质量)

| 规则 | 说明 | 示例 |
|------|------|------|
| **missing_type_hints** | 函数参数/返回值无类型提示 | `def func(x):` |
| **long_functions** | 函数超过 50 行 | 函数体 > 50 行 |
| **unused_variables** | 变量被赋值但从未使用 | `x = 10`（未使用） |
| **inline_imports** | 函数内导入 | `def f(): import os` |
| **debug_code** | print 语句 | `print("debug")` |
| **hardcoded_urls** | 硬编码 URL/IP | `url = "http://api.example.com"` |

### P3 - 可选 (风格)

| 规则 | 说明 |
|------|------|
| 代码格式 | PEP 8 风格检查 |
| 命名规范 | 变量/函数命名 |

## 🛠️ 安装

```bash
git clone https://github.com/yourusername/code-analyzer-skill.git
cd code-analyzer-skill

# 无需安装依赖，纯标准库实现
python3 example.py
```

## 📁 项目结构

```
code-analyzer/
├── SKILL.md          # Skill 文档
├── analyzer.py       # 核心分析器
├── example.py        # 使用示例
├── requirements.txt  # 依赖（空，纯标准库）
├── LICENSE           # MIT 许可证
└── .gitignore        # Git 忽略文件
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📝 许可证

[MIT](LICENSE) © sohot-gdjinni

## 🙏 致谢

灵感来自：
- Bandit (Python 安全扫描)
- Pylint (代码质量检查)
- Black (代码格式化)
