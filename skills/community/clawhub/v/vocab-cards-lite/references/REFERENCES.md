# References — vocab-cards-lite

本目录汇总 vocab-cards-lite 的参考与设计说明，供发布检测 / 维护时查阅。

## 文档索引

| 文件 | 说明 |
|------|------|
| `../README.md` | 快速上手、安装、使用方法 |
| `../CHANGELOG.md` | 版本与变更记录（v1.0.0 → v2.0.1） |
| `../SKILL.md` | 技能主说明（frontmatter + 指令） |
| `../skill-card.md` | 技能卡片：发布者、许可证、风险评估、输出规范 |
| `../_meta.json` | 发布元数据（owner / slug / version） |
| `../requirements.txt` | Python 依赖清单（pillow / fonttools / qrcode[pil]） |
| `../scripts/vocab_cards.py` | 主生成脚本 |
| `../scripts/setup.sh` | 依赖与字体校验脚本 |
| `../examples/sample.json` | 内置最小验证示例（3 条） |
| `../assets/fonts/` | 包内 IPA 裁剪字体（DejaVuSans.ttf / DejaVuSans-Bold.ttf，68KB） |

## 设计要点

- **体积优先**：仅内置 IPA 裁剪字体，中英文依赖系统字体，包体控制在 68KB。
- **黑白打印优化**：固定 1000px 宽、动态高度，灰阶配色专为打印校准。
- **健壮性**：输入字段校验（仅 `word` 必填）、字体延迟加载、逐条 try/except、规范退出码（0/2/3）。
- **可验证**：自带 `examples/sample.json`，一行命令即可跑通安装验证。
