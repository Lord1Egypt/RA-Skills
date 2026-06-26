---
name: eudic-vocab
description: 欧路词典生词本管理与每日测试技能。支持自动从欧路词典收藏夹出题、管理单词、删除已掌握词汇。适合每日背单词使用。
---

# 欧路词典每日词汇测试 📚

## 功能

- **每日自动出题** - 从欧路词典生词本随机抽取单词生成测试
- **智能选项生成** - 自动创建干扰项，只显示释义不暴露答案
- **答题核对** - 自动批改并解析错题
- **单词管理** - 支持删除已掌握的单词

## 配置

### 1. 获取欧路词典 API Token
1. 访问 https://my.eudic.net/OpenAPI/Authorization
2. 登录后复制 Token（格式：`NIS xxxxx`）
3. 将 Token 保存到环境变量或配置文件

### 2. 设置每日测试（Cron）
```bash
# 每天早上 9:00 自动发送5道题
0 9 * * * cd /path/to/eudic-vocab && python3 scripts/daily_quiz.py --token <YOUR_TOKEN> --count 5
```

## 使用方法

### 手动生成测试题
```bash
python3 scripts/quiz_generator.py --token <TOKEN> --count 5
```

### 删除已掌握的单词
```bash
python3 scripts/vocab_manager.py --token <TOKEN> --action delete --word-id <ID>
```

### 查看所有单词
```bash
python3 scripts/vocab_manager.py --token <TOKEN> --action list
```

## 工作流程

1. **早上 9:00** - 自动收到 5 道词汇测试题
2. **答题** - 回复 A/B/C/D
3. **核对** - 查看得分和错题解析
4. **删除** - 告诉龙虾哪些词记住了，自动从生词本删除

## API 信息

- **Base URL**: `https://api.frdic.com/api/open/v1`
- **认证**: `Authorization: NIS <token>`
- **限制**: 每次最多获取 233 个单词（API 限制）

## 依赖

```bash
pip install requests
```
