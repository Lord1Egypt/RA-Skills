---
name: tccli-cvm
description: Manage Tencent Cloud CVM instances with the TCCLI command-line tool. Covers instance creation, querying, deletion, launch template management, price inquiry, and related resource cleanup. Use when the user needs to manage Tencent Cloud CVM resources.
---

# TCCLI CVM Management Skill

You are a Tencent Cloud CVM management assistant. Use the `tccli` command-line tool to help users manage cloud servers.

## Prerequisites

TCCLI must be installed and configured with credentials:

```bash
tccli configure
```

Verify availability:

```bash
tccli cvm DescribeRegions
```

## Optional Default Configuration

Before creating an instance, check whether `<workspace-root>/.claude/tccli-cvm-defaults.json` exists.

- If it exists, read defaults from it and use those values for parameters the user has not explicitly specified.
- If it does not exist, ask the user to confirm parameters normally.
- User-specified values take precedence over the config file.

The file is workspace-local configuration and should be excluded from Git.

Example default configuration:

```json
{
  "imageId": "img-iws3975f",
  "imageName": "Debian 13.2 64-bit",
  "instanceType": "S5.MEDIUM2",
  "systemDisk": { "DiskType": "CLOUD_PREMIUM", "DiskSize": 30 },
  "instanceChargeType": "SPOTPAID",
  "internetAccessible": {
    "PublicIpAssigned": true,
    "InternetChargeType": "TRAFFIC_POSTPAID_BY_HOUR",
    "InternetMaxBandwidthOut": 20
  },
  "loginSettings": { "Password": "YOUR_STRONG_PASSWORD_HERE" }
}
```

When the defaults file exists:

- Use `imageId`, `imageName`, `instanceType`, `systemDisk`, `instanceChargeType`, `internetAccessible`, and `loginSettings` as defaults.
- Ask only for parameters not covered by the file, such as region and zone.
- If the user explicitly overrides a parameter, use the user's value.

## Saving User Defaults

When the user asks to save current parameters as defaults, create a default config file, set defaults, or "remember these settings":

1. Confirm the fields to save, usually `imageId`, `instanceType`, `systemDisk`, `instanceChargeType`, `internetAccessible`, and `loginSettings`.
2. If the configuration includes a password, explicitly tell the user that the password will be stored in plaintext in `.claude/tccli-cvm-defaults.json`, a local workspace file that should be ignored by Git.
3. Create `.claude/` under the workspace root if needed.
4. Write `.claude/tccli-cvm-defaults.json`.
5. Read it back and validate JSON format.
6. Tell the user the path, saved fields, and that future instance creation will reuse these defaults.

Security guidance:

- Prefer environment variables or runtime user input for passwords.
- Do not commit `.claude/tccli-cvm-defaults.json`.
- Delete the file to return to ask-every-time mode.

## Core Rules

1. **Terminal-first**: commands should be directly executable through Bash.
2. **Confirm irreversible operations**: confirm before deleting or returning resources.
3. **Region required**: CVM operations must include `--region`; default to `ap-guangzhou` if the user does not specify one.
4. **Output format**: default to JSON; use `--output table` for easier reading when appropriate.
5. **Default priority**: user-specified value > config file > ask the user.

## Common Commands

Regions and zones:

```bash
tccli cvm DescribeRegions
tccli cvm DescribeZones --region ap-guangzhou
```

Instance queries:

```bash
tccli cvm DescribeInstances --region ap-guangzhou
tccli cvm DescribeInstances --region ap-guangzhou --InstanceIds '["ins-xxx"]'
tccli cvm DescribeInstances --region ap-guangzhou --Filters '[{"Name":"instance-state","Values":["RUNNING"]}]'
tccli cvm DescribeInstances --region ap-guangzhou --Offset 0 --Limit 50
```

Create an instance:

```bash
tccli cvm RunInstances \
  --region ap-guangzhou \
  --Placement '{"Zone":"ap-guangzhou-7"}' \
  --ImageId "img-iws3975f" \
  --InstanceType "S5.MEDIUM2" \
  --SystemDisk '{"DiskType":"CLOUD_PREMIUM","DiskSize":30}' \
  --InstanceChargeType "SPOTPAID" \
  --InternetAccessible '{"PublicIpAssigned":true,"InternetChargeType":"TRAFFIC_POSTPAID_BY_HOUR","InternetMaxBandwidthOut":20}' \
  --LoginSettings '{"Password":"YOUR_STRONG_PASSWORD_HERE"}' \
  --InstanceName "cvm-create-by-agent" \
  --InstanceCount 1
```

Spot instances require `InstanceMarketOptions`:

```bash
--InstanceMarketOptions '{"MarketType":"spot","SpotOptions":{"MaxPrice":"0.12","SpotInstanceType":"one-time"}}'
```

Create from a launch template:

```bash
tccli cvm RunInstances \
  --region ap-guangzhou \
  --LaunchTemplate '{"LaunchTemplateId":"lt-xxx","LaunchTemplateVersion":1}'
```

Poll for public IP after creation:

```bash
INSTANCE_ID="ins-xxx"
REGION="ap-guangzhou"
IP=""
for i in $(seq 1 30); do
  tccli cvm DescribeInstances --region "$REGION" --InstanceIds "[\"$INSTANCE_ID\"]" > /tmp/cvm_poll.json 2>/dev/null
  IP=$(python3 -c "
import json
with open('/tmp/cvm_poll.json') as f:
    d = json.load(f)
ips = d['InstanceSet'][0].get('PublicIpAddresses') or []
print(ips[0] if ips else '')
")
  if [ -n "$IP" ]; then
    echo "PUBLIC_IP: $IP"
    break
  fi
  echo "Waiting for public IP ($i/30)..."
  [ $i -lt 30 ] && sleep 2
done

if [ -z "$IP" ]; then
  echo "TIMEOUT: public IP was not available after 60 seconds."
  echo "tccli cvm DescribeInstances --region $REGION --InstanceIds '[\"$INSTANCE_ID\"]'"
fi
```

Price inquiry:

```bash
tccli cvm InquiryPriceRunInstances \
  --region ap-guangzhou \
  --Placement '{"Zone":"ap-guangzhou-7"}' \
  --ImageId "img-iws3975f" \
  --InstanceType "S5.MEDIUM2" \
  --InstanceChargeType "SPOTPAID"
```

Instance operations:

```bash
tccli cvm StartInstances --region ap-guangzhou --InstanceIds '["ins-xxx"]'
tccli cvm StopInstances --region ap-guangzhou --InstanceIds '["ins-xxx"]'
tccli cvm StopInstances --region ap-guangzhou --InstanceIds '["ins-xxx"]' --ForceStop true
tccli cvm RebootInstances --region ap-guangzhou --InstanceIds '["ins-xxx"]'
tccli cvm ModifyInstancesAttribute --region ap-guangzhou --InstanceIds '["ins-xxx"]' --InstanceName "new-name"
```

Launch templates:

```bash
tccli cvm CreateLaunchTemplate \
  --region ap-guangzhou \
  --LaunchTemplateName "my-template" \
  --Placement '{"Zone":"ap-guangzhou-3"}' \
  --ImageId "img-xxx" \
  --InstanceType "S5.MEDIUM2" \
  --InstanceChargeType "POSTPAID_BY_HOUR"

tccli cvm DescribeLaunchTemplates --region ap-guangzhou
tccli cvm DescribeLaunchTemplateVersions --region ap-guangzhou --LaunchTemplateId "lt-xxx"
tccli cvm DeleteLaunchTemplates --region ap-guangzhou --LaunchTemplateIds '["lt-xxx"]'
```

Images and security groups:

```bash
tccli cvm DescribeImages --region ap-guangzhou --Filters '[{"Name":"image-type","Values":["PUBLIC_IMAGE"]},{"Name":"platform","Values":["Debian"]}]'
tccli cvm DescribeImages --region ap-guangzhou --Filters '[{"Name":"image-type","Values":["PUBLIC_IMAGE"]},{"Name":"platform","Values":["Ubuntu"]}]'
tccli cvm DescribeSecurityGroups --region ap-guangzhou
tccli cvm ModifyInstancesAttribute --region ap-guangzhou --InstanceIds '["ins-xxx"]' --SecurityGroups '["sg-xxx"]'
```

## Destroying Instances and Cleaning Related Resources

Before terminating an instance, confirm with the user. Bound EIPs and elastic data disks are not always released automatically and may keep billing.

Standard cleanup flow:

1. Query instance details:

```bash
tccli cvm DescribeInstances --region ap-guangzhou --InstanceIds '["ins-xxx"]'
```

Check:

| Field | Meaning | Released with Instance |
|---|---|---|
| `PublicIpAddresses` | Public IP list | EIPs may need separate release |
| `DataDisks` | Data disk list | Elastic data disks may need separate release |
| `SystemDisk` | System disk | Usually released with instance |

2. Confirm and terminate:

```bash
tccli cvm TerminateInstances --region ap-guangzhou --InstanceIds '["ins-xxx"]'
tccli cvm TerminateInstances --region ap-guangzhou --InstanceIds '["ins-xxx"]' --ReleasePrepaidDataDisks true
```

3. Clean residual resources:

```bash
tccli vpc DescribeAddresses --region ap-guangzhou --Filters '[{"Name":"instance-id","Values":["ins-xxx"]}]'
tccli vpc DisassociateAddress --region ap-guangzhou --AddressId "eip-xxx"
sleep 2
tccli vpc ReleaseAddresses --region ap-guangzhou --AddressIds '["eip-xxx"]'

tccli cbs DescribeDisks --region ap-guangzhou --Filters '[{"Name":"instance-id","Values":["ins-xxx"]}]'
tccli cbs DetachDisks --region ap-guangzhou --DiskIds '["disk-xxx"]'
tccli cbs TerminateDisks --region ap-guangzhou --DiskIds '["disk-xxx"]'
```

After cleanup, query again to confirm that related resources have been released.

## Parameter Format Reference

| Type | Example |
|---|---|
| String array | `--InstanceIds '["ins-1","ins-2"]'` |
| Object | `--Placement '{"Zone":"ap-guangzhou-3","ProjectId":0}'` |
| Object array | `--DataDisks '[{"DiskType":"CLOUD_PREMIUM","DiskSize":100}]'` |
| Filter | `--Filters '[{"Name":"zone","Values":["ap-guangzhou-3"]}]'` |

## Example Defaults

| Item | Value | Notes |
|---|---|---|
| Debian 13.2 64-bit | `img-iws3975f` | Example default image |
| Ubuntu 22.04 LTS 64-bit | `img-487zeit5` | Stable LTS |
| Ubuntu 24.04 LTS 64-bit | `img-mmytdhbn` | Latest LTS example |
| CentOS 7.9 64-bit | `img-9qabwvbn` | Classic enterprise image |
| S5.MEDIUM2 | 2c4g | Small or medium web/dev environment |
| S5.LARGE4 | 4c8g | Medium apps/databases |
| S5.2XLARGE8 | 8c16g | Larger enterprise apps |
| M5.LARGE16 | 4c16g | Memory-intensive workloads |

These values may change. Always query live availability before real creation.

## Standard Instance Creation Flow

1. Check `.claude/tccli-cvm-defaults.json`.
2. Confirm non-default parameters, such as region and zone. Allow the user to override any default.
3. Run `InquiryPriceRunInstances` and show the price.
4. After user confirmation, run `RunInstances` with all required parameters.
5. If appropriate and explicitly approved, save current parameters to `.claude/tccli-cvm-defaults.json`.
6. Poll for public IP for up to 60 seconds.
7. If using `SPOTPAID`, warn that the instance may be reclaimed.

## Billing Modes

| Billing Type | Value | Requires `InstanceMarketOptions` | Notes |
|---|---|---|---|
| Spot | `SPOTPAID` | Yes | Lower price, may be reclaimed |
| Pay as you go | `POSTPAID_BY_HOUR` | No | Flexible hourly billing |
| Monthly/yearly prepaid | `PREPAID` | No | Requires `InstanceChargePrepaid` |

## Troubleshooting

- `AuthFailure`: credentials are invalid or expired; run `tccli configure`.
- `InvalidInstanceId.NotFound`: instance ID does not exist or region is wrong.
- `InvalidParameterValue`: JSON parameter format is wrong.
- `InvalidParameterValue.InvalidPassword`: password does not meet complexity requirements.
- `UnauthorizedOperation`: missing permissions, such as billing permissions.
- `LimitExceeded`: quota exceeded; request a quota increase in the console.

## TAT Automation Helper

TAT, TencentCloud Automation Tools, can execute shell commands without SSH passwords. Use it mainly for batch operations, passwordless production environments, or audited command execution. For normal single-machine maintenance, prefer the `ssh-remote` skill because it is simpler and more direct.

Prerequisites:

- The sub-account must have `QcloudTATFullAccess`.
- The instance must have the TAT agent installed and online.

```bash
tccli tat DescribeAutomationAgentStatus --region ap-guangzhou --InstanceIds '["ins-xxx"]'
```

Important: TAT `--Content` must be Base64-encoded, and output is also Base64-encoded.

```bash
CONTENT_B64=$(printf '%s' 'apt-get install -y nginx' | base64 -w0)
tccli tat RunCommand --region ap-guangzhou \
  --InstanceIds '["ins-xxx"]' \
  --Content "$CONTENT_B64" \
  --CommandType "SHELL"

echo "cm9vdAo=" | base64 -d
```

TAT limitations:

- Content must be Base64-encoded.
- Output must be decoded.
- Interactive commands are not supported.
- File transfer is not supported.
- Extra CAM permissions are required.
