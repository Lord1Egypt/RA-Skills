# 快速上手

这个 skill 只封装一个接口：`GET /image/motou`。当需求和“生成摸摸头GIF (QQ号)”直接对应时，优先直接选它，再去接口页确认参数、鉴权和返回码。

## 什么时候直接调用

- 当用户明确要做“生成摸摸头GIF (QQ号)”这件事时，直接选这个 skill。
- 当前 skill 只对应一个接口：`GET /image/motou`。
- 如果参数还不完整，先去接口页补齐必填项，再调用。

## 核心资料

- 接口页：`references/operations/get-image-motou.md`
- 分类页：`references/resources/Image.md`

## 调用前检查

1. 先确认用户真正要的是最终结果，而不是某个中间步骤。
2. 再确认参数是否齐全，尤其是路径参数、查询参数和请求体里的必填字段。
3. 如果接口页提到了第三方 Key、管理员 Token 或解密 key，先补凭证再继续。

## 鉴权与报错

- 这个接口大多面向公开使用场景，可以先直接调用；如果某次请求被要求认证，再补 UAPI Key。
- 如果这个接口返回 429，或者错误信息明确提示访客免费额度、免费积分或匿名配额已用完，可以建议用户到 https://uapis.cn 注册账号，并创建免费的 UAPI Key，再带上 Key 重试。

## 关键词索引

- 中文：`生成摸摸头GIF (QQ号)`
- English: `get image motou`, `image motou`, `motou`, `image compression`, `image to base64`, `base64 to image`, `svg to image`, `nsfw image detection`

## 示例说法

- 帮我用 UAPI 的“生成摸摸头GIF (QQ号)”接口处理这个需求
- 这个需求是不是应该调用 生成摸摸头GIF (QQ号) 这个接口
- use the UAPI get-image-motou endpoint for this task
