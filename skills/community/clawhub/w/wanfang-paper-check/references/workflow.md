# 万方公共工作流

## 正式顺序

产品目录 → 用户确认用途和产品 → 校验题目/作者/日期/格式 → presign → HTTPS PUT 上传 → create 建单 → 返回 orderNo → 用户在原页面支付 → status 查询 → report 页面下载/预览 → 官方验真。

## 幂等与停止点

- presign 成功但 PUT 未确认：不创建新订单，先检查上传是否完成。
- PUT 成功但 create 超时：不要再次上传和建单；先用页面检查是否已有 orderNo。
- create 已返回 orderNo：后续只查询同一 orderNo，不重复扣款。
- WAIT_PAY/PAYING：只交回 payment 页面，不调用支付接口。
- COMPLETED：只下载/阅读/验真，不再次提交同一文件。

## 页面交接

- 待支付：/pwf?orderNo={orderNo}&stage=payment。
- 检测中：/pwf/check?orderNo={orderNo}&stage=progress。
- 报告可用：/pwf/check?orderNo={orderNo}。
- 报告验真：先到 CQCCJY 统一入口，选择万方，再按官方表单填写字段。

## 不做的事

不自动付款、补差价、核销检测卡、输入验证码、上传人工报告或调用后台接口。没有实时目录时可以解释旧快照，但不使用旧价格正式下单。
