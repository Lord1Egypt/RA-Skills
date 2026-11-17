# workbuddy-skin

给自己写的 WorkBuddy 换肤工具。CDP 运行时注入，不改 `app.asar`，重载即还原。

## 当前皮肤：机甲壁纸 + 深色玻璃

- 机甲壁纸铺底（挂 body），全局深色基底，accent 紫 `#7C5CFC`
- 顶部日历条：周视图、今天紫色高亮、‹ › 翻周、点日期高亮当天任务；与对话标题栏全透明融入壁纸
- 侧栏入口（新建任务 / 助理 / 项目 / 专家·技能·连接器）→ Arc 风方块磁贴
- 敲木鱼：跟随输入框（纵轴对准输入框中心，横轴居中于输入框-窗口右缘间隙），间隙不够或右侧面板打开时自动隐藏；音效 + 功德计数持久化
- 对话消息：整组垫深色玻璃阅读面板；用户气泡暗紫玻璃
- 新对话输入框：近透明薄膜（0.04 白 + 4px 模糊）

## 使用

```bash
node src/apply.mjs   # 应用（会先把 WorkBuddy 重启为调试模式，任务先保存）
node src/pause.mjs   # 还原官方外观（重载界面）
```

或双击 `scripts/apply.command`。

### 自动换肤（推荐）

```bash
bash scripts/install-flag.sh    # 一次性：给 WorkBuddy 加启动引子，任何方式启动都自带调试端口
bash scripts/install-auto.sh    # 开启：注册 LaunchAgent，以后正常打开 WorkBuddy 自动换肤
bash scripts/uninstall-auto.sh  # 关闭自动换肤；scripts/uninstall-flag.sh 还原启动引子
```

看守脚本常驻后台（日志 `scripts/watch.log`），检测到 WorkBuddy 新进程就自动注入，**不重启 app**，打开后 ~14s 皮肤生效。
**给小白装机**：目标机器需有 Node.js（无则 `brew install node`），依次跑 install-flag.sh + install-auto.sh 即可。WorkBuddy 自动更新会覆盖启动引子，需重跑 install-flag.sh。

**注意**：WorkBuddy 完全重启后注入消失，重跑 apply 即可（装了自动换肤则无需手动）。

## 结构

- `src/theme.css` — 配色与磁贴/日历/消息面板样式（改皮肤主要改这里）
- `src/inject.js` — 注入 payload：挂载样式、切深色基底、日历组件、木鱼
- `src/apply.mjs` — 确保调试模式 + 注入
- `src/pause.mjs` — 还原
- `scripts/watch.sh` — 自动换肤看守循环；`scripts/install-auto.sh` / `uninstall-auto.sh` 注册/卸载 LaunchAgent
- `scripts/install-flag.sh` / `uninstall-flag.sh` — 安装/还原启动引子（Electron.real 改名 + 转发脚本附调试端口）
- `tools/cdp.mjs` — 调试工具，对 renderer 执行任意 JS
- `tools/shot.mjs` — 截图（窗口隐藏时 captureScreenshot 会挂，先 activate）
- `assets/bg.jpg` — 机甲壁纸；`assets/muyu.wav` — 木鱼采样

## 技术要点

- WorkBuddy 是 Electron，`--remote-debugging-port=9223` 启动后经 CDP `Runtime.evaluate` 注入
- DOM 锚点：`[data-view-id]`、`.teams-content-wrapper`、`.conversation-list-tab-row`、`[class*=_editable]`
- 配色覆盖 `--cb-*` 变量；深浅色基底是 html/body 上的 `dark cb-dark vscode-dark` class
- **backdrop-filter 会创建堆叠上下文**：给容器加模糊时小心把内部弹层（z-index 再高也会被"关"进该上下文）压到别的层下面。弹层容器要用 `:has(> [class*=_menu_])` 豁免
- 原生组件常用 `!important` 内联主题，覆盖时要比拼选择器优先级（如 `.x.x.x` 三连接类名）
- 页面 CSP 禁 data: URL 媒体，木鱼音效走 WebAudio decodeAudioData 播放 PCM WAV

## 素材来源

- `assets/muyu.wav` — 木鱼采样：用户提供（爱给网「古风 木鱼 寺庙」），取三声中第一声裁剪至 0.7s，PCM WAV
- `assets/bg.jpg` — 机甲英雄壁纸（用户提供无水印版，1920w/q82 优化至 ~580KB）
