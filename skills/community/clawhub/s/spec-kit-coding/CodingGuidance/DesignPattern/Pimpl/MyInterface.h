#pragma once

// 减少头文件包含链，大型项目编译优化。
// 隐藏第三方库依赖，减少编译依赖和暴露的实现细节。
#include <memory>

class MyInterface {
public:
    MyInterface();

    // 析构函数必须在头文件声明、在 .cpp 中定义（即使 = default）。
    // 原因：unique_ptr<Impl> 的删除器需要 Impl 为完整类型，
    // 而头文件中 Impl 仅有前置声明，编译器生成的内联析构会编译失败。
    ~MyInterface();

    // 移动语义：同理需要在 .cpp 中定义，因为移动操作涉及 unique_ptr 的析构/转移。
    // 若不声明，由于用户声明了析构函数，编译器不会自动生成移动构造/赋值。
    MyInterface(MyInterface&&) noexcept;
    MyInterface& operator=(MyInterface&&) noexcept;

    // 拷贝禁用（unique_ptr 天然不可拷贝，显式声明更清晰）
    MyInterface(const MyInterface&) = delete;
    MyInterface& operator=(const MyInterface&) = delete;

    // 只暴露公共API。
    // 用于第三方API封装。

    int publicApi1();
    int publicApi2();

private:

    // 这个暴露公共API的头文件中不包含任何成员变量。
    // 修改 Impl 的实现不会引起 MyInterface 的重新编译，接口稳定。

    struct Impl;
    std::unique_ptr<Impl> mImpl;
};
