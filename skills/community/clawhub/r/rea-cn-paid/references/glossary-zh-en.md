# REA-CN 英汉对照表（Glossary · 中英文术语与工具名对照）

> **本文件是 REA 逆向审计助手（国内适配版 / REA-CN）的核心本地化文件之一。**
> 它解决一个致命问题：**纯英文引擎在中文 LLM 环境下，工具名极容易被"翻译"成中文而导致调用失败。**
>
> **⚠️ 黄金铁律（任何调用前必读）：**
> 1. 调用引擎工具时，**工具名（英文名）必须逐字照抄下表「英文原名」一栏**，一字不改、不加空格、不做任何翻译或本地化。
> 2. 下表「中文功能名 / 中文简述」仅用于**给人（分析师 / 中文 LLM 理解语义）看**，绝不能作为 `tool` 参数传给引擎。
> 3. 本表共 **170** 个工具，与引擎运行时自报 `tool_count: 170` 严格一致（已通过源码 `TOOL_CONTRACTS` 编译期枚举交叉验证）。
> 4. 工具名全部小写 + 下划线（`snake_case`）。例如 `open_binary`、`analyze_function`。

---

## 0. 通用术语对照（General Terms）

| 英文术语 | 中文术语 | 说明 |
|---|---|---|
| Reverse Engineering (RE) | 逆向工程 | 从可执行文件/字节码/产物反推其结构与行为 |
| binary | 二进制文件 / 可执行文件 | 泛指 exe、Mach-O、ELF、PE 等原生程序 |
| artifact | 产物 / 工件 | 被分析的原始对象（安装包、固件、归档等），REA 术语 |
| provider | 分析提供方 | 真正干活的后端（Ghidra/Hopper/JADX/JEB/adb 等），引擎是中间件 |
| bridge | 桥接器 | REA 与各 provider 之间的适配程序（如 Hopper bridge） |
| MCP (Model Context Protocol) | 模型上下文协议 | 引擎以 MCP 服务器形式暴露工具给 LLM |
| tool / tool_contract | 工具 / 工具契约 | 引擎向 LLM 暴露的每一个可调用的能力 |
| Evidence | 证据 | REA 对每一次观测的结构化、可校验记录（带 SHA-256） |
| snapshot | 分析快照 | 可序列化的中立分析状态，跨会话保存 |
| digest / SHA-256 | 摘要 / 哈希 | 用于完整性校验的内容指纹 |
| decompile | 反编译 | 将机器码/字节码还原为高级语言（伪代码） |
| pseudocode | 伪代码 | 反编译产出（非原始源码） |
| assembly / disassembly | 汇编 / 反汇编 | 指令级文本 |
| Mach-O | Mach-O 格式 | macOS/iOS 原生可执行格式 |
| PE / PE32+ | PE 格式 | Windows 可执行格式 |
| ELF | ELF 格式 | Linux 可执行格式 |
| APK | Android 安装包 | Android 应用包 |
| IPA | iOS 安装包 | Apple 应用归档 |
| DMG | 苹果磁盘镜像 | macOS 磁盘映像 |
| ASAR | ASAR 归档 | Electron 应用资源归档格式 |
| bundle | 应用包 / 捆绑包 | 含多组件的目录（如 .app） |
| DEX / smali | Dalvik 字节码 / smali | Android 编译后格式及其汇编 |
| CFG (Control Flow Graph) | 控制流图 | 函数/程序控制流 |
| IL / CIL | 中间语言 | .NET 公共中间语言 |
| P/Invoke | 平台调用 | 托管代码调用原生 API |
| xrefs (cross references) | 交叉引用 | 某地址被谁引用 / 引用了谁 |
| address | 地址 | 虚拟地址（VA） |
| offset | 文件偏移 | 文件中的物理偏移量 |
| caller / callee | 调用者 / 被调用者 | 函数调用关系两端 |
| thunk | 跳板函数 | 小型转发函数 |
| entitlement | 授权 / 权利 | macOS 代码签名授权项 |
| hardened runtime | 强化运行时 | macOS 安全机制 |
| dylib | 动态库 | macOS 动态链接库 |
| dyld | 动态链接器 | macOS 的动态加载器 |
| COM (DOS COM) | DOS COM 映像 | 早期 DOS 纯二进制格式 |
| firmware | 固件 | 嵌入式设备固件镜像 |
| JADX | JADX 反编译器 | Android DEX/APK 反编译工具 |
| JEB | JEB 反编译器 | 商业多平台反编译器 |
| Ghidra | Ghidra | NSA 开源逆向工具 |
| Hopper | Hopper | macOS 逆向 GUI 工具 |
| IDA | IDA Pro | 商业逆向工具 |
| ADB (Android Debug Bridge) | Android 调试桥 | Android 设备调试命令行 |
| Electron | Electron 框架 | 桌面应用框架 |
| V8 Inspector | V8 检查器 | Node/Electron JS 运行时调试接口 |
| CDP (Chrome DevTools Protocol) | Chrome 开发者工具协议 | 浏览器/Electron 调试协议 |
| WebMCP | WebMCP 协议 | 网页端暴露 MCP 工具的实验协议 |
| resolution / residual unknown | 残差未知 | REA 对无法确定的事实显式标记为未知 |

---

## 1. 官方桥接 / 导航类（official-proxy · 40 个）

> 这组是引擎对 Hopper/Ghidra 等官方能力的"代理"封装，用于地址、符号、过程、注释、字符串等基础导航与编辑。

| 英文原名 | 中文功能名 | 中文简述 |
|---|---|---|
| `annotate_native_function` | 标注函数 | 原子化更新某函数名/入口注释并回读，返回完整函数档案（不改动原始字节） |
| `inspect_native_load_image` | 校验加载映像 | 将已加载的 DOS MZ / COM 映像与不可变目标快照比对，返回原始/修改字节摘要与校验 |
| `inspect_native_data_type` | 检视原生数据类型 | 按数据库类别路径或类型数据地址检视某 recovered 类型的尺寸/对齐/字段/枚举 |
| `inspect_native_instruction` | 检视原生指令 | 检视某精确指令地址：解码字节、助记符、操作数、流与类型引用 |
| `resolve_native_call_targets` | 解析原生调用目标 | 用类型化调用引用解析一个显式静态调用点（不执行代码/不遍历调用图） |
| `address_name` | 地址名称解析 | 解析某代码/数据地址的主要分析名称 |
| `comment` | 读取注释 | 只读读取某地址的常规分析注释（写用 set_comment） |
| `current_address` | 当前光标地址 | 返回 Hopper 当前文档光标地址（仅导航态，复现分析请用品名地址） |
| `current_procedure` | 当前过程 | 返回包含 Hopper 当前光标的已分析过程（非过程名查找） |
| `current_document` | 当前文档 | 返回 REA 的 Hopper 桥当前选中的文档 |
| `goto_address` | 跳转地址 | 移动 Hopper GUI 光标到映射地址并返回观测地址（仅改导航态） |
| `inline_comment` | 读取内联注释 | 只读读取某地址的内联指令注释（写用 set_inline_comment） |
| `list_bookmarks` | 列出书签 | 列出当前文档全部书签（地址+名称对） |
| `list_documents` | 列出文档 | 列出 provider 的程序/文档标识 |
| `list_names` | 列出名称 | 列出全部已分析内存与外部符号（地址/值对） |
| `list_procedures` | 列出过程 | 列出全部已分析过程（地址/值对），供后续函数操作 |
| `list_segments` | 列出段 | 用排他结束地址列出段/内存块及其权限、基址等 |
| `list_strings` | 列出字符串 | 列出 provider 定义的所有字符串对象（地址/值/编码/长度） |
| `next_address` | 下一地址 | 返回显式地址或当前光标之后的下一个已分析对象地址 |
| `prev_address` | 上一地址 | 返回显式地址或当前光标之前的上一已分析对象起始地址 |
| `procedure_address` | 过程地址解析 | 将明确的过程符号名或规范地址解析为其规范入口地址 |
| `procedure_assembly` | 过程汇编 | 返回某过程的汇编（符号名或十六进制地址标识） |
| `procedure_callees` | 过程被调者 | 返回某过程 provider 已解析的直接被调函数 |
| `procedure_callers` | 过程调用者 | 返回某过程 provider 已解析的直接调用者 |
| `procedure_info` | 过程信息 | 返回某过程的入口、签名、局部变量、大小、块数等元数据 |
| `read_function_instructions` | 读取函数指令 | 返回某过程的所有原始指令 |
| `read_bytes` | 读取字节 | 从 provider 规范虚拟地址读取已分析字节（返回精确长度） |
| `address_to_file_offset` | 地址转文件偏移 | 将一个虚拟地址映射回原始非负文件偏移 |
| `procedure_references` | 过程引用 | 返回某过程的所有原始入/出引用边 |
| `procedure_pseudo_code` | 过程伪代码 | 反编译某过程（返回 provider 特定伪代码，可能为空） |
| `resolve_containing_procedure` | 解析所属过程 | 将任意地址（含内部指令/外部入口）解析为其所属已分析过程 |
| `search_procedures` | 搜索过程 | 按字面或正则搜索全部过程名（结果确定且完整） |
| `search_strings` | 搜索字符串 | 按字面或正则搜索全部 provider 定义字符串对象 |
| `set_address_name` | 设置地址名 | 给一个映射地址赋予分析师名称并报告回写是否匹配 |
| `set_addresses_names` | 批量设置地址名 | 一次为多个映射地址赋名，返回逐地址成功/回写布尔 |
| `set_bookmark` | 设置书签 | 在某映射地址创建/替换书签 |
| `set_comment` | 设置注释 | 在某地址写入常规分析注释（空注释即清除） |
| `set_inline_comment` | 设置内联注释 | 在某地址写入内联指令注释（空注释即清除） |
| `unset_bookmark` | 清除书签 | 移除某映射地址的书签 |
| `xrefs` | 交叉引用 | 返回某代码/数据地址的分析引用（连接字符串/全局/选择器/函数） |

---

## 2. 增强分析类（enhanced · 14 个）

> 这组是 REA 在官方能力之上做的高层组合分析（调用图、特征追踪、类型分类等）。

| 英文原名 | 中文功能名 | 中文简述 |
|---|---|---|
| `inspect_native_dispatch_metadata` | 检视原生派发元数据 | 检视绑定 provider 的 Obj-C 类/方法符号与 Swift 符号名清单（符号级证据，非运行时） |
| `get_objc_classes` | 获取 Obj-C 类 | 发现并去重 Objective-C 类标签（可按子串过滤） |
| `get_objc_protocols` | 获取 Obj-C 协议 | 发现并去重 Objective-C 与 Swift 协议标签 |
| `batch_decompile` | 批量反编译 | 并发反编译每个显式过程符号/地址，返回逐项成败与聚合计数 |
| `get_call_graph` | 获取调用图 | 解析符号/地址到规范入口，遍历调用者或被调者关系直到图耗尽 |
| `analyze_swift_types` | 分析 Swift 类型 | 按 mangling 分类 Swift 过程名（类/结构/枚举/协议/扩展） |
| `find_xrefs_to_name` | 按名查找引用 | 将精确名称解析到 provider 名称清单并返回已解析/未解析结果 |
| `binary_overview` | 二进制概览 | 返回原生二进制元数据、各段长度、过程/字符串总数 |
| `analyze_function` | 分析函数 | 为某原生函数构建档案：伪代码、汇编、注释、调用、引用、CFG 块等 |
| `inspect_native_api` | 检视原生 API | 分析某函数的原生 API 边界（跳转表、数据/分支映射、默认目标等） |
| `trace_feature` | 追踪特征 | 将完整字面查询逐字追踪过每个匹配字符串与过程及其 xrefs |
| `trace_call_path` | 追踪调用路径 | 解析起止符号/地址并追踪直接调用者/被调者直到图耗尽或到达目标 |
| `trace_native_ui_action` | 追踪原生 UI 动作 | 追踪一个编译后的 UI 动作经授权连接、Obj-C handler、静态调用引用 |
| `trace_native_values` | 追踪原生值 | 从某原生过程追踪有界静态依赖图（def-use、常量、调用边、参数/返回值绑定） |

---

## 3. 原生分析类（native-provider · 11 个）

> 这组直接检视 Mach-O/PE/ELF 等原生文件结构，多数无需启动 Hopper。

| 英文原名 | 中文功能名 | 中文简述 |
|---|---|---|
| `observe_native_ui` | 观察原生 UI | 按 PID+窗口 ID 观察已运行原生 App，捕获可达性树与截图 |
| `capture_native_ui_scenario` | 捕获原生 UI 场景 | 在指定原生窗口运行点击/滚动/输入等受控步骤，返回前后捕获 |
| `observe_native_calls` | 观察原生调用 | 在 LLDB 下启动目标并记录进入指定函数/Obj-C 方法的每次调用 |
| `inspect_macho` | 检视 Mach-O | 检视 Mach-O 片、加载命令、导入/导出、依赖、段权限（不启动 Hopper） |
| `inspect_signature` | 检视签名 | 检视活动产物的代码签名身份、哈希、授权、entitlements、强化运行时 |
| `inspect_plist` | 检视 plist | 解析 Info.plist（或任意本地 plist），返回规范化 JSON |
| `list_architectures` | 列出架构 | 列出 thin/universal Mach-O 切片（偏移/大小/对齐/来源） |
| `demangle_swift` | Swift 符号还原 | 还原有序 Swift 符号列表（无需 Hopper） |
| `inspect_pe_resources` | 检视 PE 资源 | 检视本地 PE32/PE32+ 的完整资源树（类型/名称/语言/哈希） |
| `inspect_binary_layout` | 检视二进制布局 | 检视本地二进制段/节范围、符号/重定位表、缓解措施推断（Linux ELF） |
| `inspect_recorded_crash` | 检视崩溃记录 | 检视提供的 Linux ELF64 core（段/笔记/线程寄存器/SIGINFO） |

---

## 4. 应用图与重建类（application · 18 个）

> 这组处理"应用图（Application Graph）"、版本比对、JS 语义追踪与重建义务账本。

| 英文原名 | 中文功能名 | 中文简述 |
|---|---|---|
| `inspect_analysis_view` | 检视分析视图 | 检视已完成二进制布局/JS 应用/函数分析的选定视图（不重复分析） |
| `compare_managed_members` | 比对托管成员 | 用唯一性分级比对两条托管成员 Evidence（类型/名称/签名） |
| `verify_managed_native_boundaries` | 校验托管原生边界 | 将托管 P/Invoke 声明与已认证原生导出/函数 Evidence 校验 |
| `import_managed_reconstruction` | 导入托管重建 | 将反编译器产出的托管重建与已认证托管成员 Evidence 关联锁定 |
| `project_managed_application_graph` | 投影托管应用图 | 将托管产物/成员/原生边界 Evidence 投影为中立应用图 |
| `trace_application_feature` | 追踪应用特征 | 将类型化字面种子追踪过 JS 应用图每个可达部分 |
| `trace_javascript_semantics` | 追踪 JS 语义 | 追踪静态 JS 数据流/直接调用返回/闭包关系 |
| `compare_application_versions` | 比对应用版本 | 比对两个 JS 应用图版本（增/删/改/歧义/未知） |
| `compare_source_to_bundle` | 源码比对产物 | 将历史源码图与已认证 JS 应用图 Evidence 比对（改/删/拆/合/复制） |
| `compare_javascript_export_shapes` | 比对 JS 导出形态 | 比对两应用图上同一模块/导出选择器的静态返回形态 |
| `build_reconstruction_obligation_ledger` | 构建重建义务账本 | 从 Evidence 包生成确定性"重建义务账本"（失败即关闭） |
| `evaluate_reconstruction_coverage` | 评估重建覆盖 | 评估证据支撑的重建覆盖是否达到某命名边界 |
| `project_android_application_graph` | 投影 Android 应用图 | 将 APK 清单 Evidence 投影为免执行 Android 应用清单 |
| `project_apple_application_graph` | 投影 Apple 应用图 | 将 IPA/.app/ZIP/DMG 清单 Evidence 投影为免执行 Apple 应用清单 |
| `trace_web_source_location` | 追踪 Web 源码位置 | 经显式配对的 source map 追踪网页脚本中某生成位置对应的源位置 |
| `trace_web_module_imports` | 追踪 Web 模块导入 | 追踪某导出网页脚本的对外原生 ES import/re-export（按 URL 解析） |
| `export_web_scripts` | 导出 Web 脚本 | 将已保留的 JS 字节写出到本地目录并生成摘要校验的清单 |
| `recover_javascript_sources` | 恢复 JS 源码 | 用 Wakaru 将本地 JS 脚本/包恢复为可读模块到新目录 |

---

## 5. 工件 / 固件类（artifact-provider 7 + firmware-provider 2 · 共 9 个）

| 英文原名 | 中文功能名 | 中文简述 |
|---|---|---|
| `inspect_artifact` | 检视工件 | 一次性检视活动归档/应用包的内容寻址图（根/完整性/假设/未探分支） |
| `extract_artifact` | 提取工件 | 将活动归档/应用包的全部常规文件提取到 REA 新建临时目录 |
| `decode_interface_builder` | 解码 IB 归档 | 解码 Apple 应用包内编译后的 storyboard/nib 归档为对象/层级/连接图 |
| `inspect_keyed_archive` | 检视键值归档 | 检视应用包内 Foundation NSKeyedArchiver plist（对象表/类描述/根） |
| `inspect_asset_catalog` | 检视资源目录 | 检视 Apple 应用包内编译 Assets.car 元数据（分页记录/摘要） |
| `trace_dylib_resolution` | 追踪 dylib 解析 | 追踪 dyld 如何为 Mach-O/ app 内各可执行解析每个 dylib 加载（纯头解析） |
| `inspect_evm_interface` | 检视 EVM 接口 | 检视本地 EVM 字节码载体并推断分派选择器/参数/可变性（不执行） |
| `inspect_firmware_regions` | 检视固件区域 | 用 Binwalk 检视本地固件文件的签名候选（偏移/长度/描述/置信度） |
| `extract_firmware` | 提取固件 | 用 Unblob 提取选定固件字节到新目录（返回校验后的子路径/摘要） |

---

## 6. 托管 / .NET 类（managed-provider · 3 个）

| 英文原名 | 中文功能名 | 中文简述 |
|---|---|---|
| `inspect_managed_artifact` | 检视托管产物 | 打开并分类托管 PE/CLI 路径，盘点程序集/模块/引用/资源（不执行） |
| `inspect_managed_members` | 检视托管成员 | 检视 PE/CLI 元数据成员/签名/CIL 哈希/异常区/调用边（不执行） |
| `inspect_managed_native_boundaries` | 检视托管原生边界 | 检视 ModuleRef/ImplMap/PInvoke/CLI 原生头标志（不执行） |

---

## 7. Android / JADX 类（android-provider 5 + apktool-provider 2 · 共 7 个）

| 英文原名 | 中文功能名 | 中文简述 |
|---|---|---|
| `inspect_android_package` | 检视 APK 包 | 检视本地 APK 的包名/SDK/权限/清单/类与资源计数（不执行） |
| `search_android_classes` | 搜索 Android 类 | 按大小写敏感子串搜索 APK 全部反编译类名 |
| `inspect_android_class` | 检视 Android 类 | 检视某 Android 类的解析方法/字段/内部类（含合成成员） |
| `inspect_android_method` | 检视 Android 方法 | 反编译某 Android 方法（smali 兜底，需显式 overload_index） |
| `trace_android_references` | 追踪 Android 引用 | 追踪指向某 Android 类/唯一方法的入向静态引用 |
| `inspect_apktool_client` | 检视 apktool 客户端 | 检视所选 apktool 启动器（命令/来源/版本），不解码 |
| `decode_android_resources` | 解码 Android 资源 | 用 apktool 解码某 APK 资源（AndroidManifest/字符串/语言） |

---

## 8. JEB 类（jeb-provider · 4 个）

| 英文原名 | 中文功能名 | 中文简述 |
|---|---|---|
| `inspect_jeb_client` | 检视 JEB 客户端 | 检视运行中的 JEB MCP 客户端（版本/GUI 或 headless/启动时间） |
| `open_jeb_project` | 打开 JEB 工程 | 从产物文件或现有 .jdb2 打开/创建 JEB 工程，返回单元清单 |
| `list_jeb_units` | 列出 JEB 单元 | 按稳定单元路径与类型列出工程单元（支持通配/分页） |
| `decompile_jeb_item` | JEB 反编译项 | 用 JEB 反编译器将某类型/方法反编译为引擎伪代码 |

---

## 9. ADB 类（adb-provider · 24 个）

> 这组通过 Android Debug Bridge 检视/操控设备。只读为主，少量会修改设备。

| 英文原名 | 中文功能名 | 中文简述 |
|---|---|---|
| `inspect_adb_client` | 检视 ADB 客户端 | 检视所选 adb 客户端（二进制/版本/安装路径），不连设备 |
| `list_adb_devices` | 列出 ADB 设备 | 列出已连接设备（序列号/状态/传输/型号/模拟器或物理） |
| `inspect_adb_device` | 检视 ADB 设备 | 通过 getprop 白名单检视设备构建身份（Android/SDK/补丁/ABI 等） |
| `list_adb_packages` | 列出 ADB 包 | 列出设备已安装包及其 base APK 设备路径（可按三方/系统过滤） |
| `pull_adb_package` | 拉取 ADB 包 | 将某安装包的完整 APK 集（base+split）拉到本地输出目录并 SHA-256 |
| `read_adb_logcat` | 读取 ADB 日志 | 读取设备日志有界转储（logcat -d -t，可按 pid 过滤） |
| `inspect_adb_package` | 检视 ADB 包 | 通过 dumpsys package 检视某安装包（版本/安装时间/权限数等） |
| `pull_adb_file` | 拉取 ADB 文件 | 将某绝对设备路径文件拉到本地并 SHA-256 |
| `push_adb_file` | 推送 ADB 文件 | 将本地文件推送到绝对设备路径（唯一会改设备的 ADB 工具之一） |
| `capture_adb_screen` | 捕获 ADB 截屏 | 将设备屏幕一帧捕获为 PNG 到本地并 SHA-256 |
| `list_adb_processes` | 列出 ADB 进程 | 列出运行进程（用户/pid/ppid/rss/状态/名称） |
| `list_adb_directory` | 列出 ADB 目录 | 列出某绝对设备目录（名称/类型/权限/所有者/大小/符号链接） |
| `list_adb_features` | 列出 ADB 特性 | 列出设备声明的硬件/软件特性（pm list features） |
| `list_adb_services` | 列出 ADB 服务 | 列出设备 binder 服务及其接口（service list） |
| `inspect_adb_display` | 检视 ADB 显示 | 报告设备显示尺寸与密度（wm size / wm density） |
| `inspect_adb_window` | 检视 ADB 窗口 | 报告窗口管理器当前焦点（mCurrentFocus / mFocusedApp） |
| `read_adb_setting` | 读取 ADB 设置 | 读取系统/安全/全局命名空间下某设置值（settings get） |
| `collect_adb_bugreport` | 收集 ADB 错误报告 | 收集设备生成的 bugreport 归档（adb bugreport）到本地并摘要 |
| `resolve_adb_packages` | 解析 ADB 包名 | 按包名大小写不敏感子串查找已安装包（如 whatsapp→com.whatsapp） |
| `install_adb_package` | 安装 ADB 包 | 在设备安装本地 APK（adb install [-r]，会改设备） |
| `uninstall_adb_package` | 卸载 ADB 包 | 从设备卸载某包（含 user 0 数据，会改设备） |
| `start_adb_app` | 启动 ADB 应用 | 通过启动其 launcher activity 启动某已安装应用（会改设备） |
| `start_adb_activity` | 启动 ADB 活动 | 用 am start 启动一个 Intent（动作/数据/组件/最多 16 个 extra） |
| `stop_adb_app` | 停止 ADB 应用 | 强制停止某包的所有进程（am force-stop，会改设备） |

---

## 10. 浏览器 / Web 类（browser-provider · 12 个）

| 英文原名 | 中文功能名 | 中文简述 |
|---|---|---|
| `list_browser_targets` | 列出浏览器目标 | 列出所选本地 CDP 端点暴露的页面目标（可按源过滤） |
| `inspect_web_page` | 检视网页 | 通过 CDP 被动检视某页面（DOM/无障碍/脚本/资源/网络/控制台，不执行 JS） |
| `analyze_web_bundle` | 分析 Web 包 | 捕获某 CDP 页面 JS 源码并静态派生分块图/路由/端点/指纹 |
| `observe_web_session` | 观察 Web 会话 | 在用户操作页面时开启一个有界 CDP 观察窗口，记录导航/生命周期事件 |
| `discover_webmcp_tools` | 发现 WebMCP 工具 | 被动盘点页面注册的所有 WebMCP 工具及其输入结构（不调用） |
| `compare_web_captures` | 比对 Web 捕获 | 比对被动 Web 捕获（inspect_web_page / scenario / webmcp） |
| `capture_web_screenshot` | 捕获 Web 截图 | 捕获某配置页面当前视口为内联 PNG（不滚动/导航/执行 JS） |
| `compare_web_screenshots` | 比对 Web 截图 | 用本地像素指标比对两张 PNG 截图（变更像素比/通道差） |
| `capture_browser_scenario` | 捕获浏览器场景 | 运行受控浏览器场景（启动/连接 CDP、URL、动作、网络/产物选择） |
| `observe_web_execution` | 观察 Web 执行 | 为某 CDP 页面开启有限精确覆盖率窗口（重置计数，不导航/点击） |
| `inspect_web_event_listeners` | 检视 Web 事件监听 | 检视某页面主文档 CSS 匹配上直接注册的事件监听器（不派发/执行） |
| `inspect_web_network_capture` | 检视 Web 网络捕获 | 检视保留的本地 HAR 1.2 / mitmproxy 捕获记录（不连原 URL） |

---

## 11. Electron 类（electron-provider · 5 个）

| 英文原名 | 中文功能名 | 中文简述 |
|---|---|---|
| `list_electron_targets` | 列出 Electron 目标 | 列出所选本地 CDP 端点暴露的每个 Electron file:// 页面目标 |
| `inspect_electron_page` | 检视 Electron 页面 | 被动检视某 Electron 本地文件页面（帧/DOM/资源/脚本，不执行渲染 JS） |
| `analyze_javascript_application` | 分析 JS 应用 | 将本地 ASAR/解包 JS 应用重建为内联应用图（不执行） |
| `reconcile_javascript_runtime` | 协调 JS 运行时 | 将已验证静态 JS 应用图与被动 Web/Electron/V8 Evidence 协调 |
| `capture_electron_scenario` | 捕获 Electron 场景 | REA 自有 Electron 运行，接受点击/等待等动作，返回关联 Evidence |

---

## 12. JS 运行时类（runtime-provider · 2 个）

| 英文原名 | 中文功能名 | 中文简述 |
|---|---|---|
| `list_javascript_runtime_targets` | 列出 JS 运行时目标 | 列出显式本地 V8 Inspector 端点暴露的每个 Node/Electron 目标 |
| `observe_javascript_runtime` | 观察 JS 运行时 | 被动附加某 V8 Inspector 目标，捕获脚本与执行上下文元数据（不插桩） |

---

## 13. 会话 / 证据类（session · 21 个）

> 这组管理"打开目标—分析—保存证据—关闭"的整个生命周期，以及证据/未知/比对工作流。

| 英文原名 | 中文功能名 | 中文简述 |
|---|---|---|
| `open_binary` | 打开二进制 | 校验后打开本地可执行/应用包/归档/JS/源映射/plist/分析库（绑定 provider） |
| `close_binary` | 关闭二进制 | 排空请求、可选写快照、关闭活动目标与全部 provider 资源 |
| `binary_session` | 二进制会话状态 | 报告当前目标/provider/能力/客户端特性/分析/服务器身份状态 |
| `export_evidence_bundle` | 导出证据包 | 将会话确定性 Evidence 包原子写入本地路径（需 overwrite） |
| `import_evidence_bundle` | 导入证据包 | 读取并校验本地 JSON 包后原子合并（仅数据，绝不执行） |
| `capture_process_scenario` | 捕获进程场景 | 在 PTY 下运行某命令并返回进程捕获 Evidence（含未知项） |
| `compare_process_captures` | 比对进程捕获 | 跨终端/交互/生命周期/文件/HTTP/WS 比对两次进程捕获 |
| `compare_artifacts` | 比对工件 | 按逻辑路径/内容身份/元数据/图关系比对两个完整工件清单 |
| `compare_functions` | 比对函数 | 比对两组 analyze_function Evidence（身份/文本/调用/引用/CFG 拓扑） |
| `compare_bundles` | 比对证据包 | 按精确记录成员/一对一观测对/残差未知修订史比对两个 Evidence 包 |
| `find_changed_behavior` | 查找变更行为 | 聚合已验证进程与工件比对 Evidence，产出变更发现 |
| `build_call_path` | 构建调用路径 | 从完整 analyze_function Evidence 构建每条最短直接被调路径 |
| `correlate_static_and_runtime` | 关联静态与运行时 | 评估静态比对发现与运行时比对维度间的显式假设关联 |
| `verify_reconstruction` | 校验重建 | 针对规范 Evidence 包校验有限类型化行为与结构规格 |
| `list_unknowns` | 列出未知项 | 按确定性 ID 顺序列出当前全部残差未知头（可选状态/严重度/域过滤） |
| `record_unknown` | 记录未知项 | 创建一个确定性残差未知与不可变变更 Evidence |
| `update_unknown` | 更新未知项 | 追加一条不可变全状态修订（需精确 expected_revision，防并发覆盖） |
| `verify_unknown_resolution` | 校验未知解决 | 用实时证据重新校验当前残差未知头（权威/置信/环境/修订完整性） |
| `get_evidence_bundle` | 获取证据包 | 默认返回全部保留 Evidence 记录与残差未知（可 summary/过滤） |
| `get_navigation_context` | 获取导航上下文 | 返回所选文档/当前地址/所属过程的中立结果 |
| `inspect_address_context` | 检视地址上下文 | 检视某显式可复现地址的名称/所属过程/常规与内联注释/书签 |

---

## 14. 使用提醒（给中文 LLM）

1. **永远不要**把上表的「中文功能名」当作工具名传给引擎——引擎只认 `snake_case` 英文原名。
2. 当你（中文 LLM）想调用某能力时，先在本表找到语义对应的「英文原名」，再原样填入 `tool` 参数。
3. 若不确定英文原名，回到 `references/tool-invocation-contract.md` 与 `tool-manifest.json`（权威 170 清单）。
4. 引擎所有输出与错误信息均为英文；中文环境下请将结果翻译给用户，但**传给引擎的参数保持英文原样**。
