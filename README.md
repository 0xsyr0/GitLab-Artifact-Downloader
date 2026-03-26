# gitlab-artifact-fetch

A minimal Python utility to retrieve the latest build artifact from a GitLab CI/CD pipeline via the GitLab REST API.

## Overview

`gitlab-artifact-fetch` queries a target project's pipeline history, identifies the most recent successful run, and downloads its artifact archive to disk. Useful for automating artifact retrieval in scripts, assessments, or tooling pipelines where GitLab access tokens are available.

## Requirements

- Python 3.7+
- `requests`
```bash
pip install requests
```

## Configuration

Edit the constants at the top of the script before use:

| Variable | Description |
|---|---|
| `GITLAB_URL` | Base URL of the GitLab instance |
| `PROJECT_ID` | URL-encoded project path (e.g. `user%2Frepo`) |
| `TOKEN` | GitLab Personal Access Token (`glpat-...`) |
| `BRANCH` | Target branch to query pipelines from |
| `OUTPUT_FILE` | Filename for the downloaded artifact archive |

## Token Setup

Navigate to `Project` > `Settings` > `Access Tokens` to create a project-scoped token.

**Role:** Developer or higher

**Scopes:**

| Scope | Purpose |
|---|---|
| `api` | Full API access including pipelines, jobs, and artifact downloads |
| `read_api` | Read-only API access (sufficient for artifact retrieval) |
| `read_repository` | Access to repository content and metadata |

> For least-privilege operation, `read_api` and `read_repository` are sufficient. Grant `api` only if write operations are required elsewhere in your pipeline.

## Usage
```bash
python gitlab_artifact_fetch.py
```

On success, the artifact archive is written to the configured `OUTPUT_FILE` path:
```
[+] Artifact saved as artifact.zip
```

## How It Works

1. Queries the GitLab Pipelines API for the most recent successful pipeline on the target branch.
2. Retrieves the job list for that pipeline and selects the first job with an associated artifact.
3. Downloads the artifact archive and writes it to disk.

## Notes

- Only the first artifact-bearing job from the latest successful pipeline is fetched. Adjust the job selection logic if multiple jobs or specific job names are needed.
- For private instances, update `GITLAB_URL` accordingly.

## License

MIT
