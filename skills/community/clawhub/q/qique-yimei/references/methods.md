# QiQue SDK Methods

Source: QiQue API method catalog (text protocol extraction)

## Read Operations

| SDK method                    | Remote method                 | HTTP | Key params                                                           |
| ----------------------------- | ----------------------------- | ---- | -------------------------------------------------------------------- |
| `getSignPackage`              | `getsignpackage`              | GET  | `wxappId`, `url`                                                     |
| `getWalletChangeList`         | `getwalletchangelist`         | POST | `telnum`, `type?`, `date00?`, `date01?`, `page?`                     |
| `getCusInfoByCusId`           | `getcusinfobycusid`           | GET  | `cusId`                                                              |
| `getCusInfoByTelnum`          | `getcusinfobycusid`           | GET  | `telnum`                                                             |
| `getAllChatHistoryByTime`     | `getallchathistorybytime`     | GET  | `lastChatTime?`, `page?`                                             |
| `getChatHistoryByOpenId`      | `getchathistorybyopenid`      | GET  | `wxac`, `openId`, `lastChatTime?`, `page?`                           |
| `getOfflinePay`               | `getofflinepay`               | GET  | `lastPayId?`, `page?`                                                |
| `getOfflineExcute`            | `getofflineexcute`            | GET  | `lastExcuteId?`, `page?`                                             |
| `getOfflineProducts`          | `getofflineproducts`          | GET  | `cusId`, `type?`, `page?`                                            |
| `getOnlineOrders`             | `getonlineorders`             | GET  | `lastGetPayTime?`, `lastRefundTime?`                                 |
| `getGoodsList`                | `getgoodslist`                | GET  | `page?`, `goodType?`                                                 |
| `getOrderDetail`              | `getorderdetail`              | GET  | `billId?`, `useCode?`                                                |
| `getAppointmentList`          | `getappointmentlist`          | GET  | `lastCreateTime?`, `lastCompleteTime?`, `lastAppointTime?`, `cusId?` |
| `getCustomersList`            | `getcustomerslist`            | GET  | `lastId?`, `page?`                                                   |
| `getPayTypeList`              | `getpaytypelist`              | GET  | `page?`                                                              |
| `getChannelList`              | `getchannellist`              | GET  | `page?`                                                              |
| `getEmployeeList`             | `getemployeelist`             | GET  | `page?`                                                              |
| `getCustomerInfo`             | `getcustomerinfo`             | GET  | `openId`, `wxappId`                                                  |
| `getSyncHealthCommissionData` | `getsynchealthcommissiondata` | GET  | none                                                                 |

## Write Operations

| SDK method             | Remote method       | HTTP | Key params                                                                                                                                                |
| ---------------------- | ------------------- | ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `addCustomer`          | `addcustomer`       | POST | `name`, `telnum`, `erpId?`, `sex?`, `birthday?`, `channelName?`, `channelUserName?`, `preConsultName?`, `ownerName?`, `description?`                      |
| `changeWallet`         | `changewallet`      | POST | `telnum`, `type?`, `action?`, `changeNum?`, `remark?`, `sendNotify?`                                                                                      |
| `offlineBuy`           | `offlinebuy`        | GET  | `telnum`, `pName`, `num`, `money?`, `buyTime?`                                                                                                            |
| `offlineExcute`        | `offlineexcute`     | GET  | `telnum`, `pName`, `num`, `excuteTime?`                                                                                                                   |
| `delivery`             | `delivery`          | GET  | `billId?`, `useCode?`, `detailIds?`, `deliveryCompany?`, `deliveryNumber?`, `deliveryComment?`, `type?`                                                   |
| `addOneAppointment`    | `addoneappointment` | GET  | `appointmentTime`, `pId`, plus one of `cusId` / `telnum`; optional `teamId`, `type`, `content`, `comment`, `appointmentTime1`, `doctorId`, `technicianId` |
| `changeOneAppointment` | `changeappointment` | GET  | `id`, optional `teamId`, `type`, `content`, `comment`, `appointmentTime`, `appointmentTime1`, `pId`, `doctorId`, `technicianId`                           |
| `cancelOneAppointment` | `cancelappointment` | GET  | `id`, `comment?`                                                                                                                                          |
| `sendMsgTotel`         | `sendmsgtotel`      | GET  | `tel`, `type?`, `theParams?`                                                                                                                              |
| `sendCardOrCoupons`    | `sendcardorcoupons` | GET  | `cusId`, `cardOrCouponsId`                                                                                                                                |

## Notes

1. `getCusInfoByTelnum` and `getCusInfoByCusId` both map to `getcusinfobycusid`; they differ only by parameter key.
2. Core credentials required by all calls:
   - `appId`
   - `appSecret`
   - `distributionAppId`
   - `distributionAppSecret`

## Request Protocol (From Original SDK)

### Base URL and Method Path

1. Base URL (as found in original SDK snapshot):
   - `https://pre-e.qique.cn/index.php?r=data/api/`
2. Final request URL:
   - `<base_url><remote_method>`
   - Example: `https://pre-e.qique.cn/index.php?r=data/api/getcustomerslist`
3. HTTP method:
   - Use the table above (`GET`/`POST`) per method.

### Common Parameters (Always Included)

The SDK injects these public keys before sending business parameters:

- `t`: appId
- `dis`: distributionAppId
- `timeStamp`: current time (`Y-m-d H:i:s`)
- `format`: `json`
- `signMethod`: `md5`
- `v`: `3.0`
- `sign`: request signature

### Signature Rule (Critical)

1. Merge common params + business params.
2. Sort all params by key in ascending order (`ksort` behavior).
3. Concatenate as plain text without separators:
   - `k1v1k2v2k3v3...`
4. Build source text:
   - `appSecret + distributionAppSecret + concatenated_text + appSecret`
5. Signature:
   - `sign = md5(source_text)`

Formula:

```text
sign = md5(appSecret + distributionAppSecret + concat(sorted(k+v)) + appSecret)
```

### Response Parsing

1. Response format is JSON.
2. If JSON decode fails, treat as invalid response.
3. Business success/failure is usually indicated by `errNum`:
   - `errNum = 0`: success
   - `errNum != 0`: business failure (check `errMsg`)
