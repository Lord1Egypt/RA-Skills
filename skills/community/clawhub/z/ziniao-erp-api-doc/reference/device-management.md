# 设备管理接口

> 本文件是 ziniao-erp-api-doc 的 Level 2 参考文档。
> 仅在需要查阅设备套餐、购买、续费、绑定、解绑、查询、自有设备管理接口时加载。

所有接口方法均为 POST，Content-Type 为 application/json。

---

## ERP-套餐列表查询

- **路径**：`/superbrowser/rest/v1/erp/package/new`　**权限点**：ERP-设备套餐列表查询权限

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |

**响应 data**：数组，每项含 regionCloudId(套餐ID)、ctype(0站群/1云平台/2自有/3本地)、networkType、areaId、areaName、city、priceOriginal、deviceConfigName、deviceType(1标准/2节能/3高配)、deviceOs、deviceSupportRemoteLogin、deviceCpuSize、deviceMemorySize、deviceBandWidth、deviceDiskSize、platformName (均 string)。

---

## ERP-购买设备

- **路径**：`/superbrowser/rest/v1/erp/purchase`　**权限点**：ERP-设备购买与续费权限

> 需要紫鸟账号上有余额。

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | string |
| purchase | 购买信息对象 | 是 | object |
| purchase.packageId | 套餐id | 是 | number |
| purchase.periodId | 时长id（1:1月/2:3月/3:6月/4:12月） | 是 | number |
| purchase.num | 数量（单次最多5个） | 是 | number |
| storeIds | 要绑定的账号id（未绑设备的） | 否 | number[] |

**响应 data**：含 order_id(string)、create_time(string)、proxyIdList(number[] 设备ID列表)。

---

## ERP-续费设备

- **路径**：`/superbrowser/rest/v1/erp/renew`　**权限点**：ERP-设备购买与续费权限

> 仅支持紫鸟 IP 续费；自有设备请通过开启自动续费。

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | string |
| renew | 续费信息对象 | 是 | object |
| renew.periodId | 时长id | 是 | string |
| renew.ipIds | proxy_id 数组 | 是 | integer[] |

**响应 data**：含 id(设备id)、ip(设备ip)、expire(过期时间)。另有 orderId、createTime。

---

## ERP-开关自动续费

- **路径**：`/superbrowser/rest/v1/erp/ip/renewal`　**权限点**：ERP-开关自动续费

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| ids | proxy_id 数组 | 是 | number[] |
| isOpen | 0关闭 1开启 | 是 | number |

**响应**：ret / msg / status

---

## ERP-设备查询

- **路径**：`/superbrowser/rest/v1/erp/ip/page`　**权限点**：ERP-设备查询

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| ipAddr | 设备地址 | 否 | string |
| page | 页码 | 否 | string |
| limit | 每页条数 | 否 | string |

**响应 data**：数组，每项含 id(number)、ip、proxyName、proxyType(0站群/1云平台/2自有/3vps/4虚拟机/5本地)、port、ptype(0http/1https/2socks5)、expiry、isRenewal(0关/1开)、createtime、delflag(0正常/2回收站) (均 string)。另有 count。

---

## ERP-绑定设备

- **路径**：`/superbrowser/rest/v1/erp/ip/bind`　**权限点**：ERP-设备绑定权限

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| proxyId | 设备id | 是 | number |
| storeIdList | 账号id列表 | 是 | number[] |
| defyWarning | 是否无视风险：1是 0否（默认1） | 否 | number |

**响应**：ret / status / msg / riskMsgList(string[])

---

## ERP-解绑设备

- **路径**：`/superbrowser/rest/v1/erp/ip/unbind`　**权限点**：ERP-解绑设备

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| storeId | 账号ID | 是 | number |

**响应**：ret / msg / status

---

## ERP-查询已购设备价格接口

- **路径**：`/superbrowser/rest/v1/erp/proxy/purchased_package_info`　**权限点**：ERP-查询已购设备价格接口

> 仅支持查询云平台设备。

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司ID | 是 | number |
| proxyId | 设备ID | 是 | number |

**响应 data**：含 proxyId(number)、regionCloudId(number 套餐ID)、price(number 续费价格)。

---

## ERP-设备历史绑定记录

- **路径**：`/superbrowser/rest/v1/erp/ip/historybind`　**权限点**：ERP-设备查询

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司id | 是 | number |
| proxyId | 设备id | 是 | number |

**响应 data**：对象含 list 数组，每项含 storeId、storeName、proxyName、unBindTime、unbindUserId、unbindUsername、cloudType (均 string)。另有 count。

---

## ERP-添加自有设备（新）

- **路径**：`/superbrowser/rest/v1/erp/ip/self/add/new`　**权限点**：ERP-添加自有设备（新）

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司ID | 是 | string |
| defyWarning | 1无视风险 0风险提示 | 是 | number |
| base | 基础信息对象 | 是 | object |
| base.deviceName | 设备名称 | 是 | string |
| base.isDynamic | 是否动态网络（false静态/true动态） | 是 | boolean |
| proxy | 代理信息对象 | 是 | object |
| proxy.type | 0http/1https/2sock5/3ssh/4ssl | 是 | string |
| proxy.addr | 代理地址 | 是 | string |
| proxy.port | 代理端口 | 是 | string |
| proxy.username | 用户名 | 否 | string |
| proxy.passwd | 密码 | 否 | string |
| proxy.isSetAccount | 是否设密码 0否 1是 | 是 | number |

**响应 data**：含 id(number 设备ID)。

---

## ERP-修改自有设备信息（新）

- **路径**：`/superbrowser/rest/v1/erp/ip/self/edit/new`　**权限点**：ERP-修改自有设备信息（新）

| 参数 | 说明 | 必须 | 类型 |
|------|------|------|------|
| companyId | 公司ID | 是 | string |
| defyWarning | 1无视风险 0风险提示 | 是 | number |
| proxyId | 设备ID | 是 | string |
| base | 基础信息对象 | 是 | object |
| base.deviceName | 设备名称（不传不更新） | 否 | string |
| base.isDynamic | 是否动态网络 | 是 | boolean |
| proxy | 代理信息对象（字段同添加接口） | 是 | object |

**响应**：ret / status / msg
