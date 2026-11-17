# 本地配置与发布清单

## 存放位置和生命周期

- 配置路径优先级：本次显式指定 > `HTML_PUBLISH_CONFIG` > `${XDG_CONFIG_HOME:-$HOME/.config}/wrangler-html-publish/config.json`。
- Node 解析 HOME 使用 `os.homedir()`；Windows 可沿用用户主目录 `.config`，不要求设置 XDG。
- 在配置文件旁维护 `sites/<本地站点ID>/manifest.json`，按 Cloudflare 账号、项目、分支隔离，不能混用清单。ID 用安全字符，检查文件里目标字段，不凭目录名认定目标。
- 配置、manifest、plan 都在上传目录之外；仅本机使用，不随技能分发。不保存 token、Cookie、认证头、客户姓名或正文、带签名查询参数的 URL。
- 首次配置只创建不存在的文件；已有配置先读、定点更新，保留未知字段。原子写临时文件后替换配置，不覆盖用户未读改动；POSIX 目录 700、文件 600，Windows 继承用户私有目录权限。
- 配置不是秘密存储，也不是发布授权。发布授权仍须来自当前用户或明确有效的既有授权。

## 最小配置示例

```json
{
  "version": 1,
  "archive_root": "<当前用户解析出的绝对路径>/Documents/published-html",
  "account_id": "<已核验账号ID>",
  "project": "<用户确认项目>",
  "branch": "<目标分支>",
  "production_branch": "<已核验生产分支>",
  "site_id": "reports-production"
}
```

配置缺失时由 Agent 与用户完成一次引导，不要求手动编辑 JSON。账号/项目变化需重新核验。脚本 `defaults` 只给出默认值，不代替 Agent 加载已有配置。

## 本次上传计划

每条白名单明确源根目录、源相对路径、目标相对路径和 SHA256。所有路径由 Agent 解析，不把示例占位符直接执行。旧文件来自前次成功部署的快照，新增文件来自本次已审核归档。

```json
{
  "project": "reports-example",
  "branch": "main",
  "files": [
    {
      "root": "<历史快照绝对路径>",
      "source": "old-report/index.html",
      "target": "old-report/index.html",
      "sha256": "<64位小写十六进制哈希>"
    },
    {
      "root": "<归档根目录>/new-report",
      "source": "index.html",
      "target": "new-report/index.html",
      "sha256": "<64位小写十六进制哈希>"
    }
  ]
}
```

对需要更新的同一目标只保留新文件一条；先展示差异并取得覆盖授权，不同时列新旧副本。`files.mjs stage` 只按白名单复制，拒绝已存在 staging；不扫描并收集额外文件。文件后缀检查只是结构防线，不证明无敏感信息。

## 发布 manifest

```json
{
  "version": 1,
  "account_id": "<已核验账号ID>",
  "project": "reports-example",
  "branch": "main",
  "snapshot_root": "<本次成功上传的独立快照绝对路径>",
  "deployment_id": "<实际回执ID，如可取得>",
  "deployment_url": "<实际HTTPS URL>",
  "deployed_at": "<ISO时间>",
  "verification": "deployed_unverified",
  "files": [
    { "target": "new-report/index.html", "sha256": "<实际SHA256>" }
  ]
}
```

manifest 的 files 必须包含完整远端快照，不仅是本次新增文件。hash 与快照逐个对应。归档中存在但 manifest 未列出的文件不得自动上传。

部署成功但访问失败：保存回执，保持 `deployed_unverified`；之后验证成功更新为 `verified`。部署命令失败：保留上一份成功 manifest，不用失败计划替换它。网络中断导致结果未知时先查询部署列表/详情、核对实际回执，不能直接假设上传失败而覆盖重试。

状态丢失或快照缺失：不得把本地现有文件假装为完整站点；阻止覆盖原分支，先找回可信快照或选择经确认的独立目标。无权自动删除项目、历史快照或回滚远端。
