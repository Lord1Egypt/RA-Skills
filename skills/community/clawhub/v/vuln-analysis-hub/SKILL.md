---
name: vuln-analysis-hub
description: 聚合漏洞分析技能中心。整合 IDA Pro 逆向、CVE 查询、静态代码分析（CodeQL/Semgrep）、故障根因分析、二进制漏洞利用工具链。当用户需要分析已知 CVE、挖掘未知漏洞、逆向二进制、构建 PoC、分析漏洞链、生成完整漏洞报告时使用此技能。
metadata:
  tags:
    - vuln-analysis
    - cve
    - reverse-engineering
    - exploit
    - binary-analysis
    - static-analysis
    - kernel
  category: security
allowed-tools: Read Write WebSearch WebFetch exec
---

# vuln-analysis-hub — 聚合漏洞分析技能中心

> 整合 IDA Pro 逆向、CVE 查询、静态分析（CodeQL/Semgrep）、故障根因分析、Linux 内核漏洞主动发现、二进制漏洞利用工具链
>
> 单一入口，多能力协同

## 触发词

漏洞分析、CVE、逆向、漏洞挖掘、二进制、漏洞利用、exploit、根因分析、故障分析、PoC、漏洞复现、静态分析、安全审计、CVE 编号查询、内核漏洞扫描、驱动安全审计

---

## 技能架构

本技能由 7 个子能力聚合而成，形成从**已知漏洞查询** → **未知漏洞发现** → **二进制逆向** → **静态审计** → **漏洞利用开发** → **完整报告输出**的完整闭环。

```
用户输入
  │
  ├─ CVE 编号 / 漏洞查询
  │   ├── cve-lookup      （已知 CVE 详情，多源查询）
  │   └── kernel-cve-tracker（Ubuntu USN 批量追踪）
  │
  ├─ 二进制文件（exe/dll/so/elf/macho/apk/sys）
  │   ├── ida-reverse     （IDA Pro 逆向分析，72 MCP 工具）
  │   └── binary-exploitation-tools（二进制利用工具链）
  │
  ├─ 源码/内核/驱动
  │   ├── kernel-vuln-discover（内核漏洞主动发现）
  │   └── trailofbits-security（CodeQL/Semgrep 静态审计）
  │
  └─ 故障/事件描述
      └── internet-failure-analysis-expert（根因分析）

                      报告输出
```

---

## 子技能速查表

| 子技能 | 触发词 | 核心功能 |
|--------|--------|---------|
| **ida-reverse** | 分析二进制、逆向、exe/dll/so | IDA Pro 反编译、72 MCP 工具、7 阶段工作流 |
| **cve-lookup** | CVE-XXXX、漏洞查询、漏洞详情 | NVD/MITRE/GitHub Advisory 多源查询 |
| **kernel-cve-tracker** | 内核 CVE、Ubuntu CVE | Ubuntu USN 批量查询 |
| **kernel-vuln-discover** | 挖漏洞、发现漏洞、内核扫描 | Fuzzer、静态分析、模式扫描、PoC 生成 |
| **trailofbits-security** | CodeQL、Semgrep、静态审计 | 驱动/内核漏洞静态检测 |
| **binary-exploitation-tools** | 利用工具、pwntools、ROP | 调试 + 利用框架 + Shellcode |
| **internet-failure-analysis-expert** | 故障分析、根因分析、事件报告 | 官方报告 + 时间线 + 改进建议 |

---

## 工作流模式

### 模式 A：CVE 深度分析（已知漏洞）

```
用户输入 CVE 编号
    │
    ├── cve-lookup → 多源搜索 → 结构化报告
    │                   │
    │                   └── 包含：描述、CVSS、CWE、PoC、缓解/防御/修复
    │
    └── internet-failure-analysis-expert → 时间线 → 根因 → 改进建议
```

### 模式 B：二进制漏洞挖掘（未知漏洞）

```
用户提供二进制文件（exe/so/dll/apk）
    │
    ├── ida-reverse → 打开 → 7 阶段逆向 → 漏洞定位
    │                   │
    │                   └── 可选：binary-exploitation-tools 辅助
    │
    └── trailofbits-security → 静态分析 → 漏洞报告
```

### 模式 C：Linux 内核漏洞主动发现

```
用户要求扫描内核源码 / 发现新漏洞
    │
    ├── kernel-vuln-discover
    │   ├── Phase 1: 攻击面枚举（子系统入口点）
    │   ├── Phase 2: CVE 模式归纳扫描（8 种已知根因模式）
    │   ├── Phase 3: Fuzzing（syzkaller/trinity）
    │   └── Phase 4: 静态审计（Coccinelle/semgrep）
    │   └── Phase 5: PoC 生成 + 漏洞报告
    │
    └── kernel-cve-tracker → 已有 CVE 批量查询
```

### 模式 D：故障/安全事件根因分析

```
用户提供故障描述（Facebook 宕机、阿里云故障等）
    │
    └── internet-failure-analysis-expert
        ├── 模式 A：CVE 编号
        └── 模式 B：通用故障描述
            ├── 步骤1：获取官方报告
            ├── 步骤2：拆解时间线
            ├── 步骤3：分析导火索 + 连环故障
            ├── 步骤4：识别根本原因（人/组织因素）
            └── 步骤5：技术改进建议
```

---

## IDA Pro 逆向分析 — 完整 7 阶段工作流

> 当用户提供二进制文件（exe/dll/so/elf/macho/apk/sys）时触发

### 阶段 1：启动服务器

```powershell
# 启动 ida-pro-mcp HTTP 服务器（后台静默）
powershell -File "<skill-root>/ida-reverse/scripts/start.ps1"
# 输出：OK:72（72 个工具就绪）或 ERR:timeout
```

### 阶段 2：打开二进制文件

```powershell
# 打开目标文件（自动处理 System32 权限问题）
powershell -File "<skill-root>/ida-reverse/scripts/open.ps1" -Path "C:\path\to\target.exe" -TimeoutSeconds 600

# 输出：
#   OK:文件名:session_id          （成功）
#   OK:guid-sample.exe:session_id （降级到 Temp 副本）
#   ERR:open_timeout_600s         （超时，需手动检查）
```

### 阶段 3：概况分析（必做第一步）

```python
# 快速摸底：函数数、字符串、段、入口点、导入分类
idapro_survey_binary(detail_level="minimal")

# 列出所有函数（分页）
idapro_list_funcs(queries={})

# 列出全局变量
idapro_list_globals(queries={})

# 统一查询：functions/globals/imports/strings/names
idapro_entity_query(kind="functions", filter={})
```

### 阶段 4：反编译与反汇编

```python
# 反编译为伪代码
idapro_decompile(addr=0x401000)

# 反汇编指定行数
idapro_disasm(addr=0x401000, max_instructions=20)

# 综合分析（伪代码+字符串+常量+调用者+被调用者+块）
idapro_analyze_function(addr=0x401000, include_asm=false)

# 函数概要指标
idapro_func_profile(queries={})
```

### 阶段 5：交叉引用与调用关系

```python
# 查谁引用了目标地址
idapro_xrefs_to(addrs=[0x401000])

# 高级 xref 查询（方向/类型过滤）
idapro_xref_query(addr=0x401000, direction="both")

# 子函数列表
idapro_callees(addrs=[0x401000])

# 调用图（可指定深度）
idapro_callgraph(roots=[0x401000], max_depth=3)

# 数据流追踪（前向/后向）
idapro_trace_data_flow(addr=0x401000, direction="backward", max_depth=5)
```

### 阶段 6：搜索与内存分析

```python
# 正则搜索字符串
idapro_find_regex(pattern=r"password|token|key|secret", limit=50)

# 在反汇编列表中搜文本
idapro_search_text(pattern="strcpy")

# 字节模式搜索（支持 ?? 通配符）
idapro_find_bytes(patterns=["48 8B ?? ?? ?? ?? 00"], limit=20)

# 高级搜索（立即数/字符串/引用）
idapro_find(type="immediate", targets=["0x1000"])

# 读原始字节
idapro_get_bytes(addrs=[0x401000, 0x401020])

# 读字符串
idapro_get_string(addrs=[0x402000])

# 读整数值
idapro_get_int(queries={"addrs": [0x601000], "size": 4})

# 读全局变量值
idapro_get_global_value(queries={"names": ["glibc_version"]})

# 读结构体字段值
idapro_read_struct(queries={"struct_name": "FILE", "addr": 0x601000})

# 搜索结构体
idapro_search_structs(filter={"name": "sockaddr"})
```

### 阶段 7：修改操作与类型系统

```python
# 添加注释（反汇编+反编译双向同步）
idapro_set_comments(items=[{"addr": 0x401000, "text": "漏洞点：strcpy 未校验长度"}])

# 追加注释
idapro_append_comments(items=[{"addr": 0x401000, "text": " → 可利用"}])

# 批量重命名（函数/全局/局部/栈变量）
idapro_rename(batch=[{"old_name": "FUN_00401000", "new_name": "vuln_strcpy"}])

# Patch 汇编指令
idapro_patch_asm(items=[{"addr": 0x401000, "new_asm": "xor rax, rax"}])

# Patch 字节
idapro_patch(patches=[{"addr": 0x401000, "old_bytes": "48 8B 45 00", "new_bytes": "48 31 C0 90"}])

# 定义函数
idapro_define_func(items=[{"addr": 0x401000, "name": "vuln_func"}])

# 取消定义
idapro_undefine(items=[{"addr": 0x401000}])

# 将字节转为代码
idapro_define_code(items=[{"addr": 0x401050}])

# 声明 C 结构体/枚举/联合体
idapro_declare_type(decls=[{"kind": "struct", "name": "payload_hdr", "fields": [{"name": "magic", "type": "uint32_t"}, {"name": "len", "type": "int"}]}])

# 应用类型到函数/全局/局部
idapro_set_type(edits=[{"addr": 0x401000, "type": "int (*)(char*, int)"}])

# 推断类型
idapro_infer_types(addrs=[0x401000])

# 查询已声明类型
idapro_type_query(queries={"name": "payload_hdr"})

# 查看类型详情
idapro_type_inspect(queries={"name": "FILE"})

# 声明栈变量
idapro_declare_stack(items=[{"addr": 0x401000, "name": "buf", "type": "char[256]"}])

# 删除栈变量
idapro_delete_stack(items=[{"addr": 0x401000, "name": "tmp"}])

# 查看栈帧变量
idapro_stack_frame(addrs=[0x401000])
```

### 阶段 8：签名与导出

```python
# 为地址生成唯一字节签名
idapro_make_signature(addrs=[0x401000])

# 为函数生成签名
idapro_make_signature_for_function(addrs=[0x401000])

# 为引用地址的代码生成签名
idapro_find_xref_signatures(addrs=[0x401000])

# 导出函数（json/C header/prototypes）
idapro_export_funcs(addrs=[0x401000], format="json")

# 进制转换（必须用这个，不要自己算！）
idapro_int_convert(inputs=[{"value": "0x41414141", "from": 16, "to": 10}])
```

### 调试器工具（如需动态调试，加 `?ext=dbg`）

```python
# 在 GUI IDA 实例中打开文件
idapro_open_file(file_path="C:\\path\\to\\target.exe")
```

### 会话管理

```python
# 列出所有 session
idapro_idalib_list()

# 获取当前上下文绑定的 session
idapro_idalib_current()

# 切换到其他 session
idapro_idalib_switch(session_id="abcd1234")

# 关闭 session
idapro_idalib_close(session_id="abcd1234")

# 保存数据库
idapro_idalib_save(path="C:\\path\\to\\save.idb")

# 检查 worker 健康状态
idapro_idalib_health(session_id="abcd1234")

# 服务器健康检查
idapro_server_health()

# 预热子系统（字符串缓存、Hex-Rays 等）
idapro_server_warmup()

# 执行 Python 代码
idapro_py_eval(code="print(ida_funcs.get_func(0x401000).flags)")
```

### IDA 已知问题与处理

| 问题 | 解决方案 |
|------|---------|
| `idalib_open` schema 校验报错 | 用 `scripts/open.ps1` 绕 MCP 直调 HTTP API |
| System32 文件无权限 | open.ps1 自动复制到 Temp 再打开 |
| 带自动分析长时间无响应 | 加 `-TimeoutSeconds 600`，非卡死 |
| 旧数据库被锁 | open.ps1 自动降级到 Temp 加 GUID 前缀 |
| IDA GUI 假死 | start.ps1 用 `taskkill /F /T` 杀孤儿进程树 |
| 需要远程调试 | IDA → Debugger → Process options → 配置远程 IP |

---

## IDA Pro 全部 MCP 工具速查（72 个）

### 概况分析（4 个）

| 工具 | 用途 |
|------|------|
| `idapro_survey_binary` | 快速概况：函数数、字符串、段、入口点、导入分类 |
| `idapro_list_funcs` | 列出函数（分页、按名称过滤） |
| `idapro_list_globals` | 列出全局变量 |
| `idapro_entity_query` | 统一查询：functions/globals/imports/strings/names |

### 反编译与反汇编（4 个）

| 工具 | 用途 |
|------|------|
| `idapro_decompile` | 反编译为伪代码 |
| `idapro_disasm` | 反汇编（可指定最大指令数） |
| `idapro_analyze_function` | 综合分析（伪代码+字符串+常量+调用者+被调用者+块） |
| `idapro_func_profile` | 函数概要指标 |

### 交叉引用与调用关系（5 个）

| 工具 | 用途 |
|------|------|
| `idapro_xrefs_to` | 查谁引用目标地址 |
| `idapro_xref_query` | 高级 xref 查询（方向/类型过滤） |
| `idapro_callees` | 子函数列表 |
| `idapro_callgraph` | 调用图（可指定深度） |
| `idapro_trace_data_flow` | 数据流追踪（forward/backward） |

### 搜索（4 个）

| 工具 | 用途 |
|------|------|
| `idapro_find_regex` | 正则搜字符串 |
| `idapro_search_text` | 在反汇编列表中搜文本 |
| `idapro_find_bytes` | 字节模式搜索（支持 ?? 通配符） |
| `idapro_find` | 高级搜索（立即数/字符串/引用） |

### 内存与数据（6 个）

| 工具 | 用途 |
|------|------|
| `idapro_get_bytes` | 读原始字节 |
| `idapro_get_string` | 读字符串 |
| `idapro_get_int` | 读整数值 |
| `idapro_get_global_value` | 读全局变量值 |
| `idapro_read_struct` | 读结构体字段值 |
| `idapro_search_structs` | 搜索结构体 |

### 修改操作（8 个）

| 工具 | 用途 |
|------|------|
| `idapro_set_comments` | 添加注释（反汇编+反编译双向同步） |
| `idapro_append_comments` | 追加注释 |
| `idapro_rename` | 批量重命名（函数/全局/局部/栈变量） |
| `idapro_patch_asm` | Patch 汇编指令 |
| `idapro_patch` | Patch 字节 |
| `idapro_define_func` | 定义函数 |
| `idapro_undefine` | 取消定义 |
| `idapro_define_code` | 将字节转为代码 |

### 类型系统（5 个）

| 工具 | 用途 |
|------|------|
| `idapro_declare_type` | 声明 C 结构体/枚举/联合体 |
| `idapro_set_type` | 应用类型到函数/全局/局部 |
| `idapro_infer_types` | 推断类型 |
| `idapro_type_query` | 查询已声明类型 |
| `idapro_type_inspect` | 查看类型详情 |

### 栈帧（3 个）

| 工具 | 用途 |
|------|------|
| `idapro_stack_frame` | 查看栈帧变量 |
| `idapro_declare_stack` | 声明栈变量 |
| `idapro_delete_stack` | 删除栈变量 |

### 签名（3 个）

| 工具 | 用途 |
|------|------|
| `idapro_make_signature` | 为地址生成唯一字节签名 |
| `idapro_make_signature_for_function` | 为函数生成签名 |
| `idapro_find_xref_signatures` | 为引用地址的代码生成签名 |

### 调试器（1 个）

| 工具 | 用途 |
|------|------|
| `idapro_open_file` | 在 GUI IDA 实例中打开文件（需 `?ext=dbg`） |

### 会话管理（6 个）

| 工具 | 用途 |
|------|------|
| `idapro_idalib_list` | 列出所有 session |
| `idapro_idalib_current` | 获取当前上下文 session |
| `idapro_idalib_switch` | 切换到其他 session |
| `idapro_idalib_close` | 关闭 session |
| `idapro_idalib_save` | 保存数据库 |
| `idapro_idalib_health` | 检查 worker 健康状态 |

### 其他（6 个）

| 工具 | 用途 |
|------|------|
| `idapro_int_convert` | 进制转换（必须用这个，不要自己算！） |
| `idapro_export_funcs` | 导出函数（json/C header/prototypes） |
| `idapro_py_eval` | 在 IDA 上下文执行 Python |
| `idapro_server_health` | 服务器健康检查 |
| `idapro_server_warmup` | 预热子系统（字符串缓存、Hex-Rays 等） |
| `idapro_idalib_open` | ⚠️ 不推荐，直接用 `open.ps1` 脚本 |

---

## 静态分析工具集成（CodeQL/Semgrep）

### CodeQL 漏洞查询命令

```bash
# 创建 CodeQL 数据库
codeql database create /path/to/db --language=cpp --source-root=/path/to/kernel/driver

# 查询特定漏洞模式
codeql database analyze /path/to/db /path/to/rules/buffer-overflow.ql --format=sarif-latest --output=results.sarif

# 常用漏洞规则
# - 缓冲区溢出：codeql query run "semmle-code-cpp/cpp buffer overflow"
# - Use-after-free：codeql query run "semmle-code-cpp/cpp too-small-buffer-size"
# - 整数溢出：codeql query run "semmle-code-cpp/cpp integer-overflow"
```

### Semgrep 规则扫描命令

```bash
# 扫描驱动源码
semgrep --config=rules.yaml /path/to/driver/

# 使用内置规则
semgrep --lang=c --pattern 'strcpy($BUF, $SRC)' /path/to/code/

# 输出 SARIF 格式（可集成到 CI）
semgrep --json --output=sarif.json /path/to/code/
```

### Coccinelle 语义 Patch（Linux 内核）

```bash
# 扫描内核源码
spatch --sp-file /path/to/rules.cocci /path/to/linux/fs/overlayfs/ --very-quiet

# 常用检测规则
# - copy_from_user 未检查返回值
# - kmalloc 大小整数溢出
# - use-after-free（fput 后再次使用）
```

---

## 内核漏洞主动发现 — 完整流程

### Phase 1：攻击面枚举

识别高风险子系统：`io_uring`、`Netfilter`、`SMB`、`OverlayFS`、`BPF`、`TLS/XFRM`

### Phase 2：CVE 模式归纳扫描

使用 `scripts/cve-pattern-scan.sh`（来自 kernel-vuln-discover）进行自动化模式扫描：

```bash
# 扫描所有已知模式
~/.agents/skills/kernel-vuln-discover/scripts/cve-pattern-scan.sh /path/to/kernel-src all

# 扫描特定模式
~/.agents/skills/kernel-vuln-discover/scripts/cve-pattern-scan.sh /path/to/kernel-src io_uring_ring
```

### Phase 3：Fuzzing

| 工具 | 命令 | 说明 |
|------|------|------|
| **syzkaller** | `cd ~/syzkaller && ./bin/syz-manager -config=my.cfg` | 系统性内核 Fuzzing |
| **trinity** | `trinity -l amd64 -c "io_uring_setup"` | 系统调用 Fuzzing |
| **libfuzzer** | `clang -fsanitize=fuzzer target.c` | 组件级 Fuzzing |

### Phase 4：静态审计

结合 `trailofbits-security` 和 `kernel-vuln-discover` 的子系统检查表：

| 子系统 | 关键检查项 | 关键词 |
|--------|---------|--------|
| io_uring | ring mmap 越界、fixed buffer 重叠 | `io_uring_enter`、`mmap.*ring` |
| Netfilter | nft_expr 整数溢出 | `shift << 32`、`nft_set_elem` |
| SMB | pdu_length 边界错误 | `pdu_length == data_len + header` |
| OverlayFS | upper/lower 层权限绕过 | `ovl_rename`、`ovl_path_real` |
| BPF | 验证器指针类型绕过 | `check_ptr_alignment`、`PTR_INVALID` |

### Phase 5：漏洞报告 + PoC

输出：漏洞描述 → 根因分析 → 触发条件 → 概念性 PoC（伪代码）

---

## 工具链速查对照表

### 调试工具

| 工具 | 平台 | 核心命令 | 特色 |
|------|------|---------|------|
| **GDB + GEF** | Linux ELF | `gdb -q ./binary` | `checksec`/`canary`/`vmmap` |
| **pwndbg** | Linux ELF | `./setup.sh` | 自动显示寄存器/栈/反汇编 |
| **x64dbg** | Windows PE | 图形界面 | 图形化断点/内存查看 |
| **IDA Pro** | 跨平台 | `start.ps1` + `open.ps1` | Hex-Rays 反编译、72 MCP 工具 |
| **radare2** | 跨平台 | `r2 -A ./binary` | 命令行逆向框架 |
| **gdbserver** | 远程 | `gdbserver --multi 0.0.0.0:23947` | 远程调试嵌入式 |

### 利用开发框架

| 工具 | 用途 | 关键命令 |
|------|------|---------|
| **pwntools** | Python exploit | `process()`/`remote()`/`ELF()`/`ROP()` |
| **ROPgadget** | ROP gadget 搜索 | `--binary ./bin --only "pop\|ret"` |
| **ropper** | gadget + chain | `--file ./bin --search "pop rdi"` |
| **one_gadget** | libc one-shot | `/lib/x86_64-linux-gnu/libc.so.6` |
| **msfvenom** | shellcode | `-p linux/x64/shell_reverse_tcp` |

### Fuzzing 工具

| 工具 | 目标 | 特点 |
|------|------|------|
| **syzkaller** | Linux 内核 | 系统性 Fuzzing，覆盖所有子系统 |
| **trinity** | Linux 系统调用 | 多架构支持，快速生成用例 |
| **libfuzzer** | LLVM 组件 | 集成在编译器中，cov 导向 |
| **AFL** | 用户态程序 | 遗传算法，fork server |

---

## 输出约束

| 约束 | 说明 |
|------|------|
| 概念性 PoC | 仅伪代码 + 触发序列，不生成可执行攻击代码 |
| 信息来源 | 至少 3 个不同来源，标注可信度 |
| 报告路径 | CVE 报告 → `CVE-Reports/` |
| 免责声明 | PoC 部分必须添加免责说明 |
| 不执行 PoC | 报告生成过程绝不运行任何 PoC 代码 |
| 中文优先 | 中英文混合场景优先中文输出 |

---

## 注意事项

1. **IDA Pro 逆向**：优先用 `scripts/open.ps1` 而非直接调用 `idalib_open`
2. **CVE 查询**：格式校验失败立即停止，不做模糊搜索
3. **PoC 生成**：严格限制为概念性，伪代码 + 自然语言描述
4. **内核漏洞发现**：结合 kernel-cve-tracker 查询已有 CVE，避免重复
5. **故障分析**：以官方报告为主，无官方报告时多源交叉验证