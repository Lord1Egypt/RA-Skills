# 语法查询接口

更新时间：2023/01/11



- 接口地址：/openApi/search
- 请求方式：GET
- 接口说明：该接口适用于对小批量数据进行语法查询。平台支持自动Api生成， 用户可在搜索列表页搜索后获取自动生成的Api，可生成的语法类型包括bash、golang、python和php。

**query参数说明：**

| api-key     | 是   | api-key，用户登录后在个人中心获取                            |
| ----------- | ---- | ------------------------------------------------------------ |
| search      | 是   | 经过符合RFC 4648标准的base64url编码编码后的搜索语法，语法规则见首页-查询语法 |
| start_time  | 否   | 开始时间，格式为2021-01-01(时间范围超出近30天，将扣除权益积分) |
| end_time    | 否   | 结束时间，格式为2021-03-01(时间范围超出近30天，将扣除权益积分) |
| page        | 是   | 页码                                                         |
| page_size   | 是   | 每页资产条数                                                 |
| is_web      | 否   | 资产类型，1代表”web资产“，2代表”非web资产“，3代表”全部“      |
| status_code | 否   | 状态码列表，以逗号分隔，如”200,401“                          |
| fields      | 否   | 可选返回字段，以逗号分隔，枚举值有: "ip,port,domain,ip_tag,url,web_title,is_risk_protocol,protocol,base_protocol,status_code,os,company,number,icp_exception,country,province,city,is_web,isp,as_org,cert_sha256,ssl_certificate,component,asset_tag,updated_at,header,header_server,banner" |

**BASH请求格式：**

```
curl -X GET -k "https://hunter.qianxin.com/openApi/search?api-key={api-key}&search={search}&page=1&page_size=10&is_web=1&start_time=2021-01-01&end_time=2021-03-01"
        
```

**Golang 编码样例：**

```
package main
import (
    "encoding/base64"
    "fmt"
)
func main() {
    search := `title="北京"`
    search = base64.URLEncoding.EncodeToString([]byte(search))
    fmt.Println("search: ", search)
}
        
```

**Python 编码样例：**

```
import base64
search = 'title="北京"'
search = base64.urlsafe_b64encode(search.encode("utf-8"))
print("search:", search)
        
```

**Php 编码样例：**

```
<?php
$search = 'title="北京"';
$search = strtr(base64_encode($search), '+/', '-_');
printf("search: %s", $search);
?>
        
```

**正确响应示例：**

```
{
    "code": 200,
    "message": "success",
    "data": {
        "account_type": "个人账号",
        "total": 1,
        "time": 1,
        "arr": [
            {
                "ip": "127.0.0.1",
                "port": 443,
                "domain": "abc.qianxin.com",
                "ip_tag": "CDN,云厂商",
                "url": "https://abc.qianxin.com",
                "web_title": "欢迎登录",
                "is_risk_protocol": "否",
                "protocol": "https",
                "base_protocol": "tcp",
                "status_code": 200,
                "os": "linux",
                "company": "奇安信科技集团股份有限公司",
                "number": "京ICP备16020626号-8",
                "icp_exception": [
                    "页面多备案号",
                    "备案跳转异常"
                ],
                "country": "中国",
                "province": "山东省",
                "city": "济南市",
                "is_web": "是",
                "isp": "中国电信",
                "as_org": "Chinanet",
                "cert_sha256": "4e71bb0cb707d3b9fbb832938efacbd480d8b50c86899c3f370bc63a66be2bdd",
                "ssl_certificate": "xxx",
                "component": [
                    {
                        "name": "Nginx",
                        "version": "1.20.2"
                    }
                ],
                "asset_tag": "Web servers,登录页面",
                "updated_at": "2025-01-01",
                "header": "xxx",
                "header_server": "nginx",
                "banner": "xxx"
            }
        ],
        "consume_quota": "消耗积分：1",
        "rest_quota": "今日剩余积分：499",
        "syntax_prompt": ""
    }
}
        
```

**错误响应示例：**

```
{
  "code": 400,
  "message": "任务不存在",
  "data": null
}
        
```