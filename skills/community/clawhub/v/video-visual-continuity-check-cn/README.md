# 多镜头视觉连续性检查

![多镜头视觉连续性检查推广图](assets/promo-1600x900.png)

在拍摄或生成视频前，快速找出既有镜头表里的角色、道具、光线和空间断裂，并得到不改故事的最小修订建议。

输入是已写好的镜头表，以及人物/场景参考说明；结果是一份按严重度排序、标明证据镜头的连续性问题清单和可执行的最小改动。缺少镜头表或参考资料时，会明确列出缺项，不补造设定。

严重度有三级：高表示人物身份/外观、道具状态或场景地点冲突；中表示持有手侧、道具位置或来光方向/色温差异；低表示光线明暗等较轻偏差。

## 安装

```bash
npx skills add xxjrq/video-visual-continuity-check-cn
```

## 适用范围

检查单次章节、场景或短片的既有方案，表格最多 100 行。它不创作新故事或分镜，也不充当模型编译器；超过上限请按章节或场景分批提交。

## 输入示例

```json
{
  "references": {"character": "林岚：深蓝外套、红围巾", "scene": "书店门口，傍晚暖光从左侧照入"},
  "shots": [
    {"id": "01", "character": "林岚穿深蓝外套和红围巾", "prop": "右手拿黄色纸袋", "lighting": "暖光从左侧", "space": "书店门口面向右"}
  ]
}
```

检查器只报告文字能明确支持的冲突，不会因为两镜措辞不同就报错。道具交接、人物移动、换装或布光/时间变化已写明时，可直接写入该镜头文字，或使用 `"transition": {"prop": "放下纸袋"}`；它只解释纸袋本身，不会豁免手机等其他道具的位置变化。每镜须有 `id` 与至少一项画面信息；镜头涉及人物或场景时，参考中须有对应的 `character` 或 `scene`。

可复制的完整输入和交付：

- [成功输入](fixtures/success-input.json) 与 [成功交付](fixtures/success-output.json)
- [缺料输入](fixtures/failure-input.json) 与 [缺料交付](fixtures/failure-output.json)

## 本地检查

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/self_test.py
```

检查器同时读取 `description`、`visual` 和分类画面字段；只比较能确认是同一人物的服装与手持道具。可提供 `character_id` 和人物参考字典消除歧义。`transition` 只解释对应类别的明确动作，未发生的换装不能消除服装问题。

这是保守的中文文字检查器，不分析图片或视频。人物身份、措辞或变化含义不清时保留人工确认，不将未识别内容宣称为一致。自检验证必要文件、PNG 签名、成功/缺料输入，并执行独立正反回归，包括不同人物、具名持有人、描述字段、分类动作交代与否定动作。检查器可直接执行：`python3 scripts/check_continuity.py fixtures/success-input.json`。

## 来源与许可

本 Skill 的说明、步骤和示例均为原创。仅参考 [seaartpublic/skills](https://github.com/seaartpublic/skills) 中关于故事板辅助的业务用途，不复制其文本或源码；未引入其中的内容。仓库采用 [MIT License](LICENSE)。

English documentation: [README.en.md](README.en.md)
