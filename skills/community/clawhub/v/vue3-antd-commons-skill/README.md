# Vue3全家桶 + Ant Design 技能总结

## 项目介绍

这是一个全面的Vue3全家桶+Ant Design开发技能总结项目，包含了Vue3核心特性、TypeScript集成、Ant Design Vue使用、Vue Router、Pinia状态管理、网络请求封装、项目构建优化等内容。

## 目录结构

```
Vue3全家桶-antd/
 ├── skill.md                    # 技能总结主文件
 ├── skill.yaml                  # 元数据配置
 ├── prompt.md                   # 主指令文件
 ├── README.md                   # 说明文档
 ├── examples/
 │   ├── prop-type-definition.ts # 示例1：prop类型定义
 │   └── fetch-wrapper.ts        # 示例2：fetch封装及基础使用
 └── templates/
     └── output-template.md      # 输出模板
```

## 文件说明

- **skill.md**: 包含所有Vue3全家桶+Ant Design的技能总结内容
- **skill.yaml**: 项目的元数据配置文件，包含技能点、依赖、示例等配置
- **prompt.md**: 主指令文件，包含使用方法和命令说明
- **README.md**: 项目说明文档
- **examples/**: 示例代码目录
- **templates/**: 输出模板目录

## 技能点覆盖

1. **Vue3核心特性**
   - 组合式API (Composition API)
   - 响应式系统
   - 生命周期钩子
   - 计算属性与监听器

2. **TypeScript集成**
   - 组件类型定义
   - 响应式数据类型
   - Prop类型定义
   - 事件类型定义

3. **Ant Design Vue**
   - 组件使用
   - 自定义主题
   - 动态主题切换

4. **Vue Router**
   - 路由配置
   - 路由懒加载
   - 路由守卫

5. **Pinia状态管理**
   - 定义Store
   - Actions和Getters
   - 持久化存储

6. **网络请求与API**
   - fetch基础使用
   - 封装请求工具
   - 环境变量配置
   - 拦截器实现

7. **项目构建与优化**
   - Vite配置
   - 性能优化
   - 代码格式化(Prettier)

8. **publish-commons组件库**
   - 组件库概览
   - 安装与配置
   - 组件使用
   - 类型定义

9. **最佳实践**
   - 代码组织
   - 测试
   - 开发规范

## 使用方法

### 查看技能总结

直接打开`skill.md`文件查看完整的技能总结内容。

### 查看示例代码

```bash
# 查看Prop类型定义示例
cat examples/prop-type-definition.ts

# 查看fetch封装示例
cat examples/fetch-wrapper.ts
```

### 生成自定义文档

```bash
# 使用模板生成文档
vue3-antd-skill --generate --template templates/output-template.md
```

## 示例代码说明

### 1. Prop类型定义 (examples/prop-type-definition.ts)

展示Vue3组件中如何使用TypeScript定义Prop类型，包括必选属性、可选属性和默认值。

### 2. Fetch封装及基础使用 (examples/fetch-wrapper.ts)

展示如何封装fetch网络请求工具，包括URL参数处理、请求头配置、认证token、超时处理、错误处理等功能。

## 输出模板

`templates/output-template.md`是生成自定义文档的模板文件，可以根据需要修改模板内容。

## 贡献指南

欢迎贡献内容：

1. Fork项目
2. 创建新分支
3. 添加或修改内容
4. 提交Pull Request

## 许可证

MIT License
