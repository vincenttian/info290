import csv
import datetime
import collections
from collections import defaultdict
from scipy.stats.stats import pearsonr
from sklearn import svm
import numpy

def valid_date(datestring):
    try:
        datetime.datetime.strptime(datestring, '%Y-%m-%d')
        return True
    except ValueError:
        return False


if __name__ == '__main__':

    with open('Engineering_CS101_Summer2014_Forum_Sensitive.csv', 'rb') as csvfile:
        contents = csv.reader(csvfile)
        master_dict = dict()
        for row in contents:
            if len(row) < 17:
                continue
            if row[0][0] != '5':
                continue
            if len(row[1]) != 40:
                continue
            anon_screen_name = row[1]
            comment_type = row[2]
            forum_uid = row[6]
            comment = row[7]
            date = row[9].split(' ')[0]
            votes = row[11]
            voters = row[14]
            comment_thread_id = row[16]
            parent_id = row[17]
            if anon_screen_name not in master_dict:
                data = master_dict[anon_screen_name] = []
                # this is where you change it if you want more attributes
                # [0] = num of total posts
                # [1] = average len of posts but will temporarily hold total words
                # [2] = num of comments
                # [3] = num of comment threads
                # [4] = num of questions
                for i in range(5):
                    data.append(0)
            data[0] += 1
            data[1] += len(comment.split())
            if 'Thread' in comment_type:
                data[3] += 1
            else:
                data[2] += 1
            if '?' in comment:
                data[4] += 1
        #getting the average
        for user in master_dict:
            master_dict[user][1] /= master_dict[user][0]

    with open('gradesAndCerts.csv', 'rb') as csvfile:
        grades_dict = dict()
        certified_dict = dict()
        contents = csv.reader(csvfile)
        for row in contents:
            if len(row) != 3:
                continue
            anon_screen_name = row[0]
            grade = row[1]
            certified = row[2]
            grades_dict[anon_screen_name] = grade
            certified_dict[anon_screen_name] = certified
            if anon_screen_name not in master_dict:
                data = master_dict[anon_screen_name] = []
                for i in range(5):
                    data.append(0)
    ordered_certified = collections.OrderedDict(sorted(certified_dict.items()))
    ordered_master_dict = collections.OrderedDict(sorted(master_dict.items()))
    # print ordered_certified
    print len(ordered_certified)
    print len(ordered_master_dict)

    training_features = []
    training_scores = []
    training_certified = []
    testing_features = []
    testing_scores = []
    testing_certified = []
    count = 0
    for i in ordered_master_dict:
        if count > 1000:
            break
        if i not in ordered_certified:
            continue
        if count <= 500:
            f_array = ordered_master_dict[i]
            training_features.append(f_array)
            training_scores.append(grades_dict[i])
            training_certified.append(certified_dict[i])
        if count > 500:
            f_array = ordered_master_dict[i]
            testing_features.append(f_array)
            testing_scores.append(grades_dict[i])
            testing_certified.append(certified_dict[i])
        count += 1
    print len(training_features)
    print len(testing_features)
    clf = svm.SVC()
    clf.fit(training_features, training_certified)



    # NLTK, regex
