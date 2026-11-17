# 编码硬约束与模式契约（Stage 3 动手前必读）

权威来源：`doc/project_conventions.md`（编码/命名/依赖/settings/HTTP）、`doc/框架架构设计文档.md`（接口/按键/服务）、`doc/功能开发SOP.md`（新增功能 6 步）。本文件是执行摘要，冲突时以 doc 为准。

---

## BaseMode 模式契约

一个功能 = `src/modes/` 下一个插件文件：

```python
"""
<模式中文名> - 一句话定位
（文件必须以中文 docstring 开头，test.py 强制检查）
"""
from framework.colors import CLR_BG, ...
from modes.base import BaseMode


class XxxMode(BaseMode):
    MODE_ID = "xxx"          # 与文件名、app_config id、registry 键、profile id 四处一致

    def __init__(self, display, buttons, buzzer=None):
        super().__init__(display, buttons, buzzer)

    def enter(self):
        self.display.fill(CLR_BG)   # 首行必须清屏 + 首绘

    def loop(self):
        # 返回 True 继续 / False 退出；每帧收尾 sleep_ms(30~50)
        ...
        return True
```

- 必须实现 `enter()` / `loop()`；可选重写 `exit()`（退出时 `gc.collect()` 并卸载本模式自有的大模块）。
- BaseMode 现成工具：`_scan_with_timing()`（按键采集唯一入口）、`draw_wifi_bar()`、`draw_card()`、`flash_exit()`、`beep(freq, ms)`。
- `run()` 每帧自动夹带**三个全局服务** tick（闹钟 alarm / 整点新闻 news / 云端 cloud，见 `src/modes/base.py` run()），任一服务接管屏幕后会调 `enter()` 整页重绘，模式内不用自己调。
- 崩溃隔离由 `registry.dispatch` 提供（屏显 MODE ERROR + REPL 打日志），模式内无需自救。

## 注册三处（缺一处就对不上）

| 位置 | 作用 | 谁读它 |
|------|------|--------|
| `src/app_config.py` MENU_ITEMS | 菜单编排（id/name/color/icon） | 仿真器菜单、test.py 一致性检查 |
| `src/modes/registry.py` `_MODULE_MAP` | MODE_ID → (模块, 类) | 仿真器加载模式 |
| `profiles/<p>.json` features | 构建功能清单 | build.py（自动生成部署版 registry/app_config） |

新增 `framework/<x>.py` 且被运行时用到 → 追加进 `tools/build.py` **FRAMEWORK_FILES 白名单**。模式的伴生模块（非独立模式）放 `MODES_EXTRA`。历史先例：provision / qrcode / sdcard / http_nb 都这么登记的。

## 编码硬约束（MicroPython 环境）

- **禁 f-string**（固件裁剪版不支持）；字符串拼用 `%` 或 `+`。Web 模板 `www/index.html` 占位符必须 `%(key)s`（不能带空格），字面 `%` 写 `%%`，改模板后必须重新 build。
- **避免 `with` 语句**。
- 时间一律 `time.ticks_ms()` / `time.ticks_diff()`，禁 `time.time()` 算时长。
- 像素/坐标除法用 `//`（int 结果）。
- **颜色只从 `framework.colors` import**，任何地方不得自定义色值。
- gc 时机：开机后、模式退出后、批量绘制后、png 解码后各 `gc.collect()`；长循环每 100 帧一次；**WiFi 连接期间禁止 gc.collect()**（会断连）。
- 模块级常量用 tuple（省 RAM）。
- 字体：固定 `from font import hanzi_24 as hanzi24` 等经 font 包导入；**写文案前查字库 MAP，缺字渲染为空白**（设备与仿真同款表现）。
- 依赖方向：modes 只准 import `framework`（含 colors）/ `hal` / `wifi` / `settings` / `config` / `modes/base`；**模式之间禁止互相 import**（跨模式协作经 MODE_ID + registry 调度）；framework 禁止依赖 app_config / modes。
- 命名：文件名小写下划线；类 PascalCase + `Mode` 后缀；常量 UPPER_SNAKE；私有成员 `_` 前缀；`MODE_ID` 与文件名一致。
- `settings.json` 是唯一持久化配置（不进版本控制），读写一律 `framework/settings.update()`（自动校验），**禁止直接 `open("settings.json","w")`**；`secrets.py` / `swipe_settings.json` 已废弃。

## 按键统一规范（架构文档 2.4）

原则：**短按为主，禁止新增长按**（全项目唯一例外：swipe 非运行态 A 长按切 BLE 设备；已知遗留：摩斯电码 B 长按返回待统一）。

| 页面类型 | A | B | C |
|----------|---|---|---|
| 内容浏览页 | 短按=翻页（下一项） | 短按=主操作（刷新/确认） | 短按=退出返回主菜单（先 `flash_exit()`） |
| 菜单/列表页 | 选中上移 | 确认/执行 | 选中下移（退出走页面内「退出」项） |

- 按键采集唯一入口 `buttons.scan()` / `scan_timed()`（30ms 消抖 + 15ms 最短按压）；**新页面禁止自行 `read_raw()` 比较边沿**。
- 模式交接处调用 `buttons.clear_events()`，防串键。
- 长按阈值 `LONG_PRESS_MS = 800`（仅存量功能使用）。

## UI 视觉与页面

- 240×240 屏，iOS 暗色模式风格（细节见 conventions 第 4 节）。
- 布局先出 spec 设计稿过仿真器（`designs/` 流程），确认后按稿实现。
- 播放类页面顶部无通栏（用户明确的既有偏好，改版前先确认）。

## 文档产出（新增模式完整清单）

1. 复制 `doc/模式功能文档模板.md` → `doc/<功能名>模式功能文档.md`：八节骨架（概述/页面导航/按键表/各页布局/后台服务/性能资源/数据依赖/状态已知问题）；**按键表逐项对照 `_scan_with_timing()` 源码**核实。
2. `doc/功能文档总览.md` 索引表加行：`| 功能 | MODE_ID | 功能文档 | 一句话定位 |`。
3. README 功能模块表 + 目录树。
4. `doc/项目目录结构说明.md` 文档清单。

以上与代码**同批提交**（DoD）。
