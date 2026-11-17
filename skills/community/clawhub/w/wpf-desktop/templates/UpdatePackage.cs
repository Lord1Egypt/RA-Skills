// Copy into the application's update layer and set its namespace.
// Selection/cache helpers only. Offline apps keep manual updates and need no service.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text.RegularExpressions;

namespace DesktopDelivery;

public static class UpdatePackage
{
    private static string Version(string version)
    {
        version = version.StartsWith('v') ? version[1..] : version;
        if (!Regex.IsMatch(version, @"^\d+\.\d+\.\d+$")) throw new ArgumentException("Expected a stable version", nameof(version));
        return version;
    }

    public static string Cpu(Architecture? architecture = null) => (architecture ?? RuntimeInformation.ProcessArchitecture) switch
    {
        Architecture.X64 => "x64",
        Architecture.Arm64 => "arm64",
        _ => throw new PlatformNotSupportedException("Supported update architectures are x64 and arm64")
    };

    public static string? SelectZip(IEnumerable<string> assets, string appName, string version, Architecture? architecture = null)
    {
        var name = $"{appName}-v{Version(version)}-win-{Cpu(architecture)}.zip";
        // Exact match excludes a framework-dependent package or a raw executable.
        return assets.SingleOrDefault(asset => string.Equals(asset, name, StringComparison.Ordinal));
    }

    public static string CacheDirectory(string root, string version, Architecture? architecture = null)
        => Path.Combine(root, Cpu(architecture), Version(version));
}
