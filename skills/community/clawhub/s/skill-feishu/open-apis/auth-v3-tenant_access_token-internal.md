# 自建应用获取 tenant_access_token

## 注意事项

`tenant_access_token` 的最大有效期是 2 小时。

- 剩余有效期小于 30 分钟时，调用本接口会返回一个新的 `tenant_access_token`，这会同时存在两个有效的 `tenant_access_token`。
- 剩余有效期大于等于 30 分钟时，调用本接口会返回原有的 `tenant_access_token`。

## 权限要求

### 必要权限

无需权限

### 可选权限

无需权限

## 接口信息

| API 路径 | `https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal` |
|----------|--------------------------------------------------------------------------|
| 请求方法 | POST |
| 调用频率限制 | - |
| 支持的应用类型 | Custom App |
| 文档地址 | [飞书开放平台](https://open.feishu.cn/document/ukTMukTMukTM/uETNz4SM1MjLxUzM/reference/auth-v3/tenant_access_token/internal) |

## 接口请求

### 请求头

| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `Content-Type` | string | 是 | 固定值："application/json; charset=utf-8" |

### 请求参数

无查询参数

### 请求体

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，创建应用后获得。有关 `app_id` 的详细介绍，请参考[通用参数](https://open.feishu.cn/document/ukTMukTMukTM/uYTM5UjL2ETO14iNxkTN/terminology)介绍 |
| `app_secret` | string | 是 | 应用秘钥，创建应用后获得。有关 `app_secret` 的详细介绍，请参考[通用参数](https://open.feishu.cn/document/ukTMukTMukTM/uYTM5UjL2ETO14iNxkTN/terminology)介绍 |

### 请求示例

#### cURL 请求示例

```bash
curl -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d '{
    "app_id": "cli_slkdjalasdkjasd",
    "app_secret": "dskLLdkasdjlasdKK"
  }'
```

#### Python 请求示例

```python
import requests
import json

def main():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "app_id": "cli_slkdjalasdkjasd",
        "app_secret": "dskLLdkasdjlasdKK"
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
```

#### Go 请求示例

```go
import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
)

func main() {
	url := "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
	
	data := map[string]string{
		"app_id":     "cli_slkdjalasdkjasd",
		"app_secret": "dskLLdkasdjlasdKK",
	}
	
	jsonData, _ := json.Marshal(data)
	
	req, _ := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	req.Header.Set("Content-Type", "application/json; charset=utf-8")
	
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	defer resp.Body.Close()
	
	fmt.Println("Response status:", resp.Status)
}
```

## 接口响应

### 响应头

| 名称 | 类型 | 描述 |
|------|------|------|
| - | - | 无额外响应头字段 |

### 响应体

| 字段 | 类型 | 描述 |
|------|------|------|
| `code` | int | 错误码，非 0 取值表示失败 |
| `msg` | string | 错误描述 |
| `tenant_access_token` | string | 租户访问凭证 |
| `expire` | int | `tenant_access_token` 的过期时间，单位为秒 |

### 响应示例

```json
{
    "code": 0,
    "msg": "ok",
    "tenant_access_token": "t-caecc734c2e3328a62489fe0648c4b98779515d3",
    "expire": 7200
}
```

## 响应码定义

### 成功码

| HTTP状态码 | 错误码 | 描述 |
|------------|--------|------|
| 200 | 0 | 请求成功 |

### 客户端错误码 (4xx)

| HTTP状态码 | 错误码 | 描述 |
|------------|--------|------|
| - | - | 暂无（具体错误码请参考[通用错误码](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN)） |

### 服务端错误码 (5xx)

| HTTP状态码 | 错误码 | 描述 |
|------------|--------|------|
| - | - | 暂无 |

## 附录

### 相关链接

| 链接类型 | 链接 |
|----------|------|
| 通用参数 | [https://open.feishu.cn/document/ukTMukTMukTM/uYTM5UjL2ETO14iNxkTN/terminology](https://open.feishu.cn/document/ukTMukTMukTM/uYTM5UjL2ETO14iNxkTN/terminology) |
| 通用错误码 | [https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN) |