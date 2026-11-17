# 群作业接口参考

## 页面入口

| 用途 | URL |
|------|-----|
| 列表页 | `https://qun.qq.com/homework/features/index.html?gid=<群号>` |
| 详情页 | `//qun.qq.com/homework/features/detail.html?_wv=1027&_bid=2146#group_id=<gid>&hw_id=<id>&puin=0&need_feedback=0` |

⚠️ 旧路径 `https://qun.qq.com/homework/p/features#?gid=` 已 **404**，网上流传的教程多用旧地址。

## 接口

Base：`//qun.qq.com/cgi-bin/homework/`

| 名称 | 端点 | 方法 |
|------|------|------|
| 作业列表 | `hw/get_hw_list.fcg` | POST |
| 作业详情（**含图片**） | `hw/get_hw_detail.fcg` | POST |
| 是否作业群 | `//qun.qq.com/cgi-bin/hw/util/checkishwgroup?gc=&bkn=` | GET |

### 列表接口参数

```
cmd=21&group_id=<gid>&num=1&page_size=100&bkn=<bkn>
```

- `cmd=21` = HW_ALL（全部作业）；`cmd` 另有 HW_MINE
- 一次最多稳定取 100 条；`end_flag=0` 表示后面可能还有

返回结构：

```json
{ "retcode": 0, "msg": "",
  "data": { "end_flag": 0, "identity": 2, "hw_role": 334,
            "server_time": 1788026848,
            "homework": [ { "hw_id": 2600000000000001,
                             "hw_title": "语文作业",
                             "ts_create": 1781597767,
                             "course_name": "语文",
                             "content": { "c": [ {"type":"str","text":"..."} ] } } ] } }
```

### 详情接口参数

```
hw_id=<id>&group_id=<gid>&bkn=<bkn>&puin=0&need_feedback=0
```

返回结构（**图片在这里**）：

```json
{ "retcode": 0, "msg": "success",
  "data": { "hw_id": 2600000000000000, "hw_title": "5月14日语文作业",
             "puin": 1234567890, "pnick_name": "语文-某某老师",
             "course_name": "语文", "ts_create": 1778725507,
             "content": { "c": [ { "type": "img", "text": "",
                                    "url": "https://qunhwfile-30054.sz.gfp.tencent-cloud.com/...jpg?md5=...",
                                    "height": 6144, "width": 8192 } ] },
             "feedback": { "uin": 123456789, "nick_name": "<孩子昵称>", "status": 1 } } }

> 以上为脱敏示例，数字与姓名均非真实值。
```

## ⚠️ 列表接口会剥掉图片

`get_hw_list.fcg` 的 `content.c[]` **只有 `type:"str"`**。
图片作业在列表里仅显示占位文字「**【图片】**」，`url` 字段为空或缺失。

**→ 要拿图片必须逐条调 `get_hw_detail.fcg`。**

## content.c[] 内容块

| type | 含义 | 关键字段 |
|------|------|---------|
| `str` | 文字 | `text` |
| `img` | 图片 | `url`, `width`, `height` |
| （其他） | 附件/语音等 | `url`, `name`, `size`, `time` |

图片 URL 形如：
`https://qunhwfile-30054.sz.gfp.tencent-cloud.com/<YYYYMMDD>/<hash>.jpg?md5=<MD5>`
下载需带 `Referer: https://qun.qq.com/`。

## bkn 的获取

`bkn` 由 `skey` cookie 计算（hash 5381 算法），但 **skey 是 HttpOnly，JS 读不到**。

解法：从页面已发出的请求里捞 ——

```javascript
performance.getEntriesByType('resource')
  .map(x => x.name)
  .filter(n => n.indexOf('cgi-bin') > -1)
```

其中 GET 类请求（如 `get_banner`、`checkishwgroup`）的 URL 里就带着真实 `bkn=xxxxx`。
`qq_hw.py bkn` 子命令已封装此逻辑并缓存到 `qq_hw.json`。

> bkn 会随登录态变化；接口返回非 0 retcode 时，重新执行 `bkn` 子命令。

## 前端常量（供逆向参考）

从 `https://qq-qun-web.cdn-go.cn/homework-mobile-features/v1.7.2/js/index-bc7367.js` 可得：

```javascript
GET_HW_LIST : "//qun.qq.com/cgi-bin/homework/" + "hw/get_hw_list.fcg"
GET_GROUP_CARD : ".../group/get_group_card.fcg"
IS_HW_GP : "//qun.qq.com/cgi-bin/hw/util/checkishwgroup"
DEL_HW : ".../hw/delete_hw.fcg"
```

页面依赖 `open.mobile.qq.com/sdk/qqapi.js` 提供的 `window.mqq` JS Bridge 做鉴权。
