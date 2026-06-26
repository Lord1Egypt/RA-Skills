# u - Universal Utility Toolkit

全能实用工具包，提供开发者日常工作中最常用的8大功能模块。

## 功能模块

1. **Unit Converter** - 单位转换器（长度、重量、温度、货币、数据大小、时间）
2. **UUID Generator** - UUID生成器（v1, v4, v5，支持批量）
3. **URL Toolkit** - URL工具集（编码/解码、参数解析、验证）
4. **Unicode Explorer** - Unicode字符探索（特殊字符、表情符号、编码转换）
5. **Data Formatter** - 数据格式化（JSON、YAML、Base64）
6. **Hash Calculator** - 哈希计算器（MD5, SHA-1, SHA-256, SHA-512）
7. **Password Generator** - 安全密码生成器
8. **Color Picker** - 颜色选择器（RGB/HEX/HSL转换）

## 安装

```bash
npm install u-utility-toolkit
```

## 使用示例

```javascript
import { unitConverter, uuidGenerator, hashCalculator } from 'u-utility-toolkit';

// 单位转换
console.log(unitConverter.convert(100, 'cm', 'inch'));

// 生成UUID
console.log(uuidGenerator.v4());

// 计算哈希
console.log(hashCalculator.sha256('hello'));
```

## 许可证

MIT
