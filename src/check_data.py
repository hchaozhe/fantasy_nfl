'''
For usage of nfl_data_py see https://pypi.org/project/nfl-data-py/
'''

import nfl_data_py as nfl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os
# %%
file_root = os.path.dirname(os.path.abspath(__file__))
data_root = os.path.join(file_root, "..", "data")
# %%
pbp_data = nfl.import_pbp_data([2022])
pbp_data.to_csv(os.path.join(data_root, "pbp_2022.csv"))

# %% Pick a game play to check the details of the pbp data
idx = pbp_data[(pbp_data["home_team"] == "BUF") & (pbp_data["away_team"] == "MIN")].index
BUFvsMIN = pbp_data.loc[idx]
BUFvsMIN.to_csv(os.path.join(data_root, "pbp_BUF_vs_MIN_2022.csv"))
play = np.random.randint(0, len(BUFvsMIN))
BUFvsMIN.iloc[play:play+1].T.to_csv(
    os.path.join(data_root, "pbp_BUF_vs_MIN_2022_play{}.csv".format(str(play))))

# %% Roster
# roster = nfl.import_rosters([2023])

# %% Play season data
player_season_data = nfl.import_seasonal_data([2022])
player_season_data.to_csv(os.path.join(data_root, "player_season_data_2022.csv"))
