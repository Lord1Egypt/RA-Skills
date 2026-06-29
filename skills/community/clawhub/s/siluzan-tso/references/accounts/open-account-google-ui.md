## 一、开户流程（五步语义）

| 步骤 | 含义       | CLI / Skill                                                          |
| ---- | ---------- | -------------------------------------------------------------------- |
| ①    | 准备资料   | 向用户说明清单；无法代替用户准备资质                                 |
| ②    | 填写并提交 | `open-account google-wizard`（TTY）或 `open-account google`          |
| ③    | 等待审核   | `account-history -m Google`                                          |
| ④    | 审核通过   | 同上                                                                 |
| ⑤    | 充值激活   | **必须网页**；`config show` → `webUrl` + 充值路径（见 `finance.md`） |

美元账户最低充值约 **100 USD**，人民币约 **700 CNY**（以平台为准）。

---

## 二、非交互提交字段

| 字段                 | CLI 选项                                            |
| -------------------- | --------------------------------------------------- |
| 公司名称             | `--company`                                         |
| 推广网址             | `--promotion-link`（可只写域名，CLI 补协议）        |
| 推广类型 B2B/B2C/APP | `--promotion-type`：`b2b` \| `b2c` \| `app`         |
| 行业（可选）         | `--industry1` / `--industry2`                       |
| 账户名称             | `--account-name`                                    |
| 币种 CNY/USD         | `--currency`                                        |
| 时区 IANA            | `--timezone`；列表：`open-account google-timezones` |
| 开户数量 1～3        | `--counts`                                          |
| 邀请邮箱             | `--invite-email`                                    |

**币种默认时区**：CNY → `Asia/Shanghai`；USD（或其它非 CNY）→ `Asia/Hong_Kong`。其它时区从 `google-timezones` 取 **Code** 列。

提交时按 `--company` 自动查找/创建广告主组并拿 `magKey`，**无需**手动填 magKey。

---

## 三、推荐用法

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

常用时区：`Asia/Shanghai`、`Asia/Hong_Kong`、`America/New_York`、`America/Los_Angeles`、`Europe/London`。完整列表：`open-account google-timezones [--keyword <关键词>]`

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

1. **首次回复**：向用户输出 Google **全部必填项**（见 § 二表格；与 `open-account-by-media.md` § 全平台总览一致），含 CLI 选项名与枚举，再请用户逐项提供；勿只问一两个字段。
2. 时区不明时运行 `google-timezones` 或给出常用时区表。
3. 用户确认资料齐全后执行 `open-account google`。
4. `account-history -m Google` 轮询。
5. 通过后引导充值（`finance.md`）。

---

## 五、命令速查

| 命令                            | 作用       |
| ------------------------------- | ---------- |
| `open-account google-wizard`    | 交互向导   |
| `open-account google-timezones` | 时区列表   |
| `open-account google`           | 非交互提交 |
| `account-history -m Google`     | 审核进度   |

完整参数见 `references/accounts/accounts.md` → **open-account**。
