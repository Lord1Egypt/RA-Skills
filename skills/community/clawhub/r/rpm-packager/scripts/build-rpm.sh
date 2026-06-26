#!/bin/bash
# build-rpm.sh - Build RPM package from source code
# Usage: ./build-rpm.sh <source-dir> <package-name> <version> <release>

set -e

SOURCE_DIR="${1:-.}"
PACKAGE_NAME="${2:-$(basename "$SOURCE_DIR")}"
VERSION="${3:-1.0.0}"
RELEASE="${4:-1}"

# Configurable build directory (default: ~/rpmbuild)
RPM_BUILD_DIR="${RPM_BUILD_DIR:-$HOME/rpmbuild}"

# Builder name for changelog (anonymized by default)
RPM_BUILDER_NAME="${RPM_BUILDER_NAME:-OpenClaw Builder}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing=()
    for cmd in rpmbuild mock; do
        if ! command -v "$cmd" &> /dev/null; then
            missing+=("$cmd")
        fi
    done
    
    if [ ${#missing[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing[*]}"
        log_info "Install with: sudo yum install rpm-build mock"
        exit 1
    fi
    
    log_info "All prerequisites met"
}

# Validate source directory
validate_source_dir() {
    log_info "Validating source directory: $SOURCE_DIR"
    
    if [ ! -d "$SOURCE_DIR" ]; then
        log_error "Source directory does not exist: $SOURCE_DIR"
        log_info "Please provide a valid source directory path"
        exit 1
    fi
    
    if [ ! -r "$SOURCE_DIR" ]; then
        log_error "Source directory is not readable: $SOURCE_DIR"
        exit 1
    fi
    
    # Check if directory is empty
    if [ -z "$(ls -A "$SOURCE_DIR" 2>/dev/null)" ]; then
        log_error "Source directory is empty: $SOURCE_DIR"
        exit 1
    fi
    
    log_info "Source directory validated"
}

# Create RPM build directory structure
setup_build_env() {
    log_info "Setting up RPM build environment at $RPM_BUILD_DIR..."
    
    mkdir -p "$RPM_BUILD_DIR"/{BUILD,RPMS,SOURCES,SPECS,SRPMS,BUILDLOGS}
    
    log_info "Build environment ready at $RPM_BUILD_DIR"
}

# Create tarball from source
create_source_tarball() {
    log_info "Creating source tarball..."
    
    local TARBALL_NAME="${PACKAGE_NAME}-${VERSION}.tar.gz"
    local TARBALL_PATH="$RPM_BUILD_DIR/SOURCES/$TARBALL_NAME"
    
    # Get absolute path
    local ABS_SOURCE_DIR
    ABS_SOURCE_DIR="$(cd "$SOURCE_DIR" && pwd)"
    
    tar -czf "$TARBALL_PATH" -C "$(dirname "$ABS_SOURCE_DIR")" "$(basename "$ABS_SOURCE_DIR")"
    
    log_info "Source tarball created: $TARBALL_PATH"
    echo "$TARBALL_PATH"
}

# Generate SPEC file template
generate_spec_file() {
    local SPEC_FILE="$RPM_BUILD_DIR/SPECS/${PACKAGE_NAME}.spec"
    
    log_info "Generating SPEC file: $SPEC_FILE"
    
    cat > "$SPEC_FILE" << EOF
Name:           ${PACKAGE_NAME}
Version:        ${VERSION}
Release:        ${RELEASE}%{?dist}
Summary:        ${PACKAGE_NAME} application

License:        MIT
URL:            https://example.com/${PACKAGE_NAME}
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc make
Requires:       glibc

%description
${PACKAGE_NAME} - Built from source automatically

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/${PACKAGE_NAME}

%changelog
* $(date +%a\ %b\ %d\ %Y) ${RPM_BUILDER_NAME} - ${VERSION}-${RELEASE}
- Initial package build
EOF

    log_info "SPEC file generated"
    echo "$SPEC_FILE"
}

# Build RPM package
build_rpm() {
    local SPEC_FILE="$1"
    
    log_info "Building RPM package..."
    
    rpmbuild -ba "$SPEC_FILE" 2>&1 | tee "$RPM_BUILD_DIR/BUILDLOGS/${PACKAGE_NAME}-${VERSION}.log"
    
    log_info "RPM build completed"
    log_info "Packages located at:"
    
    if [ -d "$RPM_BUILD_DIR/RPMS" ]; then
        find "$RPM_BUILD_DIR/RPMS" -name "${PACKAGE_NAME}-${VERSION}-${RELEASE}*.rpm" -exec ls -lh {} \;
    fi
    
    if [ -d "$RPM_BUILD_DIR/SRPMS" ]; then
        find "$RPM_BUILD_DIR/SRPMS" -name "${PACKAGE_NAME}-${VERSION}-${RELEASE}*.src.rpm" -exec ls -lh {} \;
    fi
}

# Cleanup function
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_warn "Build failed with exit code $exit_code"
        log_info "Check build logs at: $RPM_BUILD_DIR/BUILDLOGS/"
    fi
}

trap cleanup EXIT

# Main execution
main() {
    log_info "Starting RPM build process for ${PACKAGE_NAME} v${VERSION}"
    log_info "Build directory: $RPM_BUILD_DIR"
    log_info "Builder: $RPM_BUILDER_NAME"
    
    validate_source_dir
    check_prerequisites
    setup_build_env
    create_source_tarball
    generate_spec_file
    build_rpm "$RPM_BUILD_DIR/SPECS/${PACKAGE_NAME}.spec"
    
    log_info "Build complete! RPM packages ready for installation on CentOS/RHEL"
}

main "$@"
