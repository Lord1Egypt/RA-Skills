# 发布到 ClawHub

这个目录现在已经可以作为 ClawHub skill bundle 发布。

## 发布前检查

先在本地执行：

```bash
npm install
npm run check
```

这会完成：
- TypeScript 构建
- 配置结构校验
- 本地 mock 测试

如果你修改过源码，发布前请确认 `dist/` 是最新的。

## 登录 ClawHub

先安装并登录 CLI：

```bash
npm i -g clawhub
clawhub login
```

## 发布命令

在当前 skill 目录执行：

```bash
clawhub publish . \
  --slug video-wechat-ip-script-agent \
  --name "视频号爆款 IP 脚本工厂" \
  --version 1.3.0 \
  --tags latest,content,wechat-video,medical-aesthetics,personal-brand
```

如果这是后续版本，请同步修改：
- `package.json`
- `SKILL.md`
- 上面的 `--version`

## 发布建议

- `dist/` 建议一起发布，这样安装者不需要先本地编译
- `examples/requests/` 建议保留，方便安装后直接联调
- 如果技能依赖真实模型，请在说明里写清环境变量要求

## 发布后自检

发布成功后，建议至少做一次：

```bash
clawhub install video-wechat-ip-script-agent --force
node skills/video-wechat-ip-script-agent/dist/openclaw.js --file skills/video-wechat-ip-script-agent/examples/requests/script.json
```

如果只做链路验证，可以先设置：

```bash
export MODEL_MOCK_RESPONSE='{"titles":["测试标题"],"hook":"测试钩子","script":"测试脚本","coverText":"测试封面"}'
```
