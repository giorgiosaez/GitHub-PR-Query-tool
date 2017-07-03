# -*- coding: utf-8 -*-
"""
set PYTHONIOENCODING=UTF-8
Usage: 
Windows/Linux:   ghq.py --repo 'giorgiosaez/GitHub-PR-Query-tool' --jira_key "QT-1" --since "3 days" --github_token "YourToken"
Mac:              ./ghq --repo 'giorgiosaez/GitHub-PR-Query-tool' --jira_key "QT-1" --since "3 days" --github_token "YourToken"
"""

import sys, getopt
import datetime, dateparser
from github import Github
from tabulate import tabulate
from collections import Counter
import re
from pandas import DataFrame

def getFilesSummary(fileList):
    summary = []
    for prFile in fileList:
        summary.append( str(prFile.filename.split(".")[-1]))
    return  re.sub("}|{","",str(dict(Counter(summary))))
    
def main(argv):
    repo = ''
    jira_key = ''  
    since = ''
    gitToken = "9355c989087d07f311345f3dadcd1f829b9f0aab"
    try:
        opts, args = getopt.getopt(argv,"hs:k:r:",["since=","jira_key=","repo="])
    except getopt.GetoptError:
        print ('[+] Usage: %s -r <repo> -k <jira_key> -s <since>' % sys.argv[0])
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'ghp.py -r <repo> -k <jira_key> -s <since>'
            sys.exit()
        elif opt in ("-r" ,"--repo"):
            repo = arg.strip("'") 
        elif opt in ("-k", "--jira_key"):
            jira_key = arg   
        elif opt in ("-s", "--since"):
            since = arg
            if len(since.split(" ")) < 2 or (len(since.split(" ")) >= 2 and 'ago' in since):
                since = "1 " + since 
            if 'ago' not in since:
                since += ' ago'       
        elif opt in ("-t","--github_token") :
            gitToken = arg
    dateFrom = dateparser.parse(since)
    dateTo = datetime.date.today()
    
    git = Github(gitToken)

    gitRepo = git.get_repo('h2oai/h2o-3')
    pulls = gitRepo.get_pulls(state="all")
    usersTable = []
    prTable = []
    for PR in pulls:
       if PR.created_at > dateFrom:
           merged = PR.merged_at.strftime("%Y-%m-%d") if isinstance(PR.merged_at, datetime.date) else "---"   
           timeToMerge = (PR.merged_at-PR.created_at) if PR.merged_at else "---" 
           offensive = "!!!" if jira_key not in PR.title else ""
           
           prTable.append([PR.title,PR.state,PR.created_at.strftime("%Y-%m-%d"), merged, timeToMerge, offensive, getFilesSummary(PR.get_files())])
           usersTable.append([(PR.user.login), 1 if (PR.state)=="closed" else 0 , 1])
    
    #aggreation users table to sum # of PR merged and total merged PR
    df = DataFrame(data=usersTable,columns=["Authors", "Merged PRs","All PRs"])
    df1 = df.groupby(df['Authors']).sum()

    print ("*** GitHub repo %s (from %s to %s) ***" % (repo, (dateFrom).strftime("%Y-%m-%d"), str(dateTo)))
    if prTable:
        print tabulate(prTable, headers = ["Title", "State", 'Created at', 'Merged at', 'Time to merge', 'Offensive', 'File Stats'])
        print
        print "*** Authors ***"
        print tabulate(df1, headers = ["Authors", "Merged PRs","All PRs"])
    else:
        print "Sorry there aren't any Pull Request since " + since
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("[+] Usage: %s -r <repo> -k <jira_key> -s <since>" % sys.argv[0])
        sys.exit(0)
    else:
        main(sys.argv[1:])
