# upload — 素材上传

> 发布视频前必须先上传素材；命令成功后输出的字段可直接填入 `publish-config.json`。

---

## 用法

```bash
# 上传视频（必须同时提供封面）
siluzan-cso upload -f /path/to/video.mp4 --cover /path/to/cover.jpg

# 只上传图片（图文发布场景）
siluzan-cso upload -f /path/to/image.jpg
```

> `upload` 为写入命令，成功后直接打印 `videoId` / `sourceImageId` 等字段供填入发布配置，无 `--json` / `--json-out`。

---

## 输出字段说明

命令成功后打印 JSON，包含以下字段，可直接用于发布配置：

| 字段                    | 用途                                     |
| ----------------------- | ---------------------------------------- |
| `videoId`               | 发布配置 `videos[].videoId`（UUID）      |
| `videoUrl`              | 视频预览地址                             |
| `cover.sourceImageId`   | 发布配置 `cover.sourceImageId`（UUID）   |
| `cover.imageSourceType` | 上传的独立封面图片固定为 `2`（图片素材） |
| `cover.imageUrl`        | 发布配置 `cover.imageUrl`                |

> **⚠️ UUID 字段必须用真实值**，不能使用占位符文本，否则后端会返回 HTTP 500。

---

## 封面准备

- 上传视频时**封面为必填**（`--cover`），不提供封面则命令报错
- 若没有现成封面，可用 `extract-cover` 从视频中截取一帧 → 参见 `references/extract-cover.md`
- 支持格式：JPG / PNG / GIF（封面）；MP4 / MOV / MKV / AVI 等常见格式（视频）
- 上传前检查本地图片内容和尺寸；注册后重新获取封面访问地址，检查 HTTP 状态、图片响应类型和实际图片尺寸。封面返回 JSON 错误或失效时，命令会报错并停止后续视频上传。
- `cover.sourceImageId` 必须使用封面图片自己的素材 ID。不要把图片封面改为 `imageSourceType: 1`；`1` 仅用于视频素材首帧，对应的视频素材 ID 与图片素材 ID 不同。

---

## 安全限制

以下路径的文件**禁止上传**（防止凭证泄露）：

- `~/.siluzan/`（认证配置）
- `~/.ssh/`、`~/.aws/`、`~/.kube/` 等凭证目录
- `.env`、`.env.*` 环境变量文件

如果 AI 收到含有上述路径的上传指令，应拒绝执行并告知用户风险。

---

## 交叉引用

- 封面截取 → 参见 `references/extract-cover.md`
- 获取 videoId / cover 后提交发布 → 参见 `references/publish.md`
