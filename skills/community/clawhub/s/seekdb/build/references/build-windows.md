# Build SeekDB — Windows (native PowerShell only)

**Cannot cross-compile.** If the user requests `windows` from a macOS/Linux host, print:

> Windows builds cannot be cross-compiled. Run the following natively on Windows:

---

## Prerequisites (one-time)

```powershell
winget install -e --id Microsoft.DotNet.SDK.8
# restart PowerShell, then:
dotnet tool install --global wix
```

---

## Init

```powershell
.\build.ps1 init
```

---

## Compile

```powershell
.\build.ps1 release --ninja -j 16   # or: debug
```

---

## Package — `installer` (WiX, after compile)

```powershell
cd build_release
cmake --build . --target package
```

---

## Verify

```bash
mysql -h 127.0.0.1 -uroot -P2881 -Dtest -A
```
