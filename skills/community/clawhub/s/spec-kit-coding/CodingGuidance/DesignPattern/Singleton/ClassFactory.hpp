#pragma once

/**
 * @file    ClassFactory.hpp
 * @brief   Generic class factory with singleton pattern (header-only).
 *
 * @details
 * Provides compile-time automatic registration and run-time name-based
 * object creation.  Useful for plugin architectures, config-driven
 * handler selection, protocol parser dispatch, etc.
 *
 * How it works:
 *   1. ClassFactory is a Meyers' Singleton holding a name -> creator map.
 *   2. The REGISTER_CLASS(ClassName) macro defines a static AutoRegister
 *      object whose constructor runs before main(), inserting the class
 *      into the factory's registry.
 *   3. At run time call ClassFactory::instance().create<Base>("Name") to
 *      obtain a type-safe std::unique_ptr<Base>.
 *
 * Thread safety: the singleton initialisation is thread-safe per C++11.
 * Concurrent reads (create / has / registeredNames) are safe once all
 * registrations have completed (before main).
 *
 * Dependencies: C++11 standard library only. No third-party libraries.
 *
 * Platforms: Linux, Windows (MSVC / MinGW / GCC / Clang).
 *
 * @code
 *   // --- registration (global scope in a .cpp) ---
 *   class MyHandler : public Handler { ... };
 *   REGISTER_CLASS(MyHandler);
 *
 *   // --- creation (at run time) ---
 *   auto ptr = ClassFactory::instance().create<Handler>("MyHandler");
 *   if (ptr) ptr->handle(request);
 *
 *   // --- query ---
 *   for (auto& n : ClassFactory::instance().registeredNames())
 *       std::cout << n << std::endl;
 * @endcode
 */

#include <map>
#include <string>
#include <memory>
#include <vector>
#include <functional>
#include <cassert>

/**
 * @class ClassFactory
 * @brief Singleton class factory: compile-time registration, run-time creation.
 */
class ClassFactory {
public:
    /** @brief Type of a creator function returning a heap-allocated object. */
    using Creator = std::function<void*()>;

    /* ========================= Core API ========================= */

    /**
     * @brief  Obtain the global factory singleton.
     * @return Reference to the unique ClassFactory instance.
     *
     * Uses a function-local static (Meyers' Singleton) which is
     * guaranteed to be thread-safe in C++11 and later.
     */
    static ClassFactory& instance() {
        static ClassFactory sInstance;
        return sInstance;
    }

    /**
     * @brief  Register a class into the factory.
     * @param  name     String identifier for the class.
     * @param  creator  Function that creates a new instance on the heap.
     *
     * If @p name already exists the registration is silently skipped
     * (first-registered wins).
     */
    void registerClass(const std::string& name, Creator creator) {
        mRegistry.emplace(name, std::move(creator));
    }

    /**
     * @brief  Create an object by registered name (type-safe).
     * @tparam T  Expected return type (typically the base class).
     * @param  name  The name the class was registered under.
     * @return A unique_ptr<T> owning the new object, or nullptr on failure.
     *
     * Internally the Creator returns void* which is static_cast to T*.
     * The caller must ensure T is a base of the actual registered class.
     */
    template <typename T = void>
    std::unique_ptr<T> create(const std::string& name) const {
        auto it = mRegistry.find(name);
        if (it == mRegistry.end()) {
            return nullptr;
        }
        void* raw = it->second();
        // Check that the created object can be safely cast to T* (debug mode only).
        assert(dynamic_cast<T*>(static_cast<T*>(raw)) != nullptr &&
               "ClassFactory::create: registered class is not derived from T");
        return std::unique_ptr<T>(static_cast<T*>(raw));
    }

    /**
     * @brief  Create an object by name (raw pointer, C-style).
     * @param  name  The registered class name.
     * @return void* pointing to the new object, or nullptr. Caller owns it.
     *
     * @warning Not recommended use this API because it returns a raw pointer and is not type-safe.
     *          Use create<T>() instead for type safety and automatic memory management.
     */
    [[deprecated("Use create<T>() instead to avoid memory leaks")]]
    void* createRaw(const std::string& name) const {
        auto it = mRegistry.find(name);
        if (it == mRegistry.end()) {
            return nullptr;
        }
        return it->second();
    }

    /* ======================== Query API ========================= */

    /** @brief Check whether a class name is registered. */
    bool has(const std::string& name) const {
        return mRegistry.find(name) != mRegistry.end();
    }

    /** @brief Return a list of all registered class names. */
    std::vector<std::string> registeredNames() const {
        std::vector<std::string> names;
        names.reserve(mRegistry.size());
        for (auto& kv : mRegistry) {
            names.push_back(kv.first);
        }
        return names;
    }

    /** @brief Return the number of registered classes. */
    size_t size() const { return mRegistry.size(); }

private:
    ClassFactory()  = default;
    ~ClassFactory() = default;
    ClassFactory(const ClassFactory&)            = delete;
    ClassFactory& operator=(const ClassFactory&) = delete;

    std::map<std::string, Creator> mRegistry;  ///< Name -> creator map.
};

/* ==================== Auto-registration helper ==================== */

/**
 * @class AutoRegister
 * @brief Helper whose constructor registers a class before main() runs.
 *
 * Not intended for direct use; prefer the REGISTER_CLASS macro.
 */
class AutoRegister {
public:
    /**
     * @brief Construct and register a creator under @p name.
     * @param name     Class identifier string.
     * @param creator  Factory function.
     */
    AutoRegister(const std::string& name, ClassFactory::Creator creator) {
        ClassFactory::instance().registerClass(name, std::move(creator));
    }
};

/**
 * @def REGISTER_CLASS(ClassName)
 * @brief Place in global scope of a .cpp file to register ClassName.
 *
 * Expands to a static creator function and a static AutoRegister object
 * whose constructor runs before main(), inserting ClassName into the
 * ClassFactory registry.
 *
 * @code
 *   class MyParser : public Parser { ... };
 *   REGISTER_CLASS(MyParser);
 *   // Now ClassFactory::instance().create<Parser>("MyParser") works.
 * @endcode
 */
#define REGISTER_CLASS(ClassName)                                           \
    static void* classFactoryCreator_##ClassName() {                        \
        return new ClassName();                                             \
    }                                                                       \
    static AutoRegister classFactoryReg_##ClassName(                        \
        #ClassName, classFactoryCreator_##ClassName)
