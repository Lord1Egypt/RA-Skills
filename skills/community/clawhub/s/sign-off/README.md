# 🖌️ Sign-Off

> 给 AI 输出加个性化落款签名。像对讲机的 Over，让 AI 说完了你知道。
>
> Add a personalized signature to mark the end of AI output. Like saying "Over" on a walkie-talkie.

## 效果 / Preview

```
杭州今天多云17°C，晚上有小雨，记得带伞。

      小橘 书于杭州 春
      🏮 [橘印]
```

一看落款 → AI 说完了 → 该你了。
See the signature → AI is done → your turn.

## 安装 / Install

### OpenClaw

```bash
clawhub install sign-off
```

### Git

```bash
git clone https://github.com/Z35th3rJJ/sign-off.git ~/.openclaw/workspace/skills/sign-off
cp ~/.openclaw/workspace/skills/sign-off/sign-off.json.example ~/.openclaw/workspace/sign-off.json
```

## 配置 / Configuration

复制 `sign-off.json.example` 为 `sign-off.json`，修改配置：

Copy `sign-off.json.example` to `sign-off.json` and customize:

```json
{
  "name": "小橘",
  "location": "杭州",
  "template": "{name} 书于 {location} {season}\n{emoji} {seal}",
  "emoji": "🏮",
  "seal": "[橘印]",
  "contextMode": "auto"
}
```

也可以直接告诉 AI：
Or just tell your AI:

> "你的签名改成 From 小橘, Hangzhou, with 🧡"
>
> "Change your signature to From Luna, Hangzhou, with 🧡"

## 预装模板 / Built-in Templates

| 模板 / Template | 风格 / Style | 预览 / Preview |
|-----------------|-------------|----------------|
| 🖌️ calligraphy | 书法风 / Calligraphy | 小橘 书于杭州 春 🏮 [橘印] |
| 💌 letter | 信笺风 / Letter | From 小橘, Hangzhou, with 🧡 |
| 🎭 ancient | 古风 / Classical | 蛇年春，小橘灯下 |
| 🤖 geek | 极客风 / Geek | // signed: xiaoju @ hangzhou |
| 📻 walkie-talkie | 对讲机风 / Walkie-Talkie | 📻 小橘 Over |

使用：告诉 AI "给我换成书法风" / "Switch to calligraphy style"

## 变量 / Variables

详见 [变量参考](docs/variables.md) / See [Variables Reference](docs/variables.md)

| 变量 / Variable | 说明 / Description | 示例 / Example |
|-----------------|-------------------|----------------|
| `{name}` | AI 名字 | 小橘 |
| `{location}` | 地点 | 杭州 |
| `{emoji}` | 自定义图标 | 🏮 |
| `{seal}` | 印章文字 | [橘印] |
| `{season}` | 季节（自动） | 春/夏/秋/冬 |
| `{weather}` | 天气（自动） | 晴/雨 |
| `{time}` | 时段（自动） | 午后/深夜 |
| `{greeting}` | 问候（自动） | 早安/夜安 |
| `{dayOfWeek}` | 星期（自动） | 周五 |
| `{zodiac}` | 生肖（自动） | 蛇年 |

## 贡献模板 / Contribute

欢迎提交你的签名模板！

1. Fork 本仓库 / Fork this repo
2. 在 `templates/` 下新建 JSON 文件 / Add a JSON file under `templates/`
3. 参考已有模板格式 / Follow existing template format
4. 提交 PR / Open a PR

## License

MIT
