---
name: moji-vocab
description: Moji辞書生词本管理与每日测试技能。支持读取日语收藏夹、按时间排序（早期单词优先）、混合模式出题（释义+读音）、删除已掌握单词。
---

# Moji辞書每日词汇测试 🇯🇵

## 功能

- **📖 读取收藏夹** - 获取 Moji 辞书日语生词本
- **⏰ 时间排序** - 按添加时间排序，优先复习早期单词
- **📝 混合出题** - 随机选择「释义题」或「读音题」
- **🎯 智能选项** - 自动从收藏夹生成干扰项
- **🗑️ 批量删除** - 删除已掌握的单词

## 配置

### 获取 Token 和 Device ID

1. 打开 https://www.mojidict.com 并登录
2. 按 F12 → Application/Storage → Local Storage
3. 找到：
   - `sessionToken` (x-moji-token)
   - `deviceId` (x-moji-device-id)

### 设置环境变量

```bash
export MOJI_TOKEN="你的sessionToken"
export MOJI_DEVICE_ID="你的deviceId"
```

## 使用方法

### 1. 查看收藏夹统计
```bash
python3 scripts/moji_manager.py --action stats
```

### 2. 生成混合测试题（释义+读音）
```bash
python3 scripts/moji_quiz.py --count 5
```

### 3. 只测早期单词（2020年收藏的）
```bash
python3 scripts/moji_early_quiz.py --count 5
```

### 4. 删除指定单词
```bash
python3 scripts/moji_manager.py --action delete --word-id <objectId>
```

## 题型说明

### 释义题
> **関係 | かんけい** (N1) 的意思是？
> - A) 关系；关联，联系
> - B) 判断；占卜
> - C) 嫉妒，吃醋
> - D) 解决

### 读音题
> **判断**
> 释义: [名·サ变] 判断；占卜...
> 
> 这个汉字怎么读？
> - A) かいさい
> - B) はんだん ✅
> - C) てんけい
> - D) かくれる

## API 信息

- **Base URL**: `https://api.mojidict.com`
- **认证方式**: Header `x-moji-token`
- **排序参数**: sortType=5（从最老的开始）

## 工作流程

1. **每天早上 9:00** - 自动发送 5 道日语词汇测试（混合题型）
2. **答题** - 选择正确的释义或读音
3. **核对** - 查看得分和错题解析
4. **删除** - 告诉龙虾哪些词记住了，自动从收藏夹删除

## 依赖

```bash
pip install requests
```
