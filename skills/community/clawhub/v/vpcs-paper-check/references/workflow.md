# 页面操作与用户交接

## 页面全链路

1. 打开 <https://vpcs.cqccjy.cn/pwp>，确认浏览器地址栏域名。
2. 在“查重检测”中选择学校/期刊要求的版本。
3. 填写题目（最多 128 个字符）和作者（2-20 个字符）。职称版若页面要求发布日期，按页面填写。
4. 选择最终排版文件上传。不要上传摘要、节选或未确认的临时版本。
5. 等待页面解析，核对网站显示的字符数、计费件数、产品和金额。
6. 在支付页选择当前可用支付渠道并由用户完成支付。
7. 回到订单进度页，确认支付状态后提交检测；等待 `DETECTING` 变为报告完成。
8. 进入“我的报告”查看/下载；需要确认来源时，再去 `/pwp/verify` 验真。

## 字符与计费检查

- Word/WPS 统计只能做预估，必须记录“字符数（不计空格）”与统计选项。
- 维普页面的解析结果才是计费依据。中文、英文、空格、脚注、尾注和文本框的处理可能造成差异。
- 普通查重可用 `ceil(预估字符数 / 1000)` 估算档位，职称版可用 `ceil(预估字符数 / 10000)` 估算档位；这只是解释档位变化的公式，不是最终金额计算器。
- 上传后重点看 `wordCount`、`billingWordCount`、购买量/件数、`payAmount`；若 `needSupplement=true`，再看 `shortWordCount` 和 `supplementAmount`，回到原订单补差，不要重新建单。
- 不把“字数”“中文字符”“英文单词数”直接当成维普计费字符数。
- 不通过隐藏字符、图片化正文、拆分文件或改扩展名规避检测或计费。

完整的字段含义和示例见 [character-count.md](character-count.md)。

## 支付交接

脚本返回 `browser_urls.payment` 后，用户应在浏览器完成支付。支付方式、价格、是否需要补差和支付二维码都以页面实时状态为准。Skill 不收集银行卡、支付密码、验证码或检测卡密。

如果支付页打开但订单仍是未支付：让用户在同一页面刷新或重新选择渠道，不创建新订单。支付接口/页面异常时保留订单号并联系客服。

## 报告与保留期

完成后尽快下载报告。报告保留天数是实时配置，不在 Skill 中写死。下载异常时优先换电脑浏览器、允许下载或把压缩包保存到本地再解压；不要通过修改 URL 猜报告地址。

## 状态判断

- `COUNTING` / `PARSING`：等待平台解析字符数；
- `WAIT_SUBMIT` 且需要补差：处理原订单的补差或补单提示；
- `WAIT_SUBMIT` 且无需补差：等待页面自动提交或由用户在页面点击一次；
- `DETECTING`：已进入检测，保留原订单号查询；
- `REPORT_READY`：进入 `/reports` 下载，再按报告编码验真；
- `FAIL`：先看 `failReason` 和页面是否允许客服处理，不把接口超时直接说成检测失败。

## 图片参考

以下图片是用户提供的流程示例，只用于帮助定位页面字段，不承载真实订单或当前价格：

- `assets/report-guides/01-word-character-count.jpg`：Word/WPS 字符数（不计空格）预检。
- `assets/report-guides/02-vpcs-report-number.jpg`：报告首页报告编号位置示例。
- `assets/report-guides/03-report-download-archive.jpg`：报告下载压缩包与解压提示。
- `assets/report-guides/04-report-authenticity.jpg`：查重报告验真字段示例。
- `assets/report-guides/05-aigc-report-authenticity.jpg`：AIGC 报告编号与验真入口示例。
- `assets/report-guides/06-verify-report-code.jpg`：验真页面输入报告编码，前后不要有空格。
