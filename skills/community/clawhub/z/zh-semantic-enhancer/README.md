# 🀄 中文语义理解增强技能

> 专为中文语境打造的语义理解增强层，让OpenClaw真正"懂中文"

## 功能特性

- ✅ 中文分词增强 - 支持新词发现 + 专业术语识别
- ✅ 歧义消解 - 理解"意思""方便"等多义词
- ✅ 成语/俗语识别 - 理解"画蛇添足""内卷""yyds"等
- ✅ 意图理解增强 - 结构化中文语义输出
- ✅ 文化上下文 - 理解中式委婉表达
- ✅ 100次免费试用

## 快速开始

```bash
# 安装技能
npx clawhub install zh-semantic-enhancer

# 使用
python index.py --input "中文文本"
```

## 示例

```python
from index import on_user_input

result = on_user_input("他有点意思")
# 输出: {"normalized": "他很有趣", "expressions": [...], ...}
```

## 支持开发者

**EVM Address**: `0xf8ea28c182245d9f66f63749c9bbfb3cfc7d4815`

## License

MIT
