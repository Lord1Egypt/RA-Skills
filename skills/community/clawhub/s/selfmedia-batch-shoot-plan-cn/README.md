# 批量拍摄排期单

![推广图](assets/promo-1600x900.png)

把已定稿的多条脚本按场景和机位合并，减少换景、换机位与道具搬运，得到可带到现场核对的拍摄顺序及素材命名表。

**输入**：已有脚本编号、场景、人物和动作/台词摘要；附已知场地、道具与机位，可拍时段及人物档期可选。  
**结果**：拍摄顺序表、现场核对项、唯一素材文件名；若关键资料缺失，先输出明确缺项，不虚构排期。

## 安装

```bash
npx skills add xxjrq/selfmedia-batch-shoot-plan-cn
```

## 适用范围

适合单次章节、场景或短文的集中拍摄（最多100条记录）。它只重排用户已经确定的内容，不生成小说、脚本或分镜。超过100条请先按批次拆分。

## 使用方式

粘贴脚本表及已知人物、场地、道具和机位；时段可选。成片时长保留为成片目标，布置、排练和重拍耗时未给时只输出非钟点顺序。例如：

> 根据以下已定稿脚本生成拍摄顺序和素材命名表。场地为吧台和靠窗桌；机位已确定为 A、B、C。资料缺失请先列出，不要补写镜头或剧情。

交付会先核对资料，然后按“场地 → 布置 → 机位 → 人物”排序，并使用 `项目_日期_场景_机位_脚本号_条次` 生成文件名。

## 可复制示例

- [完整输入](fixtures/success-input.md) → [非钟点拍摄顺序与命名交付](fixtures/success-output.md)
- [真正缺核心字段的输入](fixtures/failure-input.md) → [已确认项与缺项清单](fixtures/failure-output.md)

旧的 I01 采访输入虽然没有项目代号、拍摄日期、成片时长和机位，但脚本编号、场景、人物、动作摘要均齐全。它不是失败案例；[旧前向结果](fixtures/forward-failure.md)保留为“可先整理单场景预排”的部分/可选信息案例。当前 failure-input 确实缺脚本编号和动作/台词摘要，输出列出已确认项与缺项并停止生成完整顺序和命名记录。

- [完整输入前向参考](fixtures/forward-success.md) · [可预排但可选信息缺失的前向参考](fixtures/forward-failure.md)
- [额外新输入](fixtures/forward-additional-input.json) → [额外成功/缺核心字段结果](fixtures/forward-additional.md)

## 自检

在仓库根目录运行：

```bash
python3 scripts/self_test.py
```

该检查只依赖 Python 标准库，验证发布所需结构、名称一致性、图标尺寸和成功/失败样例。

## 来源与许可证

业务方向参考 [social-media-skills/skills](https://github.com/social-media-skills/skills) 的公开分类；本仓库说明、流程和示例均为原创，未复制其内容或代码。采用 [MIT-0](LICENSE)。
