import os
import requests
import urllib3
from mcp.server.fastmcp import FastMCP

# Disable insecure request warnings for VCF self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize the MCP Server
mcp = FastMCP("VCF-LCM-Precheck-Analyzer")

@mcp.tool()
def analyze_lcm_precheck() -> str:
    """
    Retrieves the most recent LCM upgrade pre-check results from SDDC Manager 
    and summarizes any failures, warnings, and necessary remediation steps.
    """
    host = os.getenv("SDDCMANAGER_HOST")
    token = os.getenv("SDDCMANAGER_API_TOKEN")

    if not host or not token:
        return "Error: SDDCMANAGER_HOST and SDDCMANAGER_API_TOKEN environment variables must be set."

    # Standard VCF API endpoint for pre-checks
    url = f"https://{host}/v1/upgrades/prechecks"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        
        elements = data.get("elements", [])
        if not elements:
            return "No recent upgrade pre-checks found in SDDC Manager."
        
        # Analyze the most recent pre-check execution
        latest_precheck = elements[0]
        result_status = latest_precheck.get("resultStatus", "UNKNOWN")
        
        output = f"Latest Pre-check Status: {result_status}\n"
        output += "=" * 40 + "\n\n"
        
        if result_status == "SUCCEEDED":
            output += " All pre-checks passed! The environment is ready for upgrade."
            return output
            
        output += "Identified Issues & Remediation:\n\n"
        
        # Parse resource-level results and extract failures/warnings
        for resource in latest_precheck.get("resourcePrecheckResults", []):
            res_name = resource.get("resourceName", "Unknown Resource")
            for check in resource.get("checks", []):
                if check.get("resultStatus") in ["FAILED", "WARNING"]:
                    output += f"[{check.get('resultStatus')}] Component: {res_name}\n"
                    output += f"  Issue: {check.get('description', 'No description provided')}\n"
                    output += f"  Action Required: {check.get('remediation', 'Review SDDC Manager UI for details')}\n\n"
                    
        return output

    except requests.exceptions.RequestException as e:
        return f"Failed to retrieve pre-checks from SDDC Manager API: {str(e)}"

if __name__ == "__main__":
    mcp.run()