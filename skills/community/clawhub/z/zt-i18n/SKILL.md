---
name: zt-i18n
description: ZT Digital I18n 国际化组件,提供接口国际化、异常信息国际化、参数校验国际化及动态参数支持。支持 Properties 配置文件和数据库两种资源加载方式。适用于需要多语言支持的 Java Spring Boot 项目。
---

# ZT Digital I18n 国际化组件

本技能提供 ZT Digital Common I18n Starter 组件的使用指导。该组件规范了后端国际化接口,支持多语言资源管理、动态参数填充以及统一返回结果 (ResultVo) 的自动国际化。

## 核心功能

### 1. 多语言资源管理
支持两种资源加载方式:
- **Properties 配置文件**: 灵活便捷,适合静态词条。
- **数据库加载**: 动态管理,适合频繁变更的业务词条。

### 2. 统一返回结果 (ResultVo) 国际化
拦截器自动解析 `ResultVo` 的 `message` 属性作为国际化 Key,并根据请求头语言标识返回对应文本。

### 3. 异常提示与参数校验国际化
- **异常国际化**: 抛出 `BusinessException` 等异常时,`ResultCode` 中的 message 会被自动转换。
- **参数校验**: 在 Bean Validation 注解 (如 `@NotEmpty`) 的 `message` 属性中使用国际化 Key。

### 4. 动态参数支持
基于 `MessageFormat` 语法,支持在国际化文本中使用 `{0}`, `{1}` 等占位符,并在代码中传入动态参数进行填充。

## 快速接入

### 添加依赖

```xml
<dependency>
    <groupId>com.zt</groupId>
    <artifactId>zt-digital-common-i18n-starter</artifactId>
</dependency>
```

### 资源管理方式

#### 方式 1: Properties 配置文件 (推荐)
1. 在 `resources/i18n/` 目录下创建资源文件。
2. 命名规范: `messages_语言代码_国家代码.properties` (如: `messages_zh_CN.properties`)。
3. 在 `application.yml` 中配置:
```yaml
spring:
  messages:
    basename: i18n/messages
    encoding: UTF-8
```

#### 方式 2: 数据库加载 (V1.4.4+)
1. 开启配置:
```yaml
zt:
  i18n:
    db-resource-enable: true
```
2. 执行 `i18n_resource` 表脚本并插入词条数据。
3. 注意: 数据库 `language` 字段必须使用中划线 (如: `zh-CN`)。

## 国际化请求标识

客户端需在请求头 (Headers) 中携带语言标识:
- **Key**: `locale-language` (推荐) 或 `locale_language`
- **Value**: 必须使用中划线格式,如 `zh-CN`, `en-US`, `zh-TW`。

## 国际化使用场景

### 1. ResultVo 自动国际化
```java
// 返回成功, message 为国际化 Key
return ResultVo.success(data, "query.result.success");
```

### 2. 异常信息国际化 (带动态参数)
```java
// 词条: business.error=业务异常, 用户 {0} 状态为 {1}
throw new BusinessException(new ResultCode(506, "business.error", "张三", "禁用"));
```

### 3. 参数校验国际化
```java
public class UserVO {
    @NotEmpty(message = "user.name.empty")
    private String name;
}
```

### 4. 手动获取 (Service 注入)
```java
@Autowired
private MessageSourceService messageSourceService;

String msg = messageSourceService.getMessage("key", "param1", "param2");
```

## 最佳实践

1. **编码格式**: Properties 文件统一使用 **UTF-8**, 避免乱码。
2. **Key 命名**: 建议使用小写字母加点号分隔 (如: `user.login.fail`), 具有语义化且不冲突。
3. **动态参数**: 占位符使用 `{0}`, `{1}` 格式, 顺序必须与代码传入参数一致。
4. **优先级**: 如果同时存在配置文件和数据库词条, **数据库优先级更高**。
5. **异常处理**: 确保自定义异常继承自 `BaseException`, 否则可能无法触发自动国际化。

## 代码模板
- `templates/messages_zh_CN.properties`: Properties 资源文件示例。
- `templates/i18n_usage_example.java`: 包含 ResultVo、异常、校验及手动获取的完整示例。

## 何时使用本技能
- 配置 Spring Boot 项目的多语言支持
- 实现接口返回结果、异常信息、参数校验的国际化
- 管理 Properties 或数据库中的国际化词条
- 处理带动态参数的国际化文本
