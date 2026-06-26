---
name: rpm-packager
description: Build RPM packages from source code for CentOS/RHEL systems. Use when user needs to: (1) package software source into installable RPM, (2) create SPEC files, (3) build packages for CentOS 7/8/9 or RHEL, (4) prepare software for distribution on RPM-based Linux systems.
---

# RPM Packager Skill

Transform source code into installable RPM packages for CentOS/RHEL systems.

## Quick Start

```bash
# Basic usage
./scripts/build-rpm.sh <source-dir> <package-name> <version> <release>

# Example
./scripts/build-rpm.sh ./myapp myapp 1.0.0 1
```

## Workflow

### 1. Prepare Source Code

Ensure source code is ready:
- Has a build system (Makefile, CMakeLists.txt, setup.py, etc.)
- Clean directory structure
- No build artifacts

### 2. Check Prerequisites

Required tools on CentOS/RHEL (**requires sudo privileges**):
```bash
sudo yum install rpm-build mock gcc make
```

> **Note:** Installing system packages requires `sudo` privileges. The build process itself runs as your user account.

### 3. Run Build Script

```bash
cd ~/.openclaw/workspace/skills/rpm-packager
chmod +x scripts/build-rpm.sh
./scripts/build-rpm.sh /path/to/source package-name 1.0.0 1
```

### 4. Verify Output

Build produces:
- Binary RPM: `~/rpmbuild/RPMS/x86_64/package-name-1.0.0-1.el8.x86_64.rpm`
- Source RPM: `~/rpmbuild/SRPMS/package-name-1.0.0-1.el8.src.rpm`

### 5. Install & Test

```bash
# Install the RPM
sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/package-name-1.0.0-1.el8.x86_64.rpm

# Or use yum/dnf for dependency resolution
sudo yum localinstall ~/rpmbuild/RPMS/x86_64/package-name-1.0.0-1.el8.x86_64.rpm

# Verify installation
rpm -q package-name
```

## SPEC File Customization

For complex packages, customize the SPEC file:

1. **Review template**: See [references/spec-template.md](references/spec-template.md)
2. **Edit generated SPEC**: Modify `~/rpmbuild/SPECS/package-name.spec`
3. **Rebuild**: `rpmbuild -ba ~/rpmbuild/SPECS/package-name.spec`

### Common Customizations

**Add dependencies:**
```spec
BuildRequires: python3-devel openssl-devel
Requires: python3 openssl-libs
```

**Custom install paths:**
```spec
%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/package-name
install -m 755 myapp %{buildroot}%{_bindir}/
install -m 644 config.conf %{buildroot}%{_sysconfdir}/package-name/
```

**Include documentation:**
```spec
%files
%doc README.md LICENSE CHANGELOG.md
%{_bindir}/myapp
```

## Build for Different CentOS Versions

Use mock for clean builds targeting specific versions:

```bash
# CentOS 7
mock -r centos-7-x86_64 package-name.spec

# CentOS 8
mock -r centos-8-x86_64 package-name.spec

# CentOS 9
mock -r centos-9-x86_64 package-name.spec
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `RPM_BUILDER_NAME` | `OpenClaw Builder` | Builder name in changelog |
| `RPM_BUILD_DIR` | `~/rpmbuild` | Custom build directory |

## Troubleshooting

### Build fails with "No such file or directory"
- Check `BuildRequires` for missing tools
- Verify source tarball extracts correctly

### RPM installs but command not found
- Ensure `%files` section includes correct paths
- Check executable permissions in `%install`

### Dependency errors during install
- Add missing `Requires` entries to SPEC file
- Use `yum localinstall` instead of `rpm -i` for auto-dependency resolution

## Output Locations

After successful build:
- **Binary RPMs**: `~/rpmbuild/RPMS/<arch>/`
- **Source RPM**: `~/rpmbuild/SRPMS/`
- **Build logs**: `~/rpmbuild/BUILDLOGS/`
- **SPEC files**: `~/rpmbuild/SPECS/`

## Security Notes

- Build directory defaults to `~/rpmbuild` to avoid conflicts with system-wide builds
- Builder identity is anonymized by default (uses `OpenClaw Builder`)
- No personal information is embedded in generated RPMs unless explicitly configured
