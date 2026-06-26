# RPM SPEC File Template Reference

## Basic SPEC File Structure

```spec
Name:           package-name
Version:        1.0.0
Release:        1%{?dist}
Summary:        Short description of the package

License:        MIT
URL:            https://example.com
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc make
Requires:       glibc

%description
Longer description of the package. Can span multiple lines.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/package-name

%changelog
* Mon Jan 01 2024 OpenClaw Builder <builder@openclaw.local> - 1.0.0-1
- Initial package
```

> **Privacy Note:** Use generic builder names (e.g., `OpenClaw Builder`) and avoid personal email addresses in distributed packages.

## Common Macros

| Macro | Description |
|-------|-------------|
| `%{_bindir}` | /usr/bin |
| `%{_sbindir}` | /usr/sbin |
| `%{_libdir}` | /usr/lib64 |
| `%{_datadir}` | /usr/share |
| `%{_mandir}` | /usr/share/man |
| `%{_sysconfdir}` | /etc |
| `%{?dist}` | Distribution tag (.el8, .el9, etc.) |
| `%{?_smp_mflags}` | Parallel build flags |

## Common BuildRequires

- **C/C++**: `gcc`, `gcc-c++`, `make`, `cmake`
- **Python**: `python3`, `python3-devel`, `python3-pip`
- **Java**: `java-11-openjdk`, `maven`
- **Node.js**: `nodejs`, `npm`
- **Go**: `golang`

## License Identifiers

- `MIT`
- `GPLv2`
- `GPLv3`
- `Apache-2.0`
- `BSD`
- `ISC`
- `Proprietary`

## Common Sections

### %prep
Prepare source code:
```spec
%prep
%setup -q
# Or with custom extraction
%setup -q -n %{name}-%{version}
```

### %build
Compile the software:
```spec
%build
%configure
make %{?_smp_mflags}

# Or for CMake
%build
cmake -B _build -S . -DCMAKE_BUILD_TYPE=Release
cmake --build _build
```

### %install
Install to build root:
```spec
%install
make install DESTDIR=%{buildroot}

# Or manual installation
mkdir -p %{buildroot}%{_bindir}
install -m 755 myapp %{buildroot}%{_bindir}/
```

### %files
List files to include:
```spec
%files
%defattr(-,root,root,-)
%{_bindir}/myapp
%{_mandir}/man1/myapp.1.gz
%doc README.md LICENSE
%config(noreplace) %{_sysconfdir}/myapp.conf
```

## Troubleshooting

### Missing BuildRequires
Error: `command not found` during build
Solution: Add required tools to `BuildRequires`

### File conflicts
Error: `file conflicts between packages`
Solution: Check `%files` section, ensure unique paths

### Permission issues
Error: `Permission denied`
Solution: Use proper `install -m` flags or `%attr` macro

## Security Best Practices

1. **Anonymize builder info** - Use generic names in `%changelog`
2. **Avoid hardcoded paths** - Use RPM macros like `%{_bindir}`
3. **Minimize permissions** - Set appropriate file modes with `%attr`
4. **Document dependencies** - Clearly list all `Requires` and `BuildRequires`
