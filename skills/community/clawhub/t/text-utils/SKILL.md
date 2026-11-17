---
name: text-utils
description: "文本处理小工具：字数/汉字/单词统计、大小写转换、反转、去重、行数统计、去空格。纯本地运行，无网络依赖。"
homepage: ""
metadata:
  {
    "openclaw":
      {
        "emoji": "📝",
        "install":
          [
            {
              "id": "python3",
              "kind": "apt",
              "formula": "python3",
              "bins": ["python3"],
              "label": "Install python3",
            },
          ],
      },
  }
---

# text-utils.sh 文本处理工具

纯本地的文本小工具，**零网络依赖**，快速处理常见文本任务。

## 用法

```bash
text-utils.sh count "你好 world 123"    # 字数/字符/汉字/单词/行数统计
text-utils.sh upper "hello"             # 转大写
text-utils.sh lower "HELLO"             # 转小写
text-utils.sh reverse "abc"             # 反转文本
text-utils.sh unique a b b c c          # 去重
text-utils.sh lines < file.txt          # 统计行数
text-utils.sh trim "  hi  "             # 去首尾空格
text-utils.sh --help                    # 帮助
```

## 特点

- 📊 `count` 支持中英文混合统计（字符数、汉字数、单词数）
- 🔒 完全本地运行，文本不离开设备
- ⚡ 即时响应，无 API 延迟

## 适用场景

- 写作时检查字数
- 批量处理文本格式
- 数据去重
