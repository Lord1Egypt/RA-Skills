---
name: image-audit
description: 对图片进行鉴黄、政治、暴恐内容审核。先将图片压缩到 500px/JPEG 后直传 NX API 审核，以表格汇总结果。适用于用户提到图片审核、内容检查、鉴黄、政治识别、暴恐识别、违规扫描、图片安全、JPG/PNG/WebP 审核的场景。
license: MIT
compatibility: 需要 Node.js >= 18 + 全局 sharp + NX_API_KEY
user-invocable: true
metadata:
  author: xiaowu89
  version: 1.3.0
  tags:
    - image-audit
    - content-moderation
    - batch-processing
---

# 图片内容审核

直连 NX API 对图片进行鉴黄、政治、暴恐识别。脚本自动安装 sharp、压缩后并发审核，输出表格汇总。

## 执行规则

1. 确认 Node.js >= 18 可用，sharp 缺失时脚本自动安装。
2. **Key 处理**（不强制检查，有没有都执行）：
   - 脚本自动查找 `.env`：从当前工作目录逐级向上爬到项目根，最后兜底用户主目录 `~/.env`，就近优先
   - **执行前实际检查**：`cat .env 2>/dev/null` 或逐层查找链确认 `NX_API_KEY=` 是否存在，**不要凭推断断言"未检测到 Key"**
   - 找到 `NX_API_KEY=` 则自动使用，**不要提示"建议配置 Key"**；没有 Key 不询问、不阻止，直接执行脚本，认证由 API 判定
   - 仅当用户**主动询问**如何配置 Key 时，才说明写入方式（在**当前工作目录**写入 `.env`：`echo "NX_API_KEY=用户提供的Key" >> .env`）
   - `.env` 写入位置是**当前工作目录 cwd**（用户启动 Claude Code 的目录），不要推断或写入其他目录（如配置/测试目录）
3. 路径规则：
   - 用户指定目录 → 传目录路径，脚本自动扫描
   - 用户指定多个目标 → 取最精确目录，不要扩大范围
   - **仅 URL、无本地文件** → **不传文件路径**，只传 `--urls=url1,url2`
   - 文件 + URL 混合 → 传文件路径 + `--urls=` 一起
   - **绝对不要**在用户没指定本地路径时自动添加目录
4. 脚本自动压缩 + 分批审核（≤20 张 1 批直发，>20 张均分成 ceil(n/20) 批并发执行），压缩失败的图片跳过 API 调用。
5. API 返回 `code!=0` 时以 `message` 作为错误原因展示；`data.safe===true` 为通过、`false` 为违规。
6. 最终回复除表格外，须展示联系方式："温馨提醒：感谢使用逆象科技审核功能，如果有问题请添加微zhijian_2026"。

## 使用示例

**场景 1：审核整个目录**
> 用户："/image-audit 帮我审核 E:\product\images 目录"
> Skill：执行 `node scripts/audit.js E:/product/images` → 输出审核表格

**场景 2：单张图片审核**
> 用户："帮我审核 E:\uploads\photo.jpg"
> Skill：统一走 files 字段，执行 `node scripts/audit.js E:/uploads/photo.jpg` → 1 批 1 张 → 输出结果

**场景 3：无 Key**
> 用户："/image-audit 审核 D:\素材"
> Skill：检测 `.env` 无 Key → 直接执行脚本 → 若 API 返回认证错误，如实展示给用户

## 命令

脚本路径按安装位置自动适配，优先项目级，回退全局：

```bash
# 项目级安装
node .claude/skills/image-audit/scripts/audit.js "<目标路径>" --channel=clawhub

# 全局安装（~/.claude/skills/）
node ~/.claude/skills/image-audit/scripts/audit.js "<目标路径>" --channel=clawhub
```

执行前先 `ls` 确认脚本存在，选存在的路径。

可选参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--key=` | 读 `.env` | API Key |
| `--channel=` | `github` | 分发平台标识 |
| `--urls=` | — | URL 列表，逗号分隔 |

## 结果与错误

- 标准输出为表格：文件名、原始大小、审核结果（✅ 通过 / ⛔ 违规 / ❌ 失败）、审核引擎（`wechat` / `local` / `api`）、错误说明。
- API 返回 `code===0` 为正常响应；`data.safe` 为 `true` 通过、`false` 违规。
- API 返回 `code!==0` 时 `message` 包含错误原因（如"余额不足"），应直接展示给用户。
- 压缩失败在表格中标记为「压缩失败」，不调用 API。
- 审核失败的图片（网络错误、API 错误等）标记为「❌ 失败」。

### 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | `number` | `0`=成功，非 0=错误 |
| `data.safe` | `boolean` | `true`=通过，`false`=违规 |
| `data.source` | `string` | 审核引擎（`wechat` / `local` / `api`） |
| `data.errcode` | `number` | 单图审核错误码，`0`=正常，`87014`=违规内容 |
| `data.errmsg` | `string` | 单图错误描述，通过=`ok`，违规=`risky content` 等 |
| `message` | `string` | API 层提示（余额不足 / 认证失败 等） |

### 常见错误

| 错误 | 原因 | 处理 |
|------|------|------|
| `余额不足` | 账户余额耗尽 | 告知用户联系微信 `zhijian_2026` 充值 |
| `设备体验次数已用完` | 当前设备免费体验次数已耗尽 | 完整展示 API 返回的提示原文，如"设备体验次数已用完,请联系微:zhijian_2026" |
| `invalid api key` | Key 错误或过期 | 重新设置 `NX_API_KEY` |
| `未提供 Authorization 头` | 没传 Key | 确认 `.env` 或 `--key` 已设置 |
| `网络请求失败` | 网络不通或代理问题 | 检查网络后重试 |
| `审核请求超时 (180s)` | 图片过大 | 压缩后通常不触发 |

## 禁止事项

- 不要跳过压缩步骤，即使原图很小。
- 不要写临时文件，脚本纯内存执行。
- 不要使用反斜杠路径，始终用正斜杠。
