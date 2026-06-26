# splitsym - 注释即文档

## 核心理念

> **"代码未动，注释先行"** — 通过注释快速理解代码意图

这个工具的本质是：**从代码中提取注释，作为理解代码的快捷入口**。

## 适用场景

### 1. 快速代码审查
```
# 不用逐行读代码，直接看注释就知道功能
splitsym large_file.py | head -50
```

### 2. 遗留代码理解
```
# 注释规范的项目，注释就是文档
splitsym legacy_module.py
```

### 3. 生成文档摘要
```
# 提取所有注释，生成代码结构概览
splitsym src/ --config custom.json
```

## 示例对比

**传统方式：** 逐行阅读 2000 行代码 → 耗时 30 分钟

**使用 splitsym：**
```bash
$ splitsym mymodule.py
   123      PAIR: Authentication module - handles JWT token validation
   456    # Validate user credentials against LDAP
   789      PAIR: Rate limiter - prevents brute force attacks
   901    # Check if IP is in whitelist
```

## 支持的注释风格

| 语言/格式 | 单行注释 | 多行注释 |
|-----------|----------|----------|
| Python | `# comment` / `"""docstring"""` | `"""..."""` |
| JavaScript | `// comment` | `/* ... */` |
| HTML/XML | `<!-- comment -->` | 同左 |
| SQL | `-- comment` | - |
| Shell | `# comment` | - |

## 实际使用

```bash
# 安装
uv pip install splitsym

# 或者直接运行脚本
python splitsym.py your_file.py

# 指定行范围
splitsym large_file.py --lines 100-500

# 自定义配置
splitsym file.rs --config my_symbols.json
```

## 配置说明

`symbols.json` 定义了不同文件类型的注释提取规则：

```json
{
  "symbols": {
    "line": [...],   // 单行注释规则
    "pair": [...]    // 多行注释块规则
  },
  "fallback": {...}  // 默认规则
}
```
