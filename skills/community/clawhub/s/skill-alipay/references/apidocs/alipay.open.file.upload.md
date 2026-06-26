# alipay.open.file.upload (支付宝文件上传接口)

**接口用途**：支付宝通用文件上传接口，开发者可调用此接口上传文件，提供给其他业务使用，例如：上传素材（视频/图片），供给到生活号+/小程序等业务使用。

**文档地址**：https://opendocs.alipay.com/mini/03hvl1

**注意**：

- 本接口为文件上传类接口，需要使用 `multipart/form-data` 格式提交数据
- 如使用支付宝 SDK，可参考示例代码接入
- 如未使用 SDK 自行构造 HTTP 请求：
    - v2 版本接口：参考「自行实现签名」文档中文件上传部分的说明
    - v3 版本接口：参考「签名规则」文档中文件上传请求部分的说明

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

| 参数                 | 类型                   | 必填 | 说明                                                        |
|--------------------|----------------------|----|-----------------------------------------------------------|
| `biz_code`         | string               | 是  | 素材使用场景，请关联其他开放平台接口联合使用。如果素材用于内容发布，请必传入 `content_creation` |
| `file_content`     | byte[]               | 是  | 文件内容的二进制流，最大为512MB（512000000字节）                           |
| `md5`              | string               | 否  | 文件的md5值，如果不传则不校验md5                                       |
| `extra_parameters` | FileUploadExtraParam | 否  | 文件额外参数，见下方子属性                                             |

#### extra_parameters（文件上传额外参数）子参数

| 参数              | 类型     | 必填 | 说明                                                                     |
|-----------------|--------|----|------------------------------------------------------------------------|
| `extern_upload` | string | 否  | 是否同步上传到其他平台。素材类型为视频且需要同步优酷，请必传入参数 `youku`，素材接口将代上传到优酷账号；素材类型为图片，无需传入参数 |

### 公共响应参数

| 参数         | 类型     | 必填 | 说明      |
|------------|--------|----|---------|
| `code`     | string | 是  | 网关返回码   |
| `msg`      | string | 是  | 网关返回码描述 |
| `sub_code` | string | 否  | 业务返回码   |
| `sub_msg`  | string | 否  | 业务返回码描述 |
| `sign`     | string | 是  | 签名      |

### 业务响应参数

| 参数          | 类型     | 必填 | 说明                                                          |
|-------------|--------|----|-------------------------------------------------------------|
| `file_id`   | string | 是  | 文件id，用于提供后后续业务调用使用                                          |
| `extern_id` | string | 否  | 视频资源id，同步外部渠道后，外部渠道返回的id。目前支持同步优酷场景，返回优酷视频id，用于支付宝客户端播放视频使用 |

### 错误码

| 错误码               | 说明           | 解决方案                    |
|-------------------|--------------|-------------------------|
| `BIZ_ERROR`       | 业务异常，账号未绑定优酷 | 将支付宝账号绑定优酷服务            |
| `FILE_CHECK_FAIL` | 文件MD5值校验失败   | 确认MD5值是否正确，如果MD5值正确，可重试 |

### 请求示例

```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.open.file.upload&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'app_auth_token=${app_auth_token}' \
 -F 'biz_code=content_creation' \
 -F 'md5=9cff2d79bc81acf12abbaca7328a4dc5' \
 -F 'extra_parameters={"extern_upload":"youku"}' \
 -F 'file_content=@/home/admin/test.jpg'
```

### 响应示例

```json
{
  "alipay_open_file_upload_response": {
    "code": "10000",
    "msg": "Success",
    "file_id": "A*6XqwQKpS1t0AAAAAAAAAAAAADi92AA",
    "extern_id": "XNTk0NjE5NjI4OA=="
  },
  "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```

> 说明：本示例仅供参考。
