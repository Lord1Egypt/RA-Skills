# vod_aigc_token — 详细参数与示例
> 此文件由 references 拆分生成，对应脚本：`scripts/vod_aigc_token.py`

## 参数说明


### 通用参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `--region` | string | 地域，默认 `ap-guangzhou` |
| `--sub-app-id` | int | VOD 子应用 ID（2023-12-25 后开通的必填，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--json` | flag | JSON 格式输出 |
| `--dry-run` | flag | 预览参数，不调用 API |

### create 参数（创建 Token）

| 参数 | 类型 | 说明 |
|------|------|------|
| `--sub-app-id` | int | VOD 子应用 ID（可选，2023-12-25 后开通的必填，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |

> 💡 若环境变量 `TENCENTCLOUD_VOD_AIGC_TOKEN` 中已有 Token，脚本会扫描所有配置文件并列出哪些文件含有该配置，提示是否继续，输入 `y` 或 `yes` 继续，直接回车则取消。

> 💡 创建成功后，Token 会**自动写入**环境变量配置文件（若已有配置则更新所有含该变量的文件，否则写入 `~/.env`），并设置 `TENCENTCLOUD_VOD_AIGC_TOKEN`。

> ⚠️ **Token 注意事项：**
> 1. Token **没有过期时间**，请妥善保管
> 2. 创建后需等约 **1 分钟**同步到网关，请勿立即使用
> 3. 每个用户最多 **50 个** Token

### list 参数（查询 Token 列表）

| 参数 | 类型 | 说明 |
|------|------|------|
| `--sub-app-id` | int | VOD 子应用 ID（可选，2023-12-25 后开通的必填，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |

> 💡 输出字段说明：每条记录包含 `Token ID`、`Token`（Token 字符串）、`创建时间`。删除 Token 时，`--api-token` 参数应传入 `Token` 字段的值（非 `Token ID`）。

### delete 参数（删除 Token）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--api-token` | string | ✅ | 要删除的 API Token 字符串（通过 `list` 获取，填写 `Token` 字段值，非 `Token ID`） |
| `--sub-app-id` | int | - | VOD 子应用 ID（可选，2023-12-25 后开通的必填，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |

> 💡 删除后约 **1 分钟**后在网关失效，期间 Token 仍可使用。

### usage 参数（查询 AIGC 用量统计）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--sub-app-id` | int | - | VOD 子应用 ID（可选，2023-12-25 后开通的必填，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--type` / `-t` | string | ✅ | AIGC 类型：`Video`（视频）、`Image`（图片）、`Text`（文本） |
| `--start` | string | - | 起始日期，格式 `YYYY-MM-DD` 或完整 ISO 格式（如 `2026-03-01T00:00:00+08:00`）；**默认为 30 天前** |
| `--end` | string | - | 结束日期，格式 `YYYY-MM-DD` 或完整 ISO 格式（如 `2026-03-31T23:59:59+08:00`）；**默认为今天** |

> 💡 `--start`/`--end` 传入 `YYYY-MM-DD` 时，脚本会自动补全为 `T00:00:00+08:00` 和 `T23:59:59+08:00`

### API 接口对应关系

| 功能 | API 接口 | 文档链接 |
|------|---------|---------|
| 创建 Token | `CreateAigcApiToken` | https://cloud.tencent.com/document/api/266/128386 |
| 删除 Token | `DeleteAigcApiToken` | https://cloud.tencent.com/document/api/266/128387 |
| 查询 Token | `DescribeAigcApiTokens` | https://cloud.tencent.com/document/api/266/128388 |
| 查询 AIGC 用量 | `DescribeAigcUsageData` | https://cloud.tencent.com/document/api/266/128389 |
| 调用 LLM Chat 接口 | POST `https://text-aigc.vod-qcloud.com/v1/chat/completions` | — |

---


---


## 使用示例


### Token 生命周期管理

#### 创建 Token（首次使用）
```bash
python scripts/vod_aigc_token.py create
# 若已有 Token，会提示是否覆盖，输入 y 或 yes 继续，回车取消
```

#### 查询 Token 列表
```bash
python scripts/vod_aigc_token.py list
```

#### 删除指定 Token
```bash
python scripts/vod_aigc_token.py delete --api-token tok_abc123
```

#### 指定子应用 ID（2023年12月后开通的用户必须填写）
```bash
python scripts/vod_aigc_token.py create --sub-app-id 1500000001
python scripts/vod_aigc_token.py list   --sub-app-id 1500000001
```

---

### AIGC 用量统计

#### 查询文本生成用量（本月）
```bash
python scripts/vod_aigc_token.py usage \
    --type Text \
    --start 2026-03-01 \
    --end 2026-03-31
```

#### 查询视频生成用量
```bash
python scripts/vod_aigc_token.py usage \
    --type Video \
    --start 2026-03-01 \
    --end 2026-03-31
```

#### 查询图片生成用量（JSON 格式）
```bash
python scripts/vod_aigc_token.py usage \
    --type Image \
    --start 2026-03-01 \
    --end 2026-03-31 \
    --json
```

#### dry-run 预览参数
```bash
python scripts/vod_aigc_token.py --dry-run usage \
    --type Text \
    --start 2026-03-01 \
    --end 2026-03-31
```

---

