# douyin.open.client.token (生成 client_token)

## 接口说明

该接口用于获取接口调用的凭证 `client_token`。该接口适用于抖音授权；

业务场景：`client_token` 用于**不需要用户授权**就可以调用的接口。

## 注意事项

- `client_token` 的有效时间为 **2 个小时**，重复获取 `client_token` 后会使上次的 `client_token` 失效（但有 5
  分钟的缓冲时间，连续多次获取 `client_token` 只会保留最新的两个 `client_token`）。
- 禁止频繁调用 access-token 接口（频控规则：5 分钟内超过 500 次接口调用，接口报错，错误码 10020）。
- 正式上线后，测试环境不能使用正式的 `client_key`、`client_secret` 获取 token，否则会导致线上正式环境的 token 失效，影响线上业务。

## 基本信息

| 名称          | 描述                                            |
|-------------|-----------------------------------------------|
| HTTP URL    | `https://open.douyin.com/oauth/client_token/` |
| HTTP Method | POST                                          |

## 请求参数

### 请求头

| 参数           | 必填 | 类型     | 说明                     |
|--------------|----|--------|------------------------|
| Content-Type | 是  | String | 固定值 `application/json` |

### Body

| 参数            | 必填 | 类型     | 示例                                  | 说明                               |
|---------------|----|--------|-------------------------------------|----------------------------------|
| client_key    | 是  | String | `ttxxxxxx`                          | 应用唯一标识。获取方式参考：小程序通用参数、移动网站应用通用参数 |
| client_secret | 是  | String | `7802f4e6f243e659d51135445fe******` | 应用的密钥，用于获取接口调用凭证                 |
| grant_type    | 是  | String | `client_credential`                 | 固定值 `client_credential`          |

## 请求示例

```bash
curl --location 'https://open.douyin.com/oauth/client_token/' \
--header 'Content-Type: application/json' \
--data '{
    "grant_type": "client_credential",
    "client_key": "ttxxxxxx",
    "client_secret": "7802f4e6f243e659d51135445fe********"
}'
```

## 响应参数

| 参数                | 类型      | 说明                      |
|-------------------|---------|-------------------------|
| data              | Struct  | 响应数据                    |
| data.access_token | String  | 接口调用凭证                  |
| data.expires_in   | Integer | 凭证有效时间，单位：秒（7200 = 2小时） |
| data.description  | String  | 错误描述                    |
| data.error_code   | Integer | 错误码，0 表示成功              |
| message           | String  | 请求响应信息                  |

### 响应示例

正常响应：

```json
{
  "data": {
    "access_token": "clt.75c380db41e815978a733994d96f5d23RqilUxH48iobyWhbIOQFo******",
    "description": "",
    "error_code": 0,
    "expires_in": 7200
  },
  "message": "success"
}
```

异常响应：

```json
{
  "data": {
    "error_code": 10003,
    "description": "client_key 或者 client_secret 报错"
  },
  "message": "error"
}
```

## 错误码

| HTTP 状态码 | 错误码   | 错误码描述                          | 排查建议                               |
|----------|-------|--------------------------------|------------------------------------|
| 200      | 10002 | 参数错误                           | 检查参数是否漏传                           |
| 200      | 10003 | client_key 不存在                 | 检查 client_key 参数是否正确               |
| 200      | 10013 | client_key 或者 client_secret 报错 | 检查 client_key 和 client_secret 是否正确 |

