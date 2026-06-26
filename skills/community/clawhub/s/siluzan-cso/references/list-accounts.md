# list-accounts — 媒体账号列表

> 账号 ID（entityId / mediaCustomerId）是发布配置和数据查询的基础字段，使用 `publish` 或 `report` 前通常需要先运行本命令。

---

## 常用场景速查

| 用户意图                                 | 命令                                                                                   |
| ---------------------------------------- | -------------------------------------------------------------------------------------- |
| 查所有账号总览（粉丝/播放/获赞横向对比） | `siluzan-cso list-accounts`                                                            |
| 按平台筛选账号                           | `siluzan-cso list-accounts --media-type <平台>`                                        |
| 按名称搜索账号                           | `siluzan-cso list-accounts --name "账号名"`                                            |
| 获取账号完整字段（用于发布配置或脚本）   | `siluzan-cso list-accounts --json-out ./snap-cso`                                      |
| 精准定位单个账号（名称 + 平台）          | `siluzan-cso list-accounts --name "账号名" --media-type YouTube --json-out ./snap-cso` |
| 只看异常/过期账号                        | `siluzan-cso list-accounts --state abnormal`                                           |
| 只展示基础信息（隐藏总览数据）           | `siluzan-cso list-accounts --no-overview`                                              |

---

## 平台名称对照表

| 用户常说                                    | `--media-type` 参数值   |
| ------------------------------------------- | ----------------------- |
| 抖音                                        | `Douyin`                |
| TikTok                                      | `TikTokBusinessAccount` |
| YouTube                                     | `YouTube`               |
| 微信视频号 / 视频号                         | `Wechat`                |
| Instagram / IG                              | `Instagram`             |
| Facebook / FB                               | `Facebook`              |
| Twitter / X（同一平台，Twitter 已更名为 X） | `Twitter`               |
| Kwai / 快手                                 | `Kwai`                  |

> 同一平台名称在 `--media-type`（list-accounts）和 `report fetch --media` 中通用。

---

## JSON 输出字段说明

`--json-out` 落盘的每个账号对象中，常用字段如下（处理落盘 JSON 前先读同名 `*.outline.txt`，见 `references/core/agent-conventions.md`）：

| 字段                          | 用途                                                                   |
| ----------------------------- | ---------------------------------------------------------------------- |
| `entityId`                    | 发布配置 `accounts[].entityId`（UUID 格式）                            |
| `mediaCustomerId`             | `report fetch --maids <id>` 的参数；也用于账号分组                     |
| `mediaAccountType`            | 发布配置 `accounts[].mediaAccountType`；`--media-type` 参数值          |
| `mediaCustomerName`           | 发布配置 `accounts[].mediaCustomerName`                                |
| `externalMediaAccountTokenId` | 发布配置 `accounts[].externalMediaAccountTokenId`（UUID 格式）         |
| `invalidOAuthToken`           | `true` 表示 Token 已失效，需重新授权（参见 `references/authorize.md`） |
| `expiresOn`                   | Token 到期时间                                                         |
| `overview.fansCount`          | 当前粉丝数                                                             |
| `overview.videoCount`         | 发布作品总数                                                           |
| `overview.playCount`          | 历史总播放数                                                           |

---

## 示例

```bash
# 查所有账号总览
siluzan-cso list-accounts

# 只看 TikTok 平台
siluzan-cso list-accounts --media-type TikTokBusinessAccount

# 精准定位 + 获取完整字段（用于填写发布配置），落盘后用脚本读盘（见 references/core/tips.md）
siluzan-cso list-accounts --name "品牌账号" --media-type YouTube --json-out ./snap-cso

# 搜索所有平台中名称包含关键词的账号
siluzan-cso list-accounts --name "品牌名" --json-out ./snap-cso

# 只看异常账号（Token 过期等）
siluzan-cso list-accounts --state abnormal
```

---

## AI 行为规则

- 用户要找一个具体账号时，**优先用 `--name` + `--media-type` 双重过滤**，通常可直接得到唯一结果。
- 找到账号后，`entityId` + `externalMediaAccountTokenId` + `mediaCustomerId` 即可直接填入发布配置，无需再次询问用户。
- 账号 `overview` 字段已包含粉丝数/播放数等基本数据，找到账号后无需再单独调用 `report fetch`。
- `invalidOAuthToken: true` 的账号需先重新授权，再发布（参见 `references/authorize.md`）。

---

## 交叉引用

- 发布时需要账号字段 → 参见 `references/publish.md`
- 用账号 ID 查运营数据 → 参见 `references/report.md`
- 将账号加入分组 → 参见 `references/account-group.md`
- 账号 Token 失效需重授权 → 参见 `references/authorize.md`
