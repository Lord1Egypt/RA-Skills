## 一、开户流程（五步语义）

| 步骤 | 含义       | Agent 内部动作（勿原样贴给用户）                                     |
| ---- | ---------- | -------------------------------------------------------------------- |
| ①    | 准备资料   | 向用户说明**业务项清单**；无法代替用户准备资质                       |
| ②    | 填写并提交 | `open-account google-wizard`（TTY）或 `open-account google`          |
| ③    | 等待审核   | `account-history -m Google`                                          |
| ④    | 审核通过   | 同上                                                                 |
| ⑤    | 充值激活   | **必须网页**；`config show` → `webUrl` + 充值路径（见 `finance.md`） |

美元账户最低充值约 **100 USD**，人民币约 **700 CNY**（以平台为准）。

---

## 二、字段（对用户 vs Agent）

**对用户说明时**只使用「字段 / 说明」两列（业务语言）。  
**Agent 参数**列仅供内部组命令，**禁止**写入对用户回复。

| 字段            | 说明（可对用户说）                                                   | Agent 参数（勿展示）                                             |
| --------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------- |
| 公司名称        | 用于匹配/创建广告主组                                                | `--company`                                                      |
| 推广网址        | 可只写域名，提交时会自动补协议                                       | `--promotion-link`                                               |
| 推广类型        | 企业对企业（b2b）/ 企业对消费者（b2c）/ 应用（app）                  | `--promotion-type`：`b2b` \| `b2c` \| `app`                      |
| 一级 / 二级行业 | **可选**；网页自 2025-04-22 起已隐藏 Google 行业下拉（后端字典不稳） | `--industry1` / `--industry2`（可选）；列表：`google-industries` |
| 账户名称        | 广告账户显示名                                                       | `--account-name`                                                 |
| 币种            | CNY 或 USD                                                           | `--currency`                                                     |
| 时区            | 时区 Code；可省略走币种默认；勿用展示名                              | `--timezone`（可选）；列表：`google-timezones`                   |
| 开户数量        | 1～3                                                                 | `--counts`                                                       |
| 邀请邮箱        | 开通后接收账户邀请的邮箱                                             | `--invite-email`                                                 |

**币种默认时区**：CNY → `Asia/Shanghai`；USD（或其它非 CNY）→ `Asia/Hong_Kong`。其它时区从 `google-timezones` 取 **Code** 列。

**行业（与网页一致，非必填）**：不传时 MAG `industry.level1/level2` 为空串，账户 **`customer_info.industry` 统一为 `"-"`**（与网页未填抓包一致）。若传齐一级/二级则拼 `level1-level2`。

提交时按公司名称自动查找/创建广告主组并拿 `magKey`，**无需**让用户填 magKey。

---

## 三、推荐用法（Agent 执行参考，勿贴给用户）

### 非交互（Agent / 脚本首选）

```bash
siluzan-tso open-account google \
  --company "某某公司" \
  --promotion-link "https://www.example.com" \
  --promotion-type b2c \
  --account-name "某某公司-美国投放" \
  --currency USD \
  --timezone "America/New_York" \
  --invite-email "user@gmail.com" \
  --counts 1
```

常用时区：`Asia/Shanghai`、`Asia/Hong_Kong`、`America/New_York`、`America/Los_Angeles`、`Europe/London`。完整列表：`open-account google-timezones [--keyword <关键词>]`。行业可选：`google-industries`（CI 上字典接口可能 500，与网页隐藏行业同源问题）。

### 交互向导（需真实 TTY；Agent 不可用）

```bash
siluzan-tso open-account google-wizard
```

### 审核与充值

```bash
siluzan-tso account-history -m Google
# 审核通过后：config show → https://www.siluzan.com/v3/foreign_trade/tso/recharge/pay?mediaType=Google
```

---

## 四、Agent 指令模板

1. **首次回复**：向用户输出 Google **全部必填业务项**（见 § 二「字段 / 说明」；与 `open-account-by-media.md` § 全平台总览一致），含格式/枚举（如 b2b/b2c/app、USD/CNY），再请用户逐项提供；**勿**输出 `--flag` / CLI 选项名 / 命令行参数列；勿只问一两个字段。
2. 时区不明时运行 `google-timezones`，或用业务语言给出常用时区表（勿贴完整 CLI）。
3. 用户确认资料齐全后执行 `open-account google`（命令留在工具侧，勿把完整命令块贴进对话）。
4. `account-history -m Google` 轮询；向用户只说进度结论。
5. 通过后引导充值（`finance.md`）。

---

## 五、命令速查（Agent 内部）

| 命令                            | 作用       |
| ------------------------------- | ---------- |
| `open-account google-wizard`    | 交互向导   |
| `open-account google-timezones` | 时区列表   |
| `open-account google`           | 非交互提交 |
| `account-history -m Google`     | 审核进度   |

完整参数见 `references/accounts/open-account-by-media.md`。
