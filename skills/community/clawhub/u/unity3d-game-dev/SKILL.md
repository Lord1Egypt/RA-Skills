# Unity3D 游戏开发助手

**Unity3D Game Development Assistant**

一个全面的AI驱动的Unity游戏开发插件，涵盖场景管理、资源优化、代码生成、自动化构建与打包发布全流程。

## 功能特性

### 1. 场景与对象管理
- 场景创建/加载/保存
- GameObject/Component 智能操作
- 层级结构分析与管理
- Prefab 创建与实例化

### 2. 代码生成与辅助
- C# 脚本自动生成（MonoBehaviour、管理器、工具类）
- Shader 代码辅助
- 设计模式模板（Singleton、ObjectPool、Factory等）
- 代码重构与优化建议

### 3. 资源管理与优化
- 纹理/模型/音频资源分析
- 内存使用报告
- 性能热点检测
- AssetBundle 打包配置

### 4. 自动化构建
- 多平台构建配置（Windows/Mac/iOS/Android/WebGL）
- 自动化打包脚本生成
- 版本号管理与增量构建
- CI/CD 集成

### 5. 调试与测试
- Play Mode 自动控制
- 日志分析与错误修复建议
- 单元测试模板生成
- Scene 快照对比

## 定价方案

| 方案 | 价格 | 说明 |
|------|------|------|
| 月付 | **29 USDT/月** | 全功能无限使用 |
| 按次 | **0.035 USDT/次** | 按AI请求计费 |

## 安装要求

- Unity 2021.3 LTS 或更新版本
- Unity Editor 已安装并登录
- （可选）Unity Hub 用于版本管理

## 快速开始

1. 安装此技能
2. 打开Unity项目
3. 使用以下命令操作Unity：

### 示例命令

`unity3d open project:/path/to/project`
打开Unity项目

`unity3d create scene "GameScene"`
创建新场景

`unity3d add-component PlayerController.cs --move forward`
创建玩家控制脚本

`unity3d build windows --output ./builds`
构建Windows版本

`unity3d optimize textures`
分析并优化纹理资源

`unity3d profile memory`
获取内存使用报告

## 技术架构

`
Unity3D编辑器 ← → UnityEditor API (C#) ← → OpenClaw Plugin Bridge ← → AI Agent
                                ↓
                        Unity Package (EditorWindow)
                                ↓
                      HTTP Server (本地通信端口)
`

## 计费说明
- 月付：不限请求次数
- 按次：每次AI请求计费
- USDT通过OpenClaw网关结算
- 首次使用赠送20次免费体验
