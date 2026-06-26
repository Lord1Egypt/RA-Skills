# Team Memory 升级与兼容说明

当前产品版本：`v2.4.0`  
当前数据结构版本：`schema-version: "2.0"`

发布包是 lean runtime 包，不包含 `data/`、真实 `skill-config.yaml` 或示例成员数据。升级时只更新 skill 能力，不触碰用户记忆。

## 升级原则

- 不覆盖 `skill-config.yaml`
- 不打包 `data/`
- 不自动迁移
- 迁移脚本默认 dry-run
- `--apply` 也只复制，不删除，不覆盖
- 新功能需要新目录或默认文件时，由 `init.sh` 在缺失时创建

## v1 兼容

v2.4.0 同时支持读取：

```text
data/members/member-001/profile.md
data/members/member-001/timeline.md
data/members/member-001/distill.md
```

以及 v1 旧文件：

```text
data/members/张三-档案.md
data/members/张三-时间轴.md
data/members/张三-蒸馏.md
```

如果 v1 和 v2 同时存在，默认优先使用 v2，把 v1 当作只读历史来源。

## 升级前备份

推荐先备份整个 skill 目录：

```bash
cd ~/.config/opencode/skills
zip -r "team-memory-backup-$(date +%Y%m%d-%H%M%S).zip" team-memory
```

迁移脚本在 `--apply` 时也会自动创建：

```text
data/.backup/YYYYMMDD-HHMMSS/
```

## 预览迁移

```bash
cd ~/.config/opencode/skills/team-memory
bash scripts/migrate-v1-to-v2.sh
```

预览会显示：

- 将识别哪些成员
- 将复制哪些 v1 文件
- 将创建哪些 v2 目标文件
- 是否存在别名冲突、配置缺失或目标文件已存在

## 执行迁移

确认预览无误后执行：

```bash
bash scripts/migrate-v1-to-v2.sh --apply
```

脚本行为：

- 创建 `data/.backup/{timestamp}/`
- 把旧文件备份进去
- 把旧文件复制到 v2 目录
- 保留所有 v1 原文件
- 遇到目标文件已存在时停止，不覆盖

## 回滚方式

因为迁移不会删除旧文件，最简单的回滚方式是继续使用 v1 文件。

如果想移除已生成的 v2 文件，请先确认备份存在，再手动删除对应 `data/members/member-XXX/` 目录。不要删除 `data/.backup/`。

## 常见升级问题

### 迁移脚本提示别名冲突

说明 `skill-config.yaml` 中有两个成员使用同一个 `alias` 或 `shortcuts`。请先改成唯一别名，再重新运行 dry-run。

### 迁移脚本提示目标文件已存在

说明该成员已经有 v2 文件。脚本不会覆盖。请手动比较内容后决定是否保留、重命名或归档。

### 没有找到某个成员的旧文件

脚本会跳过缺失文件。例如只有 `张三-时间轴.md` 时，只迁移时间轴，不伪造档案或蒸馏文件。

## v2.4.0 变更摘要

- 新增成员独立目录结构：`data/members/member-XXX/profile.md`、`timeline.md`、`distill.md`
- 新增 v1 到 v2 的只复制迁移脚本
- `SKILL.md` 改为明确执行规则
- 发布包改为 lean runtime，不携带用户态数据
- 中文文件名仍可读，但默认写入路径使用 `member-XXX`
