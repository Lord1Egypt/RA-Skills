# 工具速查对照表

## 调试工具

| 工具 | 平台 | 核心命令 | 特色 |
|------|------|---------|------|
| **GDB + GEF** | Linux ELF | `gdb -q ./binary` | `checksec`/`canary`/`vmmap` |
| **pwndbg** | Linux ELF | `./setup.sh` | 自动显示寄存器/栈/反汇编 |
| **x64dbg** | Windows PE | 图形界面 | 图形化断点/内存查看 |
| **IDA Pro** | 跨平台 | `start.ps1` + `open.ps1` | Hex-Rays 反编译、72 MCP 工具 |
| **radare2** | 跨平台 | `r2 -A ./binary` | 命令行逆向框架 |
| **gdbserver** | 远程 | `gdbserver --multi 0.0.0.0:23947` | 远程调试嵌入式 |

## 反编译工具

| 工具 | 许可 | 特色 |
|------|------|------|
| **Ghidra** | 免费开源 | C 伪代码质量高、脚本 API |
| **IDA Pro** | 商业 | Hex-Rays、插件生态、远程调试 |
| **Binary Ninja** | 商业 | API 友好、自动化分析 |
| **objdump** | 免费 | 快速反汇编、符号表 |

## 利用开发框架

| 工具 | 用途 | 关键命令 |
|------|------|---------|
| **pwntools** | Python exploit | `process()`/`remote()`/`ELF()`/`ROP()` |
| **ROPgadget** | ROP gadget 搜索 | `--binary ./bin --only "pop\|ret"` |
| **ropper** | gadget + chain | `--file ./bin --search "pop rdi"` |
| **one_gadget** | libc one-shot | `/lib/x86_64-linux-gnu/libc.so.6` |
| **msfvenom** | shellcode | `-p linux/x64/shell_reverse_tcp` |

## 静态分析工具

| 工具 | 用途 | 关键命令 |
|------|------|---------|
| **CodeQL** | 语义漏洞查询 | `codeql database create` |
| **Semgrep** | 结构化规则 | `semgrep --config rules.yaml` |
| **Coccinelle** | 内核语义 patch | `spatch --sp-file rules.cocci` |
| **grep** | 快速关键词 | `grep -rn "pattern" ./` |

## Fuzzing 工具

| 工具 | 目标 | 特点 |
|------|------|------|
| **syzkaller** | Linux 内核 | 系统性 Fuzzing，覆盖所有子系统 |
| **trinity** | Linux 系统调用 | 多架构支持，快速生成用例 |
| **libfuzzer** | LLVM 组件 | 集成在编译器中，cov 导向 |
| **AFL** | 用户态程序 | 遗传算法，fork server |

## 动态追踪工具

| 工具 | 用途 | 关键命令 |
|------|------|---------|
| **strace** | 系统调用 | `strace -f ./binary` |
| **ltrace** | 库函数 | `ltrace -e strcmp ./binary` |
| **Frida** | 动态插桩 | `frida -f ./binary` |
| **valgrind** | 内存错误 | `valgrind --tool=memcheck ./binary` |
| **pahole** | 结构体分析 | `pahole vmlinux` |

## 漏洞查询来源

| 来源 | 内容 | URL |
|------|------|-----|
| **NVD** | CVSS/CWE/版本 | nvd.nist.gov |
| **MITRE** | CVE 描述/状态 | cve.mitre.org |
| **GitHub Advisory** | 开源组件漏洞 | github.com/advisories |
| **CISA KEV** | 已知被利用漏洞 | cisa.gov/kev |
| **Exploit-DB** | PoC/利用代码 | exploit-db.com |
| **CNNVD** | 中文漏洞库 | cnnvd.org.cn |
| **CNVD** | 中文漏洞库 | cnvd.org.cn |
| **AVD** | 阿里云漏洞库 | avd.aliyun.com |

## 内核子系统攻击面

| 子系统 | 入口点 | 高风险操作 |
|--------|--------|---------|
| **io_uring** | `io_uring_setup/enter/register` | ring mmap/fixed buffer/越界 |
| **Netfilter** | `nf_register_hook/nf_tables_newrule` | nft_expr 整数溢出 |
| **SMB/CIFS** | `smb2_read/write/negotiate` | pdu_length 边界 |
| **OverlayFS** | `overlayfs_rename/getattr` | upper/lower 层穿越 |
| **BPF** | `bpf(2)/bpf_prog_load` | 验证器绕过/指针追踪 |
| **TLS/XFRM** | `crypto_aead_*` | AEAD 复制失败 |
| **Ext4** | `ext4_ext_map_blocks` | extent 越界 |
| **USB/HID** | `hid_submit_ctrl/usb_set_configuration` | descriptor 越界 |

## CVE 根因模式

| 模式 | 典型特征 | 检测关键词 |
|------|---------|-----------|
| **aead_copy_fail** | in-place 加密复制失败 | `src == dst`、`crypto_aead_encrypt` |
| **overlayfs_priv** | upper/lower 层权限绕过 | `ovl_rename`、`ovl_path_real` |
| **io_uring_ring** | ring buffer mmap 越界 | `mmap.*ring`、`io_buffer_register` |
| **netfilter_overflow** | nft_expr shift 溢出 | `shift << 32`、`nft_set_elem` |
| **smb_boundary** | pdu_length 与实际不符 | `pdu_length == data_len + header` |
| **bpf_sandbox** | 验证器指针类型绕过 | `check_ptr_alignment`、`PTR_INVALID` |
| **ext4_overflow** | extent 块越界 | `ext4_ext_map_blocks` + `len > EXT_MAX_BLOCK` |
| **usb_hid** | descriptor len 未校验 | `hid_parse` + `report.*len` |

## 编译保护选项

| 选项 | 作用 | 测试关闭 |
|------|------|---------|
| `-fstack-protector` | Stack Canary | `-fno-stack-protector` |
| `-D_FORTIFY_SOURCE` | Fortify Source | `-D_FORTIFY_SOURCE=0` |
| `-z relro` | RELRO | `-z norelro` |
| `-z execstack` | NX | `-z execstack` |
| `-no-pie` | PIE | （默认开启需关闭） |

## IDA Pro MCP 工具分类（72 个）

| 类别 | 工具数 | 工具列表 | 用途 |
|------|--------|---------|------|
| 概况分析 | 4 | `survey_binary`, `list_funcs`, `list_globals`, `entity_query` | 快速摸底、函数/变量列表 |
| 反编译 | 4 | `decompile`, `disasm`, `analyze_function`, `func_profile` | 伪代码、汇编、综合分析 |
| 交叉引用 | 5 | `xrefs_to`, `xref_query`, `callees`, `callgraph`, `trace_data_flow` | 引用追踪、调用图、数据流 |
| 搜索 | 4 | `find_regex`, `search_text`, `find_bytes`, `find` | 字符串/字节/正则搜索 |
| 内存数据 | 6 | `get_bytes`, `get_string`, `get_int`, `get_global_value`, `read_struct`, `search_structs` | 读原始字节、结构体、变量值 |
| 修改操作 | 8 | `set_comments`, `append_comments`, `rename`, `patch_asm`, `patch`, `define_func`, `undefine`, `define_code` | 注释、重命名、Patch |
| 类型系统 | 5 | `declare_type`, `set_type`, `infer_types`, `type_query`, `type_inspect` | 结构体/枚举声明、类型推断 |
| 栈帧 | 3 | `stack_frame`, `declare_stack`, `delete_stack` | 栈变量查看/声明/删除 |
| 签名 | 3 | `make_signature`, `make_signature_for_function`, `find_xref_signatures` | 字节签名生成 |
| 会话管理 | 6 | `idalib_list`, `idalib_current`, `idalib_switch`, `idalib_close`, `idalib_save`, `idalib_health` | session 管理 |
| 其他 | 6 | `int_convert`, `export_funcs`, `py_eval`, `server_health`, `server_warmup`, `idalib_open` | 进制转换、导出、Python执行 |
| 调试器 | 1 | `open_file` | GUI 中打开文件（需 `?ext=dbg`） |

**总计：72 个 MCP 工具**

### 重要工具详解

| 工具 | 使用场景 |
|------|---------|
| `idapro_int_convert` | **必须用这个**，不要自己算进制！进制转换 |
| `idapro_trace_data_flow` | 漏洞利用路径追踪，前向/后向数据流 |
| `idapro_declare_type` | 声明结构体用于解析复杂数据结构（如网络协议、文件格式） |
| `idapro_search_structs` | 搜索已定义结构体，快速定位 `sockaddr`、`FILE` 等 |
| `idapro_server_warmup` | 预热字符串缓存和 Hex-Rays 反编译器，提升响应速度 |