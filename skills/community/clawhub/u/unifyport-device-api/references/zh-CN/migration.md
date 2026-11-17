# 迁移到 1.1.0

[English](../en/migration.md) | [简体中文](migration.md)

状态：未发布。发布后从 ClawHub 安装 @unifyport/unifyport-device-api 的精确 1.1.0 版本，核对 owner、版本和文件。整体替换旧 Skill 目录，避免遗留 skill-card.md 等旧文件。API key 不写入文件，docs-only 不需要凭据。要求 Node.js >=20。

## 既有集成

既有 action ID、API origin、确认 domain/schema、五分钟 TTL 和 opt-in 分类保持稳定。升级或改变输入后重新预览，未知结果的写操作不自动重试。导入成功或 authorized 不等于 running；删除返回 202 不等于完成。ID 和时间字符串不转换为数字或 Date。消息别名不继承其他别名字段。update-account.provider_account_ref 的公开语义待澄清，继续不可用。

## 新增字段

- import-auth-session：whatsapp-protocol 只能放在 body 的专用嵌套对象中，不能放入 provider_data。必填非空字符串为 phone、static_pub_key、static_pri_key、identity_pub_key、identity_pri_key。保留格式化 phone，归一化由服务端完成。platform 为 int32，device 为 uint32，use_xxkem_handshake 为 boolean；仅允许文档列出的可选字段。省略已废弃且上游忽略的 hash；authhexdata 保留为废弃别名，优先使用 auth_hex_data。禁止传 edge_routing。服务器覆盖可使用公网 host 或 host:port；私网/本机被拒绝，不保证 DNS 可达性。完整输入走 --input-stdin，再用 credential opt-in 和精确 HMAC 确认；session 和协议密钥不能进入聊天、argv 或日志。runner 不提供明文凭据输出通道。旧 X session_url、pin、proxy_config 继续支持。
- list-conversations：query.label_id 是原样保留的渠道字符串，不能转成数字或 trim；WhatsApp 省略它时仅返回特别关注会话，不代表全部会话。cursor 保持原样，不自动翻页。
- mark-conversation-read：WhatsApp 消息已读必须同时提供非空 up_to_message_id 与 up_to_message_sender_id，群消息 sender 取 data.sender.id；逗号分隔的多个消息 ID 必须来自同一 sender。仅 WhatsApp 支持双省略或 trim 后双空标记整会话已读。Telegram 使用单个已接收消息 ID 字符串，trim 后只含 ASCII 数字且数值在 1–2147483647，拒绝非空 sender 及整会话省略形式。runner 无法推断渠道，保留 Telegram 单 ID 输入；调用前按渠道核对文档。非空 sender 缺少非空消息时本地拒绝。保持字符串原文，修改 sender 后重新确认。

## Webhook 归属及替换

list/get/deactivate/delete 使用 query.account_id；create/update 使用 body.account_id。必须精确大小写且只提供一个非空字符串；数组 Query、null、空白及错误位置均拒绝。CLI 在 JSON 解析掩盖重复键前拒绝重复 account_id。list 省略筛选仅返回 workspace 端点；提供筛选仅返回账号独立配置，不混入继承配置。

create 绑定账号，省略则创建 workspace 端点；update 的 account_id 只校验原归属，不能换账号、清除绑定或转换归属，省略则保留。read/deactivate/delete 的归属由服务端校验。PATCH 替换配置，必须提交全部保留设置和已安全保存的 signing secret；省略可能关闭签名或重置事件/重试。不得从脱敏输出推断密钥。每账号最多一个 active 独立端点；409 account_webhook_already_exists（40008）需要核对，不自动重试。停用或订阅不匹配不会回退 workspace；删除最后一个独立端点后，后续初始投递恢复继承。HMAC 包含原样 account scope，改变必须重新预览。既有 HTTPS/公网边界、脱敏及 destructive opt-in 仍适用。

## 验证及回退

先完成文档及 mock 读写验证，真实账号业务验收单独进行。回退时重装此前审查的不可变 1.0.0 bundle，新字段/动作将不可用；回退不能撤销既有 API 副作用，也不能迁移 Webhook 归属。报告问题时不得附带凭据或客户数据。
