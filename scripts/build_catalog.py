import json
import requests

projects = []
creators = {}

# Read repositories

with open("repos.txt", "r", encoding="utf-8") as f:
repos = [r.strip() for r in f.readlines() if r.strip()]

print(f"Found {len(repos)} repositories")

for repo in repos:

```
print(f"\nProcessing: {repo}")

try:

    # Clean URL
    repo = repo.strip()
    repo = repo.replace("https://github.com/", "")
    repo = repo.replace(".git", "")

    parts = repo.split("/")

    if len(parts) != 2:
        print(f"Skipping invalid repo: {repo}")
        continue

    owner = parts[0]
    repository = parts[1]

    url = f"https://api.github.com/repos/{owner}/{repository}"

    response = requests.get(
        url,
        headers={
            "Accept": "application/vnd.github+json"
        },
        timeout=30
    )

    print(f"{url} -> {response.status_code}")

    if response.status_code != 200:
        print("Repository not accessible")
        continue

    data = response.json()

    creator_id = owner.lower()

    creators[creator_id] = {
        "creator_id": creator_id,
        "name": owner,
        "github": f"https://github.com/{owner}"
    }

    topics = data.get("topics", [])

    category = "CaseStudies"

    mapping = {
        "sql": "SQL",
        "mysql": "SQL",
        "postgresql": "SQL",
        "excel": "Excel",
        "powerbi": "PowerBI",
        "power-bi": "PowerBI",
        "python": "Python",
        "machine-learning": "MachineLearning",
        "deep-learning": "DeepLearning",
        "computer-vision": "ComputerVision",
        "data-engineering": "DataEngineering",
        "generative-ai": "GenAI",
        "genai": "GenAI"
    }

    for topic in topics:
        topic = topic.lower()

        if topic in mapping:
            category = mapping[topic]
            break

    projects.append({
        "project_name": data.get("name"),
        "author": owner,
        "creator_id": creator_id,
        "category": category,
        "description": data.get("description"),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "language": data.get("language"),
        "license": (
            data["license"]["spdx_id"]
            if data.get("license")
            else "Unknown"
        ),
        "github_url": data.get("html_url")
    })

    print(f"Added: {data.get('name')}")

except Exception as e:
    print(f"Error processing {repo}")
    print(str(e))
```

# Save Projects

with open("projects.json", "w", encoding="utf-8") as f:
json.dump(projects, f, indent=2, ensure_ascii=False)

# Save Creators

with open("creators.json", "w", encoding="utf-8") as f:
json.dump(
list(creators.values()),
f,
indent=2,
ensure_ascii=False
)

print("\n=================================")
print(f"Projects: {len(projects)}")
print(f"Creators: {len(creators)}")
print("Catalog Generated Successfully")
print("=================================")
