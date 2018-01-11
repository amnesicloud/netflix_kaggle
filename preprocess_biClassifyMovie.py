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

file_lines = [24058263, 26982302,22605786, 26851926]


# data_path = os.path.join(data_dir_path, 'combined_data_sample.txt')
for file_num in range(1,5):
    data_path = os.path.join(data_dir_path, 'combined_data_%d.txt' % file_num)
    user_rating_mean_output_path = os.path.join(data_dir_path, 'user_rating_means%d.csv' % file_num)
    user_rating_mean_dict = {}
    user_ratings = []
    line_count = 0
    with open(data_path, 'r') as r:
        for line in r:
            line_count += 1
            if ':' in line:
                if not len(user_ratings) == 0:
                    rating_mean = np.mean(user_ratings)
                    user_rating_mean_dict[user_id] = rating_mean
                user_id = int(line.split(':')[0])
            else:
                user_ratings.append(int(line.split(',')[1]))
            if line_count % 20000 == 0:
                print('line %d / %d' %(line_count, file_lines[file_num-1]))