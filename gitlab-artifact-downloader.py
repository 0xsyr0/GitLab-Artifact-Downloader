import requests

GITLAB_URL = "https://gitlab.com"
PROJECT_ID = "<ACCOUNT_NAME>%2F<PROJECT>"
TOKEN = "glpat-XXXXXXXXXXXXXXXXXXXX"
BRANCH = "main"
OUTPUT_FILE = "artifact.zip"

headers = {
    "PRIVATE-TOKEN": TOKEN
}

pipeline_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/pipelines"
params = {"ref": BRANCH, "status": "success", "order_by": "updated_at", "sort": "desc"}
resp = requests.get(pipeline_url, headers=headers, params=params)
resp.raise_for_status()
pipelines = resp.json()
if not pipelines:
    raise Exception("No successful pipelines found.")
pipeline_id = pipelines[0]["id"]

jobs_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/pipelines/{pipeline_id}/jobs"
resp = requests.get(jobs_url, headers=headers)
resp.raise_for_status()
jobs = [job for job in resp.json() if job["artifacts_file"]["filename"]]

if not jobs:
    raise Exception("No jobs with artifacts found.")

job_id = jobs[0]["id"]
artifact_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/jobs/{job_id}/artifacts"

resp = requests.get(artifact_url, headers=headers)
resp.raise_for_status()

with open(OUTPUT_FILE, "wb") as f:
    f.write(resp.content)

print(f"[+] Artifact saved as {OUTPUT_FILE}")
