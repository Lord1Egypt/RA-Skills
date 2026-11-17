# 安装/卸载协议（install-protocol.md）

## 1. 安装流程（即装即用）

```
manage_skill.py install --source <URL或路径> --reason "<匹配理由>"
manage_skill.py install --repo <owner/name> [--subdir <包内路径>] [--all-skills] --reason "<匹配理由>"
```

- `--source`：git URL / zip URL / 本地路径（本地已下载的候选）
- `--repo`：GitHub `owner/name`，脚本自动 `git clone --depth 1`（剥离死代理环境变量）
- `--subdir`：多技能包（一个仓库多个 SKILL.md）装指定子技能；不带且检测到多技能时，脚本列出所有技能并中止，要求明确选择
- `--all-skills`：整包安装（包内多技能都有用时）；超过 5 个技能时暂停并要求用户确认

固定六步，任何一步失败即中止并报告：

1. **快照**：skills 目录是 git 仓库时 `git add -A && git commit`（恢复点，记录 commit hash）；非 git 环境（普通用户常见）改为复制技能目录清单到 `state/.snapshots/<时间戳>/`
2. **下载**：`git clone --depth 1` 优先；失败退 zip 下载解压
3. **校验**（硬性，不过即拒）：
   - 存在 SKILL.md
   - frontmatter 含 `name` 与 `description`
   - SKILL.md 体积 < 500KB（防塞入巨型 payload）
   - 无敏感模式（见第 4 节红线）
4. **落盘**：复制到 `~/.workbuddy/skills/<name>/`（重名时追加 `-2` 后缀并在报告说明）
5. **git 登记**（仅 git 环境）：`git add <name>` + commit——未追踪文件无法被后续 `git rm` 卸载，此步不可省略
6. **manifest 记录**：向 `state/manifest.json` 追加记录（含技能 description，供善后询问时向用户解释「这技能是干嘛的」）

## 2. manifest 格式

```json
{
  "installs": [
    {
      "batch_id": "2026-10-23T0930_产品演示动画",
      "skill": "video-talkcraft",
      "source": "https://github.com/Vincentwei1021/video-talkcraft",
      "repo": "Vincentwei1021/video-talkcraft",
      "subdir": ".",
      "reason": "用户要做 APP 产品演示，本地无动效类技能",
      "description": "Turn an AI agent into a motion-design studio...",
      "category": "commercial",
      "installed_at": "2026-10-23T09:30:00",
      "git_snapshot": "665db67",
      "status": "active"
    }
  ]
}
```

`status` 取值：`active`（已装待裁决）→ `kept`（用户选择保留，今后不再询问）/ 删除（卸载后记录一并移除）。

## 3. 卸载与保留流程

```
manage_skill.py list
manage_skill.py keep --name <技能名>
manage_skill.py uninstall --name <技能名>
manage_skill.py uninstall --batch <batch_id>
```

### 卸载（用户回复「2」时执行）

1. 校验目标技能在 manifest 中——**防止误卸用户原有技能**（原有 54 项/346 项技能不在 manifest，一律卸不掉）
2. 移除目录：
   - git 环境且已被追踪 → `git rm -r` + commit
   - 非 git 环境或未追踪 → **移入 `state/.trash/<时间戳>/<技能名>/`**（软删除，保留在路由器自己的 state 内，可随时移回）
   - 任何情况下**禁止** `rm -rf` / `shutil.rmtree` / `del /S /Q`
3. 移除成功后才同步清理 manifest 记录（原子性：失败则 manifest 不动，重试即可）
4. 输出「已卸载 + 恢复方法」：
   - git 环境：`git restore --worktree .`（在 skills 目录内执行）回到快照点
   - 软删除：从 `state/.trash/<时间戳>/` 移回 `~/.workbuddy/skills/`

### 保留（用户回复「1」时执行）

`manage_skill.py keep --name <技能名>`：manifest 中该记录 `status` 置为 `kept`。作用：① 今后同类需求直接本地命中，不再重复下载；② 善后询问不再打扰用户。

## 4. 安全红线

第三方 SKILL.md 含以下内容时**拒绝安装**并报告：

- 要求读取 `cookies.json` / `session_api.json` / `*token*` 等凭据文件
- 要求向非本地地址外发数据
- 含 `rm -rf` / `shutil.rmtree` 破坏性代码且无确认逻辑
- 含 `eval(` 动态执行

其他规则：

- 安装失败时已完成的快照保留，用户可自行回滚
- 单批次安装数 > 5 时暂停并向用户确认（防止批量污染技能体系）
- 多技能包不明确指定子技能时不装（防止把整个大仓库糊进 skills 目录）

## 5. 版本记录

| 版本 | 日期 | 更新内容摘要 | 操作人 |
|------|------|------------|--------|
| v1.0 | 2026-10-23 | 创建安装/卸载协议：五步安装、manifest 格式、git rm 卸载、安全红线 | 桂皮 |
| v1.1 | 2026-10-23 | 安装流程增至六步：新增「git 登记」步（修复未追踪文件 git rm 失败缺陷） | 桂皮 |
| v2.0.0 | 2026-10-23 | 适配普通用户环境：新增 --repo/--subdir/--all-skills；快照/软卸载改到 state 目录（不再污染 skills 目录）；新增 keep 保留流程；manifest 增加 description/category/status 字段；红线补 eval | 桂皮 |
