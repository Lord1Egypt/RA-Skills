# 腾讯云短信常见错误码参考

当 API 调用失败时，返回结构化错误 JSON，其中 `code` 字段为腾讯云错误码。以下是常见错误码及其解决方案。

## 认证与权限错误

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| AuthFailure.SecretIdNotFound | SecretId 不存在 | 检查 `TENCENTCLOUD_SECRET_ID` 是否正确 |
| AuthFailure.SignatureFailure | 签名验证失败 | 检查 `TENCENTCLOUD_SECRET_KEY` 是否正确 |
| AuthFailure.TokenFailure | Token 错误 | 如使用临时密钥，检查 Token 是否过期 |
| UnauthorizedOperation.RequestIpNotInWhitelist | IP 不在白名单 | 在 API 密钥管理中添加当前 IP |
| UnauthorizedOperation.ServiceSuspendDueToArrears | 欠费停服 | 前往控制台充值 |

## 签名相关错误

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| FailedOperation.NotEnterpriseCertification | 非企业认证用户 | 签名/模板增查 API 仅支持企业认证，个人用户请在控制台操作 |
| FailedOperation.MissingSignature | 缺少签名 | 需先申请并通过签名审核 |
| FailedOperation.SignNumberLimit | 签名数量超限 | 国内短信上限 200 个签名 |
| FailedOperation.MissingSignatureToModify | 待修改的签名不存在 | 检查签名 ID 是否正确 |
| FailedOperation.SignInReviewingSet | 签名审核中 | 等待审核完成后再操作 |

## 模板相关错误

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| InvalidParameterValue.InvalidTemplateFormat | 模板格式错误 | 检查模板内容是否符合格式要求 |
| FailedOperation.TemplateNumberLimit | 模板数量超限 | 国内短信上限 1000 个模板 |
| FailedOperation.MissingTemplateToModify | 待修改的模板不存在 | 检查模板 ID 是否正确 |
| FailedOperation.TemplateAlreadyPassedCheck | 模板已通过审核 | 已通过的模板不能再次修改 |

## 发送相关错误

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| FailedOperation.TemplateParamSetNotMatchApprovedTemplate | 模板参数不匹配 | 检查模板参数数量和格式是否与模板一致 |
| FailedOperation.PhoneNumberInBlacklist | 手机号在免打扰 | 联系 [腾讯云 SMS 控制台](https://console.cloud.tencent.com/smsv2) 解除 |
| FailedOperation.InsufficientBalanceInSmsPackage | 套餐包余量不足 | 前往控制台购买套餐包 |
| LimitExceeded.PhoneNumberDailyLimit | 手机号日发送上限 | 单个手机号同一签名下每日上限，具体限制见控制台 |
| LimitExceeded.PhoneNumberThirtySecondLimit | 手机号 30 秒限频 | 降低同一手机号的发送频率 |
| LimitExceeded.PhoneNumberOneHourLimit | 手机号 1 小时限频 | 降低同一手机号的发送频率 |

## 参数错误

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| InvalidParameterValue.SdkAppIdNotExist | SdkAppId 不存在 | 前往控制台确认应用 ID |
| InvalidParameterValue.ContentLengthLimit | 短信内容长度超限 | 国内短信单条最多 500 字（含签名） |
| InvalidParameterValue.IncorrectPhoneNumber | 手机号格式错误 | 使用 E.164 格式，如 +8618501234444 |
| MissingParameter | 缺少必填参数 | 检查请求参数完整性 |

## 套餐包相关错误

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| InvalidParameterValue.BeginTimeVerifyFail | 起始时间验证失败 | 格式为 yyyymmddhh，如 2025010100 |
| InvalidParameterValue.EndTimeVerifyFail | 结束时间验证失败 | 格式为 yyyymmddhh，确保不早于起始时间 |

## 故障排查步骤

1. **检查凭证**：确认 `TENCENTCLOUD_SECRET_ID` 和 `TENCENTCLOUD_SECRET_KEY` 环境变量已正确配置
2. **检查权限**：确认 API 密钥对应的子账号有 SMS 相关权限（`QcloudSMSFullAccess`）
3. **检查签名/模板状态**：使用 `describe_sign.py` / `describe_template.py` 确认审核状态为"已通过"
4. **检查套餐包余量**：使用 `packages_statistics.py` 确认套餐包未过期且有余量
5. **使用 `--dry-run`**：先用预览模式验证参数正确性，再实际执行

官方错误码完整列表：https://cloud.tencent.com/document/product/382/52075
