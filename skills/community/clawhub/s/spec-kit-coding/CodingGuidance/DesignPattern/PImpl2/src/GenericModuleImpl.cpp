#include "../inc_private/GenericModuleImpl.h"

#include <mutex>
#include <iostream>

// 构造函数
GenericModuleImpl::GenericModuleImpl() {
    // 基础构造逻辑，通常不建议这里做复杂的初始化
}

// 析构函数
GenericModuleImpl::~GenericModuleImpl() {
    Deinit(); // 确保安全反初始化
}

// 模块初始化
int GenericModuleImpl::Init() {
    // 原子状态转换：仅当当前为 Uninitialized 时才能进入 Initializing
    // 若已是 Initialized/Initializing/Deinitializing，直接返回，天然防重入
    ModuleState expected = ModuleState::Uninitialized;
    if (!mInitState.compare_exchange_strong(expected, ModuleState::Initializing)) {
        if (expected == ModuleState::Initialized) {
            std::cerr << "Module is already initialized!" << std::endl;
            return 0;
        }
        std::cerr << "Module is initializing or deinitializing, skipping init" << std::endl;
        return -1;
    }

    std::unique_lock<std::shared_mutex> writeLock(mMutex);

    //
    // TODO: 在这里添加模块的具体初始化工作
    // 例如外部回调的注册，线程的启动，总线订阅等
    // 若任何初始化失败，应回退状态：
    //   mInitState.store(ModuleState::Uninitialized);
    //   return -1;
    //

    mInitState.store(ModuleState::Initialized);
    return 0;
}

bool GenericModuleImpl::getIsInited() {
    return mInitState.load() == ModuleState::Initialized;
}

// 模块反初始化
int GenericModuleImpl::Deinit() {
    // 原子状态转换：仅当当前为 Initialized 时才能进入 Deinitializing
    ModuleState expected = ModuleState::Initialized;
    if (!mInitState.compare_exchange_strong(expected, ModuleState::Deinitializing)) {
        if (expected == ModuleState::Uninitialized) {
            std::cerr << "Module is already deinitialized!" << std::endl;
            return 0;
        }
        std::cerr << "Module is initializing or deinitializing, skipping deinit" << std::endl;
        return -1;
    }

    std::unique_lock<std::shared_mutex> writeLock(mMutex);

    //
    // TODO: 回收资源，取消订阅回调，关闭线程等
    //

    mInitState.store(ModuleState::Uninitialized);
    return 0;
}

// 具体业务任务
void GenericModuleImpl::DoTask() {
    // 无锁快速路径：只有 Initialized 状态才执行业务
    if (!getIsInited()) {
        std::cerr << "Module is not initialized!" << std::endl;
        return;
    }

    {
        std::shared_lock<std::shared_mutex> readLock(mMutex); // 读锁保护业务逻辑中的共享状态访问
        // std::unique_lock<std::shared_mutex> writeLock(mMutex); // 若业务逻辑需要修改共享状态，则使用写锁

        // 在锁的环境下获取必要信息的拷贝
        // 或者直接在锁内执行业务逻辑，视具体情况而定
    }

    //
    // 根据上面在锁的环境里面获取的信息拷贝，执行具体的内部业务流程
    //
}
