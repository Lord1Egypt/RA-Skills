# 元鉴静态初筛规范（triage-spec）

本文档描述元鉴（yotta-triage）v0.1.1 的静态分析项、判定口径与已知取舍。
所有分析均为**纯静态**：不反混淆、不解包、不动态执行（红线）。

## 1. 输入与边界

- 输入：单个文件，或目录（--recursive 递归子目录）。
- 文件哈希流式计算（MD5/SHA1/SHA256），大文件不整体读入内存。
- 特征分析窗口 = 文件前 16 MiB（MAX_ANALYZE_BYTES）；超出部分只参与哈希，不参与熵 / 字符串 / 头解析。
- 超过 --max-file-mb（默认 256 MB）的文件跳过并记入报告 summary.errors。

## 2. 类型识别（魔数表）

按顺序匹配文件头：

| 魔数 | kind | 说明 |
|---|---|---|
| MZ | pe | DOS/PE 可执行 |
| 0x7F 45 4C 46 | elf | ELF 可执行 |
| CF FA ED FE / CE FA ED FE / FE ED FA CE… | macho | Mach-O |
| CA FE BA BE | macho | Mach-O fat / Java class（需进一步区分） |
| 25 50 44 46 | pdf | PDF |
| 50 4B 03 04 / 50 4B 05 06 | zip | ZIP |
| 1F 8B | gzip | gzip |
| 37 7A BC AF 27 1C | 7z | 7-Zip |
| 52 61 72 21 | rar | RAR |
| D0 CF 11 E0 A1 B1 1A E1 | ole | OLE2/CFB（Office/MSI） |
| 89 50 4E 47 / FF D8 FF / 47 49 46 38 | image | PNG / JPEG / GIF |
| 00 00 01 00 | icon | Windows ICO/CUR |
| 03 F3 0D 0A | pyc | Python 字节码 |
| 1A 2B 3C 4D | class | Java class（旧魔数） |

- 未命中魔数时：前 4096 字节可打印比例 ≥ 0.85 → text / script；shebang（#!）→ script。
- 否则再尝试整段严格 UTF-8 解码 → text（utf-8）（覆盖中文等非 ASCII 文本）。
- 其余 → data / unknown。

## 3. 熵

- 整体 Shannon 熵（0..8），基于分析窗口。
- PE 区段熵：对每个区段的 raw 数据（PointerToRawData + SizeOfRawData）单独计算。
- 判定阈值：≥5.5 提示；≥6.5 偏高（常见于加密 / 压缩载荷）；≥7.5 疑似强加密 / 加壳。

## 4. 字符串提取与分类

- 可打印字符串：ASCII（0x20-0x7E）连续段 + UTF-16LE（偶偏移可打印 + 奇偏移 0x00）连续段。
- 默认最小长度 4（--strings-min），每文件上限 500 条（--strings-limit）。
- `--no-strings` 时 `strings.count=0` 且 `strings.skipped=true`；文本报告显示“字符串: 已跳过”，避免与真实零字符串混淆。
- 分类：
  - URL：http / https / ftp 开头，去尾部标点（.,;:!?)]}> 与引号）。
  - 域名：多段标签 + 末段 ≥2 字母；**非 TLD 后缀黑名单**（exe/dll/py/js/txt/md/zip/png…）过滤，避免 payload.exe / a.exe 误判。
  - IP：IPv4 四段 0-255 校验。
  - 邮箱：标准 user@domain.tld。
  - 可疑命令：关键字正则（powershell -enc / certutil -urlcache / bitsadmin /transfer / regsvr32 /s /i / mshta / rundll32 / schtasks /create / cmd /c / iex / Invoke-WebRequest / curl / wget / downloadstring / base64 -d / Assembly.Load / wscript / cscript / -windowstyle 等）。
  - 路径：Windows 盘符路径、UNC、%ENV% 路径、/etc /tmp /var /usr /bin /dev、Windows\System32、AppData、Users 等。
  - base64：≥60 字符的 base64 字符集连续段。

## 5. PE 头解析字段

| 字段 | 说明 |
|---|---|
| machine | 机器类型（x86 / x86-64 / ARM / ARM64 / IA64 / RISC-V…） |
| timestamp | 编译时间戳（0、早于 1990、晚于 2100 → 异常提示） |
| optional_magic | PE32 / PE32+ |
| subsystem | NATIVE / WINDOWS_GUI / WINDOWS_CUI 等 |
| sections_detail | 区段名、virtual/raw 大小、executable/writable/code 标志、区段熵 |
| suspicious_sections | 加壳区段名（.upx0/.packed/.aspack/.nsp0/.petite/.mpress1/.enigma1/.themida/.vmp0…） |
| rwx_sections | 可写可执行区段（0x20000000|0x80000000） |
| high_entropy_sections | 熵 ≥ 7.0 的区段 |

## 6. ELF 头解析字段

| 字段 | 说明 |
|---|---|
| class / endian | ELF32 / ELF64；little / big |
| type | NONE / REL / EXEC / DYN / CORE |
| machine | x86 / x86-64 / ARM / ARM64 / RISC-V 等 |
| entry | 入口地址 |
| segments | 程序头（type / flags / filesz / memsz） |
| rwx_segments | PT_LOAD 且 flags=R|W|X(7) 的段 |
| sections | SHF_WRITE|SHF_EXECINSTR 的可写可执行节 |

## 7. 已知取舍

- 大文件只分析前 16 MiB 窗口（哈希全量）；超大文件可跳过。
- 不做导入表 / 资源 / 数字签名 / 反混淆 / 解包解析（v0.1 范围）。
- Mach-O / Java class 只做魔数识别，不深解析（v0.1 范围）。
- 风险分级为线索提示，不构成恶意结论。
