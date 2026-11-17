# IOC 类型与判定规则（ioc-spec）

> 元情 yotta-intel v0.2.1 内部规范：七类 IOC 的提取 / 归一 / 误报控制规则。
> 本文件是引擎行为的权威说明；SKILL.md 只放入口，细节在这里。

## 1. 支持的类型

| 类型 key | 中文 | 示例 | STIX 对象 |
|---|---|---|---|
| `ipv4` | IPv4 地址 | `203.0.113.5` | `ipv4-addr` |
| `ipv6` | IPv6 地址 | `2001:db8::1` | `ipv6-addr` |
| `domain` | 域名（FQDN） | `evil.example.com` | `domain-name` |
| `url` | URL | `http://evil.example.com/a` | `url` |
| `email` | 邮箱 | `admin@example.com` | `email-addr` |
| `hash` | 哈希（MD5/SHA1/SHA256/SHA512） | `44d886…2f` | `file:hashes` |
| `cve` | CVE 编号 | `CVE-2024-1234` | `vulnerability` |

## 2. 提取流程

1. **refang 预处理**：先识别并还原 defang 写法（`hxxp`、`[.]`、`(.)`、`[dot]`、`[:]`、`[@]`、`[/]`），
   让 defang 文本与原始文本走同一套提取逻辑；还原只替换分隔符，不改变行结构（行号可追溯）。
2. **逐行提取**：对每一行跑类型正则 + 校验函数，输出 `(start, end, type, canonical)`。
3. **归一化**：每种类型转成唯一的规范形态（见 §3）。
4. **去重计数**：以 `(type, canonical)` 为键合并，记录 `count`（出现次数）、`first_line`（首次行号）与
   `snippet`（首次出现的整行上下文）。

## 3. 归一化规则

| 类型 | 规则 |
|---|---|
| ipv4 | 用 `ipaddress.IPv4Address` 校验并规范化；前导零（如 `010.0.0.1`）归一为 `10.0.0.1`；非法八位组（如 `999.1.1.1`）剔除 |
| ipv6 | 用 `ipaddress.IPv6Address` 校验；输出压缩写法（如 `2001:0db8::1` → `2001:db8::1`）；IPv4-mapped（`::ffff:192.168.1.1`）输出规范十六进制 `::ffff:c0a8:101` |
| domain | 小写；去尾点（`example.com.` → `example.com`）；IDN 转 punycode（`例子.测试` → `xn--fsqu00a.xn--0zwm56d`） |
| url | scheme/host 小写；host 做 IDN；去默认端口（http:80 / https:443 / ftp:21）；去 fragment（`#…` 不发给服务器）；保留 userinfo、path、query |
| email | 小写；域名段做 IDN；要求域名段合法 |
| hash | 十六进制小写；仅接受 32/40/64/128 位（MD5/SHA1/SHA256/SHA512） |
| cve | 统一大写 `CVE-YYYY-NNNN` |

## 4. 误报控制

- **域名 TLD 白名单**：`valid_domain()` 只接受内置 TLD 集合（常见 gTLD + 主流新 gTLD + 全部 ISO 3166-1 ccTLD）内
  的末段，或 `xn--` 开头的 IDN TLD；`badexample.zzz` 这类不存在的 TLD 不会误报。
- **文件名过滤**：与常见文件扩展名重叠的 TLD（`md`/`py`/`sh`/`js`/`ts`/`json`/`log`/`png`/`pdf`…）在
  **二段域名**命中时按文件名处理（`README.md`、`test.py` 不算域名）；三段及以上（如 `cdn.evil.md`）仍按域名。
- **数字末段**：`1.2.3.44` 的末段 `44` 不是合法 TLD → 不算域名（由 IPv4 提取接管）。
- **单标签**：`localhost` 等无点名称不算域名。
- **邮箱内嵌域名**：`admin@example.com` 只提 email，`example.com` 不会被重复提为 domain。
- **URL 标点**：URL 正则排除中文/全角标点（`，。！？；：、（）【】《》`），并去掉尾部 ASCII 标点
  （`http://a.com/a.` → `http://a.com/a`）。
- **哈希**：只接受连续的 32/40/64/128 位十六进制串；UUID（带连字符）与非常规长度（如 48 位）不匹配。
- **IPv6**：`ipaddress` 严格校验；`namespace::method` 里的 `::` 因前邻单词字符不会误报为 IPv6。

## 5. 已知取舍

- 二段 `x.md` 这类「真域名 vs 文件名」无法仅凭文本区分，本引擎按文件名处理（降低常见误报），
  需要时可在结果里人工放行。
- 域名不去 `www.` 前缀、不拆注册域（eTLD+1），去重键 = 完整 FQDN；同一域名的不同子域是不同 IOC。
- URL 与其中包含的 IP / 域名会同时输出（`http://1.2.3.4/x` 同时有 url 与 ipv4），便于下游按需取用。
- defang 流式输出（`defang` 子命令）只替换识别为 IOC 的部分，其余文本原样保留；非 IOC 的零散 `[.]` 会被
  refang 归一为 `.`（见 defang-rules.md）。

## 6. 边界与红线

- 纯本地离线：不联网查证、不下载样本、不主动扫描任何系统；只做文本提取与规范化。
- 提取结果只是「候选指标」，是否恶意需人工 / 其他情报源核实；本引擎不给恶意定性。
- 仅用于已获授权 / 自有资产 / 教学环境的安全分析。
