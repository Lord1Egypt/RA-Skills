# 通用安装说明

本安装包不绑定 OpenClaw、WorkBuddy 或其他特定宿主。安装位置和重新加载方式由宿主 Agent 决定，运行时契约由安装包提供且不得修改。

## 安装步骤

1. 识别当前宿主官方支持的用户级 Skill 机制和目录；优先使用宿主提供的安装或导入功能。
2. 将整个 `suno-cn-music` 目录复制到目标位置，并保持目录名称不变。
3. 不得修改、重新生成或删除 `SKILL.md`、`INSTALL.md`、`references/api.md`、`scripts/suno-client.mjs`或 `install.sh`。
4. 根据宿主要求重新加载 Skill 或重启 Agent，然后在 Skill 根目录执行 `node scripts/suno-client.mjs version`。
5. 执行 `node scripts/suno-client.mjs account`。若返回网页授权链接，将完整链接交给用户并等待用户确认授权完成。

若无法确认安装目录，停止安装并询问用户，不得猜测路径，也不得通过改名或改写 Skill 来适配宿主。

## 可选安装脚本

宿主已经确定完整目标目录时，可以执行：

```bash
./install.sh "/absolute/path/to/suno-cn-music"
```

Windows 用户请通过宿主 Agent 的 Skill 导入功能安装，或将整个 `suno-cn-music` 目录复制到宿主确认的 Skill 目录。本发布包不包含批处理安装脚本。

也可以通过 `SUNO_CN_SKILL_DIR` 提供同一完整目标目录。未提供明确目录时，脚本会直接退出，不会默认安装到任何特定宿主。

## 不可修改的运行时契约

- 所有网络请求只能通过 `scripts/suno-client.mjs` 发起。
- 不得以 curl、自行拼接 HTTP 请求、MCP JSON-RPC 或浏览器脚本替代 helper。
- 网页登录授权、积分不足后的购买确认、待恢复操作和未知结果防重试流程不得修改或跳过。
- 不得读取、打印或要求用户提供 Skill Key、网站 Token、凭证文件或 API Key。
- `SUNO_CN_MCP_URL` 与 `SUNO_CN_CONFIG_DIR` 仅供明确的运维或调试场景覆盖；普通安装不得自行改写默认值。
