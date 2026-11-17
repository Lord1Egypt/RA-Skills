# Windows 安装与连接

本 Skill 只包含操作规范；运行包（UE 插件 + bridge）单独分发，避免把原生 DLL
塞进 Skill 包。

## 0. 版本对照

| 项 | 版本 |
|---|---|
| 本 Skill 包 | 6.5.10 |
| 运行包 | 6.5.4 |
| 适用引擎 | UE 5.1.x 开箱；5.8.x 预编译；5.2–5.7 需自行重编译 |

运行包下载（固定入口）：

```text
https://github.com/miracle1814/ue5-automation/releases/tag/v6.5.4
https://github.com/miracle1814/ue5-automation/releases/download/v6.5.4/ue5-automation-v6.5.4-portable.zip
```

> 不要用旧版本 DLL 冒充当前版本；DLL 与引擎版本不匹配会报
> `Incompatible or missing module`。

## 1. 准备

- Windows 10/11 x64；
- UE 5.1.x 或 5.8.x；
- 项目已启用：
  - `Python Editor Script Plugin`
  - `Editor Scripting Utilities`
- 关闭其他占用 8889 端口的编辑器实例，或给当前实例设置
  `UE5_BRIDGE_PORT=8890` 后重启。

## 2. 安装运行包

解压 portable 包，运行：

```bat
tools\install.bat
```

> 包根目录没有 `install.bat`（v6.5.4 包里在 `tools\`）。如果系统没有
> `py` / `python`，用引擎自带 Python 直接跑部署脚本：
>
> ```bat
> "<UE>\Engine\Binaries\ThirdParty\Python3\Win64\python.exe" tools\deploy_portable.py --project "<项目>.uproject"
> ```

把 `.uproject` 拖进窗口。脚本会：

1. 读 `EngineAssociation`；
2. 选 5.1 / 5.8 DLL；
3. 安装插件到 `Plugins/BlueprintPythonBridge`；
4. 安装宿主脚本到 `Content/Python`；
5. 写自启入口；
6. 跑环境自检，看到 `FAIL 0` 即成功。

### 2.1 编辑器 Python 依赖

bridge 需要 `fastapi` / `uvicorn` / `pydantic`。启动日志如果报
`ModuleNotFoundError: No module named 'pydantic'`，用**引擎自带 Python** 安装：

```bat
"<UE>\Engine\Binaries\ThirdParty\Python3\Win64\python.exe" -m pip install fastapi uvicorn pydantic
```

**不要加 `--user`**：UE 内嵌 Python 可能不加载用户 site-packages，装到用户目录
等于没装。装完重启编辑器。

5.8 注意：项目自身 `Content/Python/init_unreal.py` 不再自动执行，自启挂在
`Plugins/ue5-automation-extras/Content/Python/init_unreal.py`。`ue5_bridge.start()`
是幂等的，重复调用无害。

## 3. 启动编辑器

重启 UE 编辑器，Output Log 搜索 `ue5_bridge`，应看到：

```text
[ue5_bridge] [OK] 服务已在后台启动 → http://127.0.0.1:8889/docs
```

再搜索 `BlueprintPythonBridge`，不应出现 `Incompatible or missing module`。

## 4. 连接 MCP

### HTTP（推荐）

```text
URL:    http://127.0.0.1:8889/mcp
Header: X-Skill-Token: <token>
```

token 文件：

```text
%APPDATA%\ue5_bridge\token
```

通用客户端配置（字段名以你使用的客户端为准）：

```json
{
  "mcpServers": {
    "ue5-automation": {
      "type": "http",
      "url": "http://127.0.0.1:8889/mcp",
      "headers": { "X-Skill-Token": "<token>" }
    }
  }
}
```

Claude Code 示例：

```bat
claude mcp add --transport http ue5-automation http://127.0.0.1:8889/mcp --header "X-Skill-Token: <token>"
```

### stdio

```json
{
  "mcpServers": {
    "ue5-automation": {
      "command": "python",
      "args": ["<项目路径>/Content/Python/ue5_mcp_stdio.py"],
      "env": { "UE5_BRIDGE_TOKEN": "<token>" }
    }
  }
}
```

或使用运行包自带脚本一键探测并写入常见客户端配置：

```bat
python Content\Python\install_mcp.py --dry-run
python Content\Python\install_mcp.py
```

## 5. 自检

```json
{"command":"health","params":{}}
```

应返回：

```json
{"status":"ok","ue_info":{"engine_version":"5.x","bridge_loaded":true}}
```

同时确认 `mcp_tool_profile` 与 `mcp_tool_count`：

- `gateway`：12 个入口；
- `core`：18 个；
- `full`：34 个。

## 6. 升级与卸载

升级：

1. 关闭编辑器；
2. 用新版本 portable 包重新运行 `install.bat`（会覆盖插件与宿主脚本）；
3. 重启编辑器，重新 `health` 确认版本。

卸载：

1. 关闭编辑器；
2. 删除项目内 `Plugins/BlueprintPythonBridge` 与
   `Plugins/ue5-automation-extras`；
3. 删除 `Content/Python` 下由安装器写入的 `ue5_bridge.py` /
   `ue5_mcp_stdio.py` / `init_unreal.py` 入口；
4. 删除 `%APPDATA%\ue5_bridge`（含 token、回执、幂等缓存）。

## 7. 常见问题

| 现象 | 处理 |
|---|---|
| 没有“服务已在后台启动” | 检查插件启用、自启入口是否存在；5.8 看插件侧 init |
| `Incompatible or missing module` | DLL 与引擎版本不匹配，重跑 `install.bat` |
| FastAPI/uvicorn 未安装 | 用引擎自带 Python：`python.exe -m pip install fastapi uvicorn pydantic` |
| 403 | 读 `%APPDATA%\ue5_bridge\token`，与客户端配置保持一致；没有默认 token |
| 端口占用 | 关掉另一个编辑器，或设 `UE5_BRIDGE_PORT=8890` 后重启 |
| `health` 正常但工具很少 | 当前是 gateway 档；需要时切 `core` / `full` 后重启 |
