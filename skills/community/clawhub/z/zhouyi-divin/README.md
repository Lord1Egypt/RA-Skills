# 🔮 周易占卜 - ZhouYi Divination

> 基于《周易》的完整占卜系统，支持铜钱起卦 + 八字排盘 + 综合解读

## ✨ 特色功能

- 🎲 **铜钱法起卦** - 传统三枚铜钱摇卦
- 📜 **八字排盘** - 四柱干支自动计算
- ⚖️ **五行分析** - 日主强弱、用神推断
- 🌟 **大运推演** - 十年大运推算
- 💡 **综合解读** - 八字 + 卦象智能结合

## 🚀 快速使用

### 纯起卦
```bash
python scripts/divine.py --question "问题"
```

### 八字 + 起卦
```bash
python scripts/divine.py ^
  --question "问题" ^
  --birth-year 1990 --birth-month 5 --birth-day 15 --birth-hour 14
```

### 交互模式
```bash
python scripts/divine.py
```

## 📁 目录结构

```
zhouyi-divination/
├── SKILL.md          # 技能文档
├── README.md         # 本文件
└── scripts/
    ├── divine.py     # 主程序（起卦 + 解读）
    └── bazi.py       # 八字排盘模块
```

## ⚠️ 免责声明

本工具仅供学习和娱乐，不构成任何决策建议。人生大事请结合自身实际情况理性判断～

---

*Made with 💕 by 小艺*