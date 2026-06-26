# Eval 3 Fixture

This fixture validates the quick-scan path for a plain HTML site without
launching a browser during eval execution.

## Expected Behavior

- Exactly one page is represented.
- No markdown report is generated.
- The conversational summary data contains one critical violation from
  `button-name`.
- Lighthouse remains skipped because quick checks do not require it.
