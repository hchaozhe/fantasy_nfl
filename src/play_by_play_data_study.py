import nfl_data_py as nfl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from util import get_key_relations
# %%
file_root = os.path.dirname(os.path.abspath(__file__))
data_root = os.path.join(file_root, "..", "data")
# %%
# get the latest from database
# raw_df = nfl.import_pbp_data([2022])
# or if already cached
raw_df = pd.read_csv(os.path.join("..", "data", "pbp_2022.csv"))
# %% play type association
key1 = "play_type"
key2 = "play_type_nfl"
play_type_relation = get_key_relations(raw_df, key1, key2)
get_key_relations(raw_df, key2, key1)

# %% Plan on the analysis
'''
    TODO: 
    1. need to figure what each columns means
    2. need to think about what kind of model is needed.
    For each team, check its offense formation ("offense formation" + "offense_person"),
    associated with player scored fantasy points and yard progressed
    and the defense formation ("defense_personnel", "defenders_in_box")
'''
# %%
cols = list(raw_df.columns)
offense_col = [col for col in cols if col.startswith("off")]
defense_col = [col for col in cols if col.startswith("def")]

# %% only select raws where all the relavent cols are not empty
relavent_cols = ["possession_team", "offense_formation", "offense_personnel"]
df = raw_df[raw_df[relavent_cols].notna().all(axis=1)]

# %% understand offense statistics by each team
# check only the pass game or rush game formation for each team
df["offense_detail"] = df["offense_formation"] + " " + df["offense_personnel"]

teams = df["home_team"].unique()


# %%
def criteria(play, play_type="All"):
    if play_type == "Rush":
        t1, t2 = ["run",], ["RUSH",]
    elif play_type == "Pass":
        t1, t2 = ["pass",], ["PASS",]
    else:
        t1, t2 = ["pass", "run",], ["PASS", "RUSH",]

    return (play["play_type"] in t1
            and play["play_type_nfl"] in t2
        )

# # %% if use agg function, we will be limited by functionality
# agg_config = dict()
# for col in ["offense_formation", "offense_detail"]:
#     agg_config[col] = "nunique"
# df_useful = df[(~df["offense_formation"].isna()) &
#                (~df["offense_personnel"].isna())]
# sum_df = df_useful.groupby('possession_team').agg(agg_config)


# %% Stats: how many offensive formations each team has for each team 
sum_df = pd.DataFrame(columns=["Team", "All#", "Rush#", "Pass#",
                               "All", "Rush", "Pass"])
key_to_check = "offense_formation"
save_name = "offense_summary_2022"
# key_to_check = "offense_detail"
# save_name = "offense_detail_summary_2022"
for team in teams:
    df_sub = df[(df["possession_team"] == team)].copy()
    entry = {"Team": [team,]}
    for key in "All", "Rush", "Pass":
        idx = df_sub[df_sub.apply(lambda x: criteria(x, key), axis=1)].index
        options = [("N/A" if key is None else key)
                    for key in df[key_to_check][idx].unique()]
        options.sort()
        entry[key + "#"] = [len(options),]
        entry[key] = [",".join(options),]
    sum_df = pd.concat([sum_df, pd.DataFrame(entry)], ignore_index=True)
sum_df = sum_df.sort_values(by=["Team"], ignore_index=True)
sum_df.reset_index(inplace=True)
sum_df.to_csv(os.path.join(data_root, save_name + ".csv"))
