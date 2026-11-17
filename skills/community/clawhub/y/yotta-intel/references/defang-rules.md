# defang / refang 规则与共享建议

> 元情 yotta-intel v0.2.1：去活性（defang）写法识别、还原与安全共享指引。

## 1. 为什么要 defang

威胁情报共享时，邮件客户端 / 聊天平台 / 工单系统会把文本中的 URL、邮箱、IP 自动识别为可点击链接或可解析地址：

- 收件人误点恶意链接；
- 平台把 IOC 当普通链接处理、丢失原文；
- 自动化沙箱在共享环节触发外联。

defang（去活性）把 IOC 中的「可识别分隔符」替换成安全写法，让平台不再自动识别，同时人仍然能读懂。

## 2. 引擎识别的 defang 写法（refang 输入）

| 原始 | 常见 defang 写法（引擎都能还原） |
|---|---|
| `.` | `[.]` `(.)` `{.}` `[dot]` `(dot)` `{dot}`（大小写不敏感） |
| `:` | `[:]` `(:)` `{:}` `[colon]` `(colon)` `{colon}` |
| `@` | `[@]` `(@)` `{@}` `[at]` `(at)` `{at}` |
| `/` | `[/]` `(/)` `[\/]` `[\\]` |
| `http` | `hxxp` `hXXp` |
| `https` | `hxxps` `hXXps` |

例：`hxxp://malware[.]example[.]com/loader.exe` → refang → `http://malware.example.com/loader.exe`。

## 3. 引擎输出的统一 defang 形态（defang_value）

引擎输出统一风格，保证同一 IOC 在任何地方 defang 后形态一致：

| 类型 | 原始 | defang |
|---|---|---|
| ipv4 | `203.0.113.5` | `203[.]0[.]113[.]5` |
| ipv6 | `2001:db8::1` | `2001[:]db8[:][:]1` |
| domain | `evil.example.com` | `evil[.]example[.]com` |
| url | `https://evil.example.com/a` | `hxxps://evil[.]example[.]com/a` |
| email | `admin@example.com` | `admin[@]example[.]com` |
| hash | `44d886…2f` | 不变（十六进制不会被自动链接） |
| cve | `CVE-2024-1234` | 不变（不会被自动链接） |

URL 的 defang 会同时处理 host 里的 `@`（userinfo）：`http://user@evil.com/a` →
`hxxp://user[@]evil[.]com/a`。

## 4. 三个子命令怎么配合

- `extract`：提取 + 归一 + 去重 + 输出。每条结果自带 `value`（原始规范形态）与 `defanged`（安全共享形态）。
- `defang`：流式把一段文本中识别到的 IOC 替换为 defang 形态（其余原文保留）——适合「把报告转成可安全粘贴的版本」。
- `refang`：把 defang 文本还原为原始形态——适合「把别人发来的 defang 情报喂给 extract 或其它工具」。

```bash
# 把一份威胁报告转成安全共享版
python3 scripts/yotta_intel.py defang --path report.txt --output safe.txt

# 把安全共享版还原后再提取
python3 scripts/yotta_intel.py refang --path safe.txt | python3 scripts/yotta_intel.py extract --stdin --format json
```

## 5. 共享纪律建议

1. 在邮件 / 群聊 / 工单里共享 IOC 时，优先贴 defang 形态 + 注明「已 defang」。
3. 贴原始形态时，用代码块或等宽字体包起来，降低被自动链接的风险。
3. 不要把 defang 当加密：defang 只是防误点，不是防分析——机器可以一键还原。
4. 哈希与 CVE 无需 defang；不要给它们画蛇添足加括号，避免下游解析出错。
5. 共享 STIX-lite 时（stix-lite-spec.md），pattern 内用原始值（机器可解析），
   人看的备注列用 defang 形态。
