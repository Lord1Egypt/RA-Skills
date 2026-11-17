# 踩坑笔记

这些不是推测，是把一条 9 分 29 秒的英文访谈完整跑通后实测出来的。按"踩中的概率"排序。

## 1. 假失败：清理临时目录导致 tasks 报 failed

**现象**：配音脚本明明打印了 `完成! 已生成 output.mp3`，任务却是以 failed 结束的。

**原因**：脚本最后一步是 `shutil.rmtree(temp_audio)`。一次性删除上百个临时片段，在某些环境（带批量删除保护的执行环境、企业版杀软、文件正被索引器占用）会被直接拦截并终止进程。此时 mp3 早已完整写盘。

**这不是本机特例**：在完全干净的 Windows 环境里同样复现（167 个文件触发保护）。只要字幕条数上百，就一定会遇到，请默认它会发生。

**为什么危险**：这是整条流水线最贵的一步（十几到几十分钟）。一旦误判成失败去重跑，白白再等一遍。

**对策**：

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1 output.mp3
```

时长接近「末条字幕结束 + 0.5 秒」就是成功，直接进下一步。**永远以产物为准，不以任务退出码为准。**

已在 `synthesize.py` 中把成功日志移到清理之前，并给清理加了异常兜底。

## 2. `SSLKEYLOGFILE` 能把"已安装"伪装成"未安装"

**现象**：`pip list` 里看得到 `edge-tts 7.2.8`，但 `import edge_tts` 报 `PermissionError: [Errno 13]`，进而 `No module named edge_tts`。连 `pip install` 本身都崩。

**原因**：环境变量 `SSLKEYLOGFILE=c:\sslkey.log` 指向 C 盘根目录。SSL 库初始化时要写这个文件，普通用户无权限写盘根目录于是崩溃。

**为什么难查**：报错落在导入阶段，症状与"包没装"一模一样，很容易一路往"重装、换源、改 PYTHONPATH"上钻，全是白费力气。

**对策**：

```bash
unset SSLKEYLOGFILE          # Git Bash / Linux / macOS
Remove-Item Env:SSLKEYLOGFILE  # PowerShell
```

彻底解决去系统环境变量里删掉它。`check_env.py` 会自动检测这个陷阱并给出提示。

**已内置自动诊断**：`check_env.py` 会区分「包没装」（`ModuleNotFoundError`）和「装了但导入崩溃」（其他异常）。前者提示 `pip install`，后者标记 `BROKEN` 并指向本条——因为两者的**处置方式完全相反**：一个要装，一个千万别装。

另外别用 `os.access()` 判断文件可写性，它会误报；必须真的 `open(path, "a")` 试一次。这一点在实测中翻过车。

## 3. Python 3.13 起标准库移除了 `audioop`，pydub 会崩

**现象**：`import pydub` 报 `ModuleNotFoundError: No module named 'audioop'`。

**原因**：`audioop` 属于 PEP 594 里被清理的"dead batteries"，Python 3.13 起从标准库移除。但 pydub 仍在用它。

**为什么坑**：报错指向 `audioop`，而 pip 上并没有一个叫 `audioop` 的包（`pip install audioop` 会失败），很容易卡住。

**对策**：

```bash
pip install audioop-lts
```

该包要求 Python ≥ 3.13，且有 Windows wheel。**在 3.12 及以下无需安装**（标准库自带），所以不要在旧版本上找它——那会报"找不到匹配的发行版"。

`check_env.py` 会自动检测并提示。

## 3b. Windows 缺 VC++ 运行库，torch / whisper 导入崩溃

**现象**：whisper 或 torch 在 import 阶段崩溃，报错提及 DLL、动态库加载失败，或干脆是难以理解的 `ImportError`。

**原因**：系统缺少 Visual C++ 2022 可再发行组件。

**典型报错**：`OSError: [WinError 126] 找不到指定的模块` 且路径指向 `c10.dll`。

**对策**：

```bash
pip install msvc-runtime
```

**优先用它而不是 vc_redist 安装程序**：后者需要管理员权限，在受限账户或公司机器上装不了，
而这个 pip 包直接把运行库放进环境，无需提权。

这个坑与第 2 条同属"环境问题伪装成包问题"家族——报错完全不提运行库，靠猜很难命中。

## 3c. 装 torch 时可能拉到数 GB 的 CUDA 包

**现象**：`pip install openai-whisper` 长时间卡在下载，进度条显示几百 MB 到数 GB。

**原因**：torch 的默认 wheel 可能带 CUDA 运行时，而本项目纯 CPU 推理即可。

**对策**：先单独装 CPU 版，再装其余依赖：

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

`check_env.py` 会检测已装的 torch 是否含 CUDA，并在是的情况下提示换 CPU 版。

## 3d. 缺 `ffprobe.exe` 会让 pydub 解不了 mp3

**现象**：ffmpeg 明明能正常调用，但 pydub 读取 mp3 时失败，报错看起来像文件格式问题。

**原因**：pydub 用 ffprobe 获取音频时长与元信息。有些 ffmpeg 发行版/便携包**只有 `ffmpeg.exe`**，不带 ffprobe。

**对策**：补一个 `ffprobe.exe` 与 ffmpeg 放在同一目录并加入 PATH。

**别把 ffprobe 当可选项**——它是必需的。早期版本把它标为警告，实测证明会导致步骤 3 失败。

## 3. 后台任务的 stdout 会被缓冲，看不到输出 ≠ 卡死

**现象**：后台跑配音，等了三分钟一条日志都没有，看着像挂了。

**原因**：Python 在非 TTY 环境下对 stdout 是块缓冲的，输出攒够一定量才刷出来。

**对策**：**看磁盘上的文件数，不看日志。**

```bash
ls temp_audio/ | wc -l
```

每生成一条就多一个 `seg_XXXX.mp3`，这是唯一可靠的进度指标。

## 4. 选错 Python 解释器

**现象**：`ModuleNotFoundError: No module named 'whisper'`。

**原因**：机器上往往有多个 Python（系统版、版本管理器托管版、venv、conda）。依赖装在其中一个里，而直接敲 `python` 命中的未必是它。

**对策**：用 `check_env.py` 逐个试，找到四个依赖全 OK 的那个，全程用它的绝对路径。**不要在每个解释器里都重装一遍依赖**——那是制造更多混乱。

另外：每条命令在独立 shell 中执行，`export PY=...` 不会带到下一条命令，别指望它。

## 5. ffmpeg 缺 `-y` 会静默挂起

**现象**：合成命令敲下去没有任何动静，既不报错也不返回。

**原因**：ffmpeg 发现输出文件已存在，停在 `Overwrite? [y/N]` 等你输入，而批处理环境下永远等不到。

**对策**：任何 ffmpeg 写文件的命令都加 `-y`。

## 6. Whisper 会把专有名词听错

这不是配置问题，是 ASR 的固有弱点。实测一条美式访谈的结果：

| Whisper 输出 | 实际 |
| --- | --- |
| Suzy Walsh | Susie Wiles（人名） |
| Electromp | the President-elect（当选总统） |
| blanket partners | blanket pardons（全面赦免） |
| mega | MAGA |

**对策**：翻译时（步骤 2）对可疑拼写按常识回正，**不要照字面直译**。人名、地名、党派、节目名尤其容易翻车。

## 7. 配音时长溢出字幕时槽

详见 `sync-tuning.md`。这是 TTS 方案的固有短板，不是 bug。

全量实测（166 条，两次独立运行）：

```
A：中位 0.95，溢出 42/166（25%）
B：中位 1.01，溢出 57/166（34%）—— 加了 --rate "+10%"
```

**两次数据不可直接比较**（译文不同），但共同点是：**溢出几乎全部集中在 1–2 秒的短碎片上**。
因此「中位数正常」不等于「不用管」——这两个数字必须分开看，处理方式也不同。详见 `sync-tuning.md`。

## 7b. ffmpeg 放在工作目录里，不在 PATH

**现象**：有时能跑有时不能；换到别的目录就报"找不到 ffmpeg"。

**原因**：Windows 上 `shutil.which()` 会顺带搜索**当前目录**，所以 ffmpeg 即使没进 PATH，
只要和工作目录放一起，当下也能被找到——脚本跑得通。但这是假象，换个目录立刻失效。

**为什么坑**：它属于"现在能用、以后会坏"的状态，排查时最难联想到 PATH。

**对策**：

1. 把 ffmpeg / ffprobe 所在目录加入 PATH（正解）
2. 临时方案：命令写成 `./ffmpeg`（Git Bash）或 `.\ffmpeg.exe`（PowerShell / CMD）

`check_env.py` 会检测出这种状态并给出警告——看到那句 WARN 就该处理，别放着不管。

## 8. 固定 `sleep(10)` 吃掉绝大部分耗时

原脚本在每条合成之间固定等待 10 秒，166 条光睡眠就 27 分钟，占总耗时的九成以上。

`synthesize.py` 改成默认 `--sleep 1.5` + 失败指数退避重试——绝大多数情况下根本不会触发限流，没必要为人人预付 10 秒。若真遇到大量失败，用 `--sleep 10` 退回保守策略。
