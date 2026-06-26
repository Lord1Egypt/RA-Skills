# ant.merchant.expand.indirect.image.upload (图片上传接口)

**接口用途**：图片上传。

**注意**：本接口为文件上传类接口，与普通OpenAPI接口的入参构造格式不同，如果您没有使用官方SDK发起OpenAPI调用，自行构造HTTP请求时，需要使用multipart/form-data格式发起请求，注意以下事项：

1. 文件参数单独作为一个part，key为参数名，内容为文件，需要携带完整文件名（例如：Content-Disposition: form-data; name="
   file_content"; filename="example.png"），缺少文件名或后缀，会提示为类型错误
2. 其余参数，对于v2版本的协议，公共参数需要使用query传入，业务参数使用query或body传入，使用body时每个字段作为一个单独part；v3协议需要按接口约定位置传入

**文档地址**：https://opendocs.alipay.com/solution/d0814d9c_ant.merchant.expand.indirect.image.upload

### 公共请求参数

| 参数               | 类型     | 必填 | 说明                             |
|------------------|--------|----|--------------------------------|
| `app_id`         | string | 是  | 支付宝分配给开发者的应用ID                 |
| `method`         | string | 是  | 接口名称                           |
| `format`         | string | 否  | 仅支持JSON                        |
| `charset`        | string | 是  | 请求使用的编码格式，如utf-8, gbk, gb2312等 |
| `sign_type`      | string | 是  | 签名算法类型：RSA2或RSA，推荐使用RSA2       |
| `sign`           | string | 是  | 商户请求参数的签名串                     |
| `timestamp`      | string | 是  | 发送请求的时间，格式yyyy-MM-dd HH:mm:ss  |
| `version`        | string | 是  | 接口版本，固定为1.0                    |
| `app_auth_token` | string | 否  | 应用授权令牌                         |

### 业务请求参数

| 参数              | 类型     | 必填 | 说明                             |
|-----------------|--------|----|--------------------------------|
| `image_type`    | string | 是  | 图片格式，支持格式：bmp、jpg、jpeg、png、gif |
| `image_content` | byte[] | 是  | 图片二进制字节流，最大为10M                |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数         | 类型     | 必填 | 说明           |
|------------|--------|----|--------------|
| `image_id` | string | 是  | 图片在文件存储平台的标识 |

### 错误码

| 错误码                         | 说明                | 解决方案                                        |
|-----------------------------|-------------------|---------------------------------------------|
| `SYSTEM_ERROR`              | 系统繁忙              | 服务器异常，可能发生了网络或者系统异常，导致服务调用失败，商户可以用同样的请求发起重试 |
| `EXCEED_MAX_SIZE`           | 超过单个图片允许的最大值（10M） | 请适当压缩图片大小以免超过上传限制                           |
| `IMAGE_UNSAFE`              | 文件未通过安全校验         | 图片中可能注入了恶意代码，请重新制作图片                        |
| `INVALID_IMAGE_FORMAT`      | 文件格式不支持           | 请不要使用非常用的图片格式，如CMYK                         |
| `MERCHANT_ILLEGAL_ARGUMENT` | 参数格式非法            | 参数格式非法，请检查                                  |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=ant.merchant.expand.indirect.image.upload&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'image_type=jpg' \
 -F 'image_content=@/home/admin/test.jpg'
```

### 响应示例

```json
{
  "ant_merchant_expand_indirect_image_upload_response": {
    "code": "10000",
    "msg": "Success",
    "image_id": "a5d373f6-3e79-405f-9993-fb7ea051c372.jpg"
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。