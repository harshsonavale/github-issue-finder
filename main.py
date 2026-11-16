import requests
language = input("enter the programming language that you want to search for:")
url = "https://api.github.com/search/issues"

params = { "q": f'is:issue is:open label:"good first issue" language:{language}', 
          "per_page": 5 }
response = requests.get(url, params=params,timeout=10)

if response.status_code == 200:
    data = response.json()
    issues = data.get("items", [])
    if issues:
        print(f"Top 5 open 'good first issue' for {language}:")
        for issue in issues:
            print(f"- {issue['title']} (URL: {issue['html_url']})")
    else:
        print(f"No open 'good first issue' found for {language}.")