// Copy into the application, set its namespace, and configure Options in trusted application code.
// The helper registers only this executable. It never accepts a target path or command from the CLI.
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Security.Principal;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using System.Xml.Linq;
using System.Xml;
using System.Globalization;
using Microsoft.Win32;

namespace DesktopStartup;

public enum StartupOperation { Install, Repair, Uninstall, Plain }
public enum StartupOutcome { Applied, Unchanged, Cancelled, Failed, Uncertain }
public enum StartupFailure { None, AccountMismatch, AccessDenied, OwnershipConflict, RollbackIncomplete }
public sealed record StartupResult(StartupOutcome Outcome, string? Detail = null, StartupFailure Failure = StartupFailure.None);
public sealed class StartupOwnershipException(string message) : InvalidOperationException(message);
public sealed class StartupRollbackException(string message, Exception inner) : IOException(message, inner);
public sealed record StartupOptions(string AppId, string ExecutableName, string TrayArguments = "--tray", string? LegacyRunValueName = null, string? PlainArguments = null, int LogonDelaySeconds = 3);
public sealed record StartupTarget(StartupOptions Options, string Executable, string UserSid)
{
    public string TaskName => Options.AppId + ".Startup." + UserSid;
    public string Source => "urn:desktop-startup:" + Options.AppId + ":" + UserSid;
}

// Tests supply a memory implementation; the Windows backend is never needed for isolated tests.
public interface IStartupStore
{
    string? ReadTask(string name);
    void WriteTask(string name, string xml, string userSid);
    void DeleteTask(string name);
    string? ReadRun(string valueName);
    void WriteRun(string valueName, string? command);
}

public static class ElevatedStartup
{
    public const string HelperSwitch = "--startup-task";
    private static readonly XNamespace Ns = "http://schemas.microsoft.com/windows/2004/02/mit/task";

    public static string NormalizePath(string path)
    {
        string value = path.Trim();
        if (value.Length >= 2 && value[0] == '"' && value[^1] == '"') value = value[1..^1];
        if (value.Contains('"') || !Path.IsPathFullyQualified(value))
            throw new ArgumentException("Expected an absolute executable path, without command arguments.");
        return Path.GetFullPath(value);
    }

    public static StartupTarget Target(StartupOptions options, string executable, string userSid)
    {
        if (!Regex.IsMatch(options.AppId, @"\A[A-Za-z0-9][A-Za-z0-9._-]{0,79}\z") ||
            Path.GetFileName(options.ExecutableName) != options.ExecutableName ||
            !options.ExecutableName.EndsWith(".exe", StringComparison.OrdinalIgnoreCase) ||
            options.ExecutableName.Equals("dotnet.exe", StringComparison.OrdinalIgnoreCase))
            throw new ArgumentException("Configure a stable application ID and the published application exe name.");
        ValidateDelay(options.LogonDelaySeconds);
        string path = NormalizePath(executable);
        if (!Path.GetFileName(path).Equals(options.ExecutableName, StringComparison.OrdinalIgnoreCase))
            throw new ArgumentException("Use Environment.ProcessPath of the published apphost, not a development host.");
        _ = new SecurityIdentifier(userSid);
        return new(options, path, userSid);
    }

    public static void ValidateDelay(int seconds)
    {
        if ((uint)seconds > 300) throw new ArgumentOutOfRangeException(nameof(seconds), "Logon delay must be between 0 and 300 seconds.");
    }

    public static string PlainCommand(StartupTarget target)
    {
        string command = ($"\"{target.Executable}\" " + (target.Options.PlainArguments ?? target.Options.TrayArguments)).TrimEnd();
        if (command.Length > 260) throw new ArgumentException("The Run command exceeds Windows' 260-character limit; use a shorter path or a logon-task backend.");
        return command;
    }

    public static string TaskXml(StartupTarget target)
    {
        ValidateDelay(target.Options.LogonDelaySeconds);
        XElement E(string name, object value) => new(Ns + name, value);
        var trigger = new XElement(Ns + "LogonTrigger", E("Enabled", "true"), E("UserId", target.UserSid));
        if (target.Options.LogonDelaySeconds != 0)
            trigger.Add(E("Delay", XmlConvert.ToString(TimeSpan.FromSeconds(target.Options.LogonDelaySeconds))));
        return new XDocument(new XElement(Ns + "Task", new XAttribute("version", "1.2"),
            E("RegistrationInfo", E("Source", target.Source)),
            E("Triggers", trigger),
            E("Principals", new XElement(Ns + "Principal", new XAttribute("id", "User"),
                E("UserId", target.UserSid), E("LogonType", "InteractiveToken"), E("RunLevel", "HighestAvailable"))),
            E("Settings", new[] {
                E("MultipleInstancesPolicy", "IgnoreNew"), E("DisallowStartIfOnBatteries", "false"),
                E("StopIfGoingOnBatteries", "false"), E("StartWhenAvailable", "true"),
                E("RunOnlyIfNetworkAvailable", "false"), E("RunOnlyIfIdle", "false"),
                E("Enabled", "true"), E("ExecutionTimeLimit", "PT0S"), E("Priority", "4") }),
            new XElement(Ns + "Actions", new XAttribute("Context", "User"),
                E("Exec", new[] { E("Command", target.Executable), E("Arguments", target.Options.TrayArguments),
                    E("WorkingDirectory", Path.GetDirectoryName(target.Executable)!) })))).ToString();
    }

    private static XElement Root(string xml) => XDocument.Parse(xml).Root
        ?? throw new InvalidDataException("Task XML has no root.");
    private static string Value(XElement root, params string[] path)
    {
        XElement? node = root;
        foreach (string name in path) node = node?.Element(Ns + name);
        return node?.Value ?? "";
    }

    public static bool Owned(string xml, StartupTarget target)
        => Value(Root(xml), "RegistrationInfo", "Source") == target.Source;

    public static bool Matches(string? xml, StartupTarget target)
    {
        if (xml is null) return false;
        try
        {
            var root = Root(xml);
            return Owned(xml, target) &&
                root.Element(Ns + "Actions")?.Elements().Count() == 1 &&
                root.Element(Ns + "Principals")?.Elements().Count() == 1 &&
                root.Element(Ns + "Principals")?.Element(Ns + "Principal")?.Attribute("id")?.Value == "User" &&
                root.Element(Ns + "Actions")?.Attribute("Context")?.Value == "User" &&
                root.Element(Ns + "Triggers")?.Elements().Count() == 1 &&
                Value(root, "Principals", "Principal", "UserId") == target.UserSid &&
                Value(root, "Principals", "Principal", "LogonType") == "InteractiveToken" &&
                Value(root, "Principals", "Principal", "RunLevel") == "HighestAvailable" &&
                Value(root, "Triggers", "LogonTrigger", "UserId") == target.UserSid &&
                Value(root, "Triggers", "LogonTrigger", "Enabled") == "true" &&
                !root.Element(Ns + "Triggers")!.Descendants().Any(e =>
                    e.Name == Ns + "StartBoundary" || e.Name == Ns + "EndBoundary" ||
                    e.Name == Ns + "Repetition") &&
                DelayMatches(root, target.Options.LogonDelaySeconds) &&
                NormalizePath(Value(root, "Actions", "Exec", "Command")).Equals(target.Executable, StringComparison.OrdinalIgnoreCase) &&
                Value(root, "Actions", "Exec", "Arguments") == target.Options.TrayArguments &&
                NormalizePath(Value(root, "Actions", "Exec", "WorkingDirectory")).Equals(
                    Path.GetDirectoryName(target.Executable), StringComparison.OrdinalIgnoreCase) &&
                Value(root, "Settings", "Enabled") == "true" &&
                Value(root, "Settings", "Priority") == "4" &&
                Value(root, "Settings", "MultipleInstancesPolicy") == "IgnoreNew" &&
                Value(root, "Settings", "DisallowStartIfOnBatteries") == "false" &&
                Value(root, "Settings", "StopIfGoingOnBatteries") == "false" &&
                Value(root, "Settings", "StartWhenAvailable") == "true" &&
                Value(root, "Settings", "RunOnlyIfNetworkAvailable") == "false" &&
                Value(root, "Settings", "RunOnlyIfIdle") == "false" &&
                Value(root, "Settings", "ExecutionTimeLimit") == "PT0S";
        }
        catch { return false; }
    }

    private static bool DelayMatches(XElement root, int seconds)
    {
        ValidateDelay(seconds);
        string value = Value(root, "Triggers", "LogonTrigger", "Delay");
        return (value.Length == 0 ? TimeSpan.Zero : XmlConvert.ToTimeSpan(value)) == TimeSpan.FromSeconds(seconds);
    }

    // Register/repair/remove and Run-value cleanup form one transaction. A failed read is never "missing".
    public static StartupResult Apply(StartupOperation operation, StartupTarget target, IStartupStore store)
    {
        // Helper dispatch precedes the app mutex. Separate copies and uninstallers must not race
        // snapshots and rollback against another helper's successful commit.
        string key = Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(target.TaskName)));
        using var mutex = new Mutex(false, "DesktopStartup." + key,
            new NamedWaitHandleOptions { CurrentUserOnly = true, CurrentSessionOnly = false });
        bool acquired;
        try { acquired = mutex.WaitOne(0); }
        catch (AbandonedMutexException) { acquired = true; }
        if (!acquired) throw Failure("another startup operation is in progress", target,
            new IOException("Wait for that operation and read state before retrying."));
        try { return ApplyCore(operation, target, store); }
        finally { mutex.ReleaseMutex(); }
    }

    private static StartupResult ApplyCore(StartupOperation operation, StartupTarget target, IStartupStore store)
    {
        if (!Enum.IsDefined(operation)) throw new ArgumentOutOfRangeException(nameof(operation));
        string name = target.TaskName;
        string? beforeTask, beforeRun, beforeLegacy;
        try
        {
            beforeTask = store.ReadTask(name);
            beforeRun = store.ReadRun(target.Options.AppId);
            beforeLegacy = target.Options.LegacyRunValueName is { } legacy ? store.ReadRun(legacy) : null;
            if (beforeTask is not null && !Owned(beforeTask, target))
                throw new StartupOwnershipException("Task name belongs to another application; no changes made.");
        }
        catch (Exception ex) { throw Failure("preflight", target, ex); }

        bool remove = operation is StartupOperation.Uninstall or StartupOperation.Plain;
        string? desiredRun = operation == StartupOperation.Plain ? PlainCommand(target) : null;
        bool alreadyCorrect = remove ? beforeTask is null : Matches(beforeTask, target);
        if (alreadyCorrect && beforeRun == desiredRun && beforeLegacy is null) return new(StartupOutcome.Unchanged);
        string stage = remove ? "remove task" : "register task";
        try
        {
            if (!alreadyCorrect)
            {
                if (remove) store.DeleteTask(name);
                else store.WriteTask(name, TaskXml(target), target.UserSid);
            }
            stage = "verify task";
            string? after = store.ReadTask(name);
            if (remove ? after is not null : !Matches(after, target))
                throw new IOException("Task readback does not match the requested state.");
            stage = "update plain startup";
            store.WriteRun(target.Options.AppId, desiredRun);
            if (target.Options.LegacyRunValueName is { } legacy) store.WriteRun(legacy, null);
            if (store.ReadRun(target.Options.AppId) != desiredRun ||
                (target.Options.LegacyRunValueName is { } legacyCheck && store.ReadRun(legacyCheck) is not null))
                throw new IOException("The old Run entry is still present.");
            return new(StartupOutcome.Applied);
        }
        catch (Exception ex)
        {
            // Attempt both restores even if one fails, and report any incomplete rollback honestly.
            var errors = new List<Exception> { ex };
            try
            {
                if (beforeTask is null) store.DeleteTask(name);
                else store.WriteTask(name, beforeTask, target.UserSid);
                string? restored = store.ReadTask(name);
                if (beforeTask is null ? restored is not null : restored is null ||
                    !XNode.DeepEquals(Root(beforeTask), Root(restored)))
                    throw new IOException("Previous task definition could not be verified after rollback.");
            }
            catch (Exception rollback) { errors.Add(rollback); }
            try
            {
                store.WriteRun(target.Options.AppId, beforeRun);
                if (store.ReadRun(target.Options.AppId) != beforeRun)
                    throw new IOException("Previous Run entry could not be verified after rollback.");
            }
            catch (Exception rollback) { errors.Add(rollback); }
            if (target.Options.LegacyRunValueName is { } legacy)
            {
                try
                {
                    store.WriteRun(legacy, beforeLegacy);
                    if (store.ReadRun(legacy) != beforeLegacy)
                        throw new IOException("Legacy Run entry could not be verified after rollback.");
                }
                catch (Exception rollback) { errors.Add(rollback); }
            }
            var failure = Failure(stage + (errors.Count > 1 ? "; rollback incomplete" : "; previous startup restored"), target,
                new AggregateException(errors));
            if (errors.Count > 1) throw new StartupRollbackException(failure.Message, failure);
            throw failure;
        }
    }

    private static Exception Failure(string stage, StartupTarget target, Exception error)
        => new IOException($"Startup {stage}; task: {target.TaskName}; executable: {target.Executable}; " +
            $"error: 0x{error.HResult:X8}; {error.Message}", error);

    public static StartupFailure Classify(Exception error)
    {
        if (error is StartupRollbackException) return StartupFailure.RollbackIncomplete;
        if (error is StartupOwnershipException) return StartupFailure.OwnershipConflict;
        if (error is UnauthorizedAccessException || error.HResult == unchecked((int)0x80070005))
            return StartupFailure.AccessDenied;
        if (error is AggregateException aggregate)
        {
            foreach (var inner in aggregate.InnerExceptions)
                if (Classify(inner) is var failure && failure != StartupFailure.None) return failure;
        }
        return error.InnerException is { } nested ? Classify(nested) : StartupFailure.None;
    }

    public static StartupOperation ParseHelper(string[] args, string currentSid)
    {
        if (args.Length is not (3 or 4) || args[0] != HelperSwitch)
            throw new ArgumentException("Invalid startup-helper request. No changes made.");
        if (args.Length == 4) _ = HelperDelay(args);
        if (args[2] != currentSid)
            throw new UnauthorizedAccessException("Different UAC account; this template requires the requesting administrator's own account. No changes made.");
        return args[1] switch {
            "install" => StartupOperation.Install, "repair" => StartupOperation.Repair,
            "uninstall" => StartupOperation.Uninstall, "plain" => StartupOperation.Plain,
            _ => throw new ArgumentException("Unknown startup-helper operation.") };
    }

    public static int HelperDelay(string[] args)
    {
        if (args.Length != 4 || !int.TryParse(args[3], NumberStyles.None, CultureInfo.InvariantCulture, out int seconds))
            throw new ArgumentException("Invalid startup delay. No changes made.");
        ValidateDelay(seconds);
        return seconds;
    }

    private static bool IsAdministrator()
    {
        using var identity = WindowsIdentity.GetCurrent();
        return new WindowsPrincipal(identity).IsInRole(WindowsBuiltInRole.Administrator);
    }

    [DllImport("advapi32.dll", SetLastError = true)]
    private static extern bool OpenProcessToken(IntPtr ProcessHandle, uint DesiredAccess, out IntPtr TokenHandle);

    [DllImport("advapi32.dll", SetLastError = true)]
    private static extern bool GetTokenInformation(IntPtr TokenHandle, int TokenInformationClass, IntPtr TokenInformation, uint TokenInformationLength, out uint ReturnLength);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool CloseHandle(IntPtr hObject);

    private const uint TOKEN_QUERY = 0x0008;
    private const int TokenElevationTypeClass = 18;
    private const int TokenElevationTypeLimitedValue = 3;

    /// <summary>
    /// Checks whether the current user is an administrator account. Under UAC, unelevated processes
    /// run with a split/limited token where BUILTIN\Administrators is marked Deny-Only and filtered by .NET.
    /// This method queries TokenElevationType to reliably detect administrator status before triggering UAC.
    /// </summary>
    public static bool IsAdministratorAccount()
    {
        if (!OperatingSystem.IsWindows()) return false;
        try
        {
            using var identity = WindowsIdentity.GetCurrent();
            var principal = new WindowsPrincipal(identity);
            if (principal.IsInRole(WindowsBuiltInRole.Administrator)) return true;

            if (OpenProcessToken(Process.GetCurrentProcess().Handle, TOKEN_QUERY, out var hToken))
            {
                try
                {
                    int size = sizeof(int);
                    IntPtr pElevationType = Marshal.AllocHGlobal(size);
                    try
                    {
                        if (GetTokenInformation(hToken, TokenElevationTypeClass, pElevationType, (uint)size, out _))
                        {
                            int elevationType = Marshal.ReadInt32(pElevationType);
                            if (elevationType == TokenElevationTypeLimitedValue) return true;
                        }
                    }
                    finally { Marshal.FreeHGlobal(pElevationType); }
                }
                finally { CloseHandle(hToken); }
            }
        }
        catch { }
        return false;
    }

    // Call before the application mutex, settings writes, tray icon, hooks or ordinary CLI dispatch.
    // Supply the app's logger; map the exit status to localized UI in the requesting process.
    public static bool TryHandleHelper(string[] args, StartupOptions options, Action<Exception> log, out int exitCode)
    {
        exitCode = 0;
        if (args.Length == 0 || args[0] != HelperSwitch) return false;
        try
        {
            using var identity = WindowsIdentity.GetCurrent();
            var operation = ParseHelper(args, identity.User!.Value);
            if (!IsAdministrator()) throw new UnauthorizedAccessException("Startup helper requires UAC elevation.");
            if (args.Length == 4) options = options with { LogonDelaySeconds = HelperDelay(args) };
            var target = Target(options, Environment.ProcessPath ?? "", identity.User.Value);
            if (!File.Exists(target.Executable)) throw new FileNotFoundException("Application exe is missing.");
            Apply(operation, target, new WindowsStartupStore());
        }
        catch (Exception ex)
        {
            exitCode = ex is UnauthorizedAccessException ? 5 : Classify(ex) switch
            {
                StartupFailure.RollbackIncomplete => 6,
                StartupFailure.AccessDenied => 7,
                StartupFailure.OwnershipConflict => 8,
                _ => 4,
            };
            try { log(ex); } catch { /* Keep the failure exit status even if logging fails. */ }
        }
        return true;
    }

    // STA worker keeps ShellExecute/UAC and task COM off the WPF dispatcher. Timeout is uncertainty,
    // not cancellation: do not kill or replay a helper that may already have committed a task.
    private static int _helperPending;
    public static bool IsHelperPending => Volatile.Read(ref _helperPending) != 0;

    public static Task<StartupResult> ChangeAsync(StartupOperation operation, StartupOptions options)
    {
        if (Interlocked.CompareExchange(ref _helperPending, 1, 0) != 0)
            return Task.FromResult(new StartupResult(StartupOutcome.Uncertain, "A startup helper is still running."));
        var completion = new TaskCompletionSource<StartupResult>(TaskCreationOptions.RunContinuationsAsynchronously);
        var thread = new Thread(() =>
        {
            bool watching = false;
            StartupResult result;
            try
            {
                if (!Enum.IsDefined(operation)) throw new ArgumentOutOfRangeException(nameof(operation));
                using var identity = WindowsIdentity.GetCurrent();
                var target = Target(options, Environment.ProcessPath ?? "", identity.User!.Value);
                result = Request(operation, target, info =>
                {
                    var process = Process.Start(info) ?? throw new IOException("Could not start the UAC helper.");
                    if (process.WaitForExit(60000))
                    {
                        using (process) return process.ExitCode;
                    }
                    watching = true;
                    _ = Task.Run(() =>
                    {
                        try { process.WaitForExit(); }
                        finally { process.Dispose(); Interlocked.Exchange(ref _helperPending, 0); }
                    });
                    return null;
                }, new WindowsStartupStore());
            }
            catch (Exception ex) { result = new(StartupOutcome.Failed, ex.ToString(), Classify(ex)); }
            if (!watching) Interlocked.Exchange(ref _helperPending, 0);
            completion.SetResult(result);
        }) { IsBackground = true };
        try
        {
            thread.SetApartmentState(ApartmentState.STA);
            thread.Start();
        }
        catch (Exception ex)
        {
            Interlocked.Exchange(ref _helperPending, 0);
            completion.SetResult(new(StartupOutcome.Failed, ex.ToString()));
        }
        return completion.Task;
    }

    // runHelper returns null on timeout. Injection here verifies UAC outcomes without launching a process.
    public static StartupResult Request(StartupOperation operation, StartupTarget target,
        Func<ProcessStartInfo, int?> runHelper, IStartupStore store)
    {
        bool committed = false;
        try
        {
            if (!Enum.IsDefined(operation)) throw new ArgumentOutOfRangeException(nameof(operation));
            var info = new ProcessStartInfo(target.Executable) {
                UseShellExecute = true, Verb = "runas", WorkingDirectory = Path.GetDirectoryName(target.Executable)!,
                WindowStyle = ProcessWindowStyle.Hidden };
            info.ArgumentList.Add(HelperSwitch);
            info.ArgumentList.Add(operation.ToString().ToLowerInvariant());
            ValidateDelay(target.Options.LogonDelaySeconds);
            info.ArgumentList.Add(target.UserSid);
            info.ArgumentList.Add(target.Options.LogonDelaySeconds.ToString(CultureInfo.InvariantCulture));
            int? code = runHelper(info);
            if (code is null) return new(StartupOutcome.Uncertain, "Startup helper is still running; read state before retrying.");
            if (code == 5) return new(StartupOutcome.Failed, "UAC helper must be elevated in the requesting administrator's own account; no changes made.", StartupFailure.AccountMismatch);
            if (code is 6 or 7 or 8) return new(StartupOutcome.Failed, $"Startup helper exited {code}; see startup-helper.log.",
                code == 6 ? StartupFailure.RollbackIncomplete : code == 7 ? StartupFailure.AccessDenied : StartupFailure.OwnershipConflict);
            if (code != 0) return new(StartupOutcome.Failed, $"Startup helper exited {code}; see the application log.");
            committed = true;
            bool valid = operation is StartupOperation.Uninstall or StartupOperation.Plain ? store.ReadTask(target.TaskName) is null
                : Matches(store.ReadTask(target.TaskName), target);
            return valid && store.ReadRun(target.Options.AppId) ==
                (operation == StartupOperation.Plain ? PlainCommand(target) : null) &&
                (target.Options.LegacyRunValueName is not { } legacy || store.ReadRun(legacy) is null)
                ? new(StartupOutcome.Applied) : new(StartupOutcome.Uncertain, "Post-helper readback failed; read state before retrying.");
        }
        catch (Win32Exception ex) when (ex.NativeErrorCode == 1223)
        { return new(StartupOutcome.Cancelled); }
        catch (Exception ex) { return new(committed ? StartupOutcome.Uncertain : StartupOutcome.Failed, ex.ToString(), Classify(ex)); }
    }
}

// Windows-only adapter. The engine above is independently testable without touching OS state.
public sealed class WindowsStartupStore : IStartupStore
{
    private const string RunKey = @"Software\Microsoft\Windows\CurrentVersion\Run";

    private static T WithFolder<T>(Func<dynamic, T> action)
    {
        object? service = null, folder = null;
        try
        {
            service = Activator.CreateInstance(Type.GetTypeFromProgID("Schedule.Service")!);
            ((dynamic)service!).Connect();
            folder = ((dynamic)service).GetFolder(@"\");
            return action(folder!);
        }
        finally { Release(folder); Release(service); }
    }
    private static void Release(object? value)
    {
        if (value is not null && Marshal.IsComObject(value)) Marshal.FinalReleaseComObject(value);
    }
    public string? ReadTask(string name) => WithFolder<string?>(folder =>
    {
        object? task = null;
        try { task = folder.GetTask(name); return (string)((dynamic)task).Xml; }
        catch (COMException ex) when (ex.HResult == unchecked((int)0x80070002)) { return null; }
        finally { Release(task); }
    });
    public void WriteTask(string name, string xml, string userSid) => WithFolder(folder =>
    {
        object? task = null;
        // Explicit DACL prevents an ordinary-user principal ACE from permitting task modification.
        // Do not add a principal write ACE or fire registration triggers during restore.
        try { task = folder.RegisterTask(name, xml, 6 | 0x10 | 0x20, userSid, null, 3,
            $"D:P(A;;FA;;;SY)(A;;FA;;;BA)(A;;FR;;;{userSid})"); return true; }
        finally { Release(task); }
    });
    public void DeleteTask(string name) => WithFolder(folder =>
    {
        try { folder.DeleteTask(name, 0); }
        catch (COMException ex) when (ex.HResult == unchecked((int)0x80070002)) { }
        return true;
    });
    public string? ReadRun(string valueName)
    {
        using var key = Registry.CurrentUser.OpenSubKey(RunKey);
        object? value = key?.GetValue(valueName, null, RegistryValueOptions.DoNotExpandEnvironmentNames);
        if (value is not null && (value is not string || key!.GetValueKind(valueName) != RegistryValueKind.String))
            throw new IOException("Unexpected Run value type; preserve it and migrate explicitly.");
        return (string?)value;
    }
    public void WriteRun(string valueName, string? command)
    {
        using var key = Registry.CurrentUser.CreateSubKey(RunKey);
        if (command is null) key.DeleteValue(valueName, false);
        else key.SetValue(valueName, command, RegistryValueKind.String);
    }
}
