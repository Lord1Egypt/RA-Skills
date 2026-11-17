#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read a .sav (SPSS) data file and print a short summary.

The file path is passed as argv[1] and is used ONLY as a filesystem path
argument -- never interpolated into source code -- so an untrusted path
cannot break out into code injection (SDI-1 fix in statsoft-spss.ps1).
"""
import sys


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("usage: _data_info.py <data_file>\n")
        return 1
    path = sys.argv[1]
    try:
        import pyreadstat
    except ImportError:
        sys.stderr.write("ERROR: pyreadstat is required (pip install pyreadstat)\n")
        return 1
    try:
        df, meta = pyreadstat.read_sav(path)
    except Exception as exc:  # pragma: no cover - defensive
        sys.stderr.write("ERROR: %s\n" % (exc,))
        return 1
    print("Variables:", len(df.columns), "Rows:", len(df))
    print(df.head(20).to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
