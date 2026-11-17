# SkillHub 图标/封面上传：真实链路与踩坑

> 结论来源：2026-09-19 用真实账号 + 真实图片完成端到端验证。

## 一句话结论

图标走**两步**：

1. `POST /api/v1/community/skill-icons/upload` —— multipart，字段名必须是 **`file`**
   → 返回 `{"iconUrl": "...", "objectKey": "..."}`
2. 把拿到的 `iconUrl` 放进发布 body 的 **`payload.iconUrl`** 再提交

**把图片直接做成一个 `cover`（或 `icon`）multipart part 是无效的** —— 服务端静默忽略。

## 为什么容易踩错

| 错误做法 | 表象 | 真相 |
|---|---|---|
| `add("cover", bytes, ...)` | HTTP **201**，看着像成功 | 服务端根本不读这个 part；`iconAuditStatus` 恒为 `null` |
| `add("icon", bytes, ...)` | 同上 | 同上 |
| 想从官方 CLI 找线索 | `grep -n "cover\|icon\|封面" skills_store_cli.py` 只命中 1 处无关行 | 官方 CLI **完全没有**图标功能 |

连一张纯文本内容、扩展名为 `.png` 的假图片提交，服务端也返回 201 —— 说明它压根没校验这个 part。
**"201 即成功"是错觉**，真正的判据是响应里的 `iconAuditStatus`。

## 怎么确认生效

看发布响应：

```
"iconAuditStatus": "pending"     ← 生效（进入审核）
"iconAuditStatus": null          ← 没生效
```

`pending` = 图标已收到、正在审核。`null` = 压根没收到图标，服务端会用 `getPresetSkillIconBySeed()`
按 seed 分配一个预设图标（这也是为什么"没传图标"看起来也不难看）。

## 反查方法（可复用）

平台只有网页、没有图标上传 API 文档时：

1. 打开前端 bundle（3.7MB 左右），搜 `skill-icons` 或 `iconUrl`，定位 `uploadSkillIcon()`
2. 从源码读出端点路径、multipart 字段名、响应字段名
3. 用 `curl` / `urllib` 手工构造同款请求打一发，验证

本机已验证可用的 bundle 地址形如
`https://cloudcache.tencent-cloud.com/qcloud/tea/app/skillhub/assets/skill-hub.<hash>.js`
（hash 会随版本变，抓页面的 script 标签现取）。

## 本脚本的封装

```bash
python publish.py publish <dir> --icon icon.png
```

- `--cover` 作为 `--icon` 的**别名**保留（向后兼容旧命令）
- 默认按 `cover.png / cover.jpg / icon.png / icon.jpg ...` 顺序自动找
- 支持 png / jpg / jpeg / webp / gif，**上限 2MB**
- 上传失败**只告警不阻断发布**（宁可少个图标，也别让发布失败）

## 图标规范建议

- 尺寸：256×256 起，正方形
- 体积：控制在 2MB 内；纯色块 PNG 约 100~150KB
- 不要打进发布包：服务端拒收包内位图，只会得到 `400 不允许的文件类型`
