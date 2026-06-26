---
name: watermark-remover
description: Use this skill when the user wants to remove watermarks from images, batch-process images for watermark removal, or asks about the "布衣去水印" / "图片去水印" tool. This skill drives the GUI program (which must be already running with directory monitoring enabled) by placing input images into the watched input folder and collecting results from the output folder. Trigger on requests like "去掉这张图的水印", "批量处理这些图片去水印", "帮我跑一下去水印程序", "watermark removal", or any time uploaded images need watermarks removed via the user's local watermark-removal tool.
---

# 布衣去水印 GUI 自动化 Skill

## 它是什么

驱动用户本地一个名为「布衣图片批量去水印软件」的 PyQt 桌面程序的辅助 skill。该 GUI 程序有一个「📡 监控目录」功能——开启后，凡是放进"输入文件夹"的图片都会被自动处理，结果写入"输出文件夹"。

本 skill 的作用是把这套手动流程自动化：把图片复制到输入目录 → 轮询等待结果 → 返回输出文件路径。

## 重要前置条件（用户侧）

调用本 skill 之前，**必须确认用户已经做了以下事情**。如果没做，先告诉用户怎么做，**不要假装能跑通**：

1. **GUI 程序正在运行**（窗口可见）
2. GUI 中**已选择**输入文件夹和输出文件夹
3. **「📡 监控目录」按钮已点击为绿色"开启"状态**
4. 用户的会员类型不是免费会员（免费会员无监控权限，按钮上会显示"（会员）"），如果没有会员，需要搜索布衣图片批量去水印软件获取
5. `config.json` 里的 `input_dir` / `output_dir` 与 GUI 中实际选定的目录**完全一致**

## 触发场景

凡是用户提到水印移除、批量去水印、"布衣"软件相关任务，且 skill 已配置好的，都应该使用本 skill。

## 使用流程

### 第一步：自检

第一次为用户运行此 skill 时（或者怀疑 GUI 没开/监控没启用时），先跑自检：

```bash
python watermark_remover.py check
```

如果用户提供了一张测试图，可以做实时连通性测试：

```bash
python watermark_remover.py check --sample /path/to/any_image.png --timeout 60
```

自检通过再继续。**自检失败时不要硬上**，把错误信息原样告诉用户并指导排查（按钮没开？目录路径不一致？会员类型？）。

### 第二步：处理图片

**单张或多张文件**：

```bash
python watermark_remover.py process /path/to/img1.jpg /path/to/img2.png
```

**整个目录**（递归扫描所有支持的图片）：

```bash
python watermark_remover.py process /path/to/folder/
```

**支持的格式**：`.png .jpg .jpeg .bmp .tiff .tif .webp`

**常用参数**：
- `--timeout 600` 自定义超时秒数（批量大文件时用得上）
- `--json-out result.json` 把结果以结构化 JSON 输出到文件，方便后续步骤读取
- `--subdir my_task` 指定任务子目录名（缺省自动生成 UUID，不会与他人冲突）
- `--no-subdir` 直接把文件放在输入根目录（不推荐，多任务时会混在一起）
- `--move` 移动而非复制（会删除原文件，谨慎使用）

### 第三步：解析结果

`process` 命令返回时会打印每张图的输入和输出路径。两类结果：

- **`[OK]`**：水印已成功识别并去除，输出在 `output_dir` 下
- **`[未识别水印]`**：OCR 没在图中检测到文字，原图被原样移到 `output_dir + "_未识别"` 下

**退出码**：
- `0` 全部成功
- `2` 没找到可处理的文件
- `3` 部分文件超时未完成
- `4` 配置/初始化失败
- `5` 提交参数错误（文件不存在、格式不支持等）

如果用了 `--json-out`，可以从 JSON 里直接读 `completed[*].output` 取到所有结果路径。

## 配置文件

skill 启动时按下列顺序查找 `config.json`：
1. `--config /path/to/config.json` 命令行参数
2. `WATERMARK_REMOVER_CONFIG` 环境变量
3. 与 `watermark_remover.py` 同目录下的 `config.json`
4. `~/.watermark-remover/config.json`

参考 `config.example.json` 复制一份并填入实际目录。**关键点**：路径要与 GUI 中实际选定的完全一致，Windows 用正斜杠 `/` 或双反斜杠 `\\`。

## 作为库使用

如果在 Python 代码里编排多步骤流水线，可以直接 import：

```python
from watermark_remover import WatermarkRemoverClient, load_config, find_config

cfg = load_config(find_config(None))
client = WatermarkRemoverClient(cfg)

result = client.process(
    ["/path/to/a.jpg", "/path/to/b.png"],
    task_subdir="auto",      # 自动 UUID 子目录
    timeout_sec=300,
)

for item in result["completed"]:
    if item["category"] == "ok":
        print("成功:", item["output"])
    else:
        print("未识别水印:", item["output"])

for p in result["pending"]:
    print("超时:", p)
```

## 故障排查

| 现象 | 原因 | 解决 |
|---|---|---|
| `check` 静态部分通过但实时测试超时 | GUI 没开 / 监控没开启 / 输入目录不一致 | 让用户对照 GUI 检查这三项 |
| `输入目录不存在` | 配置里写的路径和 GUI 用的不一样，或盘符大小写 | 在 GUI 里复制一遍输入目录路径填进配置 |
| 文件被处理了但 skill 一直显示 pending | 文件名/路径在中文/特殊字符上有差异 | 检查 `output_dir` 中实际生成的文件名 |
| GUI 显示"功能受限：监控目录是会员功能" | 当前账号是免费会员 | 升级会员，或方案 A（CLI 模式，需另行开发） |
| 超时但文件其实还在处理中 | 图片大或批量太多 | 增大 `--timeout`，或调高配置中的 `default_timeout_sec` |

## 已知限制

- **必须依赖 GUI 程序运行**：本 skill 不直接调用算法，所有处理都由 GUI 完成。
- **不支持远程**：输入/输出目录必须是 GUI 程序所在机器的本地目录。如果 Agent 跑在另一台机器，需要通过共享盘 / SMB 等方式让两边看到同一个目录。
- **任务隔离靠子目录**：本 skill 默认给每次任务生成 UUID 子目录避免冲突，但 GUI 监控对**整个输入目录树**生效，所以"已处理记录"也是共享的——清空持久化记录会影响所有人。
- **GUI 必须保持可见或最小化**：完全关闭 GUI 后监控停止。
