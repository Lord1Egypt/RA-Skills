# WeChat Mini Program UI/UX Skill

[English](./README.md)

一个面向 Codex 的微信小程序 UI/UX 技能包，用于设计、实现、优化和评审微信小程序界面。

## 简介

这个 skill 结合了以下能力：

- 微信小程序官方设计原则与平台约束
- 借鉴 `ui-ux-pro-max` 的轻量设计系统工作流
- 面向移动端小程序的 anti-pattern 过滤
- 面向生产页面的状态与交付检查清单

## 适用场景

适用于以下工作：

- WXML / WXSS / JS 页面设计与实现
- 页面重构、视觉整理、交互优化
- 菜品详情、列表页、表单页、管理页等典型小程序页面
- 小程序 UI/UX 评审与可用性问题排查
- 小程序项目的页面设计系统约束

它面向微信小程序，不是通用网页 UI 规范。

## 设计约束

这个 skill 会推动产出符合以下方向：

- 页面目标清晰
- 每个主要区域只有一个主操作
- 优先保证移动端层级、阅读节奏和点击舒适度
- 明确处理加载、空态、错误态、权限态
- 固定底部操作栏考虑安全区
- 视觉上更像微信小程序，而不是移植网页落地页

## 目录结构

```text
wechat-miniprogram-ui-ux/
├── README.md
├── README.zh-CN.md
├── SKILL.md
└── references/
    ├── design-system-pattern.md
    └── wechat-design-principles.md
```

## 参考来源

- 微信小程序官方设计指南
  `https://developers.weixin.qq.com/miniprogram/design/`
- `ui-ux-pro-max-skill`
  `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`

## 工作方式

这个 skill 引导 agent 按下面顺序工作：

1. 识别页面类型、用户目标和状态复杂度
2. 读取小程序设计原则与轻量设计系统参考
3. 定义页面意图、信息层级、视觉方向和状态覆盖
4. 使用小程序原生模式在 WXML/WXSS/JS 中实现
5. 交付前按小程序专项清单复核

## 典型输出结构

处理具体页面任务时，skill 会优先围绕以下顺序组织思考：

1. 页面意图
2. 主操作
3. 内容层级
4. 状态覆盖
5. 视觉系统
6. 交互细节

## 使用示例

- 将菜品详情页重构为更符合微信小程序习惯的详情页，并避免加载失败时白屏
- 将冗长表单拆成更适合手机端的分组结构，并补充校验与反馈
- 审查管理页中的权限表达、危险操作区分和状态覆盖
- 为一个小程序项目建立统一但不过度网页化的界面风格

## 说明

- 这个仓库只包含 skill 本身，不包含演示应用
- 该 skill 优先适配 Codex 本地 skills 工作流，但其中的规则也可复用于其他 agent 场景
