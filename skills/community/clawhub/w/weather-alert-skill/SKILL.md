# Weather Alert Skill

Sends summarized weather alerts for a configured region. Supports severity filtering and returns structured alert counts.

## Inputs

- **region** (string, required): The geographic region to monitor.
- **severity** (string, optional): Filter alerts by severity level. Defaults to "all".

## Outputs

- **alert_count** (number): The number of active alerts matching the query.

## Usage

Provide a `region` and optionally a `severity` to receive a summary of active weather alerts for that area.
