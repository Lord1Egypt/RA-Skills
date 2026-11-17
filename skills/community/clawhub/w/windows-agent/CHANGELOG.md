# windows-agent Skill — CHANGELOG / 完善记录

> 记录本 skill 的开发与完善历程。当前状态：**v0.0.1 发布版**。
> 本文档说明各轮改动、关键决策、验证结果，供 review 与后续发布参考。

---

## 当前版本：v0.0.1（发布版）

- **状态**：首发版本，已完成全板块完善与发布前整治
- **脚本**：`scripts/` 下 10 个 `.ps1`（录屏板块已切割删除）
- **平台**：Windows 11，全部 Windows 原生（user32 / UIAutomation / GDI+ / PowerShell），统一 `pwsh`(PS7) 执行
- **路径兜底**：截图目录可探测（OPENCLAW_STATE_DIR/当前目录/脚本上级/TEMP），支持 -OutputPath 自由指定
- **安全**：不含任何密钥/API/账号信息，不上传数据
- **配套文档**：`SKILL.md`（用法）+ `PREREQUISITES.md`（前置条件+使用前说明）+ `CHANGELOG.md`（本文件）

---

## 历轮完善记录

### 四~十二轮：逐板块深度测试 + 全板块验收（2026-08-29，critique_008 每项多次）

**目标**：12 板块逐一真实测试（独立脚本、可观测效果、测后清理），确认"调用就成功、出错必报清楚、无破坏性副作用"。

| 轮 | 板块 | 关键验证 |
|----|------|---------|
| 四 | screen | capture 1707x1067 / capture-region 精确尺寸 / capture-window 3/3。**确认截图=逻辑坐标, 点击用UIA物理坐标**(防DPI偏差, 写入 screen help+SKILL) |
| 五 | uiauto | dump 26控件 / find-text 物理坐标 center / **click-text 真实弹菜单** / **SendInput坐标点击(1134,314)生效** / type中文无乱码 |
| 六 | process | list/info/monitor/wait/start/kill 全通过。**info/monitor/wait 只支持 -ProcId 不支持 -Name**(补 help 提示先用 list 查 PID) |
| 七 | mouse-drag | 真实拖"哇哇哇" (632,980)→(632,1442) 下移462px。**桌面图标定位必须用 uiauto find-text**(vision换算易错); 拖拽落点受网格吸附(系统) |
| 七B | drag提速 | GitHub调研: sendinput exe不支持中文/inputsimulator需编译DLL → 都不适配。**自建 batch.ps1**: 一次启动+一次C#编译多操作。实测4操作快64%、单次drag 236ms(vs 850ms) |
| 七C | batch健壮 | 修4坑: 空序列友好提示 / N安全数字转换 / per-command参数校验(防危险点击) / 注释序列友好退出。调用不崩 |
| 八 | wait | window命中/超时/**延迟出现2s后FOUND(核心价值)**/text/control 全通过 |
| 九 | read-text | read前台/指定窗口/不存在(ERROR exit1)/菜单文本。Edit路径 ValuePattern→Text→Name 三级兜底 |
| 十 | clipboard | set中文/get/clear/set空(ERROR)闭环。**测前备份剪贴板→测后恢复**(不破坏用户内容) |
| 十一 | record | status→start→recording→stop→not recording 状态机, 录3s产9.6MB mp4。**必须5.1** |
| 十二 | 全板块验收 | **12/12 PASS**。唯一FAIL=验收脚本选前台Electron(OpenClaw Control UIA树空=已知局限), 换记事本验26控件正常, 非skill bug |

**验收脚本踩坑**: PowerShell 内置别名 `r`=Invoke-History 覆盖自定义函数 `R` → 改名 `RES` 解决(已记记忆)。

### 三轮：全板块收官（2026-08-29）

**目标**：全 10 板块逐一核对"脚本功能 / SKILL.md 文档 / 记忆调用"三者一致，做到"调用就成功、问题由 skill 消化"。

**改动**：
1. **SKILL.md 动作引用与脚本 ValidateSet 100% 对齐**
   - `vision.ps1 -Action screenshot` → `observe`（原文档写错动作，调用必报错）
   - `window.ps1 -Action list` → `list-windows`（3 处修正）
   - `open` 描述：三级 → 六级确定性链路
   - 补齐缺失动作示例：input 补 `mouse-down/up/get-pos`；uiauto 补 `invoke/find-text/click-text`；process 补 `wait`
2. **全脚本语法 + C# 编译验证**通过
3. **`record.ps1` 确认必须 5.1** 跑

**验证**：SKILL.md 动作覆盖矩阵 100%，10/10 脚本语法通过。

---

### 二轮：功能健壮性修复（2026-08-29）

**目标**：修掉"调用时真会出错"的功能性坑，而非让调用者记忆避坑。

**改动**：
1. **input.ps1 — SendInput 精准鼠标**（替代废弃 mouse_event）
   - 加 `SetProcessDPIAware()`（消除 DPI 虚拟化点偏，本机 144% = 1.5x）
   - 鼠标移动/点击/双击/滚轮/拖拽全部迁移到 `SendInput` + `MOUSEEVENTF_ABSOLUTE` 归一化坐标（0-65535，系统内部换算物理像素，天然免责 DPI）
   - 新增 `-Action get-pos`（读当前物理坐标）
2. **uiauto.ps1 — 坐标点击/填字兜底统一调 input.ps1 的 SendInput**
   - 原 `Cursor.Position`（逻辑坐标，DPI 点偏）+ `SendKeys`（中文丢字符）→ 全部换 SendInput 精准能力
   - 新增辅助函数 `Invoke-PreciseClick` / `Invoke-PreciseType`（填中文不乱码）
3. **window.ps1 — open 升级为六级确定性链路**
   - ①a shell 系统项（`explorer shell:MyComputerFolder` 开"此电脑"等，零鼠标零坐标）
   - ①b 开始菜单 .lnk → ① 桌面 .lnk（确定性启动，不碰 UIA）
   - ② 桌面图标 UIA → ②b 任务栏图标 UIA（补 3 次重试应对 UIA 不稳定）
   - ③ 截图兜底（供视觉定位）

**验证**：
- SendInput 精准移动 **9/9 零偏差**（目标 vs `get-pos` 回读 ±0）
- 点击/双击/滚轮/拖拽 各 3/3 位置精确
- **真实触发**：SendInput 点击任务栏"文件资源管理器"图标 (1446,1564) → 窗口被真实激活
- `open "此电脑"` → `OPENED(shell)` 直接打开；`open "网易发烧游戏"` → `OPENED(start-menu .lnk)`

---

### 一轮：基础能力补齐（前期已完成）

**目标**：对照 GitHub 社区方案，补齐 Windows 原生能力。

**改动**：
- 拖拽 / 智能等待 / 读窗口文本 / 按文本定位点击（全部 Windows 原生）
- `screen.ps1 capture-window` 内建**最小化窗口自适应**（IsIconic→restore→截图→minimize 复原）
- 拆掉旧 `desktop-control-win` 融入本 skill

---

## 关键决策记录

| 决策 | 内容 | 原因 |
|------|------|------|
| 全部 Windows 原生 | 只用 user32/UIA/GDI+/WinForms/PowerShell 内建，不用 Python 三方库/ffmpeg | Sunset 明确要求 |
| 统一 pwsh(PS7) | 避免 5.1 GBK 编码问题 | 中文乱码教训 |
| `record.ps1` 用 5.1 | Game Bar 热键 Win+Alt+R 在 5.1 稳定 | 平台限制 |
| 鼠标用 SendInput+ABSOLUTE | 0-65535 归一化免责 DPI；`SetProcessDPIAware` 双保险 | GitHub 调研（movemouse/precision-desktop）|
| 坐标源 UIA 物理坐标优先 | UIA `BoundingRectangle` 返回物理坐标，天然规避 DPI | 微软官方文档 + precision-desktop |
| open 六级确定性链路 | shell→开始菜单.lnk→桌面.lnk→UIA→截图 | "调用就成功"，UIA 不稳定降为兜底 |
| 能力内建到脚本/文档 | 不靠调用者记忆避坑 | Sunset 核心诉求 |
| drag 自适应段数 | 短距2段×10ms/中距6段/长距12段 | 拖拽本尊快 4.6 倍(460→100ms) |
| 批量执行器 batch.ps1 | 一次进程+一次C#编译做多操作 | 多次操作省64%(2861→1030ms), 单次drag 236ms |
| GitHub 方案取舍 | sendinput exe(不支持中文)/inputsimulator(需编译DLL)/Power Automate(GUI非API) 均不采用 | 自建 batch 最贴合"高效+中文+拖拽+原生+安全" |

---

## 已知局限（Windows 系统级，非 bug）

- **UIA 桌面图标/任务栏图标枚举不稳定**：有时能拿到全部元素，有时只剩空 Pane。已通过重试 3 次 + 确定性链路优先缓解；极端情况落到截图兜底
- **Electron 应用**（如 OpenClaw Control）UIA 坐标部分异常/树不完整：用 `vision` 截图兜底
- **桌面图标坐标**：UIA 拿不到时用 `.lnk`/开始菜单/shell 项确定性打开，避免点图标
- **Videos\Captures 删除受限**：record 测试残留 mp4 删不掉(Access denied, ACL 却 FullControl, cmd del/f 也删不掉) = 疑 Windows 受控文件夹访问/OneDrive 保护。系统安全机制, 非 skill bug, 未绕过强删

---

## 发布状态（v0.0.1）
- [x] 录屏板块切割删除及文档清理、板块重排
- [x] 路径兜底整改（可探测目录 + -OutputPath）
- [x] screen.ps1 Split-Path bug 修复
- [x] 全板块核心动作真实验证通过、语法 0 失败、help 10/10
- [x] 公化安全复核（无密钥/模型名通用化）

- [x] 12 板块深度测试 + 全板块验收（2026-08-29，已 12/12 PASS）
- [ ] real-world 真实场景回归（多应用组合操作）
- [ ] Videos\Captures 测试残留 mp4 处理（受控文件夹访问限制, 待 Sunset 手动清理或授权）
- [ ] 清理历史 tmp 残留脚本（约 18 个，非本 skill 文件）
- [ ] Sunset 确认定版与版本号（迭代由 Sunset 决定）
