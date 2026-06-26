# Contributing to Seedance Video Skill (火山方舟)

本技能说明如何通过**火山方舟（Ark）** REST API 调用豆包 Seedance 进行文生视频/图生视频。请按问题类型选择反馈位置。

## 别人在哪提 Issue？

**Issue 地址：** [https://github.com/maddy-cc/seedance-video-skill/issues](https://github.com/maddy-cc/seedance-video-skill/issues)

若发布到 ClawHub，可在 `clawhub.json` 里设置 `support_url` 为上述链接。

---

## 在哪里反馈

### 在本仓库提 Issue（适合）

- 技能文档不清楚、错误或示例无法运行
- 希望增加示例或改进流程说明
- 使用 Ark API 时与本技能描述不一致

### 联系火山引擎/豆包（适合）

- API 返回错误、计费、推理接入点配置
- 需要新的模型能力或 API 参数

## 提 Issue 前

1. 确认已设置 `ARK_API_KEY` 且接入点已开通视频生成。
2. 在终端用 curl 复现请求，便于定位是 API 还是文档问题。
3. 查阅[火山方舟视频生成 API](https://www.volcengine.com/docs/82379/1520757)确认最新参数与错误码。

## 更新参数或接口

当火山方舟新增参数或接口时：

- 在 SKILL.md 的「API 参考」和「创建任务：请求体说明」中同步更新。
- 如有常见用法，可补充对应示例。
- 保持「创建任务 → 轮询状态 → 取 video_url」的流程一致。
