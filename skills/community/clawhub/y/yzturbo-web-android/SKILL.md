---
name: yzturbo-web-android
description: |
  YZTurboWebAndroid 高性能 Android WebView 容器 SDK 接入。用于在 Android 项目中集成 WebView 容器，实现：
  (1) WebView 预加载与复用，提升 H5 页面加载速度
  (2) 离线包管理，拦截请求优先命中本地资源
  (3) JS Bridge 双向通信，Native 与 H5 互调
  适用场景：Android App 接入 H5 页面、需要离线包能力、需要 JS 通信的业务
---

# YZTurboWebAndroid

Android 高性能 WebView 容器解决方案，支持 WebView 复用、离线包管理、JS Bridge 通信。

## 初始化配置

在 `Application` 中初始化：

```kotlin
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        WebViewLoader.INSTANCE.init(
            WebViewLoaderConfig.Builder(getApplication())
                .appKey("retail")           // 应用标识
                .poolSize(2)                // WebView 池大小
                .preloadUrl("https://xxx.com/m")
                .build()
        )
    }
}
```

添加依赖：
```groovy
dependencies {
    implementation 'com.youzan.turboweb:turbo-web:1.0.1'
}
```

## 使用 WebViewFragment（推荐）

### 基础用法

```kotlin
class WebActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_web)

        if (savedInstanceState == null) {
            val fragment = WebViewFragment().apply {
                arguments = Bundle().apply {
                    putString("web_view_url", "https://your-domain.com/path")
                    putString("web_view_title", "页面标题")
                    putBoolean("show_title_bar", true)
                    putBoolean("show_progress_bar", true)
                }
            }
            supportFragmentManager.beginTransaction()
                .replace(R.id.container, fragment)
                .commit()
        }
    }
}
```

### 继承定制

```kotlin
class MyWebFragment : WebViewFragment() {
    override fun onPageReady() {
        super.onPageReady()
        // 页面加载完成后的自定义逻辑
    }
}
```

## 手动管理 WebView（进阶）

```kotlin
// 1. 获取 WebView（复用池中有可用则复用）
val (webView, isReused) = WebViewLoader.acquireWebView(
    context = this,
    url = "https://your-domain.com/app/path",
    listener = object : WebViewListener {
        override fun onPageFinished(view: WebView?, url: String?) {}
    }
)

// 2. 添加到视图
container.addView(webView)

// 3. 页面销毁时归还
override fun onDestroy() {
    super.onDestroy()
    WebViewLoader.release(webView)
}
```

## JS Bridge 通信

### Native 注册 Handler

```kotlin
// 1. 定义 Handler
class GetUserInfoHandler : IJsCallNativeHandler {
    override fun method(): String = "getUserInfo" // 支持通配符如 "Life.*"

    override fun handleRequest(
        webView: WebView,
        request: IJsCallRequest,
        callback: IJsCallback?
    ): Boolean {
        val params = request.jsData() // 获取 JS 传递的参数
        val userInfo = mapOf("id" to 123, "name" to "Tom")
        callback?.invoke(userInfo)    // 回调 JS
        return true
    }
}

// 2. 注册（建议在 Application 初始化时）
JsHandlerRegistry.register(GetUserInfoHandler())
```

### 前端调用 Native

```javascript
// 封装调用方法
function callNative(method, params, callback) {
    if (window.YouzanJSBridge) {
        YouzanJSBridge.call(method, params, callback);
    } else {
        document.addEventListener('YouzanJSBridgeReady', () => {
            YouzanJSBridge.call(method, params, callback);
        }, false);
    }
}

// 调用示例
callNative('getUserInfo', { needDetail: true }, (response) => {
    console.log('User Info:', response);
});
```

### Native 主动调用 JS

```kotlin
// 触发自定义事件
val eventData = JsonObject().apply {
    addProperty("status", "connected")
}
WebViewLoader.trigger(webView, "networkChange", eventData)
```

JS 端监听：
```javascript
YouzanJSBridge.on('networkChange', (data) => {
    console.log('Network changed:', data.status);
});
```

### 内置事件

* `hostHide`: WebView 容器关闭/回收时触发，前端应清理全局 UI（Toast、Dialog）

```javascript
YouzanJSBridge.on('hostHide', () => {
    Toast.clear();
    Dialog.closeAll();
});
```

## 注意事项

1. **Context 切换**: `release` 时自动切回 Application Context，`acquire` 时切到当前 Activity Context
2. **池大小**: 页面切换极快时，建议 poolSize > 1
3. **路由**: 配合前端使用 `replace` 模式跳转，避免历史栈堆积
