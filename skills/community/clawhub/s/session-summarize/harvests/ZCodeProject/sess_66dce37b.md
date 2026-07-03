# ZCodeProject — sess_66dce37b 归档
> 最后更新: 2026-06-24

## 压缩上下文
目标：解决 ZCode 界面只显示"思考 X秒"不显示推理内容的问题。
1. 排查发现：当前 DeepSeek 以 Anthropic 协议接入（kind: anthropic），该端不返回 thinking block，只能显示耗时数字。
2. 调研确认：DeepSeek OpenAI 协议（/v1/chat/completions）支持 reasoning_content 字段返回推理链。
3. 用户通过 UI 添加 OpenAI 协议 provider 时，因模型名大小写错误（DeepSeek-v4-flash → deepseek-v4-flash）首次连接失败，修正后成功。
4. 测试验证：9.9 vs 9.11 推理任务，推理内容正常显示，但 DeepSeek 强制英文输出，无法改为中文。
5. 当前状态：OpenAI 协议已生效，推理可见，语言为英文不可控。

## 完整文件清单
- .zcode/v2/config.json — 用户通过 UI 新增 OpenAI 协议 provider（未直接改文件）
- .agents/skills/summarize/harvests/ZCodeProject/sess_66dce37b.md — 本归档（新建）

## 完整错误列表
| 错误 | 分类 | 原文引用 |
|------|:--:|---------|
| 模型名大小写：传入 DeepSeek-v4-flash 但要求 deepseek-v4-flash | ASSU | "The supported API model names are deepseek-v4-pro or deepseek-v4-flash, but you passed DeepSeek-v4-flash" |

## 技能调用详情
- summarize ×1: 当前会话压缩归档
