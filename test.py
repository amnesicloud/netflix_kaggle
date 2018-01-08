import os

use_station = 'local'
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

