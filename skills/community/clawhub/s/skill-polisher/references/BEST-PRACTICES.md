# Skill 最佳实践

## 文档编写

### SKILL.md 结构

```markdown
---
name: skill-name
description: "当用户需要...时使用。支持..."
metadata:
  author: xxx
  version: "1.0"
---

# Skill 标题

一句话描述。

## 快速开始

最常用的命令放在最前面。

```bash
python3 scripts/main.py --help
```

## 核心功能

### 功能 A
...

### 功能 B
...

## 参考

- [references/xxx.md](references/xxx.md)
```

### description 写作

好的 description：
- ✅ "当用户需要审查代码、检查代码质量、查找潜在问题时使用"
- ✅ "系统化代码审查工具，提供检查清单、陷阱检测和审查报告生成"

不好的 description：
- ❌ "这是一个代码审查工具"
- ❌ "用于代码审查"

### 命名规范

- 技能名：`lowercase-with-hyphens`
- 脚本名：`动词-名词.py`，如 `collect-feedback.py`
- 函数名：`snake_case`
- 常量名：`UPPER_CASE`

## 脚本设计

### 错误处理模板

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

def main():
    try:
        result = do_something()
        print(json.dumps(result))
        return 0
    except FileNotFoundError as e:
        print(f"错误: 文件不存在 - {e.filename}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    exit(main())
```

### 参数解析模板

```python
import argparse

parser = argparse.ArgumentParser(description="简短描述")
parser.add_argument("--skill", "-s", required=True, help="技能名称")
parser.add_argument("--output", "-o", choices=["text", "json"], default="text")
parser.add_argument("--dry-run", "-n", action="store_true")
args = parser.parse_args()
```

## 数据存储

### 核心原则：用户数据与技能代码分离

**必须遵守**：所有用户个人数据、项目信息、隐私内容**绝对不能**存放在技能目录内。

```
~/.openclaw/workspace/
├── .skill-name/              ← 用户数据（隐私，不同步）
│   ├── feedback/
│   ├── config/
│   └── logs/
└── skills/skill-name/        ← 技能代码（可同步到 clawhub）
    ├── SKILL.md
    ├── scripts/
    └── references/
```

### 为什么重要？

1. **隐私保护**：用户反馈、项目信息不会泄露到公共仓库
2. **技能可共享**：技能目录可以安全地发布到 clawhub
3. **多用户安全**：不同用户的数据互不干扰

### 正确示例

```python
from pathlib import Path

# ✅ 正确：用户数据放在 workspace 下的隐藏目录
def get_data_dir() -> Path:
    return Path.home() / ".openclaw/workspace/.my-skill"

# ❌ 错误：用户数据放在技能目录内
def get_data_dir_wrong() -> Path:
    return Path(__file__).parent.parent / "user-data"
```

### 数据分类

| 类型 | 存放位置 | 示例 |
|------|----------|------|
| **用户数据** | `~/.openclaw/workspace/.skill-name/` | 反馈记录、配置、日志 |
| **技能代码** | `~/.openclaw/workspace/skills/skill-name/` | SKILL.md、脚本、文档 |
| **项目数据** | 项目目录内 | 生成的报告、分析结果 |

## 反馈收集

### 在脚本结尾添加

```python
# scripts/xxx.py 结尾
import subprocess
import sys

def collect_feedback():
    try:
        subprocess.run([
            "python3",
            "~/.openclaw/workspace/skills/skill-polisher/scripts/collect-feedback.py",
            "--skill", "your-skill-name"
        ], timeout=30)
    except Exception:
        pass  # 反馈收集失败不影响主流程

if __name__ == "__main__":
    result = main()
    collect_feedback()
    sys.exit(result)
```

## 版本管理

### 版本号规则

- `0.x` - 开发阶段
- `1.0` - 第一个稳定版本
- `x.y` - 功能更新
- `x.y.z` - Bug 修复

### 更新 SKILL.md

每次打磨后更新 version 字段：

```yaml
metadata:
  version: "1.1"  # 打磨后递增
```

## 常见模式

### 批量处理

```python
from concurrent.futures import ThreadPoolExecutor

def process_items(items, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(process_one, items)
    return list(results)
```

### 进度显示

```python
import sys

def progress(current, total, message=""):
    pct = current / total * 100
    sys.stderr.write(f"\r{message}: {pct:.1f}% ({current}/{total})")
    sys.stderr.flush()
```

### 缓存机制

```python
import json
import hashlib
from pathlib import Path

def get_cache_path(key: str) -> Path:
    cache_dir = Path.home() / ".cache/skill-name"
    cache_dir.mkdir(parents=True, exist_ok=True)
    filename = hashlib.md5(key.encode()).hexdigest() + ".json"
    return cache_dir / filename
```
