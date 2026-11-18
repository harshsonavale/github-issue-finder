import requests

language = input("enter the programming language that you want to search for:")
url = "https://api.github.com/search/issues"

params = {
    "q": f"is:issue is:open language:{language}",
    "per_page": 100,
    "sort": "updated",
    "order": "desc"
}


def classify_issue(issue):
    labels = [
        label["name"].lower()
        for label in issue.get("labels", [])
    ]

    if any(label in labels for label in ["good first issue", "beginner-friendly", "easy"]):
        return "beginner-friendly"

    if any(label in labels for label in ["advance", "advanced", "hard", "complex"]):
        return "advanced"

    if any(label in labels for label in ["intermediate", "medium"]):
        return "intermediate"

    return "needs review"


try:
    response = requests.get(url, params=params, timeout=15)

    if response.status_code == 200:
        issues = response.json()["items"]
        categories = {
            "beginner-friendly": [],
            "intermediate": [],
            "advanced": [],
            "needs to verify": []
        }

        for issue in issues:
            level = classify_issue(issue)
            if level == "needs review":
                level = "needs to verify"
            categories[level].append(issue)

        for level, items in categories.items():
            print(f"========= {level.upper()} ========= ")

            if not items:
                print("No issues found.")
                continue

            for number, issue in enumerate(items[:5], start=1):
                print(f'{number}. {issue["title"]}')
                print(f'url: {issue["html_url"]}')
    else:
        print("github API error:", response.status_code)
        print("response text:", response.text[:300])

except requests.RequestException as error:
    print("request error:", error)
    