#pragma once

// 使用例子：
// Singleton::getInst().doSomething();

class Singleton {
public:
    // 获取单例实例的静态方法
    // C++11 起，静态局部变量的初始化是线程安全的 (Meyers' Singleton)
    static Singleton& getInst();

    // 示例业务方法
    void doSomething();

    // 删除拷贝构造函数和赋值运算符，防止复制
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;

private:
    // 私有构造函数，防止外部实例化
    Singleton() = default;
    ~Singleton() = default;
};

// 或者，如果一个类只需要一个全局实例，可以使用全局实例的方式实现单例模式，示例如下：
// 单例类只用 .h 文件里面 放一个 `extern class classType Global<name>Inst;` 这种方式
// （在 .cpp 里面去声明 `class classType Global<name>Inst;`），之后全局调用 `Global<name>Inst` 即可。
//
// ! WARN: 此方式有“静态初始化顺序问题”（SIOF）风险：
// 如果另一个翻译单元的静态/全局对象在构造时使用该全局实例，
// 而该实例可能尚未构造完成，将导致未定义行为。
// 推荐优先使用上述 Meyers' Singleton（函数局部静态变量）来避免此问题。
