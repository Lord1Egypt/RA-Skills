---
name: meeting-minutes-assistant
description: 智能会议纪要助手 - 自动完成会议录音转写、会议纪要生成、待办事项提取的全流程处理。使用场景：(1) 处理会议录音文件（mp3/wav/m4a）需要转写为文字；(2) 从会议转写文本生成结构化会议纪要；(3) 从会议内容中提取待办事项和行动项；(4) 一站式处理会议全流程（转写→纪要→待办）。触发词：会议纪要、转写、待办提取、会议录音、meeting minutes、transcribe。
---

# 智能会议纪要助手

自动完成「会议录音转写 → 会议纪要生成 → 待办事项提取」全流程。

## 快速开始

### 完整流程（推荐）

```bash
python scripts/meeting_assistant.py full-pipeline meeting.mp3 \
  --output ./output/ \
  --title "产品周会" \
  --language zh
```

输出三个文件：
- `{name}_transcript_{timestamp}.txt` - 转写文本
- `{name}_summary_{timestamp}.md` - 会议纪要
- `{name}_todos_{timestamp}.json` - 待办事项

### 分步使用

```bash
# 仅转写
python scripts/meeting_assistant.py transcribe meeting.mp3 -o transcript.txt

# 仅生成纪要（需要先转写）
python scripts/meeting_assistant.py summarize transcript.txt -t "周会"

# 仅提取待办
python scripts/meeting_assistant.py extract-todos transcript.txt -o todos.json
```

## 环境配置

```bash
# 设置 API Key（必需）
export ASTRONCLAW_API_KEY="your_api_key"

# 可选：自定义 API 地址
export ASTRONCLAW_API_BASE="https://api.astronclaw.com"
```

## 输出格式

### 会议纪要 (Markdown)

```markdown
# 会议纪要

**会议主题**: 产品周会
**生成时间**: 2024-01-15T10:30:00

---

## 参会人员
- 张三（产品）
- 李四（开发）
- 王五（设计）

## 主要讨论
1. 新功能上线进度
2. 用户反馈处理
3. 下周计划

## 决议
- 周三前完成测试
- 周五上线 v2.1
```

### 待办事项 (JSON)

```json
{
  "todos": [
    {
      "task": "完成登录模块测试",
      "assignee": "李四",
      "deadline": "周三",
      "priority": "high",
      "context": "需要在新版本上线前完成"
    }
  ]
}
```

## 支持的音频格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| MP3 | .mp3 | 最常用 |
| WAV | .wav | 无损音质 |
| M4A | .m4a | Apple 设备常用 |
| WebM | .webm | 在线会议常用 |
| OGG | .ogg | 开源格式 |
| FLAC | .flac | 无损压缩 |

## 语言支持

```bash
# 中文（默认）
--language zh

# 英文
--language en

# 日文
--language ja

# 韩文
--language ko
```

## 工作流建议

1. **会议前**：准备录音设备，确保音质清晰
2. **会议中**：记录参会人员名单
3. **会议后**：
   ```bash
   # 一键处理
   python scripts/meeting_assistant.py full-pipeline recording.mp3 \
     --title "$(date +%Y-%m-%d) 周会"
   ```
4. **分发**：将纪要和待办发送给参会人员

## 故障排除

### 转写失败
- 检查 API Key 是否正确
- 确认音频文件大小 < 25MB
- 验证音频格式是否支持

### 纪要质量不佳
- 确保转写质量（音质清晰）
- 添加会议标题帮助模型理解上下文
- 考虑分段处理超长会议

## 参考资料

- [API 参考](references/api_reference.md) - AstronClaw API 详细文档