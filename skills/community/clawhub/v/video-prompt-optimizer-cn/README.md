# AI视频提示词优化

![AI 视频提示词优化](assets/promo-1600x900.png)

把模糊的中文 AI 视频想法整理为可复制的最终提示词、镜头动作顺序和连续性约束。输入画面意图、已有提示词与素材描述，得到一份可交给生成工具的画面说明；直接用支持 Skill 的助手处理，无需浏览器或额外 API Key。

适合中文自媒体创作者和小店经营者在生成视频前，把“想拍得好看”的描述收紧成更稳定、可交接的画面说明。

## 立即使用

把下面的信息交给支持读取 `SKILL.md` 的助手：

```text
画面意图：让路过店铺的人觉得这杯桂花拿铁温暖、值得进店购买。
原始提示词：秋天咖啡，桂花拿铁，很高级，女孩喝一口，镜头好看。
时长：6 秒，单镜头；比例：9:16；用途：抖音店铺新品预告。
主体：成年女店员，米白针织衫、深棕围裙；透明玻璃杯装的桂花拿铁。
限制：暖色自然窗光；不要文字、品牌标识、第二人物或夸张蒸汽。
```

交付会包含四段：最终提示词、镜头动作顺序、连续性约束、对比与待确认。完整可运行样例见 [fixtures/success-input.md](fixtures/success-input.md) 和 [fixtures/success-expected.md](fixtures/success-expected.md)。资料不足时，参照 [fixtures/failure-missing-brief.md](fixtures/failure-missing-brief.md) 先补齐主体和画面意图；时长或镜头数可省略，届时会按一个 5–8 秒镜头处理，并明确标注这一假设。

## 使用边界

- 提示词写作的语言模型与实际视频生成模型是两回事。若你选择 Opus 5.5 来写提示词，会保留该选择，不会自动切换或强制版本。
- 不虚构实际视频模型的参数、seed、专有语法或能力；未指定模型时输出模型无关的自然语言提示词。
- 只整理提示词与镜头说明；实际视频生成由你使用的工具完成。

## 验证

无需安装依赖：

```bash
node scripts/self-test.mjs
```

## 许可证

本 Skill 提供原创视频提示词整理指令与示例，采用 [MIT-0 License](LICENSE)。

## 安装

```bash
npx skills add xxjrq/video-prompt-optimizer-cn
```

也可以把本仓库目录复制到 Agent 的 Skills 目录，再用 `$video-prompt-optimizer-cn` 加上你的输入调用。
