import os
import pandas as pd
from sklearn.model_selection import train_test_split

current_dir = os.path.dirname(__file__)
data_dir = os.path.join(os.path.abspath(os.path.join(current_dir, os.pardir)), 'data')

header = ['article_title', 'paragraph_number', 'sentence']
normal_df = pd.read_csv(os.path.join(data_dir, 'normal.aligned'), delimiter='\t\t', names=header)
simple_df = pd.read_csv(os.path.join(data_dir, 'simple.aligned'), delimiter='\t\t', names=header)

RANDOM_STATE = 9

X_train, X_test, y_train, y_test = train_test_split(normal_df.sentence, simple_df.sentence,
                                                    test_size=0.20, random_state=RANDOM_STATE)

# Write CSVs with splited data
X_train.to_csv(os.path.join(data_dir, 'normal.train'), index=False, header=False)
X_test.to_csv(os.path.join(data_dir, 'normal.test'), index=False, header=False)
y_train.to_csv(os.path.join(data_dir, 'simple.train'), index=False, header=False)
y_test.to_csv(os.path.join(data_dir, 'simple.test'), index=False, header=False)
