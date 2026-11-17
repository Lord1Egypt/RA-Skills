# skill-template 工具

## 推荐：脚手架创建新技能

**不要**用资源管理器整文件夹复制 `skill-template`（会带走隐藏 `.git`，导致 push 串库）。

Windows 首选：

```powershell
cd D:\OpenClaw\client-commons\skill-template
.\tools\scaffold_skill.ps1 -Slug my-new-skill -Destination D:\OpenClaw\client-gdcm\my-new-skill
```

跨平台（Python 3.10+）：

```bash
python tools/scaffold_skill.py --slug my-new-skill --destination /path/to/my-new-skill
```

脚本行为：

- 复制模板到 `-Destination`（目录末段须与 `-Slug` 一致）
- **排除**：`.git`、`.pytest_cache`、`__pycache__`、`.env`、`.env.local`、`*.pyc`
- 删除目标中的 `.openclaw-skill-template` 标记
- **不**自动 `git init`；打印后续 Git 与测试命令

目标目录若已存在且非空，需加 `-Force` / `--force`（且目标**不得**含 `.git`）。

## 手工复制后的补救

若已整目录复制，必须先清理再初始化：

```powershell
cd <新技能目录>
Remove-Item -Recurse -Force .git
Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue
Remove-Item -Force .openclaw-skill-template -ErrorAction SilentlyContinue
git init
git remote add origin <新技能仓库 URL>
git remote -v
```

确认 `origin` **不是** skill-template 的远端 URL。

## 模板标记

源仓库根目录有 `.openclaw-skill-template`（仅 template 保留）。业务技能不得保留该文件；`tests/test_scaffold_guard.py` 会守护。
