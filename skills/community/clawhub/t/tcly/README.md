# 🌍 同程旅业入境游需求收集助手 (Inbound Travel Collector)

这是一个专为入境游 (Inbound Tourism) 设计的 OpenClaw 技能插件。它能通过中英文双语自然对话，收集海外客户来华旅游的需求，并自动结构化存储到飞书多维表格中，极大提高跨境旅游服务的效率。

This is an OpenClaw skill plugin designed specifically for Inbound Tourism. It collects travel requirements from international clients visiting China through bilingual (Chinese/English) natural conversation and automatically stores structured data into Feishu Bitable, significantly improving cross-border tourism service efficiency.

## ✨ 功能特点 (Features)
- 🌐 **双语智能交互 (Bilingual Interaction)**: 自动识别用户语言（中/英），并用同种语言流畅交流。
- 📝 **入境游专用字段 (Inbound Specific Fields)**: 专门收集国籍、护照、签证状态、饮食禁忌（如清真）、导游语言需求等关键信息。
- ✅ **二次确认机制 (Confirmation Workflow)**: 提交前强制总结并确认，确保跨国沟通信息无误。
- 🔗 **无缝集成 (Seamless Integration)**: 数据直达飞书多维表格，支持团队协作跟进。
- 🔒 **隐私保护 (Privacy)**: 敏感信息仅在内存中处理并加密传输至飞书，不留存本地日志。

## 🚀 安装与配置 (Installation & Configuration)

### 1. 前置准备：配置飞书多维表格 (Prerequisites: Feishu Bitable Setup)
为了支持入境游业务，请按以下步骤创建或修改您的飞书表格：

1. **新建多维表格**: 创建一个新的飞书多维表格。
2. **设置列名 (Set Columns)**:
   建议直接使用英文列名，方便国际团队查看，或者使用“英文 (中文)”格式。
   请确保包含以下列（字段类型建议）：
   - `Name` (文本) - 姓名
   - `Nationality` (文本) - 国籍
   - `Contact` (文本) - 邮箱/电话
   - `Destination` (文本) - 意向目的地
   - `Group Size` (数字) - 出行人数
   - `Departure Date` (日期) - 预计出发日期
   - `Budget` (数字) - 预算
   - `Currency` (文本) - 货币单位
   - `Preferences` (文本/多选) - 兴趣偏好
   - `Guide Language` (文本/单选) - 导游语言需求
   - `Dietary Restrictions` (文本) - 饮食禁忌
   - `Visa Assistance Needed` (单选/文本) - 是否需要签证协助

3. **获取凭证**:
   - **Base Token**: 从浏览器 URL 中 `/base/` 后获取 (以 `bascn_` 开头)。
   - **Table ID**: 从浏览器 URL 中 `table=` 后获取 (以 `tbl_` 开头)。

4. **配置飞书应用权限**:
   - 访问 [飞书开放平台](https://open.feishu.cn/)。
   - 确保应用拥有 `bitable:app` 和 `base:record:create` 权限。
   - 获取 `App ID` 和 `App Secret`。
   - **重要**: 将该应用添加为多维表格的协作者，并赋予“可编辑”权限。

### 2. 在 ClawHub 中安装 (Install in ClawHub)
1. 在 ClawHub 搜索 "Inbound Travel Collector" 或 "入境游助手" 并点击安装。
2. 在配置页面填入以下环境变量：
   - `FEISHU_APP_ID`: `cli_xxxxx`
   - `FEISHU_APP_SECRET`: `xxxxx` (⚠️ Keep this secret!)
   - `FEISHU_BASE_TOKEN`: `bascn_xxxxx`
   - `FEISHU_TABLE_ID`: `tbl_xxxxx`
3. 保存配置即可开始使用。

## 💬 使用示例 (Usage Examples)

### 场景 A: 英文用户 (English User)
> **User**: "I'm planning a trip to Xi'an with my family. We need an English guide."
> **Assistant**: "Wonderful! Xi'an is historic. To help us arrange the best service, could you please share your **nationality**? This helps with visa advice. Also, do you have any dietary restrictions (e.g., Halal, Vegetarian)?"
> ...
> **Assistant**: "Summary: Mr. Johnson (UK), 4 people, Xi'an, English guide, Halal food. Budget $1500/person. Confirm submission?"
> **User**: "Yes."
> **Assistant**: "✅ Submitted! Our specialist will email you within 24 hours."

### 场景 B: 中文用户 (Chinese User)
> **User**: "我想帮我的美国朋友咨询一下去北京的行程。"
> **Assistant**: "好的！请问您朋友的 **国籍** 是美国吗？我们需要确认最新的免签政策。另外，他们对导游语言有什么要求？需要英文导游吗？"
> ...
> **Assistant**: "帮您总结：美国籍，2人，北京，需英文导游，无饮食禁忌。确认提交吗？"
> **User**: "确认。"
> **Assistant**: "✅ 提交成功！顾问将尽快联系。"

## 📥 源码安装 (Source Installation)
如果你已安装 ClawHub CLI，可以直接运行以下命令安装此插件：

```bash
clawhub install https://github.com/lijingxu007/travel-Inbound-customizer.git