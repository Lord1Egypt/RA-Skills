# 🎓 营中智教助手 Yingzhong Smart Teaching Assistant

[![版本 Version](https://img.shields.io/badge/version-5.0.0-blue)](https://github.com/SimonsTang/yingzhong-smart-teacher)
[![平台 Platform](https://img.shields.io/badge/platform-OpenClaw-green)](https://github.com/SimonsTang/yingzhong-smart-teacher)
[![语言 Lang](https://img.shields.io/badge/lang-Chinese-red)](https://github.com/SimonsTang/yingzhong-smart-teacher)

---

## 📖 简介 Introduction

**营中智教助手** 是专为中小学教师打造的一站式AI智教助手。

基于飞飞学伴v4.0升级，集成清华MAIC虚拟教室、ChinaTextbook教材库、OCR批改、微信家校通，是营山中学×学来学去学习社联合出品的教师必备工具。

---

## ✨ 核心功能 Features

### 🎯 六大核心模块

| 模块 | 说明 | 优先级 |
|------|------|--------|
| 教学工作台 | 课程规划、进度管理、备课助手 | P0 |
| 出题组卷助手 | 智能出题、自动组卷、题库管理 | P0 |
| 学情分析系统 | 成绩分析、薄弱点识别、分层教学 | P0 |
| 作业批改助手 | OCR拍照批改、AI批注、错题归纳 | P0 |
| 家校沟通助手 | 微信通知、家长话术、家长会助手 | P0 |
| 班级管理助手 | 班级日志、学生档案、评优评先 | P1 |

### 🌟 三大特色能力

| 能力 | 说明 |
|------|------|
| 🌐 清华MAIC虚拟教室 | 一键打开open.maic.chat，自动生成课件 |
| 📚 ChinaTextbook教材库 | 70,778+Star最大中文教材库，本地索引 |
| 🔍 互联网教案搜索 | 多引擎搜索优质教案，自动整理 |

### 🔧 技术架构

- **平台**: OpenClaw Agent
- **OCR**: Tesseract.js（本地免费）
- **文档**: docx/xlsx生成
- **搜索**: multi-search-engine
- **AI**: 飞飞学伴v4.0全功能继承

---

## 🚀 安装 Installation

### 方式一：SkillHub安装（推荐）

```bash
skillhub install yingzhong-smart-teacher
```

### 方式二：GitHub直接下载

```bash
# 克隆仓库
git clone https://github.com/SimonsTang/yingzhong-smart-teacher.git

# 或下载最新Release的zip文件
```

---

## 📋 使用指南 Quick Start

### 首次使用

```markdown
我是XX老师，任教高中数学，需要绑定教材
```

系统将引导您完成：
1. 身份确认（学科/年级/班级）
2. 教材绑定（人教版/北师大版等）
3. 智能体初始化

### 常用命令

| 功能 | 触发关键词 |
|------|-----------|
| 清华MAIC | "打开清华MAIC"、"虚拟教室" |
| 教材搜索 | "查教材"、"下载教材" |
| 教案搜索 | "搜索教案"、"找课件" |
| 备课 | "帮我备课"、"生成教案" |
| 出题 | "出一道XX题"、"组卷" |
| 批改 | "批改作业"、"上传照片" |
| 学情 | "分析成绩"、"知识点掌握" |
| 家校 | "发通知"、"家长会" |

---

## 📄 版本历史 Changelog

### v5.0.0 (2026-05-15)
- 全新创建
- 集成清华MAIC虚拟教室
- 集成ChinaTextbook教材库
- 集成OCR本地批改
- 集成微信家校通
- 继承飞飞学伴v4.0全功能

---

## 🤝 合作方 Partners

- **营山中学** - 百年名校，联合出品
- **学来学去学习社** - AI教育团队
- **巧未来AI** - 技术支持

---

## 📧 联系我们 Contact

- **学来学去学习社**: learn2study@163.com
- **GitHub Issues**: https://github.com/SimonsTang/yingzhong-smart-teacher/issues

---

## 📄 许可证 License

MIT License - 开源免费使用

---

**让老师从重复性工作中解放出来，专注于真正的教学和学生成长** 🎓
