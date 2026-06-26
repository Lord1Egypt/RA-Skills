# Qoder 使用示例

## 1. 基础代码生成
**用户请求**: "用Python写一个快速排序算法"
**调用方式**: 
```bash
qoder generate --language python --task "快速排序算法" --output quicksort.py
```

## 2. 代码重构
**用户请求**: "重构这个JavaScript函数，让它更易读"
**调用方式**:
```bash
qoder refactor --input original.js --style readable --output refactored.js
```

## 3. SPEC驱动开发
**用户请求**: "根据这个需求文档生成API代码"
**调用方式**:
```bash
qoder spec --spec requirements.txt --framework express --output api/
```

## 4. 代码解释
**用户请求**: "解释这段Go代码的作用"
**调用方式**:
```bash
qoder explain --input complex.go --format markdown --output explanation.md
```

## 5. 测试生成
**用户请求**: "为这个Python类生成单元测试"
**调用方式**:
```bash
qoder test --input myclass.py --framework pytest --output test_myclass.py
```

## 6. 多文件项目生成
**用户请求**: "创建一个完整的React Todo应用"
**调用方式**:
```bash
qoder project --template react-todo --name todo-app --output ./todo-app
```

## 7. 代码审查
**用户请求**: "审查这段代码的安全问题"
**调用方式**:
```bash
qoder review --input suspicious_code.py --focus security --output security_report.md
```

## 8. 文档生成
**用户请求**: "为这个模块生成API文档"
**调用方式**:
```bash
qoder document --input module/ --format markdown --output docs/
```

## 参数说明

### 通用参数
- `--model`: 指定使用的模型（默认：qwen-coder-max）
- `--temperature`: 控制生成的随机性（0.0-1.0，默认：0.2）
- `--max-tokens`: 最大输出token数（默认：4096）

### 输出控制
- `--output`: 指定输出路径
- `--format`: 输出格式（code/markdown/json等）
- `--verbose`: 显示详细日志

### 高级功能
- `--context-files`: 提供上下文文件列表
- `--workspace`: 指定工作空间目录
- `--config`: 使用自定义配置文件