# 坑点手册

## 1. 文件上传判断（ServletFileUpload 不可用）

问题：`isMultipartContent` 入参类型依赖 `javax.servlet.http.HttpServletRequest`，升级后不可用。

改造：

```java
if (!(request instanceof MultipartHttpServletRequest multipartRequest)) {
  logger.info("文件不可为空");
  return new BWJsonResult<FileResult>(new MoiraiException("-1", "请选择需要上传的文件！"));
}
```

## 2. CommonsMultipartResolver 移除

改造：

```java
if (request instanceof MultipartHttpServletRequest) {
  // multipart logic
} else {
  msg = "找不到文件！";
}
```

## 3. 多线程上下文传递

问题：`ContextExecutorWrapper` `LazyTraceThreadPoolTaskExecutor`不再支持。

改造方向：仅使用 `ThreadPoolTaskExecutor` 或 `ThreadPoolTaskScheduler`，并注入 `TaskDecorator`。

```java
@Bean
public ThreadPoolTaskExecutor moreOrgGoodsCodeThreadPool(TaskDecorator taskDecorator){
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(20);
    executor.setMaxPoolSize(25);
    executor.setQueueCapacity(256);
    executor.setKeepAliveSeconds(30);
    executor.setTaskDecorator(taskDecorator);
    return executor;
}
```

## 4. Trace 迁移（Sleuth -> Micrometer）

```java
public String currentSpanId() {
    Span span = tracer.currentSpan();
    return span == null ? null : span.context().spanId();
}
```

并补充依赖：`feign-micrometer`。

## 5. 自动配置扩展点变更

- 关注 `spring.factories` 到 `AutoConfiguration.imports` 的迁移。
- 升级后若第三方 starter 不生效，优先检查该处。

## 6. 典型运行期信号

- Logback `springProfile` 嵌套告警：需要调整到 Boot3 兼容写法。

## 7.SecurityManager已废弃

+ SecurityManager已废弃，若发现使用了SecurityManager，需做适配兼容JDK21。
