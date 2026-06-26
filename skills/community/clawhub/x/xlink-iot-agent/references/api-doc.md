

### 1.获取设备列表 

返回格式：简化格式`{"count":n,"list":[...]}`

接口描述：

跨产品查询设备列表，支持分类过滤和结构化查询

请求URL：/v2/devices/def-filter/aggregates?type=all

请求方式：POST


请求参数：

| 参数名           | 位置 | 是否必须 | 类型   | 说明                                                         |
| ---------------- | ---- | -------- | ------ | ------------------------------------------------------------ |
| offset           | Body | 否       | Int    | 从某个偏移量开始请求，默认为0                                |
| limit            | Body | 否       | Int    | 请求的条目数量，默认为10                                     |
| order            | Body | 否       | Object | 可以指定通过设备默认的某个字段排序，desc降序，asc升序        |
| filter           | Body | 是       | Object | 指定返回字段                                                 |
| filter.device    | Body | 否       | Array  | 指定设备信息返回字段，可选字段：id,mac,name,is_active,active_date,mcu_mod,mcu_version,firmware_mod,firmware_version,product_id,sn,create_time,groups,last_reset,gateway_id,project_id,tags_map,space_id,space_type |
| filter.vdevice   | Body | 否       | Array  | 指定设备状态返回字段，可选字段：last_login,last_logout,connect_protocol,connector_id |
| filter.online    | Body | 否       | Array  | 指定设备在线状态返回字段：可选字段：is_online               |
| filter.geography | Body | 否       | Array  | 指定设备位置信息返回字段：可选字段：country,city,province,district,address |
| filter.product   | Body | 否       | Array  | 指定产品信息返回字段：name、pics                             |
| query            | Body | 否       | Object | 查询条件，可以根据不同字段加上不同的比较指令来查询，查询条件字段包含设备所有默认字段，不支持扩展属性字段，支持比较指令包含如下:in：包含于该列表任意一个值lt：小于该字段值lte：小于或等于字段值gt：大于该字段值gte：大于或等于该字段and：组合并查询字段$or：组合或查询字段 |
| query.logical    | Body | True     | String | 固定为：AND                                                  |
| query.device     | Body | 否       | Object | 通过设备信息字段查询，可选字段：mac,id,product_id,name,create_time,tags_map,project_id,is_exception,project_id,space_id,space_type |
| query.vdevice    | Body | 否       | Object | 通过设备状态字段查询，可选字段：last_login,last_logout,connect_protocol,connector_id |
| query.online     | Body | 否       | Object | 通过设备在线字段查询，可选字段：is_online                   |
| query.geography  | Body | 否       | Object | 通过设备位置字段查询，可选字段：country,city,province        |

请求示例

```text/x-sh
{
    "offset": 0,
    "limit": 10,
    "filter": {
        "device": ["mac", "id", "sn", "name", "project_id"],
        "online": ["is_online"],
        "vdevice": ["online_count", "last_login"]
    },
    "query": {
        "logic":"AND",
        "device": {
            "project_id": {
                "$eq": "XJA1JJAJA"
            },
            "id": {
                "$eq": 452872518
            },
            "$and": [{
                "tags_map": {
                    "$elemMatch": {
                        "key": {
                            "$eq": "Project"
                        },
                        "value": {
                            "$eq": "青创汇"
                        }
                    }
                }
            }, {
                "tags_map": {
                    "$elemMatch": {
                        "key": {
                            "$eq": "Type"
                        },
                        "value": {
                            "$eq": "Light"
                        }
                    }
                }
            }],
            "$or": [{
                "tags_map": {
                    "$elemMatch": {
                        "key": {
                            "$eq": "Project"
                        },
                        "value": {
                            "$eq": "青创汇"
                        }
                    }
                }
            }, {
                "tags_map": {
                    "$elemMatch": {
                        "key": {
                            "$eq": "Project"
                        },
                        "value": {
                            "$eq": "小谷围"
                        }
                    }
                }
            }]
        }
    },
    "order": {}
}
```

返回参数说明

| 字段                           | 必填 | 类型    | 备注                                                         |
| ------------------------------ | ---- | ------- | ------------------------------------------------------------ |
| count                          | True | Int     | 总数量                                                       |
| list                           | True | Array   | 设备列表                                                     |
| list.vdevice                   | 否   | Object  | 设备影子信息                                                 |
| list.vdevice.online_count     | 否   | Int     | 在线时长                                                     |
| list.vdevice.last_login       | 否   | String  | 最近上线时间，yyyy-MM-dd'T'HH:mm:ss.SSS'Z'格式               |
| list.vdevice.last_logout      | 否   | String  | 最近离线线时间，yyyy-MM-dd'T'HH:mm:ss.SSS'Z'格式             |
| list.vdevice.connect_protocol | 否   | Int     | 连接来源协议，枚举值:2                                       |
| list.vdevice.connector_id     | 否   | String  | 根据connect_protocol取值，如果connect_protocol是融合平台，这里取值为融合平台配置ID。 |
| list.geography                 | 否   | Object  | 地理位置                                                     |
| list.geography.country         | 否   | String  | 地理位置-国家                                                |
| list.geography.province        | 否   | String  | 地理位置-省份                                                |
| list.geography.city            | 否   | String  | 地理位置-城市                                                |
| list.geography.district        | 否   | String  | 地理位置-街道                                                |
| list.online                    | 否   | Object  | 在线信息                                                     |
| list.online.is_online         | 否   | Boolean | 是否在线，true在线，false离线                                |
| list.device                    | 否   | Object  | 设备信息                                                     |
| list.device.product_id        | 否   | String  | 产品ID                                                       |
| list.device.id                 | 否   | Int     | 设备ID                                                       |
| list.device.sn                 | 否   | String  | 设备sn                                                       |
| list.device.mac                | 否   | String  | 设备mac                                                      |
| list.device.project_id        | 否   | String  | 项目ID                                                       |
| list.device.name               | 否   | String  | 设备名称                                                     |
| list.device.is_active         | 否   | Boolean | 是否激活                                                     |
| list.device.active_date       | 否   | String  | 激活时间，yyyy-MM-dd'T'HH:mm:ss.SSS'Z'格式                   |
| list.device.mcu_mod           | 否   | String  | MCU型号                                                      |
| list.device.mcu_version       | 否   | Int     | MCU版本号                                                    |
| list.device.firmware_version  | 否   | Int     | 固件版本号                                                   |
| list.device.firmware_mod      | 否   | String  | 固件型号                                                     |
| list.device.create_time       | 否   | String  | 创建时间，yyyy-MM-dd'T'HH:mm:ss.SSS'Z'格式                   |
| list.device.groups             | 否   | List    | 所属设备分组ID列表                                           |
| list.device.last_reset        | 否   | String  | 最近重置时间，yyyy-MM-dd'T'HH:mm:ss.SSS'Z'格式               |
| list.device.gateway_id        | 否   | Int     | 所属网关设备ID                                               |
| list.device.tags_map          | 否   | List    | 设备标签信息                                                 |
| list.device.tags_map.key      | 否   | String  | 标签键                                                       |
| list.device.tags_map.value    | 否   | String  | 标签键的值                                                   |
| list.device.project_id        | 否   | String  | 项目ID                                                       |
| list.device.is_exception      | 否   | Boolean | 是否异常                                                     |
| list.device.space_id          | 否   | String  | 所属空间ID                                                   |
| list.device.space_type        | 否   | String  | 所属空间类型                                                 |

返回示例

```text/x-java
{
    "count": 2,
    "list": [
        {
            "vdevice": {
                "online_count": 13975,
                "last_login": "2019-08-22T17:17:46.26Z"
            },
            "geography": {
              "country": "中国",
              "province": "广东省",
              "city": "广州市",
              "district": ""
            },
            "online": {
                "is_online": false
            },
            "device": {
                   "is_active": true,
                "create_time": "2022-11-16T01:24:06.228Z",
                "active_date": "2022-11-16T15:45:34.502Z",
                "groups": ["4e05e0c83001f400"],
                "mcu_version": 0,
                "firmware_version": 0,
                "mac": "72536ac7-6243-42f1-b001-6f0c8b1e651b",
                "product_id": "16024cc6e782000116024cc6e7822601",
                "name": "0003空气指令变送器_000322070800005",
                "id": 452871922,
                "sn": "",
                "project_id": "",
                "space_id": "",
                "space_type": "",
            }
        }
    ]
}
```

错误码

| 错误码  | 说明         |
| ------- | ------------ |
| 4001001 | type参数错误 |
| 4041070 | 过滤器不存在 |

### 2.获取事件实例列表

**接口描述**

查询全量事件实例列表，支持按状态、时间、设备等条件过滤

**接口URI**

/v2/service/events/all-instances

**接口调用Method**

POST


**请求参数**

| 名称                      | 位置 | 必填  | 类型   | 备注                                                         |
| ------------------------- | ---- | ----- | ------ | ------------------------------------------------------------ |
| offset                    | Body | False | Int    | 偏移量，默认值0                                              |
| limit                     | Body | False | Int    | 查询量，默认值10                                             |
| applications              | Body | False | Array  | 应用类型列表<br>需要查询全部<br>等级<br>时，不传该字段       |
| classification_ids       | Body | False | Array  | 事件分类标识列表<br>需要查询全部等级时，不传该字段           |
| tag_ids                  | Body | False | Array  | 事件标签标识列表<br>需要查询全部等级时，不传该字段           |
| rank_ids                 | Body | False | Array  | 事件等级标识列表<br>需要查询全部等级时，不传该字段           |
| project_ids              | Body | False | Array  | 事件发生的项目标识列表<br>建议前端传业务组织下拥有的项目列表，会做为默认条件 |
| device_name              | Body | False | String | 事件中设备名称,以like查询                                   |
| trigger_condition        | Body | False | String | 事件中触发条件，以like查询                                   |
| processed_operator_name | Body | False | String | 事件处理人名称，以like查询                                   |
| gt_create_time          | Body | False | String | 大于事件触发时间条件<br>格式为2019-11-13T14:54:00.00Z        |
| lt_create_time          | Body | False | String | 小于事件触发时间条件<br>格式为<br>2019-11-13T14:54:00.00Z    |
| name                      | Body | False | String | 事件名称，以like查询                                         |
| status                    | Body | False | Array  | 事件状态<br>1:待处理<br>2:处理中<br>3:已处理              |
| event_ids                | Body | False | Array  | 事件标识列表<br>需要查询全部等级时，不传该字段               |
| processed_ways           | Body | False | Array  | 事件处理类型列表<br>，枚举<br>\-1:未处理<br>1:设备调试<br>2:真实故障<br>3:误报<br>4:其他<br>5:转工单<br>6:抑制7:自动恢复 |
| device_id                | Body | False | Int    | 设备标识                                                     |

```text/x-java
{
	"offset": "偏移量",
	"limit": "查询量",
	"applications": ["应用枚举"],
	"classification_ids": ["分类标识"],
	"tag_ids": ["标签标识"],
	"rank_ids": ["等级标识"],
	"project_ids": ["项目标识"],
	"device_name": "设备名称, 以like查询",
	"trigger_condition": "触发条件, 以like查询",
	"gt_create_time": "大于触发时间",
	"lt_create_time": "小于触发时间",
	"name": "事件名称, 以like查询",
	"status": ["事件状态"],
	"event_ids": ["事件标识"],
	"processed_ways": ["事件处理类型"],
	"device_id": "设备标识"
}
```

**返回参数说明**

| 名称                                              | 必填  | 类型    | 备注                                                         |
| ------------------------------------------------- | ----- | ------- | ------------------------------------------------------------ |
| status                                            | True  | Int     | HTTP状态码                                                   |
| code                                              | False | Int     | 业务错误码                                                   |
| msg                                               | False | String  | 业务错误信息                                                 |
| data                                              | False | Object  | 业务响应数据                                                 |
| data.count                                        | False | Int     | 事件总数                                                     |
| data.list                                         | False | Array   | 事件列表                                                     |
| [data.list.id](http://data.list.id)               | False | String  | 事件标识                                                     |
| data.list.application                             | True  | String  | 事件归属应用枚举                                             |
| data.list.base.create_time                       | False | String  | 事件发生时间                                                 |
| data.list.base.process_time                      | False | String  | 事件处理时间                                                 |
| data.list.base.corp_id                           | False | String  | 事件归属企业                                                 |
| data.list.base.status                             | False | Int     | 事件状态<br>1:待处理<br>2:处理中<br>3:已处理              |
| data.list.base.classification_id                 | False | String  | 事件归属分类标识                                             |
| data.list.base.rank_id                           | False | String  | 事件归属等级标识                                             |
| [data.list.base.name](http://data.list.base.name) | False | String  | 事件名称                                                     |
| data.list.base.desc                               | False | String  | 事件描述                                                     |
| data.list.base.project_id                        | False | String  | 事件归属项目标识                                             |
| data.list.base.area_id                           | False | String  | 事件归属片区标识                                             |
| data.list.base.definition_id                     | False | String  | 事件归属定义标识                                             |
| data.list.base.biz_organization_id              | False | String  | 事件归属业务组织标识                                         |
| data.list.base.source                             | False | String  | 事件源                                                       |
| data.list.base.regions                            | False | Array   | 事件实例所属区域列表                                         |
| data.list.base.full_biz_organization_id        | False | String  | 所属业务组织全标识，A:B:C:D:E:F:G                            |
| data.list.base.<br>tag_id                        | False | String  | 事件标签标识                                                 |
| data.list.base.<br>space_group_location         | False | String  | 事件所属管理区域(空间分组)位置名称，所有管理区域名称，以分隔符/拼接 |
| data.list.base.<br>space_location                | False | String  | 事件所属空间位置名称，全名称，以分隔符/拼接                  |
| data.list.base.product_id                        | False | String  | 事件关联产品标识                                             |
| data.list.base.<br>device_id                     | False | String  | 事件关联设备标识                                             |
| data.list.base.<br>device_name                   | False | String  | 事件关联设备名称                                             |
| data.list.base.<br>device_mac                    | False | String  | 事件关联设备mac                                              |
| data.list.base.<br>trigger_condition             | False | String  | 时间关联触发条件规则                                         |
| data.list.base.<br>project_name                  | False | String  | 事件所属项目名称                                             |
| data.list.base.address                            | False | String  | 事件发生详细地址                                             |
| data.list.base.rank_name                         | False | String  | 事件归属等级名称                                             |
| data.list.base.processed_way                     | Fase  | Int     | 事件已处理处理方式<br>，枚举<br>\-1:未处理<br>1:设备调试<br>2:真实故障<br>3:误报<br>4:其他<br>5:转工单<br>6:抑制7:自动恢复 |
| data.list.base.first_expire                      | False | Boolean | 一级是否超时                                                 |
| data.list.base.second_expire                     | False | Boolean | 二级是否超时                                                 |
| data.list.base.third_expire                      | False | Boolean | 三级是否超时                                                 |
| data.list.base.area_id                           | False | String  | 空间区域标识                                                 |
| data.list.base.area_name                         | False | String  | 空间区域名称                                                 |
| data.list.base.build_id                          | False | String  | 空间楼栋标识                                                 |
| data.list.base.build_name                        | False | String  | 空间楼栋名称                                                 |
| data.list.base.unit_id                           | False | String  | 空间单元标识                                                 |
| data.list.base.unit_name                         | False | String  | 空间单元名称                                                 |
| data.list.base.floor_id                          | False | String  | 空间楼层标识                                                 |
| data.list.base.floor_name                        | False | String  | 空间楼层名称                                                 |
| data.list.base.house_id                          | False | String  | 空间房屋标识                                                 |
| data.list.base.house_name                        | False | String  | 空间房屋名称                                                 |
| data.list.base.space_location_id                | False | String  | 事件所属空间位置ID                                           |
| data.list.base.space_location_type              | False | Int     | 事件所属空间位置类型，枚举<br>1:项目<br>2:区域<br>3:楼栋<br>4:单元<br>5:<br>房屋<br>6:<br>楼层 |
| data.list.extend                                  | False | Object  | 事件拓展信息                                                 |
| data.list.extend.work_order_id                  | False | String  | 事件工单标识                                                 |
| data.list.extend.intention_router_type          | False | String  | 意图路由类型，在移动推送时会可以提取该参数作为路由类型       |
| data.list.extend.intention_router_url           | False | String  | 意图路由地址，在移动推送时会可以提取该参数作为路由地址       |
| data.list.processed                               | False | Object  | 事件被处理信息                                               |
| data.list.processed.opinion                       | False | String  | 事件被处理意见                                               |
| data.list.processed.operator_type                | False | Int     | 事件被处理类型  <br>1:自动恢复  <br>2:物联平台处理  <br>3:工单系统处理 |
| data.list.processed.operator_id                  | False | String  | 事件被处理人标识，唯一标识，可用于调用接口查询详细信息<br>1.  物联平台建议存储成员标识<br>    <br>2.  外部系统可以为外部系统标识或账号 |
| data.list.processed.operator_account             | False | String  | 事件被处理人账号，账号，用于展示<br>1.  物联平台建议存储成员Account或者Email<br>    <br>2.  外部系统可以为外部系统账号 |
| data.list.processed.operator_name                | False | String  | 事件被处理人名称                                             |
| data.list.processed.way                           | Fase  | Int     | 事件已处理处理方式<br>，枚举<br>\-1:未处理<br>1:设备调试<br>2:真实故障<br>3:误报<br>4:其他<br>5:转工单<br>6:抑制7:自动恢复 |

```text/x-java
{
	"status": "HTTP状态码",
	"code": "业务错误码",
	"msg": "业务错误信息",
	"data": {
		"count": "事件总数",
		"list": [{
			"id": "事件标识",
			"storage_time": "事件存储时间",
			"application": "事件归属应用类型枚举",
			"base": {
				"status": "事件状态",
				"create_time": "事件触发时间",
				"process_time": "事件处理时间",
				"corp_id": "事件归属企业标识",
				"classification_id": "事件归属分类标识",
				"rank_id": "事件等级标识",
				"priority": "事件优先级",
				"name": "事件名称",
				"desc": "事件描述",
				"project_id": "事件归属项目标识",
				"definition_id": "事件归属定义标识",
				"area_id": "事件归属片区标识",
				"source": "事件来源",
				"biz_organization_id": "事件归属业务组织标识",
				"regions": ["所属区域"],
				"full_biz_organization_id": "所属业务组织全标识，A:B:C:D:E:F:G",
				"tag_id": "事件标签标识",
				"space_group_location": "事件所属管理区域(空间分组)位置名称，所有管理区域名称，以分隔符/拼接",
				"space_location": "事件所属空间位置名称，全名称，以分隔符/拼接",
				"product_id": "事件关联产品标识",
				"device_id": "事件关联设备标识",
				"device_name": "事件关联设备名称",
				"device_mac": "事件关联设备mac",
				"trigger_condition": "时间关联触发条件规则",
				"project_name": "事件所属项目名称",
				"address": "事件发生详细位置",
				"rank_name": "事件归属等级名称",
				"processed_way": "事件已处理方式",
				"first_expire": "一级是否超时",
				"second_expire": "二级是否超时",
				"third_expire": "三级是否超时",
				"area_id": "空间区域标识",
				"area_name": "空间区域名称",
				"build_id": "空间楼栋标识",
				"build_name": "空间楼栋名称",
				"unit_id": "空间单元标识",
				"unit_name": "空间单元名称",
				"floor_id": "空间楼层标识",
				"floor_name": "空间楼层名称",
				"house_id": "空间房屋标识"，
				"house_name": "空间房屋名称",
				"space_location_id": "事件所属空间位置ID",
				"space_location_type": "事件所属空间位置类型"
			},
			"extend": {
				"work_order_id": "事件工单标识",
		        "intention_router_type": "意图路由类型，在移动推送时会可以提取该参数作为路由类型",
		        "intention_router_url": "意图路由地址，在移动推送时会可以提取该参数作为路由地址"
			},
			"processed": {
				"opinion": "处理意见",
				"operator_type": "处理人类型",
				"operator_id": "处理人标识",
				"operator_account": "处理人账号",
				"operator_name": "处理人名字",
				"way": "事件已处理方式"
			}
		}]
	}
}
```

**错误码**

| 错误码   | 描述                                    |
| -------- | --------------------------------------- |
| 4001002  | 请求字段不允许为空                      |
| 40010001 | 请求字段<br>验证不通过                  |
| 40029015 | 事件实例状态参数非法                    |
| 40029013 | 请求时间字段参数非法                    |
| 40029012 | 分类标识数量<br>超过<br>限制,512个     |
| 40029009 | 标签标识数量<br>超过<br>限制<br>,512个 |
| 40029010 | 项目标识数量超过限制<br>,512个         |
| 40029011 | 等级标识数量超过限制,512个             |
| 40029016 | 实例标识数量<br>超过限制,512个         |


### 3. 获取设备属性的历史数据

**接口描述**：获取多个设备的历史属性快照数据，支持时间范围过滤和分页 

**请求URL**：/v2/snapshot/device-attribute

**请求方式**：POST


**请求参数**：

| 参数名 | 位置 | 是否必须 | 类型 | 说明 |
| --- | --- | --- | --- | --- |
| device_ids | Body | 是 | List<Int> | 设备ID列表，传入的设备ID必须同属一个产品。 |
| offset | Body | 否 | Int | 请求纪录的偏移量 |
| limit | Body | 否 | Int | 请求数量 |
| date | Body | 否 | Object | 是否通过时间作为查询的过滤条件 |
| date.begin | Body | date节点中必须 | Long | 查询开始时间,时间戳 |
| date.end | Body | date节点中必须 | Long | 查询结束时间,时间戳 |
| rule_id | Body | 否 | String | 快照规则id |
| sort_by_date | Body | 否 | String | desc:降序,asc:升序 |

请求示例

```text/x-java
{
  "device_ids":[1000,1002],
  "offset": "请求纪录的偏移量",
  "limit": "请求数量",
  "date": {
    "begin" : 通过时间查询，开始时间,
    "end" : 通过时间查询，结束时间
  },
  "rule_id":快照规则id"
  "sort_by_date":"desc:降序, asc:升序"
}
```

**返回参数**：

| 参数名 | 是否必须 | 类型 | 说明 |
| --- | --- | --- | --- |
| count | 是 | Int | 获取的条目个数 |
| list | 是 | List | 获取的快照列表 |

**list:**

| 参数名 | 是否必须 | 类型 | 说明 |
| --- | --- | --- | --- |
| _id | 是 | String | 设备快照ID |
| device_id | 是 | Int | 设备ID |
| cm_id | 否 | String | 登录CM服务器ID |
| ip | 否 | String | 登录IP |
| online | 否 | Int | 是否在线 |
| last_online | 否 | Date | 上次登录时间 |
| last_offline | 否 | Date | 上次离线时间 |
| last_update | 否 | Date | 上次属性变化时间 |
| tml | 否 | List<Object> | 物模型定义的属性列表 |
| tml.field_name | 否 | Object | 中英文名称信息 |
| tml.field_name.cn | 否 | String | 中文名称 |
| tml.field_name.en | 否 | String | 英文名称 |
| tml.type | 否 | Object | 类型信息 |
| tml.type.type | 否 | String | 数据类型，bool/uint8/int16/int32/float/string/uint32/double/int32array/date/int64/uint8enum/boolarray |
| tml.type.enums | 否 | Array | 枚举说明 |
| tml.type.enums.enum | 否 | String | 枚举值 |
| tml.type.enums.desc | 否 | String | 枚举值说明 |
| tml.min | 否 | Int | 字段最小值 |
| tml.max | 否 | Int | 字段最大值 |
| tml.symbol | 否 | String | 单位符号 |
| tml.is_display | 否 | Boolean | 是否展示 |
| tml.display_mode | 否 | Int | 展示方式 |
| tml.default_value | 否 | String | 默认值 |
| rule_id | 是 | String | 数据快照规则id |
| 属性索引 | 否 | Object | 属性值 |

返回示例

```text/x-java
{
  "count": 1,
  "tml": [
    {
      "symbol": "",
      "min": 1,
      "max": 100,
      "type": {
        "enums": [
          {
            "enum": 1,
            "desc": "离线"
          },
          {
            "enum": 2,
            "desc": "正常"
          },
          {
            "enum": 3,
            "desc": "故障"
          }
        ],
        "type": "uint8enum"
      },
      "field_name": {
        "en": "status",
        "cn": "告警状态"
      },
      "is_display": true,
      "display_mode": 1,
      "default_value": "xx"
    }
  ],
  "list": [
    {
      "0": "属性值",
      "1": "属性值",
      "id": "设备快照ID",
      "device_id": "设备ID",
      "snapshot_date": "快照时间,例：2015-10-09T08:15:40.843Z",
      "rule_id": "快照规则id "
    }
  ]
}
```

### 4. 批量查询设备最新属性信息

返回格式：标准格式`{"code":200,"status":200,"msg":"OK","data":{...}}`

接口描述：

批量获取多个产品下的设备最新属性信息，支持按 device_id 或 product_id 过滤

请求URL：/v2/device-shadow/device-attribute-query?load_exception=false

请求方式：POST


请求参数：

| 参数名 | 位置 | 是否必须 | 类型  | 说明                                      |
| ------ | ---- | -------- | ----- | ----------------------------------------- |
| offset | Body | 否       | int   | 请求偏移量，默认0                         |
| limit  | Body | 否       | int   | 本次请求拉取大小，默认10，最大10000       |
| query  | Body | 否       | Array | 查询条件：允许product_id、device_id查询 |

请求示例：

```text/x-java
{
  "offset": 0,
  "limit": 10,
  "query": {
    "device_id": {
      "$in": [
        228546143,
        1839137554
      ]
    }
  }
}
```

返回参数：

| 参数名                             | 是否必须 | 类型    | 说明                                                         |
| ---------------------------------- | -------- | ------- | ------------------------------------------------------------ |
| count                              | 是       | Int     | 总数                                                         |
| tmls                               | 是       | Object  | 返回数据关联的TML信息                                        |
| tmls.{product_id}                 | 否       | Array   | 返回某个产品的TML信息                                        |
| tmls.{product_id}.field_name     | 否       | Object  | 中英文名称信息                                               |
| tmls.{product_id}.field_name.cn  | 否       | String  | 中文名称                                                     |
| tmls.{product_id}.field_name.en  | 否       | String  | 英文名称                                                     |
| tmls.{product_id}.type            | 否       | Object  | 类型信息                                                     |
| tmls.{product_id}.type.type       | 否       | String  | 数据类型，bool/uint8/int16/int32/float/string/uint32/double/int32array/date/int64/uint8enum/boolarray |
| tmls.{product_id}.type.enums      | 否       | Array   | 枚举说明                                                     |
| tmls.{product_id}.type.enums.enum | 否       | String  | 枚举值                                                       |
| tmls.{product_id}.type.enums.desc | 否       | String  | 枚举值说明                                                   |
| tmls.{product_id}.min             | 否       | Int     | 字段最小值                                                   |
| tmls.{product_id}.max             | 否       | Int     | 字段最大值                                                   |
| tmls.{product_id}.symbol          | 否       | String  | 单位符号                                                     |
| tmls.{product_id}.is_display     | 否       | Boolean | 是否展示                                                     |
| tmls.{product_id}.display_mode   | 否       | Int     | 展示方式                                                     |
| tmls.{product_id}.default_value  | 否       | String  | 默认值                                                       |
| list                               | 是       | Array   | 返回列表                                                     |
| list.device_id                    | 是       | Int     | 设备ID                                                       |
| list.product_id                   | 是       | String  | 产品ID                                                       |
| list.last_login                   | 否       | String  | 最近上线时间，格式，例："2015-10-09T08:15:40.843Z"           |
| list.last_logout                  | 否       | String  | 最近下线时间，格式，例："2015-10-09T08:15:40.843Z"           |
| list.is_online                    | 是       | Boolean | 是否在线                                                     |
| list.last_update                  | 是       | String  | 最近一次属性更新时间，格式，例："2015-10-09T08:15:40.843Z"   |
| list.conn_prot                    | 是       | Int     | 连接来源                                                     |
| list.online_count                 | 是       | Int     | 上次在线周期的累计在线时长（毫秒）；如果当前设备在线，不包括本次在线的时长 |
| list.attributes                    | 是       | Array   | 属性列表                                                     |
| list.attributes.index              | 是       | Int     | 属性索引                                                     |
| list.attributes.field              | 否       | String  | 属性字段名                                                   |
| list.attributes.value              | 是       | String  | 属性值                                                       |
| list.attributes.time               | 否       | Long    | 上报时间                                                     |
| list.attributes.lable              | 否       | Striing | 属性标签                                                     |
| list.attributes.exception          | 否       | Array   | 异常的规则ID列表，如不异常为空                               |

返回示例：

```text/x-java
{
  "msg": "OK",
  "code": 200,
  "data": {
    "tmls": {
      "16a8b0d3133f000116a8b0d3133fc801": [
        {
          "symbol": "℃",
          "min": 0,
          "display_mode": 0,
          "max": 0,
          "index": 0,
          "default_value": "null",
          "type": {
            "specs": {},
            "type": "float"
          },
          "field_name": {
            "en": "temperature",
            "cn": "温度"
          },
          "is_display": false
        },
        {
          "symbol": "%",
          "min": 0,
          "display_mode": 0,
          "max": 0,
          "index": 1,
          "default_value": "null",
          "type": {
            "specs": {},
            "type": "float"
          },
          "field_name": {
            "en": "humidity",
            "cn": "湿度"
          },
          "is_display": false
        },
        {
          "symbol": "V",
          "min": 1,
          "display_mode": 0,
          "max": 10000,
          "index": 2,
          "default_value": "",
          "type": {
            "specs": {},
            "type": "float"
          },
          "field_name": {
            "en": "battery_voltage",
            "cn": "电池电压"
          },
          "is_display": false
        },
        {
          "symbol": "%",
          "min": 0,
          "display_mode": 0,
          "max": 100,
          "index": 3,
          "default_value": "",
          "type": {
            "specs": {},
            "type": "int32"
          },
          "field_name": {
            "en": "electricity",
            "cn": "剩余电量"
          },
          "is_display": false
        },
        {
          "symbol": "",
          "min": 0,
          "display_mode": 0,
          "max": 100,
          "index": 4,
          "default_value": "",
          "type": {
            "specs": {},
            "type": "float"
          },
          "field_name": {
            "en": "signal strength",
            "cn": "信号强度"
          },
          "is_display": false
        }
      ]
    },
    "count": 1,
    "list": [
      {
        "online_count": 127,
        "conn_prot": 2,
        "device_id": 938245653,
        "last_login": "2026-02-11T15:00:55.903Z",
        "product_id": "16a8b0d3133f000116a8b0d3133fc801",
        "last_update": "2026-02-11T15:06:08.921Z",
        "attributes": [
          {
            "field": "temperature",
            "index": 0,
            "time": 1770793568921,
            "value": 1.0
          },
          {
            "field": "humidity",
            "index": 1,
            "time": 1770793568921,
            "value": 0.0
          },
          {
            "field": "battery_voltage",
            "index": 2,
            "time": 1770793568921,
            "value": 7513.0
          },
          {
            "field": "electricity",
            "index": 3,
            "time": 1770793568921,
            "value": 16
          },
          {
            "field": "signal_strength",
            "index": 4,
            "time": 1770793568921,
            "value": 67.0
          }
        ],
        "is_online": true,
        "last_logout": "2026-02-09T16:54:49.856Z"
      }
    ]
  },
  "status": 200
}
```

错误码

| 错误码   | 错误码描述           |
| -------- | -------------------- |
| 4001002  | 缺少必填请求字段     |
| 40428001 | 请求的设备信息不存在 |
| 4031003  | 无效的AccessToken    |


### 5.设备控制-根据设备ID下发

返回格式：简化格式（直接返回数据对象）

\-根据设备ID调用设备（物模型）服务。

\-设备具有的服务根据物模型功能定义，设置属性使用固定服务名（device_attribute_set_service）调用。

\-指令缓存流程见：设备影子服务设计文档-2.2.1.3指令缓存流程

请求URL：/v2/device-shadow/service_invoke

请求方式：POST

请求参数：

| 参数名    | 位置 | 是否必须 | 类型   | 说明                                                         |
| --------- | ---- | -------- | ------ | ------------------------------------------------------------ |
| thing_id | Body | 是       | String | 设备ID                                                       |
| service   | Body | 是       | String | 产品物模型定义的服务名，如过是设置属性使用固定服务：device_attribute_set_service |
| input     | Body | 是       | Object | 产品物模型定义输入参数，以Key、Value形式输入                 |
| ttl       | Body | 否       | int    | 控制指令缓存时长，单位秒，数值范围：1-864000；表示1秒-10天；不需要缓存不填或者填≤0； |

请求示例

```text/x-java
{
    "thing_id":"10299402",
    "service":"device_attribute_set_service",
    "input":{
        "ColorTemperature":8
    },
    "ttl":-1
}
```

返回参数：

| 参数名      | 是否必须 | 类型   | 说明                                                         |
| ----------- | -------- | ------ | ------------------------------------------------------------ |
| thing_id   | 是       | String | 设备ID                                                       |
| code        | 否       | String | 控制返回的错误码西宁西，当请求参数指定了ttl参数并且ttl>0，不返回该字段。 |
| msg         | 否       | String | 控制返回的错误信息，当请求参数指定了ttl参数并且ttl>0，不返回该字段。 |
| output      | 否       | Object | 控制成功后，设备基于物模型服务定义输出返回参数，当请求参数指定了ttl参数并且ttl>0，不返回该字段。 |
| command_id | 否       | String | 控制指令缓存时长或异步响应时长，当请求参数指定了ttl参数并且ttl>0；表示控制指令ID，用于查询指令下发状态。 |

返回示例：

```text/x-java
{
     "xnms": "..",
    "thing_id": "45281011",
    "code": "200",
    "msg": "ok",
    "output": {},
    "command_id":"0ajskjska092"
}
```

错误码

| 错误码     | 错误码描述                                                   |
| ---------- | ------------------------------------------------------------ |
| 200        | 代表成功下发，并得到设备端的回复                             |
| 202        | 设备在云平台为离线状态，不进行下发；                         |
| 408        | 连接通道断开；可能情况：设备处于休眠状态。                   |
| 503        | 控制出现错误，可能情况：1.平台内部无法访问IoT平台下发2.（常见原因）设备收到数据无响应3.（场景原因）设备没有实现该物模型服务 |
| 其他返回码 | 其他返回码为设备响应的code，具体按设备端的返回code定义       |
| 4001002    | 接口返回的错误，缺少必填请求字段                             |
| 40428001   | 接口返回的错误，请求的设备信息不存在                         |
| 4031003    | 接口返回的错误，无效的AccessToken                            |
| 40428009   | 接口返回的错误，产品没有定义物模型                           |
| 40075001   | 受指令缓存写入QPS限制，写入失败                              |
| 40075002   | 指令缓存写入时发生服务器错误                                 |
| 40075003   | 产品指令缓存功能被禁用                                       |
| 40075004   | 指令缓存TTL超过上限                                          |


### 6.设备概览

返回格式：标准格式`{"code":200,"status":200,"msg":"OK","data":{...}}`

接口描述：

返回设备的总数，在线数，激活数等基础

请求URL：/v3/device-service/devices/overview

请求方式：POST


请求参数：

| 参数名      | 位置 | 是否必须 | 类型   | 说明   |
| ----------- | ---- | -------- | ------ | ------ |
| product_id | Body | 否       | String | 产品ID |
| project_id | Body | 否       | String | 项目ID |

请求示例：

```text/x-java
{
    "project_id":"ab582",
    "product_id":"160593ec01"
}
```

完整返回参数定义：

| 参数名          | 位置 | 是否必须 | 类型  | 说明            |
| --------------- | ---- | -------- | ----- | --------------- |
| total           | \-   | 是       | int   | 设备总数        |
| online          | \-   | 是       | int   | 在线数          |
| activated       | \-   | 是       | int   | 激活数          |
| online_rate    | \-   | 是       | float | 在线率，范围0~1 |
| activated_rate | \-   | 是       | float | 激活率，范围0~1 |

返回示例：

```text/x-java
{
  "msg": "OK",
  "code": 200,
  "data": {
    "total": 120034,
    "online": 87433,
    "activated": 110223,
    "online_rate": 0.72,
    "activated_rate": 0.91
  },
  "status": 200
}
```

### 7. 设备统计趋势

返回格式：标准格式`{"code":200,"status":200,"msg":"OK","data":{"list":[...]}}`

接口描述：

返回最近的设备在线数，设备总数等。

请求URL：/v3/device-service/devices/statistics

请求方式：POST


请求参数：

| 参数名      | 位置 | 是否必须 | 类型   | 说明                                                |
| ----------- | ---- | -------- | ------ | --------------------------------------------------- |
| product_id | Body | 否       | String | 产品ID                                              |
| project_id | Body | 否       | String | 项目ID                                              |
| interval    | Body | 否       | String | 时间粒度，hour/day                                  |
| start       | Body | 否       | String | 开始时间，ISO8601格式，如：2026-02-10T00:00:00.000Z |
| end         | Body | 否       | String | 结束时间，ISO8601格式，如：2026-02-10T00:00:00.000Z |

请求示例：

```text/x-java
{
  "project_id": "ab582",
  "product_id": "160593ec01",
  "interval":"hour",
  "start": "2026-02-10T00:00:00.000Z",
  "end": "2026-02-10T00:00:00.000Z"
}
```

完整返回参数定义：

| 参数名               | 位置 | 是否必须 | 类型                              | 说明 |
| -------------------- | ---- | -------- | --------------------------------- | ---- |
| list                 | 是   | Array    | 返回结果列表                      |      |
| list.time            | 是   | String   | 时间，如：2026-02-10T00:00:00.000 |      |
| list.total           | 是   | int      | 设备总数                          |      |
| list.online          | 是   | int      | 在线数                            |      |
| list.activated       | 是   | int      | 激活数                            |      |
| list.online_rate    | 是   | float    | 在线率，范围0~1                   |      |
| list.activated_rate | 是   | float    | 激活率，范围0~1                   |      |

返回示例：

```text/x-java
{
  "msg": "OK",
  "code": 200,
  "status": 200,
  "data": {
    "list": [
      {
        "time": "2026-02-11T07:00:00.000Z",
        "total": 120034,
        "online": 87433,
        "activated": 110223,
        "online_rate": 0.72,
        "activated_rate": 0.91
      },
      {
        "time": "2026-02-11T08:00:00.000Z",
        "total": 120034,
        "online": 87433,
        "activated": 110223,
        "online_rate": 0.72,
        "activated_rate": 0.91
      }
    ]
  }
}
```

### 8.设备异常概览

返回格式：标准格式`{"code":200,"status":200,"msg":"OK","data":{...}}`

接口描述：

返回当前异常，今日异常数，异常设备数,异常率

请求URL：/v3/alert/overview

请求方式：POST


请求参数：

| 参数名      | 位置 | 是否必须 | 类型   | 说明   |
| ----------- | ---- | -------- | ------ | ------ |
| product_id | Body | 否       | String | 产品ID |
| project_id | Body | 否       | String | 项目ID |

请求示例：

```text/x-java
{
    "project_id":"ab582",
    "product_id":"160593ec01"
}
```

完整返回参数定义：

| 参数名              | 位置 | 是否必须 | 类型                | 说明 |
| ------------------- | ---- | -------- | ------------------- | ---- |
| added_alert_num   | 是   | int      | 新增异常数          |      |
| history_alert_num | 是   | int      | 异常总数            |      |
| device_alert_num  | 是   | int      | 设备异常数          |      |
| device_alert_rate | 是   | float    | 设备异常率，范围0~1 |      |

返回示例：

```text/x-java
{
  "msg": "OK",
  "code": 200,
  "data": {
    "added_alert_num": 231,
    "history_alert_num": 8433,
    "device_alert_num": 182,
    "device_alert_rate": 0.0.1
  },
  "status": 200
}
```

### 9.设备异常统计

返回格式：标准格式`{"code":200,"status":200,"msg":"OK","data":{"list":[...]}}`

接口描述：

返回最近24小时当前异常，今日异常数，异常设备数,异常率等。

请求URL：/v3/alert/statistics

请求方式：POST


请求参数：

| 参数名      | 位置 | 是否必须 | 类型   | 说明                                                |
| ----------- | ---- | -------- | ------ | --------------------------------------------------- |
| product_id | Body | 否       | String | 产品ID                                              |
| project_id | Body | 否       | String | 项目ID                                              |
| interval    | Body | 否       | String | 时间粒度，hour/day                                  |
| start       | Body | 否       | String | 开始时间，ISO8601格式，如：2026-02-10T00:00:00.000Z |
| end         | Body | 否       | String | 结束时间，ISO8601格式，如：2026-02-10T00:00:00.000Z |

请求示例：

```text/x-java
{
  "project_id": "ab582",
  "product_id": "160593ec01",
  "start": "2026-02-10T00:00:00.000Z",
  "end": "2026-02-10T00:00:00.000Z"
}
```

完整返回参数定义：

| 参数名                   | 位置 | 是否必须 | 类型                              | 说明 |
| ------------------------ | ---- | -------- | --------------------------------- | ---- |
| list                     | 是   | Array    | 返回结果列表                      |      |
| list.time                | 是   | String   | 时间，如：2026-02-10T00:00:00.000 |      |
| list.added_alert_num   | 是   | int      | 新增异常数                        |      |
| list.history_alert_num | 是   | int      | 异常总数                          |      |
| list.device_alert_num  | 是   | int      | 设备异常数                        |      |
| list.device_alert_rate | 是   | float    | 设备异常率，范围0~1               |      |

返回示例：

```text/x-java
{
  "msg": "OK",
  "code": 200,
  "data": {
    "list": [
      {
        "time": "2026-02-11T07:00:00.000",
        "added_alert_num": 231,
        "history_alert_num": 8433,
        "device_alert_num": 182,
        "device_alert_rate": 0.01
      },
      {
        "time": "2026-02-11T08:00:00.000",
        "added_alert_num": 231,
        "history_alert_num": 8433,
        "device_alert_num": 182,
        "device_alert_rate": 0.01
      }
    ]
  },
  "status": 200
}
```



