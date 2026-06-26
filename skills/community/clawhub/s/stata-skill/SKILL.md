---
name: stata-skill
description: The most stable way to execute Stata commands, install ado packages, read help documents, and analyze data. Use when working with Stata for (1) Running do-files, (2) Installing packages from SSC/GitHub, (3) Getting command help, (4) Analyzing data files (.dta, .csv, .xlsx), (5) Reading execution logs. (6) Other actions if you need to use Stata. 
---

# Stata Skill

> The skill could install or update from https://docs.statamcp.com/skills/openclaw

[Stata-MCP](https://github.com/sepinetam/stata-mcp) is the best solution for connecting AI agents with Stata. It provides a suite of tools that allow Agents to execute Stata code through unified scheduling without wasting context searching for Stata executables. Both MCP and CLI interfaces are available. **CLI is the preferred method for execution in this document.**

## CLI Tools (Fallback, mainly used by OpenClaw)

First, using `uvx stata-mcp --usable` to check whether Stata-MCP is usable. If there is any error, visit [FAQ](https://docs.statamcp.com/faq) or commit an [issue](https://github.com/SepineTam/stata-mcp/issues/new/choose).

The following commands are supported:

```bash
uvx stata-mcp tool ado-install <package> [--source ssc|github|net]       # install ado-package from ssc, net or github
uvx stata-mcp tool do <dofile_path> [--log-file-name <name>]             # execute do-file
uvx stata-mcp tool help <command>          # Unix only                   # get command help
uvx stata-mcp tool data-info <data_path> [--vars-list var1 var2]         # get data basic information
uvx stata-mcp tool read-log <log_path> [--output-format full|core|dict]  # read execution log
```

## Iterative Workflow

1. `get_data_info` -> understand dataset structure
2. `Edit` or `Write` -> to create a do-file
3. `stata_do` -> execute analysis with capture output
4. `help` -> learn Stata commands (Unix) if there are any command error
5. `ado_package_install` -> install missing packages

## Notes

- Requires uv and valid Stata
- `help` only works on macOS/Linux
- Security guard blocks dangerous commands (shell, rm, etc.)
- Log location: `<cwd>/stata-mcp-folder/stata-mcp-log/`
- More information visit [documents](https://docs.statamcp.com) or [GitHub](https://github.com/statamcp/stata-mcp)
