# WeCom 文件发送技能

> 创建时间: 2026-03-18
> 适用于: 企业微信 (WeCom)

## 技能描述

将本地文件通过企业微信发送给用户的功能封装。通过此技能，可以将本地文件（如文档、图片、视频、语音等）发送给用户。

## 触发词

- "发送文件给我"
- "传输文件"
- "发送XX文件"
- "把这个文件发给我"
- "文件发给我"

## 使用方法

### 1. 文件路径

文件存放在以下目录：
- 主工作目录: `~/.openclaw/workspace/`
- 公司业务目录: `~/.openclaw/workspace/memory/companywork/`
- 抖音内容: `~/.openclaw/workspace/memory/douyin-videos/`

### 2. 发送指令

在回复中单独一行使用 MEDIA: 指令，后面跟文件的本地路径。

格式：
```
MEDIA: /文件的绝对路径
```

示例：
```
MEDIA: ~/.openclaw/workspace/memory/companywork/会议纪要.md
MEDIA: ~/openclaw/workspace/test.pdf
```

### 3. 文件大小限制

| 类型 | 限制 |
|------|------|
| 图片 | ≤10MB |
| 视频 | ≤10MB |
| 语音 | ≤2MB (仅支持AMR格式) |
| 文件 | ≤20MB |

超过限制会被自动转为文件格式发送。

### 4. 查找文件

使用 ls 命令查找文件：
```bash
ls -la ~/.openclaw/workspace/memory/companywork/
```

## 注意事项

- MEDIA: 必须在行首，后面紧跟文件路径
- 路径中包含空格时用反引号包裹
- 每个文件单独一行 MEDIA: 指令
- 可以附带文字说明

## 示例

**用户请求**: "把XX会议纪要发给我"

**处理步骤**:
1. 查找文件: `ls ~/.openclaw/workspace/memory/companywork/ | grep 关键词`
2. 确认文件路径
3. 发送文件:
```
MEDIA: ~/.openclaw/workspace/memory/companywork/XX会议纪要.md
```

---

*此技能封装了企业微信文件发送功能，方便快速将本地文件分享给用户*
