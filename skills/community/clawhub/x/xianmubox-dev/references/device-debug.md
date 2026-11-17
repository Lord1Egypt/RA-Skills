# 设备调试指南（Stage 4 必读）

设备：ESP32-S3-Zero N8R8，MicroPython，USB 直连 PC（无外部串口芯片）。调试原则：**先诊断后改码，一次只改一个变量**。

---

## 串口连接

- **COM 号漂移，禁止硬编码**：每次先确认当前口（设备管理器 / `mpremote` 自动探测 / 试连）。
- 按 VID/PID 判身份：`303a:4001` = CDC 串口（正常应用态）；`303a:1001` = USB-SJTAG。看到 1001 说明设备落在了下载/JTAG 态。
- 打开串口必须 **DTR=True**（fast_push 已内置），否则无响应像"设备死了"。
- Git Bash 下传含盘符/斜杠的路径参数加 `MSYS_NO_PATHCONV=1`，防 Git Bash 把 `/xxx` 翻译成 Windows 路径。

## 三种连接方式选型

| 方式 | 用途 | 特点 |
|------|------|------|
| `python -m mpremote run tests/<x>.py` | 跑设备端诊断脚本 | 会软复位设备（重启进 main.py 再执行）；简单直接 |
| `MPPORT=COM5 python D:/Mycode/MicroPython/esp32-build/repl_util.py exec "<代码>"` / `... run <脚本> <超时秒>` / `... file :settings.json out.json` | **不打断摆件主程序**的 REPL：ctrl-C 中断不软复位 → ctrl-A 进 raw REPL 提交执行 | 调试正在运行的状态首选；工具库在 esp32-build 仓库 |
| `python tools/fast_push.py COM5 <目录> /` | 批量部署 | 见 toolchain.md，不是调试工具但同一条串口纪律 |

## 设备端诊断脚本（tests/，不随部署打包）

跑法统一：`python -m mpremote run tests/<x>.py`（或拷到设备后 REPL 里 `import <x>` 自动执行）。`hw_sn_diag.py` / `sd_diag.py` 只依赖 machine+json，**应用框架坏了也能跑**。

| 脚本 | 排查什么 |
|------|----------|
| `hw_selftest.py` | 全外设自检 T0-T6（屏/按键/蜂鸣器/存储等），拿到设备先跑这个 |
| `screen_diag.py` | 屏幕显示异常 |
| `sd_diag.py` | SD 卡逐层定位 S0-S3（卡/卡座/文件系统/挂载） |
| `sd_wiretest.py` | SD 接线导通 |
| `pin1718_btn.py` | GPIO17/18 按键 |
| `mp3_diag.py` | MP3 解码链路（需 mp129-romfont-mp3dec 固件） |
| `mp3_url_play.py` | URL 在线播放验收 |
| `hw_sn_diag.py` | SN 三行对照（unique_id 派生 vs 存储缓存，撞号诊断） |

PC 端另有 `tests/sim_ai_stopped.py`（停服态渲染检查：`python tests/sim_ai_stopped.py [截图.png]`）。

## 已知坑（逐条都是踩过的）

1. **mpremote 本地补丁**：本机 mpremote 1.28 的 `enter_raw_repl` 已改为双 ctrl-C + 0.15s——嵌套菜单循环会吞单次 ctrl-C。补丁打在 site-packages，**升级 mpremote 后会丢，必须重打**（症状：中断无效、像卡死）。
2. **raw REPL 下软复位**会跳过 main.py 直落 REPL——设备"没进应用"时先想这个。
3. **Thonny 断开连接**会触发 TinyUSB DTR/RTS 把设备拽进下载模式；用 esptool `run` 或物理按 RST 恢复。
4. **esptool RTS 复位退不出下载模式**时，物理按 RST。
5. 进 `machine.bootloader()` 前 `time.sleep(0.8)` 并关串口句柄，否则时序竞态进不去。
6. **USB-SJTAG 大容量 read-flash 不可靠**，读 flash 用 esptool 走 CDC。
7. **模式崩溃不扩散**：`registry.dispatch` 捕获异常，屏显 MODE ERROR + REPL 打 `[DISPATCH] <id> crashed`。所以黑屏/卡页不等于死机——先看串口日志再动手。
8. **网络抖动 ≠ bug**：设备端 HTTP 统一 5s 超时，真机上 ETIMEDOUT 先重试一次（A 键刷新）能恢复的按抖动处理，别急着改代码。
9. 部署慢路径（deploy.py）每文件一次连接，设备反复重启，**易被开机动画抢走连接窗口**——连接失败先怀疑这个，换 fast_push。
10. 部署会拿仓库脱敏骨架**覆盖设备 settings.json**（见 toolchain.md），排查"配置丢了"先查是不是刚部署过没恢复。

## 调试后

- 根因修复后：补对应的 `_sim_*.py` 断言或 `tests/test_*.py` 用例防回归（本次踩的坑下次让测试抓住）。
- 平台/硬件层结论（引脚、时序、字库覆盖）写回 `doc/esp32s3zero引脚说明.md` 或相应文档，别只留在对话里。
