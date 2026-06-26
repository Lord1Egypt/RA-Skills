---
name: unit-testing
description: ｜
  根据识别出的代码变更方法，为变更方法生成单元测试用例。
  当用户明确要求"生成单测用例"时触发
---

# 单元测试

基于.md描述的标准skill，使用大模型为变更方法生成高质量单测。

## Skill定义

### 基本信息
- **名称**: 单元测试
- **描述**: 为变更方法生成单测用例
- **支持语言**: Java

### 核心原则

- **禁止修改源代码**
- **测试代码必须完全独立于被测代码**
- **遇到枚举或者常量一定要理解其实际值，避免出现断言的时候使用了错误的预期值**
- **删除测试文件中没有使用的导入**
- **Java中@Data标注的类，bool类型的Get应该用isXXX的形式**
- **如果测试文件已经存在，不要重写，一定要用use_replace_file工具修改**
- **不要假设，所有的代码需要在确定的基础上编写**


### 测试类结构

#### 命名规范

- 测试类命名: `[类名]Test`
- 测试方法命名: `methodName_Scenario_ExpectedResult()`
- 示例: `calculatePrice_WhenDiscountApplied_ReturnsDiscountedPrice()`

#### 关键约束

- **优先使用现有的框架和模式，如果当前没有任何的单元测试可参考，则优先使用JUnit4进行测试**
- ❌ **禁止**使用 `@SpringBootTest`
- ❌ **禁止**在测试类中使用内部类
- ✅ 使用 `@RunWith(MockitoJUnitRunner.class)`
- ✅ 所有外部依赖用 `@Mock` 模拟
- ✅ 被测类用 `@InjectMocks` 注入
- ✅ 若测试类已存在,追加新测试方法到现有类

#### Mock 规则

1. **模拟所有外部依赖**
    - 包括方法直接调用的依赖
    - 包括代码中嵌套调用的方法
2. **严格遵循方法签名**
3. **使用项目已有对象**
    - 不创建新的测试对象类
    - 直接使用项目中的实体类、DTO等

#### 分支覆盖原则

为每个方法生成多个测试用例,覆盖:
- 正常执行路径
- 边界条件
- 异常情况
- 空值/null处理
- 条件分支(if/else、switch等)

#### 测试独立性

- 每个测试方法必须遵循以下规则:
    - 独立设置自己的测试数据
    - 不依赖其他测试方法的执行结果
    - 独立验证自己的断言

#### 断言
- 一定要按照项目依赖的JUnit版本使用特定的方法，避免junit4中使用了junit5中才有的方法，类似的
- 对于复杂对象，考虑使用AssertJ等提供更丰富断言的库

#### Mock 使用规范

- when().thenReturn() 模式
- verify() 验证调用
- Mockito 参数匹配器
- ❌ **禁止使用 spy mock 同一个实现类里的方法**
- ❌ **禁止对被测试类使用 spy**
- ✅ **让被测方法真实执行**
- ✅ **嵌套方法也要 mock**

#### 异常测试

- JUnit4 异常测试

#### 测试用例编译验证

- 编译命令

```bash
mvn clean test -DfailIfNoTests=false -Dtest=[类名]Test
```

**重要**: 仅使用此命令验证测试用例编译,不使用其他命令。

- 示例

```bash
# 测试单个类
mvn clean test -DfailIfNoTests=false -Dtest=UserServiceTest

# 测试多个类
mvn clean test -DfailIfNoTests=false -Dtest=UserServiceTest,OrderServiceTest

# 测试特定方法
mvn clean test -DfailIfNoTests=false -Dtest=UserServiceTest#getUserById_WhenUserFound_ReturnsUser
```

#### 检查清单

在生成测试用例后,验证:

- [ ] 测试类命名为 `[类名]Test`
- [ ] 使用 `@RunWith(MockitoJUnitRunner.class)`
- [ ] 所有外部依赖使用 `@Mock`
- [ ] 被测类使用 `@InjectMocks`
- [ ] 没有使用 `@SpringBootTest`
- [ ] 没有内部类
- [ ] 测试方法命名有意义
- [ ] 每个测试方法独立
- [ ] 添加了详细的 JavaDoc 中文注释
- [ ] 覆盖所有代码分支
- [ ] 没有使用 spy mock 被测类
- [ ] 所有嵌套依赖都已模拟
- [ ] 使用 `mvn clean test -DfailIfNoTests=false -Dtest=[类名]Test` 验证编译

#### 使用说明

1. **触发条件**
    - 代码变更

2. **分析被测类**
    - 识别所有外部依赖
    - 分析方法的分支逻辑
    - 确定测试场景

3. **生成测试类框架**
    - 创建 `[类名]Test` 类
    - 配置注解和依赖注入
    - 设置 `@Before` 方法

4. **编写测试用例**
    - 为每个方法设计多个测试场景
    - 覆盖正常、异常、边界情况
    - 添加详细注释

5. **编译测试用例**
    - 使用指定 Maven 命令编译
    - 确保所有测试用例编译通过

### 集成方式
此skill通过RiskForge CLI框架自动加载，执行分析时会使用大模型进行智能分析。
