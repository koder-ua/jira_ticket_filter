from jira import JIRA
from jira_ticket_filter import options, oauth_dict


def filter_issues(jira, query):
    return jira.search_issues(query)


jira = JIRA(options=options, oauth=oauth_dict)
print filter_issues(jira, 'project=MOL')
