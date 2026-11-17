# 子 SKILL 开发标准模板

> 供开发新校园服务子 SKILL（timetable/mail/library/info 等）时遵循。
> 参照已完成的 learn / search / literature 三个子 SKILL。

## 1. 目录结构

```
skill/campus/<system>/
├── SKILL.md              # 子 SKILL 规范（AI 指令 + 用户说明）
└── scripts/
    ├── <system>.py       # 统一入口（AI 只调这一个）
    ├── <system>_api.py   # 底层 API 封装（如有）
    └── _config.py        # 桥接 base-cas 会话/凭据（如需登录）
```

## 2. SKILL.md 必含章节

```markdown
---
name: campus-<system>
description: <一句话描述 + 触发词>
metadata:
  openclaw:
    os: [windows, macos, linux]
---

# <中文名>

## 如果你是 AI，请阅读以下内容
### 铁律
- AI 运行所有脚本；stdout JSON，进度写 runtime/logs/campus.log，不写 stderr
- 脚本禁止 input() 阻塞；凭据走 --value-stdin
### 使用
<CLI 命令>
### 工作流
<AI 如何一步步执行>
### 边界
<已知限制>

## 如果你是用户，请阅读以下内容
<一句话就能用的示例>
```

## 3. 统一入口脚本规范

- 文件名 `<system>.py`，argparse 子命令
- stdout 只输出 JSON（`common.output_json`），**绝不写 stderr**
- 需要登录的系统 → `_config.py` 桥接 base-cas：
  ```python
  sys.path.insert(0, <base-cas/scripts>)
  import session as _cas_session
  state = _cas_session.load_session("<system>")  # 读登录态
  ```
- session 失效 → 调 `login.py --system <system> --ensure`（两阶段，非阻塞）

## 4. 凭据

- 在 `creds/scripts/creds.py` 的 `CRED_SCHEMA` 注册所需凭据（含 how_to_get 责任告知）
- 读取用 `vault.vault_decrypt(key, raw)`，禁止硬编码

## 5. 验收标准

1. `python <system>.py --help` 无报错
2. 真实数据链路跑通（登录→取数→JSON 输出）
3. **无 stderr 输出**（PowerShell 不出现 `python.exe : ...`）
4. **全程 headless**：登录走 base-cas（无头浏览器），登录后浏览器自动关闭、不残留
5. 集成进主 SKILL.md 路由
6. 补 smoke_test.py 检查项

## 6. 通用注意事项

- 进度日志用 `common.log()`（写日志文件），不用 `print(..., file=sys.stderr)`
- 别写 `time.sleep = N`（赋值笔误会让 sleep 不可调用）
- 中文路径/输出用 UTF-8：`sys.stdout.reconfigure(encoding='utf-8')`
