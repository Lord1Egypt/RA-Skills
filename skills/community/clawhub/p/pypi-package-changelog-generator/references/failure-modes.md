# Failure Modes

- If the package name is missing, ask for it before running the wrapper.
- If neither a version range nor an explicit version pair is available, ask for the missing scope.
- If GitHub API access is rate limited, prefer the retry guidance from the structured error or warning output.
- If repository analysis fails and archive diff is used, say that the result came from source archives rather than git history.
- If truncation is reported, tell the user the summary may omit low-signal files or commits.
