# 店铺订单状态清单

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；目前 Mac 版仅支持 M 芯片。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

从当前可见的本人订单列表中，快速得到能核对的状态计数、待商家处理订单和页面证据位置；默认只读，敏感信息会遮盖，不会修改订单或发送消息。

**输入**：本轮请求已说明是本人或有权查看的店铺订单页面，并提供指定 `browserId`、日期范围和状态筛选；每次最多 20 单。已有明确说明时不重复询问，只有权限归属不清楚时才暂停澄清。  
**结果**：已确认范围内的状态计数、待处理清单、每项可见证据位置和缺项说明。日期或状态筛选未确认时，Skill 明确不报告全店总数。

![订单状态清单推广图](assets/promo.png)

## 安装

```bash
npx skills add xxjrq/shop-order-status-digest-free
```

## 使用方式

这是浏览器类 Skill，需先安装并连接 Easy WebBridge。GitHub 主下载地址：<https://github.com/xxjrq/easy-webbridge>；Gitee 备用地址：<https://gitee.com/xxjrq/easy-webbridge>。

向 Agent 提供订单页、要使用的 browserId 和范围；如果本轮请求已说明订单属于你或你获准查看，无需额外确认。例如：

```text
使用我有权查看的店铺订单列表，在我指定的 browserId 中只读汇总 2026-09-01 至 2026-09-30、全部状态的当前可见订单；最多20单，输出状态计数、待处理事项和证据位置，遮盖敏感信息，不修改订单或发送消息。
```

Skill 会为一次任务单独创建并复用一个标签组，只管理自己创建的 session；不会广播到所有账号或接管已有页面。遇到登录、验证码、风控或筛选未确认时会暂停，不会绕过。

## 交付示例

```text
范围：2026-09-01 至 2026-09-30；状态筛选：全部状态；可见订单：4/最多20
来源：订单列表，第1页第1–4行
状态计数：待发货 1，已发货 1，退款中 1，已完成 1
需商家接手：ORD-…001（待发货，核对库存后发货；第1页第1行状态标签）
缺项/限制：无
```

示例仅展示结果格式，不代表在线采集。完整行为和边界见 [SKILL.md](SKILL.md)。

## 自测

```bash
node scripts/self-test.mjs
```

自测只使用仓库内的离线成功与失败页面资料模拟，不打开浏览器、不依赖兄弟 Skill 或本机绝对路径。

## 来源与许可证

业务场景仅参考 [Saleor](https://github.com/saleor/saleor) 的公开项目说明；本仓库的说明、样例和实现均为原创，未复制其源码或文案。许可证为 [MIT-0](LICENSE)。
