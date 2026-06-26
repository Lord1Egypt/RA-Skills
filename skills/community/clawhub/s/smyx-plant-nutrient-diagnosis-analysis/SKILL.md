---
name: "smyx-plant-nutrient-diagnosis-analysis"
description: "AI-powered plant nutrient deficiency diagnosis from leaf images. Detects leaf color, morphology changes (pale green/yellow-green/purple-red, marginal scorch, interveinal chlorosis) via computer vision, matches against common deficiency symptom databases, and outputs the most likely deficient nutrient element (nitrogen, phosphorus, potassium, iron, magnesium, zinc, etc.) with confidence score. Enables precision fertilization, avoids blind over-fertilization. Scenarios: smart planters, home gardening, agricultural greenhouses, plant factories. | 通过智能花盆、农业大棚或手机拍摄的植物叶片高清图像，利用AI视觉分析技术识别叶片颜色、形态变化（如叶色浅绿/黄绿/紫红、叶缘焦枯、叶脉间失绿等），与常见营养缺乏症特征库比对，输出最可能缺乏的营养元素（氮、磷、钾、铁、镁、锌等）及置信度。有助于精准施肥，避免盲目用肥造成浪费或伤害。应用场景：智能花盆、家庭园艺、农业大棚、植物工厂。"
version: "1.0.0"
---

# Plant Nutrient Deficiency Diagnosis | 植物缺素症视觉诊断

AI-powered plant nutrient deficiency diagnosis from leaf images. Detects leaf color, morphology changes (pale
green/yellow-green/purple-red, marginal scorch, interveinal chlorosis) via computer vision, matches against common
deficiency symptom databases, and outputs the most likely deficient nutrient element (nitrogen, phosphorus, potassium,
iron, magnesium, zinc, etc.) with confidence score. Enables precision fertilization, avoids blind over-fertilization.
Scenarios: smart planters, home gardening, agricultural greenhouses, plant factories.

通过智能花盆、农业大棚或手机拍摄的植物叶片高清图像，利用AI视觉分析技术识别叶片颜色、形态变化（如叶色浅绿/黄绿/紫红、叶缘焦枯、叶脉间失绿等），与常见营养缺乏症特征库比对，输出最可能缺乏的营养元素（氮、磷、钾、铁、镁、锌等）及置信度。有助于精准施肥，避免盲目用肥造成浪费或伤害。应用场景：智能花盆、家庭园艺、农业大棚、植物工厂。

## 🎯 AI 角色

**假设你是一个专业的植物营养学AI。你的任务是分析植物叶片的图像（老叶或新叶），识别叶片颜色异常、形态畸变、失绿分布等特征，与常见缺素症状进行比对，输出最可能缺乏的营养元素类型。不要提供具体化肥浓度，仅输出缺素诊断结果及置信度。
**

## 任务目标

- 本 Skill 用于：通过植物叶片高清图像进行缺素症视觉诊断，输出最可能缺乏的营养元素类型、置信度及施肥方向建议
- 能力包含：叶片颜色异常检测、叶脉间失绿识别、叶缘焦枯检测、老叶/新叶症状区分、常见缺素症比对（氮/磷/钾/铁/镁/锌/钙/硼/锰/铜/硫等）、置信度评分、施肥方向建议
- 触发条件:
    1. **默认触发**：当用户提供植物叶片图像或视频需要缺素诊断时，默认触发本技能
    2. 当用户明确需要植物营养诊断时，提及缺素、黄叶、叶缘焦枯、叶脉间失绿、缺氮、缺磷、缺钾、缺铁、缺镁、植物营养不良、叶片发黄等关键词，并且上传了图像或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史缺素诊断报告、历史植物营养报告、缺素症报告清单、显示所有缺素报告、查询植物营养诊断记录
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有缺素诊断报告"、"
       显示植物营养报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_plant_nutrient_diagnosis_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行植物缺素症视觉诊断前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：【最高优先级】检查技能所在目录的配置文件（优先）
        路径：skills/smyx_common/scripts/config.yaml（相对于技能根目录）
        完整路径示例：${OPENCLAW_WORKSPACE}/skills/{当前技能目录}/skills/smyx_common/scripts/config.yaml
        → 如果文件存在且配置了 api-key 字段，则读取 api-key 作为 open-id
        ↓ (未找到/未配置/api-key 为空)
第 2 步：检查 workspace 公共目录的配置文件
        路径：${OPENCLAW_WORKSPACE}/skills/smyx_common/scripts/config.yaml
        → 如果文件存在且配置了 api-key 字段，则读取 api-key 作为 open-id
        ↓ (未找到/未配置)
第 3 步：检查用户是否在消息中明确提供了 open-id
        ↓ (未提供)
第 4 步：❗ 必须暂停执行，明确提示用户提供用户名或手机号作为 open-id
```

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、userC113、user123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询历史报告记录），并询问是否继续

---

- 标准流程:
    1. **准备图像/视频输入**
        - 提供本地植物叶片高清图像/视频文件路径或网络 URL
        - 拍摄建议：
            - **聚焦叶片**（10-30cm 近距离），单片叶片占画面主要区域
            - **正反面均拍**：正面可见叶色变化，反面可辅助判断叶脉特征
            - **区分老叶/新叶**：老叶症状多提示氮/磷/钾/镁等移动性元素缺乏；新叶症状多提示铁/钙/硼/锌等非移动性元素缺乏
            - **光线充足**（自然光最佳），避免逆光、过曝、阴影
            - **背景简洁**：避免杂乱背景干扰叶片特征识别
        - 支持图像（jpg/png）和视频（mp4/avi/mov）格式
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行缺素诊断**
        - 调用 `-m scripts.smyx_plant_nutrient_diagnosis_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地植物叶片图像/视频文件路径
            - `--url`: 网络植物叶片图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 对象类型，植物场景默认 other
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示植物缺素症诊断历史报告列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看诊断结果**
        - 接收结构化的植物缺素症诊断报告
        - 包含：**叶片特征描述**（颜色异常、失绿分布、形态畸变）、**最可能缺乏元素**（如氮/磷/钾/铁/镁等）、**置信度评分**
          （0-100%）、**症状严重程度**（轻度/中度/重度）、**施肥方向建议**（如"缺氮，建议追施尿素或高氮复合肥"，不涉及具体浓度）
        - **重要提示**：仅输出基于视觉的缺素诊断结果及施肥方向，**不提供具体化肥浓度与用量**；专业施肥方案请咨询农技专家

## 🌿 常见植物缺素症状对照表

| 缺乏元素     | 典型症状                  | 症状部位 | 易发植物       |
|----------|-----------------------|------|------------|
| 🟡 氮(N)  | 老叶均匀黄化、植株矮小、生长缓慢      | 老叶先发 | 叶菜类、玉米、草坪  |
| 🟣 磷(P)  | 叶片暗绿/紫红色、根系发育差、开花延迟   | 老叶先发 | 豆科、玉米、番茄   |
| 🟤 钾(K)  | 老叶叶缘焦枯、叶尖褐变、抗逆性下降     | 老叶先发 | 马铃薯、番茄、烟草  |
| 🟢 铁(Fe) | 新叶叶脉间失绿（黄化）、叶脉仍绿（网纹状） | 新叶先发 | 喜酸植物、柑橘、杜鹃 |
| 🟡 镁(Mg) | 老叶叶脉间失绿、叶片卷曲、提早脱落     | 老叶先发 | 番茄、葡萄、玫瑰   |
| ⚪ 锌(Zn)  | 新叶小而簇生（小叶病）、节间缩短      | 新叶先发 | 玉米、苹果、柑橘   |
| 🟤 钙(Ca) | 新叶畸形/卷曲、生长点坏死、裂果      | 新叶先发 | 番茄（脐腐病）、苹果 |
| 🟡 硼(B)  | 生长点死亡、花器发育不良、茎干裂开     | 新叶先发 | 油菜、甜菜、花椰菜  |
| 🟢 锰(Mn) | 新叶叶脉间失绿（与缺铁相似但更细碎）    | 新叶先发 | 燕麦、大豆、苹果   |
| 🟤 铜(Cu) | 新叶失绿萎蔫、叶尖发白卷曲         | 新叶先发 | 小麦、柑橘、洋葱   |
| 🟡 硫(S)  | 新叶均匀黄化（与缺氮相似但出现在新叶）   | 新叶先发 | 十字花科、豆科    |

## 🔍 缺素症状识别维度

| 维度   | 观察重点          | 判断意义                                     |
|------|---------------|------------------------------------------|
| 症状部位 | 老叶 vs 新叶      | 老叶→移动性元素(N/P/K/Mg)，新叶→非移动性元素(Fe/Ca/B/Zn) |
| 失绿模式 | 均匀失绿 vs 叶脉间失绿 | 均匀→N/S，叶脉间→Fe/Mg/Mn                      |
| 颜色变化 | 黄化/紫红/暗绿/白化   | 紫红→P，暗绿→P，白化→Cu                          |
| 形态畸变 | 小叶/卷曲/畸形/坏死   | 小叶→Zn，卷曲→Ca/Cu，坏死→Ca/B                   |
| 叶缘特征 | 焦枯/褐变/正常      | 焦枯→K，正常→排除K                              |
| 叶片质地 | 厚硬/薄软/正常      | 厚硬→缺P，薄软→缺N                              |

## 📊 缺素严重程度分级

| 等级    | 症状表现            | 施肥建议             |
|-------|-----------------|------------------|
| 🟢 轻度 | 叶片轻微失绿，局部少量变色   | 补充对应元素水溶肥，叶面喷施   |
| 🟡 中度 | 叶片明显黄化/变色，面积扩大  | 追施对应元素肥料，根部+叶面双施 |
| 🟠 重度 | 大面积失绿/畸形，生长严重受阻 | 紧急追肥，咨询农技专家      |
| 🔴 严重 | 植株濒死，叶片大量枯萎脱落   | 立即综合救治，专业农技指导    |

## 💡 施肥方向参考

| 缺素类型  | 施肥方向                       |
|-------|----------------------------|
| 🟡 缺氮 | 追施尿素、高氮复合肥；叶面喷施氨基酸叶面肥      |
| 🟣 缺磷 | 追施过磷酸钙、磷酸二铵；叶面喷施磷酸二氢钾      |
| 🟤 缺钾 | 追施硫酸钾、氯化钾；叶面喷施磷酸二氢钾        |
| 🟢 缺铁 | 叶面喷施EDTA-Fe/硫酸亚铁；调节土壤pH至酸性 |
| 🟡 缺镁 | 追施硫酸镁、钙镁磷肥；叶面喷施硫酸镁溶液       |
| ⚪ 缺锌  | 叶面喷施硫酸锌；土壤施用锌肥             |
| 🟤 缺钙 | 追施硝酸钙、氯化钙；叶面喷施钙肥           |
| 🟡 缺硼 | 叶面喷施硼砂/硼酸溶液；土壤施用硼肥         |
| 🟢 缺锰 | 叶面喷施硫酸锰溶液                  |
| 🟤 缺铜 | 叶面喷施硫酸铜溶液；注意用量防毒害          |
| 🟡 缺硫 | 追施含硫肥料（硫酸铵、硫酸钾等）           |

> ⚠️ 本技能仅提供**施肥方向建议**，**不提供具体化肥浓度与用量**；精准施肥需根据植物种类、生长阶段、土壤检测结果咨询农技专家。

## 🔄 与植物病害的区分要点

| 特征  | 缺素症       | 病害          |
|-----|-----------|-------------|
| 分布  | 全株对称、规律性强 | 局部散发、不规则    |
| 进展  | 缓慢渐进      | 可能快速蔓延      |
| 边界  | 渐变过渡      | 常有明显病斑边界    |
| 附着物 | 无霉层/孢子    | 可能有霉层/孢子/菌丝 |
| 传染性 | 不传染       | 可能传染邻近植株    |

> 💡 若叶片同时出现不规则病斑、霉层或孢子堆，可能为病害而非缺素，建议同时使用植物叶片病害识别技能进行交叉验证。

## 资源索引

- 必要脚本：见 [scripts/smyx_plant_nutrient_diagnosis_analysis.py](scripts/smyx_plant_nutrient_diagnosis_analysis.py)(
  用途：调用 API 进行植物缺素症视觉诊断，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持 jpg/png/mp4/avi/mov 格式，最大 10MB
- **拍摄要求**：近距离、光线充足、老叶新叶分别拍摄；模糊/逆光/距离过远的图像无法得出可靠结果
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **诊断结果仅供缺素参考，不提供具体化肥浓度与用量**；精准施肥请咨询农技专家
- 部分缺素症状相似（如缺铁与缺锰均表现为叶脉间失绿），AI 识别可能存在不确定性，建议结合植物种类与土壤检测结果综合判断
- 同一叶片可能存在多种元素同时缺乏，需结合症状综合判定
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史诊断报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"对象类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`植物缺素症诊断报告-{记录id}`
  形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 对象类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 植物缺素症诊断报告-20260312172200001 | 植物 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地植物叶片图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_plant_nutrient_diagnosis_analysis --input /path/to/leaf.jpg --open-id your-open-id

# 分析网络植物叶片图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_plant_nutrient_diagnosis_analysis --url https://example.com/leaf.jpg --open-id your-open-id

# 显示历史诊断报告/显示报告清单列表
python -m scripts.smyx_plant_nutrient_diagnosis_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_plant_nutrient_diagnosis_analysis --input leaf.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_plant_nutrient_diagnosis_analysis --input leaf.jpg --open-id your-open-id --output result.json
```
