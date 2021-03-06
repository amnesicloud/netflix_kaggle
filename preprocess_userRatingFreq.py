import os, csv
import numpy as np
from mpi4py import MPI


use_station = 'wukong'
if use_station == 'local':
    dataset_dir = '/home/yuzhuoran/Documents/datasets'
    log_root = '/home/yuzhuoran/Documents/logs/acnn'
if use_station == 'wukong':
    dataset_dir = '/home/yunzhou/fromFiles/datasets'
    log_root = '/home/yunzhou/local/logs/acnn'
if use_station == 'kongming':
    dataset_dir = '/home/yunzhou/fromFiles/datasets'
    log_root = '/home/yunzhou/local/logs/acnn'
if use_station == 'master':
    dataset_dir = '/data/yz_dataset'

data_dir_path = os.path.join(dataset_dir, 'netflix-prize-data')

# data_path1 = os.path.join(data_dir_path, 'combined_data_1.txt')
# data_path2 = os.path.join(data_dir_path, 'combined_data_2.txt')
# data_path3 = os.path.join(data_dir_path, 'combined_data_3.txt')
# data_path4 = os.path.join(data_dir_path, 'combined_data_4.txt')
#
# data_paths = [data_path1, data_path2, data_path3, data_path4]
file_lines = [24058263, 26982302,22605786, 26851926]


# data_path = os.path.join(data_dir_path, 'combined_data_sample.txt')
for file_num in range(1,5):
    data_path = os.path.join(data_dir_path, 'combined_data_%d.txt' % file_num)
    user_rating_mean_output_path = os.path.join(data_dir_path, 'user_rating_freq%d.csv' % file_num)
    user_rating_freq_dict = {}
    user_ratings = [0,0,0,0,0]
    line_count = 0
    with open(data_path, 'r') as r:
        for line in r:
            line_count += 1
            if ':' in line:
                if not user_ratings == [0,0,0,0,0]:
                    user_rating_freq_dict[user_id] = user_ratings
                    user_ratings = [0, 0, 0, 0, 0]
                user_id = int(line.split(':')[0])
            else:
                user_ratings[int(line.split(',')[1])-1] += 1
            if line_count % 50000 == 0:
                print('line %d / %d' %(line_count, file_lines[file_num-1]))
        user_rating_freq_dict[user_id] = user_ratings


    with open(user_rating_mean_output_path, 'w') as w:
        csvw = csv.writer(w)
        user_count = 0
        for user_id in user_rating_freq_dict:
            user_count += 1
            csvw.writerow([user_id, user_rating_freq_dict[user_id]])
            if user_count % 1000 == 0:
                print('finished writing user %d / %d' % (user_count, len(user_rating_freq_dict)))