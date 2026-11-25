# SkillHub 发布页参考

## 当前入口

- 页面：`https://skillhub.cn/dashboard/publish`
- 入口按钮：`发布 Skill` → `发布 Skill · 最快上架`
- 表单标题：`发布新技能`
- 更新入口：`我的 Skills` → 按 slug 找到原条目 → `更新`

## 字段

| 字段 | 当前选择器 | 内容来源 |
|---|---|---|
| Skill 包 | `input[type="file"][accept*=".zip"]` | `dist/<slug>-<version>.zip` |
| slug | `#skill-slug` | `manifest.yaml` 的 `slug` |
| 显示名称 | `#skill-displayName` | `manifest.yaml` 的 `display_name` |
| 中文简介 | `#skill-summaryZh` | `manifest.yaml` 的 `description` |
| 版本 | `#skill-version` | `manifest.yaml` 的 `version` |
| 更新说明 | `#skill-changelog` | 任务输入或默认首发说明 |
| 自定义图标 | `input[type="file"][accept*="image"]` | 根目录 `icon-512.png` |

SkillHub 当前会拒绝上传包中的 `LICENSE` 条目。仓库仍保留许可证并在本地校验；发布脚本只在上传归档中排除该文件。

图标流程是：选择“自定义” → “点击上传图片” → 选择文件 → 裁剪窗口“上传” → 等待“已选图标 / 重新上传 / 图标审核中” → 读取可见图标面板的远程图片 URL。

更新表单沿用同一批字段，但 slug 只读；脚本必须核对页面 slug 与本地 manifest 一致，并通过“重新上传”替换图标，不能只复用旧图标。

## 平台回执

提交后重新读取页面。以下文案可作为平台已接收证据：`提交成功`、`待审核`、`审核中`、`under review`、`pending review`。以下情况必须停下并记录为 `needs_user_action`：`请先登录`、`需要完成实名认证`、验证码/风控、`提交失败`、不允许的文件类型，或等待超时未出现任何确认文案。

“审核中”是已提交但未审核通过；SkillHub 的公开详情页出现之前，不能声称已公开可安装。

若全局 slug 已被其他作者使用，平台会显示“发布到你的命名空间”并要求二次“确认发布”。只有提示明确属于同名 slug/当前账号命名空间时才继续；确认后仍需读取正式审核状态。
