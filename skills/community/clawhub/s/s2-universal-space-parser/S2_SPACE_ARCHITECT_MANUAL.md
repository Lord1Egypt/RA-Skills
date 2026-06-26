# 🌌 S2 Space Architect: Enhancement Module Manual
**《S2 空间造物主·增强组件设计与销售使用指南》**

**Document ID:** S2-ARCHITECT-GUIDE-V1.0
**Target Audience:** 智能家居方案设计师、技术型销售工程师 (Sales Engineer)、全屋智能交付大拿。

---

## 1. 模块定位与核心哲学 (Philosophy)

告别传统的“五金店报菜名”式 Excel 报价单。**S2 空间造物主 (The Space Architect)** 是基于《SSSU 空间标准单元法则》构建的终极空间配置可视化引擎。

本组件的核心哲学是**“满配穷举，做减法设计 (Pruning)”**：
1. **去品牌化 (Brand Agnostic)**：组件不输出特定品牌的 SKU，而是输出底层的物理逻辑（如：不写“某某品牌人体传感器”，而是“24GHz/77GHz 毫米波存在感知雷达”）。
2. **六维张量 (The 6-Element Matrix)**：将复杂的智能硬件降维打击，完美归类到“光、气、声、电磁、能、视”六个基础物理维度。
3. **降维销售**：让客户直观地看到每个房间的“灵魂（场景）”与“肉体（硬件）”是如何结合的，极大提升方案的客单价与专业度。

---

## 2. 组件架构与文件清单 (Architecture)

本增强组件由“Python 穷举解析后端”与“React 全息驾驶舱前端”两部分组成，无缝挂载于 S2 OS 或任何企业级私有化平台之上。

### 📦 后端引擎字典 (Python)
* `s2_parser_engine.py`: 主解析引擎，提供对外的指令/API 调用接口。
* `dict_01_residential_core.py`: 核心起居空间字典 (涵盖客厅、卧室等)
* `dict_02_leisure_outdoor.py`: 休闲户外空间字典 (涵盖影音室、车库等)
* `dict_03_commercial_hospitality.py`: 商业服务空间字典 (涵盖酒店、咖啡馆等)
* `dict_04_office_industrial.py`: 办公产业空间字典 (涵盖会议室、厂房等)
* `dict_05_health_mobility.py`: 康养移动空间字典 (涵盖病房、房车等)

### 🖥️ 前端全息驾驶舱 (Next.js / React)
* `src/app/architect/page.tsx`: The Space Architect 交互式赛博数据看板。

---

## 3. 销售工程师与设计师实战指南 (User Guide)

### 🎯 场景一：展厅客户接待 (The Pitch)
当客户来到智能家居展厅，或者在方案汇报会议上：
1. **打开驾驶舱**：在平板或大屏上打开 `http://localhost:3000/architect`。
2. **选择空间**：询问客户重点关注的空间（如：“您平时喝茶吗？我们来看看『智能茶室』的空间矩阵”）。
3. **引导六要素**：
   * 指着【光】的卡片告诉客户：“为了凸显您的茶具，我们配置了低色温的聚光射灯。”
   * 指着【气】的卡片告诉客户：“由于需要点香，系统配置了茶香辅助抽风系统，控制香雾的走向。”
4. **价值传递**：让客户明白，他买的不是一堆冷冰冰的开关，而是一套拥有“感知、计算、执行”能力的微型生态系统。

### ✂️ 场景二：方案裁减与落地 (The Pruning)
后台输出的是**顶配穷举字典**。设计师的职责是根据客户预算进行**“做减法”**：
1. **预算受限**：客户觉得“智慧客厅”造价太高。
   * *设计师操作*：在方案中将【电磁】维度的“77GHz 毫米波”降级为“红外 PIR 传感器”，将【光】维度的“RGBW 幻彩洗墙灯带”删减。
2. **管线受限**：老房改造，无法布置新风管道。
   * *设计师操作*：在【气】维度中，将“中央空调/新风底层网关”裁减，替换为“红外转发器控制的壁挂空调”。
3. **生成 BOM 表**：裁减完毕后，依据最终的六要素基元，在公司的 ERP 或报价库中，填入具体的合作品牌（如紫光、鸿雁、绿米、涂鸦）的 SKU 与单价，生成最终报价单。

---

## 4. 极客部署指南 (For Developers)

### 🌉 建立 Next.js API 路由桥梁
在您的 Next.js 前端项目中，新建文件 `src/app/api/parse-space/route.ts`，以便前端调用 Python 引擎：

```typescript
import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import util from 'util';
import path from 'path';

const execAsync = util.promisify(exec);

export async function POST(request: Request) {
  try {
    const { space } = await request.json();
    const pythonScriptPath = path.join(process.cwd(), '../s2_space_parser/s2_parser_engine.py');
    const { stdout, stderr } = await execAsync(`python3 ${pythonScriptPath} --space "${space}"`);
    
    if (stderr) console.error('Python Error:', stderr);
    return NextResponse.json(JSON.parse(stdout));
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

在 src/app/architect/page.tsx 前端中，通过 fetch('/api/parse-space') 发起请求，即可瞬间解锁全宇宙 62 个空间的实时解析能力！