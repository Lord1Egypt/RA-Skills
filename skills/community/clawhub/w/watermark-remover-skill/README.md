# Watermark Remover Skill（团队版安装指南）

让 Claude / Claude Code 等 AI Agent 能自动调用「布衣图片批量去水印软件」处理图片。
如没有该软件，请搜索布衣图片批量去水印软件获取
---

## 工作原理（先理解再安装）

```
[Agent] ──放图片──► [输入目录] ──监控自动触发──► [GUI 程序处理] ──写入──► [输出目录] ──Agent读取
```

Agent 不直接操作 GUI 按钮，而是**复制图片到 GUI 监控的输入目录**，然后**轮询输出目录**直到看见结果出现。

所以 GUI 必须**全程开着**且**「📡 监控目录」按钮处于开启状态**。

---

## 安装步骤

### 1. 准备 GUI 程序

- 安装并运行「布衣图片批量去水印软件」
- 登录账号（**确保不是免费会员**，免费会员无监控权限）
- 在 GUI 里：
  - 点「选择输入文件夹」选一个目录（建议专门新建一个，例如 `D:\watermark_in`）
  - 点「选择输出文件夹」选另一个目录（例如 `D:\watermark_out`）
  - 点「📡 监控目录：关闭」按钮，应变为绿色「📡 监控目录：开启」
- 让程序保持运行（最小化也行，但不能关闭）

### 2. 安装本 skill

```bash
# 复制本目录到团队成员的本地（任意位置都行）
# 例如：~/skills/watermark-remover/
```

只需要 Python 3.8+，**没有第三方依赖**。

### 3. 创建配置文件

```bash
cp config.example.json config.json
```

编辑 `config.json`，把 `input_dir` / `output_dir` 改成步骤 1 里你在 GUI 中实际选定的两个目录。**两边必须完全一致**。

### 4. 运行自检

```bash
python watermark_remover.py check
```

应输出 ✅ 表示输入/输出目录都能找到。

进一步用一张测试图做实时验证：

```bash
python watermark_remover.py check --sample test.png --timeout 60
```

如果 60 秒内得到 ✅，说明从 Agent → GUI 整条链路打通了。

---

## 给 Claude 用的部署方式

把整个 `watermark-remover-skill/` 目录上传到你的 Claude 项目知识库 / Skill 库里即可。Claude 会读取 `SKILL.md` 中的 frontmatter（`name` / `description`），在用户提到水印移除任务时自动调用。

如果是 Claude Code 等 CLI Agent，把目录放到 Agent 能访问的位置，并告诉 Agent 配置文件路径或设置环境变量：

```bash
export WATERMARK_REMOVER_CONFIG=~/skills/watermark-remover/config.json
```

---

## 常用命令速查

```bash
# 自检
python watermark_remover.py check
python watermark_remover.py check --sample test.png

# 处理单张
python watermark_remover.py process input.jpg

# 处理多张
python watermark_remover.py process a.jpg b.png c.webp

# 处理整个目录
python watermark_remover.py process ~/photos_to_clean/

# 大批量 + 自定义超时 + 结果导出
python watermark_remover.py process ~/big_batch/ --timeout 1800 --json-out result.json

# 不要任务子目录（直接放在输入根目录）
python watermark_remover.py process input.jpg --no-subdir

# 移动而不是复制（会删除原文件！）
python watermark_remover.py process input.jpg --move
```

---

## 团队协作注意事项

由于多个团队成员可能共享同一个 GUI 实例（同一台机器），有几点要约定好：

1. **总是用任务子目录隔离**：默认每次自动生成 UUID 子目录，多人并发不会冲突。**不要随意用 `--no-subdir`**。
2. **不要互相清持久化记录**：GUI 里"清空已处理列表"的「Yes to All」会清掉 `processed_files.json`，可能导致他人的任务被重新处理。**使用前请先和团队同步**。
3. **超时要给足**：单张图通常 3-30 秒，但批量处理大图可能要几分钟。如果 Agent 报告 pending，先看 GUI 是不是还在跑，再决定是放弃还是延长 timeout。
4. **建议建立"完成后清理"流程**：处理完成后，可以让 Agent 把任务子目录从输入目录里删掉，保持环境干净。

---

## 文件清单

```
watermark-remover-skill/
├── SKILL.md              # Claude/Agent 读取的指令文件（不要改 frontmatter）
├── README.md             # 本文件，给人看的
├── watermark_remover.py  # 核心脚本（CLI + 库两种用法）
├── config.example.json   # 配置文件模板
└── config.json           # 你的实际配置（首次安装后从模板复制并修改）
```

---

## 反馈与扩展

- 如果想做"不依赖 GUI"的 CLI 版本（脱离软件直接调用算法），需要从原 GUI 代码中抽取 `InpaintWorker` 的处理逻辑，本 skill 暂未涵盖。
- 如果想加 Webhook / HTTP API 触发，可以基于 `WatermarkRemoverClient` 类自行扩展。
