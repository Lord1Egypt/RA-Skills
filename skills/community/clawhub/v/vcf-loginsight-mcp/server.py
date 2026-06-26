import os
import requests
import urllib3
from mcp.server.fastmcp import FastMCP

# Disable insecure request warnings for VCF self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize the MCP Server
mcp = FastMCP("VCF-LogInsight-Server")

@mcp.tool()
def query_vcf_logs(keyword: str, limit: int = 15) -> str:
    """
    Search VMware Aria Operations for Logs (Log Insight) for a specific keyword.
    
    Args:
        keyword: The search term (e.g., 'failed', 'esxi', 'vcenter', 'unauthorized').
        limit: The maximum number of log events to retrieve.
    """
    host = os.getenv("LOGINSIGHT_HOST")
    token = os.getenv("LOGINSIGHT_API_TOKEN")

    if not host or not token:
        return "Error: LOGINSIGHT_HOST and LOGINSIGHT_API_TOKEN environment variables must be set."

    url = f"https://{host}/api/v1/events?keyword={keyword}&limit={limit}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        
        events = data.get("events", [])
        if not events:
            return f"No logs found in VCF for keyword: '{keyword}'"
        
        # Format the JSON securely before sending it back to the AI
        result = f"Found {len(events)} events for '{keyword}':\n\n"
        for ev in events:
            timestamp = ev.get("timestamp", "Unknown Time")
            text = ev.get("text", "No text provided")
            source = ev.get("source", "Unknown Source")
            result += f"[{timestamp}] (Source: {source})\nMessage: {text}\n"
            result += "-" * 40 + "\n"
        
        return result

    except requests.exceptions.RequestException as e:
        return f"Failed to query Log Insight API: {str(e)}"

if __name__ == "__main__":
    mcp.run()