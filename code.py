import csv
import datetime


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
        count_dict['question'] = 0
        count_dict['thanks'] = 0
        count_dict['sentence'] = 0
        count_dict['comment'] = 0
        count_dict['commentThread'] = 0
        count_dict['introduction'] = 0
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
            if 'hi' in comment.lower() or 'hello' in comment.lower() or 'hey' in comment.lower() or 'everyone' in comment.lower():
                count_dict['introduction'] += 1;
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
        print date_dict
        print '# of questions: ' + str(count_dict['question'])
        print '# of thanks: ' + str(count_dict['thanks'])
        print '# of sentences: ' + str(count_dict['sentence'])
        print '# of comments: ' + str(count_dict['comment'])
        print '# of commentThreads: ' + str(count_dict['commentThread'])
        print '# of introductions: ' + str(count_dict['introduction'])





