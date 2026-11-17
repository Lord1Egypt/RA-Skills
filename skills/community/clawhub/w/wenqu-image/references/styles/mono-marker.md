# 单色马克笔风格参考库（mono-marker-style）
> 通用画图规范见 [core-principles.md](../core-principles.md)、[pitfalls.md](../pitfalls.md)。


> 参考图存放于 `https://github.com/gogoingai/wenqu-skills/tree/master/wenqu-image-assets/styles/mono-marker/`

第三种手绘风格家族，与手绘插画风格（[handdrawn.md](handdrawn.md)）、Excalidraw 风格（[excalidraw.md](excalidraw.md)）都不同——核心特征是**全图单一主色调、奶油色背景、波浪线引出注释**，视觉上更像用马克笔在米色笔记本上手绘的图解。

| 特征 | 描述 |
| --- | --- |
| 背景 | 米白色/奶油色（非纯白），带轻微纸张质感 |
| 配色 | **全图只用一种主色**（如绿色/蓝色）：节点描边、节点填充、连接箭头、分组外框全部同色系，只有极少数"类别标签"节点例外用灰色 |
| 节点 | 圆角胶囊/椭圆形，同色系描边与填充（填充可以是浅色调，不强制饱和实心） |
| 分组框 | 粗描边圆角矩形/胶囊形状，内部无填充（透明），把一组节点框在一起 |
| 线条 | 手绘感圆润流畅，不是锯齿状潦草描边（区别于 Excalidraw 的 rough.js 感） |
| 注释连接 | **标志性特征**：节点向右侧引出一条卷曲波浪线（形似手绘的 `~`），末端带箭头，连接到黑色手写说明文字；左侧/其他方向的说明用直线小箭头即可 |
| 字体 | 手写体，笔画偏粗饱满 |

完整风格选择见 `SKILL.md` 风格库表。

### 生成规则（--ref 必须，prompt 只写轻描述——见 pitfalls.md 踩坑 9）

**--ref 必须**：这套风格的"波浪线注释"、"同色系分组框"等细节仅靠文字描述很难稳定复现，务必传参考图：

```
--ref "$(wenqu image fetch-ref mono-marker/mono-marker-01-gateway-flow.png)"          # 竖向分组流程
--ref "$(wenqu image fetch-ref mono-marker/mono-marker-02-branch-decision.png)"       # 含判断菱形的分支合并
--ref "$(wenqu image fetch-ref mono-marker/mono-marker-03-layered-arch.png)"          # 多层横向分层架构
--ref "$(wenqu image fetch-ref mono-marker/mono-marker-04-sync-async-comparison.png)" # 左右并排对比
```

**prompt 只写"参考图风格与内容"，不要逐条复述视觉细节**（单色调、波浪线注释、分组框等一律交给 `--ref`）：

```
参考图风格，[颜色]单色调。[内容描述]。所有文字用中文，拼写清晰。
```

**⚠️ 配色可替换**：主色可以换成蓝、橙、紫等任意单一颜色，只要保证全图同一色系——一旦引入第二种高饱和度颜色（灰色类别标签除外），就偏离了这套风格的识别特征。指定颜色时在 prompt 里点出"[颜色]单色调"即可，不需要展开描述"节点、描边、箭头都用这个颜色"，--ref 已经锚定了这个规则。

### 参考图索引

| 文件 | 图类型 | 特点 |
| --- | --- | --- |
| `mono-marker-01-gateway-flow.png` | 竖向分组流程图 | 顶部入口→网关层分组框（三步骤串联）→底部三路分发，右侧波浪线引出每步说明，蓝色单色调 |
| `mono-marker-02-branch-decision.png` | 含判断菱形的分支流程 | 判断菱形分两路，左右间距拉大、分支间无任何连线，各分支独立两步串联与波浪线注释，最终向下汇合，橙色单色调 |
| `mono-marker-03-layered-arch.png` | 三层横向分层架构 | 接入层、应用层、数据层三个分组框纵向堆叠，层内节点横向排列，层间箭头相连，紫色单色调 |
| `mono-marker-04-sync-async-comparison.png` | 左右并排对比 | 同步调用 vs 异步调用两个分组框并排，异步侧用虚线箭头表示延迟，底部波浪线引出结论，红色单色调 |

### Prompt 模板片段

**竖向分组流程（含波浪线注释）** — 参考 `mono-marker-01`：
```
参考图风格，[颜色]单色调。顶部「[入口节点]」，箭头向下进入分组框「[分组名]」，框内纵向串联 [N] 个节点：「[步骤1]」→「[步骤2]」→…，每个节点引出说明文字：「[说明1]」「[说明2]」…分组框下方指向底部横向排列的 [N] 个节点：「[分支1]」「[分支2]」…所有文字用中文，拼写清晰。
```
