# Eval 4 Fixture

This fixture validates degraded report generation when Lighthouse is
unavailable but axe-style scan data exists.

## Expected Behavior

- `report.js` still generates markdown and JSON.
- The Lighthouse skip reason appears in both Executive Summary and
  Methodology.
- JSON output uses `lighthouse.status: "skipped"`.
- No numeric Lighthouse score is invented.
