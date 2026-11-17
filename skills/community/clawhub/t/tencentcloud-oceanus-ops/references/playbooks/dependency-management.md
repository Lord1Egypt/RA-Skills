# Playbook: Dependency Resource Management

工作空间内依赖资源（jar 包 / 配置文件）的全生命周期管理。

涵盖：上传、版本、查询、目录组织。

## 资源类型与目录类型

`Resource.Type`（上传时通过 `--resource_type` 指定）：

| Value | Meaning |
| ----- | ------- |
| 1 | jar 包（`RESOURCE_TYPE_JAR`） |
| 2 | 配置文件（`RESOURCE_TYPE_DEPENDENCY`，例如 `.properties`） |

`FolderType`：

| Value | Meaning |
| ----- | ------- |
| 0 | 作业目录（默认） |
| 1 | 依赖资源目录 |

> `Resource.Type` 与作业引用资源时的 `ResourceRef.Type`
> （0=DEPENDENCY_JAR / 1=MAIN / 2=DEPENDENCY）**不是同一个枚举**，
> 详见 `references/enum-reference.md`。

## 一键上传依赖（推荐）

`upload_resource` 是一个编排命令，依次完成：

1. `CreatePresignedUrl` 获取 COS 预签名 URL（Location/Bucket/Key/Region）
2. HTTP `PUT` 把本地文件上传到该 URL
3. `CreateResourceConfig` 创建资源新版本，关联 COS 存储位置

前置条件：资源记录（`ResourceId`）已创建。

```bash
python scripts/oceanus_ops.py upload_resource \
  --resource_id resource-xxx \
  --file /path/to/my-connector.jar \
  --region ap-guangzhou \
  --confirm
```

输出会包含 `ResourceId` 和新的 `Version` —— 后续在作业 `--resource_refs` 中
按 `{"ResourceId":"...", "Type":0|1|2, "Version":N}` 引用
（0=DEPENDENCY_JAR 辅助 jar / 1=MAIN 主程序包 JAR-only / 2=DEPENDENCY 配置文件）。

## 分步流程

### 创建资源记录

```bash
# jar 包
python scripts/oceanus_ops.py create_resource \
  --name my-connector.jar \
  --resource_type 1 \
  --region ap-guangzhou --workspace_id space-xxx \
  --confirm

# 配置文件
python scripts/oceanus_ops.py create_resource \
  --name app-config.properties \
  --resource_type 2 \
  --region ap-guangzhou --workspace_id space-xxx \
  --confirm

# 创建到指定文件夹
python scripts/oceanus_ops.py create_resource \
  --name my-lib.jar --resource_type 1 \
  --folder_id folder-xxx \
  --region ap-guangzhou --confirm
```

### 手动获取预签名 URL（不推荐，调试用）

```bash
python scripts/oceanus_ops.py create_presigned_url \
  --file_name my-connector.jar \
  --region ap-guangzhou
# 拿到 Location 后用 curl PUT 上传
curl -X PUT -T /path/to/my-connector.jar -H "Content-Type: application/java-archive" "<Location>"
```

### 创建资源新版本（手动指定 COS 位置）

```bash
python scripts/oceanus_ops.py create_resource_config \
  --resource_id resource-xxx \
  --bucket my-bucket \
  --cos_path path/to/file \
  --cos_region ap-guangzhou \
  --region ap-guangzhou
```

## 查询

```bash
# 按工作空间查依赖列表（树状）
python scripts/oceanus_ops.py describe_tree_resources \
  --region ap-guangzhou --workspace_id space-xxx
```

## 依赖资源目录管理

依赖资源目录使用 `--folder_type 1` 区分于作业目录。

```bash
# 创建依赖资源目录
python scripts/oceanus_ops.py create_folder \
  --folder_name "connectors" \
  --folder_type 1 \
  --region ap-guangzhou --workspace_id space-xxx \
  --confirm

# 查询目录详情
python scripts/oceanus_ops.py describe_folder \
  --folder_id folder-xxx \
  --folder_type 1 \
  --region ap-guangzhou --workspace_id space-xxx
```

## Common Errors

| Code / Message | 原因 | 处理 |
| -------------- | ---- | ---- |
| `MissingParameter: ResourceLoc` | 调用 `create_resource` 时缺少 `--bucket/--cos_path/--cos_region` | 使用一键流程 `create_presigned_url` → `curl PUT` → `create_resource --bucket ... --cos_path ...`，或直接用 `upload_resource` |
| `ResourceNotFound` | `resource_id` 不存在或不在指定 workspace | 确认 `--workspace_id` 与 `--resource_id` 是否匹配；用 `describe_tree_resources` 复核 |
| 上传 PUT 失败（5xx / 403） | 预签名 URL 过期 / Content-Type 不匹配 | 重新获取 URL；保持 `Content-Type: application/java-archive`（jar）或 `text/plain`（properties） |

## 与作业关联

上传完成后，作业通过 `--resource_refs`（顶层 JSON 数组）引用资源。
`ResourceRef.Type` 的取值规则（按单个条目用途）：

| `ResourceRef.Type` | 含义 | 用途 |
| ------------------ | ---- | ---- |
| `0` (DEPENDENCY_JAR) | 辅助 jar 包（非主程序） | SQL / JAR 作业引用 **jar 包** 时统一使用 |
| `1` (MAIN)           | JAR 主程序包 | **仅 JAR 作业**，且必须恰好一个 |
| `2` (DEPENDENCY)     | 非 jar 的依赖文件（配置文件等） | SQL / JAR 作业引用 **配置文件** 时使用 |

- **SQL 作业**：jar 引用用 `Type=0`，配置文件用 `Type=2`；`Type=1` 会被 CLI 拒绝。
- **JAR 作业**：必须 **恰好一个** `Type=1`（MAIN，主程序包），其余 jar 用 `Type=0`、配置文件用 `Type=2`。

详见 `references/playbooks/create-sql-job.md` / `create-jar-job.md`。
