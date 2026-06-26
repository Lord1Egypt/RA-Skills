# SQLBot-skills

这个仓库现在是一个 **Agent Skills / Claude Code Skill** 目录，同时也保留了单文件脚本 `sqlbot_skills.py` 可直接执行。

它用来操作 SQLBot 的工作空间、数据源、问数与仪表板：

- 查询当前用户可访问的工作空间
- 切换当前工作空间
- 查询当前工作空间下的数据源
- 切换当前数据源（skill 本地上下文）
- 基于当前或指定数据源问数
- 查询当前工作空间下的仪表板
- 查看指定仪表板详情
- 通过前端预览页导出指定仪表板的截图或 PDF

## 能力边界

这个 skill 直接调用 SQLBot 现有 API：

- 工作空间列表：`GET /api/v1/user/ws`
- 切换工作空间：`PUT /api/v1/user/ws/{oid}`
- 数据源列表：`GET /api/v1/datasource/list`
- 开始问数会话：`POST /api/v1/chat/start`
- 发起问数：`POST /api/v1/chat/question`
- 查询问数结果数据：`GET /api/v1/chat/record/{record_id}/data`
- 仪表板列表：`POST /api/v1/dashboard/list_resource`
- 仪表板详情：`POST /api/v1/dashboard/load_resource`

认证方式：

- skill 使用 SQLBot API Key 进行认证
- 请求头格式为 `X-SQLBOT-ASK-TOKEN: sk <signed-jwt>`
- 脚本会基于 `.env` 中的 `access_key` 和 `secret_key` 为每个请求动态生成短时签名

注意：

- SQLBot 的仪表板查询是基于“当前工作空间 + 当前用户”双重限定的。
- 数据源列表和问数同样依赖当前工作空间。
- 所以查询某个工作空间下的数据源、仪表板，或对指定工作空间问数前，skill 会先切换工作空间。
- SQLBot 后端没有独立的“切换数据源”接口，所以 skill 会把当前数据源保存在本地状态文件里，供后续 `ask` 作为默认数据源使用。
- SQLBot 后端当前没有原生的仪表板截图 / PDF 导出接口，导出能力通过前端预览页 + Playwright 实现。

## 作为 Skill 使用

Claude Code / Agent Skills 标准入口文件是根目录的 `SKILL.md`。

如果你要把它安装成 Claude Code Skill，可以直接复制整个目录：

```bash
mkdir -p ~/.claude/skills/sqlbot-workspace-dashboard
cp -R /path/to/SQLBot-skills/* ~/.claude/skills/sqlbot-workspace-dashboard/
```

然后在 Claude Code 中使用：

```text
/sqlbot-workspace-dashboard list workspaces
/sqlbot-workspace-dashboard switch workspace 2
/sqlbot-workspace-dashboard list datasources in workspace 2
/sqlbot-workspace-dashboard switch datasource 12
/sqlbot-workspace-dashboard ask 本周销售额是多少
/sqlbot-workspace-dashboard list dashboards in workspace 2
```

如果你的 OpenClaw 环境支持 Agent Skills，同样复制整个目录并保留 `SKILL.md`、`.env.example`、`sqlbot_skills.py` 这些文件即可。

更详细的 Skill 说明见 [reference.md](reference.md)。

## 直接执行脚本

如果你只想直接执行脚本，不需要安装，直接运行：

```bash
python3 sqlbot_skills.py --help
```

如果你想安装成命令：

```bash
pip install -e .
```

启用截图 / PDF 导出：

```bash
pip install -e .[browser]
playwright install chromium
```

## 配置

先复制模板：

```bash
cp .env.example .env
```

然后填写 `.env`：

```bash
SQLBOT_BASE_URL=http://127.0.0.1:8000/api/v1
SQLBOT_API_KEY_ACCESS_KEY=your-access-key
SQLBOT_API_KEY_SECRET_KEY=your-secret-key
SQLBOT_API_KEY_TTL_SECONDS=300
SQLBOT_TIMEOUT=30
# SQLBOT_BROWSER_PATH=/path/to/chrome
# SQLBOT_STATE_FILE=/absolute/path/to/.sqlbot-skill-state.json
```

说明：

- `SQLBOT_BASE_URL` 可以直接传 `http://host/api/v1`，也可以传应用根地址，脚本会自动补全。
- `SQLBOT_API_KEY_TTL_SECONDS` 是 skill 生成短时签名的有效期，默认 `300` 秒。
- 默认优先读取 skill 目录下的 `.env`，也兼容当前工作目录下的 `.env`；也可以通过 `--env-file` 指定别的配置文件。
- `SQLBOT_APP_URL` 可以去掉，前端预览地址会从 `SQLBOT_BASE_URL` 自动推导。
- `SQLBOT_STATE_FILE` 用于保存 skill 当前数据源上下文；默认写到 skill 目录下的 `.sqlbot-skill-state.json`。
- 导出仍然走前端预览页，但浏览器请求会附带 API Key 认证头，同时用占位 `user.token` 通过前端路由守卫。

## CLI 用法

查询工作空间：

```bash
python3 sqlbot_skills.py workspace list
python3 sqlbot_skills.py --env-file ./.env workspace list
```

切换工作空间：

```bash
python3 sqlbot_skills.py workspace switch 2
python3 sqlbot_skills.py workspace switch "运营中心"
```

查询数据源：

```bash
python3 sqlbot_skills.py datasource list
python3 sqlbot_skills.py datasource list --workspace 2
```

切换数据源：

```bash
python3 sqlbot_skills.py datasource switch 12
python3 sqlbot_skills.py datasource switch "订单中心" --workspace 2
python3 sqlbot_skills.py datasource current
```

问数：

```bash
python3 sqlbot_skills.py ask 本周销售额是多少
python3 sqlbot_skills.py ask 本周销售额是多少 --datasource 12
python3 sqlbot_skills.py ask 本周销售额是多少 --workspace 2 --datasource "订单中心"
python3 sqlbot_skills.py ask 继续按地区拆分 --chat-id 101
```

查询仪表板：

```bash
python3 sqlbot_skills.py dashboard list --workspace 2
python3 sqlbot_skills.py dashboard list --workspace "运营中心" --node-type leaf
```

查看仪表板详情：

```bash
python3 sqlbot_skills.py dashboard show 4a2c7e5a0d1c4e4f8a0b5d1142f4c999 --workspace 2
```

导出仪表板截图：

```bash
python3 sqlbot_skills.py dashboard export 4a2c7e5a0d1c4e4f8a0b5d1142f4c999 \
  --workspace 2 \
  --format png \
  --output ./exports/dashboard.png
```

导出仪表板 PDF：

```bash
python3 sqlbot_skills.py dashboard export 4a2c7e5a0d1c4e4f8a0b5d1142f4c999 \
  --workspace 2 \
  --format pdf \
  --output ./exports/dashboard.pdf
```

也可以安装后继续用命令入口：

```bash
sqlbot-skills workspace list
sqlbot-skills datasource list
sqlbot-skills ask 本周销售额是多少
```

## 测试

仓库使用标准库 `unittest`：

```bash
python3 -m unittest discover -s tests -v
```
