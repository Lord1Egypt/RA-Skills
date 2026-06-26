# Todoist Manager Security & Privacy Guidelines

*   **API Token**: The Todoist API token must be kept confidential. It is loaded via the `TODOIST_API_KEY` environment variable. Ensure this variable is never exposed in logs or shared code.
*   **Data Handling**: Tasks often contain sensitive data (e.g., project names, deadlines, personal notes). Do not use any public or unencrypted logging methods within the implemented Python script that output task content or IDs.
*   **Error Reporting**: Ensure your API implementation handles errors gracefully without leaking details about the request structure or the authentication failure to the console/logs, outside of what is strictly necessary for debugging (and only when debugging is explicitly enabled).