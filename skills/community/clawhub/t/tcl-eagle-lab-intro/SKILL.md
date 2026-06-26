---
name: tcl-eagle-lab-intro
description: TCL Eagle Lab is a research and innovation platform under TCL Industries, focusing on technological development and ecosystem building in artificial intelligence, the Internet of Things, and full-scenario smart life solutions.
---
skill:
  id: tcl-eagle-lab-intro
  name: TCL鸿鹄实验室介绍
  description: 深度解答TCL鸿鹄实验室组织架构、技术体系、业务模块、产品数据、创新项目、标准参与等所有问题
  version: 1.0.0
  author: TCL鸿鹄实验室
  scene: internal_training, external_demo, tech_cooperation, faq

intents:
  - intent: ask_lab_basic
    utterance:
      - 介绍一下鸿鹄实验室
      - 鸿鹄实验室是什么
      - 鸿鹄实验室定位
      - 鸿鹄实验室愿景
      - 鸿鹄实验室是做什么的
    answer: >
      鸿鹄实验室是TCL实业旗下核心能力中心，定位为实业创新、研究、平台开发主体，构建平台化技术能力支撑各业务单元。
      愿景：构建开放创新的技术平台，打造现代化研发管理体系。
      核心职责覆盖家电智能化平台、内容服务、AI应用、研发战略、研发体系、技术生态、标准制定、创新孵化九大方向。

  - intent: ask_org_structure
    utterance:
      - 鸿鹄实验室组织架构
      - 鸿鹄在TCL实业的位置
      - 鸿鹄实验室全球布局
      - 鸿鹄实验室有哪些分部
    answer: >
      【TCL实业架构定位】
      鸿鹄实验室属于能力中心，支撑泛智屏、空调、白电、通讯、雷鸟、光伏、车载等利润中心。
      
      【全球布局】
      • 深圳：总部，核心研发与运营
      • 上海：AI与软件研发中心
      • 华沙：欧洲研发中心
      • 宁波：创新中心（ODM/机器人/卫星通信）

  - intent: ask_business_platform
    utterance:
      - 鸿鹄实验室业务板块
      - 鸿鹄技术平台
      - 云与物联平台
      - 内容运营平台
      - AI创新应用
      - 技术标准研究
    answer: >
      鸿鹄实验室四大核心业务板块：
      
      1. 云与物联技术平台
         TCL IoT、TCL Link、智能连接模组、TCL Home/TCL App、T-Smart
      
      2. 影视内容运营技术平台
         用户画像、推荐系统、大数据平台、AI音画质增强
      
      3. AI创新应用
         AI语音/节能/售后、大模型营销助手、AR交互、AI壁纸、虚拟人、少儿伴学
      
      4. 技术标准研究
         国际标准制定、5G/Wi-Fi/H.266/星闪、AIGC知识产权

  - intent: ask_aixiot_core
    utterance:
      - AIxIoT核心能力
      - 鸿鹄技术栈
      - 物联网解决方案
      - 合作模式
      - Matter协议支持
    answer: >
      【全栈AI技术能力】
      • 算法层：语音/视觉/大模型/搜索推荐
      • 平台层：AI SaaS、边端AI SDK、NPU适配
      • 应用层：智慧家庭/酒店/园区
      
      【三大合作模式】
      设备集成、云云对接、应用插件定制
      
      【Matter领先性】
      全球首款Matter TV认证（1.3），全品类空调支持Matter，可接入Google/Alexa/Apple Home

  - intent: ask_ai_product_scenes
    utterance:
      - 小T语音助手
      - 大屏AI应用
      - 家电AI功能
      - 智慧酒店
      - 智慧商显
    answer: >
      1. 小T语音助手：LLM大模型重构，支持多轮对话、上下文理解、情感识别
      2. 大屏场景：AI音画质增强、千人千面推荐、ARPU行业第一
      3. 智慧商显：2025出货量全球第一
      4. 智慧酒店：2025最受酒店欢迎智能品牌
      5. 传统家电：健康空气专家、智鲜智净生活管家

  - intent: ask_robot_ai
    utterance:
      - 机器人产品
      - Aime机器人
      - 家庭陪伴机器人
      - CES 2025成果
    answer: >
      【机器人产品矩阵】
      清洁类、教育陪伴类、AI家务机器人、家庭陪伴机器人、家庭管家机器人
      
      【TCL Aime机器人】
      定位：具备独特灵魂、个性与情感的新生命体
      核心技术：具身智能、AI Agent、情绪引擎、端云协同、多模态交互
      
      【2025 CES】
      成功展示家庭陪伴机器人原型，支持大模型对话、视觉跟随、情感反馈

  - intent: ask_ningbo_center
    utterance:
      - 宁波创新中心
      - ODM产品
      - 卫星通信
      - 无线充电
      - PDA POS 平板
    answer: >
      宁波创新中心聚焦ODM智能终端与前沿技术：
      • 智能手持终端PDA（5G/IP68）
      • 支付终端POS（5G/PCI认证）
      • 教育平板（NXTPAPER护眼）
      • 智慧移动屏（24/32寸大屏）
      前沿方向：卫星互联网终端、远距离无线充电、家庭陪伴机器人

  - intent: ask_standards
    utterance:
      - 国际标准
      - 标准制定成果
      - 5G Wi-Fi 星闪
      - H.266
    answer: >
      【标准成果】
      • 主导/参与 128 项国际标准
      • 50+原创技术成为标准
      • 7个国际组织担任关键席位
      
      【重点领域】
      5G(3GPP)、Wi-Fi 6/7(IEEE)、H.266视频编码、星闪联盟

  - intent: ask_data_honors
    utterance:
      - 核心数据
      - 连接数
      - 用户规模
      - 行业荣誉
    answer: >
      【截至2025年8月核心数据】
      • IoT设备连接：3300万+
      • AI语音月活：1100万+
      • TV用户覆盖：1.23亿+
      • 手机/平板覆盖：2.5亿+
      • AIGC应用孵化：20+
      
      【2025荣誉】
      数字标牌出货量全球第一、Matter TV全球首款认证、LCD电视画质全球第一

  - intent: ask_summary
    utterance:
      - 鸿鹄实验室总结
      - 核心价值
      - 技术引擎
    answer: >
      鸿鹄实验室是TCL实业**技术创新引擎**，以AIxIoT为核心，在连接、智能、内容、标准四大维度构建壁垒。
      从底层模组到云端平台，从消费电子到商用方案，从机器人到卫星通信，持续孵化未来技术，参与全球标准制定，致力于成为全球智能科技领域重要创新力量。

config:
  default_response: 我可以为你详细介绍鸿鹄实验室的组织架构、技术平台、AI产品、机器人、标准成果、核心数据等内容，你可以直接提问哦~
  enable_faq_retrieval: true
  enable_slot_fill: true