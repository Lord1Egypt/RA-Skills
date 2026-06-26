# 第一步：确定寄件地址 + 寄件人信息

> **触发**：`next_state ∈ {step1-sender-address, step1-sender-contact}`

## 0. 调命令前的前置判断（硬约束）

调 `resolve-address sender` **之前**必须先确认 **`<keyword>` 来源合法**。关键词有 3 类合法来源：

| 用户当轮消息情况 | 合法 `<keyword>` 来源 | 动作 |
|---|---|---|
| 提到**具体地名**（"从中关村寄"/"从望京SOHO寄到 XX"/"在国贸寄"） | 用户原文抽取的地名 | 调 `resolve-address sender "<地名>"` |
| 提到**地址簿别名 / 联系人名**（"从公司寄"/"从家寄"/"妈妈家"/"寄给张三"/"回老地方"） | 用户原文里的别名词 / 联系人名 | 直接调 `resolve-address sender "<别名或联系人>"`；脚本会自动查 [PREFERENCE.md](../../assets/PREFERENCE.md) 地址簿，命中齐全的条目会返回 `decision: address_book_hit` + 保存的地址/联系人 |
| 只说"帮我叫个跑腿"/"帮我寄个东西"等通用诉求，**既没提具体地名也没提任何别名** | — | **禁调 resolve-address**，先开口问用户：「您要从哪里寄出？（小区名 / 楼宇 / 商家名，或直接说"从公司/从家"等已保存地址）」 |
| **只给了联系人字段但完全没提地点**（如"寄件人：王念 18717178957  收件人：王先生 15171448989"） | — | **先调 `prefill-contacts <s_name> <s_phone> <r_name> <r_phone>`** 一次性把 4 个字段（任一空串=未抽到）落盘——这样后续地址确认完即可直接进入第三步询价，避免再问联系人。**再开口问寄件地址**：「您要从哪里寄出？（小区名 / 楼宇 / 商家名，或直接说"从公司/从家"等已保存地址）」。**禁直接调 `resolve-address sender "王念"`**——脚本兜底虽会拦住姓名形态 keyword，但绕路且报错信息粗糙 |
| 提到别名但地址簿里没录入该别名（如用户说"从老地方寄"但地址簿无此条目） | — | 脚本会返回 `decision: empty` 或 SUG 结果；按返回值走即可，不要自己猜老地方是哪里 |

🛑 **严禁**基于以下信息凭空生成 `<keyword>`：
- 模型自身的背景知识 / 常识（例：用户没说"腾讯"就拿"北京腾讯总部"去搜）
- IP 归属地 / 地理位置推测
- 跨会话历史记忆 / 之前的订单（地址簿以外的历史）
- 工具返回值里的占位文案

⚠️ **关于"联系人名作为合法 keyword" 的隐含前提**：仅当用户表达"寄给某人 / 从某人那里寄 / 妈妈家 / 张三家"这类**地址簿查询语义**时才适用。**只在用户消息里出现一个 2-4 字中文人名 ≠ 它就是合法地址 keyword**——若用户只是在交代联系人姓名/手机号字段，应该按上表第 4 行处理，先开口问地址。

💡 **判定口诀**：`<keyword>` 要么是**用户原文里能明确指向地点的词**（地名 / 别名 / "寄给 X / 从 X 那里"中的 X），要么就**先开口问用户**。地址簿查询是脚本的职责，LLM 只要把用户说的词原样传给 `resolve-address` 即可，**不要替地址簿做翻译**（用户说"公司"就传"公司"，不要传"腾讯总部"）。

---

## 0.1 联系人字段乱序预登记（`prefill-contacts`）

用户首条消息**只要带了联系人字段**（姓名 / 手机号），不论顺序、不论是寄件人还是收件人，**第一时间调一次 `prefill-contacts`**：

```bash
python3 ./scripts/tms_delivery.py prefill-contacts "<sender_name>" "<sender_phone>" "<receiver_name>" "<receiver_phone>"
```

- 4 个位置参数都必须传，**没抽到的字段传空串 `""` 跳过**
- 手机号格式非法直接拒绝整条命令（不做部分写入）；姓名不做格式校验
- 已落盘的字段不会被覆盖（修改请走 `commit-contact`）
- 调完后**继续按当前 FSM 状态流转**（多半还停在 `step1-sender-address`，去问寄件地址）

**收益**：脚本 `_compute_current_state` 会自动跳过已填齐的 contact 状态——若 4 个联系人字段在第 0 步就全 prefill 进去，后续两个地址确认完会**直接跳到 `step3-estimate` 询价**，不再单独问联系人。

**典型用法**（用户首条消息："寄件人：王念 18717178957，收件人：王先生 15171448989，帮我寄个文件"）：

```bash
# 1. 预登记（4 个都抽到了）
prefill-contacts "王念" "18717178957" "王先生" "15171448989"
# → next_state: step1-sender-address

# 2. 用户没说地址 → 开口问寄件地址（按上表第 4 行 reply 模版）
```

**反例**：用户只说"寄件人是王念，手机 18717178957"——其他 3 个字段一律传空串：

```bash
prefill-contacts "王念" "18717178957" "" ""
```

---

## 命令

```bash
# 1) 搜地址（keyword 支持具体地名 / 地址簿别名 / 联系人名；脚本先查地址簿再走 POI 搜索）
python3 ./scripts/tms_delivery.py resolve-address sender "<keyword>" "<region?>"

# 2) 用户回复序号后落盘地址
python3 ./scripts/tms_delivery.py pick-address sender <序号>

# 3) 用户给出联系人后一步提交
python3 ./scripts/tms_delivery.py commit-contact sender "<姓名>" "<手机号>"
```

## 分支表：`resolve-address` 的 `decision`

| decision | 动作 |
|---|---|
| `address_book_hit` | 向用户单点确认即可（脚本已给 reply_template） |
| `show_pois` | 按 `reply_template` 展示候选，等用户回序号 → `pick-address` |
| `need_sug_refinement` | 按 `reply_template` 让用户选更精确关键词 → 重调 `resolve-address` |
| `empty` | 请用户更换关键词或补城市 |
| `error` | 按 `hint` 处理（见 [error-handling](../error-handling.md)） |

## 分支表：`pick-address` / `commit-contact` 的 `next_state`

- `contact_hit == true` → 地址簿有默认联系人，向用户确认是否沿用
- `commit-contact valid == false` → 按 `reply_template` 提示重输，**禁止**把非法号传给任何 MCP
- `next_state == "step2-receiver-address"` → 进入 [第二步](./step-2-receiver.md)

## 硬约束

- 用户回复序号后**直接** `pick-address`，**禁止**为"确认经纬度"再调 `resolve-address`
- 若 `pick-address` 返回 `no_cached_pois`，退回 `commit-address` 手动版（见脚本 `hint`）
- 防泄露规则见 [SKILL.md §4](../../SKILL.md#output-leak-firewall)
