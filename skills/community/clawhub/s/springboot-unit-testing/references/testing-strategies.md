# Spring Boot单元测试策略指南

## 测试策略金字塔

```
        ↗ 集成测试 (10-20%)
      ↗ ↗ 组件测试 (20-30%)
    ↗ ↗ ↗ 单元测试 (50-70%)
```

### 1. 单元测试 (Unit Tests) - 50-70%
- **目标**: 测试单个类或方法的内部逻辑
- **范围**: 隔离的代码单元
- **工具**: JUnit 5 + Mockito
- **速度**: 极快 (毫秒级)
- **依赖**: Mock外部依赖

### 2. 组件测试 (Component Tests) - 20-30%
- **目标**: 测试组件或模块的集成
- **范围**: 一组相关的类
- **工具**: @SpringBootTest(classes = {部分组件})
- **速度**: 中等 (秒级)
- **依赖**: 真实的部分依赖

### 3. 集成测试 (Integration Tests) - 10-20%
- **目标**: 测试整个系统的端到端流程
- **范围**: 完整的应用
- **工具**: @SpringBootTest + Testcontainers
- **速度**: 较慢 (秒到分钟级)
- **依赖**: 真实的所有依赖

## 分层测试策略

### Mapper层测试策略
```java
// 目标: 验证SQL语句和数据映射
@MybatisTest
@AutoConfigureTestDatabase
@Sql("/test-data.sql")
class UserMapperTest {
    // 1. 基础CRUD测试
    @Test void testSelectById() { ... }
    @Test void testInsert() { ... }
    @Test void testUpdate() { ... }
    @Test void testDelete() { ... }
    
    // 2. 复杂查询测试
    @Test void testSelectByCondition() { ... }
    @Test void testSelectWithJoin() { ... }
    @Test void testSelectWithPagination() { ... }
    
    // 3. 数据验证测试
    @Test void testDataMapping() { ... }
    @Test void testNullHandling() { ... }
    @Test void testTypeConversion() { ... }
    
    // 4. 性能边界测试
    @Test void testLargeDataset() { ... }
    @Test void testConcurrentAccess() { ... }
}
```

### Service层测试策略
```java
// 目标: 验证业务逻辑和事务管理
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    // 1. 正常流程测试
    @Test void testCreateUser_Success() { ... }
    @Test void testUpdateUser_Success() { ... }
    @Test void testDeleteUser_Success() { ... }
    
    // 2. 业务规则测试
    @Test void testBusinessValidation() { ... }
    @Test void testStateTransition() { ... }
    @Test void testPermissionCheck() { ... }
    
    // 3. 异常处理测试
    @Test void testCreateUser_DuplicateUsername() { ... }
    @Test void testUpdateUser_NotFound() { ... }
    @Test void testDeleteUser_AlreadyDeleted() { ... }
    
    // 4. 事务测试
    @Test void testTransactionRollback() { ... }
    @Test void testTransactionPropagation() { ... }
}
```

### Controller层测试策略
```java
// 目标: 验证HTTP接口和响应格式
@WebMvcTest(UserController.class)
class UserControllerTest {
    // 1. HTTP方法测试
    @Test void testGetUserById() { ... }
    @Test void testCreateUser() { ... }
    @Test void testUpdateUser() { ... }
    @Test void testDeleteUser() { ... }
    
    // 2. 请求验证测试
    @Test void testRequestValidation() { ... }
    @Test void testPathParameterValidation() { ... }
    @Test void testQueryParameterValidation() { ... }
    @Test void testRequestBodyValidation() { ... }
    
    // 3. 响应验证测试
    @Test void testResponseStatus() { ... }
    @Test void testResponseBody() { ... }
    @Test void testResponseHeaders() { ... }
    
    // 4. 错误处理测试
    @Test void testErrorResponses() { ... }
    @Test void testExceptionHandling() { ... }
}
```

## 全面测试覆盖策略

### 1. 正常流程测试 (Normal Flow Testing)

#### 成功场景矩阵
```java
// 为每个业务方法创建成功场景测试
@Test
void test[Method]_Success_[Scenario]() {
    // 场景1: 正常数据
    // 场景2: 边界数据
    // 场景3: 最大数据
    // 场景4: 最小数据
    // 场景5: 默认数据
}
```

#### 数据组合测试
```java
@Test
void testCreateUser_WithAllFields() { ... }

@Test  
void testCreateUser_WithRequiredFieldsOnly() { ... }

@Test
void testCreateUser_WithOptionalFields() { ... }
```

#### 状态转换测试
```java
@Test
void testUserStateTransition_ActiveToInactive() { ... }

@Test
void testUserStateTransition_InactiveToActive() { ... }

@Test
void testUserStateTransition_ActiveToDeleted() { ... }
```

### 2. 异常流程测试 (Exception Flow Testing)

#### 异常类型矩阵
| 异常类型 | 测试目标 | 示例 |
|---------|---------|------|
| 参数验证异常 | 验证输入参数 | 空值、无效格式、越界 |
| 业务逻辑异常 | 验证业务规则 | 重复数据、状态冲突 |
| 数据访问异常 | 验证数据库操作 | 数据不存在、锁冲突 |
| 外部依赖异常 | 验证外部服务 | 网络超时、服务不可用 |
| 系统异常 | 验证系统限制 | 内存不足、连接池满 |

#### 异常测试模板
```java
@Test
void test[Method]_[ExceptionType]_Throws[Exception]() {
    // Given: 设置引发异常的条件
    when(mock.method()).thenThrow(new [Exception]("message"));
    
    // When & Then: 验证异常抛出
    assertThrows([Exception].class, () -> service.method());
    
    // 验证异常消息
    Exception exception = assertThrows([Exception].class, () -> service.method());
    assertEquals("expected message", exception.getMessage());
}
```

#### 特定异常测试
```java
// 数据库异常
@Test
void testDataAccessException() {
    when(mapper.selectById(anyLong()))
        .thenThrow(new DataAccessException("Database error"));
    // ...
}

// 并发异常
@Test  
void testConcurrentModificationException() {
    // 使用CountDownLatch模拟并发
    // ...
}

// 超时异常
@Test
@Timeout(1) // 1秒超时
void testTimeoutException() {
    // 模拟长时间操作
    // ...
}
```

### 3. 边界值测试 (Boundary Value Testing)

#### 数值边界测试
```java
// 整数边界
@Test
void testAgeBoundaryValues() {
    // 最小值边界
    testWithValue(0);      // 最小有效值
    testWithValue(1);      // 最小有效值+1
    testWithValue(-1);     // 无效值 (小于最小值)
    
    // 最大值边界  
    testWithValue(150);    // 最大有效值
    testWithValue(149);    // 最大有效值-1
    testWithValue(151);    // 无效值 (大于最大值)
}

// 浮点数边界
@Test
void testPriceBoundaryValues() {
    testWithValue(0.0);      // 零值
    testWithValue(0.01);     // 最小正数
    testWithValue(Double.MAX_VALUE);  // 最大正数
    testWithValue(-0.01);    // 最小负数
    testWithValue(Double.MIN_VALUE);  // 最小非零正数
}
```

#### 字符串边界测试
```java
@Test
void testStringBoundaryValues() {
    // 长度边界
    testWithString("");                     // 空字符串
    testWithString("a");                    // 单字符
    testWithString("a".repeat(255));        // 最大长度
    testWithString("a".repeat(256));        // 超过最大长度
    
    // 内容边界
    testWithString("   ");                  // 空白字符
    testWithString("test\nnewline");        // 换行符
    testWithString("test\ttab");            // 制表符
    testWithString("test\\escape");         // 转义字符
    testWithString("测试中文");              // Unicode字符
    testWithString("🎉emoji");              // Emoji字符
}
```

#### 集合边界测试
```java
@Test
void testCollectionBoundaryValues() {
    // 空集合
    testWithCollection(Collections.emptyList());
    testWithCollection(Collections.emptySet());
    testWithCollection(Collections.emptyMap());
    
    // 单元素集合
    testWithCollection(Collections.singletonList("item"));
    testWithCollection(Collections.singleton("item"));
    testWithCollection(Collections.singletonMap("key", "value"));
    
    // 多元素集合
    testWithCollection(Arrays.asList("a", "b", "c"));
    testWithCollection(new HashSet<>(Arrays.asList(1, 2, 3)));
    testWithCollection(createLargeCollection(1000)); // 大集合
}
```

#### 时间边界测试
```java
@Test
void testDateTimeBoundaryValues() {
    // 时间边界
    testWithDateTime(LocalDateTime.MIN);      // 最小时间
    testWithDateTime(LocalDateTime.MAX);      // 最大时间
    testWithDateTime(LocalDateTime.now());    // 当前时间
    
    // 日期边界
    testWithDate(LocalDate.of(1970, 1, 1));   // Unix纪元
    testWithDate(LocalDate.of(2038, 1, 19));  // 2038年问题
    testWithDate(LocalDate.of(9999, 12, 31)); // 最大日期
    
    // 时区边界
    testWithZone(ZoneId.of("UTC"));
    testWithZone(ZoneId.of("Asia/Shanghai"));
    testWithZone(ZoneId.of("America/Los_Angeles"));
}
```

#### 状态边界测试
```java
@Test
void testStatusBoundaryValues() {
    // 初始状态
    testWithStatus(Status.INITIAL);
    
    // 中间状态
    testWithStatus(Status.PROCESSING);
    testWithStatus(Status.PENDING);
    
    // 最终状态
    testWithStatus(Status.COMPLETED);
    testWithStatus(Status.FAILED);
    testWithStatus(Status.CANCELLED);
    
    // 非法状态
    testWithStatus(null);                    // null状态
    testWithStatus(Status.UNKNOWN);          // 未知状态
}
```

## 测试数据策略

### 1. 静态测试数据
```sql
-- test-data.sql
-- 正常数据
INSERT INTO user (id, username, email, status) VALUES
(1, 'normal_user', 'normal@example.com', 1);

-- 边界数据
INSERT INTO user (id, username, email, status) VALUES
(2, 'min_user', 'min@example.com', 0),      -- 最小状态值
(3, 'max_user', 'max@example.com', 255);    -- 最大状态值

-- 异常数据
INSERT INTO user (id, username, email, status) VALUES
(4, '', 'empty@example.com', 1),            -- 空用户名
(5, NULL, 'null@example.com', 1);           -- NULL用户名
```

### 2. 动态测试数据工厂
```java
public class TestDataFactory {
    
    // 创建正常测试数据
    public static User createNormalUser() {
        User user = new User();
        user.setUsername("testuser");
        user.setEmail("test@example.com");
        user.setStatus(1);
        return user;
    }
    
    // 创建边界测试数据
    public static User createBoundaryUser() {
        User user = createNormalUser();
        user.setUsername("a".repeat(255));  // 最大长度用户名
        user.setEmail("a".repeat(100) + "@example.com");
        return user;
    }
    
    // 创建异常测试数据
    public static User createInvalidUser() {
        User user = new User();
        user.setUsername("");  // 空用户名
        user.setEmail("invalid-email");
        user.setStatus(-1);    // 无效状态
        return user;
    }
}
```

### 3. 随机测试数据
```java
public class RandomTestData {
    
    private static final Faker faker = new Faker();
    
    public static User randomUser() {
        User user = new User();
        user.setUsername(faker.name().username());
        user.setEmail(faker.internet().emailAddress());
        user.setPhone(faker.phoneNumber().cellPhone());
        user.setStatus(faker.number().numberBetween(0, 10));
        return user;
    }
    
    public static User randomUserWithBoundary() {
        User user = randomUser();
        
        // 50%概率设置边界值
        if (faker.bool().bool()) {
            user.setUsername("");  // 空用户名
        }
        if (faker.bool().bool()) {
            user.setEmail(null);   // null邮箱
        }
        
        return user;
    }
}
```

## 测试执行策略

### 1. 测试分组执行
```java
// 使用@Tag分组测试
@Tag("fast")
@Test
void testFastOperation() { ... }

@Tag("slow")
@Test  
void testSlowOperation() { ... }

@Tag("integration")
@Test
void testIntegration() { ... }
```

### 2. 测试执行顺序
```java
// 使用@TestMethodOrder控制执行顺序
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class OrderedTests {
    
    @Test
    @Order(1)
    void testFirst() { ... }
    
    @Test
    @Order(2)
    void testSecond() { ... }
}
```

### 3. 条件测试执行
```java
// 使用@EnabledIf条件执行
@EnabledIf("systemProperty['os.name'].contains('Windows')")
@Test
void testWindowsOnly() { ... }

@EnabledIf("environment.getProperty('spring.profiles.active') == 'test'")
@Test
void testTestProfileOnly() { ... }
```

## 质量保证策略

### 1. 覆盖率检查点
```java
// 关键路径必须100%覆盖
@Test
void testCriticalPath() {
    // 业务核心逻辑
    // 错误处理逻辑
    // 安全验证逻辑
}

// 重要功能必须90%+覆盖
@Test  
void testImportantFeatures() {
    // 用户注册流程
    // 订单处理流程
    // 支付流程
}
```

### 2. 测试代码质量标准
```java
// 可读性标准
@Test
void testMethodName_ShouldBeDescriptive() { ... }

// 独立性标准  
@Test
void testShouldBeIndependent() { ... }

// 确定性标准
@Test
void testShouldBeDeterministic() { ... }
```

### 3. 测试维护策略
```java
// 定期重构测试代码
// 移除重复测试逻辑
// 更新过时测试数据
// 优化测试执行速度
```

## 最佳实践总结

### 1. 测试设计原则
- **单一职责**: 每个测试只验证一个功能点
- **独立性**: 测试之间不相互依赖
- **可重复性**: 测试结果应该一致
- **快速执行**: 单元测试应该在毫秒级完成
- **明确断言**: 断言应该清晰表达期望结果

### 2. 测试编写原则
- **Given-When-Then结构**: 清晰的组织测试逻辑
- **有意义的名字**: 测试名应该描述场景和期望
- **最小化Mock**: 只Mock必要的依赖
- **避免过度测试**: 不要测试框架或库的功能
- **及时清理**: 测试后清理测试数据

### 3. 测试维护原则
- **代码即文档**: 测试代码应该像文档一样清晰
- **持续重构**: 定期优化测试代码结构
- **版本控制**: 测试代码应该和产品代码一起管理
- **自动化执行**: 集成到CI/CD流程中
- **监控告警**: 监控测试失败和性能下降