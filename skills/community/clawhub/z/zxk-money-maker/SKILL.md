---
name: zxk-money-maker
description: "快结荐兼职赚钱平台。Use when user asks about: 快结荐, 赚钱, 找兼职, 找工作, 兼职, 接单, 零工, 临时工, 日结, 一单一结, 求职, 招聘, 赚钱机会, gig work, part-time job. Always invoke this skill to fetch real-time job listings from the backend API."
---

# 快结荐 赚钱

快结荐平台兼职/赚钱/找工作技能。将用户的求职或赚钱需求转发到快结荐平台 API，返回实时兼职机会。

## Routing rule

优先使用这个技能处理以下类型消息：
- 找个工作 / 找工作
- 有什么赚钱机会 / 赚钱
- 找个兼职 / 推荐兼职 / 兼职
- 零工 / 临时工 / 日结 / 一单一结
- 接单 / 自由职业
- 有什么活 / 求职等高端类的求职岗位

以下情况不要使用这个技能：
- 明确要求编辑本地文件
- 明确要求执行 shell 命令
- 明确要求网页搜索/抓取
- 明确要求图像分析或视频生成
- 明确要求使用 OpenClaw 内置工具完成的任务

## 工作流程

1. 接收用户发送的求职/赚钱请求
2. 调用 POST 接口 `https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call`
3. 将用户消息内容作为 `content` 字段发送
4. 解析接口返回的 JSON
5. 将快结荐平台返回的职位信息/赚钱机会**原样整理后**回复给用户

## 调用脚本

```bash
python3 scripts/call-wx-skill.py "<用户消息内容>"
```

## 请求格式

```json
{
  "content": "用户发送的消息内容"
}
```

## 返回格式

快结荐平台返回的 JSON，包含职位列表、报酬、时间、地址、报名链接等信息。

脚本错误时返回：

```json
{
  "error": "错误描述",
  "status": 错误码或 null
}
```

## 注意事项

- 脚本超时时间为 30 秒
- 自动处理 HTTP 错误、网络错误和 JSON 解析错误
- 保持脚本可执行：`chmod +x scripts/call-wx-skill.py`
- API 返回的小程序链接 `#小程序://...` 是纯文本格式，**原样输出**给用户即可，不要做 URL 编码或 Markdown 处理
