---
name: sendfiles-to-feishu
description: 发送任意本地文件到飞书，自动处理大文件。视频/音频按 20MB 分段（不重新编码），其他文件压缩为 ZIP。支持大文件自动处理。
metadata:
  {
    "openclaw":
      {
        "emoji": "📤",
        "requires": { "env": ["FEISHU_APP_ID", "FEISHU_APP_SECRET"], "bins": ["ffmpeg", "ffprobe"] },
        "install":
          [
            {
              "id": "env",
              "kind": "env",
              "vars": [
                { "name": "FEISHU_APP_ID", "label": "Feishu App ID" },
                { "name": "FEISHU_APP_SECRET", "label": "Feishu App Secret", "sensitive": true }
              ]
            }
          ],
      },
  }
---

# Feishu Send File Skill

发送任意本地文件到飞书，自动处理大文件和特殊格式。

## 功能

- 自动检测文件类型（视频、音频、其他）
- 视频/音频：保持原质量，按 20MB 分段
- 其他文件：压缩为 ZIP，如仍超限则分段 ZIP
- 支持任意文件类型

## 用法

```bash
/sendfiles-to-feishu <文件路径> <接收者ID> [ID类型]
```

参数：
- `文件路径`：本地文件（绝对或相对路径）
- `接收者ID`：open_id (ou_xxx) 或 union_id (on_xxx)
- `ID类型`：可选，`open_id` 或 `union_id`（默认自动识别）

示例：
```
/sendfiles-to-feishu "C:\data\report.pdf" "ou_05eb1e0dcc31159ab77432d1d9adf7a3"
/sendfiles-to-feishu "video.mp4" "on_0144493a63e92550a0602e2b632ff597" "union_id"
```

## 处理逻辑

| 文件类型 | 处理方式 |
|----------|----------|
| 视频（含音频流） | 按时间切分，每段 < 20MB，不重新编码 |
| 视频（无音频） | 先合并音频（如有分离的音频文件），再切分 |
| 纯音频 | 按时间切分 |
| 其他（文档、图片、压缩包等） | 压缩为 ZIP，如仍 > 20MB 则分段 ZIP |

## 权限要求

飞书应用需：
- `im:message.p2p_msg` 或 `im:message.group_msg`
- `drive:file:upload`
- 机器人能力已开启

## 配置

### 方式一：.env 文件（推荐）

在技能目录下创建 `.env` 文件：

```env
# 飞书应用配置
FEISHU_APP_ID=your_app_id_here
FEISHU_APP_SECRET=your_app_secret_here
```

可复制 `.env.example` 为 `.env` 并填入实际值。

### 方式二：环境变量

设置系统环境变量：
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`

### 优先级

系统环境变量 > `.env` 文件

## 环境检测

脚本启动时自动检测依赖：

| 类型 | 依赖 | 处理方式 |
|------|------|----------|
| Python | requests | 自动安装 |
| 系统 | ffmpeg, ffprobe | 提示安装方法 |

## 依赖

- Python 3.8+
- requests
- ffmpeg

## 注意事项

- 视频分割使用 `ffmpeg -c copy`，无画质损失
- 音频视频分离检测可能不准确，如果遇到问题请手动合并
- ZIP 分割是将同一文件重复打包，接收后需解压并合并（但通常单文件压缩后不会超限）
- 发送前确保与接收者已有会话（在飞书中互发过消息）

## 故障排除

- 发送失败：检查权限和 token
- 文件过大：自动分段，如果某段仍超限（罕见），手动调整 `MAX_FILE_SIZE_MB` 常量
- 音视频分离未合并：确保同目录下有匹配的音频/视频文件（同名）