# 手绘插画风格参考库（handdrawn-style）
> 通用画图规范见 [core-principles.md](../core-principles.md)、[pitfalls.md](../pitfalls.md)。


> 参考图存放于 `https://github.com/gogoingai/wenqu-skills/tree/master/wenqu-image-assets/styles/handdrawn/`

这套风格适合技术文章配图、社交媒体传播图、流程说明图。核心特征：

| 特征 | 描述 |
| --- | --- |
| 线条感 | 圆角矩形有轻微手绘线条感，非完全机械规整 |
| 字体 | 略带手写质感，中文圆润、标题加粗 |
| 背景 | 纯白或暖白，整体明亮通透 |
| 图标 | 鲜明活泼，是全图最鲜艳的元素，与浅色底色形成反差 |
| 配色 | 各步骤用不同浅色底色（浅蓝、浅黄、浅橙、浅绿、浅紫），标题或数字圆圈用深色 |
| 标题栏 | 圆角矩形横幅，两侧带「——」装饰横线 |
| 步骤编号 | 填色圆圈（①②③…），左上角或正上方，颜色比卡片底色深一档 |

### 生成规则（--ref 必须，prompt 只写轻描述——见 pitfalls.md 踩坑 9）

**`--ref` 必须**：传入参考图锚定视觉风格（自然线条、水彩填色感），仅靠 prompt 描述无法稳定复现。推荐参考图：

```
--ref "$(wenqu image fetch-ref handdrawn/handdrawn-01-skill-creation-loop.png)"
```

（也可换 `handdrawn-02` 至 `handdrawn-07`，选和目标图类型最接近的，见下方索引）

**prompt 只写"参考图风格与内容"，不要逐条复述视觉细节**（图标怎么画、线条怎么处理等一律交给 `--ref`）：

```
参考图风格，[横向宽屏构图 / 竖版构图]。[内容描述]。所有文字用中文，拼写清晰。
```

**完整调用示例：**

```bash
RAND=$(openssl rand -hex 8)
wenqu image generate --provider codex \
  --prompt "参考图风格。[图内容描述...]。所有文字用中文。" \
  --ref "$(wenqu image fetch-ref handdrawn/handdrawn-01-skill-creation-loop.png)" \
  --out /tmp/article-img-${RAND} \
  --timeout-sec 300
```

### 参考图索引

| 文件 | 图类型 | 特点 |
| --- | --- | --- |
| `handdrawn-01-skill-creation-loop.png` | 横向线性流程、决策菱形、反馈弧线 | 步骤卡片与下方"否"路径循环框 |
| `handdrawn-02-circular-flow.png` | 环形流程与放射状原始证据区 | 圆形箭头串联 5 步，底部输入汇集区 |
| `handdrawn-03-risk-freedom-table.png` | 横向分行对比表 | 每行带仪表盘图标，列标题与要点清单 |
| `handdrawn-04-layered-arch.png` | 竖向三层架构与右侧指标卡 | 每层圆角大框内有图标和副标，层间带箭头标注 |
| `handdrawn-05-mindmap.png` | 中心辐射思维导图 | 中央大节点、四角分支卡片、底部总结横幅 |
| `handdrawn-06-retro-agent-flow.png` | 竖向多层流程与内嵌循环大框 | 顶部触发→扫描信号→Agent 循环区块，循环内含分支列表，左侧回环箭头 |
| `handdrawn-07-curator-flow.png` | 左右双列流程与顶部汇合底部 | 共同触发节点分叉为左右两列，各列独立逻辑，底部再汇合 |

### 各图类型对应的 prompt 模板片段

**横向线性流程（含判断菱形）** — 参考 `handdrawn-01`：
```
参考图风格，横向宽屏构图。主流程从左到右：[步骤1] → [步骤2] → …；判断「[条件]？」，是→[结果分支]，否→继续主流程；末尾弧形箭头回到起点，标注「[注释]」。所有文字用中文，拼写清晰。
```

**竖向三层架构** — 参考 `handdrawn-04`：
```
参考图风格，竖版构图。三层架构从上到下：[层1名]（[功能标签]）→ [层2名]（[功能标签]）→ [层3名]（[功能标签]），层间箭头带标注文字。底部一句话总结「[总结]」。所有文字用中文，拼写清晰。
```

**环形流程** — 参考 `handdrawn-02`：
```
参考图风格。环形流程：[步骤1] → [步骤2] → … → [步骤N] → 弧形箭头回到步骤1（顺时针）。底部标注输入来源「[来源]」，箭头引向对应环形步骤。所有文字用中文，拼写清晰。
```

**中心辐射思维导图** — 参考 `handdrawn-05`：
```
参考图风格。中央核心词「[核心词]」，四角延伸分支：「[分支A]」「[分支B]」「[分支C]」「[分支D]」。底部一句话总结「[总结]」。所有文字用中文，拼写清晰。
```
