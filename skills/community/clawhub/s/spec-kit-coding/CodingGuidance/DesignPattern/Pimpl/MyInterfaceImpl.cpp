#include "MyInterface.h"

// ========= MyInterface 的具体声明 =========

// 这里可以引用包含一些具体的其它头文件依赖

struct MyInterface::Impl {
    int publicApi1();
    int publicApi2();
};

int MyInterface::Impl::publicApi1()
{
    return 42;
}

int MyInterface::Impl::publicApi2()
{
    return 84;
}

// ========= MyInterface 的具体实现 =========
// 基本上就是把 Impl 的方法调用转发过去。

MyInterface::MyInterface()
    : mImpl(std::make_unique<Impl>())
{
}

MyInterface::~MyInterface() = default;

MyInterface::MyInterface(MyInterface&&) noexcept = default;
MyInterface& MyInterface::operator=(MyInterface&&) noexcept = default;

int MyInterface::publicApi1() { return mImpl->publicApi1(); }

int MyInterface::publicApi2() { return mImpl->publicApi2(); }
