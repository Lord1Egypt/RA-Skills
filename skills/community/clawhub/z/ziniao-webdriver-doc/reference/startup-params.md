# 启动参数详细说明

> 本文件是 ziniao-webdriver-doc 的 Level 2 参考文档。
> 仅在需要了解紫鸟浏览器 WebDriver 模式的启动命令行参数时加载。

## 概述

通过命令行参数启动紫鸟浏览器客户端，使其进入 WebDriver 模式。
启动前**必须**关闭紫鸟浏览器的主进程，否则可能端口占用或冲突。

## 必选参数

| 参数 | 版本支持 | 说明 |
|------|---------|------|
| `--run_type=web_driver` | V5 / V6 全平台 | 指定以 WebDriver 模式运行主进程 |
| `--ipc_type=http` | V5 / V6 全平台 | 约定通信方式为 HTTP，超时建议 ≥120 秒 |
| `--port=端口号` | V5 / V6 全平台 | 指定通讯端口，紫鸟在本机以此端口启动 HTTP 服务 |

## 可选参数

| 参数 | 版本支持 | 说明 |
|------|---------|------|
| `--port_exception=1886,1567` | V5 only | 店铺内允许连接到本地的端口号，逗号分隔 |
| `--multip` | V5 only | 去除干扰自动化的功能，多账号建议与 `--enforce-cache-path` 一起使用 |
| `--enforce-cache-path=路径` | V5 only | 指定独立缓存目录，允许多账号同时运行，需自行调整 `--port` 避免冲突 |
| `--listen_ip=IP` | V5 only | 设置监听地址，默认 127.0.0.1。非本机时允许远程控制 |
| `--dns=DNS服务器` | V5 only | 设置 DNS，默认使用本机 DNS。示例：`--dns=223.5.5.5` |

## 启动命令示例

### Python

```python
import subprocess, platform, time

client_path = "紫鸟浏览器可执行文件路径"
socket_port = 9515

is_windows = platform.system() == 'Windows'
is_mac = platform.system() == 'Darwin'
is_linux = platform.system() == 'Linux'

def start_browser():
    try:
        if is_windows:
            cmd = [client_path,
                   '--run_type=web_driver',
                   '--ipc_type=http',
                   '--port=' + str(socket_port)]
        elif is_mac:
            cmd = ['open', '-a', client_path, '--args',
                   '--run_type=web_driver',
                   '--ipc_type=http',
                   '--port=' + str(socket_port)]
        elif is_linux:
            cmd = [client_path, '--no-sandbox',
                   '--run_type=web_driver',
                   '--ipc_type=http',
                   '--port=' + str(socket_port)]
        else:
            exit()
        subprocess.Popen(cmd)
        time.sleep(5)
    except Exception:
        import traceback
        print('start browser process failed: ' + traceback.format_exc())
        exit()
```

### JavaScript (Node.js)

```javascript
const childProcess = require('child_process');
const util = require('util');
const os = require('os');
const execFile = util.promisify(childProcess.execFile);

const clientPath = '紫鸟浏览器可执行文件路径';
const socketPort = 9515;

const is_windows = os.platform() === 'win32';
const is_mac = os.platform() === 'darwin';
const is_linux = os.platform() === 'linux';

async function startBrowser() {
    try {
        if (is_windows) {
            const cmd = [clientPath,
                '--run_type=web_driver',
                '--ipc_type=http',
                `--port=${socketPort}`];
            execFile(cmd[0], cmd.slice(1));
        } else if (is_mac) {
            const cmd = ['open', '-a', clientPath, '--args',
                '--run_type=web_driver',
                '--ipc_type=http',
                `--port=${socketPort}`];
            execFile(cmd[0], cmd.slice(1));
        } else if (is_linux) {
            const cmd = [clientPath, '--no-sandbox',
                '--run_type=web_driver',
                '--ipc_type=http',
                `--port=${socketPort}`];
            execFile(cmd[0], cmd.slice(1));
        } else {
            process.exit();
        }
        await new Promise(resolve => setTimeout(resolve, 5000));
    } catch (error) {
        console.log(`start browser process failed: ${error}`);
        process.exit();
    }
}
```

## 各操作系统差异

| 操作系统 | 启动方式 | 特殊参数 |
|---------|---------|---------|
| Windows | 直接调用可执行文件 | 无 |
| macOS | 通过 `open -a` 启动，`--args` 传参 | 无 |
| Linux | 直接调用可执行文件 | 需追加 `--no-sandbox` |
