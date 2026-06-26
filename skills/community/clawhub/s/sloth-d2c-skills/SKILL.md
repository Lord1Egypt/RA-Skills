---
name: sloth-d2c-skills
description: 将Figma设计稿转换为前端组件代码（Design to Code）。通过 `sloth d2c` CLI 获取设计稿数据，分片处理并生成最终代码。当用户提到Figma转代码、设计稿转代码、D2C、design to code、生成页面时使用。
allowed-tools: Bash, Task, Read, Write, Edit, Glob, Grep
disable: false
---

# Figma 设计稿转代码（D2C）

## 前置校验

### 必需参数

| 参数    | 说明           |
| ------- | -------------- |
| fileKey | Figma 文件 Key |
| nodeId  | Figma 节点 ID  |

缺少以上参数时，提示用户提供。

### 可选参数

| 参数      | 默认值  | 使用时机                                                                                                            |
| --------- | ------- | ------------------------------------------------------------------------------------------------------------------- |
| framework | 自动    | 用户明确指定目标框架时传入，取值：`react` / `vue` / `ios-oc` / `ios-swift` / `kuikly` / `taro` / `uniapp` / `hippy` |
| depth     | 自动    | 仅当用户显式要求限制节点树遍历深度时传入，否则不加                                                                  |
| local     | `false` | **默认不要加**。仅当用户明确要求"使用本地缓存"才传入                                                                |
| update    | `false` | 仅当用户明确表示"修改/更新之前生成的代码"时传入；新建代码时一律不传                                                 |
| silent    | `true`  | 默认静默。仅当用户要求交互式配置页面时显式传 `--silent=false`                                                       |

> ⚠️ `local` 与 `update` 都是**显式触发**参数，默认一律不传。不要因为"为了更快"而主动加 `--local`——运行没有缓存会直接失败。

### 环境检查

执行 `sloth --version` 确认 CLI 可用。不可用则跳转[错误排除](#错误排除)。

## 执行流程

```
Task Progress:
- [ ] Step 1: 执行 sloth d2c CLI 生成 chunks
- [ ] Step 2: 并行处理代码片段与聚合
- [ ] Step 3: 生成最终代码并写入文件
```

### Step 1：执行 `sloth d2c` CLI

在工作区根目录运行（Bash）：

```bash
sloth d2c \
  --file-key <fileKey> \
  --node-id <nodeId> \
  [--framework <react|vue|ios-oc|ios-swift|kuikly|taro|uniapp|hippy>] \
  [--depth <n>] \
  [--local] \
  [--update] \
  --silent --json
```

CLI 成功时以 JSON 形式输出到 stdout：

```json
{
  "ok": true,
  "fileKey": "...",
  "nodeId": "...",
  "convertedNodeId": "...",
  "chunksDir": ".sloth/<fileKey>/<convertedNodeId>/chunks"
}
```

- 解析 JSON 得到 `chunksDir` 与 `convertedNodeId`。
- `ok=false` 或非零退出码时跳转[错误排除](#错误排除)。

### Step 2：并行处理代码片段与聚合

以 Step 1 返回的 `chunksDir` 为基础，启动多个 **sloth-d2c-agent** subagent，**并行执行**：

| 任务                 | 提示词路径                       |
| -------------------- | -------------------------------- |
| 代码片段处理（多个） | `{chunksDir}/{index}.md`         |
| 聚合处理             | `{chunksDir}/codeAggregation.md` |

全部 Subagent 完成后进入下一步。

### Step 3：生成最终代码并写入文件

主 Agent 收集第 2 步执行完毕的结果，结合读取 `{chunksDir}/finalGenerate.md` 的内容作为提示词转换代码，写入项目文件中。

## 错误排除

| 错误场景                     | 处理方式                                                                                               |
| ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| `sloth: command not found`   | 执行 `sloth -v`：有版本号则提示配置 PATH；无版本号则执行 `npm install -g sloth-d2c-mcp` 安装           |
| CLI 退出码非 0 / `ok:false`  | 读取 JSON 中的 `error`/`message` 字段并展示给用户                                                      |
| 文件不存在（chunksDir 为空） | 提示用户检查 fileKey 和 nodeId 是否正确，**停止执行**                                                  |
| 超时                         | 建议用户先执行 `sloth server restart` 再重试；或增加 shell 超时配置                                    |
| 403 错误                     | 未配置有效 Figma Token，提示用户执行 `sloth config` 并配置 `mcp.figmaApiKey`，或使用 `--figma-api-key` |
| 404 错误                     | 设计稿未找到，提示用户核实 fileKey 和 nodeId                                                           |
| Node 版本过低                | 检查用户 Node 版本是否 ≥ 18                                                                            |