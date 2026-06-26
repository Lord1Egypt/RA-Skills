#include "RAII.h"

#include <climits>
#include <cerrno>
#include <cstring>
#include <iostream>
#include <memory>
#include <utility>

namespace {
int makeError(const char* prefix, int err) {
    if (err <= 0) {
        err = EIO;
    }
    std::cout << "[Error] " << prefix << ": " << std::strerror(err) << " (ret=" << -err << ")" << std::endl;
    return -err;
}

int makeConditionalSuccess(const char* prefix, int value) {
    std::cout << "[Info] " << prefix << ": partial success, value=" << value << std::endl;
    return value;
}
}

FileGuard::FileGuard(const std::string& path, const char* mode) noexcept {
    open(path, mode);
}

FileGuard::~FileGuard() {
    // ! WARN: Not recommended using std::cerr in destructors, but for demonstration purposes we will log the destructor call.
    std::cout << "FileGuard destructor called, closing file if open." << std::endl;
    // Call close() to release the file resource if still open
    close();
    std::cout << "FileGuard destructor finished." << std::endl;
}

FileGuard::FileGuard(FileGuard&& other) noexcept : mFile(other.mFile) {
    // After move, the source guard should no longer own the file resource
    other.mFile = nullptr;
}

FileGuard& FileGuard::operator=(FileGuard&& other) noexcept {
    if (this == &other) {
        return *this;
    }

    close();
    mFile = other.mFile;
    other.mFile = nullptr;
    return *this;
}

bool FileGuard::isOpen() const noexcept {
    return mFile != nullptr;
}

std::FILE* FileGuard::get() const noexcept {
    return mFile;
}

int FileGuard::open(const std::string& path, const char* mode) noexcept {
    if (path.empty() || mode == nullptr) {
        return makeError("FileGuard::open invalid argument", EINVAL);
    }

    if (mFile != nullptr) {
        const int closeRet = close();
        if (closeRet < 0) {
            return closeRet;
        }
    }

    mFile = std::fopen(path.c_str(), mode);
    if (mFile == nullptr) {
        return makeError("FileGuard::open failed", errno);
    }

    return 0;
}

int FileGuard::write(const void* data, std::size_t size, std::size_t count) noexcept {
    if (mFile == nullptr) {
        return makeError("FileGuard::write failed", EBADF);
    }
    if ((data == nullptr && count > 0) || size == 0) {
        return makeError("FileGuard::write invalid argument", EINVAL);
    }

    const std::size_t writtenCount = std::fwrite(data, size, count, mFile);
    if (writtenCount != count) {
        if (std::ferror(mFile) != 0) {
            return makeError("FileGuard::write failed", errno);
        }
        const int val = (writtenCount > static_cast<std::size_t>(INT_MAX)) ? INT_MAX : static_cast<int>(writtenCount);
        return makeConditionalSuccess("FileGuard::write", val);
    }

    return 0;
}

int FileGuard::read(void* buffer, std::size_t size, std::size_t count) noexcept {
    if (mFile == nullptr) {
        return makeError("FileGuard::read failed", EBADF);
    }
    if ((buffer == nullptr && count > 0) || size == 0) {
        return makeError("FileGuard::read invalid argument", EINVAL);
    }

    const std::size_t readCount = std::fread(buffer, size, count, mFile);
    if (readCount != count && std::ferror(mFile) != 0) {
        return makeError("FileGuard::read failed", errno);
    }

    if (readCount != count) {
        const int val = (readCount > static_cast<std::size_t>(INT_MAX)) ? INT_MAX : static_cast<int>(readCount);
        return makeConditionalSuccess("FileGuard::read", val);
    }

    return 0;
}

int FileGuard::flush() noexcept {
    if (mFile == nullptr) {
        return makeError("FileGuard::flush failed", EBADF);
    }
    if (std::fflush(mFile) != 0) {
        return makeError("FileGuard::flush failed", errno);
    }

    return 0;
}

int FileGuard::close() noexcept {
    if (mFile != nullptr) {
        if (std::fclose(mFile) != 0) {
            const int ret = makeError("FileGuard::close failed", errno);
            mFile = nullptr;
            return ret;
        }
        mFile = nullptr;
    }

    return 0;
}

void RAIIExample() {
    {
        std::cout << "[Part1] shared_ptr example" << std::endl;

        std::shared_ptr<FileGuard> file = std::make_shared<FileGuard>();
        int ret = file->open("raii_demo.txt", "wb");
        if (ret < 0) {
            std::cout << "RAIIExample part1 failed in open(), ret=" << ret << std::endl;
            return;
        }

        const char text[] = "RAII demo: resource is managed automatically.\n";
        ret = file->write(text, sizeof(char), sizeof(text) - 1);
        if (ret < 0) {
            std::cout << "RAIIExample part1 failed in write(), ret=" << ret << std::endl;
            return;
        }
        if (ret > 0) {
            std::cout << "RAIIExample part1 write partial success, count=" << ret << std::endl;
        }

        ret = file->flush();
        if (ret < 0) {
            std::cout << "RAIIExample part1 failed in flush(), ret=" << ret << std::endl;
            return;
        }

        // Resetting the shared_ptr will automatically call the FileGuard destructor
        file.reset();
        std::cout << "RAIIExample part1 finished successfully." << std::endl;
    }

    {
        std::cout << "[Part2] move semantics example" << std::endl;

        FileGuard src;
        int ret = src.open("raii_move_demo.txt", "wb");
        if (ret < 0) {
            std::cout << "RAIIExample part2 failed in open(), ret=" << ret << std::endl;
            return;
        }

        // Move the FileGuard to a new instance, transferring ownership of the file resource.
        FileGuard dst = std::move(src);
        std::cout << "after move: src.isOpen=" << src.isOpen() << ", dst.isOpen=" << dst.isOpen() << std::endl;

        const char moveText[] = "Move demo: resource ownership transferred.\n";
        ret = dst.write(moveText, sizeof(char), sizeof(moveText) - 1);
        if (ret < 0) {
            std::cout << "RAIIExample part2 failed in write(), ret=" << ret << std::endl;
            return;
        }
        if (ret > 0) {
            std::cout << "RAIIExample part2 write partial success, count=" << ret << std::endl;
        }

        ret = dst.flush();
        if (ret < 0) {
            std::cout << "RAIIExample part2 failed in flush(), ret=" << ret << std::endl;
            return;
        }

        std::cout << "RAIIExample part2 finished successfully." << std::endl;
    }
}
