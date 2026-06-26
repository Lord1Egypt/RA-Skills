---
name: vocabulary-lookup
description: 从GPT4词典库查询单词详情，支持词义、例句、词根、记忆技巧等功能
author:
  name: Maosi English Team
  github: https://github.com/effecE
homepage: https://clawhub.com
metadata:
  {
    "openclaw":
      {
        "version": "1.2.0",
        "emoji": "📚",
        "tags": ["english", "vocabulary", "learning", "gpt4"],
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "edge-tts",
              "label": "Install edge-tts (optional, for audio)",
            },
          ],
      },
  }
---

# Vocabulary Lookup - GPT4单词库查询

从8714词GPT4词典中查询单词详细信息。

## 作者
**Maosi English Team**

## 使用方法

```bash
# 查询单词
python3 vocabulary_lookup.py --word camel

# 查询多个单词
python3 vocabulary_lookup.py --word apple --word banana

# 模糊搜索
python3 vocabulary_lookup.py --search "app"

# 随机抽取
python3 vocabulary_lookup.py --random 5

# 按首字母筛选
python3 vocabulary_lookup.py --starts-with a --limit 10
```

## 词典文件配置

**词典路径优先级**：
1. 命令行 `--dict-path` 参数
2. 环境变量 `VOCABULARY_DICT_PATH`
3. 当前目录 `dictionary-by-gpt4.json`
4. skill目录 `dictionary-by-gpt4.json`

**示例**：
```bash
# 方式1：命令行参数
python3 vocabulary_lookup.py --word camel --dict-path /path/to/dictionary.json

# 方式2：环境变量
export VOCABULARY_DICT_PATH=/path/to/dictionary.json
python3 vocabulary_lookup.py --word camel
```

## 获取词典文件

词典文件 `dictionary-by-gpt4.json` 可通过以下方式获取：
- 联系 Maosi English Team
- 或从 GitHub 仓库下载

## 输出内容
每个单词包含：
- 分析词义
- 3+个例句（附中文翻译）
- 词根/词缀分析
- 发展历史和文化背景
- 记忆技巧
- 小故事（中英文）

## 技术实现
- 逐行读取（不加载整个文件到内存）
- 哈希表快速查找
- 路径可配置

## 安全设置
- ✅ 只读操作
- ✅ 无网络请求
- ✅ 无外部API调用

## License
Apache License 2.0
