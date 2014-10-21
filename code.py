import csv

if __name__ == '__main__':
    with open('Engineering_CS101_Summer2014_Forum.csv', 'rb') as csvfile:
        contents = csv.reader(csvfile)
        count = 0
        
        master_dict = dict()
        
        for row in contents:
            if len(row) < 17:
                continue
            if row[0][0] != '5':
                continue
            forum_post_id = row[0]
            forum_uid = row[6]
            comment = row[7]
            votes = row[11]
            voters = row[14]
            comment_thread_id = row[16]
            parent_id = row[17]
            info = dict()
            info['forum_uid'] = forum_uid
            info['comment'] = comment
            info['votes'] = votes
            info['voters'] = voters
            info['comment_thread_id'] = comment_thread_id
            info['parent_id'] = parent_id
            if 'thank' in comment or 'thx' in comment:
                info['thanks'] = True
            else:
                info['thanks'] = False
            master_dict[forum_post_id] = info