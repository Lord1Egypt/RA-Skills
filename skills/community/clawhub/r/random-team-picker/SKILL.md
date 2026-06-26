# random-team-picker

Randomly select team members for meetings, code reviews, or activities. Supports weighted selection, exclusion lists, and team splitting.

## Features

- Pick N random members from a list
- Split a group into N teams
- Weighted random selection (higher weight = more likely to be picked)
- Exclude certain members (e.g., on vacation)
- Ensure fair distribution over multiple rounds

## Usage

```
pick --from "Alice,Bob,Charlie,Dave,Eve" --count 2
pick --teams "Alice,Bob,Charlie,Dave" --num-teams 2
pick --from "Alice,Bob,Charlie" --weighted "Alice:3,Bob:2,Charlie:1"
pick --from "Alice,Bob,Charlie" --exclude "Alice" --count 1
```

## Parameters

- `from`: Comma-separated list of member names
- `count`: Number of members to pick (default: 1)
- `num_teams`: Number of teams to split into
- `weighted`: Weighted selection in format "name:weight" pairs
- `exclude`: Members to exclude from selection

## ⚠️ Disclaimer

This tool is provided "as is" for informational purposes only. Data accuracy is not guaranteed. Not financial, legal, or professional advice. Always verify critical information from official sources.

本工具仅供信息参考，不保证数据完全准确，不构成任何金融/法律/专业建议。请以官方来源为准。
