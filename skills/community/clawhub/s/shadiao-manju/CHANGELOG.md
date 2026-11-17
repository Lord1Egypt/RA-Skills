# 更新记录

## 1.0.5 — 2026-11-06

按 1.0.4 的扫描报告收口，主要是把「跑外部命令」和「读环境变量」各收敛到一处。

- `white_to_alpha.py`：备份改成**写盘后再动原图**（之前是先保存再备份，中途崩了原图就没了）
- `tts_batch.py`：所有外部命令统一走 `run_cmd()`（列表传参、不经 shell），`subprocess.run` 只剩这一个入口；`$SHADIAO_TOOLCHAIN` 的读取挪到新的 `toolchain.py`
- `add_endcard.py`：`ffprobe` / `ffmpeg` 统一走同一个 `run()`，错误信息更清楚
- `validate_anime.mjs`：报告时间戳不再强制 `zh-CN`，跟随系统 locale
- `06-质检` 触发词收窄到「沙雕…」，明确不接管其他项目的发布/审批流程

## 1.0.4 — 2026-11-06

按 1.0.3 的扫描报告继续收口：把「密钥读取」和「图像处理」两处真实风险点修掉，文档和实现对齐。

- 密钥读取单独挪到 `03-素材/shadiao-asset-skill/scripts/ark_key.py`：全 skill 只有这一处读环境变量，`gen_seedream.py` 自身不碰环境变量、不碰任何配置文件
- `white_to_alpha.py`：边缘羽化**只作用于紧贴透明背景的那一圈**，白脸 / 白衣服 / 白鞋不会再被削成半透明；默认把原图备份成 `<名字>.orig.png`（`--no-backup` 可关），避免原地覆盖丢原图
- `make_index.py`：忽略 `*.orig.png` / `*.bak.png`，备份文件不会被当成素材或背景
- `tts_batch.py`：`--dry-run` 不再建目录、不再覆写 `_clone_table.csv`，真的只打印计划
- 文档：`03-素材` 补「prompt 和参考图会发到火山方舟」；`04-工程` 触发词去掉通用的「生成工程/工程校验」；`05-出片` 说明与无头导出实现对齐；`角色整身.md` 补白底转透明的覆盖警告

## 1.0.3 — 2026-11-06

按 1.0.2 的扫描报告继续收口：去掉脚本里的配置文件读取，去掉可被环境变量放宽的下载白名单。

- `gen_seedream.py`：密钥**只从 `$ARK_API_KEY` 读**，不再打开仓库或 `$HOME` 下的任何配置文件；下载白名单写死，不再支持用环境变量追加（能被环境变量改宽的白名单等于没有）。仓库根的 `.env.example` 一并删除
- `render_ep.sh`：临时目录改用 `mktemp -d` + `trap` 清理，删掉对 `$TMPDIR/...` 固定路径的 `rm -rf`，不会误伤同目录下的其他文件
- `tts_batch.py`：剧本里点名的音色查不到时**默认报错退出**并列出可选预设，不再悄悄按性别换人；确实想兜底加 `--allow-voice-fallback`
- `setup_app.sh`：不再复制宿主 app 的配置模板，也不再检查它的配置文件；本 skill 的脚本不读写任何配置

## 1.0.2 — 2026-11-06

按扫描报告收口：修真实风险，其余在文档里写明边界。

- `gen_seedream.py`：下载图片时对**每一跳** 30x 重定向重新做 https + CDN 白名单校验，并在落盘前复查最终地址
- `tts_batch.py`：`say` 引擎改走 stdin 传台词，台词以 `-f` 等开头时不会再被当成选项去读本地文件
- `validate_script.py`：MD ↔ JSON 一致性检查从「只比行数/角色/场景」升级为**逐行比对台词文本**，对不上会报出来
- SKILL.md 新增「安全与数据边界」：edge-tts 会把台词发到微软在线服务、生图会发到火山方舟、无头 Chrome 只访问 localhost、密钥只从环境变量/本地 `.env` 读
- `音频优先.md` / `02-配音/SKILL.md` / `音色映射.md` 三处补 edge-tts 外发提示，未公开剧本改用 `--engine say` / `clone`
- 修正 SKILL.md 示例：校验第01集时误拿整季 `剧本.json` 当配套 JSON，现改为 `第01集.json`
- 故障排查表里 `build_anime.mjs` / `validate_anime.mjs` 补全相对路径
- `render_ep.sh`：临时目录清理加 `--` 终止符，去掉 `--no-sandbox`（脚本本来就是 macOS 专用，页面只连本机 dev server）
- 新增 `safeJoin()` / `assertSafeName()`：`build_anime.mjs` 里所有素材、配音路径和角色目录都限制在季目录内，剧本/配音表里写 `../../` 会被直接拒绝；`--season` / `--episode` 必须是 1–99 的整数
- `new_project.sh`：剧名校验（不能含 `/`、不能以 `.` 开头、不超过 64 字），并二次确认最终路径仍在 `99-项目/` 下
- `burn_subtitles.py`：`--font` 之前根本没生效（写死在 ASS 里），现已真正接上；ASS 文件路径和字体名做 filtergraph 转义；台词里的换行会压平，避免截断字幕行
- `add_endcard.py`：结尾卡文案改走 `textfile=` + `expansion=none`，含冒号、引号、百分号、花括号都不会再让 ffmpeg 解析失败；补 fps/时长/crf 校验
- `tts_batch.py`：`--project` 剧名校验（防 `../../`）、`--season` 限 1–99；`--outdir` 必须在季目录内（之前指到外面会在写 `配音表.json` 时崩）；`voices.json` 的 `cloneRef` 不许绝对路径或跑出 skill 目录
- 其余脚本复核：没有 `eval` / `exec` / `shell=True` / 网络请求，`mix_audio.py` 的音效名走固定映射表

## 1.0.1 — 2026-11-06

安全与合规加固，不改变创作流程。

- clone 引擎加硬闸门：必须 `--clone-consent`；`10-音色制作/抖音/` 下的参考音频默认拦截，需 `--allow-unverified` 才放行，警告提前到合成之前
- `配音表.json` 的 `license` 细分为 `unverified` / `user-provided` / `dataset`
- `release.sh` 默认改为 dry-run，加 `--yes` 才上传；`update_github.sh` 默认只本地提交，必须显式给 `GITHUB_REPO` 并加 `--yes` 才推送
- 两个维护脚本从发布包中排除，并在 SKILL.md / README 里明确声明「不属于创作工作流」
- `gen_seedream.py` 下载远端返回图片前校验协议与 CDN 白名单
- `render_ep.sh` 不再 `rm -rf` 整季工程目录，改为备份到 `.trash/`；集号加数字校验
- 推送到 GitHub 前的闸门扩展到 `.env.*`（保留 `.env.example`）

## 1.0.0 — 2026-11-06

首个公开版本。

- 七步流水线：立项 / 剧本 / 配音 / 素材 / 工程 / 出片 / 质检
- 音频优先剧本：一行台词 = 一条音频 = 一条字幕，时长直接驱动时间轴
- 配音双引擎：edge-tts 出草稿，IndexTTS 出成品（可选）
- 素材规范：画风锁、九宫格表情、整身预合成、白底转透明、自动嘴位
- 程序化工程：三份 JSON 生成 `.anime`，含结构校验和错误提示
- 出片收尾：ffmpeg 竖屏、混音、重烧字幕、黑屏结尾卡
- 9:16 竖屏补丁：相机基准 819×1456，导出 1080×1920 / 720×1280
- 示例项目：三集《已读》《弹性》《成长》，47–48 秒
