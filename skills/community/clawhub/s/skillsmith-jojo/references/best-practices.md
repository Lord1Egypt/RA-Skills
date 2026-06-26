# 技能设计最佳实践
## JOJO's Workshop 内部指南

---

## 一、SKILL.md 写作规范

### Frontmatter 必填字段

```yaml
---
name: skill-name
description: |
  技能描述，包含：
  1. 功能说明
  2. 触发场景（用户会说什么）
  3. 使用时机
  4. 与其他技能的区别
metadata:
  openclaw:
    emoji: "🔧"
---

# Body 内容
```

### Description 黄金公式

**触发词 + 功能 + 使用场景 + 排除场景**

```yaml
description: |
  技能功能描述。

  使用场景：
  - 用户说"帮我XXX"
  - 用户说"YYY"

  何时触发：
  - 当用户需要XXX时

  何时不触发：
  - 当用户需要其他功能时
```

---

## 二、脚本设计规范

### 必须包含的元素

```python
#!/usr/bin/env python3
"""
脚本名称
功能描述
"""

import sys
import argparse
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='脚本描述')
    parser.add_argument('--input', '-i', required=True, help='输入文件')
    parser.add_argument('--output', '-o', help='输出文件')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    return parser.parse_args()

def check_dependencies():
    """检查依赖"""
    return True

def main():
    """主函数"""
    args = parse_args()
    logger.info("开始执行")
    
    # TODO: 实现具体功能
    
    logger.info("执行完成")
    sys.exit(0)

if __name__ == '__main__':
    main()
```

### 用户友好输出规范

| 状态 | 前缀 | 示例 |
|------|------|------|
| 成功 | ✅ | ✅ 提交成功 |
| 失败 | ❌ | ❌ 文件不存在 |
| 警告 | ⚠️ | ⚠️ 文件已存在 |
| 进度 | 🔄 | 🔄 正在处理... |
| 信息 | ℹ️ | ℹ️ 共 3 个文件 |

### 错误处理模板

```python
try:
    result = do_something()
    print(f"✅ 成功: {result}")
    sys.exit(0)
except FileNotFoundError:
    print("❌ 文件不存在，请检查路径")
    sys.exit(1)
except PermissionError:
    print("❌ 权限不足，请以管理员身份运行")
    sys.exit(1)
except Exception as e:
    print(f"❌ 未知错误: {e}")
    sys.exit(1)
```

---

## 三、目录结构规范

### 标准结构

```
skill-name/
├── SKILL.md              # 必需：技能定义
├── scripts/              # 可选：脚本目录
│   ├── main.py          # 主脚本
│   ├── utils.py         # 工具函数
│   └── config.py        # 配置
├── references/          # 可选：参考文档
│   ├── api.md          # API 文档
│   ├── examples.md    # 使用示例
│   └── patterns.md    # 模式库
└── assets/              # 可选：模板文件
    ├── template.xlsx    # Excel 模板
    └── config.json      # 默认配置
```

### 何时使用各目录

| 目录 | 使用时机 | 示例 |
|------|---------|------|
| scripts/ | 需要确定性执行时 | API调用、文件操作 |
| references/ | 文档超过100行时 | API文档、详细指南 |
| assets/ | 需要模板文件时 | Excel模板、图片 |

---

## 四、Token 优化策略

### 渐进式披露

```
Level 1: Frontmatter (~100 tokens)
         → 始终在上下文中
         → 决定技能是否触发

Level 2: SKILL.md body (~500-1500 tokens)
         → 技能触发时加载
         → 包含核心工作流

Level 3: references/ (无限制)
         → 按需加载
         → 包含详细文档

Level 4: scripts/ (无限制)
         → 执行时不加载
         → 包含可执行代码
```

### 优化检查清单

| 问题 | 解决方案 | Token节省 |
|------|---------|---------|
| SKILL.md过大 | 拆分到references/ | 50-80% |
| 重复代码 | 移至scripts/ | 30-60% |
| 冗长说明 | 改用表格 | 20-40% |
| 多语言内容 | 只保留目标语言 | 30-50% |

---

## 五、质量检查清单

### 发布前必须通过

| 检查项 | 命令 | 标准 |
|--------|------|------|
| 结构完整性 | `python skill-test.py` | 全部通过 |
| 安全审查 | `python security-check.py` | 无EXTREME/HIGH |
| Token效率 | `python token-analyzer.py` | 评级A或B |
| 描述完整性 | 人工检查 | 包含触发词 |
| 脚本可执行 | 实际运行 | 无报错 |

### 自检问题清单

- [ ] SKILL.md 有正确的 YAML frontmatter？
- [ ] description 包含触发场景？
- [ ] 所有脚本有错误处理？
- [ ] 所有命令有使用示例？
- [ ] 安全检查通过？
- [ ] Token 评级达到 B 以上？

---

## 六、常见反模式

### ❌ 应该避免的

```markdown
<!-- 过于冗长的描述 -->
这个技能可以帮你做很多事情，包括但是不限于...（500字）

<!-- 过于模糊的触发词 -->
用户说"帮帮我"（太模糊，无法触发）

<!-- 缺少错误处理 -->
try:
    do_something()
except:
    pass  # 太糟糕
```

### ✅ 推荐做法

```markdown
<!-- 简洁明确的描述 -->
天气查询技能，获取实时天气和预报。

<!-- 明确的触发词 -->
- 用户说"今天天气怎么样"
- 用户说"明天会下雨吗"

<!-- 完善的错误处理 -->
try:
    result = api.call()
except TimeoutError:
    print("⚠️ 请求超时，请检查网络")
    sys.exit(1)
```

---

## 七、版本管理

### 版本号规范

| 变更类型 | 版本升级 | 示例 |
|---------|---------|------|
| 重大功能 | Major (x.0.0) | 1.0.0 → 2.0.0 |
| 新功能 | Minor (0.x.0) | 1.0.0 → 1.1.0 |
| Bug修复 | Patch (0.0.x) | 1.0.0 → 1.0.1 |

### CHANGELOG 模板

```markdown
## [版本号] - 日期

### 新增
- 功能A
- 功能B

### 改进
- 性能优化
- 文档完善

### 修复
- Bug #123
- Bug #456
```

---

## 八、测试指南

### 单元测试模板

```python
import unittest

class TestMySkill(unittest.TestCase):
    def test_basic_function(self):
        result = basic_function("input")
        self.assertEqual(result, "expected")
    
    def test_error_handling(self):
        with self.assertRaises(ValueError):
            error_function("invalid")

if __name__ == '__main__':
    unittest.main()
```

### 测试覆盖标准

| 覆盖率 | 评级 |
|--------|------|
| 80%+ | ⭐⭐⭐ 优秀 |
| 60-80% | ⭐⭐ 良好 |
| 40-60% | ⭐ 合格 |
| <40% | ❌ 不达标 |

---

*JOJO's Workshop · 完美主义标准*
*最后更新: 2026-03-21*
