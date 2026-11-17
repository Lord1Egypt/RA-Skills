---
name: xianmubox-dev
description: 闲沐盒子（本仓库）全流程开发工作流——需求梳理、方案制定、实施开发、设备调试、上传部署。凡在本项目提出新功能、新模式、界面改版、修 bug、真机排查、推送设备、构建部署等开发请求时使用，即使用户没有明说"走流程"；本 skill 规定各阶段的门禁与命令，跳过阶段会违反项目强制约定（UI 先仿真、test.py 全绿、文档同批同步、禁 GUI 提交）。
---

# 闲沐盒子全流程开发

一个开发请求按六个阶段推进。**先按用户请求定位入口阶段**：
新功能/新模式从 Stage 1 进入；真机异常、修 bug 从 Stage 4 进入；「把代码推到设备」从 Stage 5 进入。
无论从哪个阶段进入，Stage 0 的门禁贯穿全程，收尾（Stage 6）不可省略。

| 阶段 | 做什么 | 门禁（不过不许往下走） |
|------|--------|----------------------|
| 1 需求梳理 | 问清交互 / 数据源 / 字库 / 硬件 | scope 未与用户确认，不动手 |
| 2 方案制定 | 出方案并获批 | 非小改动方案未批准，不写码 |
| 3 实施开发 | 写码 + 注册 + 仿真回归 | `tools/test.py` 不全绿，不构建 |
| 4 设备调试 | 串口诊断、定位根因 | 未定位根因，不盲改代码 |
| 5 上传设备 | 备份 → 构建 → 快推 | 未备份 settings.json，不部署 |
| 6 收尾 | 文档同步 + 命令行提交 | 文档未同步 = 任务未完成 |

---

## Stage 0 · 贯穿全程的门禁

这四条是项目强制约定（AGENTS.md），任何阶段都适用：

1. **UI 一律先仿真后烧录**：任何界面改动先过 `tools/simulator/`（GUI 人工确认或无头截图自检），确认后才上真机。仿真不行就是不行，不存在"真机上看看再说"。
2. **`python tools/test.py` 必须全绿**：提交与构建前的静态质量门。已知例外：`secrets.py` 缺失导致的 1 项 FAIL 属预期，不算红；其余任何红都不许继续。
3. **文档同批同步**：功能 / 接口 / 结构改动必须在同一批提交里更新对应文档（对照 AGENTS.md 的同步表），事后补 = 未完成。
4. **提交只走命令行**：`git add -A` + `git commit -F <文件>`。禁用 GUI「版本提交」——本仓库 31 个中文名文件会被客户端 UTF-8 分块解码缺陷损坏（与 `core.quotepath` 无关，勿往该方向排查）。

---

## Stage 1 · 需求梳理

目标：把一句话需求变成可实施的明确 scope。**先查现状再提问**——很多需求已有现成模式或 framework 服务，避免重复造轮子。

动笔前先自查（读代码 / 文档，不用问用户）：

- 现有 13 个模式（`profiles/full.json` features）是否已有近似功能？能否扩展而非新建？
- `src/framework/` 已有 18 个服务模块能否复用：colors / hal / wifi / settings / http_server(+http_server_state) / http_nb / alarm / cloud / news / audio（play_wav/play_mp3）/ radio / story / weather / sdcard / provision / qrcode / moon。
- 数据源是否可达：外部 API 现在通不通、返回字段结构、设备端 5s 超时约束。

必须与用户确认的四件事：

1. **交互与按键**：内容浏览页 A 短按翻页 / B 主操作 / C 退出；菜单列表页 A 上移 / B 确认 / C 下移。**禁止新增长按**（全项目唯一例外：swipe 非运行态 A 长按切 BLE 设备）。与规范不符的交互要求要当场指出。
2. **文案用字**：240×240 屏用嵌入字库，**缺字渲染为空白且真机仿真同款**。界面文案确定前查字库 MAP（`src/font/`），缺字要么换词要么先补字模。状态类小字用 vga 字库同理。
3. **硬件边界**：涉及引脚 / 接线时对照 `doc/完整接线总表.md`（引脚总表见 `doc/esp32s3zero引脚说明.md`）。本板仅引出 GPIO 1-18 / 38-45，空闲池 = **2**（唯一空闲 ADC1 脚）/ **14/15/16**（I2S 迁移后释放）/ **41/42**；43/44 留作串口调试；板载 WS2812 = GP21。
4. **配置与持久化**：需要记住的配置进 `settings.json`（唯一持久化，经 `framework/settings.update()` 读写并受校验），临时状态不落盘。

产出：一句话 scope + 预期改动文件清单（草案即可）。

## Stage 2 · 方案制定

按改动量分级，**不要什么都直通实施**：

- **小改动**（改文案、调布局参数、修明显 bug）：说清改法直接进 Stage 3。
- **常规功能**（新页面 / 改交互 / 换数据源）：先给方案——MODE_ID 命名、页面结构、按键表、数据契约、涉及文件清单——**用户认可后再写码**（用计划模式或对话确认均可）。
- **重大变更**（新硬件 / 改架构 / 改 settings 结构 / 换引脚）：必须先出书面方案：
  - 硬件类：仿照 `doc/I2S引脚调整实施方案.md` / `doc/SD卡模块实施方案.md` 写《实施方案》文档（引脚选择依据、接线表、实施/验证状态）。
  - UI 类：走设计稿流程——设计转 spec JSON 放 `designs/`，`python tools/simulator/run.py --spec designs/xxx.json` 渲染，对话内迭代到满意，**spec 存档为实现唯一对齐依据**。

方案要落定的要素：MODE_ID（= 文件名 = 类名去 Mode 后缀的对应关系）、新增还是复用 framework 服务、数据字段契约、注册点与白名单（见 coding-rules.md）、文档同步清单。

## Stage 3 · 实施开发

标准序列（细节与代码契约见 `references/coding-rules.md`，动手前必读）：

1. 写 `src/modes/<x>.py`：继承 `modes/base.BaseMode`，实现 `enter()` / `loop()`，文件以中文 docstring 开头。
2. **三处同步注册**（缺一处仿真或部署就会对不上）：
   - `src/app_config.py` MENU_ITEMS 加一行（仿真器读这里）
   - `src/modes/registry.py` `_MODULE_MAP` 加一行（仿真器读这里）
   - `profiles/<p>.json` features 加一条（部署构建权威；build 产物里的 registry/app_config 由它自动生成）
   - 新增 `framework/<x>.py` 被运行时用到，须在 `tools/build.py` 的 FRAMEWORK_FILES 白名单登记，否则部署后 ImportError。
3. **仿真确认**：
   - 人工点按：`python tools/simulator/run.py --mode <x> --zoom 3`（键盘：← 或 a=A，回车/b/空格=B，→/c/Esc=C；`--list` 看已注册模式）
   - 回归断言：照 `tools/_sim_sn.py` 模板写 `tools/_sim_<x>.py`（stub 环境 + 按键脚本驱动 loop + 截图到 `tools/shots/` + PASS/FAIL 计数退出码），运行 `python tools/_sim_<x>.py`。
   - 改了已有模式 UI 的，把对应的既有 `_sim_*.py` 也跑一遍防回归。
4. **质量门**：`python tools/test.py` 全绿（secrets 1 项预期 FAIL 除外）。不绿不进 Stage 5。

编码红线速记（全文见 coding-rules.md）：禁 f-string；时间用 `time.ticks_ms()/ticks_diff()`；模式退出 `gc.collect()` 并卸载自有大模块；颜色只从 `framework.colors` import；模式之间禁止互相 import。

## Stage 4 · 设备调试

从症状到根因，**先诊断后改码**。连接方式、诊断脚本清单、全部已知坑见 `references/device-debug.md`，常用入口：

```bash
# 硬件/专项诊断（只依赖 machine+json，框架坏了也能跑）
python -m mpremote run tests/hw_selftest.py      # 全外设自检 T0-T6
python -m mpremote run tests/sd_diag.py          # SD 逐层定位 S0-S3
python -m mpremote run tests/mp3_diag.py         # 音频解码链路

# 不打断摆件主程序的 REPL（raw REPL 提交，不软复位）
MPPORT=COM5 python D:/Mycode/MicroPython/esp32-build/repl_util.py exec "<代码>"
MPPORT=COM5 python D:/Mycode/MicroPython/esp32-build/repl_util.py run tests/xxx.py 30
```

调试纪律：一次只改一个变量；网络类异常先区分「接口抖动」与「代码 bug」（设备端 HTTP 5s 超时，重试能恢复的多为抖动）；模式崩溃不会拖垮整机（registry.dispatch 捕获，屏显 MODE ERROR + REPL 打 `[DISPATCH] ... crashed`），所以黑屏不等于死机，先看串口日志。

## Stage 5 · 上传设备

标准部署序列（工具细节与快慢路径对比见 `references/toolchain.md`）：

```bash
# 1. 备份设备配置（部署会用仓库脱敏骨架覆盖设备 settings.json，闹钟/WiFi/云激活会丢！）
python -m mpremote cp :settings.json ./settings.backup.json

# 2. 构建（产物在 build/esp32s3_n8r8_full/，须 BUILD SUCCESS）
python tools/build.py --profile full --device esp32s3_n8r8

# 3. 快推（单连接秒级批量，完成自动软复位进应用）
python tools/fast_push.py COM5 build/esp32s3_n8r8_full /

# 4. 部署后确认 settings.json 已从备份恢复（settings.device-backup.json 为恢复源惯例）
```

备选路径：

- 慢路径 `python tools/deploy.py --profile full --port COM5`：mpremote 每文件一次连接、设备反复重启、易被开机动画抢窗口，仅 fast_push 不可用时用。
- 单文件热修：`python -m mpremote cp src/modes/<x>.py :modes/<x>.py` + `mpremote reset`。只修一个文件时用，注意 src 与 build 产物要保持同源。

涉及**固件本身**（烧 .bin / 换分区）：先在 `doc/固件版本履历.md` 登记版本（双归档 MD5 一致）再烧录，烧后回填真机验证状态；`erase_flash` 或分区表变更会清文件系统，烧完必须重新部署应用并恢复 settings。

部署后必做真机回归：进退出目标模式 5 次确认无内存泄漏与状态残留，核心功能走一遍。

## Stage 6 · 收尾（DoD）

1. **文档同步**（对照 AGENTS.md 表，未同步 = 任务未完成）：
   - 新增模式：复制 `doc/模式功能文档模板.md` 建 `doc/<功能名>模式功能文档.md`（按键表**逐项对照源码**核实）→ 登记 `doc/功能文档总览.md` 索引 → README 功能模块表与目录树 → `doc/项目目录结构说明.md`。
   - 改既有模式：同步该模式功能文档对应章节；framework / settings / HTTP / 约定类改动按 AGENTS.md 表逐项对号。
2. **提交**：`git add -A` + `git commit -F <UTF-8 文件>`（命令行，禁 GUI）。提交信息用 `类型(范围): 描述` 格式（feat/fix/docs/chore，参照既有历史）。
3. 向用户报告：改了什么、仿真与测试结果、真机验证还差哪些步骤。

---

## 参考文件（按需读）

- `references/coding-rules.md` —— Stage 3 动手前必读：BaseMode 契约、三处注册细则、编码硬约束、按键规范全文。
- `references/toolchain.md` —— Stage 5 部署前必读：build / test / 仿真 / fast_push / deploy / esptool 全参数与坑。
- `references/device-debug.md` —— Stage 4 必读：串口连接选型、诊断脚本清单、mpremote 补丁等已知坑全文。
