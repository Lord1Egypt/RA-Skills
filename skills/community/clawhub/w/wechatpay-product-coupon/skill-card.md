## Description: <br>
微信支付商品券接入解决方案，帮助开发者完成微信支付商品券的券类型选型、发券、核销、查询、退券、回调处理、示例代码参考、质量评估和排障。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpeng319](https://clawhub.ai/user/zhangpeng319) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and payment integration teams use this skill to plan and troubleshoot WeChat Pay product coupon integrations for brand-direct and service-provider modes. It supports choosing coupon types, locating Java and Go examples, checking API parameters, reviewing callback and signature handling, and diagnosing coupon workflow issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request sensitive payment authorization artifacts, OpenIDs, coupon codes, signatures, or response details while helping with a WeChat Pay integration. <br>
Mitigation: Use test credentials first, redact private keys, tokens, full signatures, full OpenIDs, coupon codes, response bodies, and headers before sharing, and keep diagnostic execution local. <br>
Risk: The bundled scripts and examples can call live WeChat Pay APIs when populated with real credentials and identifiers. <br>
Mitigation: Review commands before running them, start in a test environment, and verify signing, callback, and coupon-state behavior before adapting examples for production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangpeng319/wechatpay-product-coupon) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zhangpeng319) <br>
- [Brand-direct product coupon user detail API](https://pay.weixin.qq.com/doc/brand/4015736414) <br>
- [Service-provider product coupon user detail API](https://pay.weixin.qq.com/doc/partner/4013080339) <br>
- [券类型选型](references/3-品牌与服务商通用/券类型选型/券类型选型.md) <br>
- [代码示例使用规范](references/3-品牌与服务商通用/接入规范/代码示例使用规范.md) <br>
- [签名验签规范与排查](references/3-品牌与服务商通用/接入规范/签名验签规范与排查.md) <br>
- [回调处理](references/3-品牌与服务商通用/接入规范/回调处理.md) <br>
- [品牌排障手册](references/1-品牌/问题排查/排障手册.md) <br>
- [服务商排障手册](references/2-服务商/问题排查/排障手册.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Java or Go API examples, local diagnostic commands, parameter checklists, and troubleshooting analysis.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
