# Existing Deployment Detection (Step 4)

The agent directly executes CLI commands to detect whether ROS stacks created by this tool exist in the current region, then routes based on results.

---

## Query Command

```bash
aliyun ros ListStacks --RegionId "$REGION" \
  --Tag.1.Key from --Tag.1.Value qwencloud
```

---

## Parse Results

Extract the `Stacks` array from the returned JSON. **Filter out** stacks with `Status == "DELETE_COMPLETE"`.

For each surviving stack, read the `qwencloud-appName` tag value and compare with the current project's `APP_NAME`:

| Situation | Meaning |
|-----------|---------|
| A stack exists with `qwencloud-appName == APP_NAME` | **Same project already deployed** |
| Stacks exist but appName doesn't match | **Other project deployments** (no impact) |
| No surviving stacks (or Stacks is empty) | **No existing deployment** |

---

## Routing Decision

| Detection Result | Action |
|-----------------|--------|
| Same project already deployed | AskUserQuestion: ① Hot update (recommended, IP unchanged) ② Delete old stack and redeploy |
| No existing deployment | Continue full-stack deploy (Step 5) |

> User chooses hot update → jump to **Hot Update flow** (U1–U4).
> User chooses delete & redeploy → execute `bash scripts/delete_stack.sh --project-root . --yes` first, wait for completion, then continue full-stack deploy.

---

## Example Output Interpretation

```json
{
  "Stacks": [
    {
      "StackName": "qwencloud-myapp-202607151030",
      "StackId": "abc-123-def",
      "Status": "CREATE_COMPLETE",
      "CreateTime": "2026-07-15T10:30:00",
      "Tags": [
        {"Key": "from", "Value": "qwencloud"},
        {"Key": "qwencloud-appName", "Value": "myapp"}
      ]
    }
  ]
}
```

In this example, `qwencloud-appName` = `myapp`. If the current `APP_NAME` is also `myapp`, this is detected as the same project already deployed.
