import sys
import os

# Add current directory to path to allow importing qc_api
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from qc_api.client import QCApiClient
    from qc_api.config import get_default_project_id

    client = QCApiClient()
    project_id = get_default_project_id()

    print(f"Testing connection for Project ID: {project_id}")
    project_info = client.read_project(project_id)

    if project_info and 'success' in project_info and project_info['success']:
        print("API Connection Successful!")
        print(f"Project Name: {project_info.get('projects', [{}])[0].get('name', 'Unknown')}")
    else:
        print(f"API Request Failed: {project_info}")

except Exception as e:
    print(f"Error during verification: {e}")
