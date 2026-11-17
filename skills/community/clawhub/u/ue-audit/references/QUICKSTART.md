# UE 工程体检 — 快速开始

## 1. 环境

- Python 3.9+
- Windows 优先（UE 工程常用）
- 在线检查需要本机 UE 编辑器和本地 HTTP 编辑器桥；没有桥也能做离线体检

## 2. 第一次运行

```bash
python scripts/run_audit.py doctor C:/Projects/MyGame
python scripts/run_audit.py audit C:/Projects/MyGame --out D:/audit/run1
```

打开 `D:/audit/run1/report.html`。

## 3. 建立基线

```bash
python scripts/run_audit.py audit C:/Projects/MyGame \
  --out D:/audit/run1 \
  --save-baseline D:/audit/baseline.json
```

## 4. 对比基线

```bash
python scripts/run_audit.py audit C:/Projects/MyGame \
  --out D:/audit/run2 \
  --baseline D:/audit/baseline.json
```

## 5. 验收 AI 任务

```bash
python scripts/run_audit.py verify C:/Projects/MyGame \
  --task task.json \
  --baseline D:/audit/baseline.json
```

`task.json` 最小示例：

```json
{
  "task_id": "ai-task-001",
  "expected_write_set": [
    "Content/Blueprints/BP_Test.uasset",
    "/Game/Data/DT_Items"
  ]
}
```

## 6. 在线资产检查

```bash
python scripts/run_audit.py audit C:/Projects/MyGame --live \
  --blueprint /Game/Blueprints/BP_Player \
  --datatable /Game/Data/DT_Items \
  --widget /Game/UI/WBP_HUD \
  --material /Game/Materials/M_Test \
  --animbp /Game/Anims/ABP_Test
```

## 7. CI

```bash
python scripts/run_audit.py audit C:/Projects/MyGame \
  --out D:/audit/ci \
  --fail-on error
```

用 `D:/audit/ci/junit.xml` 作为测试报告。

## 读报告

- `pass`：通过
- `warn`：非阻塞问题
- `fail`：应阻断验收
- `skip`：未请求/不适用
- `unknown`：无法判断，**不能当成通过**

详见 `SKILL.md` 和 `references/CHECKS.md`。
