#pragma once

#include <memory>

/**
 * @brief GenericModule 接口类
 * 对外暴露该模块的功能，隐藏具体实现。
 */
class GenericModule {
public:
    // 工厂方法，用于创建模块实例
    static std::shared_ptr<GenericModule> Create();

    virtual ~GenericModule() = default;

    // 通用的生命周期控制接口
    virtual int Init() = 0;
    virtual bool getIsInited() = 0;
    virtual int Deinit() = 0;

    // 通用的业务接口示例
    virtual void DoTask() = 0;
};
