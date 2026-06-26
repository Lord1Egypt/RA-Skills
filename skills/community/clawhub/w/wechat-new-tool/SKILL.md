# 微信助手智能网关 (v2.0)

## 核心工具: 智能分发 (smartDispatch)
- **路径**: `POST /wechat/dispatch`
- **说明**: 统一处理发送请求。AI 提取“目标名称”和“内容”，逻辑由后端闭环。
- **参数**:
    - `query`: 用户提到的目标（姓名或群名）
    - `type`: 消息类型 ("text", "image", "file")
    - `content`: 文本内容或媒体 URL
    - `fileName`: 文件名（仅 type 为 file 时）

## 交互规范
1. **单结果**: 若后端返回 `status: "confirm"`，AI 询问“确认发送给 [名称] 吗？”
2. **多结果**: 若返回 `status: "need_choice"`，AI 展示列表让用户点选。
3. **已确认**: 用户确认后，AI 调用 `/wechat/confirm_send` 完成最终推送。