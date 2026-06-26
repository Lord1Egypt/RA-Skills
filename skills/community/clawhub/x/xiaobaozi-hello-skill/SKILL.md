---
name: hello-world-skill
description: 小包子第一个技能 - Hello World示例
metadata:
  {
    "openclaw": { "emoji": "🚀" },
    "author": "小包子",
    "version": "1.0.0"
  }
---

# Hello World 技能

小包子第一个技能，用于测试技能发布流程。

## 功能
- 返回Hello World消息
- 支持自定义名称
- 支持多种语言

## 使用方法
```bash
hello-world
# 输出: Hello, World!

hello-world --name "老板"
# 输出: Hello, 老板!

hello-world --lang zh
# 输出: 你好，世界！
```

## 参数
- `--name` 自定义名称
- `--lang` 语言选择 (en/zh/es/fr)

## 代码实现
```javascript
function helloWorld(name = "World", lang = "en") {
  const messages = {
    en: `Hello, ${name}!`,
    zh: `你好，${name}！`,
    es: `¡Hola, ${name}!`,
    fr: `Bonjour, ${name}!`
  };
  return messages[lang] || messages.en;
}
```

## 发布信息
- 作者：小包子
- 创建时间：2026-04-05
- 版本：1.0.0
- 许可证：MIT