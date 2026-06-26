---
name: qoder
description: 阿里云Qoder编程工具集成 - 提供AI代码生成、重构、SPEC驱动开发等功能。使用百炼模型的coding plan套餐进行代码相关任务。适用于代码生成、代码重构、反向生成文档、SPEC驱动开发等场景。
---

# Qoder 编程工具 Skill

## 概述

Qoder 是阿里云提供的AI编程工具，基于百炼模型的coding plan套餐，支持多种编程模式和开发场景。

## 使用场景

- 代码生成和补全
- 代码重构和优化  
- 反向生成技术文档
- SPEC驱动开发（Omni SPEC模式）
- Super Power模式开发
- 舆情分析和自动化报表

## 环境配置

### 模型选择
推荐使用 **百炼模型订阅制 coding plan** 套餐，成本可控（约200多元/月）

### 系统要求
- **推荐系统**: Mac或Linux（Windows对Qoder效率有影响）
- **大文件处理**: 文件超过4000行时建议拆分，避免上下文割裂

## 调用方式

### 1. 基础代码生成
```bash
# 生成新代码文件
qoder generate --language python --task "创建一个REST API服务"
```

### 2. 代码重构
```bash
# 重构现有代码
qoder refactor --file ./src/main.py --improvements "优化性能，添加类型注解"
```

### 3. SPEC驱动开发
```bash
# 使用Omni SPEC模式
qoder spec --mode omni --spec-file ./specs/api-spec.yaml
```

### 4. 反向生成文档
```bash
# 从代码生成文档
qoder document --source ./src/ --output ./docs/
```

### 5. Super Power模式
```bash
# 启用Super Power模式进行复杂任务
qoder super --task "实现完整的用户认证系统" --context ./existing-code/
```

## 安全注意事项

1. **权限控制**: Qoder具有文件读写权限，使用前确保工作目录安全
2. **成本控制**: 监控API调用次数，避免超出订阅套餐限制
3. **代码审查**: AI生成的代码需要人工审查后再合并到主分支

## 最佳实践

### 工作流设计
- **渐进式应用**: 从单一可自动化环节开始，不要追求全面自动化
- **先跑通再扩展**: 先验证一个点的有效性，再逐步扩散到其他场景

### 上下文管理
- **拆分大文件**: 避免单个文件过大导致上下文限制
- **明确任务边界**: 每次调用专注于单一任务

### 常见应用场景示例

#### 1. 生成周报模板
```bash
qoder generate --task "生成本周技术周报模板，包含项目进展、问题解决、下周计划" --format markdown
```

#### 2. 邮件摘要分析
```bash
qoder analyze --input ./emails/ --task "提取关键信息并生成摘要" --output summary.txt
```

#### 3. 自动化测试生成
```bash
qoder test --source ./src/module.py --coverage 90 --framework pytest
```

## 故障排除

### 常见问题
1. **上下文超限**: 拆分大文件或减少输入内容
2. **API调用失败**: 检查网络连接和API密钥配置
3. **生成质量不佳**: 提供更详细的prompt或使用Super Power模式

### 调试命令
```bash
# 查看Qoder版本和配置
qoder --version
qoder config --list

# 测试API连接
qoder health-check
```

## 参考资源

- [Qoder官方文档](https://help.aliyun.com/product/qoder)
- [百炼模型coding plan套餐详情](https)
- [OpenClaw与Qoder集成指南](https)