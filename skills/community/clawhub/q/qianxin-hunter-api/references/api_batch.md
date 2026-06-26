# 批量查询接口

更新时间：2023/01/11

**批量检索Api**

- 平台支持用户通过搜索语法或上传文件的形式，进行批量检索。平台将生成异步任务，任务结果将以文件形式导出，可通过接口查看任务执行进度。
- 上传文件批量搜索，所支持文件格式为：csv。可参照如下模板进行填写，需从表格第二行起填写检索目标，检索结果将从第二行起生效。
- [ 模板下载](https://hunter.qianxin.com/api/search/batch/template?type=api)

**批量检索:**

- 接口地址：/openApi/search/batch
- 请求方式：POST
- 接口说明：该接口支持通过搜索语法或上传文件的方式进行批量查询。接口调用成功后将返回任务id。可使用任务id查看任务执行进度和下载导出文件。

**query参数说明:**

| api-key      | 是   | api-key，用户登录后在个人中心获取                            |
| ------------ | ---- | ------------------------------------------------------------ |
| search       | 否   | 经过符合RFC 4648标准的base64url编码编码后的搜索语法，语法规则见首页-查询语法 |
| start_time   | 否   | 开始时间，格式为2021-01-01(时间范围超出近30天，将扣除权益积分) |
| end_time     | 否   | 结束时间，格式为2021-03-01(时间范围超出近30天，将扣除权益积分) |
| is_web       | 否   | 是否网站资产，1代表”是“，2代表”否“                           |
| status_code  | 否   | 状态码列表，以逗号分隔，如”200,401“                          |
| fields       | 否   | 可选返回字段，以逗号分隔，枚举值有: "ip,port,domain,ip_tag,url,web_title,is_risk_protocol,protocol,base_protocol,status_code,os,company,number,icp_exception,country,province,city,is_web,isp,as_org,cert_sha256,ssl_certificate,component,asset_tag,updated_at,header,header_server,banner" |
| search_type  | 否   | 上传文件的类型，枚举值：all、ip、domain、company，默认为all。all代表混合检索，包括ip、ip段或域名（此处域名检索效果为domain.suffix语法的检索结果），最多10个；ip代表仅ip、ip段进行精确检索，最多100个；domain代表仅域名（此处域名检索效果为domain.suffix语法的检索结果）进行检索，最多100个；company代表仅企业名称（此处企业名称检索效果为icp.name语法的精确检索结果）进行检索，最多100个 |
| assets_limit | 否   | 数字，数值表示预期导出的资产数量                             |

**BASH请求格式：**

方式一：传文件

```
curl -X POST -k -F "file=@C:/Users/{user}/Desktop/batch_file_template.csv" "https://hunter.qianxin.com/openApi/search/batch?api-key={api-key}&is_web=1&start_time=2021-01-01&end_time=2021-03-01"
        
```


![img](https://hunter.qianxin.com/geagle/static/img/17.b32c687f.png)

方式二：传语法

```
curl -X POST -k "https://hunter.qianxin.com/openApi/search/batch?api-key={api-key}&search={search}&is_web=1&start_time=2021-01-01&end_time=2021-03-01"
        
```


![img](https://hunter.qianxin.com/geagle/static/img/17-1.93bd197c.png)**正确响应示例：**

批量查询之后请保留"task_id"，供查看任务进度和下载文件时使用

```
  {
      "code": 200,
      "data": {
          "task_id": 1728,
          "filename": "assets_api_20210915_175148.csv",
          "consume_quota": "消耗积分：20",
          "rest_quota": "今日剩余积分：77"
      },
      "message": "success"
  }
        
```

**错误响应示例：**

```
  {
    "code": 400,
    "message": "上传失败",
    "data"： null
  }
        
```

**查看导出进度**

- 接口地址：/openApi/search/batch/{task_id}
- 请求方式：GET
- 接口说明：该接口用于查看任务执行进度。

**BASH请求格式：**

```
  curl -X GET –k "https://hunter.qianxin.com/openApi/search/batch/{task_id}?api-key={api-key}"          
```

**正确响应示例：**

```
  {
  "code": 200,
  "message": "success",
  "data"： {
    "status": "已完成",
    "progress": "100%",
    "rest_time": "0s"
  }
  }
          
```

**错误响应示例：**

```
  {
  "code": 400,
  "message": "任务不存在",
  "data"： null
  }
          
```

**下载导出文件**

- 接口地址：/openApi/search/download/{task_id}
- 请求方式：GET
- 接口说明：该接口用于下载导出文件。

**BASH请求格式：**

```
  curl -X GET -k "https://hunter.qianxin.com/openApi/search/download/{task_id}?api-key={api-key}" –o output.csv
            
```

- 请求参数说明：
- –o output.csv 将响应内容输出到指定文件
- –O 将响应内容输出到文件，以url为文件名

**错误响应示例1：**

```
  {
    "code": 400,
    "message": "任务不存在",
    "data"： null
  }
            
```

**错误响应示例2：**

```
  {
    "code": 400,
    "message": "文件生成中，请稍后",
    "data"： null
  }
```