import sys
import os.path
import functools

import yaml
from jira import JIRA
from colorama import Fore
from texttable import Texttable


def getattr_r(obj, attr_path):
    if '.' in attr_path:
        curr, rest = attr_path.split('.', 1)
    else:
        curr, rest = attr_path, None

    try:
        obj = getattr(obj, curr)
    except AttributeError:
        return "< err >"

    if rest is None:
        return obj

    return getattr_r(obj, rest)


def main(argv):
    def_path = os.path.expanduser("~/.jira/config.yaml")
    key_file = os.path.expanduser("~/.jira/moslinuxbot.pem")
    config = yaml.load(open(def_path))

    oauth = config['oauth_dict']
    oauth['key_cert'] = open(key_file).read()

    jira = JIRA(options=config['options'], oauth=oauth)
    table = Texttable(max_width=160)

    issue_filter = 'project=MOL'
    if len(argv) > 1:
        issue_filter += ' AND ' + argv[1]

    print issue_filter

    issues_iter = jira.search_issues(issue_filter)

    sorted_issues = sorted(issues_iter,
                           key=lambda x: x.fields.assignee.name)

    table.set_deco(Texttable.HEADER | Texttable.BORDER)

    rows = [["ID", "Status", "Owner", "Descr"]]
    for issue in sorted_issues:
        ga = functools.partial(getattr_r, issue)
        attrs = map(ga, ("key",
                         "fields.status.name",
                         "fields.assignee.name",
                         "fields.summary"))
        attrs = map(str, attrs)
        rows.append(attrs)

    table.add_rows(rows)
    res = table.draw()

    colors = {
        'Resolved': Fore.GREEN,
        'Certified': Fore.GREEN,
        'Closed': Fore.GREEN,
        "In Progress": Fore.YELLOW,
    }

    for status, color in colors.items():
        res = res.replace(" {} ".format(status),
                          " {}{}{} ".format(color, status, Fore.RESET))

    print res


if __name__ == "__main__":
    exit(main(sys.argv))
