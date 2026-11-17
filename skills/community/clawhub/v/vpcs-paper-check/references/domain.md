# 维普域名与运行时配置

## 固定站点

当前 Skill 只面向配置中 `owner_user_id=2` 的 CQCCJY VPCS 公共用户端：

| 用途 | 地址 |
|---|---|
| 官方首页 | `https://vpcs.cqccjy.cn/` |
| 查重入口 | `https://vpcs.cqccjy.cn/pwp` |
| 支付页 | `https://vpcs.cqccjy.cn/pwp?orderNo={orderNo}&stage=payment` |
| 进度页 | `https://vpcs.cqccjy.cn/pwp?orderNo={orderNo}&stage=progress` |
| 我的报告 | `https://vpcs.cqccjy.cn/reports?orderNo={orderNo}` |
| 报告验真 | `https://vpcs.cqccjy.cn/pwp/verify` |
| FAQ | `https://vpcs.cqccjy.cn/faq/vip` |
| AIGC 工作区 | `https://vpcs.cqccjy.cn/aigc-check` 或 `https://vpcs.cqccjy.cn/paper-aigc` |
| AIGC 报告 | `https://vpcs.cqccjy.cn/aigc-check/check` 或 `https://vpcs.cqccjy.cn/paper-aigc/check` |
| 智评提升 | `https://vpcs.cqccjy.cn/review-upgrade` |
| 智评提升结果 | `https://vpcs.cqccjy.cn/review-upgrade/check` |
| 报告兼容入口 | `https://vpcs.cqccjy.cn/wp/check`、`https://vpcs.cqccjy.cn/wp-vpcs/check` |
| 验真兼容入口 | `https://vpcs.cqccjy.cn/wp/verify`、`https://vpcs.cqccjy.cn/wp-vpcs/verify` |

域名、页面和接口都由 `domains/cqccjy.json` 管理。不要接受用户传入的任意 URL，也不要把 `vpcs.fanyu.com`、搜索结果或示例截图中的其他地址替换成当前入口。

## 公共 API 合约

脚本调用基地址下的以下接口。响应通常是 `{code, msg, data}`；客户端会解包 `data`，非成功 `code` 直接报错。

| 阶段 | 方法 | 路径 | 主要请求字段 | 关键响应字段 |
|---|---|---|---|---|
| 实时配置 | GET | `/api/paper/check/public/pwp/config` | 无 | `pricingItems`, `paymentChannels`, `maxWordCount`, `reportRetentionDays` |
| 实时价格 | GET | `/api/paper/check/public/pwp/pricing` | 无 | 产品编码、名称、计价模式和展示价格 |
| 创建草稿 | POST | `/api/paper/check/public/pwp/order/create-draft` | `productType`, `detectMode=AUTO`, `title`, `author`, `publishDate?`, `visitorKey` | `orderNo`, `productType`, `status`, `canUpload` |
| 获取上传票据 | POST | `/api/paper/check/public/upload/presign` | `orderNo`, `fileName` | 签名 URL 或 OSS STS 字段、`objectKey` |
| 完成上传 | POST | `/api/paper/check/public/upload/complete` | 订单、产品、题目、作者、`objectKey`, 文件元数据 | 解析任务/订单摘要 |
| 订单查询 | GET | `/api/paper/check/public/order/{orderNo}` | 无 | `status`, `payStatus`, `wordCount`, `billingWordCount`, `payAmount`, `canSubmitDetect`, `canDownloadReport` |
| 提交检测 | POST | `/api/paper/check/public/order/{orderNo}/submit-detect` | 空 JSON | 供应商提交结果；随后重新 GET 订单 |
| 报告地址 | GET | `/api/paper/check/public/order/{orderNo}/report-download-url` | 无 | 服务端生成的真实下载 URL |

当前前端还公开使用以下查重订单能力；标准脚本只默认调用建单、上传、完成、订单查询和报告地址。配置、支付、验真和页面上的提交检测动作由浏览器或文档流程负责，以下接口只用于排错和维护，不应让 agent 自己拼装：

| 能力 | 方法 | 路径 | 用途 |
|---|---|---|---|
| 订单关键字查询 | GET | `/api/paper/check/public/order/query?keyword=...` | 页面按订单号/关键字查询 |
| 重新解析 | POST | `/api/paper/check/public/order/{orderNo}/reparse` | 页面异常时重解析，需用户确认 |
| 微信/支付宝支付 | POST | `/api/paper/check/public/order/{orderNo}/pay`、`/pay/mobile`、`/pay/qr` | 创建支付单或二维码；不由 Skill 自动调用 |
| 支付二维码状态 | GET | `/api/paper/check/public/order/{orderNo}/pay/qr` | 页面轮询支付状态 |
| 检测卡结算 | POST | `/settlement/card` 或 `/settlement/detection-card` | 页面提交检测卡/卡订单凭证 |
| 报告生成任务 | POST/GET | `/report-action`、`/report-action/status` | 报告动作任务和状态 |
| 智评选项 | GET | `/api/paper/check/public/zzzp/schools`、`/zzzp/class-codes` | 智评页面的学校/班级选项 |

### AIGC 与智评独立接口

这些接口与普通 `/pwp` 查重订单不是同一订单模型，不能交叉传入 `orderNo`：

| 产品 | 配置/建单 | 订单查询 | 支付/报告 |
|---|---|---|---|
| AIGC | `/api/paper/aigc/public/config`、`/order/prepare-submit`、`/order/submit` | `/api/paper/aigc/public/order/{orderNo}`、`/order/query` | `/order/pay/draft`、`/{orderNo}/pay/qr`、`/{orderNo}/pay/mobile` |
| 智评提升 | `/api/paper/review-upgrade/public/config`、`/upload/presign`、`/order/create` | `/order/{orderNo}`、`/order/query` | `/{orderNo}/pay/qr`、`/{orderNo}/pay/mobile`、`/{orderNo}/report-download-url` |

## 产品编码与完整商品名

实时 `pricingItems` 当前返回 15 个独立 SKU。短代码用于 API，完整商品名用于回答和产品选择：

| 编码 | Skill 标准商品名 | 接口 `productLabel` 快照 | 当前价格快照 |
|---|---|---|---|
| `dxs` | 维普查重大学生版 | 大学生版 | ¥2.70/1000字符 |
| `yjs` | 维普查重研究生版 | 研究生版 | ¥2.70/1000字符 |
| `bjb` | 维普查重编辑部版 | 编辑部版 | ¥2.70/1000字符 |
| `zc` | 维普查重职称版 | 职称版 | ¥27.00/10000字符 |
| `zy` | 维普查重作业版 | 作业版 | ¥2.70/1000字符 |
| `ky` | 维普查重科研版 | 科研版 | ¥2.70/1000字符 |
| `aigc` | 维普AIGC检测 | AIGC | ¥17.99/篇 |
| `format_dxs` | 维普格式检测·大学生版 | 格式检测大学生版 | ¥30.00/篇 |
| `zzzp_dxs` | 维普斟知智评·大学生版 | 斟知智评大学生版 | ¥32.00/篇 |
| `zzzp_yjs` | 维普斟知智评·研究生版 | 斟知智评研究生版 | ¥75.00/篇 |
| `zzzp_qkb` | 维普斟知智评·期刊版 | 斟知智评期刊版 | ¥32.00/篇 |
| `special_ref_quality` | 维普参考文献质量检测 | 参考文献质量检测 | ¥18.00/篇 |
| `special_proofread` | 维普斟校对 | 斟校对 | ¥2.00/篇 |
| `special_data_image_pro` | 维普数据与图像可信度检测·专业版 | 数据与图像可信度检测专业版 | ¥180.00/篇 |
| `special_data_image_standard` | 维普数据与图像可信度检测·标准版 | 数据与图像可信度检测标准版 | ¥120.00/篇 |

价格快照抓取于 2026-09-27，已经写入 Skill 的本地目录；一般选型直接使用快照。只有用户明确要求当前值时，才查看 `/pwp` 页面或直接读取配置接口。完整别名、文件限制和选型说明见 [product-catalog.md](product-catalog.md)。

## 支付渠道

当前配置可能返回 `DETECTION_CARD`、`WECHAT`、`ALIPAY`，并带有 `enabled`、`label`、移动端模式等字段。Skill 只把这些作为页面导航信息；实际支付由用户在支付页确认。订单的 `payStatus` 和 `paymentFlowState` 是判断是否已支付的唯一依据，不能用“打开过支付页”推断支付成功。

## 订单状态交接

页面和接口可能出现以下状态：

```text
PENDING_UPLOAD -> COUNTING/PARSING -> WAIT_SUBMIT -> DETECTING -> REPORT_READY
                                      \-> FAILED
```

不同部署可能使用其他状态名，因此优先看 `statusLabel`、`can*` 能力字段和 `failReason`。当接口超时，保留原订单号并查询，不创建第二笔订单。
