#pragma once

#include "../include/GenericModule.h"
#include <atomic>
#include <shared_mutex>

/**
 * @brief 模块生命周期状态枚举
 *
 * 状态转换图：
 *   Uninitialized → Initializing → Initialized → Deinitializing → Uninitialized
 *
 * 使用 atomic + compare_exchange_strong 实现无锁状态转换，
 * 天然防止并发重复 Init/Deinit，无需额外 mutex。
 */
enum class ModuleState : int {
    Uninitialized,    ///< 未初始化（初始状态）
    Initializing,     ///< 正在初始化中（防止并发重入）
    Initialized,      ///< 已初始化，可正常工作
    Deinitializing    ///< 正在反初始化中（防止并发重入）
};

/**
 * @brief GenericModule 接口的私有实现类
 * 包含真正的内部状态逻辑或具体的业务依赖。
 */
class GenericModuleImpl : public GenericModule {
public:
    GenericModuleImpl();
    ~GenericModuleImpl() override;

    // 实现声明的生命周期接口
    int Init() override;
    bool getIsInited() override;
    int Deinit() override;

    // 实现声明的通用业务接口
    void DoTask() override;

private:
    // 模块生命周期状态，原子操作保证线程安全的状态转换
    std::atomic<ModuleState> mInitState{ModuleState::Uninitialized};

    // 读写锁，供 Init/Deinit/DoTask 内部业务逻辑按需使用
    mutable std::shared_mutex mMutex;
    // 也可以改为 使用 std::recursive_mutex，如果 Init/Deinit/DoTask 内部可能会有递归调用的情况

    // 这里可以放置只在此实现类中用的其他成员或外部依赖，比如：
    // std::shared_ptr<SomeExternalDep> external_dep;
};
