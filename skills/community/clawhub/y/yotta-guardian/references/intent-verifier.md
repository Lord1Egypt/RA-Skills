
# 意图验证器协议（yotta-guardian）

> 元盾默认纯确定性规则、不调用任何模型。需要语义级复核时，可通过本协议外接任意意图验证器（LLM 网关、本地模型、规则脚本均可），**不绑定任何固定模型**。

## 一、启用方式

1. 命令行外接：--verifier "命令 参数..."（字符串按 shell 规则拆分；Windows 下路径建议用配置文件列表形式避免反斜杠转义问题）
2. 配置文件：{"verifier": {"command": ["python3", "/path/verifier.py"], "timeout": 30}}
3. 内置启发式：--heuristic（本地确定性复核，不联网）

## 二、请求（stdin，JSON）

引擎对「允许」结论的调用发起验证，写入 stdin 的 JSON：

```json
{
  "tool": "exec",
  "cmd": "npm install",
  "path": "",
  "content_preview": "",
  "target": "",
  "policy": "default",
  "cwd": "/home/user/project",
  "findings": []
}
```

字段说明：tool 为工具类型；cmd / path / content_preview（内容前 500 字符）/ target 为调用内容；policy 为当前策略；findings 为确定性规则已命中的条目（允许结论下通常为空或仅低危）。

## 三、响应（stdout，JSON）

```json
{
  "verdict": "allow",
  "severity": "low",
  "reason": "安装依赖，无恶意信号"
}
```

- verdict：allow / deny / review 三选一（必须）。
- severity：可选，deny 时默认 high；取值 info / low / medium / high / critical。
- reason：可选，展示给用户的原因。

## 四、判定语义

| 验证器 verdict | 引擎处理 |
|---|---|
| allow | 维持确定性结论（允许） |
| deny | 升级为拒绝，严重级取响应 severity（默认 high） |
| review | 若当前为允许且低危，升级为「建议复核」（medium 警告，exit 1） |
| 无响应 / 超时 / 输出非法 | 按 review 处理（复核，不静默放行也不误杀） |

已拒绝的调用不会调用验证器（省成本，避免覆盖确定性结论）。

## 五、内置启发式（--heuristic）

本地确定性复核：扫描调用文本中的高影响动词（install / uninstall / delete / remove / overwrite / reset / drop / truncate / purge / cleanup / restart / reboot / shutdown / stop / disable / enable / start / upgrade / update / format / wipe 等），命中则升级为「建议复核」。不联网、可复现、适合作为轻量语义补充。

## 六、示例验证器（Python 桩）

```python
#!/usr/bin/env python3
import json
import sys

req = json.load(sys.stdin)
cmd = req.get("cmd", "")
if cmd.startswith("danger"):
    out = {"verdict": "deny", "severity": "high", "reason": "命中自定义策略"}
else:
    out = {"verdict": "allow", "severity": "low", "reason": "无风险信号"}
json.dump(out, sys.stdout)
```

真实场景可用该协议把调用摘要发给 LLM 网关做语义判断，返回同样的 JSON 即可接入。
