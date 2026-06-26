---
name: umeng-uapp-integration
description: "帮助用户在 Android 项目中快速集成友盟 U-APP 统计 SDK。包括自动配置依赖、权限、初始化代码、混淆规则等。触发：用户提到'友盟'、'umeng'、'U-APP'、'统计 SDK'、'集成友盟'、'移动统计'、'应用埋点'等关键词。"
homepage: https://developer.umeng.com/docs/119267/detail/118584
metadata: { "openclaw": { "emoji": "📊", "requires": { "files": ["build.gradle", "build.gradle.kts", "AndroidManifest.xml"] } } }
---

# 友盟 U-APP 统计 SDK 集成技能

## 何时使用

✅ **使用此技能当：**

- 用户需要在 Android 项目中集成友盟统计 SDK
- 用户提到"友盟"、"umeng"、"U-APP"、"统计 SDK"
- 用户需要配置移动应用数据埋点
- 用户需要添加应用分析功能
- 用户需要配置 SDK 初始化代码

❌ **不使用此技能当：**

- iOS 项目集成 → 使用 iOS 集成文档
- HarmonyOS 项目 → 使用 HarmonyOS 集成文档
- 网站统计 → 使用 U-Web SDK
- 小程序统计 → 使用 U-Mini SDK
- 消息推送功能 → 使用 U-Push SDK

## 集成流程

## 集成流程

### 1. 添加 Maven 仓库（项目级 build.gradle）

在项目根目录的 `build.gradle` 或 `build.gradle.kts` 中添加：

```groovy
buildscript {
    repositories {
        google()
        mavenCentral()
        maven { url 'https://repo1.maven.org/maven2/' }
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
        maven { url 'https://repo1.maven.org/maven2/' }
    }
}
```

### 2. 添加 SDK 依赖（应用级 build.gradle）

在 `app/build.gradle` 或 `app/build.gradle.kts` 的 dependencies 块中添加：

```groovy
dependencies {
    // 友盟统计 SDK - 必选
    implementation 'com.umeng.umsdk:common:9.6.6'
    implementation 'com.umeng.umsdk:asms:1.6.4'
    
    // 高级运营分析功能依赖库 - 可选（使用卸载分析、反作弊时必选）
    implementation 'com.umeng.umsdk:uyumao:1.1.2'
    
    // ABTest 功能 - 可选
    implementation 'com.umeng.umsdk:abtest:1.0.0'
}
```

### 3. 添加权限（AndroidManifest.xml）

在 `AndroidManifest.xml` 的 `<manifest>` 标签内添加：

```xml
<!-- 必选权限 -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.READ_PHONE_STATE" />

<!-- 可选权限（用于反作弊和地域分布） -->
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
```

### 4. 创建 Application 类并初始化 SDK

创建或修改 Application 类：

```kotlin
package com.your.package

import android.app.Application
import com.umeng.analytics.MobclickSdk
import com.umeng.commonsdk.UMGlobals

class YourApplication : Application() {

    override fun onCreate() {
        super.onCreate()
        
        // 合规初始化：预初始化（不会采集数据）
        MobclickSdk.preInit(this, "YOUR_APP_KEY", "default")
    }
    
    // 在用户同意隐私政策后调用正式初始化
    fun initUmengAfterPrivacyAgreed() {
        MobclickSdk.init(this, "YOUR_APP_KEY")
        MobclickSdk.setChannel("default")
        
        // 调试模式（发布前请关闭）
        UMGlobals.setDebugMode(true)
    }
}
```

在 `AndroidManifest.xml` 中注册 Application：

```xml
<application
    android:name=".YourApplication"
    ... >
</application>
```

### 5. 合规初始化流程

**重要**：根据工信部要求，必须在用户同意隐私政策后再初始化 SDK：

```kotlin
// 在 Application.onCreate() 中 - 预初始化（不采集数据）
override fun onCreate() {
    super.onCreate()
    MobclickSdk.preInit(this, "YOUR_APP_KEY", "channel")
}

// 在用户同意隐私政策后 - 正式初始化
fun onPrivacyPolicyAgreed() {
    MobclickSdk.init(this, "YOUR_APP_KEY")
    MobclickSdk.setChannel("channel")
}
```

### 6. 混淆配置（proguard-rules.pro）

如果应用使用混淆，添加以下规则：

```proguard
# 友盟 SDK
-keep class com.umeng.** { *; }
-keep class com.ut.** { *; }
-keep class org.android.** { *; }
-keep class org.agoo.** { *; }
-keep class anet.channel.** { *; }
-keep class anetwork.channel.** { *; }
-keep class com.ta.** { *; }
-keep class com.ut.device.** { *; }
-keep class org.json.** { *; }
-keep class com.uyumao.** { *; }

# 保留 R 文件
-keep public class com.your.package.R$* {
    public static final int *;
}
```

### 7. 埋点验证配置（可选）

在 `AndroidManifest.xml` 中添加 scheme 用于测试埋点：

```xml
<activity android:name=".MainActivity">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
    
    <!-- 埋点验证 scheme -->
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="um.YOUR_APP_KEY" />
    </intent-filter>
</activity>
```

## 常用 API 示例

### 页面统计（Activity）

```kotlin
override fun onResume() {
    super.onResume()
    MobclickSdk.onPageStart("PageName")
    MobclickSdk.onResume(this)
}

override fun onPause() {
    super.onPause()
    MobclickSdk.onPageEnd("PageName")
    MobclickSdk.onPause(this)
}
```

### 页面统计（Compose）

```kotlin
// 在 Compose 中手动统计
MobclickSdk.onPageStart("HomePage")
// ... 页面内容
MobclickSdk.onPageEnd("HomePage")
```

### 自定义事件统计

```kotlin
// 简单事件
MobclickSdk.onEvent(context, "button_click")

// 带参数的事件
val attributes = mapOf(
    "button_id" to "submit",
    "page" to "home",
    "user_level" to "vip"
)
MobclickSdk.onEvent(context, "button_click", attributes)

// 带数值的事件（用于统计金额、时长等）
MobclickSdk.onEvent(context, "purchase", mapOf("item_id" to "123"), 99.0)
```

### 用户标识

```kotlin
// 设置用户 ID（登录后调用）
MobclickSdk.setUserId("user_12345")

// 清除用户 ID（登出时调用）
MobclickSdk.clearUserId()
```

## 隐私政策条款参考

在隐私政策中需要包含以下说明：

```
我们接入了友盟+SDK，友盟+SDK需要收集您的设备信息（IMEI/MAC/Android ID/OAID/IDFA/OpenUDID/GUID/IP 地址/SIM 卡 IMSI 信息等）及粗略位置（可选），
用于统计分析服务，以帮助您了解应用使用情况。
友盟+隐私政策链接：https://www.umeng.com/page/policy
```

## 验证集成

1. 构建并运行应用
2. 在 Logcat 中搜索 "umeng" 或 "mob" 关键字
3. 查看是否有初始化成功日志
4. 登录友盟后台，等待约 15 分钟后查看数据

## 常见问题

### 1. 数据不显示？
- 检查 AppKey 是否正确
- 确认包名与友盟后台配置一致
- 等待数据延迟（约 15 分钟）
- 检查网络权限

### 2. 初始化失败？
- 确认在 Application 中初始化
- 检查是否在用户同意隐私政策后调用
- 查看 Logcat 错误日志

### 3. 混淆后 SDK 失效？
- 确保添加了完整的混淆规则
- 检查 R 文件是否被保留

## 参考资料

- [友盟开发者中心](https://developer.umeng.com/)
- [Android SDK 集成文档](https://developer.umeng.com/docs/119267/detail/118584)
- [SDK 下载](https://devs.umeng.com/sdk)
- [合规配置指引](https://developer.umeng.com/docs/119267/detail/182050)
- [常见问题](https://developer.umeng.com/docs/119267/cate/119530)

## 注意事项

1. **合规第一**：必须在用户同意隐私政策后才能正式初始化 SDK
2. **包名一致**：友盟后台配置的包名必须与应用的 applicationId 一致
3. **数据延迟**：统计数据通常有 15 分钟左右的延迟
4. **发布前关闭调试**：发布前将 `setDebugMode(false)`
5. **高级功能**：使用卸载分析、反作弊等功能需要集成 uyumao 库并配置混淆
