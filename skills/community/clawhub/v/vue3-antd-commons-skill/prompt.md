# Vue3全家桶 + Ant Design 技能总结

## 介绍

这个技能总结包含了Vue3全家桶+Ant Design开发的核心知识点和最佳实践，涵盖了Vue3核心特性、TypeScript集成、Ant Design Vue使用、Vue Router、Pinia状态管理、网络请求封装、项目构建优化等内容。

## 使用方法

### 1. 查看技能概览

```bash
# 查看所有技能点
vue3-antd-skill --list

# 查看特定技能点详情
vue3-antd-skill --skill <skill-name>
```

### 2. 查看示例代码

```bash
# 查看所有示例
vue3-antd-skill --examples

# 查看特定示例
vue3-antd-skill --example <example-name>
```

### 3. 生成技能文档

```bash
# 生成完整的技能文档
vue3-antd-skill --generate

# 生成特定技能点的文档
vue3-antd-skill --generate --skill <skill-name>
```

## 技能点列表

### 1. Vue3核心特性
- 组合式API (Composition API)
- 响应式系统
- 生命周期钩子
- 计算属性与监听器

### 2. TypeScript集成
- 组件类型定义
- 响应式数据类型
- Prop类型定义
- 事件类型定义
- 路由与状态管理类型

### 3. Ant Design Vue
- 组件使用
- 自定义主题
- 动态主题切换

### 4. Vue Router
- 路由配置
- 路由懒加载
- 路由守卫

### 5. Pinia状态管理
- 定义Store
- Actions和Getters
- 持久化存储

### 6. 网络请求与API
- fetch基础使用
- 封装请求工具
- 环境变量配置
- 拦截器实现

### 7. 项目构建与优化
- Vite配置
- 性能优化
- 代码格式化(Prettier)

### 8. publish-commons组件库
- 组件库概览
- 安装与配置
- 组件使用
- 类型定义

### 9. 最佳实践
- 代码组织
- 测试
- 开发规范

## 示例代码

### 1. Prop类型定义
展示Vue3组件中如何使用TypeScript定义Prop类型

### 2. Fetch封装及基础使用
展示如何封装fetch网络请求工具和基础使用方法

## 输出格式

可以生成以下格式的文档：
- Markdown格式
- HTML格式
- PDF格式

## 配置选项

```bash
# 指定输出格式
vue3-antd-skill --generate --format <markdown|html|pdf>

# 指定输出文件
vue3-antd-skill --generate --output <file-path>

# 包含代码高亮
vue3-antd-skill --generate --highlight

# 显示行号
vue3-antd-skill --generate --line-numbers
```

## 贡献指南

如果你想贡献内容，可以：

1. Fork这个项目
2. 添加新的技能点或完善现有内容
3. 创建Pull Request

## 许可证

MIT License
