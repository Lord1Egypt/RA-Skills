# 📚 Word Memory - 单词记忆助手

## 📖 功能说明

基于艾宾浩斯记忆曲线的单词记忆工具，支持每日推送、单词测试。

## 🚀 使用方法

### 在 OpenClaw 中使用

```
开始学习
测试我
查 abandon
切换到六级
每日 30 个
学习进度
```

### Python 脚本调用

```python
from word_memory import main

# 开始学习
result = main("开始学习")
print(result)

# 单词测试
result = main("测试我")
print(result)
```

## 📁 文件结构

```
word-memory/
├── SKILL.md              # 技能描述
├── word_memory.py        # 主程序
├── progress.json         # 学习进度（自动生成）
└── stats.json            # 统计数据（自动生成）
```

## 📊 艾宾浩斯记忆曲线

自动安排 8 个复习节点：
- 5 分钟
- 30 分钟
- 12 小时
- 1 天
- 2 天
- 4 天
- 7 天
- 15 天

## 📊 示例输出

```
📚 **今日学习计划** (2026-03-16)

📖 新词 (20 个)
1. 📖 **abandon** /əˈbændən/
   📝 释义：v. 放弃，抛弃
   📖 例句：He abandoned his plan to travel.
   🌳 词根：a-(加强) + ban(禁止) → 彻底禁止 → 放弃

2. 📖 **ability** /əˈbɪləti/
   📝 释义：n. 能力，才能
   📖 例句：She has the ability to pass the exam.
   🌳 词根：abil(能) + -ity(名词后缀)

📝 复习 (15 个)
1. previous - 掌握度 85%
2. absolute - 掌握度 92%
```

## 🛠️ 开发计划

- [x] 艾宾浩斯算法
- [x] 单词测试
- [x] 进度统计
- [ ] 定时推送
- [ ] 完整词库导入
- [ ] 听力测试

## 📝 更新日志

### v1.0.0 (2026-03-16)
- 🎉 初始版本

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License
