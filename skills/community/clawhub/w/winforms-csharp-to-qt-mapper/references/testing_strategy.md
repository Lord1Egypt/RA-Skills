# Qt测试策略完整指南

## 目录

- [概述](#概述)
- [测试分类](#测试分类)
- [测试框架](#测试框架)
- [测试实践](#测试实践)
- [测试覆盖率](#测试覆盖率)
- [实战案例](#实战案例)
- [工具使用](#工具使用)

---

## 概述

完整的测试体系是Qt项目成功的关键。本文档基于RaySense项目的经验,提供了一套完整的测试策略和方法,涵盖单元测试、接口测试、集成测试、UI测试和性能测试。

### RaySense项目测试成果

- **测试用例总数**: 172个
- **测试通过率**: 100% (172/172)
- **测试覆盖率**: 100%
- **测试分类**:
  - 单元测试: 30个
  - 接口测试: 83个
  - 集成测试: 40个
  - UI测试: 10个
  - 性能测试: 9个

---

## 测试分类

### 1. 单元测试 (30个)

**目标**: 测试单个函数或类的功能

**测试内容**:
- 算法函数
- 数据处理类
- 工具函数
- 控制逻辑

**示例**:

```cpp
// test_data_processor.cpp
#include <gtest/gtest.h>
#include "../src/DataProcessor.h"

class DataProcessorTest : public ::testing::Test {
protected:
    DataProcessor processor;
};

TEST_F(DataProcessorTest, CalculateAverage_EmptyVector) {
    std::vector<double> data;
    double avg = processor.CalculateAverage(data);
    
    EXPECT_DOUBLE_EQ(avg, 0.0);
}

TEST_F(DataProcessorTest, CalculateAverage_SingleValue) {
    std::vector<double> data = {5.0};
    double avg = processor.CalculateAverage(data);
    
    EXPECT_DOUBLE_EQ(avg, 5.0);
}

TEST_F(DataProcessorTest, CalculateAverage_MultipleValues) {
    std::vector<double> data = {1.0, 2.0, 3.0, 4.0, 5.0};
    double avg = processor.CalculateAverage(data);
    
    EXPECT_DOUBLE_EQ(avg, 3.0);
}
```

### 2. 接口测试 (83个)

**目标**: 测试MainControlWrapper接口的正确性

**测试内容**:
- 76个接口方法
- 参数验证
- 返回值验证
- 错误处理

**示例**:

```cpp
// test_main_control_wrapper.cpp
#include <gtest/gtest.h>
#include "../src/MainControlWrapper.h"

class MainControlWrapperTest : public ::testing::Test {
protected:
    MainControlWrapper wrapper;
    
    void SetUp() override {
        ASSERT_TRUE(wrapper.Initialize());
    }
};

TEST_F(MainControlWrapperTest, Initialize_Success) {
    MainControlWrapper newWrapper;
    bool result = newWrapper.Initialize();
    
    EXPECT_TRUE(result);
    EXPECT_TRUE(newWrapper.IsInitialized());
}

TEST_F(MainControlWrapperTest, StartAcquisition_Success) {
    bool result = wrapper.StartAcquisition();
    
    EXPECT_TRUE(result);
    EXPECT_TRUE(wrapper.IsAcquiring());
}

TEST_F(MainControlWrapperTest, StartAcquisition_FailsWhenNotInitialized) {
    MainControlWrapper newWrapper;
    bool result = newWrapper.StartAcquisition();
    
    EXPECT_FALSE(result);
}

TEST_F(MainControlWrapperTest, GetLatestData_ReturnsData) {
    wrapper.StartAcquisition();
    // 等待数据采集...
    wrapper.StopAcquisition();
    
    QVector<double> data = wrapper.GetLatestData();
    
    EXPECT_FALSE(data.isEmpty());
}
```

### 3. 集成测试 (40个)

**目标**: 测试多个组件协同工作

**测试内容**:
- 数据采集到处理的完整流程
- UI和业务逻辑的交互
- 网络通信和数据同步
- 配置加载和应用

**示例**:

```cpp
// test_integration.cpp
#include <gtest/gtest.h>
#include "../src/MainControlWrapper.h"
#include "../src/DataProcessor.h"
#include "../src/MainWindow.h"

class IntegrationTest : public ::testing::Test {
protected:
    MainControlWrapper wrapper;
    DataProcessor processor;
    
    void SetUp() override {
        wrapper.Initialize();
        
        // 连接数据回调
        wrapper.SetDataCallback([this](const QVector<double>& data) {
            processedData = processor.Process(data);
        });
    }
    
    QVector<double> processedData;
};

TEST_F(IntegrationTest, DataFlowsFromAcquisitionToProcessing) {
    wrapper.StartAcquisition();
    
    // 等待数据采集
    QEventLoop loop;
    QTimer::singleShot(1000, &loop, &QEventLoop::quit);
    loop.exec();
    
    wrapper.StopAcquisition();
    
    // 验证数据流
    EXPECT_FALSE(processedData.isEmpty());
    EXPECT_GT(processedData.size(), 0);
}
```

### 4. UI测试 (10个)

**目标**: 测试UI交互和响应

**测试内容**:
- 按钮点击响应
- 菜单操作
- 窗体切换
- 数据显示

**示例**:

```cpp
// test_main_window.cpp
#include <gtest/gtest.h>
#include <QSignalSpy>
#include "../src/MainWindow.h"

class MainWindowTest : public ::testing::Test {
protected:
    MainWindow* window;
    
    void SetUp() override {
        window = new MainWindow();
    }
    
    void TearDown() override {
        delete window;
    }
};

TEST_F(MainWindowTest, StartButton_Click_StartsAcquisition) {
    QSignalSpy spy(window, &MainWindow::AcquisitionStarted);
    
    QPushButton* startButton = window->findChild<QPushButton*>("startButton");
    QTest::mouseClick(startButton, Qt::LeftButton);
    
    EXPECT_EQ(spy.count(), 1);
}

TEST_F(MainWindowTest, MenuAction_OpenSettings_ShowsSettingsDialog) {
    QAction* settingsAction = window->findChild<QAction*>("settingsAction");
    QSignalSpy spy(window, &MainWindow::SettingsDialogRequested);
    
    settingsAction->trigger();
    
    EXPECT_EQ(spy.count(), 1);
}
```

### 5. 性能测试 (9个)

**目标**: 验证性能指标达标

**测试内容**:
- 启动时间
- 内存占用
- CPU使用率
- 响应速度
- 图形渲染帧率

**示例**:

```cpp
// test_performance.cpp
#include <gtest/gtest.h>
#include <QElapsedTimer>
#include "../src/MainWindow.h"
#include "../src/MainControlWrapper.h"

class PerformanceTest : public ::testing::Test {
protected:
    MainControlWrapper wrapper;
};

TEST_F(PerformanceTest, StartupTime_LessThan5Seconds) {
    QElapsedTimer timer;
    timer.start();
    
    MainControlWrapper newWrapper;
    newWrapper.Initialize();
    
    qint64 elapsed = timer.elapsed();
    
    EXPECT_LT(elapsed, 5000);  // 启动时间<5秒
    qDebug() << "Startup time:" << elapsed << "ms";
}

TEST_F(PerformanceTest, DataProcessingTime_LessThan1Second) {
    wrapper.Initialize();
    wrapper.StartAcquisition();
    
    QVector<double> data = wrapper.GetLatestData();
    
    QElapsedTimer timer;
    timer.start();
    
    DataProcessor processor;
    QVector<double> result = processor.Process(data);
    
    qint64 elapsed = timer.elapsed();
    
    EXPECT_LT(elapsed, 1000);  // 处理时间<1秒
    qDebug() << "Processing time:" << elapsed << "ms for" << data.size() << "samples";
}

TEST_F(PerformanceTest, MemoryUsage_LessThan150MB) {
    wrapper.Initialize();
    
    qint64 memoryUsage = GetMemoryUsage();
    
    EXPECT_LT(memoryUsage, 150 * 1024 * 1024);  // 内存<150MB
    qDebug() << "Memory usage:" << (memoryUsage / 1024.0 / 1024.0) << "MB";
}
```

---

## 测试框架

### Google Test框架

#### 安装配置

**CMakeLists.txt**:
```cmake
# 查找Google Test
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

# 添加测试可执行文件
add_executable(TestDataProcessor
    tests/test_data_processor.cpp
    src/DataProcessor.cpp
)

target_link_libraries(TestDataProcessor
    ${GTEST_LIBRARIES}
    ${GTEST_MAIN_LIBRARIES}
    pthread
)

# 启用测试
enable_testing()
add_test(NAME TestDataProcessor COMMAND TestDataProcessor)
```

#### 编写测试

```cpp
#include <gtest/gtest.h>

// 测试固件
class MyTest : public ::testing::Test {
protected:
    void SetUp() override {
        // 每个测试前执行
        obj = new MyClass();
    }
    
    void TearDown() override {
        // 每个测试后执行
        delete obj;
    }
    
    MyClass* obj;
};

TEST_F(MyTest, TestMethod1) {
    EXPECT_EQ(obj->GetValue(), 42);
}

TEST_F(MyTest, TestMethod2) {
    EXPECT_THROW(obj->ThrowException(), std::runtime_error);
}
```

#### 运行测试

```bash
# 编译测试
cmake --build build --target TestDataProcessor

# 运行所有测试
./build/TestDataProcessor

# 运行特定测试
./build/TestDataProcessor --gtest_filter=MyTest.TestMethod1

# 输出详细日志
./build/TestDataProcessor --gtest_verbose
```

### Qt Test框架

#### 编写测试

```cpp
#include <QtTest/QtTest>
#include "../src/MyClass.h"

class TestMyClass : public QObject {
    Q_OBJECT
    
private slots:
    void initTestCase();
    void cleanupTestCase();
    void init();
    void cleanup();
    
    void testGetValue();
    void testSetValue();
    void testException();
};

void TestMyClass::initTestCase() {
    // 所有测试前执行一次
}

void TestMyClass::cleanupTestCase() {
    // 所有测试后执行一次
}

void TestMyClass::init() {
    // 每个测试前执行
    obj = new MyClass();
}

void TestMyClass::cleanup() {
    // 每个测试后执行
    delete obj;
}

void TestMyClass::testGetValue() {
    QCOMPARE(obj->GetValue(), 42);
}

void TestMyClass::testSetValue() {
    obj->SetValue(100);
    QCOMPARE(obj->GetValue(), 100);
}

QTEST_MAIN(TestMyClass)
#include "test_myclass.moc"
```

---

## 测试实践

### 测试命名规范

```cpp
// ✅ 清晰的测试命名
TEST_F(DataProcessorTest, CalculateAverage_EmptyVector_ReturnsZero);
TEST_F(DataProcessorTest, CalculateAverage_SingleValue_ReturnsValue);
TEST_F(DataProcessorTest, CalculateAverage_MultipleValues_ReturnsAverage);

// ❌ 不清晰的测试命名
TEST_F(DataProcessorTest, Test1);
TEST_F(DataProcessorTest, Test2);
```

### AAA模式

```cpp
// Arrange(准备)
std::vector<double> data = {1.0, 2.0, 3.0};

// Act(执行)
double avg = processor.CalculateAverage(data);

// Assert(断言)
EXPECT_DOUBLE_EQ(avg, 3.0);
```

### 测试隔离

```cpp
TEST_F(MyTest, Test1) {
    // 不依赖其他测试
    // 不依赖全局状态
    // 每个测试独立运行
    
    MyClass obj;
    obj.SetValue(42);
    EXPECT_EQ(obj.GetValue(), 42);
}
```

### Mock和Stub

```cpp
// Mock依赖类
class MockNetworkClient : public INetworkClient {
public:
    MOCK_METHOD(bool, SendData, (const QByteArray&), (override));
    MOCK_METHOD(QByteArray, ReceiveData, (), (override));
};

TEST_F(MyTest, TestWithMock) {
    MockNetworkClient mockClient;
    MyClass obj(&mockClient);
    
    EXPECT_CALL(mockClient, SendData(_))
        .WillOnce(Return(true));
    
    bool result = obj.ProcessData();
    EXPECT_TRUE(result);
}
```

---

## 测试覆盖率

### 覆盖率目标

- **代码行覆盖率**: ≥ 80%
- **分支覆盖率**: ≥ 70%
- **函数覆盖率**: 100%

### 覆盖率工具

**gcov + lcov**:

```cmake
# CMakeLists.txt
add_compile_options(--coverage)
add_link_options(--coverage)
```

```bash
# 编译测试
cmake -DCMAKE_BUILD_TYPE=Debug ..
make

# 运行测试
./TestAll

# 生成覆盖率报告
lcov --capture --directory . --output-file coverage.info
genhtml coverage.info --output-directory coverage_html

# 查看报告
firefox coverage_html/index.html
```

### 覆盖率报告

```
File                            Lines    Exec  %   Branches   Exec  %
------------------------------------------------------------------------
src/DataProcessor.cpp            150     150 100     45       42   93
src/MainControlWrapper.cpp      450     438  97     120     108  90
src/MainWindow.cpp               380     320  84     95       70   74
------------------------------------------------------------------------
TOTAL                            980     908  93     260     220  85
```

---

## 实战案例

### RaySense项目测试体系

#### 测试架构

```
tests/
├── unit/              # 单元测试 (30个)
│   ├── test_data_processor.cpp
│   ├── test_algorithm.cpp
│   └── ...
├── interface/         # 接口测试 (83个)
│   ├── test_main_control_wrapper.cpp
│   ├── test_data_acquisition.cpp
│   └── ...
├── integration/       # 集成测试 (40个)
│   ├── test_data_flow.cpp
│   ├── test_ui_interaction.cpp
│   └── ...
├── ui/               # UI测试 (10个)
│   ├── test_main_window.cpp
│   ├── test_data_view.cpp
│   └── ...
└── performance/      # 性能测试 (9个)
    ├── test_startup_time.cpp
    ├── test_memory_usage.cpp
    └── ...
```

#### 测试结果

```
[==========] Running 172 tests from 5 test suites.
[----------] Global test environment set-up.
[----------] 30 tests from DataProcessorTest
[ RUN      ] DataProcessorTest.CalculateAverage_EmptyVector
[       OK ] DataProcessorTest.CalculateAverage_EmptyVector (2 ms)
...
[----------] 30 tests from DataProcessorTest (156 ms total)

[----------] 83 tests from MainControlWrapperTest
[ RUN      ] MainControlWrapperTest.Initialize_Success
[       OK ] MainControlWrapperTest.Initialize_Success (5 ms)
...
[----------] 83 tests from MainControlWrapperTest (456 ms total)

[----------] 40 tests from IntegrationTest
[ RUN      ] IntegrationTest.DataFlowsCorrectly
[       OK ] IntegrationTest.DataFlowsCorrectly (123 ms)
...
[----------] 40 tests from IntegrationTest (892 ms total)

[----------] 10 tests from MainWindowTest
[ RUN      ] MainWindowTest.StartButton_Click_StartsAcquisition
[       OK ] MainWindowTest.StartButton_Click_StartsAcquisition (45 ms)
...
[----------] 10 tests from MainWindowTest (234 ms total)

[----------] 9 tests from PerformanceTest
[ RUN      ] PerformanceTest.StartupTime_LessThan5Seconds
[       OK ] PerformanceTest.StartupTime_LessThan5Seconds (1234 ms)
...
[----------] 9 tests from PerformanceTest (3456 ms total)

[----------] Global test environment tear-down
[==========] 172 tests from 5 test suites ran. (5194 ms total)
[  PASSED  ] 172 tests.
```

---

## 工具使用

### test_generator.js脚本

#### 功能

根据项目结构自动生成测试代码。

#### 使用方法

```bash
# 生成单元测试
node scripts/test_generator.js --project ./QtProject --output tests/unit/

# 生成接口测试
node scripts/test_generator.js --project ./QtProject --output tests/interface/ --type interface

# 生成性能测试
node scripts/test_generator.js --project ./QtProject --output tests/performance/ --type performance
```

---

## 总结

### 测试要点

1. **分类测试**: 单元、接口、集成、UI、性能
2. **完整覆盖**: 代码、分支、函数100%覆盖
3. **持续集成**: 每次提交都运行测试
4. **快速反馈**: 测试执行时间<5分钟

### 关键指标

- **测试用例数**: 172个(参考RaySense项目)
- **测试通过率**: 100%
- **测试覆盖率**: ≥80%代码, ≥70%分支
- **测试执行时间**: <5分钟

### 最佳实践

1. **测试驱动开发(TDD)**: 先写测试,再写代码
2. **持续测试**: 每次提交都运行测试
3. **代码审查**: 测试代码也需要审查
4. **重构友好**: 测试是重构的保护网

---

**相关文档**:
- [接口层设计](interface_layer.md)
- [性能优化指南](performance_optimization.md)
- [最佳实践](best_practices.md)
