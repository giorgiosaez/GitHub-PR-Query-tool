# GitHub-PR-Query-tool
command line utility to get list of all PRs in given time interval 


# Usage

* Windows/Linux:   ghq.py --repo 'giorgiosaez/GitHub-PR-Query-tool' --jira_key "QT-1" --since "3 days" --github_token "YourToken"

* Mac:              ./ghq --repo 'giorgiosaez/GitHub-PR-Query-tool' --jira_key "QT-1" --since "3 days" --github_token "YourToken"

# Errors

* If you get a "github.GithubException.BadCredentialsException" please run the tool with a new github token using --github_token "YourToken"