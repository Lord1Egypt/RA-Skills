---
name: wanfang-paper-check
description: 当用户询问或操作万方本科、硕博、高职高专、期刊、职称、新文献、专著、课程作业或文本 AIGC 检测，或需要在 wanfang.cqccjy.cn 选择产品、上传论文、创建/查询订单、交接支付、下载报告、阅读报告或验真时使用。该 Skill 固定使用 CQCCJY 万方公共用户端和公开接口；不自动支付、不代填检测卡/验证码、不操作后台人工履约，也不把个人预检承诺为学校或期刊终检。
metadata:
  short-description: 万方产品选型、上传下单、订单查询、报告与验真
---

# 万方查重全流程 Skill

本 Skill 是 Fanyu/CQCCJY 万方公共用户端的操作与回答规范。固定站点是 https://wanfang.cqccjy.cn，主要入口是：

- /pwf：自助选择产品、上传文件、创建订单、在页面完成支付。
- /pwf/check：自助订单进度、报告查看与下载。
- /pwf?orderNo={order_no}&stage=payment：已有订单的支付交接页。
- /pwf/check?orderNo={order_no}&stage=progress：已有订单的进度交接页。
- 统一报告验真入口：https://vpcs.cqccjy.cn/pwp/verify；万方官方备用页：https://truth.wanfangdata.com.cn/。

站点、产品目录、页面路由和业务归属不能被用户输入覆盖。完整地址规则见 references/domain-and-routes.md。

## 一、先判断用户要什么

| 用户表达 | 默认识别 | 不能做的事 |
|---|---|---|
| 万方本科论文查重 | WF_UNDERGRADUATE | 不因价格默认本科版适合所有学校 |
| 万方硕士、博士、研究生 | WF_GRADUATE | 不把本科版当硕博替代 |
| 高职、高专、专科毕业论文 | WF_VOCATIONAL | 不把高职版和本科版混为同一比对库 |
| 期刊投稿、编辑部预检 | WF_JOURNAL | 不承诺等同期刊终审库 |
| 职称评审、已发表材料 | WF_TITLE | 不缺少发表/收稿日期时强行建单 |
| 新发表文献、刚收录材料 | WF_NEW_LITERATURE | 不把新文献版说成所有论文默认版 |
| 专著、长篇作品 | WF_MONOGRAPH | 不按毕业论文规则解释专著结果 |
| 课程作业、课程论文 | WF_COURSEWORK | 不把课程作业版当学位论文终检 |
| 万方文本 AIGC/AI 率 | WF_TEXT_AIGC | 不把 AIGC 结果当重复率 |
| 只说“万方查重” | 先确认层级/用途 | 不擅自按最低价下单 |

产品选择顺序固定为：审核方当年度书面要求 > 当前实时目录的用途、格式、字符边界和价格 > 本地快照仅作解释。只要用户没有明确用途，先问清楚，不创建订单。

## 二、当前实时产品与计费事实

截至 2026 年 10 月 2 日，GET /api/paper/wanfang/public/config 返回 10 个启用产品。以下是本地快照，正式回答“现在多少钱/能否提交”前仍须运行 products 读取实时目录：

| productCode | 当前名称 | 用途 | 计费 | 当前价格 |
|---|---|---|---|---:|
| WF_UNDERGRADUATE | 万方本科版 | 本科毕业论文 | 每 1000 字符 | ￥2.40 |
| WF_GRADUATE | 万方硕博版 | 硕士/博士学位论文 | 每 1000 字符 | ￥2.40 |
| WF_VOCATIONAL | 万方高职高专版 | 高职、高专、专科 | 每 1000 字符 | ￥2.40 |
| WF_JOURNAL | 万方期刊版 | 期刊投稿/编辑部预检 | 每 1000 字符 | ￥2.40 |
| WF_TITLE | 万方职称版 | 职称评审、已发表材料 | 每 1000 字符 | ￥4.00 |
| WF_NEW_LITERATURE | 万方新文献版 | 新文献/新收录材料 | 每 1000 字符 | ￥2.40 |
| WF_MONOGRAPH | 万方专著版 | 专著、长篇作品 | 每 1000 字符 | ￥2.60 |
| WF_COURSEWORK | 万方课程作业版 | 课程作业/课程论文 | 每 1000 字符 | ￥2.40 |
| WF_TEXT_AIGC | 万方文本 AIGC 检测 | AI 生成风险专项 | 每 1000 字符 | ￥1.60 |

当前产品的 minCount/hintMinCount 为 200，hintMaxCount 为 300000；计费单位是字符，实际金额按平台解析出的字符数和 unitWordCount=1000 向上计费。不要用 Word/WPS 本地统计替代平台解析值。

- 普通文本产品当前 fileType：doc,docx,txt,pdf,rtf。
- WF_TEXT_AIGC 当前 fileType：doc,docx,txt,pdf，不把 rtf 视为 AIGC 自动支持格式。
- WF_TITLE 当前 acceptTimeRequired=true，必须提供真实发表/收稿/录用日期；其他当前产品为 false，但若实时目录改变，按实时返回执行。
- 当前 supplementPayEnabled=true，表示页面可能支持按实际超出字符数补差价；Skill 不自动补差价、不重复扣款，只把用户交回原页面。
- 当前公开支付方式：检测卡号、微信、支付宝；是否可用以实时 paymentChannels 为准。

产品的外部供应商 ID、内部渠道码、库存/余额、人工履约路由不是用户选型依据，也不写进用户回答。

## 三、上传前检查

### 题目、作者和日期

- 题目必填，当前公共接口按最多 255 个字符校验；不要用“测试”“论文”掩盖真实题目。
- 作者必填，建议 2–64 个字符，至少包含中文或 ASCII 字母/数字，不能是纯符号。
- 只有实时产品 acceptTimeRequired=true 或页面明确出现日期字段时才填写 YYYY-MM-DD；不能编造日期。
- 公共页面不收集学校、班级、专业等内部字段；Skill 不自行补传。

### 文件

- 上传最终定稿，不上传摘要、截图、压缩包、空白占位稿或只含部分章节的节选。
- 先服从实时产品 fileType，不要把“万方官网通常支持”当成当前用户端一定支持。
- 默认硬上限 50 MiB；页面建议 20 MB 以内，接近上限时优先让用户在页面确认。
- DOC/DOCX 通常比 PDF 更适合章节、脚注、参考文献识别；但产品不支持时不能强改格式。
- 删除修订、批注和隐藏审阅痕迹后再上传；不要为了降重删除真实引用或伪造参考文献。

### 先做 dry-run

    python3 scripts/wanfang_client.py --dry-run submit --product-code WF_UNDERGRADUATE --title 论文题目 --author 作者姓名 --file ./论文.docx

dry-run 只校验本地快照、题目、作者、日期、扩展名和文件大小；不访问产品接口、不拿预签名、不上传、不建单。正式提交前仍必须重新读取 live products。

## 四、公共页面与 API 完整流程

### A. /pwf 自助流程

1. 打开 https://wanfang.cqccjy.cn/pwf，确认地址栏仍是 wanfang.cqccjy.cn。
2. 读取实时目录，按审核方要求选择 productCode；不要用外部 ID 或内部渠道码代替。
3. 填写题目、作者；职称版或页面要求时再填真实日期。
4. 页面先调用 POST /api/paper/wanfang/public/upload/presign 获取本站签发的 uploadUrl/objectKey，再用 HTTPS PUT 上传文件，最后调用 POST /api/paper/wanfang/public/order/create 建单。
5. 建单成功后记录 orderNo、productCode/productName、payAmount、payStatus、status，把用户交回 https://wanfang.cqccjy.cn/pwf?orderNo={orderNo}&stage=payment。
6. 用户本人在页面选择检测卡号、微信或支付宝完成支付。Skill 不代付、不传卡号、不提交支付密码。
7. 支付后进入 /pwf/check?orderNo={orderNo}&stage=progress，等待状态变化；不要重复上传或重复建单。

### B. 订单状态与报告

- status 只查询用户提供或本次创建的原 orderNo：

    python3 scripts/wanfang_client.py status --order-no 订单号

- report 只在订单已经完成或服务端明确返回报告字段时请求 report-download-url：

    python3 scripts/wanfang_client.py report --order-no 订单号

- 报告页优先使用 https://wanfang.cqccjy.cn/pwf/check?orderNo={orderNo} 的按钮；脚本不会猜 URL，也不会把供应商临时 HTTP 地址暴露给用户。

### C. 当前接口没有的能力

当前 CQCCJY 万方公开域名配置只声明 config/presign/create/order/report-download-url。不要自行拼接不存在的 order/query、支付回调、供应商上传或后台人工接口。用户只有第三方支付单号时，先让其在 /pwf 页面使用页面提供的查询能力；Skill 不跨产品猜测订单。

## 五、脚本命令与输出

    python3 scripts/wanfang_client.py products
    python3 scripts/wanfang_client.py submit --product-code WF_GRADUATE --title 题目 --author 作者 --file ./paper.docx
    python3 scripts/wanfang_client.py status --order-no 订单号
    python3 scripts/wanfang_client.py report --order-no 订单号
    python3 scripts/wanfang_client.py verify

脚本输出重点字段：action、products、order_no、product_code、product_name、status、status_label、pay_status、pay_amount、word_count、fail_reason、browser_url、browser_urls、report_download_url、next_action。

脚本主动过滤 uploadUrl、签名 header、STS、对象存储路径、供应商 token、渠道配置等执行字段；不会输出文件正文、凭据或支付敏感信息。

## 六、支付、状态和内部履约

页面可根据实时配置显示检测卡号、微信、支付宝以及补差价入口。Skill 只交接页面，不调用扣款、核销或补款接口。支付成功必须以订单 payStatus=PAID 或页面事实为准，不能把“打开支付页”说成已付款。

| 状态 | 用户可见解释 | 下一步 |
|---|---|---|
| PENDING_UPLOAD | 等待文件上传 | 回到同一订单页上传，不重复建单 |
| WAIT_PAY / UNPAID | 已建单待支付 | 用户在原页面完成支付 |
| PAYING | 支付处理中 | 等待页面/订单刷新，不重复支付 |
| PAID / SUBMITTING | 已支付，等待提交 | 继续查询原订单 |
| DETECTING / PROCESSING | 万方检测中 | 等待异步处理 |
| COMPLETED / SUCCESS | 检测完成 | 打开报告页下载/预览 |
| FAIL / FAILED | 处理失败 | 保留失败原因，联系客服；不改内部渠道 |

服务端可能存在 AUTO/MANUAL、供应商路由、时间窗、轮询回调和人工下载上传，但这些是内部履约逻辑。公共请求不传 processMode、fulfillmentMode、channelCode、externalProductId 或供应商回调字段，也不向用户暴露供应商名、余额、人工操作人或路由细节。详见 references/internal-routing.md。

## 七、报告阅读与官方验真

只解读报告真实出现的字段。可能出现总体相似、相似片段、来源文献、参考文献/自引识别、AIGC 风险等字段，但不同产品和报告版本不同：

- 不把总体相似率直接称为抄袭比例。
- 不用 100%-相似率自创原创率。
- AIGC、格式、数据图像专项与文本相似性报告不可互相替代。
- 是否合格只按学校、期刊或单位书面规则，Skill 不创造统一红线。

先打开统一入口 https://vpcs.cqccjy.cn/pwp/verify，选择万方报告验真；统一入口不可访问时才打开 https://truth.wanfangdata.com.cn/。万方常见字段是分段报告编号、文献名称/批次名称、验证码。验证码必须由用户本人识读并提交；验真通过只说明官方系统找到对应记录，不等于论文合格。

## 八、失败与恢复

- 4xx 参数错误：按服务端信息修正产品、题目、作者、日期或格式；不盲目重试。
- 产品配置失败：可以说明暂时无法读取实时目录，但不使用过时价格正式建单。
- 预签名失败：确认没有 orderNo 后才考虑重试；不输出签名 URL。
- PUT 上传失败：不直接重复建单；检查文件和签名是否过期，重新从同一页面开始。
- 建单超时：先查询页面或联系客服确认是否已生成订单，无法确认前不重复上传。
- 已有 orderNo 后网络超时：只查询同一订单，不创建新单。
- WAIT_PAY/PAYING：用户在原页面继续支付；不重复支付。
- FAIL/SUBMIT_FAIL：展示状态和 failReason，联系客服；不改内部渠道、不伪造完成。
- 报告完成但下载失败：先用 /pwf/check 页面按钮；不要暴露供应商 HTTP 临时地址。
- 验真失败：检查四段编号、题名、验证码的空格和字符混淆；连续失败后停止试错并联系官方支持。

## 九、不可违反的边界

- 只访问 references/domain-and-routes.md 声明的 HTTPS 公共地址，不接受用户覆盖 URL、供应商或内部渠道。
- 不自动付款、补差价、核销检测卡、提交验证码、收集支付密码、登录凭证或银行卡。
- 不调用 admin、super-admin、supplier、platform-manual、员工客户中心接口。
- 不传内部履约字段，不猜第三方支付单号对应的订单，不跨品牌复用 orderNo。
- 不删除订单、不退款、不标记失败、不上传人工报告。
- 不把个人预检承诺为学校/期刊终检，不创造统一合格线。
- 不提供隐藏字符、图片化正文、拆分规避、机械洗稿、伪造引用或验证码绕过。

## 十、专业回答模板

### 产品咨询

先说明实时产品名称、用途、字符单位、格式、边界和价格；如果用户没有论文层级或用途，先追问而不是替选。

### 上传下单

按 products -> 校验产品/格式/大小 -> dry-run -> 用户确认 -> submit -> 返回 orderNo 与支付/进度页面执行。

### 订单跟进

先给 status/payStatus/failReason，再给原订单页面和唯一下一步；不要同时建议重建订单。

### 报告解读

先识别报告类型和真实字段，再引用学校/期刊规则；明确验真、报告存在、检测完成、达到要求是四件不同的事。

## 十一、参考文件按需加载

- 固定域名与路由：references/domain-and-routes.md
- 产品、别名、实时快照：references/product-catalog.md 与 references/product-catalog.json
- 页面流程和公共 API：references/workflow.md 与 references/api-contract.md
- 支付、状态和停止条件：references/settlement-and-status.md
- 内部供应商与人工履约：references/internal-routing.md
- 报告阅读与官方验真：references/report-and-verification.md
- FAQ：references/faq.md
- 万方检索范围与学术诚信边界：references/knowledge.md
