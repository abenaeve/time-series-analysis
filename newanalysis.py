import requests
import os
from datetime import datetime


# GitHub API base URL
BASE_URL = "https://api.github.com"

# Replace with your GitHub personal access token
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Function to search GitHub repositories related to time-series analysis
def search_github_repositories(query, language="Python", max_age_in_years=2, per_page=10, page=1):
    url = f"https://api.github.com/search/repositories?q={query}+language:{language}&per_page={per_page}&page={page}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repos = response.json()['items']
        filtered_repos = []
        current_year = datetime.now().year
        
        for repo in repos:
            repo_creation_year = datetime.strptime(repo['created_at'], "%Y-%m-%dT%H:%M:%SZ").year
            if current_year - repo_creation_year <= max_age_in_years:
                filtered_repos.append(repo)
        return filtered_repos
    else:
        print(f"GitHub API request failed with status code {response.status_code}")
        return []

# Function to get user details
def get_user_details(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        email = user_data.get('email', 'Email not available')
        blog = user_data.get('blog', 'LinkedIn/Website not available')
        return {
            'username': username,
            'email': email,
            'blog': blog
        }
    else:
        print(f"Failed to retrieve details for user {username}, status code: {response.status_code}")
        return None

# Main function to gather similar repositories and fetch the key contact details
def find_recent_repos_and_contributors():
    all_github_repos = []
    page = 1
    
    while True:
        github_repos = search_github_repositories("time-series analysis", page=page)
        
        if not github_repos:
            break
        
        all_github_repos.extend(github_repos)
        page += 1
    
    for repo in all_github_repos:
        repo_name = repo['name']
        repo_owner = repo['owner']['login']
        print(f"\nRepository Name: {repo_name}\nURL: {repo['html_url']}\nLanguage: {repo['language']}\nCreated At: {repo['created_at']}\n{'-'*50}")
        
        owner_details = get_user_details(repo_owner)
        if owner_details:
            print(f"Owner's Contact Info:\nUsername: {owner_details['username']}\nEmail: {owner_details['email']}\nBlog/LinkedIn: {owner_details['blog']}\n{'-'*50}")

if __name__ == "__main__":
    find_recent_repos_and_contributors()