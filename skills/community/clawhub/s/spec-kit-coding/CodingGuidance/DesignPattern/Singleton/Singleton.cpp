#include <iostream>

#include "Singleton.h"

Singleton& Singleton::getInst() {
    // 静态局部变量，第一次调用时初始化，程序结束时销毁
    // C++11 标准保证了并发环境下的线程安全性
    static Singleton instance;
    return instance;
}

void Singleton::doSomething() {
    std::cout << "Singleton instance address: " << this << " is doing something." << std::endl;
}
