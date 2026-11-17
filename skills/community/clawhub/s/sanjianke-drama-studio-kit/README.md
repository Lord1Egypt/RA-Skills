# 三剪客 · AI 短剧创作台 Skill

短剧创作台的选型评估与私有化搭建指南

面向要自建 AI 短剧创作台的技术负责人：**先把选型决定做对，再动手部署**。
覆盖五维选型打分、自建 / 采购 / SaaS 决策、许可风险识别、
全栈部署与配置、上线检查、成本对账与故障定位。

---

## 前置条件

阅读本 Skill 的文档部分**无任何依赖**，离线即可用。

若要在自己的环境里做成本量级测算，需要：

- Python 3.8 及以上（仅用标准库，无需安装任何第三方包）

若要真正部署一套创作台，你需要自行准备：

- 一台服务器（或本地机器），配置见 `references/deploy-and-configure.md`
- 数据库、缓存、多媒体工具三件套
- 模型服务凭证（文本 / 图片 / 视频 / 配音四类）
- 对象存储（对外服务建议再加 CDN）

**明确一点**：本 Skill 只提供判断依据、配置骨架和离线测算工具，
不代为申请账号、不代管密钥、不调用任何外部服务。

---

## 使用

按这个顺序走，每一步都有产出：

```
第 1 步  判断该不该自建
         → references/selection-scorecard.md
         产出：加权得分 + 自建/采购/SaaS 结论 + 风险登记

第 2 步  先算钱，再投入
         → scripts/cost_estimate.py
         产出：成本量级与结构占比

第 3 步  部署与配置
         → references/deploy-and-configure.md
         产出：可跑通最小闭环的环境

第 4 步  上线检查与持续运维
         → references/ops-and-compliance.md
         产出：上线检查表 + 巡检例程 + 合规确认
```

成本测算示例：

```bash
# 30 集，每集 2 分钟，完整测算（含生成成本）
python scripts/cost_estimate.py --episodes 30 --minutes 2 \
  --gen-image 40 --gen-video 30 --gen-tts 30

# 只看存储与带宽，不计生成成本
python scripts/cost_estimate.py --episodes 30 --minutes 2 \
  --gen-image 0 --gen-video 0 --gen-tts 0

# 缩短中间素材保存周期，观察留存占用变化
python scripts/cost_estimate.py --episodes 30 --minutes 2 --lifecycle-days 7

# 查看全部可调参数（单价、画质系数、拍摄比、生命周期等）
python scripts/cost_estimate.py --help
```

> 脚本中的**单价均为占位示例值**，必须替换为当期真实报价再采信结论。

---

## 依赖

| 项目 | 要求 | 说明 |
|---|---|---|
| 运行环境 | Windows / Linux / macOS | 只读文档时无依赖 |
| Python | 3.8+ | 仅成本测算脚本需要，只用标准库 |
| 待部署主机 | 见 `references/deploy-and-configure.md` | 按每月集数分四档 |
| 第三方服务 | 模型 API、对象存储（可选 CDN） | 使用者自行申请 |

本 Skill **不包含任何第三方项目的源代码**，也不需要安装上游项目才能使用。

---

## 安全

- 不内嵌任何密钥
- 不发起任何网络请求，全程离线运行
- 不读取、不写入、不代管任何 API Key、数据库口令或云存储凭证
- 测算脚本为纯计算，结果仅打印到终端，不落地文件
- 文档中出现的所有凭据均为占位符（如 `REPLACE_ME`），不构成可用配置
- 涉及 `LICENSE` 的判断只提示风险点，**不构成法律意见**

---

## 能力边界速览

**覆盖**：选型打分与决策、许可风险识别、全栈部署与配置、密钥管理规范、
四类模型接入思路、上线检查、成本对账、故障定位顺序。

**不覆盖**：上游项目源代码、法律意见、内容创作（剧本/画面/配音）、
账号与密钥代管、K8s 集群编排、多租户计费系统。

---

## 版权

本 Skill 由 **三剪客** 出品并独立编写，正文为原创内容，不包含第三方项目的源代码。

本 Skill 为通用实践总结，正文由三剪客独立编写，不含上游项目源代码。上游参考项目：https://gitee.com/forproject/zhenling-drama （AGPL-3.0）

---

## 许可证

MIT，见 `LICENSE.md`。

---

---

## 联系我们

- **技术微信：9872659** —— 加好友时说一下是从哪个 Skill 找过来的，直接给你配套的 API Key 与能跑的示例。
- **要算力 / 要 API Key**：[算力集市 · 注册领 API Key](https://api.a7w.cn/) —— 一个 Key 调用全部 AI 算力，注册、充值、创建 Key 都在这里。
- **更多 AI 插件与接口**：[AI 插件市场](https://aigc.a7w.cn/)。

---

## 相关链接

| 链接 | 地址 | 说明 |
|---|---|---|
| [算力集市 · 注册领 API Key](https://api.a7w.cn/) | api.a7w.cn | 一个 Key 调用全部 AI 算力；注册、充值、创建 Key 都在这 |
| [AI 插件市场](https://aigc.a7w.cn/) | aigc.a7w.cn | 浏览全部 AI 插件与接口说明 |
| [三剪客 · 一句话批量出片](https://ks.a7w.cn/) | ks.a7w.cn | 短剧二创 / 影视解说 / 矩阵号批量混剪桌面客户端 |
| [视频超清 · 在线批量超分](https://vr.a7w.cn/) | vr.a7w.cn | 网页版视频超分，批量处理，最高 4K |
| [0人公司 · AI Agent 平台](https://a7w.cn/) | a7w.cn | 主站，了解整套 AI Agent 生态 |
