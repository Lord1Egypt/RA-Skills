# 依赖说明 / Setup Guide

## Python Runtime

- **用途**：运行 `scripts/score_skill.py`（硬指标自动判定）和 `scripts/check_environment.py`（环境检查）。
- **支持版本**：Python 3.10 及以上。
- **官方主页**：https://www.python.org/
- **下载地址**：https://www.python.org/downloads/
- **登录网址**：不需要。
- **Token/Key/OAuth 入口**：不需要。
- **权限**：无需额外权限，脚本只读被审目录，不写文件、不联网。
- **配置步骤**：安装 Python 后确保 `python` 命令可用即可，无需任何配置。
- **凭据存储**：无凭据。
- **验证方式**：`python --version`，确认版本 ≥ 3.10。
- **过期/权限/额度处理**：不涉及。
- **轮换和撤销**：不涉及。
- **核验日期**：2026-09-09。

## 降级说明 / Degradation

| 功能 | 失败条件 | 降级方式 | 限制 |
|---|---|---|---|
| 硬指标自动判定 | Python 不可用或版本过低 | 由模型按 `references/review-standards.md` 手工检查硬指标 | 结构类检查变慢、可能遗漏，标记「未做程序化校验」 |
| 脚本能力预检 | Python 不可用 | 模型静态阅读脚本源码，人工列出能力清单 | 可能漏检，标记「人工预检」 |

核心审查结论（11 维评分、P1/P2/P3、判定）不依赖 Python，模型读内容即可产出；Python 只负责加速结构类硬指标的确定性判定。
