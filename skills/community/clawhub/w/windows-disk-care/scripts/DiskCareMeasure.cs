using System;
using System.IO;
using System.Collections.Generic;
public class DiskCareSize {
    public string Path;
    public long Bytes;
    public long Files;
    public DateTime LatestWriteUtc;
}
public class DiskCareMeasure {
    public List<DiskCareSize> Directories = new List<DiskCareSize>();
    public List<DiskCareSize> LargeFiles = new List<DiskCareSize>();
    public List<string> Errors = new List<string>();
    public List<string> Links = new List<string>();
    public long ErrorCount;
    public long LinkCount;
    public long Minimum;
    public DiskCareSize Scan(string path) {
        var result = new DiskCareSize { Path = Path.GetFullPath(path), LatestWriteUtc = DateTime.MinValue };
        try {
            var dir = new DirectoryInfo(path);
            if ((dir.Attributes & FileAttributes.ReparsePoint) != 0) {
                LinkCount++; if (Links.Count < 200) Links.Add(path); return result;
            }
            foreach (var item in dir.EnumerateFileSystemInfos()) {
                try {
                    if ((item.Attributes & FileAttributes.ReparsePoint) != 0) {
                        LinkCount++; if (Links.Count < 200) Links.Add(item.FullName); continue;
                    }
                    if ((item.Attributes & FileAttributes.Directory) != 0) {
                        var sub = Scan(item.FullName);
                        result.Bytes += sub.Bytes; result.Files += sub.Files;
                        if (sub.LatestWriteUtc > result.LatestWriteUtc) result.LatestWriteUtc = sub.LatestWriteUtc;
                    } else {
                        var f = (FileInfo)item;
                        result.Bytes += f.Length; result.Files++;
                        if (f.LastWriteTimeUtc > result.LatestWriteUtc) result.LatestWriteUtc = f.LastWriteTimeUtc;
                        if (f.Length >= 512L*1024*1024) LargeFiles.Add(new DiskCareSize {Path=f.FullName, Bytes=f.Length, Files=1, LatestWriteUtc=f.LastWriteTimeUtc});
                    }
                } catch (Exception ex) { ErrorCount++; if (Errors.Count < 200) Errors.Add(item.FullName + " :: " + ex.GetType().Name); }
            }
        } catch (Exception ex) { ErrorCount++; if (Errors.Count < 200) Errors.Add(path + " :: " + ex.GetType().Name); }
        if (result.Bytes >= Minimum) Directories.Add(result);
        return result;
    }
}
