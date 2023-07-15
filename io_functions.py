import pandas as pd
import pickle
from config import Config

# load data by looping over all 12 shards
def read_data_to_feather():
    df_list = []
    for i in range(12):
        filename = f'/workspaces/axa_city_bike/data/raw/2018{i+1:02d}-citibike-tripdata.csv'
        df_list.append(pd.read_csv(filename))
        print(filename)
    df = pd.concat(df_list)
    df = df.reset_index(drop=True)
    df.to_feather('/workspaces/axa_city_bike/data/raw/2018-citibike-tripdata.feather')


def create_sample_data_set():
    df = pd.read_feather('data/raw/2018-citibike-tripdata.feather')
    df = df.sample(frac=0.001, random_state=42)
    df = df.reset_index(drop=True)
    df.to_feather('data/raw/2018-citibike-tripdata_xxs.feather')
    df.to_csv('data/raw/2018-citibike-tripdata_xxs.csv')


def save_run_to_pickle(cfg: Config) -> None:
    """ Save the config file with all experment parameter and results to file using pickle """
    
    with open(f'{cfg.path}/results.pickle', 'wb') as handle:
        pickle.dump(cfg, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    create_sample_data_set()