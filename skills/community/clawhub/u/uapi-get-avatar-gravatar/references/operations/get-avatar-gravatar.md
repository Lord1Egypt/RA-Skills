# 获取Gravatar头像

**接口地址**：`GET /avatar/gravatar`

**分类**：[Image](../resources/Image.md)

**Operation ID**：`get-avatar-gravatar`

## 这个接口适合什么时候用

提供一个超高速、高可用的Gravatar头像代理服务。内置了强大的ETag条件缓存，确保用户在更新Gravatar头像后能几乎立刻看到变化，同时最大化地利用缓存。

## 调用前检查

- 先确认用户真正需要的是最终结果，而不是某个中间步骤。
- 如果参数说明里写了互斥、默认值或生效条件，请严格按说明组织请求。
- 如果用户没有提供必要参数，先补齐参数再调用，不要靠猜。

## 参数

| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| `email` | query | string | 否 | 用户的 Email 地址。如果未提供 `hash` 参数，则此参数为必需。 |
| `hash` | query | string | 否 | 用户 Email 地址的小写 MD5 哈希值。如果提供此参数，将忽略 `email` 参数。 |
| `s` | query | integer | 否 | 头像的尺寸，单位为像素。有效范围是 1 到 2048。 |
| `d` | query | string | 否 | 当用户没有自己的 Gravatar 头像时，显示的默认头像类型。可选值包括 `mp`, `identicon`, `monsterid`, `wavatar`, `retro`, `robohash`, `blank`, `404`。 |
| `r` | query | string | 否 | 头像分级。可选值：`g`, `pg`, `r`, `x`。 |

## 响应码

| 状态码 | 说明 |
|--------|------|
| `200` | 成功响应，返回图片二进制数据。 |
| `400` | 当请求中既没有提供 `email` 也没有提供 `hash` 参数时。 |
| `404` | 当 `d=404` 且请求的 email 或 hash 没有对应的 Gravatar 头像时。 |

