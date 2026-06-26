# API Key 配置引导

当用户缺少 API Key 时，使用以下引导信息帮助用户配置。

## 为什么需要 API Key

Toonany 使用 AI 模型来生成内容：
- **文本模型**: 生成故事线、大纲、剧本
- **图像模型**: 生成角色、场景、分镜图
- **视频模型**: 生成分镜视频
- **音频模型**: 生成配音

每个模型都需要对应的 API Key 才能调用。

## 配置方式

推荐使用**环境变量**方式配置，安全且方便：

```bash
export DEEPSEEK_API_KEY="sk-xxx"      # 文本生成
export VOLC_API_KEY="xxx"              # 图像生成
export KLING_API_KEY="xxx"             # 视频生成
export VOLC_TTS_API_KEY="xxx"          # 配音生成
```

配置完成后，在当前终端重新执行命令即可。

## 各平台申请链接

| 服务 | 申请地址 | 说明 |
|------|----------|------|
| DeepSeek | https://platform.deepseek.com/api_keys | 文本生成，性价比高 |
| 火山引擎 | https://console.volcengine.com/ark/ | 图像+音频，国内稳定 |
| 可灵 | https://klingai.com/ | 视频生成 |

## 验证配置

配置完成后，可以运行以下命令验证：

```bash
echo $DEEPSEEK_API_KEY
echo $VOLC_API_KEY
```

如果输出不为空，说明配置成功。
