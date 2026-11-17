# 一键启动脚本（自行创建，可选）

> 平台对上传包的**文件类型有白名单**，`.cmd` 不在其中，所以这两段脚本以文本形式放在这里。
> 想要双击启动的话，按下面的路径各存一份即可，内容很短。

---

## Windows：`scripts/start-bridge.cmd`

> ⚠️ 这个文件**必须是纯 ASCII**。cmd.exe 按系统 ANSI 代码页（中文 Windows 上是 GBK）
> 解析 `.cmd` 文件，里面若含 UTF-8 中文，多字节序列会把脚本结构冲坏。
> 所以中文提示全部由 `a7w_bridge.py` 打印——Python 处理 UTF-8 没有问题。

```bat
@echo off
setlocal
set PORT=%~1
if "%PORT%"=="" set PORT=8788
set HERE=%~dp0

where python >nul 2>nul
if errorlevel 1 (
  echo.
  echo [X] python not found. Install Python 3.8+ and tick "Add to PATH".
  echo     https://www.python.org/downloads/
  echo.
  pause
  exit /b 1
)

python -X utf8 "%HERE%a7w_bridge.py" --port %PORT%

if errorlevel 1 (
  echo.
  echo [X] bridge exited with an error. Common causes:
  echo     - port %PORT% is in use or reserved; try: start-bridge.cmd 18899
  echo     - Python older than 3.8
  echo.
  pause
)
endlocal
```

保存到 `scripts\start-bridge.cmd`（编码选 **ANSI** 或 **UTF-8 无 BOM** 都可以，
因为内容全是 ASCII），之后双击即可；也可以带端口：`start-bridge.cmd 18899`。

---

## macOS / Linux：`scripts/start-bridge.sh`

```bash
#!/usr/bin/env bash
set -u
PORT="${1:-8788}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PY=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then echo "[X] python3 not found. Install Python 3.8+."; exit 1; fi

exec "$PY" -X utf8 "$HERE/a7w_bridge.py" --port "$PORT"
```

```bash
chmod +x scripts/start-bridge.sh
./scripts/start-bridge.sh          # 默认 8788
./scripts/start-bridge.sh 18899    # 指定端口
```

---

## 其实不写脚本也行

直接一条命令就够了：

```bash
python -X utf8 scripts/a7w_bridge.py --port 8788
```

启动横幅会把 **base_url、健康检查地址、应用透传口** 都打印出来，
以及在你还没配 API Key 时给出三步指引。

---

## 端口提示

默认 `8788`。若遇到 `WinError 10013`（本机把该端口划进了保留段），
换一个即可，例如 `18899`、`18080`——这两个在本机实测可正常绑定。
