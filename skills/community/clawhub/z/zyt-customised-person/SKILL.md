---
name: chanjing-customised-person
description: Use Chanjing customised person APIs to create, inspect, list, poll, and delete custom digital humans from uploaded source videos.
metadata:
  openclaw:
    requires:
      env:
        - CHANJING_CONFIG_DIR
    homepage: https://open-api.chanjing.cc
---

# Chanjing Customised Person

## When to Use This Skill

当用户要做这些事时使用本 Skill：

* 上传真人源视频，创建蝉镜定制数字人
* 查询定制数字人列表或单个形象详情
* 轮询定制数字人制作进度
* 删除不再需要的定制数字人

如果需求是“拿已有数字人去合成口播视频”，优先使用 `chanjing-video-compose`。  
如果需求是“上传真人视频做对口型驱动”，优先使用 `chanjing-avatar`。

## Preconditions

本 Skill 自己包含本地配置和鉴权流程，不依赖其他 skill 的运行时脚本。

本 Skill 使用：

* 配置文件：`~/.chanjing/credentials.json`
* 若设置环境变量 `CHANJING_CONFIG_DIR`：使用 `$CHANJING_CONFIG_DIR/credentials.json`
* API 基础地址固定：`https://open-api.chanjing.cc`

当本地缺少 AK/SK 或 AK/SK 无效时，脚本默认返回登录引导信息，不自动打开浏览器。  
如需本地自动开页，可显式设置：`CHANJING_AUTO_OPEN_LOGIN=1`。
`https://www.chanjing.cc/openapi/login`

## Standard Workflow

1. 调用 `upload_file` 上传本地源视频，获取 `file_id`
2. 调用 `create_person` 创建定制数字人任务，得到 `person_id`
3. 调用 `poll_person` 轮询直到成功，得到 `preview_url`，或用 `get_person --field audio_man_id` 拿到声音 id
4. 如需批量查看历史形象，用 `list_persons`
5. 如需清理资源，用 `delete_person`

## Covered APIs

本 Skill 当前覆盖：

* `GET /open/v1/common/create_upload_url`
* `GET /open/v1/common/file_detail`
* `POST /open/v1/create_customised_person`
* `POST /open/v1/list_customised_person`
* `GET /open/v1/customised_person`
* `POST /open/v1/delete_customised_person`

## Scripts

脚本目录：

* `scripts/`

| 脚本 | 说明 |
|------|------|
| `chanjing-config` | 写入/查看本地 `app_id` 与 `secret_key`，并清理旧 token 缓存 |
| `chanjing-get-token` | 从本地凭证获取有效 `access_token`（必要时自动刷新） |
| `_auth.py` | 读取凭证、获取或刷新 `access_token` |
| `get_upload_url` | 获取上传链接，输出 `sign_url`、`mime_type`、`file_id` 等 JSON |
| `upload_file` | 上传本地素材并轮询到文件可用，输出 `file_id` |
| `create_person` | 创建定制数字人任务，输出 `person_id` |
| `list_persons` | 列出定制数字人形象 |
| `get_person` | 获取单个数字人详情，默认输出 JSON |
| `poll_person` | 轮询形象详情直到完成，默认输出 `preview_url` |
| `delete_person` | 删除定制数字人，输出被删除的 `person_id` |

## Usage Examples

示例 1：从本地视频创建定制数字人

```bash
FILE_ID=$(python3 scripts/upload_file \
  --file ./source.mp4)

PERSON_ID=$(python3 scripts/create_person \
  --name "演示数字人" \
  --file-id "$FILE_ID" \
  --train-type figure)

python3 scripts/poll_person --id "$PERSON_ID"
```

示例 2：查看完整详情

```bash
python3 scripts/get_person \
  --id "C-ef91f3a6db3144ffb5d6c581ff13c7ec"
```

示例 3：列出与删除

```bash
python3 scripts/list_persons

python3 scripts/delete_person \
  --id "C-ef91f3a6db3144ffb5d6c581ff13c7ec"
```

## Output Convention

默认不自动下载任何预览视频或封面图：

* `create_person` 输出 `person_id`
* `poll_person` 输出 `preview_url`，便于继续预览或保存
* 只有在用户明确要求时，才应把返回的资源 URL 另存到本地

如果后续需要落盘预览资源，建议使用：

* `outputs/customised-person/`

## Additional Resources

更多接口细节与触发样例见：

* `reference.md`
* `examples.md`
