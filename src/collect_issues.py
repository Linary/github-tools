# -*- coding:utf-8 -*-

import sys

from github import Github

reload(sys)
sys.setdefaultencoding('utf-8')


def replace_last_char(result, signal):
    rs_list = list(result)
    last = len(rs_list) - 1
    rs_list[last] = signal
    return ''.join(rs_list)


# var legendData = ['linary', 'zhangyi', 'javame'];
def write_legend_data(legend_data):
    result = '['
    for user_name in legend_data:
        result += ('\'' + user_name + '\',')
    return replace_last_char(result, ']')


# var seriesData = [{name: 'linary', value: 2}, {name: 'zhangyi', value: 3},{name: 'javame', value: 4}];
def write_series_data(series_data):
    result = '['
    for name, value in series_data.items():
        result += ('{name:\'' + name + '\',value:' + str(value) + '},')
    return replace_last_char(result, ']')


# var selected = {'linary': true, 'zhangyi': true, 'javame': false};
def write_selected(selected):
    result = '{'
    for name, value in selected.items():
        result += ('\'' + name + '\':' + str(value).lower() + ',')
    return replace_last_char(result, '}')


if __name__ == "__main__":
    # using token
    token = 'xxx...'
    g = Github(token)

    repo = g.get_repo("hugegraph/hugegraph")

    # collect issues
    issue_file = open('issues.txt', 'w')
    all_issues = repo.get_issues(state="open")
    for issue in all_issues:
        line = '%s\t%s' % (issue.user.login, issue.title)
        issue_file.write(line + '\n')
    issue_file.close()

    # handle user issues
    authors = ['Linary', 'javeme', 'zhoney']
    legend_data = []
    series_data = {}
    selected = {}

    with open('issues.txt', "r+") as user_issues_file:
        for issue_line in user_issues_file:
            parts = issue_line.split('\t')
            assert len(parts) == 2
            user_name = parts[0]
            issue_title = parts[1]

            if user_name in series_data:
                count = series_data[user_name]
                count = count + 1
                series_data[user_name] = count
            else:
                legend_data.append(user_name)
                series_data[user_name] = 1

            selected[user_name] = True

    selected['Linary'] = False
    selected['javeme'] = False
    selected['zhoney'] = False

    # convert to echarts data strcture
    echarts = '''var legendData = %s;\nvar seriesData = %s;\nvar selected = %s;\n\nvar data = {legendData: legendData, seriesData: seriesData, selected: selected};
              ''' % (write_legend_data(legend_data), write_series_data(series_data), write_selected(selected))
    print echarts
