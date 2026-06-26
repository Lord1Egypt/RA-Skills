---
name: yoloutils
description: 基于 yoloutils 的命令级技能。用户需要执行 yoloutils 的 label、merge、copy、remove、change、crop、labelimg、resize、classify、test 任一子命令时使用。以源码真实行为为准，提供每个子命令的参数定义、执行逻辑、副作用、限制和示例。
---

# YOLOUtils（源码版）Agent Skill

本技能只以 `src/netkiller/yoloutils.py` 为准，不以外部文档为准。

## 1. 入口与总原则

1. 入口命令优先使用 `yoloutils <subcommand> ...`。
2. 若本地未安装入口脚本，可使用 `python src/netkiller/yoloutils.py <subcommand> ...`。
3. 子命令共有 10 个：`label`、`merge`、`copy`、`remove`、`change`、`crop`、`labelimg`、`resize`、`classify`、`test`。
4. 涉及目录批处理时，优先先在小样本目录试跑，再全量执行。

## 2. 预检查（所有命令通用）

执行前先检查：

1. Python 依赖可用：`opencv-python`、`pyyaml`、`pillow`、`texttable`、`tqdm`、`ultralytics`。
2. 输入目录存在且可读，输出目录可写。
3. 涉及 YOLO 标签映射时，确认 `source/classes.txt` 存在。
4. 涉及模型推理时，确认 `--model` 路径存在且可加载。
5. 使用 `--clean` 前确认输出目录可被删除。

## 3. 子命令详细用法

### 3.1 `label`

用途：查看类别、统计标签索引计数、按索引检索标签文件。

命令原型：

```bash
yoloutils label --source <dir> [--classes | --total | --index | --search <idx...>]
```

参数：

- `--source`：目录（必需）。
- `--classes`：读取并输出 `source/classes.txt`。
- `--total`：递归统计所有 `.txt`（排除 `classes.txt`）中的标签框数量。
- `--index`：调用同一统计流程，但输出“索引-数量”表。
- `--search`：按字符串索引（如 `0 2`）查找出现该索引的标注文件。

执行行为（源码）：

1. `main()` 分支优先级是：`--classes` > `--total` > `--index` > `--search`。
2. `--total/--index` 都递归扫描 `source/**/*.txt`。
3. 不带 `--index` 的统计会尝试用 `classes.txt` 把索引映射为标签名。
4. `--search` 只把命中的索引输出为 “索引-文件列表”。

示例：

```bash
yoloutils label --source ./dataset --classes
yoloutils label --source ./dataset --total
yoloutils label --source ./dataset --index
yoloutils label --source ./dataset --search 0 3
```

---

### 3.2 `merge`

用途：把左侧目录与右侧目录的标签合并到输出目录，并复制左侧图片。

命令原型：

```bash
yoloutils merge --left <left_dir> --right <right_dir> --output <output_dir> [--clean]
```

参数：

- `--left`：左侧目录（必需）。
- `--right`：右侧目录（必需）。
- `--output`：输出目录（源码中实际必需）。
- `--clean`：执行前清空输出目录。

执行行为（源码）：

1. 仅扫描 `left/*.txt` 和 `right/*.txt`，不递归。
2. `classes.txt` 会从左侧直接复制到输出。
3. 每个标签文件会先复制左侧同名 `.jpg` 到输出。
4. 右侧匹配规则是把左侧文件名中的 `"_0."` 替换为 `"."` 后再查找。
5. 若右侧不存在匹配文件，仅复制左侧标签；存在则把两个文本内容直接拼接写入输出。

示例：

```bash
yoloutils merge --left ./left --right ./right --output ./merged --clean
```

注意：

- `main()` 只检查了 `left/right`，但 `input()` 会使用 `output`；不传 `--output` 会报错。

---

### 3.3 `copy`

用途：按标签名称复制样本，或全量复制标签文件与配对图片。

命令原型：

```bash
yoloutils copy --source <src> --target <dst> [--label <name1,name2>] [--uuid] [--clean]
```

参数：

- `--source`：源目录（必需）。
- `--target`：目标目录（必需）。
- `--label`：逗号分隔标签名列表，例如 `person,dog`。
- `--uuid`：输出标签文件名改为 UUID。
- `--clean`：清空目标目录。

执行行为（源码）：

1. 启动时读取 `source/classes.txt`，把标签名映射到索引。
2. 递归扫描 `source/**/*.txt`（跳过 `classes.txt`）。
3. 若设置 `--label`，只要文件中存在任意目标索引就复制该样本。
4. 结束时会把 `source/classes.txt` 复制到 `target/classes.txt`。
5. 图片按 `.txt -> .jpg` 推导复制。

示例：

```bash
yoloutils copy --source ./dataset --target ./picked --label cat,dog
yoloutils copy --source ./dataset --target ./picked --label person --uuid --clean
```

注意：

- 标签名若不在 `classes.txt` 中，命令直接退出。
- 代码中图片复制逻辑对 `.jpg` 依赖较强。

---

### 3.4 `remove`

用途：删除指定标签（按索引或标签名）。

命令原型：

```bash
yoloutils remove --source <src> [--target <dst>] [--clean] (--classes <idx...> | --label <name...>)
```

参数：

- `--source`：源目录（必需）。
- `--target`：目标目录（可选）。不传时原地改写。
- `--clean`：清空目标目录。
- `--classes`：要删除的标签索引列表。
- `--label`：要删除的标签名列表（会先映射到索引）。

执行行为（源码）：

1. 递归扫描 `source/**/*.txt`，跳过 `classes.txt`。
2. 逐行移除匹配索引的标注。
3. 若 `--target` 存在，输出路径是 `target/<basename>.txt`（不保留原子目录）。
4. 若删除后文件为空，会删除对应 `.txt` 及同名 `.jpg`。
5. 不传 `--target` 时直接覆盖源文件。

示例：

```bash
yoloutils remove --source ./dataset --target ./cleaned --classes 0 1 --clean
yoloutils remove --source ./dataset --target ./cleaned --label cat dog
yoloutils remove --source ./dataset --classes 5
```

注意：

- 输出模式下只写“发生变更”的文件；未变化文件不会拷贝到目标目录。
- 目标目录不保留原目录结构，深层同名文件可能覆盖。

---

### 3.5 `change`

用途：批量替换标签索引（原地修改）。

命令原型：

```bash
yoloutils change --source <src> --search <old_idx...> --replace <new_idx...>
```

参数：

- `--source`：源目录（必需）。
- `--search`：旧索引列表。
- `--replace`：新索引列表，按位置一一对应。

执行行为（源码）：

1. 构造映射 `search[i] -> replace[i]`。
2. 递归扫描 `source/**/*.txt`，跳过 `classes.txt`。
3. 每行若以 `"<old> "` 开头就替换首个匹配前缀，然后写回原文件。
4. 输出索引统计表。

示例：

```bash
yoloutils change --source ./dataset --search 0 1 --replace 5 6
```

注意：

- 这是原地改写，无 `--target`。
- 代码未检查 `search/replace` 长度一致；不一致可能抛异常。

---

### 3.6 `crop`

用途：使用 YOLO 模型检测并裁剪图片。

命令原型：

```bash
yoloutils crop --source <src> --target <dst> --model <best.pt> [--output <predict_dir>] [--clean]
```

参数：

- `--source`：图片目录（必需）。
- `--target`：裁剪结果目录（必需）。
- `--model`：模型路径（必需）。
- `--output`：可选，保存推理可视化与 `save_crop` 结果。
- `--clean`：清空 `target`，并在设置了 `output` 时清空 `output`。

执行行为（源码）：

1. 递归扫描 `source/**/*.jpg`。
2. 目标路径按相对目录映射到 `target`。
3. 每张图调用 `YOLO(model)` 推理。
4. 若设置 `--output`，会保存带框图片，并将 `save_crop` 输出到 `output/crop`。
5. 实际写入 `target` 的是首个检测框裁剪图，保存文件名沿用原图相对路径。

示例：

```bash
yoloutils crop --source ./images --target ./cropped --model ./best.pt
yoloutils crop --source ./images --target ./cropped --model ./best.pt --output ./predict --clean
```

注意：

- `source == target` 会直接退出。
- 虽有 `_idx` 命名变量，但当前实现只返回并保存第一个检测结果。

---

### 3.7 `labelimg`

用途：把 labelimg 风格数据整理为 YOLO 训练目录，并生成 `data.yaml`。

命令原型：

```bash
yoloutils labelimg --source <src> --target <dst> [--val <n>] [--uuid] [--check] [--clean]
```

参数：

- `--source`：源目录（必需）。
- `--target`：目标目录（必需）。
- `--val`：每个标签抽样到验证集的数量，默认 `10`。
- `--uuid`：训练集输出标签名使用 UUID。
- `--check`：参数存在，但当前实现未使用。
- `--classes`：参数存在，但当前实现仍固定读取 `source/classes.txt`。
- `--clean`：清空目标目录。

执行行为（源码）：

1. 创建目录：`train/labels`、`train/images`、`val/labels`、`val/images`、`test/labels`、`test/images`。
2. 读取 `source/classes.txt` 初始化类别。
3. 递归扫描 `source/**/*.txt`（跳过 `classes.txt`），复制到 `train/labels`。
4. 图片按同名复制到 `train/images`，输出扩展名固定为 `.jpg`。
5. 按标签样本列表随机抽样到 `val`。
6. 生成 `target/data.yaml`（含 `train/val/test` 与 `names`）。

示例：

```bash
yoloutils labelimg --source ./labelimg_data --target ./yolo_data --clean
yoloutils labelimg --source ./labelimg_data --target ./yolo_data --val 20 --uuid
```

注意：

- `test` 目录会创建，但流程不会自动填充测试样本。
- 图片匹配逻辑主要围绕 `.jpg`。

---

### 3.8 `resize`

用途：按长边限制缩放图片。

命令原型：

```bash
yoloutils resize --source <src> --target <dst> [--imgsz <long_edge>] [--output <dir>] [--clean]
```

参数：

- `--source`：源图片目录（必需）。
- `--target`：目标目录（必需）。
- `--imgsz`：长边阈值，默认 `640`。
- `--output`：参数存在，但当前流程不参与 resize 输出。
- `--clean`：清空 `target`，若设置了 `output` 也会清空 `output`。

执行行为（源码）：

1. 递归扫描 `source/**/*.jpg`。
2. 输出路径保留原始相对目录结构。
3. 当 `max(width, height) < imgsz` 时直接复制（计入“未处理”）。
4. 其他情况执行等比例缩放后保存（计入“已处理”）。

示例：

```bash
yoloutils resize --source ./images --target ./resized --imgsz 640 --clean
yoloutils resize --source ./images --target ./resized --imgsz 1920
```

注意：

- `source == target` 会直接退出。

---

### 3.9 `classify`

用途：整理分类数据集并拆分 `train/test/val`；可选先检测裁剪再入库。

命令原型：

```bash
yoloutils classify --source <src> --target <dst> [--test <n>] [--crop --model <pt>] [--output <dir>] [--checklist <dir>] [--uuid] [--verbose] [--clean]
```

参数：

- `--source`：分类源目录（必需），要求按类别分子目录。
- `--target`：输出目录（必需）。
- `--test`：每类抽样到 `test` 和 `val` 的数量，默认 `10`。
- `--crop`：启用检测后裁剪。
- `--model`：`--crop` 时必须提供并且文件存在。
- `--output`：保存推理可视化图。
- `--checklist`：保存多检测框样本的结果及裁剪，便于复核。
- `--uuid`：目标文件名用 UUID。
- `--verbose`：传给 YOLO 推理日志。
- `--clean`：清空 `target/output/checklist`（若设置）。

执行行为（源码）：

1. 从 `source` 的一级子目录读取类别与样本。
2. 创建 `target/train|test|val/<class>` 结构。
3. `train` 阶段：
   - 非 `--crop`：直接复制源图片到 `train`。
   - `--crop`：对每张图检测，按框输出 `<name>_<idx>.<ext>` 到 `train/<class>`。
4. `train` 完成后，重新扫描 `train` 作为最终抽样池。
5. `test` 与 `val` 各自从 `train` 随机抽样并复制。
6. 如果单图检测到多个框，会记录到检查表；设置了 `--checklist` 时额外导出复核文件。

示例：

```bash
yoloutils classify --source ./source --target ./dataset --clean
yoloutils classify --source ./source --target ./dataset --test 50
yoloutils classify --source ./source --target ./dataset --crop --model ./best.pt --output ./predict --checklist ./checklist
```

注意：

- `--test` 在实现中会在小类别上被下调并直接写回 `self.args.test`，可能影响后续类别抽样数量。

---

### 3.10 `test`

用途：批量推理目录中的图片，并输出表格/CSV/可视化图。

命令原型：

```bash
yoloutils test --source <src> --model <pt> [--csv <result.csv>] [--output <dir>]
```

参数：

- `--source`：输入目录（必需）。
- `--model`：模型路径（必需）。
- `--csv`：保存结果到 CSV。
- `--output`：保存推理可视化图片。

执行行为（源码）：

1. 扫描 `source/**/*`，过滤 `.txt` 和 `.DS_Store`。
2. 每个输入只记录首个检测框的 `label/conf`。
3. 输出文本表：`文件 / 标签 / 置信度`。
4. 可选写入 CSV。
5. 末尾打印汇总：总数、未检出数量、平均置信度。

示例：

```bash
yoloutils test --source ./images --model ./best.pt
yoloutils test --source ./images --model ./best.pt --csv ./result.csv --output ./predict
```

注意：

- 当前实现的总数基于原始扫描列表，可能包含非图片项，汇总统计会受影响。

## 4. Agent 执行模板

当用户提出任务时，按以下顺序执行：

1. 先判断对应子命令。
2. 明确必填参数并检查目录/模型/`classes.txt`。
3. 给出可直接执行的一条命令（必要时再给扩展选项）。
4. 提醒该子命令的关键副作用（是否原地修改、是否会删除目录、是否可能覆盖同名文件）。
5. 执行后给核验动作：统计表、输出目录抽样、CSV 或 `data.yaml` 是否生成。
