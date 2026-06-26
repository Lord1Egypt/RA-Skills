#pragma once

// 对于某一类产品的复杂对象构建，使用建造者/工厂模式（这里混合了常见的教程里面的概念）
// 一类产品应对应一个Builder类，负责该类产品的各个部分的设置和产品类的创建
// 并可灵活的增减和修改产品的设置和内部实现

// 其中 "// ..." 表示可以继续扩展的部分，而其余部分基本都是固定的可以不动。

// 函数执行返回值约定：
//      0 表示成功
//    < 0 表示失败
//    > 0 表示警告

// 注意这个模板里面的类的公共 API 没有提供 线程安全措施，按需添加

#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cmath>
#include <memory>
#include <string>

// ========= 所有类型产品可以有一个共同的基类 =========

class ObjectBasic {
public:
    ObjectBasic() = default;
    virtual ~ObjectBasic() = default;

protected:
    size_t mId = 0;
    // ...
};

// ========= 某一类产品的抽象类的定义 =========

enum class ProductType {
    ProductA,
    ProductB,

    // 可扩展更多产品类型
    // ...
};

// 产品的各个设置项，必须包含所有，方便 Builder 设置，以及未来的类实例的克隆等作用
struct ProductSettings {

    ProductType type = ProductType::ProductA;

    // 基本设置项
    // 需要都写上默认值
    int32_t partA = 0;
    double partB = 0.0;
    std::string partC = "";
    // ...

    // 如果设置项有自定义类型，则需要提供该类型的判断相等等基础操作符重载

    // 基础操作符设施
    // 重置，赋值运算符，等号运算符，等

    void reset() {
        // 重置为默认值，或者根据需要设置为某个特定的值
        partA = 0;
        partB = 0.0;
        partC.clear();
        // ...
    }

    bool operator==(const ProductSettings& other) const {
        constexpr double epsilon = 1e-9;
        return ( ( partA == other.partA ) &&
                 // for double comparison, consider using an epsilon for floating-point comparison
                 ( std::fabs(partB - other.partB) < epsilon ) &&
                 ( partC == other.partC ) );
                 // ...
    }
};

#define HANDLE_RET(ret, fun, retIs0ThanExec, retSmallThanExec, retLargerThanExec) \
    ret = fun;                  \
    if (ret == 0) {             \
        retIs0ThanExec          \
    } else if (ret < 0) {       \
        retSmallThanExec        \
    } else {                    \
        retLargerThanExec       \
    }

#define SET_GET_PART_IMPL(funPartName, varPartName, partType, updateFunc, printFunc) \
    virtual int32_t set##funPartName(const partType& value) {  \
        if (!(varPartName == value)) {                  \
            auto oldVal_ = varPartName;                 \
            varPartName = value;                        \
            int ret = -1;                               \
            HANDLE_RET(                                 \
                ret , updateFunc ,                      \
                return 0; ,                             \
                printFunc(#updateFunc " failed, ret=%d\n", ret); \
                varPartName = oldVal_;                  \
                return ret; ,                            \
                printFunc(#updateFunc " warning, ret=%d\n", ret); \
                return ret;                             \
            )                                           \
        }                                               \
        return 0;                                       \
    }                                                   \
    virtual partType get##funPartName() const {                 \
        return varPartName;                             \
    }

class ProductBasic : public ObjectBasic {
public:
    ProductBasic() = default;
    virtual ~ProductBasic() = default;

    // 注意如果这些 API 需要多线程使用，则需要加锁保护

    // 这里仅仅设置和获取设置值，但不生效。可以用于"克隆"来自另一个实例的设置值
    SET_GET_PART_IMPL(Settings, mSettings, ProductSettings, 0, printf); // 打印函数按需修改

    // 公共的设置项
    // 设置和获取各个部分的值，并立即生效
    // 用于单独设置某个部分，操作细节
    SET_GET_PART_IMPL(PartA, mSettings.partA, int32_t, updatePartA(), printf);
    SET_GET_PART_IMPL(PartB, mSettings.partB, double, updatePartB(), printf);
    SET_GET_PART_IMPL(PartC, mSettings.partC, std::string, updatePartC(), printf);
    // ...

    // 根据最新的 mSettings 进行整体更新，使所有设置生效（进行设置项生效，运行、显示等）。
    // 里面写上所有设置值生效函数。
    // 用于创造新实例并填入所有设置值后的一次整体更新
    // 或批量设置后再生效，减少重复更新开销
    virtual int32_t makeSettingsAvailable() {

        int32_t ret = -1;
        int32_t warnCount = 0;

        HANDLE_RET(
            ret , updatePartA() ,
            ,
            printf("updatePartA() failed, ret=%d\n", ret);
            return ret; ,
            printf("updatePartA() warning, ret=%d\n", ret);
            warnCount++;
            );

        HANDLE_RET(
            ret , updatePartB() ,
            ,
            printf("updatePartB() failed, ret=%d\n", ret);
            return -1; ,
            printf("updatePartB() warning, ret=%d\n", ret);
            warnCount++;
            );

        HANDLE_RET(
            ret , updatePartC() ,
            ,
            printf("updatePartC() failed, ret=%d\n", ret);
            return -1; ,
            printf("updatePartC() warning, ret=%d\n", ret);
            warnCount++;
            );

        // ...

        return warnCount > 0 ? 1 : 0;
    }

    // 一些公共的纯虚函数接口，由具体产品类实现
    virtual void doSomething() = 0;
    // ...

protected:
    ProductSettings mSettings;

    // 实际更新各个部分的虚函数，由具体产品类实现
    virtual int32_t updatePartA() = 0;
    virtual int32_t updatePartB() = 0;
    virtual int32_t updatePartC() = 0;
    // ...
};

class ProductNextBasic : public ObjectBasic {
    // ...
};

// ========= 具体产品类的定义 =========
// 最好每个具体产品类单独放在一个头文件和源文件中（这里只留前置声明）。
// 可以用 Pimpl 模式隐藏实现细节（这里没有，对于只暴露头文件的情况需要用）。

class ProductAConcrete : public ProductBasic {
public:
    ProductAConcrete(const ProductSettings& settings) {
        mSettings = settings;
    }
    ~ProductAConcrete() override = default;

    void doSomething() override {
        // 具体实现
    }

    // ...

protected:
    int32_t updatePartA() override {
        // 具体实现
        // 根据 mSettings.partA 的值更新部分 A
        return 0;
    }

    int32_t updatePartB() override {
        // 具体实现
        // 根据 mSettings.partB 的值更新部分 B
        return 0;
    }

    int32_t updatePartC() override {
        // 具体实现
        // 根据 mSettings.partC 的值更新部分 C
        return 0;
    }

    // ...

private:
    // 具体产品类的私有成员变量

    // 如果新增新的设置项，需要在这里添加对应的成员变量的 updatePartX() 实现
    // 并添加对应设置项的 SET_GET_PART_IMPL(PartX, mSettings.PartX, std::string, updatePartX(), printf);
    // 并重写 makeSettingsAvailable()，里面先调用 ProductBasic::makeSettingsAvailable()，再调用这些新增的 updatePartX() 方法
};

class ProductBConcrete : public ProductBasic {
public:
    ProductBConcrete(const ProductSettings& settings) {
        mSettings = settings;
    }
    ~ProductBConcrete() override = default;

    void doSomething() override {
        // 具体实现
    }

    // ...

protected:
    int32_t updatePartA() override {
        // 具体实现
        // 根据 mSettings.partA 的值更新部分 A
        return 0;
    }
    int32_t updatePartB() override {
        // 具体实现
        // 根据 mSettings.partB 的值更新部分 B
        return 0;
    }

    int32_t updatePartC() override {
        // 具体实现
        // 根据 mSettings.partC 的值更新部分 C
        return 0;
    }

    // ...
};

// ========= ProductBuilder 类 =========
class ProductBuilder {
public:
    ProductBuilder() = default;
    virtual ~ProductBuilder() = default;

    std::shared_ptr<ProductBasic> createProduct(const ProductSettings& settings) {
        switch (settings.type) {
            case ProductType::ProductA:
                return std::make_shared<ProductAConcrete>(settings);
            case ProductType::ProductB:
                return std::make_shared<ProductBConcrete>(settings);
            // 可扩展更多产品类型
            // ...
            default:
                printf("Unknown ProductType: %d\n", static_cast<int>(settings.type));
                return nullptr;
        }
    }
};

// 使用例子：
// ProductBuilder builder;
// auto productA = builder.createProduct(
//     ProductSettings{
//         .type = ProductType::ProductA,
//         .partA = 10,
//         .partB = 20.5,
//         .partC = "ExampleA"
//     }
// );
// 创建的多个产品实例，可以用 ToolBox/GeneralContainer（暂未开源） 来管理。
//    简单的就用 std::vector 之类的容器 添加到 ProductBuilder 类里面 进行管理。
// 创建多个不同设置的产品实例之后，统一调用 makeSettingsAvailable() 使批量设置生效（重要）。

#undef HANDLE_RET
#undef SET_GET_PART_IMPL
