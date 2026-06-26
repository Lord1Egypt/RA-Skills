# 手机实名校验

## 接口信息

- 接口地址： https://v.juhe.cn/telecom/query
- 请求方式：http get/post
- 返回类型：json
- 接口描述：核验手机运营商三要素（手机号码、姓名、身份证号）信息是否一致。

## 请求header

- Content-Type: application/x-www-form-urlencoded

## 请求参数

| 名称     | 必填 | 类型   | 说明                                                           |
| -------- | ---- | ------ | -------------------------------------------------------------- |
| key      | 是   | string | 在个人中心->我的数据,接口名称上方查看                          |
| realname | 是   | string | 姓名                                                           |
| idcard   | 是   | string | 身份证号码                                                     |
| mobile   | 是   | string | 手机号码                                                       |
| type     | 否   | int    | 是否显示手机运营商（说明：1：显示；0：不显示（默认））         |
| showid   | 否   | int    | 是否显示聚合订单号（说明：1：显示；0：不显示（默认））         |
| province | 否   | int    | 是否显示手机号归属地（说明：1：显示；0：不显示（默认））       |
| detail   | 否   | int    | 是否显示匹配详情码（说明：1：显示；0(或其他)：不显示（默认）） |

## 返回参数

| 名称       | 类型       | 说明                                                                                                                                                                                                |
| ---------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| error_code | int        | 状态码                                                                                                                                                                                              |
| reason     | string     | 状态提示                                                                                                                                                                                            |
| result     | jsonObject | 返回结果                                                                                                                                                                                            |
| res        | int        | 核验结果                                                                                                                                                                                            |
| resmsg     | string     | 核验结果描述                                                                                                                                                                                        |
| type       | string     | 手机运营商，请求参数type=1时显示                                                                                                                                                                    |
| orderid    | string     | 聚合订单号，请求参数showid=1时显示                                                                                                                                                                  |
| province   | string     | 手机号归属省份，请求参数province=1时，显示                                                                                                                                                          |
| city       | string     | 手机号归属城市，请求参数province=1时显示                                                                                                                                                            |
| rescode    | string     | 匹配详情码，请求参数detail=1时显示（说明 1：三要素核验一致 2：三要素核验不一致0                                                                                                                     |
| resmsg     | string     | 核验结果描述                                                                                                                                                                                        |
| type       | string     | 手机运营商，请求参数type=1时显示                                                                                                                                                                    |
| orderid    | string     | 聚合订单号，请求参数showid=1时显示                                                                                                                                                                  |
| province   | string     | 手机号归属省份，请求参数province=1时，显示                                                                                                                                                          |
| city       | string     | 手机号归属城市，请求参数province=1时显示                                                                                                                                                            |
| rescode    | string     | 匹配详情码，请求参数detail=1时显示（说明：11：一致；21：姓名不一致；22：身份证不一致；23：姓名身份证均不一致；24：不一致，具体不一致要素未知；简版接口，不一致情况下rescode固定返回24，一致返回11） |

## 返回示例

```
//查询成功
{
	"reason":"成功",
	"result":{
		"realname":"****",
		"mobile":"************",
		"idcard":"********************",
		"res":1,
		"resmsg":"三要素身份验证一致",
		"orderid":"J2023120516063890969J",
		"type":"电信",
		"province":"江苏省",
		"city":"苏州市",
		"rescode":"11"
	},
	"error_code":0
}

//查无记录
{
	"reason":"查询无此记录",
	"result":null,
	"error_code":220803
}

//参数错误
{
	"reason":"参数错误:姓名不合法",
	"result":null,
	"error_code":220807
}

```
