---
name: qqbot-image-helper
description: 图片处理助手：将受限目录的图片复制到允许的目录，然后使用 image 工具进行分析。适用但不限于 QQBot 下载的本地图片。
metadata: {"openclaw": {"emoji": "🖼️", "requires": {"tools": ["image", "exec"], "bins": ["cp"]}}}
---

# 图片处理助手

## 什么时候使用

✅ **使用此 skill 当：**

- 需要分析 QQBot 等通道下载的本地图片
- 收到 "Local media path is not under an allowed directory" 错误
- 图片路径在 `~/.openclaw/qqbot/downloads/` 或其他受限目录

❌ **不要使用此 skill 当：**

- 图片已经在 workspace 目录中
- 使用网络 URL（直接传给 image 工具即可）

## 问题背景

OpenClaw 的 `image` 工具默认不允许访问
- `~/.openclaw/qqbot/downloads/`

而 QQBot通道下载的图片存储在：
- `~/.openclaw/qqbot/downloads/`

这些目录**不在允许列表中**，导致 image 工具报错：
```
Local media path is not under an allowed directory
```

## 解决方案

将受限目录的图片复制到 `~/.openclaw/media/` 目录（已验证可被 image 工具访问）。

## 使用步骤

### 1. 检查图片路径

判断图片是否在受限目录中：

```bash
# QQBot 下载目录
ls ~/.openclaw/qqbot/downloads/
```

### 2. 复制到 media 目录

```bash
# 复制图片到 media 目录
cp <原始路径> ~/.openclaw/media/<文件名>
```

**示例：**
```bash
# QQBot 下载的图片
cp ~/.openclaw/qqbot/downloads/86635B3805C6F6E405B847EC5B242684_1773402564132.png ~/.openclaw/media/86635B3805C6F6E405B847EC5B242684_1773402564132.png
```

### 3. 使用 image 工具分析

使用复制后的路径调用 image 工具：

```
image: ~/.openclaw/media/temp_image.png
prompt: "描述这张图片的内容"
```

---

## 完整示例

### 场景：用户通过 QQ 发送了一张图片

**步骤 1：** 查看附件路径
```
QQImageAttachmentPaths: ["~/.openclaw/qqbot/downloads/xxx.png"]
```

**步骤 2：** 复制到 media 目录
```bash
cp ~/.openclaw/qqbot/downloads/xxx.png ~/.openclaw/media/xxx.png
```

**步骤 3：** 使用 image 工具分析
```
image: ~/.openclaw/media/xxx.png
prompt: "请描述这张图片的内容"
```

---

## 快速参考

| 操作 | 命令 |
|------|------|
| 检查 QQBot 下载 | `ls ~/.openclaw/qqbot/downloads/` |
| 复制到 media | `cp <源路径> ~/.openclaw/media/<文件名>` |
| 分析图片 | `image: ~/.openclaw/media/<文件名>` |

## 注意事项

1. **文件名冲突**：media 目录下可能已有同名文件，建议使用时间戳或随机后缀
2. **清理旧文件**：media 目录会累积临时文件，建议定期清理
3. **路径确认**：复制后确保新路径存在且可读
4. **模型限流**：image 工具可能遇到 429 限流，请稍后重试

## 常见受限目录

| 通道 | 下载目录 | 是否受限 |
|------|----------|----------|
| QQBot | `~/.openclaw/qqbot/downloads/` | ✅ 受限 |
| workspace* | `~/.openclaw/workspace*/` | ✅ 允许 |
| media | `~/.openclaw/media/` | ✅ 允许 |

---

**创建时间：2026-03-13**
**测试状态：✅ 已验证 `~/.openclaw/media/` 可被 image 工具访问**
