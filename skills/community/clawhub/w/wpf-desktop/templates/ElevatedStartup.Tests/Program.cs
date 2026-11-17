// Dependency-free regression runner. Never instantiate WindowsStartupStore or call ChangeAsync here.
using DesktopStartup;
using System.Runtime.InteropServices;
using System.ComponentModel;
using System.Xml.Linq;

var options = new StartupOptions("Example.Tests." + Guid.NewGuid().ToString("N"), "Example.exe");
var target = ElevatedStartup.Target(options, @"D:\便携 & apps\Example.exe", "S-1-5-21-1-2-3-1001");
string desired = ElevatedStartup.TaskXml(target);
if (args.SequenceEqual(["--validate-xml"]))
{
    object? service = null, definition = null;
    try
    {
        service = Activator.CreateInstance(Type.GetTypeFromProgID("Schedule.Service")!);
        ((dynamic)service!).Connect();
        foreach (int seconds in new[] { 0, 3, 17, 300 })
        {
            var configured = target with { Options = target.Options with { LogonDelaySeconds = seconds } };
            definition = ((dynamic)service).NewTask(0);
            ((dynamic)definition).XmlText = ElevatedStartup.TaskXml(configured);
            if ((int)((dynamic)definition).Settings.Priority != 4 ||
                !ElevatedStartup.Matches((string)((dynamic)definition).XmlText, configured))
                throw new Exception("Native XML readback mismatch at delay " + seconds);
            Console.WriteLine("Task Scheduler parsed/read back Normal priority and delay " + seconds + "; no task registered.");
            Marshal.FinalReleaseComObject(definition);
            definition = null;
        }
    }
    finally
    {
        foreach (var value in new[] { definition, service })
            if (value is not null && Marshal.IsComObject(value)) Marshal.FinalReleaseComObject(value);
    }
    return;
}
int passed = 0;
void Check(bool condition, string message = "Assertion failed")
{ if (!condition) throw new Exception(message); }
void Test(string name, Action test)
{
    try { test(); passed++; Console.WriteLine("PASS " + name); }
    catch (Exception ex) { Console.Error.WriteLine("FAIL " + name + ": " + ex); Environment.Exit(1); }
}
Exception Error(Action action)
{
    try { action(); } catch (Exception ex) { return ex; }
    throw new Exception("Expected a failure");
}
string Changed(string xml, string name, string value)
{
    var document = XDocument.Parse(xml);
    document.Descendants().Single(e => e.Name.LocalName == name).Value = value;
    return document.ToString();
}

Test("Chinese, spaces and XML metacharacters survive task XML", () =>
{
    var xml = XDocument.Parse(desired);
    Check(xml.Descendants().Single(e => e.Name.LocalName == "Command").Value == target.Executable);
    Check(ElevatedStartup.Matches(desired, target));
    Check(!desired.Contains("cmd /c", StringComparison.OrdinalIgnoreCase));
});
Test("the current apphost path works independently of bundle extraction", () =>
{
    var current = ElevatedStartup.Target(new(options.AppId, "ElevatedStartup.Tests.exe"),
        Environment.ProcessPath!, target.UserSid);
    Check(current.Executable == Environment.ProcessPath);
    Check(ElevatedStartup.Matches(ElevatedStartup.TaskXml(current), current));
});
Test("legacy outer quotes normalize; appended command arguments do not", () =>
{
    Check(ElevatedStartup.Matches(Changed(desired, "Command", "\"" + target.Executable + "\""), target));
    Check(!ElevatedStartup.Matches(Changed(desired, "Command", "\"" + target.Executable + "\" --tray"), target));
    Check(!ElevatedStartup.Matches(Changed(desired, "Command", @"D:\Other\Example.exe"), target));
});
Test("relative paths and development hosts are rejected", () =>
{
    Error(() => ElevatedStartup.NormalizePath("Example.exe"));
    Error(() => ElevatedStartup.Target(options, @"C:\dotnet\dotnet.exe", target.UserSid));
    Error(() => ElevatedStartup.Target(new("../other", "Example.exe"), target.Executable, target.UserSid));
});
Test("helper accepts only fixed startup operations for the original account", () =>
{
    foreach (var operation in new[] { "install", "repair", "uninstall", "plain" })
        ElevatedStartup.ParseHelper([ElevatedStartup.HelperSwitch, operation, target.UserSid], target.UserSid);
    Error(() => ElevatedStartup.ParseHelper([ElevatedStartup.HelperSwitch, "install", "S-1-5-18"], target.UserSid));
    Error(() => ElevatedStartup.ParseHelper([ElevatedStartup.HelperSwitch, "run", target.UserSid], target.UserSid));
    Error(() => ElevatedStartup.ParseHelper([ElevatedStartup.HelperSwitch, "install", target.UserSid, "arbitrary.exe"], target.UserSid));
});
Test("task names isolate users", () =>
{
    var other = ElevatedStartup.Target(options, target.Executable, "S-1-5-21-1-2-3-1002");
    Check(other.TaskName != target.TaskName);
    Check(!ElevatedStartup.Matches(ElevatedStartup.TaskXml(other), target));
});
Test("UAC cancellation changes no startup state", () =>
{
    var store = new MemoryStore { Run = "previous", FailRead = true };
    var result = ElevatedStartup.Request(StartupOperation.Install, target, _ => throw new Win32Exception(1223), store);
    Check(result.Outcome == StartupOutcome.Cancelled && store.Writes == 0 && store.Run == "previous");
});
Test("the launch request fixes the exe, runas verb, operation and requester SID", () =>
{
    var store = new MemoryStore { Task = desired };
    var result = ElevatedStartup.Request(StartupOperation.Install, target, info =>
    {
        Check(info.FileName == target.Executable && info.Verb == "runas" && info.UseShellExecute);
        Check(info.ArgumentList.SequenceEqual([ElevatedStartup.HelperSwitch, "install", target.UserSid, "3"]));
        return 0;
    }, store);
    Check(result.Outcome == StartupOutcome.Applied && store.Writes == 0);
});
Test("timeout is uncertainty and never replays the helper", () =>
{
    int launches = 0;
    var store = new MemoryStore { Run = "previous", FailRead = true };
    var result = ElevatedStartup.Request(StartupOperation.Repair, target, _ => { launches++; return null; }, store);
    Check(result.Outcome == StartupOutcome.Uncertain && launches == 1 && store.Writes == 0);
});
Test("post-helper access denial is uncertainty, not a claimed rollback", () =>
{
    var result = ElevatedStartup.Request(StartupOperation.Install, target, _ => 0, new MemoryStore { FailRead = true });
    Check(result.Outcome == StartupOutcome.Uncertain);
});
Test("helper account mismatch and registration failure are distinct", () =>
{
    var store = new MemoryStore { FailRead = true };
    var mismatch = ElevatedStartup.Request(StartupOperation.Install, target, _ => 5, store);
    var failure = ElevatedStartup.Request(StartupOperation.Install, target, _ => 4, store);
    Check(mismatch.Outcome == StartupOutcome.Failed && mismatch.Detail!.Contains("account"));
    Check(failure.Outcome == StartupOutcome.Failed && failure.Detail!.Contains("exited 4"));
    Check(store.Writes == 0);
});
Test("privilege, logon, battery and lifetime changes fail readback", () =>
{
    foreach (var (name, value) in new[] { ("RunLevel", "LeastPrivilege"), ("LogonType", "Password"),
        ("DisallowStartIfOnBatteries", "true"), ("StopIfGoingOnBatteries", "true"),
        ("ExecutionTimeLimit", "PT72H"), ("MultipleInstancesPolicy", "Parallel"), ("Arguments", "--help"),
        ("RunOnlyIfIdle", "true"), ("RunOnlyIfNetworkAvailable", "true") })
        Check(!ElevatedStartup.Matches(Changed(desired, name, value), target), name);
});
Test("install verifies the task before removing plain startup", () =>
{
    var store = new MemoryStore { Run = "old ordinary startup" };
    var result = ElevatedStartup.Apply(StartupOperation.Install, target, store);
    Check(result.Outcome == StartupOutcome.Applied && store.Run is null);
    Check(ElevatedStartup.Matches(store.Task, target));
    Check(store.Trace.IndexOf("ReadTask:verified") < store.Trace.IndexOf("WriteRun:remove"));
});
Test("repair repoints a moved portable exe", () =>
{
    var store = new MemoryStore { Task = Changed(desired, "Command", @"C:\Old\Example.exe") };
    ElevatedStartup.Apply(StartupOperation.Repair, target, store);
    Check(ElevatedStartup.Matches(store.Task, target));
});
Test("repair re-enables a disabled task", () =>
{
    var xml = XDocument.Parse(desired);
    xml.Descendants().Where(e => e.Name.LocalName == "Enabled").Last().Value = "false";
    var store = new MemoryStore { Task = xml.ToString() };
    ElevatedStartup.Apply(StartupOperation.Repair, target, store);
    Check(ElevatedStartup.Matches(store.Task, target));
});
Test("repair removes unconfigured trigger expiration, start bounds and delays", () =>
{
    foreach (var (name, value) in new[] { ("StartBoundary", "2099-01-01T00:00:00"),
        ("EndBoundary", "2000-01-01T00:00:00"), ("Delay", "PT24H") })
    {
        var xml = XDocument.Parse(desired);
        var trigger = xml.Descendants().Single(e => e.Name.LocalName == "LogonTrigger");
        trigger.AddFirst(new XElement(trigger.Name.Namespace + name, value));
        var store = new MemoryStore { Task = xml.ToString() };
        Check(!ElevatedStartup.Matches(store.Task, target));
        Check(ElevatedStartup.Apply(StartupOperation.Repair, target, store).Outcome == StartupOutcome.Applied);
        Check(ElevatedStartup.Matches(store.Task, target));
    }
});
Test("concurrent helper cannot overwrite a transaction or its rollback snapshot", () =>
{
    using var entered = new ManualResetEventSlim();
    using var release = new ManualResetEventSlim();
    var store = new MemoryStore { BeforeWrite = () => {
        entered.Set();
        if (!release.Wait(TimeSpan.FromSeconds(10))) throw new TimeoutException("test coordination");
    } };
    var first = Task.Run(() => ElevatedStartup.Apply(StartupOperation.Install, target, store));
    try
    {
        Check(entered.Wait(TimeSpan.FromSeconds(10)), "first helper did not acquire its lock");
        int reads = store.Trace.Count;
        var error = Error(() => ElevatedStartup.Apply(StartupOperation.Uninstall, target, store));
        Check(error.Message.Contains("in progress") && store.Trace.Count == reads);
    }
    finally { release.Set(); }
    Check(first.GetAwaiter().GetResult().Outcome == StartupOutcome.Applied);
    Check(ElevatedStartup.Matches(store.Task, target));
});
Test("install, repair and uninstall are idempotent", () =>
{
    var store = new MemoryStore { Task = desired };
    Check(ElevatedStartup.Apply(StartupOperation.Install, target, store).Outcome == StartupOutcome.Unchanged);
    Check(ElevatedStartup.Apply(StartupOperation.Repair, target, store).Outcome == StartupOutcome.Unchanged);
    Check(store.Writes == 0);
    ElevatedStartup.Apply(StartupOperation.Uninstall, target, store);
    int writes = store.Writes;
    Check(store.Task is null && store.Run is null);
    Check(ElevatedStartup.Apply(StartupOperation.Uninstall, target, store).Outcome == StartupOutcome.Unchanged);
    Check(store.Writes == writes);
});
Test("uninstall clears both startup mechanisms", () =>
{
    var store = new MemoryStore { Task = desired, Run = "legacy ordinary startup" };
    ElevatedStartup.Apply(StartupOperation.Uninstall, target, store);
    Check(store.Task is null && store.Run is null);
});
Test("a foreign task is never overwritten or removed", () =>
{
    foreach (var operation in Enum.GetValues<StartupOperation>())
    {
        var store = new MemoryStore { Task = Changed(desired, "Source", "another-app"), Run = "previous" };
        Error(() => ElevatedStartup.Apply(operation, target, store));
        Check(store.Writes == 0 && store.Run == "previous");
    }
});
Test("permission-denied queries preserve uncertainty and make no writes", () =>
{
    var store = new MemoryStore { FailRead = true, Run = "previous" };
    var error = Error(() => ElevatedStartup.Apply(StartupOperation.Install, target, store));
    Check(error.ToString().Contains("80070005") && error.Message.Contains("preflight"));
    Check(store.Writes == 0 && store.Run == "previous");
});
Test("partial registration failure restores the old task and Run entry", () =>
{
    string old = Changed(desired, "Command", @"D:\Old\Example.exe");
    var store = new MemoryStore { Task = old, Run = "previous", FailWriteOnce = true };
    var error = Error(() => ElevatedStartup.Apply(StartupOperation.Repair, target, store));
    Check(store.Task == old && store.Run == "previous");
    Check(error.Message.Contains("previous startup restored"));
});
Test("bad registration readback removes the partial new task", () =>
{
    var store = new MemoryStore { Run = "previous", CorruptWriteOnce = true };
    var error = Error(() => ElevatedStartup.Apply(StartupOperation.Install, target, store));
    Check(store.Task is null && store.Run == "previous");
    Check(error.Message.Contains("verify task"));
});
Test("Run cleanup failure rolls back an already registered task", () =>
{
    var store = new MemoryStore { Run = "previous", FailRunOnce = true };
    Error(() => ElevatedStartup.Apply(StartupOperation.Install, target, store));
    Check(store.Task is null && store.Run == "previous");
});
Test("partial uninstall failure restores both old entries", () =>
{
    var store = new MemoryStore { Task = desired, Run = "previous", FailDeleteOnce = true };
    Error(() => ElevatedStartup.Apply(StartupOperation.Uninstall, target, store));
    Check(store.Task == desired && store.Run == "previous");
});
Test("failed rollback is reported; independent Run restoration is still attempted", () =>
{
    var store = new MemoryStore { Run = "previous", CorruptWriteOnce = true, FailDeleteAlways = true };
    var error = Error(() => ElevatedStartup.Apply(StartupOperation.Install, target, store));
    Check(error.Message.Contains("rollback incomplete"));
    Check(store.Trace.Contains("WriteRun:previous") && store.Run == "previous");
});


Test("configured delay and Normal priority survive generation and readback", () =>
{
    foreach (int seconds in new[] { 0, 3, 17, 300 })
    {
        var configured = target with { Options = target.Options with { LogonDelaySeconds = seconds } };
        string xml = ElevatedStartup.TaskXml(configured);
        Check(ElevatedStartup.Matches(xml, configured));
        Check(XDocument.Parse(xml).Descendants().Single(e => e.Name.LocalName == "Priority").Value == "4");
        Check(!ElevatedStartup.Matches(Changed(xml, "Priority", "7"), configured));
        if (seconds != 0)
        {
            Check(!ElevatedStartup.Matches(Changed(xml, "Delay", "PT1H"), configured));
            Check(!ElevatedStartup.Matches(Changed(xml, "Delay", "bad-duration"), configured));
        }
        var store = new MemoryStore { Task = desired };
        ElevatedStartup.Apply(StartupOperation.Repair, configured, store);
        Check(ElevatedStartup.Matches(store.Task, configured));
    }
});
Test("helper accepts only bounded numeric delay and forwards the configured value", () =>
{
    foreach (string invalid in new[] { "-1", "301", "1.5", "arbitrary.exe", "--show" })
        Error(() => ElevatedStartup.ParseHelper([ElevatedStartup.HelperSwitch, "install", target.UserSid, invalid], target.UserSid));
    var configured = target with { Options = target.Options with { LogonDelaySeconds = 17 } };
    var store = new MemoryStore { Task = ElevatedStartup.TaskXml(configured) };
    var result = ElevatedStartup.Request(StartupOperation.Install, configured, info => {
        Check(info.ArgumentList.SequenceEqual([ElevatedStartup.HelperSwitch, "install", target.UserSid, "17"]));
        Check(ElevatedStartup.HelperDelay(info.ArgumentList.ToArray()) == 17);
        return 0;
    }, store);
    Check(result.Outcome == StartupOutcome.Applied);
    foreach (int invalid in new[] { -1, 301 })
        Error(() => ElevatedStartup.Target(options with { LogonDelaySeconds = invalid }, target.Executable, target.UserSid));
});
Test("normal switch rolls back the task and both Run names together", () =>
{
    var configured = target with { Options = target.Options with { LegacyRunValueName = "Legacy.Tests" } };
    var store = new MemoryStore { Task = desired, Run = "previous", Legacy = "legacy", FailLegacyOnce = true };
    Error(() => ElevatedStartup.Apply(StartupOperation.Plain, configured, store));
    Check(store.Task == desired && store.Run == "previous" && store.Legacy == "legacy");
    ElevatedStartup.Apply(StartupOperation.Plain, configured, store);
    Check(store.Task is null && store.Run == ElevatedStartup.PlainCommand(configured) && store.Legacy is null);
});
Test("overlong Run commands fail before changing either startup mechanism", () =>
{
    var longTarget = ElevatedStartup.Target(options, @"D:\" + new string('a', 260) + @"\Example.exe", target.UserSid);
    var store = new MemoryStore { Task = desired, Run = "previous" };
    Error(() => ElevatedStartup.Apply(StartupOperation.Plain, longTarget, store));
    Check(store.Task == desired && store.Run == "previous" && store.Writes == 0);
});

Console.WriteLine($"{passed} isolated startup checks passed; no OS startup state accessed.");

sealed class MemoryStore : IStartupStore
{
    public string? Task, Run, Legacy;
    public bool FailLegacyOnce;
    public bool FailRead, FailWriteOnce, CorruptWriteOnce, FailRunOnce, FailDeleteOnce, FailDeleteAlways;
    public int Writes;
    public Action? BeforeWrite;
    public List<string> Trace { get; } = [];
    public string? ReadTask(string name)
    {
        if (FailRead) throw new COMException("access denied", unchecked((int)0x80070005));
        Trace.Add(Task is null ? "ReadTask:missing" : "ReadTask:verified");
        return Task;
    }
    public void WriteTask(string name, string xml, string userSid)
    {
        BeforeWrite?.Invoke();
        Writes++;
        Task = xml;
        if (FailWriteOnce) { FailWriteOnce = false; throw new IOException("write failed after mutation"); }
        if (CorruptWriteOnce) { CorruptWriteOnce = false; Task = xml.Replace("HighestAvailable", "LeastPrivilege"); }
    }
    public void DeleteTask(string name)
    {
        Writes++;
        if (FailDeleteAlways) throw new IOException("delete denied");
        Task = null;
        if (FailDeleteOnce) { FailDeleteOnce = false; throw new IOException("delete failed after mutation"); }
    }
    public string? ReadRun(string valueName) => valueName == "Legacy.Tests" ? Legacy : Run;
    public void WriteRun(string valueName, string? command)
    {
        Writes++;
        Trace.Add("WriteRun:" + (command ?? "remove"));
        if (valueName == "Legacy.Tests")
        {
            Legacy = command;
            if (FailLegacyOnce) { FailLegacyOnce = false; throw new IOException("legacy write failed after mutation"); }
            return;
        }
        Run = command;
        if (FailRunOnce) { FailRunOnce = false; throw new IOException("registry write failed after mutation"); }
    }
}
