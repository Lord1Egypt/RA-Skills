# account-group — 账号分组管理

> 将媒体账号归类到分组，便于发布时按组批量指定目标账号。

---

## ⚠️ 必读：用哪个 ID？

`--accounts` 参数**只接受 `mediaCustomerId`**，这是账号在媒体平台上的原生 ID。

`list-accounts --json-out` 落盘的每个账号对象中有多个 ID 字段，**极易混淆**：

| 字段                          | 示例值                                | 用途                                                            |
| ----------------------------- | ------------------------------------- | --------------------------------------------------------------- |
| `mediaCustomerId`             | `UCg3_FESu2sADBKq4WKGozug`            | ✅ **account-group 的 `--accounts` 参数用这个**                 |
| `entityId`                    | `a2ace2a2-00c1-478d-a991-...`（UUID） | 发布配置 `accounts[].entityId`，**不是这个**                    |
| `externalMediaAccountTokenId` | `f4f687..`（UUID）                    | 发布配置 `accounts[].externalMediaAccountTokenId`，**不是这个** |

**操作流程：**

```bash
# Step 1：拿到账号的 mediaCustomerId（落盘后脚本读盘，见 references/core/tips.md）
siluzan-cso list-accounts --name "账号名" --json-out ./snap-cso
# 从落盘 JSON 中取 "mediaCustomerId" 字段值

# Step 2：用 mediaCustomerId 操作分组
siluzan-cso account-group create --name "分组名" --accounts "mediaCustomerId1,mediaCustomerId2"
```

---

## 常用场景速查

| 用户意图                                 | 命令                                                                             |
| ---------------------------------------- | -------------------------------------------------------------------------------- |
| 查看所有分组                             | `siluzan-cso account-group list`                                                 |
| 查某分组内有哪些账号                     | `siluzan-cso account-group list --json-out ./snap-cso`                           |
| 新建空分组                               | `siluzan-cso account-group create --name <名称>`                                 |
| 新建分组并添加账号                       | `siluzan-cso account-group create --name <名称> --accounts <id1,id2>`            |
| **向已有分组追加账号（不影响其他账号）** | `siluzan-cso account-group add-accounts --id <groupId> --accounts <ids>`         |
| **从分组移除指定账号（不影响其他账号）** | `siluzan-cso account-group remove-accounts --id <groupId> --accounts <ids>`      |
| 全量替换分组账号列表                     | `siluzan-cso account-group update --id <groupId> --name <名称> --accounts <ids>` |
| 删除分组                                 | `siluzan-cso account-group delete --id <groupId>`                                |

---

## 命令详解

### list — 查询分组列表

```bash
# 默认表格展示（分组 ID / 名称 / 账号数 / 创建时间）
siluzan-cso account-group list

# 落盘完整数据（含 mediaAccountInfos，可获取各账号 mediaCustomerId），脚本读盘见 references/core/tips.md
siluzan-cso account-group list --json-out ./snap-cso
```

> `id === "未分组"` 是系统虚拟分组，不可编辑或删除。

---

### create — 新建分组

```bash
# 新建空分组
siluzan-cso account-group create --name "海外品牌账号"

# 新建并同时添加账号（mediaCustomerId，逗号分隔，可含空格）
siluzan-cso account-group create --name "TikTok 主账号" --accounts "id1,id2,id3"
```

成功后输出新分组 ID，可用于后续 update / delete。

---

### add-accounts — 追加账号（推荐）

```bash
# 向分组追加一个或多个账号，已在组内的账号自动跳过（幂等）
siluzan-cso account-group add-accounts --id <groupId> --accounts "新id1,新id2"
```

内部自动拉取当前账号列表再合并，**无需提前知道组内有哪些账号**。

---

### remove-accounts — 移除账号（推荐）

```bash
# 从分组移除指定账号，不在组内的账号自动跳过（幂等）
siluzan-cso account-group remove-accounts --id <groupId> --accounts "要移除的id1,id2"
```

内部自动拉取当前账号列表再过滤，**无需提前知道组内完整列表**。

---

### update — 全量替换（慎用）

```bash
# 将分组账号列表替换为指定的完整列表（不传 --accounts 则清空！）
siluzan-cso account-group update --id <groupId> --name "分组名称" --accounts "id1,id2,id3"
```

> **注意：** 后端以传入的 `--accounts` 为准，不传时**清空**分组内所有账号。  
> 需要增量操作时，请优先使用 `add-accounts` / `remove-accounts`。

---

### delete — 删除分组

```bash
siluzan-cso account-group delete --id <groupId>
```

> 「未分组」虚拟分组不可删除。

---

## 典型流程

### 向已有分组添加新账号

```bash
# Step 1：获取新账号的 mediaCustomerId（落盘后脚本读盘）
siluzan-cso list-accounts --name "新账号名" --json-out ./snap-cso

# Step 2：直接追加（无需查当前列表）
siluzan-cso account-group add-accounts --id <groupId> --accounts "新id"
```

### 从分组移除某个账号

```bash
# 直接移除（无需查当前列表）
siluzan-cso account-group remove-accounts --id <groupId> --accounts "要移除的id"
```

---

## 交叉引用

- 获取账号 `mediaCustomerId` → 参见 `references/list-accounts.md`
