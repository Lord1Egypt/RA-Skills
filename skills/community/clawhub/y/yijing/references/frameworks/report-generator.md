# 报告生成器

## 用途

将易经商业分析输出为可视化报告，支持 HTML（可打印为 PDF）和纯 SVG 图表。

## 输出模式

### 模式一：分析报告（HTML → 打印为 PDF）

基于 `{baseDir}/references/frameworks/report-template.html` 模板，将分析结果渲染为完整报告。

生成方式：
1. 将分析内容填入模板中的对应占位符
2. 卦象图引用 `{baseDir}/references/hexagrams/{卦序}-{拼音}.svg`
3. 用 Write 工具输出为 `.html` 文件
4. 用户打开 HTML 文件后 `Ctrl+P` → 另存为 PDF

### 模式二：卦象图（SVG）

直接引用 `{baseDir}/references/hexagrams/` 下的 SVG 文件。每个文件对应一个卦象。

在分析输出中嵌入卦象图时：
```markdown
![卦名]({baseDir}/references/hexagrams/03-zhun.svg)
```

### 模式三：多卦对比图

需要同时展示多个卦象时，水平排列 SVG，可用于对比主卦、错卦、综卦。

## 报告模板结构

```
封面
├── 标题：易经商业决策分析报告
├── 日期
├── 核心问题
└── 卦象图（主卦SVG）

正文
├── 一、情境识别（卦象匹配 + 西方模型类比）
├── 二、阶段判断（六爻当前位 + 建议）
├── 三、核心矛盾（阴阳消长分析）
├── 四、行动策略（卦象原则 + 西方理论操作化）
├── 五、风险警示（关键误用 + 关联卦象交叉验证）
├── 六、演化预判（卦序方向）
└── 七、双格栅验证（中西对比结论）

附录
├── 关联卦象图
└── 信息来源
```

## 卦象图文件清单

所有 SVG 文件位于 `{baseDir}/references/hexagrams/`：

| 文件 | 卦象 | 文件 | 卦象 |
|------|------|------|------|
| `01-qian.svg` | 乾䷀ | `16-yu.svg` | 豫䷏ |
| `02-kun.svg` | 坤䷁ | `17-sui.svg` | 随䷐ |
| `03-zhun.svg` | 屯䷂ | `18-gu.svg` | 蛊䷑ |
| `04-meng.svg` | 蒙䷃ | `19-lin.svg` | 临䷒ |
| `05-xu.svg` | 需䷄ | `20-guan.svg` | 观䷓ |
| `06-song.svg` | 讼䷅ | `21-shihe.svg` | 噬嗑䷔ |
| `07-shi.svg` | 师䷆ | `22-brand.svg` | 贲䷕ |
| `08-bi.svg` | 比䷇ | `23-bo.svg` | 剥䷖ |
| `09-xiaoxu.svg` | 小畜䷈ | `24-fu.svg` | 复䷗ |
| `10-lv.svg` | 履䷉ | `25-wuwang.svg` | 无妄䷘ |
| `11-tai.svg` | 泰䷊ | `26-daxu.svg` | 大畜䷙ |
| `12-pi.svg` | 否䷋ | `27-yi.svg` | 颐䷚ |
| `13-tongren.svg` | 同人䷌ | `28-daguo.svg` | 大过䷛ |
| `14-dayou.svg` | 大有䷍ | `29-kan.svg` | 坎䷜ |
| `15-modesty.svg` | 谦䷎ | `30-li.svg` | 离䷝ |

## 使用指令

当用户要求"生成报告"、"输出PDF"、"画个卦象图"时：

1. **只画卦象**：直接在分析中引用对应 SVG 文件路径
2. **生成完整报告**：读取 report-template.html，填入分析内容，写入 `.html` 文件，告知用户可打印为 PDF
3. **多卦对比**：引用多个 SVG 并排展示
