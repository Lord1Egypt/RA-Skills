# Spring Boot异常测试模式

## 异常分类体系

### 1. 参数验证异常 (Parameter Validation Exceptions)
```java
// 空值异常
@Test
void testMethod_NullParameter_ThrowsIllegalArgumentException() {
    // Given
    String nullParam = null;
    
    // When & Then
    IllegalArgumentException exception = assertThrows(
        IllegalArgumentException.class,
        () -> service.method(nullParam)
    );
    
    assertEquals("参数不能为null", exception.getMessage());
}

// 空字符串异常
@Test
void testMethod_EmptyString_ThrowsIllegalArgumentException() {
    assertThrows(IllegalArgumentException.class,
        () -> service.method(""));
}

// 空白字符串异常
@Test
void testMethod_BlankString_ThrowsIllegalArgumentException() {
    assertThrows(IllegalArgumentException.class,
        () -> service.method("   "));
}

// 格式异常
@Test
void testMethod_InvalidFormat_ThrowsIllegalArgumentException() {
    assertThrows(IllegalArgumentException.class,
        () -> service.method("invalid-email"));
}
```

### 2. 业务逻辑异常 (Business Logic Exceptions)
```java
// 数据不存在异常
@Test
void testMethod_EntityNotFound_ThrowsEntityNotFoundException() {
    // Given
    Long nonExistingId = 999L;
    when(repository.findById(nonExistingId)).thenReturn(Optional.empty());
    
    // When & Then
    EntityNotFoundException exception = assertThrows(
        EntityNotFoundException.class,
        () -> service.method(nonExistingId)
    );
    
    assertEquals("用户不存在: 999", exception.getMessage());
}

// 数据重复异常
@Test
void testMethod_DuplicateData_ThrowsDuplicateKeyException() {
    // Given
    String duplicateUsername = "existinguser";
    when(repository.existsByUsername(duplicateUsername)).thenReturn(true);
    
    // When & Then
    DuplicateKeyException exception = assertThrows(
        DuplicateKeyException.class,
        () -> service.createUser(duplicateUsername)
    );
    
    assertEquals("用户名已存在: existinguser", exception.getMessage());
}

// 状态冲突异常
@Test
void testMethod_InvalidState_ThrowsIllegalStateException() {
    // Given
    User user = TestDataFactory.createUserWithStatus(Status.DELETED);
    when(repository.findById(1L)).thenReturn(Optional.of(user));
    
    // When & Then
    IllegalStateException exception = assertThrows(
        IllegalStateException.class,
        () -> service.updateUser(1L)
    );
    
    assertEquals("用户已删除，无法修改", exception.getMessage());
}

// 业务规则异常
@Test
void testMethod_BusinessRuleViolation_ThrowsBusinessException() {
    // Given
    Order order = TestDataFactory.createOrderWithAmount(-100.0);
    
    // When & Then
    BusinessException exception = assertThrows(
        BusinessException.class,
        () -> service.processOrder(order)
    );
    
    assertEquals("订单金额必须大于0", exception.getMessage());
    assertEquals("INVALID_AMOUNT", exception.getErrorCode());
}
```

### 3. 数据访问异常 (Data Access Exceptions)
```java
// 数据库连接异常
@Test
void testMethod_DatabaseConnectionFailed_ThrowsDataAccessException() {
    // Given
    when(repository.findAll())
        .thenThrow(new DataAccessResourceFailureException("数据库连接失败"));
    
    // When & Then
    DataAccessException exception = assertThrows(
        DataAccessException.class,
        () -> service.getAllUsers()
    );
    
    assertTrue(exception.getMessage().contains("数据库"));
}

// 乐观锁异常
@Test
void testMethod_OptimisticLockingFailure_ThrowsOptimisticLockingFailureException() {
    // Given
    User user = TestDataFactory.createUser();
    user.setVersion(1L);
    when(repository.save(any(User.class)))
        .thenThrow(new OptimisticLockingFailureException("版本冲突"));
    
    // When & Then
    OptimisticLockingFailureException exception = assertThrows(
        OptimisticLockingFailureException.class,
        () -> service.updateUser(user)
    );
    
    assertEquals("版本冲突", exception.getMessage());
}

// 唯一约束异常
@Test
void testMethod_UniqueConstraintViolation_ThrowsDataIntegrityViolationException() {
    // Given
    when(repository.save(any(User.class)))
        .thenThrow(new DataIntegrityViolationException("唯一约束冲突"));
    
    // When & Then
    DataIntegrityViolationException exception = assertThrows(
        DataIntegrityViolationException.class,
        () -> service.createUser("duplicate")
    );
    
    assertTrue(exception.getMessage().contains("约束"));
}

// 死锁异常
@Test
void testMethod_DeadlockDetected_ThrowsCannotAcquireLockException() {
    // Given
    when(repository.updateStatus(anyLong(), anyInt()))
        .thenThrow(new CannotAcquireLockException("检测到死锁"));
    
    // When & Then
    CannotAcquireLockException exception = assertThrows(
        CannotAcquireLockException.class,
        () -> service.lockUser(1L)
    );
    
    assertEquals("检测到死锁", exception.getMessage());
}
```

### 4. 外部依赖异常 (External Dependency Exceptions)
```java
// HTTP客户端异常
@Test
void testMethod_HttpClientError_ThrowsRestClientException() {
    // Given
    when(externalService.callApi(any()))
        .thenThrow(new RestClientException("HTTP请求失败"));
    
    // When & Then
    RestClientException exception = assertThrows(
        RestClientException.class,
        () -> service.callExternalService()
    );
    
    assertEquals("HTTP请求失败", exception.getMessage());
}

// 服务不可用异常
@Test
void testMethod_ServiceUnavailable_ThrowsServiceUnavailableException() {
    // Given
    when(externalService.checkHealth())
        .thenThrow(new ServiceUnavailableException("服务不可用"));
    
    // When & Then
    ServiceUnavailableException exception = assertThrows(
        ServiceUnavailableException.class,
        () -> service.healthCheck()
    );
    
    assertEquals("服务不可用", exception.getMessage());
}

// 超时异常
@Test
@Timeout(2) // 2秒超时
void testMethod_Timeout_ThrowsTimeoutException() {
    // Given
    when(externalService.slowOperation())
        .thenAnswer(invocation -> {
            Thread.sleep(3000); // 3秒延迟
            return "result";
        });
    
    // When & Then
    assertThrows(TimeoutException.class,
        () -> service.callSlowOperation());
}

// 网络异常
@Test
void testMethod_NetworkError_ThrowsIOException() {
    // Given
    when(fileService.upload(any()))
        .thenThrow(new IOException("网络连接中断"));
    
    // When & Then
    IOException exception = assertThrows(
        IOException.class,
        () -> service.uploadFile(new byte[0])
    );
    
    assertEquals("网络连接中断", exception.getMessage());
}
```

### 5. 系统异常 (System Exceptions)
```java
// 内存不足异常
@Test
void testMethod_OutOfMemory_ThrowsOutOfMemoryError() {
    // Given - 模拟内存不足场景
    when(memoryService.allocateLargeMemory())
        .thenThrow(new OutOfMemoryError("Java heap space"));
    
    // When & Then
    OutOfMemoryError error = assertThrows(
        OutOfMemoryError.class,
        () -> service.processLargeData()
    );
    
    assertTrue(error.getMessage().contains("heap space"));
}

// 栈溢出异常
@Test
void testMethod_StackOverflow_ThrowsStackOverflowError() {
    // Given - 模拟无限递归
    when(recursiveService.infiniteRecursion())
        .thenThrow(new StackOverflowError());
    
    // When & Then
    StackOverflowError error = assertThrows(
        StackOverflowError.class,
        () -> service.recursiveOperation()
    );
    
    // StackOverflowError通常没有详细信息
    assertNotNull(error);
}

// 类未找到异常
@Test
void testMethod_ClassNotFound_ThrowsClassNotFoundException() {
    // Given - 模拟动态类加载失败
    when(classLoader.loadClass("NonExistingClass"))
        .thenThrow(new ClassNotFoundException("类未找到: NonExistingClass"));
    
    // When & Then
    ClassNotFoundException exception = assertThrows(
        ClassNotFoundException.class,
        () -> service.dynamicLoadClass()
    );
    
    assertEquals("类未找到: NonExistingClass", exception.getMessage());
}
```

## 异常测试模式

### 模式1: 异常消息验证
```java
@Test
void testMethod_ValidatesExceptionMessage() {
    // When
    Exception exception = assertThrows(
        IllegalArgumentException.class,
        () -> service.method("invalid")
    );
    
    // Then - 验证异常消息
    assertThat(exception.getMessage())
        .isNotNull()
        .isNotEmpty()
        .contains("参数")
        .contains("无效")
        .doesNotContain("密码"); // 不应该包含敏感信息
    
    // 验证消息格式
    assertThat(exception.getMessage())
        .matches(".*参数.*无效.*") // 正则匹配
        .hasSizeGreaterThan(5);    // 最小长度
}
```

### 模式2: 异常链验证
```java
@Test
void testMethod_ValidatesExceptionCause() {
    // When
    ServiceException exception = assertThrows(
        ServiceException.class,
        () -> service.method()
    );
    
    // Then - 验证异常原因链
    assertThat(exception)
        .hasCauseInstanceOf(IOException.class) // 直接原因
        .hasRootCauseInstanceOf(SocketException.class) // 根本原因
        .hasMessageContaining("服务调用失败");
    
    // 验证原因消息
    Throwable cause = exception.getCause();
    assertThat(cause)
        .isInstanceOf(IOException.class)
        .hasMessageContaining("连接超时");
}
```

### 模式3: 异常属性验证
```java
@Test
void testMethod_ValidatesExceptionProperties() {
    // Given
    String expectedErrorCode = "USER_NOT_FOUND";
    Map<String, Object> expectedDetails = Map.of(
        "userId", 999L,
        "timestamp", "2024-01-01T12:00:00"
    );
    
    // When
    BusinessException exception = assertThrows(
        BusinessException.class,
        () -> service.method(999L)
    );
    
    // Then - 验证异常属性
    assertThat(exception.getErrorCode()).isEqualTo(expectedErrorCode);
    assertThat(exception.getDetails()).containsAllEntriesOf(expectedDetails);
    assertThat(exception.getTimestamp()).isBefore(LocalDateTime.now());
    
    // 验证自定义属性
    if (exception instanceof ValidationException) {
        ValidationException validationException = (ValidationException) exception;
        assertThat(validationException.getFieldErrors())
            .hasSize(2)
            .containsKey("username")
            .containsKey("email");
    }
}
```

### 模式4: 多个异常场景
```java
@ParameterizedTest
@ValueSource(strings = {"", "   ", null, "invalid@", "@domain.com"})
void testCreateUser_InvalidEmail_ThrowsException(String invalidEmail) {
    // Given
    User user = TestDataFactory.createUser();
    user.setEmail(invalidEmail);
    
    // When & Then
    IllegalArgumentException exception = assertThrows(
        IllegalArgumentException.class,
        () -> service.createUser(user)
    );
    
    // 根据不同的无效邮箱类型验证不同的消息
    if (invalidEmail == null) {
        assertThat(exception.getMessage()).contains("不能为null");
    } else if (invalidEmail.trim().isEmpty()) {
        assertThat(exception.getMessage()).contains("不能为空");
    } else {
        assertThat(exception.getMessage()).contains("格式不正确");
    }
}
```

### 模式5: 异常恢复测试
```java
@Test
void testMethod_ExceptionRecovery() {
    // Given - 第一次调用失败，第二次成功
    when(externalService.call())
        .thenThrow(new RuntimeException("第一次失败"))
        .thenReturn("成功结果");
    
    // When - 带有重试逻辑的方法
    String result = service.methodWithRetry();
    
    // Then - 验证最终成功
    assertThat(result).isEqualTo("成功结果");
    
    // 验证重试次数
    verify(externalService, times(2)).call();
}
```

### 模式6: 异常传播测试
```java
@Test
void testMethod_ExceptionPropagation() {
    // Given - 内层方法抛出异常
    when(innerService.process())
        .thenThrow(new BusinessException("内部错误"));
    
    // When & Then - 验证异常正确传播
    BusinessException exception = assertThrows(
        BusinessException.class,
        () -> outerService.method()
    );
    
    // 验证异常没有被错误转换
    assertThat(exception.getMessage()).isEqualTo("内部错误");
    assertThat(exception).isExactlyInstanceOf(BusinessException.class);
    
    // 验证异常栈信息
    StackTraceElement[] stackTrace = exception.getStackTrace();
    assertThat(stackTrace[0].getClassName())
        .contains("InnerService"); // 异常源自内层服务
}
```

### 模式7: 事务异常测试
```java
@Test
@Transactional
void testMethod_TransactionRollbackOnException() {
    // Given
    User user = TestDataFactory.createUser();
    userRepository.save(user);
    
    // When - 抛出运行时异常应该触发回滚
    assertThrows(RuntimeException.class,
        () -> service.methodThatThrowsException(user.getId()));
    
    // Then - 验证数据已回滚（不存在）
    Optional<User> foundUser = userRepository.findById(user.getId());
    assertThat(foundUser).isEmpty(); // 事务已回滚，用户不存在
    
    // 验证事务状态
    assertFalse(TransactionSynchronizationManager.isActualTransactionActive());
}
```

### 模式8: 并发异常测试
```java
@Test
void testMethod_ConcurrentModificationException() throws InterruptedException {
    // Given
    int threadCount = 10;
    CountDownLatch startLatch = new CountDownLatch(1);
    CountDownLatch endLatch = new CountDownLatch(threadCount);
    AtomicInteger successCount = new AtomicInteger(0);
    AtomicInteger failureCount = new AtomicInteger(0);
    
    // When - 并发执行
    for (int i = 0; i < threadCount; i++) {
        new Thread(() -> {
            try {
                startLatch.await();
                service.concurrentOperation();
                successCount.incrementAndGet();
            } catch (ConcurrentModificationException e) {
                failureCount.incrementAndGet();
            } catch (Exception e) {
                // 其他异常
            } finally {
                endLatch.countDown();
            }
        }).start();
    }
    
    startLatch.countDown(); // 同时开始
    endLatch.await(5, TimeUnit.SECONDS); // 等待所有线程完成
    
    // Then - 验证并发结果
    assertThat(successCount.get()).isGreaterThan(0);
    assertThat(failureCount.get()).isGreaterThan(0);
    assertThat(successCount.get() + failureCount.get()).isEqualTo(threadCount);
}
```

## 异常测试最佳实践

### 1. 异常消息标准化
```java
// 使用常量定义异常消息
public class ErrorMessages {
    public static final String USER_NOT_FOUND = "用户不存在: %s";
    public static final String INVALID_EMAIL = "邮箱格式不正确: %s";
    public static final String DUPLICATE_USERNAME = "用户名已存在: %s";
}

// 测试中使用
@Test
void testMethod_ValidatesStandardErrorMessage() {
    Exception exception = assertThrows(
        BusinessException.class,
        () -> service.method()
    );
    
    String expectedMessage = String.format(ErrorMessages.USER_NOT_FOUND, 999L);
    assertEquals(expectedMessage, exception.getMessage());
}
```

### 2. 异常类型层次结构
```java
// 定义清晰的异常层次
public abstract class AppException extends RuntimeException {
    private final String errorCode;
    private final Map<String, Object> details;
    
    // 构造函数、getter等
}

public class ValidationException extends AppException {
    private final List<FieldError> fieldErrors;
    // ...
}

public class BusinessException extends AppException {
    // ...
}

public class SystemException extends AppException {
    // ...
}

// 测试异常类型
@Test
void testMethod_ThrowsCorrectExceptionType() {
    // 验证精确类型
    assertThrowsExactly(ValidationException.class,
        () -> service.validate(null));
    
    // 验证父类型
    assertThrows(AppException.class,
        () -> service.method());
}
```

### 3. 异常测试工具方法
```java
// 创建异常测试工具类
public class ExceptionAssertions {
    
    public static void assertValidationException(
            Executable executable, 
            String fieldName, 
            String errorMessage) {
        
        ValidationException exception = assertThrows(
            ValidationException.class,
            executable
        );
        
        assertThat(exception.getFieldErrors())
            .anyMatch(error -> 
                error.getField().equals(fieldName) &&
                error.getMessage().contains(errorMessage)
            );
    }
    
    public static void assertBusinessException(
            Executable executable,
            String errorCode,
            String errorMessage) {
        
        BusinessException exception = assertThrows(
            BusinessException.class,
            executable
        );
        
        assertThat(exception.getErrorCode()).isEqualTo(errorCode);
        assertThat(exception.getMessage()).contains(errorMessage);
    }
    
    public static void assertExceptionChain(
            Executable executable,
            Class<? extends Throwable> rootCause) {
        
        Exception exception = assertThrows(
            Exception.class,
            executable
        );
        
        Throwable cause = exception;
        while (cause.getCause() != null) {
            cause = cause.getCause();
        }
        
        assertThat(cause).isInstanceOf(rootCause);
    }
}

// 使用工具方法
@Test
void testMethod_UsingAssertionHelpers() {
    ExceptionAssertions.assertValidationException(
        () -> service.createUser(""),
        "username",
        "不能为空"
    );
}
```

### 4. 异常测试数据工厂
```java
// 创建专门用于异常测试的数据工厂
public class ExceptionTestDataFactory {
    
    public static User createUserWithNullUsername() {
        User user = TestDataFactory.createNormalUser();
        user.setUsername(null);
        return user;
    }
    
    public static User createUserWithInvalidEmail() {
        User user = TestDataFactory.createNormalUser();
        user.setEmail("invalid-email-format");
        return user;
    }
    
    public static User createUserWithDuplicateData() {
        User user = TestDataFactory.createNormalUser();
        user.setUsername("duplicate_username");
        return user;
    }
    
    public static Order createOrderWithNegativeAmount() {
        Order order = new Order();
        order.setAmount(-100.0);
        return order;
    }
}

// 使用异常测试数据
@Test
void testCreateUser_WithExceptionTestData() {
    User invalidUser = ExceptionTestDataFactory.createUserWithNullUsername();
    
    assertThrows(IllegalArgumentException.class,
        () -> service.createUser(invalidUser));
}
```

### 5. 异常测试覆盖率检查
```java
// 使用JaCoCo检查异常处理覆盖率
@Test
void testAllExceptionHandlingPaths() {
    // 测试所有异常分支
    testMethod_NullParameter_ThrowsException();
    testMethod_EmptyParameter_ThrowsException();
    testMethod_InvalidFormat_ThrowsException();
    testMethod_EntityNotFound_ThrowsException();
    testMethod_DuplicateData_ThrowsException();
    testMethod_DatabaseError_ThrowsException();
    testMethod_ExternalServiceError_ThrowsException();
    
    // 验证异常处理逻辑都被测试覆盖
    // 可以通过JaCoCo报告验证
}
```

## 异常测试注意事项

### 1. 不要测试框架异常
```java
// 错误：测试Spring框架的异常
@Test
void testMethod_ShouldNotTestFrameworkExceptions() {
    // 不要测试这些：
    // - NullPointerException (除非是你自己抛出的)
    // - IndexOutOfBoundsException (除非是业务逻辑)
    // - 其他运行时异常 (除非是预期的业务异常)
}
```

### 2. 避免过度细化异常测试
```java
// 错误：为每个可能的空值单独测试
@Test void testMethod_NullParam1() { ... }
@Test void testMethod_NullParam2() { ... }
@Test void testMethod_NullParam3() { ... }

// 正确：使用参数化测试
@ParameterizedTest
@NullSource
@ValueSource(strings = {"", "   "})
void testMethod_InvalidParameters(String invalidParam) {
    assertThrows(IllegalArgumentException.class,
        () -> service.method(invalidParam));
}
```

### 3. 保持异常测试的独立性
```java
// 错误：测试之间依赖异常状态
@Test
void testMethod_FirstTestSetsUpException() {
    service.methodThatThrowsException();
    // 改变了某些状态
}

@Test  
void testMethod_SecondTestDependsOnFirst() {
    // 依赖第一个测试改变的状态
}

// 正确：每个测试独立
@Test
void testMethod_IndependentTest1() {
    // 完整的Given-When-Then
}

@Test
void testMethod_IndependentTest2() {
    // 完整的Given-When-Then，不依赖其他测试
}
```

### 4. 验证异常后的清理
```java
@Test
void testMethod_ValidatesCleanupAfterException() {
    // Given
    Resource resource = acquireResource();
    
    try {
        // When - 抛出异常
        service.methodThatThrowsException(resource);
        fail("应该抛出异常");
    } catch (Exception e) {
        // Then - 验证资源已清理
        assertThat(resource.isClosed()).isTrue();
        assertThat(resource.isLocked()).isFalse();
    }
}
```

## 总结

异常测试是确保系统健壮性的关键部分。通过系统化的异常测试策略，可以：

1. **提高系统稳定性** - 确保异常情况被正确处理
2. **增强用户体验** - 提供清晰、有用的错误信息
3. **简化问题排查** - 异常信息包含足够的调试信息
4. **支持监控告警** - 异常类型和代码支持监控系统

遵循这些异常测试模式，可以为Spring Boot应用构建全面的异常处理测试覆盖。