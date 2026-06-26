---
name: subtitle-refiner
description: 优化 SRT 字幕文件。去除填充词（嗯、啊等），修正 ASR 识别错误（如 XGBT→ChatGPT、RG→RAG），保持时间戳完全不变，通过 Feishu 发送优化结果和 token 消耗报告。
user-invocable: true
metadata:
{
  "openclaw": {
    "emoji": "📝",
    "requires": {
      "bins": ["python3"],
      "env": ["SILICONFLOW_API_KEY"]
    },
    "primaryEnv": "SILICONFLOW_API_KEY"
  }
}
---

# Subtitle Refiner

AI 驱动的字幕优化工具，使用 SiliconFlow GLM-4.7 模型智能优化 SRT 字幕文件。

## 核心功能

- **自动去除语气词**：删除 "嗯"、"啊"、"那个"、"就是"、"然后"、"呃" 等口语填充词
- **智能修正 ASR 错误**：根据视频主题修正语音识别错误
  - XGBT → ChatGPT
  - RG → RAG
  - 菜GPT → ChatGPT
  - CHATPT → ChatGPT
  - 等等...
- **保持时间戳**：所有时间轴信息完全不变
- **主题感知**：分析视频主题，进行上下文相关的校对
- **Token 追踪**：详细记录每次优化的 token 消耗

---

## 触发条件

当以下情况时自动触发此技能：

1. **用户发送 .srt 文件**
2. **用户使用关键词**：
   - "优化字幕"
   - "校对字幕"
   - "去掉字幕里的口语词"
   - "fix subtitle"
   - "refine subtitle"
   - "clean subtitle"

---

## 工作流程

当技能被触发时：

### 步骤 1：获取文件路径

从用户消息中获取 SRT 文件路径。

### 步骤 2：调用优化模块

直接执行优化脚本，该脚本会将优化好的文件发送至飞书：

```bash
python3 {baseDir}/scripts/refine.py <srt_file> <chat_id> <workspace>
```

**参数说明**：
- `<srt_file>`: SRT 文件的完整路径
- `<chat_id>`: Feishu 聊天 ID（从上下文获取）
- `<workspace>`: OpenClaw workspace 目录（用于存储输出文件）

**示例**：
```bash
python3 /path/to/skill/scripts/refine.py \
    /workspace/subtitle/demo.srt \
    "oc_xxxxxxxxx" \
    /workspace
```


## 重要规则

Agent **必须**遵守以下规则：

1. ✅ **保持时间戳**：永远不修改时间轴信息
2. ✅ **保持顺序**：永远不改变字幕顺序
3. ✅ **保持索引**：永远不修改字幕序号
4. ✅ **只修改文本**：只修改字幕的文本内容
5. ✅ **调用 Python 模块**：使用上述代码导入并调用 `refine_and_send()`
6. ✅ **传递正确参数**：确保传递文件路径、chat_id 和 workspace_dir

---

## 输出格式

### 优化后的文件

- **命名格式**：`{原文件名}_优化{时间戳}.srt`
- **存储位置**：`{workspace}/subtitle_refine/`

---
## 汇总格式参考
```bash
✅ 字幕优化完成！
优化结果：
📝 处理字幕：x 条
✏️ 修正内容：x 处
🎯 主要修正：
去除口语填充词（嗯、啊、然后、那个等）
修正 ASR 识别错误（XGBT → ChatGPT、xx → xx 等）
Token 消耗：
输入：xx tokens
输出：xx tokens
总计：xx tokens
输出文件：
已自动发送到飞书，文件名：chatgpt订阅会员教程---1d420eb9-64ae-4381-ab81-5e489432d825_优化_20260308_0942.srt
请查收飞书消息中的优化后字幕文件！📤
```
## 配置

### API 配置

- **Endpoint**: `https://api.siliconflow.cn/v1/chat/completions`
- **主模型**: `Pro/zai-org/GLM-4.7`
- **API Key**: 从环境变量 `SILICONFLOW_API_KEY` 读取
- **如果用户没有填写API Key，提示**：

  注册领取API 16元代金券 https://cloud.siliconflow.cn/i/AEg95IPc
  
  获取SILICONFLOW_API_KEY：https://cloud.siliconflow.cn/me/account/ak
### 文件存储

- **原始文件**: `{workspace}/subtitle/`（由 OpenClaw 管理）
- **优化文件**: `{workspace}/subtitle_refine/`（输出目录）

---

## 错误处理

Skill 具有完善的错误检测和处理机制，会在处理前自动检查环境：

### 预检查功能

1. **🔌 网络连接检测**：自动检测是否能连接到 SiliconFlow API
2. **🔑 API Key 验证**：验证 API Key 是否有效
3. **⚠️ 早期失败**：在开始处理前发现问题，避免浪费 token

### 错误提示

| 错误类型 | 提示 | 解决方案 |
|---------|------|----------|
| 🔑 API Key 错误 (401) | API Key 未设置或无效 | 检查环境变量 `SILICONFLOW_API_KEY` |
| 💰 余额不足 (402) | API 余额不足 | [充值](https://cloud.siliconflow.cn/me/account/ak) |
| 🚫 权限不足 (403) | API 权限问题 | 检查账户状态和 API 权限 |
| ⏳ 请求频繁 (429) | 请求过于频繁 | 稍后重试 |
| ⏱️ 请求超时 | API 请求超时 | 检查网络连接或稍后重试 |
| 🔌 网络失败 | 无法连接到 API | 检查网络设置和代理配置 |

### 自动重试

- **超时重试**：支持连接超时（10秒）和读取超时（60秒）分离
- **优雅降级**：逐行优化失败时保留原文继续处理


---

## 技术细节

### 提示词策略

1. **主题分析**：分析前 20 条字幕，提取视频主题
2. **逐行优化**：基于主题和规则，逐行校对每条字幕
3. **规则约束**：6 条明确规则，确保不过度修改

### Token 追踪

- 每次API调用都记录输入和输出 token
- 汇总所有调用的总消耗
- 在总结中清晰展示

### 优化质量

- Temperature: 0.2（确保稳定性）
- 仅修正明确的问题，不润色
- 保持原句意思和语气
