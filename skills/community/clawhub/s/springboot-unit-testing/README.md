# Spring Boot单元测试专家Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-2.7%2B-green.svg)](https://spring.io/projects/spring-boot)
[![Java](https://img.shields.io/badge/Java-11%2B-blue.svg)](https://www.java.com)
[![ClawHub](https://img.shields.io/badge/ClawHub-Skill-orange.svg)](https://clawhub.com)

## 🎯 概述

这是一个专门用于Spring Boot + MyBatis + MySQL项目的专业单元测试Skill。提供全面的测试覆盖策略，确保：

1. **正常流程全面覆盖** - 所有业务逻辑都有对应的成功测试
2. **异常场景充分测试** - 各种错误情况和异常处理都有测试验证  
3. **边界值完整验证** - 数据边界、参数边界、状态边界都有测试
4. **分层测试策略** - Mapper、Service、Controller各层都有专业测试方法

## 📦 快速安装

### 从ClawHub安装（推荐）
```bash
# 待发布到ClawHub后可用
clawhub install springboot-unit-testing
```

### 手动安装
```bash
# 克隆仓库
git clone https://github.com/your-repo/springboot-unit-testing.git

# 或下载Release包
wget https://github.com/your-repo/springboot-unit-testing/releases/download/v1.0.0/springboot-unit-testing-skill-v1.0.0.zip
unzip springboot-unit-testing-skill-v1.0.0.zip
```

## 📁 目录结构

```
test-skill/
├── SKILL.md                    # Skill主文件
├── README.md                   # 说明文档
├── scripts/                    # 工具脚本
│   ├── check-coverage.sh      # 覆盖率检查脚本
│   ├── generate-test-data.py  # 测试数据生成脚本
│   └── generate-test-report.py # 测试报告生成脚本
├── references/                 # 参考文档
│   ├── dependencies.md        # 依赖配置
│   ├── testing-strategies.md  # 测试策略
│   ├── exception-patterns.md  # 异常测试模式
│   └── boundary-testing.md    # 边界值测试
└── assets/                    # 资源文件
```

## 🚀 快速开始

### 1. 安装依赖
查看 [references/dependencies.md](references/dependencies.md) 获取完整的Maven依赖配置。

### 2. 运行测试检查
```bash
# 运行测试
mvn clean test

# 检查覆盖率
./scripts/check-coverage.sh

# 生成测试报告
python scripts/generate-test-report.py .
```

### 3. 生成测试数据
```bash
python scripts/generate-test-data.py /path/to/your/project
```

## 🎯 核心功能

### 1. 分层测试策略
- **Mapper层**: `@MybatisTest` + H2内存数据库
- **Service层**: `@ExtendWith(MockitoExtension.class)` + Mock依赖  
- **Controller层**: `@WebMvcTest` + MockMvc
- **集成测试**: `@SpringBootTest` + Testcontainers

### 2. 全面测试覆盖
- **正常流程测试**: 成功场景、数据组合、状态转换
- **异常流程测试**: 参数验证、业务规则、数据访问、外部依赖异常
- **边界值测试**: 数值边界、字符串边界、集合边界、时间边界、状态边界

### 3. 测试数据管理
- **静态数据**: SQL文件导入
- **动态数据**: TestDataFactory模式
- **随机数据**: Faker库生成
- **边界数据**: 专门测试边界条件

## 📊 覆盖率目标

| 测试类型 | 覆盖率目标 | 说明 |
|---------|-----------|------|
| Mapper层 | 90%+ | 覆盖所有SQL语句 |
| Service层 | 95%+ | 覆盖所有业务逻辑分支 |
| Controller层 | 85%+ | 覆盖所有API端点 |
| 异常测试 | 100% | 所有异常处理逻辑 |
| 边界测试 | 100% | 所有边界条件 |

## 🔧 工具脚本

### 1. 覆盖率检查 (`check-coverage.sh`)
```bash
# 运行测试并检查覆盖率
./scripts/check-coverage.sh

# 输出包括：
# - 测试执行结果
# - 覆盖率百分比
# - 阈值检查
# - 测试类别分析
# - 质量建议
```

### 2. 测试报告生成 (`generate-test-report.py`)
```python
# 生成详细测试报告
python scripts/generate-test-report.py /path/to/project

# 生成文件：
# - test-report.json (JSON格式)
# - test-report.html (HTML可视化)
```

### 3. 测试数据生成 (`generate-test-data.py`)
```python
# 生成完整测试数据
python scripts/generate-test-data.py /path/to/project

# 生成文件：
# - test-data.sql (SQL数据)
# - test-data.json (JSON数据)
# - test-data.yml (YAML配置)
# - TestDataFactory.java (Java工厂类)
```

## 📚 参考文档

### 1. 依赖配置 (`references/dependencies.md`)
- Maven依赖完整配置
- 测试环境配置
- 版本兼容性说明

### 2. 测试策略 (`references/testing-strategies.md`)
- 测试分层架构
- 测试设计原则
- 执行策略优化

### 3. 异常测试 (`references/exception-patterns.md`)
- 异常分类体系
- 异常测试模式
- 最佳实践指南

### 4. 边界测试 (`references/boundary-testing.md`)
- 边界值概念
- 测试方法
- 各种边界类型详解

## 🎨 最佳实践

### 1. 测试命名规范
```java
// Given-When-Then格式
test[方法名]_[条件]_[期望结果]

// 示例
testGetUserById_Success()
testCreateUser_InvalidEmail_ThrowsException()
testUpdateUser_NotFound_Returns404()
```

### 2. 测试结构
```java
@Test
void testMethod() {
    // 1. Given - 准备测试数据
    when(mock.method()).thenReturn(result);
    
    // 2. When - 执行测试方法
    Object actual = service.method();
    
    // 3. Then - 验证结果
    assertThat(actual).isEqualTo(expected);
    verify(mock, times(1)).method();
}
```

### 3. 测试数据管理
```java
// 使用TestDataFactory
User user = TestDataFactory.createNormalUser();
User boundaryUser = TestDataFactory.createBoundaryUser();
User invalidUser = TestDataFactory.createInvalidUser();

// 使用@Sql导入
@Sql("/test-data.sql")
@Test
void testWithData() {
    // 测试方法
}
```

## 🔍 故障排除

### 常见问题

1. **事务不回滚**
   ```java
   // 确保使用@Transactional
   @Test
   @Transactional
   void testWithTransaction() {
       // 测试代码
   }
   ```

2. **Mock不生效**
   ```java
   // Service测试使用@Mock
   @Mock
   private UserMapper userMapper;
   
   // Controller测试使用@MockBean
   @MockBean
   private UserService userService;
   ```

3. **测试数据污染**
   ```java
   // 使用@Transactional自动回滚
   // 或使用@AfterEach清理
   @AfterEach
   void tearDown() {
       cleanupTestData();
   }
   ```

### 调试技巧

1. **启用详细日志**
   ```yaml
   logging:
     level:
       com.example.demo: DEBUG
       org.springframework: DEBUG
   ```

2. **打印请求详情**
   ```java
   mockMvc.perform(get("/api/users/1"))
       .andDo(print());  // 打印请求响应详情
   ```

## 📈 质量保证

### 1. 持续集成
```yaml
# GitHub Actions示例
name: Test Coverage
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests with coverage
        run: |
          mvn clean test jacoco:report
          ./scripts/check-coverage.sh
```

### 2. 质量门禁
```xml
<!-- JaCoCo质量门禁 -->
<configuration>
    <rules>
        <rule>
            <element>BUNDLE</element>
            <limits>
                <limit>
                    <counter>LINE</counter>
                    <value>COVEREDRATIO</value>
                    <minimum>0.85</minimum>
                </limit>
            </limits>
        </rule>
    </rules>
</configuration>
```

## 🚀 扩展定制

### 1. 自定义测试注解
```java
// 创建组合注解
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@MybatisTest
@AutoConfigureTestDatabase
@Sql("/test-data.sql")
public @interface MybatisIntegrationTest {
}
```

### 2. 测试工具扩展
```java
// 自定义断言
public class CustomAssertions {
    public static void assertUserEquals(User expected, User actual) {
        assertThat(actual.getUsername()).isEqualTo(expected.getUsername());
        assertThat(actual.getEmail()).isEqualTo(expected.getEmail());
    }
}
```

### 3. 性能优化
```java
// 测试分组
@Tag("fast")
@Test
void testFastOperation() { ... }

@Tag("slow")  
@Test
void testSlowOperation() { ... }
```

## 📋 使用示例

当需要为Spring Boot项目编写单元测试时：

1. **分析项目结构** - 识别Entity、Mapper、Service、Controller
2. **选择测试策略** - 根据需求选择正常/异常/边界测试
3. **生成测试代码** - 使用模板生成对应层的测试
4. **配置测试环境** - 设置依赖、数据、配置
5. **验证测试覆盖** - 检查覆盖率，补充缺失测试

## 📞 支持

### 问题反馈
1. 检查参考文档中的解决方案
2. 运行诊断脚本检查配置
3. 查看生成的测试报告

### 功能建议
1. 扩展测试覆盖类型
2. 添加新的测试工具
3. 优化测试执行性能

## 📄 许可证

本Skill遵循MIT许可证，可自由使用、修改和分发。

## 🙏 致谢

感谢所有为Spring Boot测试生态系统做出贡献的开发者。

---

**记住**: 好的测试是高质量代码的基石。通过本Skill，您可以确保您的Spring Boot项目具有专业级的测试覆盖！

---

## 📤 发布到ClawHub

### 发布准备

本Skill已配置完整的发布文件：

1. **clawhub.yml** - ClawHub发布配置文件
2. **package.json** - 标准化包描述文件
3. **LICENSE** - MIT许可证
4. **完整的目录结构** - 包含脚本、参考文档、示例

### 发布步骤

#### 步骤1：创建GitHub仓库（推荐）
```bash
# 初始化Git仓库
git init
git add .
git commit -m "feat: Spring Boot单元测试Skill v1.0.0"
git branch -M main

# 在GitHub创建新仓库，然后：
git remote add origin https://github.com/your-username/springboot-unit-testing.git
git push -u origin main
```

#### 步骤2：创建发布包
```bash
# 打包整个Skill目录
tar -czf springboot-unit-testing-skill-v1.0.0.tar.gz test-skill/

# 或使用zip
zip -r springboot-unit-testing-skill-v1.0.0.zip test-skill/
```

#### 步骤3：在ClawHub发布
1. 访问 [ClawHub网站](https://clawhub.com)
2. 注册/登录开发者账户
3. 进入"发布Skill"页面
4. 填写Skill信息：
   - **名称**: springboot-unit-testing
   - **版本**: 1.0.0
   - **描述**: 专业的Spring Boot + MyBatis + MySQL项目单元测试Skill
   - **分类**: 开发工具 / 测试框架
   - **标签**: spring-boot, mybatis, unit-testing, java, junit, mockito
   - **许可证**: MIT
5. 上传打包文件
6. 提交审核

#### 步骤4：维护和更新
- 定期收集用户反馈
- 更新测试策略和最佳实践
- 发布新版本时更新changelog
- 保持文档的最新性

### 发布检查清单

✅ **文件完整性**
- [x] SKILL.md (主技能文件)
- [x] README.md (使用文档)
- [x] scripts/ (3个实用脚本)
- [x] references/ (4个参考文档)
- [x] examples/ (示例代码)
- [x] assets/ (资源文件夹)

✅ **配置完整**
- [x] clawhub.yml (发布配置)
- [x] package.json (包管理)
- [x] LICENSE (许可证)
- [x] 测试数据文件

✅ **质量保证**
- [x] 测试策略文档齐全
- [x] 代码示例完整可运行
- [x] 工具脚本可用
- [x] 依赖配置正确

### 发布后推广

1. **文档推广**: 确保README清晰易懂
2. **社区分享**: 在相关技术社区分享
3. **用户反馈**: 积极收集用户建议
4. **版本迭代**: 根据反馈持续改进

### 联系方式

- **GitHub**: https://github.com/your-username/springboot-unit-testing
- **Issue跟踪**: 使用GitHub Issues
- **Pull Request**: 欢迎贡献改进

---

**🚀 现在您的Skill已经准备好发布到ClawHub，与全球的Spring Boot开发者分享专业的单元测试解决方案！**