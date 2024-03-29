import numpy as np
from zlib import crc32

# to make this script's output identical at every run
np.random.seed(42)

def split_train_test(data, test_ratio):
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]

def test_set_check(identifier, test_ratio):
    # Calculate CRC32 hash of the 64-bit integer representation of the identifier
    # and ensure it's a 32-bit unsigned integer using bitwise AND operation
    return crc32(np.int64(identifier)) & 0xffffffff < test_ratio * 2**32

def split_train_test_by_id(data, test_ratio, id_column):
    # Extract identifiers from the specified column in the dataset
    ids = data[id_column]
    # Apply the test_set_check function to each identifier
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio))
    # Return the training set (not in the test set) and the test set
    return data.loc[~in_test_set], data.loc[in_test_set]

if __name__ == "__main__":
    from loader import*
    df = load_data(find_directory("datasets\housing\housing.csv"))

    # train_set, test_set = split_train_test(df, 0.2)
    # print('The number of train set is: ', len(train_set))
    # print('The number of train set is: ', len(test_set))

    df_with_id = df.reset_index() # adds an `index` column#
    # train_set, test_set = split_train_test_by_id(df_with_id, 0.2, "index")

    df_with_id["id"] = df["longitude"] * 1000 + df["latitude"]
    train_set, test_set = split_train_test_by_id(df_with_id, 0.2, "id")

    print(test_set.head())