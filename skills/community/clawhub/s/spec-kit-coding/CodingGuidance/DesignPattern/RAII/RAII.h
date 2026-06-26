#pragma once

#include <cstddef>
#include <cstdio>
#include <string>

/**
 * @brief RAII wrapper for managing a C file handle (std::FILE*).
 *
 * Resource lifetime rule:
 * - Acquire with open()
 * - Release automatically in destructor or manually with close()
 *
 * Unified return convention for member functions returning int:
 * - < 0: error (-errno, e.g. -EIO)
 * - = 0: full success
 * - > 0: conditional success (e.g. partial read/write count)
 */
class FileGuard {
public:
    /**
     * @brief Constructs an empty guard without opening a file.
     */
    FileGuard() noexcept = default;

    /**
     * @brief Convenience constructor that calls open(path, mode).
     * @param path File path.
     * @param mode fopen mode string.
     */
    FileGuard(const std::string& path, const char* mode) noexcept;

    /**
     * @brief Destructor that releases the file resource if still open.
     */
    ~FileGuard();

    /** @brief Copy construction is disabled to keep unique ownership. */
    FileGuard(const FileGuard&) = delete;

    /** @brief Copy assignment is disabled to keep unique ownership. */
    FileGuard& operator=(const FileGuard&) = delete;

    /**
     * @brief Move constructor that transfers file ownership.
     * @param other Source guard.
     */
    FileGuard(FileGuard&& other) noexcept;

    /**
     * @brief Move assignment that transfers file ownership.
     * @param other Source guard.
     * @return Reference to this object.
     */
    FileGuard& operator=(FileGuard&& other) noexcept;

    /**
     * @brief Checks whether a valid file handle is currently owned.
     * @return true if open; otherwise false.
     */
    bool isOpen() const noexcept;

    /**
     * @brief Gets the raw std::FILE* handle.
     * @return Raw file handle, or nullptr if not open.
     */
    std::FILE* get() const noexcept;

    /**
     * @brief Opens a file. If already open, the current handle is closed first.
     * @param path File path.
     * @param mode fopen mode string.
     * @return 0 on success, negative errno on failure.
     */
    int open(const std::string& path, const char* mode) noexcept;

    /**
     * @brief Writes data to the file.
     * @param data Source buffer.
     * @param size Size of each element.
     * @param count Number of elements to write.
     * @return 0 if all data was written;
     *         positive value for partial success (actual element count written);
     *         negative errno on failure.
     */
    int write(const void* data, std::size_t size, std::size_t count) noexcept;

    /**
     * @brief Reads data from the file.
     * @param buffer Destination buffer.
     * @param size Size of each element.
     * @param count Number of elements to read.
     * @return 0 if all data was read;
     *         positive value for partial success/EOF (actual element count read);
     *         negative errno on failure.
     */
    int read(void* buffer, std::size_t size, std::size_t count) noexcept;

    /**
     * @brief Flushes buffered output to the file.
     * @return 0 on success, negative errno on failure.
     */
    int flush() noexcept;

    /**
     * @brief Closes the file if open. Repeated calls are safe.
     * @return 0 on success, negative errno on failure.
     */
    int close() noexcept;

private:
    std::FILE* mFile = nullptr;
};

/**
 * @brief Demonstrates FileGuard usage with shared_ptr and move semantics.
 */
void RAIIExample();
