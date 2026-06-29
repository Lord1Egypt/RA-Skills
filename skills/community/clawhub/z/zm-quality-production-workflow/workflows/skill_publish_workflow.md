# Skill 入库 / 上传流程

## 说明

本流程用于把 Skill 稳定纳入本地 Skill 库或外部 Skill 库。

当前默认：先入本地 `skills/` 目录并 git commit。外部 ClawHub / 远程仓库发布属于外部发布动作，必须确认目标后再执行。

## 本地入库流程

1. Skill 目录放在 `skills/<slug>/`。
2. `SKILL.md` frontmatter 必须包含：
   - `name`
   - `description`
3. 必须有 `_meta.json`，包含：
   - `slug`
   - `displayName`
   - `version`
   - `status`
   - `description`
4. 运行 AI 可执行性审核。
5. 运行文件完整性检查。
6. git add 仅添加本 Skill 相关文件。
7. git commit。
8. 汇报 commit id。

## 外部上传流程

外部上传前必须确认：

- 上传目标：ClawHub / Gitee / GitHub / 私有库；
- 是否公开；
- 是否包含内部规则、账号、素材路径、隐私信息；
- 是否需要脱敏；
- 版本号；
- 维护 owner。

未确认前，不得外部发布。
