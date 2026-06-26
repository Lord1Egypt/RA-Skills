# Publishing Notes

适合上传到 ClawHub 的最小内容：

- `SKILL.md`
- `README.md`
- `agents/openai.yaml`
- `scripts/`
- `references/`
- `package.json`
- `package-lock.json`

发布前确认：

- 不包含 `node_modules/`
- 不包含 `.outputs/`
- 不包含 `.state/`
- `SKILL.md` 描述与实际能力一致
- `agents/openai.yaml` 默认提示词覆盖登录、导出、本地处理和回传流程
