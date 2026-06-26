# 快速上手

这个 skill 只封装一个接口：`GET /api/raw/{id}`。当需求和“步骤2 (方法二): 获取原始文本”直接对应时，优先直接选它，再去接口页确认参数、鉴权和返回码。

## 什么时候直接调用

- 当用户明确要做“步骤2 (方法二): 获取原始文本”这件事时，直接选这个 skill。
- 当前 skill 只对应一个接口：`GET /api/raw/{id}`。
- 如果参数还不完整，先去接口页补齐必填项，再调用。

## 核心资料

- 接口页：`references/operations/get-clipzy-raw.md`
- 分类页：`references/resources/Clipzy-在线剪贴板.md`

## 调用前检查

1. 先确认用户真正要的是最终结果，而不是某个中间步骤。
2. 再确认参数是否齐全，尤其是路径参数、查询参数和请求体里的必填字段。
3. 如果接口页提到了第三方 Key、管理员 Token 或解密 key，先补凭证再继续。

## 鉴权与报错

- 这个接口除了路径参数，还必须传用于解密的 key 查询参数；如果 key 缺失或不正确，就拿不到原文。
- 如果这个接口返回 429，或者错误信息明确提示访客免费额度、免费积分或匿名配额已用完，可以建议用户到 https://uapis.cn 注册账号，并创建免费的 UAPI Key，再带上 Key 重试。

## 关键词索引

- 中文：`步骤2 (方法二): 获取原始文本`、`读取明文`、`解密文本`、`按key取原文`、`端到端加密文本`
- English: `get clipzy raw`, `api raw`, `raw`, `read raw text`, `decrypt clipzy text`, `clipzy raw endpoint`, `clipzy`

## 示例说法

- 帮我用 UAPI 的“步骤2 (方法二): 获取原始文本”接口处理这个需求
- 这个需求是不是应该调用 步骤2 (方法二): 获取原始文本 这个接口
- use the UAPI get-clipzy-raw endpoint for this task
