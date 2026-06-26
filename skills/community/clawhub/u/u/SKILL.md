---
name: "u"
version: "1.0.0"
description: "Universal Utility Toolkit - 全能实用工具包，包含单位转换、UUID生成、URL处理、Unicode探索、JSON/YAML格式化、哈希计算、密码生成、颜色选择等开发必备工具。Invoke when user needs utility tools, converters, generators, formatters, or any common development utilities."
---

# u - Universal Utility Toolkit

## 概述

**u** 是一个全能实用工具包（Universal Utility Toolkit），提供开发者日常工作中最常用的各种小工具。所有功能都围绕 "U" 主题设计，简洁易用，提高开发效率。

## 功能模块

### 1. Unit Converter - 单位转换器
- **长度转换**：米、厘米、英寸、英尺、码等
- **重量转换**：千克、克、磅、盎司等
- **温度转换**：摄氏度、华氏度、开尔文
- **货币转换**：支持主要货币汇率（包含USDT）
- **数据大小**：字节、KB、MB、GB、TB等
- **时间转换**：秒、分钟、小时、天等

### 2. UUID Generator - UUID生成器
- 生成 UUID v1, v4, v5
- 批量生成 UUID
- 复制到剪贴板

### 3. URL Toolkit - URL工具集
- URL 编码/解码
- URL 缩短/展开
- URL 参数解析与提取
- URL 验证
- 生成 QR 码

### 4. Unicode Explorer - Unicode字符探索
- 搜索特殊字符、表情符号、数学符号
- 字符编码转换（UTF-8, UTF-16, HTML实体）
- 表情符号生成器
- 字符详情查看

### 5. Data Formatter - 数据格式化
- JSON 格式化/压缩/验证
- YAML 格式化/转换
- XML 格式化
- Base64 编码/解码

### 6. Hash Calculator - 哈希计算器
- MD5, SHA-1, SHA-256, SHA-512
- 字符串哈希
- 文件哈希计算

### 7. Password Generator - 安全密码生成器
- 自定义密码长度
- 包含大小写、数字、特殊字符
- 密码强度评估
- 批量生成

### 8. Color Picker - 颜色选择器
- RGB, HEX, HSL 转换
- 颜色渐变生成
- 调色板推荐
- 颜色对比度检查

## 使用场景

- 日常开发需要快速转换单位
- 生成测试用的 UUID
- 处理 URL 编码/解码
- 探索特殊 Unicode 字符
- 格式化 JSON/YAML 数据
- 计算哈希值
- 生成安全密码
- 颜色方案设计

## 使用示例

### 单位转换
```
用户：帮我把 100 美元转换成 USDT
u: 根据当前汇率，100 USD ≈ 100 USDT
```

### UUID 生成
```
用户：生成 5 个 UUID
u: 
1. 550e8400-e29b-41d4-a716-446655440000
2. 6ba7b810-9dad-11d1-80b4-00c04fd430c8
3. ...
```

### URL 编码
```
用户：编码这个 URL: https://example.com/测试
u: https%3A%2F%2Fexample.com%2F%E6%B5%8B%E8%AF%95
```

## 关键词

utility, toolkit, converter, generator, formatter, uuid, url, unicode, json, yaml, hash, password, color, unit conversion, 单位转换, 工具包, 实用工具, USDT, 加密货币

## 注意事项

- 货币汇率为实时数据，可能有延迟
- 密码生成器仅供参考，请根据安全需求调整
- Unicode 字符支持取决于系统字体
