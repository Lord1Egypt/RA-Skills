# 通用排错参考

这份说明用于**功能主题自己的排错步骤仍不够时**的通用兜底排查。

优先顺序应当是：

1. 先看当前问题对应的功能 reference
2. 如果功能内排查仍解释不了，再回到这里做通用诊断

遇到这些情况时，优先查这里：

- 功能文档里的排错已经做过，但问题仍解释不通
- 文档里的命令、导入路径、配置文件位置和本地安装对不上
- 某个功能在说明里提到，但用户环境里“没有这个命令 / 没有这个模块 / 没有这个 extra”
- 同一份示例在不同机器上，一个能跑、一个提示参数名、模块名或行为不一致

## 先确认问题是不是功能专属

这份文档不替代功能主题内的局部排错。常见入口：

- CLI / 命令参数 / shell 工作流：`references/cli-guide.md`
- 本地模拟 / dummy / simulation 依赖：`references/simulators.md`
- 云平台 / token / task cache / dummy 提交：`references/cloud-platforms.md`
- HEA / QAOA / UCCSD / VQE：`references/variational-algorithms.md`
- PyTorch 辅助工具：`references/pytorch-integration.md`

如果这些局部文档已经看过，仍然解释不了问题，再继续下面的通用步骤。

## 推荐顺序

不要一开始就读一大堆前提。通用排障更适合按下面的顺序推进：

1. 先拍一张当前安装快照：解释器、包版本、模块路径、CLI 路径
2. 立刻判断版本变化是不是主要原因，先看对应版本摘要
3. 再查 issue / discussion 里有没有同类报错、参数改名或行为变更
4. 再回到对应功能文档和上游文档核实当前用法
5. 还解释不通时，最后再读源码

这个顺序的目标不是一次性证明所有前提，而是先快速判断“问题大概率落在哪一层”。

## 第一步：先拍安装快照

排错前不要假设用户装的是 PyPI 发布版，也不要假设 shell 里的 `uniqc` 和当前 Python 是同一套环境。至少先回答四个问题：

- 当前用的是哪个解释器
- `unified-quantum` 显示的版本号是什么
- `uniqc` 模块实际从哪里导入
- shell 里执行到的 `uniqc` 在哪里

最小检查命令：

```bash
python3 - <<'PY'
from importlib.metadata import version
from shutil import which
import sys

print("exe=", sys.executable)
print("cli=", which("uniqc"))

try:
    import uniqc
except ModuleNotFoundError:
    print("module= <uniqc not importable>")
else:
    print("module=", uniqc.__file__)

try:
    print("version=", version("unified-quantum"))
except Exception as exc:
    print("version_probe_failed=", repr(exc))
PY
```

如果用户使用的是项目虚拟环境、`uv tool`、Conda 或其他解释器，要改用对应解释器执行这条命令。

结果通常可以分成三类：

- **PyPI / wheel 安装**：模块路径位于 `site-packages`
- **源码 editable 安装但对齐某个 release/tag**：模块路径指向源码目录，版本号通常仍是正式版本
- **源码 editable 安装且跟随主线**：模块路径指向源码目录，版本号可能带 `dev`，或者与已发布行为不一致

这里最重要的是：**以当前解释器真正导入到的包为准**，不要只看用户在哪个源码目录里开了终端，也不要只看仓库 README。

如果需要快速做一次环境体检，可以运行：

```bash
bash scripts/setup_uniqc.sh
```

它更适合快速回答这些通用问题：

- `uniqc` 能不能启动
- `import uniqc` 是否成功
- 基础依赖是否缺失
- simulation / PyTorch / scikit-learn 等常见可选能力是否可用

## 第二步：先看版本摘要，不要先钻细节

拿到安装快照后，先判断“版本变化是不是主要原因”。

适合优先看版本摘要的信号包括：

- 用户看的文档、示例或笔记明显比当前安装新或旧
- 报错集中在“参数名不存在”“命令组选项变了”“导出路径改了”“模块路径变了”
- 同一段代码在两台机器上表现不同，而版本号或模块路径不同

这一层先看**对应版本附近的 release notes、changelog、tag 摘要**就够了，目的是快速判断是不是版本差异导致的，不必一上来就翻完整源码。

UnifiedQuantum 当前可直接从这里看版本摘要：

- Release Notes: `https://iai-ustc-quantum.github.io/UnifiedQuantum/source/releases/index.html`

如果用户拿的是文档站里的说明但本地行为对不上，先把本地版本号和这个页面里的相邻版本条目对一遍，再决定要不要继续查 issue 或源码。

如果已经确认用户直接在 `UnifiedQuantum` 源码 checkout 里工作，且需要判断“当前代码大致落在哪个 tag 附近”，才额外使用：

```bash
git describe --tags --always
```

它只是辅助判断源码树和最近 tag 的相对位置，不能替代“当前解释器里实际导入了哪个版本”的检查。

## 第三步：查 issue / discussion 有没有同类问题

如果版本摘要提示“这里确实变过”，或者报错看起来像回归、兼容性问题、文档滞后问题，就优先查 issue / discussion。

搜索时优先组合这些信息：

- 版本号或 tag
- 精确报错文本
- 具体命令、参数名、模块名或函数名
- 所属平台或可选依赖，例如 `simulation`、`originq`、`qiskit`、`torch`

这一层最有价值的问题通常是：

- 某个参数或命令最近是否改名
- 某个 extra 是否刚被拆分、上移或不再默认安装
- 某个功能是否只在主线修复、尚未发版
- 某个示例或文档是否已知落后于当前实现

## 第四步：再回到功能文档和上游文档

确认大致方向后，再去读具体文档，效率会高很多。优先顺序通常是：

1. 当前问题对应的主题 reference
2. 与当前安装来源匹配的上游文档
3. 与当前版本相邻的示例或官方说明

很多“看起来像程序问题”的情况，其实只是解释器、CLI 入口或可选依赖没对齐。这里重点再核对：

- 当前 shell 里的 `uniqc` 和你用来 `import uniqc` 的解释器是不是同一套环境
- 需要模拟、dummy、PyTorch、云平台适配器时，有没有装对应 extra
- 用户是不是把主线源码 README、历史笔记或旧示例，当成了当前安装版本的真实能力

## 第五步：最后再读源码

只有前面几步还解释不通时，才进入源码层。

源码排查的推荐顺序：

1. 如果模块已经能导入，先读当前环境里真正加载到的源码或已安装文件
2. 如果需要对照上游实现，再在用户允许的前提下 clone `UnifiedQuantum`
3. 如果用户已经有本地 checkout，优先让用户提供大致路径，再直接在那份仓库里读

如果要 clone 或进入用户本地仓库做进一步检查，先和用户确认再动手。不要默认把排障升级成仓库操作。

## 常见排错思路

- 缺命令、缺导入、缺 extra 时，先确认是不是装错了解释器或少装了可选依赖
- `uniqc` 能运行但 `import uniqc` 失败，或反过来时，优先怀疑不是同一个环境
- 文档和本地行为不一致时，先看安装快照，再判断是不是版本差异
- 如果模块路径指向源码目录，不要立刻把 README 上写的能力当成“当前环境一定具备”
- 如果模块路径指向 `site-packages`，但用户拿的是主线源码说明，优先怀疑“文档比安装版本新”
- 不要先入为主地判定“包坏了”或“这份说明过时了”；很多问题只是安装来源和参考文档不一致

## 使用这份参考时记住

- 功能专属问题优先回到对应主题 reference，不要在这里一次性展开所有细节
- 这里主要解决通用排错顺序、环境快照、版本识别、issue 检索和源码升级路径
- 需要解释功能差异时，优先看与当前安装来源匹配的官方版本摘要、issue 和文档
- 如果你看到手工维护的版本断点表，不要把它当成主判断依据；只有当某个识别步骤本身会影响排障时，它才值得参考
