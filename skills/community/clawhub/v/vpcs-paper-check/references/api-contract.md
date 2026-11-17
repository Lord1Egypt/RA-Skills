# Agent API 契约

脚本：`scripts/vpcs_client.py`。

脚本只保留两个命令，均只依赖 Python 标准库：

1. `submit`：建单、上传文件、完成绑定，返回 `order_no` 和浏览器链接；
2. `status`：按 `order_no` 查询订单，返回状态和下一步浏览器链接。

支付、验证码、报告阅读和报告验真都交给浏览器完成。脚本不会自动支付，也不会代替用户填写支付密码、卡号或验证码。

## 1. 提交论文并返回订单号

```bash
python3 scripts/vpcs_client.py submit \
  --product-type dxs \
  --title "论文题目" \
  --author "作者姓名" \
  --file ./论文.docx
```

`--product-type` 可以填写页面产品编码，也可以填写常见完整名称，例如：

- `dxs` 或 `维普查重大学生版`
- `yjs` 或 `维普查重研究生版`
- `bjb`、`zc`、`zy`、`ky`
- `aigc` 或 `维普AIGC检测`

必要参数只有 `--product-type`、`--title`、`--author` 和 `--file`。职称版页面要求发表日期时，可以增加 `--publish-date`。

脚本内部自动完成：

```text
create-draft -> upload/presign -> OSS PUT -> upload/complete -> GET order
```

上传完成只表示文件已经绑定到订单，不代表已经支付或已经开始检测。提交成功后，把输出中的 `browser_url` 交给用户：

- 未支付：打开支付页；
- 已支付、解析中或检测中：打开进度页；
- 已完成：打开报告页。

示例输出：

```json
{
  "action": "submit",
  "order_no": "2104087082852179968",
  "status": "WAIT_PAYMENT",
  "pay_status": "UNPAID",
  "browser_url": "https://vpcs.cqccjy.cn/pwp?orderNo=2104087082852179968&stage=payment",
  "browser_urls": {
    "payment": "https://vpcs.cqccjy.cn/pwp?orderNo=2104087082852179968&stage=payment",
    "progress": "https://vpcs.cqccjy.cn/pwp?orderNo=2104087082852179968&stage=progress",
    "reports": "https://vpcs.cqccjy.cn/reports?orderNo=2104087082852179968",
    "verify": "https://vpcs.cqccjy.cn/pwp/verify"
  }
}
```

脚本只使用 `domains/cqccjy.json` 中的固定页面地址。报告下载直链只有在服务端订单响应明确返回 HTTPS 地址时才会附加，不能根据订单号猜测。

## 2. 查询订单状态并返回链接

```bash
python3 scripts/vpcs_client.py status \
  --order-no 2104087082852179968
```

这是幂等查询。支付回调延迟、解析中、检测中或报告尚未生成时，都继续查询同一个订单号，不重新建单。

返回字段重点如下：

| 字段 | 用途 |
|---|---|
| `order_no` | 后续查询和浏览器页面使用的内部订单号 |
| `status` / `status_label` | 当前订单状态 |
| `pay_status` | 支付状态 |
| `word_count` / `billing_word_count` | 服务端解析后的字符和计费字段（若接口返回） |
| `need_supplement` / `can_supplement_pay` | 是否需要补差、页面是否允许补差 |
| `fail_reason` | 服务端给出的失败原因 |
| `browser_url` | 当前最适合交给用户打开的 URL |
| `browser_urls.payment` | 支付页 |
| `browser_urls.progress` | 订单进度页 |
| `browser_urls.reports` | 报告查询/下载页 |
| `browser_urls.verify` | 官方报告验真页 |
| `report_download_url` | 服务端明确返回的真实下载地址；没有时为 `null` |
| `next_action` | 面向用户的下一步说明 |

`browser_url` 的选择规则：

- `REPORT_READY`、`COMPLETED` 或 `canDownloadReport=true`：报告页；
- 已支付、解析中、检测中或 `canSubmitDetect=true`：进度页；
- 其他情况：支付页。

## 3. 参数检查和无网络预演

两条命令都支持：

```bash
python3 scripts/vpcs_client.py --dry-run submit \
  --product-type dxs \
  --title "论文题目" \
  --author "作者" \
  --file ./论文.docx
```

`--dry-run` 只检查文件、格式、大小、题目、作者和产品参数，不会创建订单、不上传文件，也不会生成虚假的订单号。正式提交前建议先使用一次。

## 4. 失败时怎么处理

| 情况 | 处理 |
|---|---|
| 建单请求超时且没有订单号 | 先确认服务端没有生成订单，再决定是否重试 |
| 已经拿到订单号但上传/绑定失败 | 保留原订单号，优先用 `status` 查询 |
| 打开支付页但未支付 | 在同一订单页刷新或更换支付方式 |
| 支付状态未知 | 只查询原订单，不重复付款 |
| 检测中 | 继续查询原订单，不重复点击或建单 |
| 报告完成 | 打开 `browser_urls.reports` 下载，再用报告编码去 `browser_urls.verify` 验真 |

退出码为 `0` 表示成功，`2` 表示输入或网络错误。错误输出不包含临时上传凭证、签名、文件内容或异常堆栈。
