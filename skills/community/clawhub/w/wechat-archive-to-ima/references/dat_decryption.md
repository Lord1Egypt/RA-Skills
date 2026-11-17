# .dat 解密原理与实测记录

对应脚本：`scripts/wechat_dat_decrypt.py`（独立解密）、`scripts/organize_attachments.py --decrypt`（解密后归档）。

本文件只讲三件事：格式是什么、code 怎么推出来、哪些是硬边界。
所有数字都是在 Windows 微信 4.1.15.13 上跑出来的，不是推算值。

---

## 1. V2 格式

单个 `.dat` 的字节布局：

```
偏移        内容
0x00  6B    固定文件头：07 08 'V' '2' 08 07
0x06  4B    uint32 LE = aes_size   （明文长度，实测恒为 16 的倍数）
0x0A  4B    uint32 LE = xor_size    （尾部异或区长度）
0x0E  1B    保留
0x0F  ...   AES-ECB 密文段（16 字节对齐；磁盘上实际比 aes_size 多一个 16 字节整块）
...         未加密明文段（部分文件没有，长度 = 文件总长 - 0x0F - 密文段 - xor_size）
文件尾 xor_size 字节：逐字节 XOR 混淆区
```

解密三步：

1. **AES-128-ECB** 解密密文段，取前 `aes_size` 字节 —— 这是文件主体。
2. 拼上中间的未加密明文段（多数文件为空）。
3. 尾部 `xor_size` 字节每字节 `^ (code & 0xFF)` 还原。

**密钥**：

```
key = md5( str(code) + wxid ).hexdigest()[:16].encode()   # 16 字节 ASCII = AES-128 密钥
xor = code & 0xFF
```

- `code`：账号私有的一串数字，**实测 8 位（< 1e9）**。
- `wxid`：账号自己的 wxid；账号目录名是 `<账号名>_<hash>` 时，`<账号名>` 就是 wxid 的第一候选。
- 无 IV、无 MAC，所以拿一段 16 字节密文就能当"探针"验证候选密钥：解出来以
  `FF D8 FF`（jpg）/ `89 PNG` / `GIF8` / `RIFF` / `wxgf` / `II*\0` / `BM` 开头即为命中。

解密后按 magic 还原扩展名，实测一个 3898 文件的账号：

| 格式 | 数量 |
|---|---|
| jpg | 2689 |
| wxgf（腾讯动图容器） | 794 |
| png | 415 |
| **合计** | **3898** |

**成功率：3898 / 3898 解密成功，0 失败；PIL 可打开 3104 / 3104（wxgf 794 个 PIL 不认，按设计跳过，不计失败）。**

---

## 2. code 推导原理

搜索空间 = `code × wxid 候选`，但被两条事实砍到可以秒级命中：

1. **xor = code & 0xFF 可以先算出来。**
   图片尾部有固定结束标记（jpg 的 `FF D9`、png 的 `IEND`、gif 的 `00 3B`），
   而尾部是被 XOR 过的：拿尾字节分别异或 0~255，能还原出结束标记的那个值就是 xor。
   多个文件投票即可唯一确定。**这一步把 code 候选空间直接砍到 1/256。**
2. **wxid 候选很少。** 从账号目录名（`<账号名>_<hash>` → 取 `<账号名>`）、目录里出现的
   `wxid_*` 字符串、以及 `--wxid` 显式指定的候选里去重，通常 2~5 个。
3. **剩下的就是暴力**：对每个 `c ≡ xor (mod 256)`、每个 wxid 候选算 key，
   用 3~6 个探针块做 magic 校验；命中后再做整文件复核（解密 + magic + 结束标记），
   排除误报。多进程并行，`--timeout` 到点落盘退出。

拿到 code 之后，`secret_hit.json` 落在 `--out` 下，二次使用直接 `--code <code>`（或
`--key-file`），**跳过暴力，秒出**。

---

## 3. 两个关键坑（不踩这两个，正确密钥也会判成失败）

### 坑 1：探针只能取 `msg/attach/<会话hash>/<YYYY-MM>/Img/*.dat`

`cache/`、`Bubble/` 这类目录下的 `.dat` **不是图片**，解出来不会以图片 magic 开头。
如果把它们混进探针集，**密钥明明是对的也会永远卡在 magic 校验上**，看起来像"跑不出来"。
脚本的取探针顺序是：`Img` 目录优先 → 排除 `cache`/`bubble` → 全账号兜底。

### 坑 2：code 搜索下界必须是 0

`code` 是 8 位量级。如果按"10 位数"的直觉把下界设成 1e9、上界设成 1e10，
**整段区间里根本没有这个 code**，跑满 100% 也是空手（实测第一轮跑完 36% 才反应过来）。
脚本固定 `下界 = 0`、`上界 = 1e10`，覆盖 1~10 位。

### 补充坑：密文段长度不要按 `ceil16(aes_size)` 取

实测 `aes_size` 恒为 16 的倍数，而磁盘上的密文段比 `aes_size` 还多一个 16 字节整块。
按"对齐到 16"去取段长，会在 `aes_size` 恰好是 16 倍数时少取/多取一整块，
轻则明文错位、重则布局校验直接判失败。本脚本的取段逻辑与已验证实现完全一致。

---

## 4. 边界（对用户必须说清）

| 事项 | 结论 |
|---|---|
| .dat 图片解密 | **已支持**，实测 3898/3898 成功、PIL 100% |
| 聊天正文 `db_storage/message_*.db` | **仍然解不开（SQLCipher 4），本 skill 不承诺正文导出** |
| `contact.db` → 备注名映射 | 解不开，需用户指认一次 |
| 微信没下载到本地的图片 | 盘上本来就没有，解不出来也补不了 |
| wxgf 动图 | 能解密，但它是腾讯自研容器，PIL 打不开；原样保留、不计失败 |
| code 超过 10 位 | 不在自动搜索范围，用 `--code` 直接给 |
| 账号目录里没有任何 jpg/png/gif 尾标记 | 反推不出 xor，脚本会明确报错并要求 `--code` / `--wxid` |
| 微信 4.x 以外（3.x / macOS） | 未实测，不覆盖 |
| 源目录 | **全程只读**，产物只写 `--out` |

---

## 5. 用法速查

```bash
# 自动推导（首次）
python scripts/wechat_dat_decrypt.py \
  --account "<账号目录>" \
  --out "<输出目录>" \
  [--wxid <候选>] [--timeout 900]

# 已知 code（二次使用，秒出）
python scripts/wechat_dat_decrypt.py \
  --account "<账号目录>" --out "<输出目录>" --code <已知code>

# 解密 + 归档一把过
python scripts/organize_attachments.py \
  --src "<账号目录>/msg/attach" --dst "<输出目录>" --contact "attach" \
  --decrypt --key-file "<输出目录>/secret_hit.json"
```

产物：

- `<输出目录>/decrypt_report.json` —— 统计报告（不含 code / wxid / 绝对路径）
- `<输出目录>/secret_hit.json` —— 命中的 code + wxid，**本机复用，不要随包外发**

依赖：`pycryptodome`（必需）、`Pillow`（可选，只影响图片体检）。
