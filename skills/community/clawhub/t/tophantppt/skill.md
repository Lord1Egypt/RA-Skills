name: tophantppt
slug: tophantppt
version: 1.0.4
homepage: https://clawic.com/skills/tophantppt
description: "支持两种输入方式：1）用户指定每页内容，2）用户提供原始材料自动提炼框架；两种方式均使用指定的背景图片作为视觉参考图，必须使用给的参考图，如果图片获取有问题则重试直至成功获取参考图，当参考图获取有问题时，可都获取默认页地址的图片，不可以跳过使用其他方式。调用生图工具（如codex的image2）直接生成每页幻灯片图片，并合并为全图片型PPTX。最终PPT所有内容均为图片，不可编辑。"
changelog: |
  v1.0.4 统一为全图片生成模式，移除文字可编辑要求；两种模式均使用背景图片作为参考图驱动生图。
  v1.0.2 修正模式说明。
  v1.0.1 新增模式B。
  v1.0.0 初始版本。
metadata:
  clawdbot:
    emoji: "🎨"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]

background_reference_images:
  description: |
    以下URL为各版式的背景参考图片。在生成每页幻灯片时，必须将这些图片作为视觉参考（图生图），用于确定整体配色、构图比例、氛围和版式风格。生图工具应以此为基础，生成风格一致的幻灯片图片。
  list:
    - type: 封面页
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/cover_bg.png
      usage: 标题、副标题、演讲者信息
    - type: 目录页
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/toc_bg.png
      usage: 章节导航、议程概览
    - type: 章节过渡页
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/chapter_bg.png
      usage: 大章节分隔、转场页
    - type: 内容页-纯文字
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/content_text_bg.png
      usage: 正文、段落、说明文字
    - type: 内容页-左文右图
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/content_split_bg.png
      usage: 图文混排、左右分栏
    - type: 内容页-上文下图表
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/content_chart_bg.png
      usage: 图表上方、文字总结下方
    - type: 数据可视化页
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/data_bg.png
      usage: 图表、图形、数据展示
    - type: 表格页
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/table_bg.png
      usage: 结构化数据、对比表
    - type: 时间轴页
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/timeline_bg.png
      usage: 流程、历史、里程碑
    - type: 团队/成员页
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/team_bg.png
      usage: 人物介绍、组织架构
    - type: 对比页
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/compare_bg.png
      usage: 左右/多项对比
    - type: 引用页
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/quote_bg.png
      usage: 金句、名人名言、观点强调
    - type: 列表页
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/list_bg.png
      usage: 要点、bullet points
    - type: 结尾/感谢页
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/closing_bg.png
      usage: 致谢、Q&A、联系方式
    - type: 默认页
      url: https://github.com/lizhedm/tophantppt/blob/main/assets/moren.png
      usage: 当其他类型找不到对应背景时使用

mode_selection:
  description: |
    在开始操作前，先判断用户输入：
    - 若用户明确说明“共有X页”、“第一页是……”、“第二页……”等具体结构 → 使用模式A（指定式）。
    - 若用户只提供文字段落、文章链接或原始材料，未提及页数或每页内容 → 使用模式B（自动生成式）。
    无论哪种模式，最终都生成全图片型PPT（所有内容均为图片，不可编辑）。

modes:
  A:
    name: 指定式（全图片）
    when_to_use: 用户明确给出每页的标题、要点、图表等详细内容。
    core_requirements:
      - 根据用户指定的每页内容，从 background_reference_images 中选择最匹配的版式参考图。
      - 为每页撰写详细的图片生成描述（包括布局、文字内容、字体大小、颜色、图形元素位置等），该描述将作为生图工具（image2）的提示词。
      - 调用生图工具，以对应的参考图作为视觉基底（图生图），生成每页幻灯片图片。
      - 最终将所有图片合并为 .pptx 文件，每页图片铺满幻灯片。
    workflow_steps:
      - step: 1
        action: 解析用户指定的每页内容，明确标题、正文要点、图表、图片等元素。
      - step: 2
        action: 为每一页匹配最合适的版式参考图（根据内容类型）。
      - step: 3
        action: 撰写详细的图片生成描述（可使用 Markdown 格式），包含背景风格、文字内容及样式、图形布局等，确保描述充分体现参考图的配色和构图逻辑。
      - step: 4
        action: 调用生图工具（推荐 image2），以参考图作为参考输入，将描述作为提示词，生成高清图片（分辨率 ≥ 1920×1080，16:9），命名 slide_XX.png。
      - step: 5
        action: 检查生成的图片内容是否准确、文字清晰、布局合理；如有问题，修改描述并重新生成。
      - step: 6
        action: 使用 python-pptx 等工具新建空白演示文稿（16:9），按顺序插入生成的图片，每张图片铺满整个幻灯片区域，保存为 .pptx。
    output_type: 全图片 .pptx（文字不可编辑）

  B:
    name: 自动生成式（全图片）
    when_to_use: 用户仅提供一段或若干段文字材料，未指定页数或具体每页内容。
    core_requirements:
      - 将材料提炼为逻辑清晰的演示文稿框架（不超过40页）。
      - 每页需选择对应的参考图，并生成详细的图片描述，调用生图工具生成图片。
      - 最终合并为全图片PPT。
    workflow_steps:
      - step: 1
        action: 内容提炼与框架构建 – 提取核心观点，按逻辑顺序组织成每页，明确版式类型、参考图、标题、要点、图表等。
      - step: 2
        action: 生成图片绘制描述文件 – 输出一个 Markdown 文件（如 ppt_design.md），为每一页提供详细的图片生成描述（参考图、文字内容、样式、图形等）。
      - step: 3
        action: 逐页生成图片 – 对每一页，将对应的参考图和描述输入生图工具，生成高清图片，命名 slide_XX.png。
      - step: 4
        action: 合并为PPT – 使用 python-pptx 等工具创建演示文稿，每张幻灯片插入对应图片并铺满，保存为 .pptx。
      - step: 5
        action: 质量保证 – 检查总页数≤40，图片清晰度、布局正确性、参考图风格一致性。
    output_type: 全图片 .pptx（文字不可编辑）

core_rules:
  - id: rule1
    title: 清点输入与目标
    content: 确认用户提供的是指定内容还是原始材料，选择对应模式。
  - id: rule2
    title: 版式与数量约束
    content: 最终PPT页数不超过40页（模式B强制）。每页必须选择对应的参考图，并依据 slide_type_guidelines 设计布局。
  - id: rule3
    title: 视觉一致性
    content: 所有生成的幻灯片图片必须保持与所选参考图一致的配色、字体风格和整体氛围，确保整份PPT视觉统一。
  - id: rule4
    title: 内容与布局匹配
    content: 避免单页文字过多，图表、表格等复杂元素应合理布局。生图描述必须明确文字内容、字号、颜色、对齐方式及图形元素的位置。
  - id: rule5
    title: 生图质量与可移植性
    content: 生成图片分辨率至少 1920×1080，确保清晰。所有图片直接嵌入PPT，不依赖外部链接。输出 .pptx 兼容主流办公软件。

slide_type_guidelines:
  - type: 默认页 (moren)
    reference_image: moren.png
    description: 当其他类型不匹配时使用，保持简洁，避免信息过载。
  - type: 封面页 (Cover)
    reference_image: cover_bg.png
    description: 标题、副标题、演讲者/日期信息居中或按参考图构图放置，标题字号最大。
  - type: 目录页 (Table of Contents)
    reference_image: toc_bg.png
    description: 章节条目使用项目符号或编号，对齐方式参考参考图，避免与装饰元素重叠。
  - type: 章节过渡页 (Chapter Transition)
    reference_image: chapter_bg.png
    description: 仅包含章节编号和标题，极简，居中或按参考图构图对齐。
  - type: 内容页-纯文字 (Content - Text Only)
    reference_image: content_text_bg.png
    description: 正文段落、要点列表放在空白/低纹理区域，保证行距和段落间距。
  - type: 内容页-左文右图 (Content - Split)
    reference_image: content_split_bg.png
    description: 左侧文字右侧图片（或反向），边界清晰，留白适中。
  - type: 内容页-上文下图表 (Content - Chart Below)
    reference_image: content_chart_bg.png
    description: 上方总结性文字，下方图表区域，图表颜色与参考图协调。
  - type: 数据可视化页 (Data Visualization)
    reference_image: data_bg.png
    description: 图表、信息图使用参考图的强调色，数据标签和图例清晰可读。
  - type: 表格页 (Table)
    reference_image: table_bg.png
    description: 表格线条和填充与参考图融合，表头使用强调色。
  - type: 时间轴页 (Timeline)
    reference_image: timeline_bg.png
    description: 时间节点、连接线、说明文字按流向排列，方向依参考图而定。
  - type: 团队/成员页 (Team)
    reference_image: team_bg.png
    description: 成员头像（如需要）和姓名、职位信息布局整齐，头像可圆形裁剪。
  - type: 对比页 (Comparison)
    reference_image: compare_bg.png
    description: 左右或多栏对比，严格对齐，对比项标题突出。
  - type: 引用页 (Quote)
    reference_image: quote_bg.png
    description: 引用文字和出处分开，引号符号可适度调整透明度。
  - type: 列表页 (List)
    reference_image: list_bg.png
    description: 项目符号或编号列表，缩进一致，装饰性符号与参考图协调。
  - type: 结尾/感谢页 (Closing)
    reference_image: closing_bg.png
    description: 感谢语、联系方式、Q&A 提示，保持简洁。

common_traps:
  - trap: 生图描述不够具体，导致生成图片与预期偏差，需细化文字内容、颜色、位置。
  - trap: 参考图风格未被充分遵循，生成图片配色或构图偏离，需加强 prompt 中对参考图的描述。
  - trap: 文字过小或对比不足，在投影或缩小时看不清，应使用大号字体和高对比度。
  - trap: 图片分辨率低于 1920×1080，导致模糊，需设置输出分辨率。
  - trap: 总页数超过40页，内容过于拥挤，需合并或精简。
  - trap: 生图工具无法处理复杂图表，可简化为表格或手绘图示。
  - trap: 未检查每页图片的内容准确性，可能导致数据错误或错别字。
  - trap: 合并PPT时图片未铺满，留有白边，应设置图片填充整个幻灯片。
  - trap: 忽略原始材料重点，框架偏离用户意图，应先与用户确认框架草案（模式B）。
  - trap: 不同页面的参考图风格差异大，导致PPT整体不协调，应尽量选择同一系列或风格相近的参考图。

related_skills:
  - slug: documents
    description: 文档材料预处理
  - slug: design
    description: 视觉方向建议
  - slug: brief
    description: 商业信息提炼
  - slug: powerpoint-pptx
    description: PPTX底层操作

feedback:
  star_command: clawhub star tophantppt
  sync_command: clawhub sync