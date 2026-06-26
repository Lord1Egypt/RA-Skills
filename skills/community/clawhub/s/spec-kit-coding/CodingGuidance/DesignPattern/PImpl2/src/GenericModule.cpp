#include "../inc_private/GenericModuleImpl.h"

std::shared_ptr<GenericModule> GenericModule::Create() {
    return std::make_shared<GenericModuleImpl>();
}
