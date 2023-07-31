
def get_key_relations(df, key1, key2):
    key1_key2_relation = dict()
    key1_all = df[key1].unique()
    print("'{}' has the following entry {}".format(key1, key1_all))
    for key in key1_all:
        key1_key2_relation[key] = list(df[key2][df[key1] == key].unique())
    print(key1_key2_relation)
    return key1_key2_relation
