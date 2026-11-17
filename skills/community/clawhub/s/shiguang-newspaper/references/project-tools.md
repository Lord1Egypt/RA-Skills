# 离线工程辅助工具

脚本 [newspaper_project.py](../scripts/newspaper_project.py) 不依赖网站或特定模型，也不发起网络/模型调用。它负责文件登记、输入指纹、任务状态、批准记录、页面历史、等比 PDF 导出和完整 ZIP 工程。调用图像工具仍由当前 Agent 完成。

运行需要 Python 3.10+；图像检查与 PDF 导出需要 Pillow、reportlab。优先使用环境已有依赖，缺失时在任务独立虚拟环境中安装，不改动无关应用依赖。其他宿主可以用等价工具实现相同交付与记录，不必为了读取本 Skill 安装 Python。

```sh
python -m venv .newspaper-env
# macOS / Linux：
.newspaper-env/bin/python -m pip install Pillow reportlab
.newspaper-env/bin/python /path/to/shiguang-newspaper/scripts/newspaper_project.py --help
```

Windows PowerShell 使用同一虚拟环境的解释器，无需激活脚本：

```powershell
.newspaper-env/Scripts/python.exe -m pip install Pillow reportlab
.newspaper-env/Scripts/python.exe C:/path/to/shiguang-newspaper/scripts/newspaper_project.py --help
```

所有示例 `/path/to/` 应换成安装位置，不是可直接运行的本机路径。**下文的 `python` 均指上面选定的虚拟环境解释器**，`newspaper_project.py` 指包内该脚本的实际路径；不要切回未安装依赖的系统解释器。命令的完整参数以 `COMMAND --help` 为准。A3/A4/A5 以外可使用 `--paper custom --width-mm 250 --height-mm 350`；方向决定长短边，不更改用户选定的物理尺寸。

## 创建与批准

```sh
python newspaper_project.py init --project my-issue --title "风筝镇特刊" --paper A4 --orientation landscape --sides single --pages 2
python newspaper_project.py register --project my-issue --id source-character --file character.png --role content --origin synthetic
python newspaper_project.py plan --project my-issue --file plan.json
python newspaper_project.py approve --project my-issue --stage plan --by user --note "用户已确认整期策划及逐图方案"
```

只有实际取得用户确认后才能写 `--by user`。用户明确委托自行决定或完整测试时，初始化时以 `--delegated-approval "用户授权的实际范围"` 记录，再用 `--by delegated`；它不冒充用户点击。确认阶段为 `plan`、`front`、`issue`，分别对应策划、真实头版和整期成品。

计划 JSON 含 `title`、`style`、`pages` 数组；每版保留稳定 `id`、`title`、`role`、`summary`、`visualBrief`、`articles`。按实际任务添加 imagePlans、必用素材、批准文案等字段。不要把完整确认文案只藏在聊天记录里。

## 图像任务

创建任务 spec 文件：

```json
{
  "stage": "extraction",
  "model": "actual-tool-or-model-name",
  "promptVersion": "newspaper-v1",
  "inputs": ["source-character"],
  "instruction": "忠实提取邮差人物，保持原姿态与衣着，真实透明背景",
  "caption": "邮差小禾"
}
```

`stage` 可为 `extraction`、`variant`、`page`；页面任务另填 `pageId`。实际风格、范围、姿态和所需文字应在有效输入中表达，不能放在只供展示的备注里。`caption` 与 `rationale` 顶层属于素材展示信息，不单独改变视觉缓存；需要印在版面上的图注必须进入该页的 `instruction` 或有效输入。

```sh
python newspaper_project.py begin --project my-issue --spec task.json
```

- 返回 `action=run` 才发起这一任务的模型调用；将真实返回文件立即保存。
- 返回 `action=cached` 时复用经校验的结果，不再调用模型。
- 返回 `action=blocked` 时先检查可靠记录与失败原因，不循环重复请求。

```sh
python newspaper_project.py complete --project my-issue --task TASK_ID --file actual-result.png
python newspaper_project.py fail --project my-issue --task TASK_ID --state unknown --message "响应超时，结果尚无法核验"
python newspaper_project.py status --project my-issue
```

`complete` 返回的 `asset.id` 可作为后续任务的 `inputs`；可选测量字段见命令帮助，只有实际返回的数据才能填写。服务明确在开始前拒绝且属于临时故障时，记录 `--state not-started --transient`，最多获得一次自动补试机会。脚本不会自动发起请求。用户明确要求重新生成整版时对 `begin` 使用 `--new-intent`，工具会持久化当前生成意图，同一原 spec 后续自动恢复该意图；失败重试不能反复添加 `--new-intent` 来绕过状态限制。

用户明确选择手动重试未知任务时，先确认原任务不再运行，再使用 `begin --spec SAME_SPEC --retry-manual`。可靠的迟到结果可以直接用原任务 ID `complete`，不增加生成尝试。若计划或生成意图已经更新，旧结果只保存，不覆盖新版面。

恢复历史版面使用 `restore-page --project my-issue --page page-02 --task PREVIOUS_COMPLETED_TASK_ID`；原当前版进入历史。局部修改/恢复头版保留已经完成的内页，只撤销相应确认，整期检查时核对风格是否仍一致；不能因为头版改一个字就自动重做内页。真正改变全期视觉方向时先通过 `plan` 修改共享 `style` 等字段，使受影响的全期版面失效。新制作的内页仍使用最新批准的头版。

头版完成并确认后才开始内页。保持批准记录和实际文件版本一致；某版被修改后需要重新检查相应成品。检查阶段由 Agent 真实查看，脚本不会自动理解画面或替用户评分。

## 输出与恢复

```sh
python newspaper_project.py export --project my-issue --output my-issue.pdf
python newspaper_project.py archive --project my-issue --output my-issue.newspaper.zip
python newspaper_project.py restore --archive my-issue.newspaper.zip --project restored-issue
python newspaper_project.py status --project restored-issue
```

PDF 只含按顺序排好的成品页，不嵌入原图、历史或整个工程。每页等比完整适配到物理纸张，不拉伸或裁切。单双面是打印设置；双面时在打印机选择适合横/竖版的翻边方向，先打样，脚本不假装控制打印机。

`.newspaper.zip` 包含 `project.json` 与已登记的源图、衍生图、页面和记录；恢复后文件依然可核验。它不是网站 `.shiguang.json`，也不是恢复出逐字可编辑图层。备份和恢复使用不同目录，不能覆盖用户现有工程。导入不执行归档中代码，拒绝逃逸路径和符号链接。

工具测试见 `scripts/test_newspaper_project.py`，另需 `pypdf`。测试验证离线状态与文件边界，不等于供应商真实故障测试，也不证明成品美感；完整验收仍需要查看实际报纸及逐页渲染 PDF。命令返回 JSON；`begin` 的成功退出也可能是 `action=blocked`，必须检查 action 才决定调用模型。写入锁冲突时检查进程，不盲目删除 `.project.lock`。
