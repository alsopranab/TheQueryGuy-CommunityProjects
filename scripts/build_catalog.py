import json
import os
import requests

projects = []
creators = {}

with open("repos.txt", "r", encoding="utf-8") as f:
    repos = [r.strip() for r in f.readlines() if r.strip()]

for repo in repos:

    repo = repo.replace("https://github.com/", "")
    owner, repository = repo.split("/")

    url = f"https://api.github.com/repos/{owner}/{repository}"

    response = requests.get(url)

    if response.status_code != 200:
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
        "python": "Python",
        "powerbi": "PowerBI",
        "machine-learning": "MachineLearning",
        "data-engineering": "DataEngineering",
        "computer-vision": "ComputerVision",
        "generative-ai": "GenAI"
    }

    for topic in topics:
        if topic in mapping:
            category = mapping[topic]
            break

    projects.append({
        "project_name": data["name"],
        "author": owner,
        "creator_id": creator_id,
        "category": category,
        "description": data.get("description"),
        "stars": data["stargazers_count"],
        "license": (
            data["license"]["spdx_id"]
            if data.get("license")
            else "Unknown"
        ),
        "github_url": data["html_url"]
    })

with open("projects.json", "w", encoding="utf-8") as f:
    json.dump(projects, f, indent=2)

with open("creators.json", "w", encoding="utf-8") as f:
    json.dump(list(creators.values()), f, indent=2)

print(f"Projects: {len(projects)}")
print(f"Creators: {len(creators)}")
