---
name: sanjiaozhou-random
description: 三角洲行动随机地图 + 随机装备组合生成器
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [python3]
    install:
      - kind: pip
        packages: [requests]
---
# 三角洲行动随机地图&装备生成器

## 功能介绍
本技能用于**三角洲行动**游戏中，一键随机生成：
- 随机地图
- 随机头部防具
- 随机身体护甲
- 随机主武器 + 改枪码
- 随机胸挂
- 随机背包

完全随机，适合娱乐、整活、直播互动、随机挑战使用。

## 使用方法
直接运行技能即可，无需参数：
```bash
python3 my_task.py
```
## 输出示例
🎲 随机生成结果
随机地图零号大坝
随机装备组合头：战术头盔甲：重型护甲枪: M4A1改枪码: abc123胸挂：战术胸挂背包：大容量背包

## 输出格式
```json
{"status": true, "result": "生成内容文本"}
```
## 依赖
Python 3requests 库

## 适用场景
三角洲行动娱乐对局
直播随机挑战
好友开黑趣味模式

