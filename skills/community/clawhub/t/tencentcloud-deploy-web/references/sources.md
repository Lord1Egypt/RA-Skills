# 知识来源与验证记录

标记含义：
- **[实测]**：用 agent-ops 子用户真实调用过 API，或在浏览器里真实打开过页面
- **[文档]**：腾讯云官方文档原文，没有实测
- **[经验]**：我们 2026 年 7–10 月的部署记录（tccli 日志 + 对话记录）

| 事实 | 来源 | 日期 |
|---|---|---|
| 注册页：默认微信扫码，另有邮箱/QQ/企业微信/小程序公众号；手机号只能填 +86 | [实测] 浏览器打开 cloud.tencent.com/register 的页面快照 | 2026-10-08 |
| 注册方式说明，以及"注册后需要实名认证" | [文档] cloud.tencent.com/document/product/378/17985（页面更新于 2026-08-14） | 2026-10-08 |
| 实名认证：个人用微信扫码/QQ 扫码/人脸识别；企业有 5 种方式；不实名无法购买云服务 | [文档] cloud.tencent.com/document/product/378/3629（2026-09-16） | 2026-10-08 |
| 控制台地址：实名认证、操作审计（cloudaudit）、域名信息模板、CAM 策略页都能打开 | [实测] 已登录浏览器，核对了页面标题 | 2026-10-08 |
| 域名注册分 5 步，下单时必须选已通过实名审核的信息模板 | [文档] cloud.tencent.com/document/product/242/9595（2025-05-08） | 2026-10-08 |
| 信息模板审核要 1–3 个工作日；未实名会被 ServerHold，审核通过后 1–2 个工作日恢复 | [文档] cloud.tencent.com/document/product/242/6707（2025-07-29） | 2026-10-08 |
| `domain CheckDomain` / `DescribeDomainPriceList` 子用户可以调，返回实时价格 | [实测] | 2026-10-08 |
| `domain DescribeTemplateList` 会返回实名模板里的个人信息（证件号、姓名、地址） | [实测] → 已在策略里 deny | 2026-10-08 |
| agent-ops 策略的放行和拒绝范围（含 DryRun 验证不能购买） | [实测] tests/tencentcloud-deploy-web | 2026-10-08 |
| 参数和资源存在性校验先于 CAM 鉴权 | [实测] | 2026-10-08 |
| TAT RunCommand 能以 root 在 Lighthouse 上执行命令 | [实测]（只在已有实例上试过，新买实例是否预装 TAT agent 还没验证） | 2026-10-08 |
| AssociateInstancesKeyPairs 会强制关机，并让原有密钥失效 | [文档] tccli 内置的 API 说明 | 2026-10-08 |
| Lighthouse 的 Linux 实例默认放行 22/80/443 | [文档]（第三方转述）；和 [经验] 2026-10-02 遇到的 443 不通相矛盾，以 DescribeFirewallRules 为准 | 2026-10-08 |
| 香港选「入门型」不保证大陆到香港的网络质量 | [经验] 2026-10-02，来自购买页提示 | — |
| EdgeOne 选 global/mainland 加速区域要备案，overseas 不用；国内站没有免费套餐 | [经验] 2026-08-08 | — |
| 本机 fake-IP 代理会让本地 dig/nc 结果失真 | [经验] + [实测] | 2026-10-08 |
| tcapi.py 的 TC3 签名：sts/dnspod/teo/lighthouse/domain 调用全部成功 | [实测] | 2026-10-08 |
| `sts GetCallerIdentity` 不传 Region 会报 MissingParameter | [实测] | 2026-10-08 |
| `domain DescribeDomainPriceList` 的 Year 参数必须是数组 | [实测] | 2026-10-08 |
| setup.py 网页向导：错误 token、格式错误、ID 错误、Key 错误、成功写入（权限 600），这几种情况都测过 | [实测] macOS + Chrome | 2026-10-08 |
| setup.py 在 Windows 上的表现 | **待测**（用户安排 Windows 机器测试） | — |
| run_on_server.py：输出能取回，退出码能透传，`--user ubuntu` 可用 | [实测] | 2026-10-08 |
| buy_server 生成的购买链接：regionId=5 / PURE_OS / blueprintOfficialId / bundleId 都能正确预选，loginSet 无效；附加项默认不勾；购买页默认选中的是「中国香港入门型」+ OpenCloudOS | [实测] 已登录浏览器打开购买页核对 | 2026-10-08 |
| 策略改为白名单制（8 条读 + 38 个写操作 + 38 项拒绝），动作名全部用 tccli 内置接口清单核对存在 | [实测] tccli 3.1.145 help | 2026-10-11 |
