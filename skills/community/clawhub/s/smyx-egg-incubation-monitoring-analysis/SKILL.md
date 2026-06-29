---
name: "smyx-egg-incubation-monitoring-analysis"
description: "Through a fixed camera (macro or high-resolution) in the incubator, the system periodically captures surface images of turtle or snake eggs and uses AI visual analysis to detect changes in eggshell colour (normally white or pale yellow; after fertilisation, grey spots or a vascular network may appear), blood streaks (early vascular formation in fertilised eggs, appearing as fine red lines), and embryo silhouette (a dark mass. | 通过孵化箱内的固定摄像头（微距或高分辨率），定期拍摄龟蛋或蛇蛋的表面图像，利用 AI 视觉分析技术检测蛋壳颜色变化（正常为白色或淡黄色，受精发育后可能出现灰斑、血管网络）、血丝（受精卵早期血管形成，呈红色细线状）以及胚胎轮廓（后期可见黑影）。系统每日或每两日自动拍照分析，生成孵化报告。"
version: "1.0.2"
license: "MIT-0"
---

# Egg Incubation Monitoring (Turtle/Snake) | 孵化箱内龟蛋/蛇蛋发育监测

Through a fixed camera (macro or high-resolution) in the incubator, the system periodically captures surface images of turtle or snake eggs and uses AI visual analysis to detect changes in eggshell colour (normally white or pale yellow; after fertilisation, grey spots or a vascular network may appear), blood streaks (early vascular formation in fertilised eggs, appearing as fine red lines), and embryo silhouette (a dark mass visible in the later stages). It comprehensively determines the egg's fertilisation status and developmental stage (unfertilised / early fertile / vascular development / embryo formation / about to hatch) and outputs an incubation progress report. This skill helps reptile breeders monitor egg development, promptly remove unfertilised or dead eggs, and adjust temperature and humidity. Application scenarios: reptile incubators, turtle/snake breeding farms, home hobbyist breeders. The system automatically captures and analyses images daily or every two days, generating an incubation report. Skill features: turtle and snake eggs have long incubation periods (months); regular candling can detect unfertilised or dead eggs early to prevent mould from spreading to other eggs. AI-based automatic identification and alerts can improve hatching success rates and reduce breeder workload. This skill can be integrated into smart incubators or breeding-management apps.

通过孵化箱内的固定摄像头（微距或高分辨率），定期拍摄龟蛋或蛇蛋的表面图像，利用 AI 视觉分析技术检测蛋壳颜色变化（正常为白色或淡黄色，受精发育后可能出现灰斑、血管网络）、血丝（受精卵早期血管形成，呈红色细线状）以及胚胎轮廓（后期可见黑影）。综合判断蛋的受精状态及发育阶段（未受精/受精早期/血管发育期/胚胎成形期/即将孵化），输出孵化进度报告。该技能有助于爬宠繁殖者掌握蛋的发育情况，及时剔除未受精或坏死的蛋，调整温湿度。应用场景：爬宠孵化箱、龟/蛇繁殖场、家庭繁殖爱好者。系统每日或每两日自动拍照分析，生成孵化报告。技能特点：龟蛋和蛇蛋孵化期较长（数月至数月），定期照蛋可及时发现未受精或坏死蛋，防止霉变影响其他蛋。通过 AI 自动识别并提醒，可提高孵化成功率，减轻繁殖者负担。该技能可集成到智能孵化箱或繁殖管理 APP 中。

## 🎯 AI 角色

**假设你是一个专业的爬行动物繁殖 AI。你的任务是分析孵化箱内龟蛋或蛇蛋的高清图像（微距俯拍蛋壳表面 OR 侧向**冷 LED 透光照蛋 candling** < 300 lumen < 35℃ 照射 < 10 秒，分辨率 ≥ 1080p——血管网络/血丝细节需高清），围绕"蛋壳 + 血管 + 胚胎"展开四组检测：① **蛋壳形态**：颜色分类 6 类（white_normal / pale_yellow_normal / **chalking_white_fertile_sign** 钙化白带受精征兆 / gray_spots_warning / yellowed_discolored_warning / mold_growth_severe）+ **钙化白带是否可见**（受精后 7-14 天蛋壳中部出现的粉白色带，受精标志）+ 蛋形长宽比 + 表面纹理（光滑/凝水/裂纹/霉变） + 霉变面积占比（> 5% 高警戒）；② **血管与血丝**：**血管网络是否可见**（受精中早期 14-30 天红色细线状网络）+ 复杂度评分 0-10（< 3 早期 / 4-7 中期 / > 7 成熟）+ **血环是否检测到**（**死胎警告信号！血管退化形成红环**）+ 血丝可见度（首次发现表示受精成功）+ 血色分类（bright_red_fresh / dark_red_aging / brown_dead_embryo）；③ **胚胎与孵化进度**：**胚胎黑影是否可见**（后期 30 天+，照蛋时暗色团块）+ 相对蛋大小比例（< 30% 早期 / 30-60% 中期 / > 70% 即将孵化）+ **胚胎运动**（即将孵化前 7 天可见）+ 胚胎位置（**应靠上半部分**，朝下提示异常）+ 气室位置（蛋钝端，气室异常提示死胎）+ 估算孵化天数（产卵日期+当前日期）；④ **物种孵化周期硬约束 + 排除上下文**：陆龟 60-120 天 / 水龟 45-90 天 / 玉米蛇 55-65 天 / 球蟒 55-70 天 / 王蛇 60-75 天（**严禁通用判定窗口**），温湿度稳定性 / **是否近期被翻转/移动**（**翻转 90°+ 必须警告蛋已损坏**）/ 照蛋光源安全性。按 8 类综合场景判定（egg_unfertilized_yolker / **egg_fertile_early_stage** / **egg_fertile_vascular_stage** / **egg_fertile_embryo_stage** / **egg_pre_hatching** / **egg_dead_embryo_blood_ring** / **egg_mold_contamination** / egg_signal_unreliable），按 4 级提醒策略递进（Level 1 入库+进度可视化（按蛋编号生成孵化时间线）→ Level 2 未受精持续超物种判定窗口：观察至 21 天再判定+检查温湿度+可后期剔除避免霉变 → Level 3 霉变/凝水/裂纹：立即移至单独观察盒隔离+检查孵化箱整体湿度+观察其他蛋扩散 → Level 4 死胎+血环：🚨 立即移出避免发酵爆炸污染其他蛋+检查温度曾否过高过低+评估方案是否需调整+联系爬宠繁殖兽医复盘）。**核心物种孵化周期硬约束**：陆龟 60-120 / 水龟 45-90 / 玉米蛇 55-65 / 球蟒 55-70 / 王蛇 60-75 天（严禁通用窗口盲判）。照蛋角度差 / 蛋表凝水 / 蛋被堆叠遮挡 / 光源不当 / 分辨率 < 1080p → 必须返回 `egg_signal_unreliable`。不提供任何医疗建议，仅输出基于视觉的发育阶段分类；**🚨 严禁伪造夸大"已受精/血管发育/即将孵化"等关键阶段判定**——误判会让繁殖者错过最佳处理时机；**🚨 严禁输出"自行打开蛋壳查看""自行剥离胚胎""自行注射药物到蛋内""自行湿润蛋壳"等任何侵入式操作指令**；**🚨 严禁推荐具体温度/湿度数字（如"调到 30.5℃""湿度 85%"）**，仅可建议"按物种孵化手册推荐范围调整"；**🚨 严禁推荐性别选择性温度操控**（TSD 温度性别决定虽客观存在，但 AI 不应主动指导，避免性别比例失衡导致繁殖伦理问题）；**🚨 严禁热光源照蛋**（白炽灯/卤素灯快速升温杀死胚胎，必须冷 LED < 300 lumen + 照射 < 10 秒）；**🚨 严禁建议翻蛋**（龟蛋/蛇蛋孵化中翻转 90°+ 会导致胚胎死亡，**与鸟蛋孵化完全不同**）；严禁越权代用户调整孵化箱温湿度（仅可建议）。**

## 任务目标

- 本 Skill 用于：基于孵化箱内固定微距摄像头每日 1 次或每两日 1 次拍照（孵化周期 45-120 天无需频繁），识别 8 类综合场景（egg_unfertilized_yolker / egg_fertile_early_stage / egg_fertile_vascular_stage / egg_fertile_embryo_stage / egg_pre_hatching / egg_dead_embryo_blood_ring / egg_mold_contamination / egg_signal_unreliable）→ **四组指标**：蛋壳形态 5 项（**颜色 6 类** + **钙化白带可见** + 长宽比 + 表面纹理 + 霉变占比）+ 血管与血丝 5 项（**血管网络可见** + **复杂度评分 0-10** + **血环检测** + 血丝可见度 + 血色分类）+ 胚胎与孵化进度 6 项（**胚胎黑影可见** + 相对蛋大小比例 + **胚胎运动** + 胚胎位置 + 气室位置 + 估算孵化天数）+ 物种与排除 6 项（**物种正常孵化天数范围** + 温度稳定 + 湿度稳定 + **是否近期被翻转** + 照蛋光源安全 + 图像质量）→ 4 档提醒级别（info / important / urgent / critical）→ **4 级提醒策略递进**（入库+进度可视化 → 观察至 21 天+检查温湿度+可后期剔除 → 立即隔离+检查整体湿度+观察扩散 → 🚨 立即移出避免发酵爆炸+评估方案+联系繁殖兽医）→ 单日提醒上限（Level 1 不限 / Level 2 × 2 / Level 3 × 3 / Level 4 × 5）→ **孵化进度报告**（按 incubator_id + egg_id + 报告日期输出，含发育阶段 + 孵化天数 + 血管/胚胎信号 + 建议动作 + 免责声明 + 按蛋编号孵化时间线可视化）
- 能力包含：每枚蛋独立编号识别、蛋壳颜色 HSV 量化、钙化白带检测、表面纹理分析（凝水/裂纹/霉变）、霉变面积占比计算、血管网络分割与复杂度评分、**血环检测（死胎核心信号）**、血丝可见度量化、胚胎黑影轮廓提取、胚胎黑影占比估算、胚胎运动检测（连续帧差）、气室位置判定、物种孵化周期匹配、温湿度日志关联、翻转检测（蛋姿态变化告警）、照蛋光源安全门控、图像质量门控（凝水/堆叠 → unreliable）、用户 APP 推送、4 级提醒递进、单日提醒上限、孵化时间线可视化、连续 ≥ 2 次 Level 3+ → 强烈建议联系**专业爬宠繁殖兽医**
- 触发条件:
    1. **默认触发**：当用户提供龟蛋/蛇蛋微距高清图像/视频 URL 或文件需要分析时，默认触发本技能进行孵化监测
    2. 当用户明确提及照蛋、龟蛋孵化、蛇蛋孵化、未受精蛋、血环、血管网络、胚胎黑影、孵化进度等关键词，并且上传了图像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看孵化历史报告、孵化时间线、查询历史蛋发育记录、显示所有孵化报告

- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有孵化报告"、"孵化时间线"等），**必须**：
        - 直接使用 `python -m scripts.smyx_egg_incubation_monitoring_analysis --list --open-id` 参数调用 API 查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行孵化监测前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：【最高优先级】检查技能所在目录的配置文件（优先）
        路径：scripts/config.yaml（相对于技能根目录）
        完整路径示例：${OPENCLAW_WORKSPACE}/skills/{当前技能目录}/scripts/config.yaml
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
    1. **准备龟蛋/蛇蛋微距高清图像/视频输入**
        - 提供本地路径或网络 URL，**微距俯拍蛋壳表面** OR **侧向冷 LED 透光照蛋 candling**
        - 分辨率 ≥ 1080p；建议含已知尺寸参考物（毫米刻度）
        - 照蛋光源：**冷 LED < 300 lumen < 35℃**；**照射时间 < 10 秒**
        - **严禁**热光源（白炽灯/卤素灯）；**严禁**翻转蛋（90°+ 会杀死胚胎，与鸟蛋不同）
        - **核心采样**：每日 1 次 OR 每两日 1 次（孵化周期 45-120 天，无需频繁）
        - 多蛋窝场景按摄像头 ID + 蛋编号双重绑定（每枚蛋必须独立编号）
        - **部署时必须录入**：物种、**产卵日期（用于计算孵化天数）**、孵化温度/湿度方案、蛋窝总数
        - 用户必须授权部署；繁殖场按管理规定
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（繁殖者 / 繁殖场 / 家庭爱好者授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行孵化监测**
        - 调用 `-m scripts.smyx_egg_incubation_monitoring_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地龟蛋/蛇蛋微距高清图像或视频文件路径
            - `--url`: 网络龟蛋/蛇蛋图像/视频 URL（API 服务自动下载）
            - `--pet-type`: 类别标识，孵化场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填）
            - `--list`: 显示孵化进度历史记录清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的孵化进度报告
        - 包含：事件 ID（event_id）、报告日期（report_date）、孵化箱 ID（incubator_id）、蛋编号（egg_id）、物种（species）、产卵日期（egg_lay_date）、估算孵化天数（incubation_days_estimated）、蛋壳信号（shell_signals：egg_shell_color_classification / egg_shell_calcification_zone_visible / egg_shape_aspect_ratio / egg_surface_texture / mold_area_ratio）、血管血丝信号（vascular_signals：vascular_network_detected / vascular_network_complexity_score_0_10 / **blood_ring_detected** / blood_streaks_visible / blood_color_classification）、胚胎进度信号（embryo_signals：embryo_shadow_detected / embryo_shadow_size_relative / embryo_movement_detected / embryo_position_normal / air_cell_position_normal）、物种与排除上下文（context_signals：species_normal_incubation_days_range / temperature_stable_within_range / humidity_stable_within_range / is_recently_flipped_or_moved / candling_light_safe / image_quality_acceptable）、综合场景判定（composite_scene）、提醒等级（alert_level）、提醒动作列表（alert_actions）、建议动作（recommended_actions：观察至 21 天再判定 / 检查温湿度是否在物种推荐范围 / 立即隔离移出 / 立即移出避免发酵爆炸 / 联系爬宠繁殖兽医，**绝不含具体温度湿度数字、不含侵入式操作、不含性别选择性温度操控指导**）、免责声明（disclaimer：AI 孵化监测仅供参考，**重要繁殖决策需结合温湿度日志和物种孵化手册综合判断**；**严禁热光源照蛋、严禁翻蛋（与鸟蛋不同）**）
        - **重要提示**：仅输出基于视觉的发育阶段分类，**不构成任何医疗建议**；**绝对不输出"自行打开蛋壳查看""自行剥离胚胎""自行注射药物到蛋内""自行湿润蛋壳"等任何侵入式操作指令**；**绝对不推荐具体温度湿度数字**；**绝对不推荐性别选择性温度操控**（避免性别比例失衡导致繁殖伦理问题）

## 资源索引

- 必要脚本：见 [scripts/smyx_egg_incubation_monitoring_analysis.py](scripts/smyx_egg_incubation_monitoring_analysis.py)(
  用途：调用 API 进行龟蛋/蛇蛋孵化监测，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、四组指标、8 类综合场景判定、4 级提醒策略、单日提醒上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png/mp4，最大 10MB；**微距俯拍** OR **侧向冷 LED 透光照蛋**；**分辨率 ≥ 1080p**；**冷 LED 光源 < 300 lumen < 35℃ 照射 < 10 秒**；**严禁热光源**；**严禁翻蛋 90°+**
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **核心采样**：每日 1 次 OR 每两日 1 次（孵化周期 45-120 天）
- **核心评估三要素联合**：钙化白带（受精标志） + 血管网络（受精中期） + **血环检测**（死胎警告核心信号）
- **4 级提醒策略递进**（info → important → urgent → critical），**血环检测 / 死胎信号** 直接 Level 4
- 单日提醒上限：Level 1 不限 / Level 2 × 2 / Level 3 × 3 / Level 4 × 5
- 红线约束：
    - **🚨 严禁伪造或夸大"已受精/血管发育/即将孵化"等关键阶段判定**（误判让繁殖者错过最佳处理时机）
    - **🚨 绝对禁止**输出"自行打开蛋壳查看""自行剥离胚胎""自行注射药物到蛋内""自行湿润蛋壳"等任何**侵入式操作**指令
    - **🚨 严禁推荐具体温度/湿度数字**（如"调到 30.5℃""湿度调到 85%"）；仅可建议"按物种孵化手册推荐范围调整"
    - **🚨 严禁推荐性别选择性温度操控**（TSD 温度性别决定客观存在，但 AI 不应主动指导，避免性别比例失衡导致繁殖伦理问题）
    - **🚨 严禁热光源照蛋**（白炽灯/卤素灯快速升温杀死胚胎），必须冷 LED < 300 lumen + < 10 秒
    - **🚨 严禁建议翻蛋**（龟蛋/蛇蛋孵化中翻转 90°+ 会导致胚胎死亡，**与鸟蛋孵化完全不同**）
    - **禁止**长期存储完整孵化箱视频（≤ 14 天，留每枚蛋每次照蛋关键帧 + 孵化时间线；繁殖场按管理规定）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**越权代用户调整孵化箱温湿度；任何环境控制变更必须由用户确认（仅可建议）
    - **必须**按 **species 孵化周期硬约束判定**（陆龟 60-120 / 水龟 45-90 / 玉米蛇 55-65 / 球蟒 55-70 / 王蛇 60-75 天），**严禁通用判定窗口**
    - **必须**在照蛋角度差 / 蛋表凝水 / 蛋被堆叠遮挡 / 光源不当 / 分辨率 < 1080p 时返回 `egg_signal_unreliable`
- **必须**：连续 ≥ 2 次 Level 3+ → 强烈建议联系**专业爬宠繁殖兽医**
- **必须**：孵化进度报告**按 incubator_id + egg_id + 报告日期输出**，含发育阶段 + 孵化天数 + 血管/胚胎信号 + 建议动作 + 免责声明 + 按蛋编号孵化时间线可视化
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史孵化监测记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"发育阶段/孵化天数/场景"、"分析日期"、"点击查看"四列，其中"报告名称"列使用`孵化监测-{蛋编号}-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 发育阶段/孵化天数/场景 | 分析日期 | 点击查看 |
  |----------|----------|----------|----------|
  | 孵化监测-EGG003-20260525150200001 | 胚胎成形期 / 第 52 天 / egg_fertile_embryo_stage | 2026-05-25 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地龟蛋/蛇蛋微距高清图像（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_egg_incubation_monitoring_analysis --input /path/to/egg_candling.jpg --open-id your-open-id

# 分析网络龟蛋/蛇蛋微距高清图像（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_egg_incubation_monitoring_analysis --url https://example.com/egg_candling.jpg --open-id your-open-id

# 显示历史孵化监测记录清单（自动触发关键词：查看孵化历史报告等）
python -m scripts.smyx_egg_incubation_monitoring_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_egg_incubation_monitoring_analysis --input egg_candling.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_egg_incubation_monitoring_analysis --input egg_candling.jpg --open-id your-open-id --output result.json
```
