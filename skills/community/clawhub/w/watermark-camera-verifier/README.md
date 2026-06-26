# 今日水印相机「照片验真」MCP Server

今日水印相机官方出品，通过 MCP (Model Context Protocol) 协议封装的照片真实性核验工具。

## 功能

- 检测 GPS 位置伪造
- 识别时间戳篡改
- 鉴别水印造假
- 返回拍摄地点、时间及坐标元数据

**适用场景**：保险理赔 · 劳工考勤 · 工程验收 · 法律取证 · 合规审计

---

## 前置条件

- **Node.js >= 18.0.0**（使用原生 fetch，无需额外安装 HTTP 库）
- 今日水印相机 API 凭证（`GroupKey` + `GroupSecret`），从官网 https://docs.xhey.top/docs/trutu-build-api 或电话联系：13141152023 获取

---

## 安装步骤

```bash
# 1. 进入项目目录
cd /path/to/Claude_verify

# 2. 安装依赖
npm install

# 3. 配置凭证
cp .env.example .env
# 编辑 .env，填入您的真实 TRUTU_GROUP_KEY 和 TRUTU_GROUP_SECRET
```

---

## 接入 Claude Code

### 方式一：命令行添加（推荐）

```bash
claude mcp add trutu-photo-verify \
  -e TRUTU_GROUP_KEY=your_group_key \
  -e TRUTU_GROUP_SECRET=your_group_secret \
  -- node /absolute/path/to/Claude_verify/mcp_server.js
```

### 方式二：手动编辑 `~/.claude/settings.json`

```json
{
  "mcpServers": {
    "trutu-photo-verify": {
      "command": "node",
      "args": ["/absolute/path/to/Claude_verify/mcp_server.js"],
      "env": {
        "TRUTU_GROUP_KEY": "your_group_key",
        "TRUTU_GROUP_SECRET": "your_group_secret"
      }
    }
  }
}
```

---

## 测试验证

### 验证工具注册

```bash
TRUTU_GROUP_KEY=xxx TRUTU_GROUP_SECRET=yyy \
  npx @modelcontextprotocol/inspector --cli \
  --transport stdio \
  --command "node /absolute/path/to/mcp_server.js" \
  --method tools/list
```

期望返回包含 `verify_photo_authenticity` 的工具列表。

### 端对端功能测试

```bash
# 调用工具验真
TRUTU_GROUP_KEY=xxx TRUTU_GROUP_SECRET=yyy \
  npx @modelcontextprotocol/inspector --cli \
  --transport stdio \
  --command "node /absolute/path/to/mcp_server.js" \
  --method tools/call \
  --tool-name verify_photo_authenticity \
  --tool-arg 'photo_urls=["https://example.com/photo.jpg"]'
```

### 测试用例清单

| 场景 | 期望结果 |
|------|---------|
| 有效的今日水印相机照片 URL | `verdict: "通过"` + 元数据 |
| 非今日水印相机照片 | `verdict: "未通过"` + 原因说明 |
| 无法访问的 URL | `isError: true` + 可读错误信息 |
| 超过 10 张照片 | 输入校验错误（工具层拒绝） |
| 缺少环境变量 | 启动时打印错误并退出（`process.exit(1)`） |

---

## API 响应码参考

### taskStatus（任务级别）

| 值 | 含义 |
|----|------|
| 1 | 待处理 |
| 2 | 处理中 |
| 5 | 已完成 |
| 6 | 已取消 |

### 照片 status（照片级别）

| 值 | verdict | 含义 |
|----|---------|------|
| 0 | 通过 | 照片真实，水印有效 |
| -1 | 错误 | 分辨率过低 |
| -1001 | 错误 | 网络连接出错或照片损坏 |
| -1002 | 错误 | 程序内部出错 |
| -1003 | 错误 | 未知错误 |
| -2300 | 未通过 | OCR 启动错误 |
| -2301 | 未通过 | 无防伪码 |
| -2302 | 未通过 | OCR 识别错误 |
| -2303 | 未通过 | 防伪码长度错误 |
| -2305 | 未通过 | 非今日水印相机拍摄，或无水印 |
| -2306 | 错误 | 照片 URL 无法访问 |
| -2307 | 错误 | 照片格式不支持 |
| -2308 | 错误 | 照片分辨率过低 |
| 其他负值 | 未通过 | 验真未通过 |

### HTTP 错误码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 401 | 鉴权失败（GroupKey 或 Signature 无效） |
| 4007 | 凭证无效（GroupKey 不存在或已过期） |

---

## 安全注意事项

- 切勿将 `.env` 文件提交至代码仓库，已将其加入 `.gitignore` 建议
- API 密钥按月更新，请留意邮件通知及时更换
- 照片 URL 须保证可公开访问，请勿传入含敏感信息的内部链接

---

## ClawHub 发布清单

### 代码安全
- [ ] 无硬编码密钥（所有凭证通过环境变量传入）
- [ ] `.env` 已加入 `.gitignore`
- [ ] `.env.example` 使用占位符值
- [ ] `package.json` 包含准确的 `name`、`version`、`description`
- [ ] Node.js engine 约束已声明（`>=18.0.0`）
- [ ] 依赖最小化，仅使用可信 npm 包

### SKILL.md 合规
- [ ] frontmatter `name` 与 Skill 调用名一致
- [ ] `description` 清晰描述触发条件（自动调用场景）
- [ ] `tools:` 字段中的工具名与 `mcp_server.js` 注册名一致（`verify_photo_authenticity`）
- [ ] 包含错误场景的 AI 行为指令
- [ ] `version` 字段存在

### MCP Server 功能
- [ ] `node mcp_server.js` 可干净启动（验证 stdio transport）
- [ ] `tools/list` 返回 `verify_photo_authenticity` 及完整 schema
- [ ] 超过 10 张照片时返回描述性错误
- [ ] 鉴权错误（401、4007）返回 `isError: true` 及可操作提示
- [ ] 超时/轮询耗尽返回 `isError: true`（非未捕获异常）
- [ ] 工具注解 `readOnlyHint: true` 已设置（无本地副作用）
- [ ] 缺少环境变量时产生清晰的启动错误信息

### 文档完整性
- [ ] `README.md` 包含安装步骤
- [ ] `README.md` 包含 `claude mcp add` 接入命令
- [ ] `README.md` 包含 API 凭证获取说明
- [ ] `README.md` 包含 MCP Inspector 测试命令
- [ ] 所有 API 响应码已文档化

### 市场元数据
- [ ] Skill 名称唯一且描述性强（kebab-case）
- [ ] 描述准确反映能力（无过度宣传）
- [ ] 分类选择合适（建议：Verification / Compliance / Media）
- [ ] `package.json` 中已声明 `license`
- [ ] 提供联系/支持信息

### 最终验证
- [ ] 使用真实凭证完成完整端对端测试
- [ ] 真实照片测试返回 `verdict: "AUTHENTIC"`
- [ ] 非真实照片测试返回 `verdict: "NOT_AUTHENTIC"` + 警示信息
- [ ] 无效 URL 测试返回优雅的 MCP 错误
- [ ] 缺少环境变量时启动产生清晰错误并退出
