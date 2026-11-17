# REA-CN 工具调用契约（Tool Invocation Contract）

> **为什么必须有这份契约：** REA 引擎是**纯英文**的，它向 LLM 暴露 170 个 MCP 工具，工具名全部是 `snake_case` 英文（如 `open_binary`、`analyze_function`）。中文 LLM 在中文语境下，极容易把"打开二进制"自动翻译成工具名 `打开二进制` 或 `open-binary`，**这会导致工具调用彻底失败**（引擎只认精确英文名）。
>
> 这份契约是**强制规范**：任何调用 REA 工具的中文 LLM / 用户，**工具名必须逐字照抄 `tool-manifest.json` 中的英文名**。

---

## 1. 铁律（三条，违反即失败）

1. **工具名 = 精确英文 `snake_case` 字符串，一字不改。**
   - ✅ 正确：`open_binary`、`analyze_function`、`list_adb_devices`
   - ❌ 错误：`打开二进制`、`open-binary`、`OpenBinary`、`打开Binary`
2. **工具名与中文语义解耦。** 中文只用于"理解要做什么"，最终填入 `tool` 参数的必须是英文原名。
3. **不知道英文名时，先查表，不猜。**
   - 完整 170 个：`tool-manifest.json`（权威清单）
   - 中文语义→英文映射：`glossary-zh-en.md`（英汉对照表）
   - 仍不确定时，用引擎自带的状态工具 `binary_session` 或 `get_evidence_bundle` 探活，**不要编造工具名**。

---

## 2. 引擎如何注册工具名（技术说明，供排错）

- 引擎在 `dist/server/createServer.js` 中以 `server.registerTool(contract.name, ...)` 注册每个工具。
- `contract.name` 来自 `dist/contracts/toolContracts.js` 导出的 `TOOL_CONTRACTS` 数组（运行时枚举得 **170** 个，与引擎 `tool_count: 170` 一致）。
- 因此：**工具名是编译期固定的，不存在别名、中文名或本地化名。** 任何非 `TOOL_CONTRACTS` 中的字符串都不会被识别。

---

## 3. 典型错误对照（中文 LLM 最容易踩的坑）

| 你想做的事（中文语义） | ❌ 错误工具名 | ✅ 正确工具名 |
|---|---|---|
| 打开一个二进制/APK/文件 | `打开二进制` / `open-binary` | `open_binary` |
| 关闭当前目标 | `关闭二进制` | `close_binary` |
| 反编译某个函数 | `反编译函数` | `analyze_function` 或 `batch_decompile` |
| 查看当前会话状态 | `会话状态` | `binary_session` |
| 列出已连接安卓设备 | `列出设备` | `list_adb_devices` |
| 拉取设备上的 APK | `拉取APK` | `pull_adb_package` |
| 截屏幕 | `截图` | `capture_adb_screen` / `capture_web_screenshot` |
| 搜索字符串 | `搜索字符串` | `search_strings` |
| 查看伪代码 | `伪代码` | `procedure_pseudo_code` |
| 导出证据包 | `导出证据` | `export_evidence_bundle` |
| 查看网页 | `检视网页` | `inspect_web_page` |
| 追踪调用路径 | `调用路径` | `trace_call_path` |
| 查看 Mach-O | `查看MachO` | `inspect_macho` |
| 查看签名 | `查看签名` | `inspect_signature` |

> 规律：**永远不要用中文、不要用连字符 `-`、不要大小写混写、不要在词间加空格。**

---

## 4. 调用参数（input schema）也是英文键

- 每个工具的入参是一个 JSON 对象，**键名同样是英文 `snake_case`**（如 `address`、`document`、`provider_id`、`overwrite`）。
- 参数**值**可以是中文（例如路径、注释文本），但**键**必须英文原样。
- 例（正确）：
  ```json
  { "tool": "set_comment", "address": "0x1000", "comment": "此处为用户登录校验", "document": "main" }
  ```
- 例（错误）：
  ```json
  { "工具": "设置注释", "地址": "0x1000", "备注": "..." }   // 键和工具名都错
  ```

---

## 5. 描述与输出是英文，属正常

- 引擎返回的 `description`（工具说明）与所有 Evidence/错误信息均为**英文**。这是源引擎设计，不是 bug。
- 中文环境下：把英文结果**翻译给用户看**即可，**不要把英文结果改写给引擎当输入**。

---

## 6. 自查清单（每次调用前 5 秒）

- [ ] 工具名是否来自 `tool-manifest.json` / `glossary-zh-en.md` 的「英文原名」栏？
- [ ] 是否全小写 + 下划线、无空格、无连字符、无中文？
- [ ] 参数键名是否英文 `snake_case`？
- [ ] 不确定的工具名是否已查表而非猜测？

> 凡符合以上，调用即可正常执行。本契约与 `glossary-zh-en.md`、`tool-manifest.json` 三者共同保证纯英文引擎在中文环境下稳定运行。
