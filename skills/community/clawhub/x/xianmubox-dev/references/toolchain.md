# 工具链命令速查（build / test / 仿真 / 部署 / 固件）

所有命令在仓库根目录执行。`src/` 是唯一源码目录，**`build/` 全部由 `tools/build.py` 生成，禁止手改**；部署只推 build 产物，不推 src。

---

## 构建 tools/build.py

```bash
python tools/build.py --profile full --device esp32s3_n8r8    # -p 必填，-d 可覆盖
```

- 产物目录：`build/<device>_<profile>/`，完整可部署包。
- **自动生成 5 个文件**（手改无效，下次构建被覆盖）：`config.py`、`app_config.py`、`modes/registry.py`、`boot.py`（内嵌 UTC+8 时区回调）、`main.py`（SD 挂载 + 配网引导 + 主循环）。改启动行为必须改 `tools/build.py` 的生成模板——`src/boot.py` / `src/main.py` 只是开发/仿真参考版，**不参与构建**。
- 复制范围：framework/ 按 **FRAMEWORK_FILES 白名单**（build.py 头部）——新增 `framework/<x>.py` 被运行时用到必须登记一行，否则设备上 ImportError；`font/*.py|*.mpy` 全复制（st7789_mpy 字库 vga1_8x8 等随部署携带）；icons 按profile 引用 + `icons/black/` 天气库；PNG 经 PIL 转 RGB565 `.raw`。
- profile 结构（`profiles/full.json`）：`name/device/features[]/boot_animation/menu_style/wifi/icons[]`；每个 feature 为 `{id, name, color(CLR_*字面量), icon, module, class}`，可选 `extra_icons[]`。

已知行为：

- Windows 下 build 目录被占用（资源管理器/杀毒占用）会退化为就地清空重建，删除失败报错时先关占用者。
- `src/settings.json` 缺失 → WARN 后继续，设备将以默认值启动。仓库内是**脱敏骨架**，不是真实配置。
- 无 PIL → PNG→raw 转换跳过并 WARN，图标相关功能设备上会缺资源。

## 测试 tools/test.py

```bash
python tools/test.py        # 全量；-v 详细
```

PC 端静态检查，串行跑 9 个套件：Registry Consistency / Import Rules / Mode Interface / Config Validity / Buttons / Fonts / Stock / Audio MP3 / Device SN。对应 `tests/test_*.py`（9 个，由 test.py 收录，不单独跑）。

- **门禁**：全绿才允许构建/提交。唯一预期红：`secrets.py` 缺失相关 1 项 FAIL。
- Registry Consistency 会校验 src/app_config.py、src/modes/registry.py、profiles 的一致性——所以三处注册缺一处这里就会红。

## Web 配置页预览 tools/preview_web.py

改 `src/www/index.html` 后在 PC 上离线预览与校验：`python tools/preview_web.py`（模拟设备端模板渲染 + 各 API 端点），`--check` 校验占位符与裸 `%`。模板占位符必须 `%(key)s`、字面 `%` 写 `%%`，改模板后必须重新 build。

## 仿真器 tools/simulator/

```bash
python tools/simulator/run.py --mode net_clock --zoom 3     # GUI 人工点按（--list 列注册模式）
python tools/simulator/run.py --spec designs/demo.json      # 渲染设计稿 spec
python tools/simulator/run.py --mode clock --screenshot out.png --frames 3   # 无头截图自检
python tools/_sim_radio.py                                  # 模式回归断言脚本
```

- 仿真从 `src/` 直读（`modes.registry._MODULE_MAP` + `app_config.MENU_ITEMS`），所以新模式必须先登记这两处再仿真。
- 键盘映射：←/a=A，回车/b/空格=B，→/c/Esc=C；虚拟按钮支持长按（40ms/帧 tick）。
- 回归脚本命名 `tools/_sim_<主题>.py`（现有 10 个：alarm/news/news_page/provision/radio/settings_qr/sn/stock/story/vocab），照 `tools/_sim_sn.py` 模板写：`sys.path` 指向 simulator 与 `../src` → `stubs.install(device="esp32s3_n8r8")` → SimDisplay + SimButtons/SimBuzzer → monkeypatch `_scan_with_timing` 按键脚本驱动 `loop()` → `display.screenshot("tools/shots/xxx.png")` → PASS/FAIL 计数，`sys.exit(1 if FAIL else 0)`。
- 截图统一落 `tools/shots/`。

## 部署

**部署前必备份设备配置**——部署会把仓库脱敏骨架 `src/settings.json` 覆盖到设备，WiFi/闹钟/云激活等全丢：

```bash
python -m mpremote cp :settings.json ./settings.backup.json
```

| 路径 | 命令 | 特点 |
|------|------|------|
| **快（默认）** | `python tools/fast_push.py COM5 build/esp32s3_n8r8_full /` | 单连接 raw REPL，base64 分块（3KB/块），每文件回读校验，设备全程不软复位，完成 ctrl-B+ctrl-D 一次性重启进应用。开机动画期最多重试 8 轮抢连接。依赖 pyserial，打开串口即置 DTR=True。 |
| 慢（备选） | `python tools/deploy.py --profile full --port COM5 [--skip-build]` | 进程内先构建再 mpremote 逐文件上传，**每文件一次连接、设备反复重启**，慢且易被开机动画抢窗口。仅 fast_push 不可用时用。 |
| 单文件热修 | `python -m mpremote cp src/modes/<x>.py :modes/<x>.py` + `python -m mpremote reset` | 只修一个文件时用；注意保持 src 与 build 产物同源，别让两边漂移。 |

部署后：确认设备 `settings.json` 已从备份恢复（惯例恢复源 `settings.device-backup.json`）；v1.3.1+ 固件设备 SN 会按 unique_id 开机自愈纠偏，骨架里 `device_sn` 为空是正常的。

## 固件烧录（仅换固件时）

```bash
esptool --port COM4 --chip esp32s3 --baud 460800 --before default-reset --after hard_reset write-flash 0x0 firmware.bin
```

- **先登记后烧录**：在 `doc/固件版本履历.md` 总表加行（版本标识 `mp129-<组件链>` / 日期 / 模块构成 / 双归档路径 / 大小 / MD5），归档惯例 = 仓库 `firmware/release/` + `D:\Mycode\MicroPython\esp32-build\firmware\` 各一份且 **MD5 一致**；烧录后回填真机验证状态。
- 进下载模式：按住 BOOT 短按 RST；或 REPL 里先 `time.sleep(0.8)`、关串口句柄再 `machine.bootloader()`。
- 坑：esptool RTS 复位可能退不出下载模式，需物理按 RST；`erase_flash` 或分区表变更会清文件系统，烧完必须重新部署应用 + 恢复 settings。
- mpremote 本地补丁（见 device-debug.md）在升级 mpremote 后会丢，重打后才能正常调试。
