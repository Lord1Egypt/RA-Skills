---
name: smart-voice-reply
description: "用于语音回复和回复语音音色配置。Invoke when: (1) 用户需要进行语音回复 (2) 用户要求配置或创建新的音色 (3) 用户询问音色相关功能。"
metadata:
  {
    "openclaw":
      { "requires": { "env": ["DASHSCOPE_API_KEY"] }, "primaryEnv": "DASHSCOPE_API_KEY" },
  }
---

# Smart Voice Reply
## 语音回复
这个技能用于需要不同音色的语音对话 每次执行时：
1. **确定使用场景**：办公场景 / 个人场景 / 自定义场景
2. **匹配音色**：根据场景和情绪选择合适音色
3. **调用 cli.js 合成语音**：将文字转换为语音
4. **调用 openclaw message send 发送语音**：将语音发送给用户

### cli调用

```bash
scripts/tts_cli.js --text "<reply_text>" --voice <voice> --instructions "<instructions>" --output-dir <output_dir> [--optimize-instructions]
```

参数介绍：
- `--text`           必填，待合成文本
- `--voice`          必填，音色名称（见 `docs/音色指令创建指导.md` 中的可用音色ID表）
- `--instructions`   必填，音色调整指令内容
- `--output-dir`      必填，输出目录路径(建议存在 workspace/media/voice-tmp目录下)
- `--optimize-instructions`  可选，是否优化指令（默认 true）

返回生成好的语音文件的路径

### openclaw message send使用
**注意** 使用openclaw message 发送成功消息后，不要对用户返回语音已发送成功的消息

```bash
openclaw message send --target <user_id> --media <voice_file_path>
```

## 音色配置
用于根据用户需求配置不同的回复语音音色
**音色配置所需的完整内容（包括可用音色ID列表、音色指令编写维度、预设场景示例、用户自定义音色格式）请参考**: docs/音色指令创建指导.md
该文档包含：
- 如何编写高质量的声音描述（核心原则、描述维度参考）
- 可用的音色ID列表（25种音色）
- 音色指令示例（声学属性控制、年龄控制、渐变控制、拟人感）
- 预设场景示例
- 用户自定义音色添加方式

## setup
读取 docs/技能安装配置指导.md 