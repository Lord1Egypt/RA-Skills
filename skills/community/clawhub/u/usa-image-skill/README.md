# USA GPT 生图技能

通过 https://usa0.top 的 OpenAI 兼容 Images API 使用 `gpt-image-2` 生成或编辑图片。

## 快速开始

1. 在 https://usa0.top 获取“生图分组”的 API Key，并确保账户有足够额度。其他分组的密钥不能用于本技能。
2. 配置环境变量：

```bash
export USA_API_KEY="sk-your-api-key-here"
```

Windows 用户也可以让 AI 运行以下命令，弹出本机密码输入框进行安全配置：

```powershell
uv run generate.py --configure-key
```

配置窗口使用 CustomTkinter，支持系统明暗模式、High-DPI 缩放、密码显隐、分组确认和内联错误提示。密钥会保存为当前 Windows 用户的 `USA_API_KEY`。

3. 生成图片：

```bash
cd ~/.openclaw/workspace/skills/usa-gpt-image

# 文生图
uv run generate.py --prompt "可爱柴犬头像" --size 1024x1024 --quality high

# 使用本地参考图编辑
uv run generate.py --prompt "转换为油画风格" --input-image ./photo.png

# 使用远程参考图编辑
uv run generate.py --prompt "保持主体，修改背景" --input-image https://example.com/photo.png
```

图片默认保存在 `./generated/`。完整参数、API 契约和故障排查见 [SKILL.md](./SKILL.md)。
