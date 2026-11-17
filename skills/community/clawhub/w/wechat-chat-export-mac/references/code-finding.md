# CODE（kvcomm_code）获取方法

## 这是什么

微信图片解密的账号码，参与两处：

```
AES_KEY=*** + WXID)[:16]
XOR        = int(CODE) & 0xFF
```

- 形态：**10 位纯数字**（本实战值 `1234567890`）
- 字段名：`kvcomm_code`（微信内部叫法）
- 与微信 UIN（uin）同源：10 位自增整数，2015 前后注册的号在 10^9 量级

## 为什么它是断点

明文 grep 本机**搜不到** —— 已实测这些位置都**没有**明文：

| 位置 | 结果 |
|---|---|
| `xwechat_files/<wxid>/config/`（login_config 等） | ❌ 加密 |
| `xwechat_files/all_users/config/` | ❌ 加密 |
| `xwechat_files/<wxid>/db_storage/`（SQLCipher） | ❌ 加密 |
| `Data/Library/Preferences/*.plist` | ❌ 没有 |
| `Library/Group Containers/5A4RE8SF68.com.tencent.xinWeChat` | ❌ 没有 |
| 整个 xwechat_files 全文 grep | ⏱ 超时（几十万 .dat），且命中 0 |

## 三条获取途径（按可行性排序）

### 途径 A：Windows 微信（最成熟，推荐）
同一个微信号如果在 Windows 登录过：

```
reg query "HKCU\SOFTWARE\Tencent\WeChat" /v uin
```

或从 `文档\WeChat Files\<wxid>\` 附近的配置里读。Windows 侧 uin 提取有大量成熟开源实现（WeChatMsg 等），拿**同一个账号**的 uin 即可当 CODE 用（本实战 CODE 即从 Windows 侧样例反向验证吻合）。

### 途径 B：Mac 加密配置逆向（未完成，需另行研究）
`login_config` / `global_config` / `file_config` 是微信自己的分块加密，**另有解密 key**，比图片的 V2 更麻烦。`db_storage/*.db` 是 SQLCipher，取库密钥需 lldb 断点 + 重签名 + 重启微信（动静大，本次没做）。

### 途径 C：拿到候选后验证（配套工具，必做）
不管 CODE 从哪来，**用 `wx_probe.py` 验证**：

```bash
python3 wx_probe.py --code <候选CODE> --wxid <WXID> --dat <任一.dat>
```

- 输出 `✅ magic=wxgf/jpg` → **CODE 和 WXID 都对**，可批量解密
- 输出 `❌ magic未知` → CODE 或 WXID 不对（XOR 只由 CODE 低 8 位决定，先核对 WXID）

> 本实战：`--code 1234567890 --wxid wxid_abc123def456` → `KEY=<md5结果16位> XOR=0x48`，full 出 `wxgf`、`_t` 出 `jpg` ✅

## 快速自检顺序

```bash
python3 wx_locate.py                 # 1) 拿 wxid（自动去后缀）+ 会话 hash
python3 wx_probe.py --code ... --wxid ... --dat ...   # 2) 验 CODE/WXID
python3 wx_decrypt.py ...            # 3) 批量解密
python3 wx_verify.py ...             # 4) 验收缺口=0
```
