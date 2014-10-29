import csv
import datetime
import collections
from collections import defaultdict
from scipy.stats.stats import pearsonr

def valid_date(datestring):
    try:
        datetime.datetime.strptime(datestring, '%Y-%m-%d')
        return True
    except ValueError:
        return False



if __name__ == '__main__':
    with open('Engineering_CS101_Summer2014_Forum.csv', 'rb') as csvfile:
        contents = csv.reader(csvfile)
        count = 0

        master_dict = dict()
        count_dict = dict()
        date_dict = dict()
        week_dict = dict()
        week_posts = []
        week_non_intro_posts = []
        for i in range(8):
            week_posts.append(0)
            week_non_intro_posts.append(0)
        count_dict['question'] = 0
        count_dict['thanks'] = 0
        count_dict['sentence'] = 0
        count_dict['comment'] = 0
        count_dict['commentThread'] = 0
        count_dict['introduction'] = 0
        count_dict['not_introduction'] = 0
        for row in contents:
            if len(row) < 17:
                continue
            if row[0][0] != '5':
                continue
            forum_post_id = row[0]
            comment_type = row[2]
            forum_uid = row[6]
            comment = row[7]
            date = row[9].split(' ')[0]
            votes = row[11]
            voters = row[14]
            comment_thread_id = row[16]
            parent_id = row[17]
            info = dict()
            info['forum_uid'] = forum_uid
            info['comment'] = comment
            info['date'] = date
            info['votes'] = votes
            info['voters'] = voters
            info['comment_thread_id'] = comment_thread_id
            info['parent_id'] = parent_id
            if 'thank' in comment or 'thx' in comment:
                info['thanks'] = True
                count_dict['thanks'] += 1
            else:
                info['thanks'] = False
            if 'hi' in comment.lower() or 'hello' in comment.lower() or 'hey' in comment.lower():
                info['intro'] = True
                count_dict['introduction'] += 1;
            else:
                info['intro'] = False
                count_dict['not_introduction'] += 1;
            if '?' in comment:
                count_dict['question'] += 1
            if '.' in comment or '!' in comment:
                count_dict['sentence'] += 1
            if 'Thread' in comment_type:
                count_dict['commentThread'] += 1
            else:
                count_dict['comment'] += 1
            master_dict[forum_post_id] = info

        #counting dates
        print 'TOTAL: ' + str(len(master_dict))
        for posts in master_dict:
            info = master_dict[posts]
            d = info['date']
            if valid_date(d):
                if d in date_dict:
                    date_dict[d] += 1
                else:
                    date_dict[d] = 1
                week = (datetime.datetime.strptime(d,'%Y-%m-%d') - datetime.datetime.strptime('2014-07-15', '%Y-%m-%d')).days/7
                week_posts[week] += 1;
                if week + 1 in week_dict:
                    week_dict[week + 1] += 1
                else:
                    week_dict[week + 1] = 1
                if not info['intro']:
                    # print week
                    week_non_intro_posts[week] += 1
        print 'non intro posts'
        print week_non_intro_posts
        print 'sum of above'
        print sum(week_non_intro_posts)
        print 'week posts'
        print week_posts
        print 'percentages'
        week_posts_percentages = [x / 2543.0 for x in week_posts]
        print week_posts_percentages
        print 'total non_intro'
        print sum(week_posts)
        print 'non intro percentages'
        print sum(week_non_intro_posts)

        week_non_intro_percentages = [x / 1341.0 for x in week_non_intro_posts]
        print week_non_intro_percentages
        ordered_date_dict = collections.OrderedDict(sorted(date_dict.items()))
        # print ordered_date_dict
        print '# of questions: ' + str(count_dict['question'])
        print '# of thanks: ' + str(count_dict['thanks'])
        print '# of sentences: ' + str(count_dict['sentence'])
        print '# of comments: ' + str(count_dict['comment'])
        print '# of commentThreads: ' + str(count_dict['commentThread'])
        print '# of introductions: ' + str(count_dict['introduction'])
        print '# of not_introductions: ' + str(count_dict['not_introduction'])

    # Gets dictionary of effort in seconds of a class based on week
    master_effort = defaultdict(int)
    weekly_effort = []
    for i in range(8):
        weekly_effort.append(0)

    with open('engagement_Engineering_CS101_Summer2014_weeklyEffort.csv', 'rb') as csvfile:
        contents = csv.reader(csvfile)
        for row in contents:
            week = row[3]
            try:
                effort = int(row[4])
                weekly_effort[int(week) - 1] += effort
                master_effort[week] += effort
            except ValueError:
                continue
    # print 'week, effort'
    print weekly_effort
    print sum(weekly_effort)
    # print dict(master_effort)

    print 'correlation between weekly effort and # posts: ' + str(pearsonr(weekly_effort, week_posts)[0])

    for i in range(8):
        print '[' + str(weekly_effort[i]) + ', ' + str(week_posts[i]) + ']'


    print 'correlation between weekly effort and # sig posts: ' + str(pearsonr(weekly_effort, week_non_intro_posts)[0])

    for i in range(8):
        print '[' + str(weekly_effort[i]) + ', ' + str(week_non_intro_posts[i]) + ']'


    # NLTK, regex
