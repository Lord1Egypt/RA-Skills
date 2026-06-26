# 友盟 U-APP 统计 SDK 集成 Skill

## 安装位置

```
~/.openclaw/skills/umeng-uapp-integration/SKILL.md
```

## 触发关键词

- 友盟
- umeng
- U-APP
- 统计 SDK
- 集成友盟
- 移动统计
- 应用埋点
- 数据分析 SDK

## 使用示例

### 示例 1：基础集成

**用户：** 帮我在 APK 里集成一下友盟 U-APP 统计 SDK

**Skill 响应：**
1. 添加 Maven 仓库到项目级 build.gradle
2. 添加 SDK 依赖到 app 级 build.gradle
3. 添加必要权限到 AndroidManifest.xml
4. 创建 Application 类初始化 SDK
5. 配置 ProGuard 规则

### 示例 2：获取 AppKey

**用户：** 友盟的 AppKey 在哪里找？

**Skill 响应：**
1. 登录 https://www.umeng.com/
2. 进入「U-APP 统计」产品
3. 创建或选择应用
4. 在应用设置中查看 AppKey

### 示例 3：合规初始化

**用户：** 友盟 SDK 如何合规初始化？

**Skill 响应：**
1. 在 Application.onCreate() 中调用 preInit()（预初始化）
2. 在用户同意隐私政策后调用 init()（正式初始化）
3. 在隐私政策中声明使用友盟 SDK

## 输出内容

Skill 会根据用户需求提供：

1. **代码片段** - Gradle 配置、Kotlin/Java 代码、XML 配置
2. **步骤说明** - 详细的集成步骤
3. **注意事项** - 合规要求、常见问题
4. **参考链接** - 官方文档、SDK 下载

## 依赖检查

Skill 会检查以下文件是否存在：

- `build.gradle` 或 `build.gradle.kts`（项目级）
- `app/build.gradle` 或 `app/build.gradle.kts`（应用级）
- `AndroidManifest.xml`
- `proguard-rules.pro`（如使用混淆）

## 版本信息

- SDK 版本：common 9.6.6, asms 1.6.4
- 最低 Android SDK：21
- 目标 Android SDK：34
- Java 版本：17

## 更新日志

- 2026-03-14: 初始版本创建
  - 基于友盟官方文档 118584
  - 包含完整集成流程
  - 包含合规初始化指南
