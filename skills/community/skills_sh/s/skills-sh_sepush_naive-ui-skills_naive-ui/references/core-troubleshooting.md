---
name: core-troubleshooting
description: Naive UI documentation for Troubleshooting and Common Issues
---

# Troubleshooting

## Common Issues Quick Fix

| Issue                                          | Solution                                                     |
| ---------------------------------------------- | ------------------------------------------------------------ |
| InputNumber validation not triggering on input | Use `trigger: ['blur']` or validate manually on blur         |
| Select filter not working with custom render   | Ensure `label` property exists in options for filtering      |
| DataTable fixed column shadow missing          | Use numeric pixel value for `scroll-x` instead of percentage |
| DatePicker throws error with empty string      | Initialize with `null` instead of empty string               |
| Theme colors not applied in dark mode          | Set `primaryColorSuppl` in theme overrides                   |
| Modal cannot focus input inside                | Check `trap-focus` and `auto-focus` props                    |
| Tree data update not triggering render         | Create new array reference when modifying                    |
| Upload accept attribute not working            | Use MIME types instead of file extensions                    |
