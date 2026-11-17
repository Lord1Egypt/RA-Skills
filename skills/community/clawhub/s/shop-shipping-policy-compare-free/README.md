# 店铺配送政策对照

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

把 2–3 个指定公开配送或售后政策页变成一张可追溯的对照表：明确展示发货时效、适用地区、费用条件和缺失条款。条件无法归属店铺或页面互相矛盾时，结果会明确标为“无法确定”，不会猜测运费、送达日期或交易资格。

输入是用户指定的 `browserId` 与 2–3 个公开政策 URL；结果是带页面标题与 URL 来源的 Markdown 对照表，以及不可作出结论的缺项清单。默认只读，可选的草稿填充也绝不发布或发送。

![店铺配送政策对照推广图](assets/promo.png)

## 安装

```bash
npx skills add xxjrq/shop-shipping-policy-compare-free
```

## 使用方式

本 Skill 需要已安装的 Easy WebBridge，主下载地址为 [GitHub](https://github.com/xxjrq/easy-webbridge)，备用地址为 [Gitee](https://gitee.com/xxjrq/easy-webbridge)。请在目标浏览器 Profile 中连接扩展，并在请求中给出要使用的 `browserId`；一次任务只使用该环境，并创建自己的 session 标签组。

示例请求：

```text
使用 browserId <我指定的环境>，只读对照这三个公开配送政策页：
https://shop-a.example/shipping
https://shop-b.example/policy
https://shop-c.example/delivery
整理发货时效、适用地区、费用条件和缺失条款，保留每条来源；不推断运费或送达。
```

## 结果示例

| 店铺/页面 | 发货时效 | 适用地区 | 费用条件 | 判断 | 来源与缺项 |
| --- | --- | --- | --- | --- | --- |
| 店铺 A | 付款后 1–2 个工作日 | 中国大陆 | 满 99 元免运费；未满 99 元时结算页显示运费 | 明确 | 配送说明；URL |
| 店铺 B | 页面未见明确时长（仅称库存确认后安排发货） | 页面未见明确条款（偏远地区范围以结算页为准） | 页面未见明确条款 | 无法确定 | 售后与配送；时长、地区范围与费用缺失 |

来源页未写明的内容会保留为缺项；如果有冲突或店铺归属不清，只报告证据和“无法确定”。本工具不提供法律意见，也不保证实际交易条件。

## 验证

```bash
node scripts/self-test.mjs
```

该命令只检查仓库结构、图标和离线资料模拟；fixtures 明确不代表在线采集或真实店铺结论。

## 素材与参考

- `assets/promo.png`：本 Skill 的原创推广图；`icon-512.png` 为对应的 512×512 原创图标。
- 业务参考：[Saleor repository](https://github.com/saleor/saleor) 与其 [README](https://github.com/saleor/saleor/blob/main/README.md)，仅用于核对公开电商业务语境，未复制代码或文本实现。
- 仓库采用 [MIT-0](LICENSE)。
