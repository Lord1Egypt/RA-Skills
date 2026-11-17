# Aliyun CLI Install & Credential Check

This skill uses Alibaba Cloud International (alibabacloud.com). Prices are USD.

## Install (need 3.x)

```bash
# macOS
brew install aliyun-cli && brew upgrade aliyun-cli
# Linux
wget https://aliyuncli.alicdn.com/aliyun-cli-linux-latest-amd64.tgz
tar -xzf aliyun-cli-linux-latest-amd64.tgz && sudo mv aliyun /usr/local/bin/

aliyun version   # verify 3.x
```

## Command form

All queries use the PascalCase native form straight to OpenAPI (including `aliyun cms
DescribeMetricList`, `DescribeMonitoringAgentStatuses`); no plugin dependency.

Parameter shapes, time formats, and response-parsing gotchas are in `api_gotchas.md`.

## Credential check (read status only)

```bash
aliyun configure list
```

- **Never** read, echo, print, or ask for AK/SK/STS tokens.
- **Never** run `aliyun configure set` with literal credential values in this session.
- If no valid profile exists, stop and ask the user to configure credentials **outside** this
  session (terminal `aliyun configure`, or environment variables). Resume once
  `aliyun configure list` shows a valid profile.

## Region

Use `region_id` from `.qwencloud-deploy` for every call.

## References

- CLI docs: https://help.aliyun.com/zh/cli/
- AccessKey management: https://ram.console.aliyun.com/manage/ak
