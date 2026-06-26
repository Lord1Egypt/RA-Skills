# 发布前检查清单

- [ ] `SKILL.md` 校验通过
- [ ] `skill.json` 是合法 JSON，并声明版本号、脚本、网络、隐私和 OpenClaw 边界
- [ ] `skill.json` 已声明 `homepage`、`repository`、`source.directory=skill` 和 `install.script=install.sh`
- [ ] `skill.json` 已声明 registry 可读的 `install_spec`，并与 `openclaw.installSpec` 保持一致
- [ ] OpenClaw 元数据声明为 executable-skill，不是 instruction-only
- [ ] README 和 `references/privacy-boundaries.md` 已声明默认后端、接口、手机号发送路径和本地状态路径
- [ ] README 和 `references/privacy-boundaries.md` 已声明只使用本人手机号、共享机器清缓存、订单查询必须由明确个人订单/偏好场景触发
- [ ] 可选环境变量已声明：`XINYI_API_BASE_URL`、`XINYI_TIMEOUT_SECONDS`、`XINYI_DRINK_STATE_FILE`
- [ ] 安全扫描通过
- [ ] `install.sh --dry-run --platform openclaw` 通过
- [ ] `install.sh --dry-run --platform hermes` 通过
- [ ] `install.sh --dry-run --platform claude-code` 通过
- [ ] `install.sh --dry-run --platform cursor` 通过
- [ ] `install.sh --dry-run --platform universal` 通过（同目标路径覆盖 `codex` / `qclaw` / `lobsterai` / `workbuddy`）
- [ ] 如本机已有安装，`install.sh --platform codex --check-installed` 能明确报告一致或漂移
- [ ] README 已包含平台安装说明
- [ ] GitHub 发布信息已准备
- [ ] ClawHub 上架文案已准备
