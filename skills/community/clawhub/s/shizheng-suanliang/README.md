# 市政算量（shizheng-suanliang）

**[English](./README.en.md) | [中文](./README.md)**

**v0.1.0** · 正式量只从 `lis-skill-bus` 按 `contract_id` 取契约；不碰图纸解析，只把 `cad-file-reader` 的市政识图契约（`municipal-geometry` 识图包产物）变成 **管道延米带 + 管径分档 + 井类计数 + 道路面积带 + 材料清单**。

正式识图链路固定为 `cad-file-reader -> cad-municipal-geometry/v1 -> lis-skill-bus -> shizheng-suanliang`。本技能不读取 DWG/DXF/PDF，也不提供绕开 `cad-file-reader` 或 `lis-skill-bus` 的第二套识图路径。`--municipal`/位置参数是文件入口，必须显式 `--allow-manual`，一律按 `manual` 降级，不是正式量。

## 先确认能不能用

单独安装本技能，**不会自动带入** `cad-file-reader` 和 `lis-skill-bus`。从市场安装后先跑一次：

```bash
python3 scripts/municipal_qty.py --check-deps
```

- 两项都找到：退出码 0，正式识图链路可开工。
- 缺任意一项：退出码 20/21（缺 reader 20、缺 bus 21），明确列出缺什么，并给一条可复制安装命令；此时不能从 DWG 开始识图。文件契约仍可计算，但必须显式 `--allow-manual`，结果 `final_quantity=false`，不是正式量。
- 识图前置：先跑 `cad-file-reader` 的市政识图包生成 `*.municipal.json`（schema `cad-municipal-geometry/v1`）。

## 能做什么

- 消费 `cad-municipal-geometry/v1` 契约 JSON，输出 `cad-municipal-qty/v0.1` 的 `json + md + csv`。
- 管道延米按系统分组（雨水/污水/给水/再生水/热力/燃气/电力/通信），图面几何段长 ×[1.00, 1.15] 估算带；无法映射系统的段单独归「未分类」。
- 管径从 `pipe_network[].pipe_size` 文本提取（DN/De/d/Φ），按 300~1500+ 分档**只计数**，不做管径×段长强配。
- 井类（检查井/雨水口/跌水井/阀门井/泵站）按系统计数；管网开放端点/汇聚节点作连通性交叉核对并提示。
- 道路面积带＝道路中线/边线段长 × labels 宽度标注多数档（±15%）；缺宽度标注即 `unavailable`，不默认宽度。
- 路面材料/做法只列清单并标注层厚缺失，不做分层面积。
- 识别待复核项与警告透传：图例剔除、缺管径、微圆剔除、开放端点偏少等，全部可追溯。
- m 单位图纸必须给 `unit_scale`；缺了只出计数与缺项清单，不出长度/面积。

## 用法

```bash
# 只体检契约（不出量）
python3 scripts/municipal_qty.py --validate 市政识图/xxx.municipal.json

# 手工/文件降级：必须显式 --allow-manual，结果 final_quantity=false
python3 scripts/municipal_qty.py --municipal 市政识图/xxx.municipal.json \
    --allow-manual --out-prefix 市政算量

# 正式入口：只从 lis-skill-bus 按 contract_id 取契约
python3 scripts/municipal_qty.py --from-contract <contract_id> \
    --project 项目 --out-prefix 市政算量
```

## 不做什么

- 不替代工程量清单编制、竣工计量、劳务结算与报价（估算带 `final_quantity=false`）。
- 不做土方：无横断面填挖数据，任何土方数字都是编造。
- 不出桥梁/涵洞/隧道构件量（桩基、箱梁、衬砌等本版只透传候选与待复核项）。
- 不做水力计算、结构计算、设计合规判断。

## 授权

CC-BY-NC-SA-4.0，仅限非商业用途；商业使用须另行书面授权，见 `LICENSE.md`。


## 手工兜底参数（v0.3.0）

- `--unit-scale FACTOR`：坐标→mm 换算系数手工指定（m 图 1000，mm 图 1），覆盖契约声明；歧义区停算时使用。
- `--road-width M`：道路红线宽显式传参（m），缺宽度标注时使用，不默认。
