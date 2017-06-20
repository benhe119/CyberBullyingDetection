from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import numpy as np
import string
import os

references = {'./textpacket1/file0.txt': False,'./textpacket1/file1.txt': False,'./textpacket1/file2.txt': True, './textpacket1/file3.txt': True,'./textpacket1/file4.txt': False,'./textpacket1/file5.txt': False, './textpacket1/file6.txt': False,'./textpacket1/file7.txt': True,
'./textpacket1/file8.txt': False,'./textpacket1/file9.txt': False,'./textpacket1/file10.txt': True,'./textpacket1/file11.txt': False,'./textpacket1/file12.txt': True,'./textpacket1/file13.txt': True,'./textpacket1/file14.txt': True,'./textpacket1/file15.txt': False,
'./textpacket1/file16.txt': False,'./textpacket1/file17.txt': False,'./textpacket1/file18.txt': False,'./textpacket1/file19.txt': False,'./textpacket1/file20.txt': False,'./textpacket1/file21.txt': False,'./textpacket1/file22.txt': False,'./textpacket1/file23.txt': False,
'./textpacket1/file24.txt': False,'./textpacket1/file25.txt': True,'./textpacket1/file26.txt': True,'./textpacket1/file27.txt': False,'./textpacket1/file28.txt': False,'./textpacket1/file29.txt': False,'./textpacket1/file30.txt': False,'./textpacket1/file31.txt': False,
'./textpacket1/file32.txt': False,'./textpacket1/file33.txt': False,'./textpacket1/file34.txt': False,'./textpacket1/file35.txt': False,'./textpacket1/file36.txt': False,'./textpacket1/file37.txt': False,'./textpacket1/file38.txt': True,'./textpacket1/file39.txt': False,
'./textpacket1/file40.txt': False,'./textpacket1/file41.txt': False,'./textpacket1/file42.txt': False,'./textpacket1/file43.txt': False,'./textpacket1/file44.txt': False,'./textpacket1/file45.txt': True,'./textpacket1/file46.txt': False,'./textpacket1/file47.txt': False,
'./textpacket1/file48.txt': False,'./textpacket1/file49.txt': False,'./textpacket1/file50.txt': False,'./textpacket1/file51.txt': False,'./textpacket1/file52.txt': False,'./textpacket1/file53.txt': False,'./textpacket1/file54.txt': False,'./textpacket1/file55.txt': False,
'./textpacket1/file56.txt': True,'./textpacket1/file57.txt': False,'./textpacket1/file58.txt': False,'./textpacket1/file59.txt': False,'./textpacket1/file60.txt': False,'./textpacket1/file61.txt': False,'./textpacket1/file62.txt': False,'./textpacket1/file63.txt': True,
'./textpacket1/file64.txt': True,'./textpacket1/file65.txt': False,'./textpacket1/file66.txt': False,'./textpacket1/file67.txt': False,'./textpacket1/file68.txt': False,'./textpacket1/file69.txt': False,'./textpacket1/file70.txt': False,'./textpacket1/file71.txt': False,
'./textpacket1/file72.txt': True,'./textpacket1/file73.txt': False,'./textpacket1/file74.txt': True,'./textpacket1/file75.txt': True,'./textpacket1/file76.txt': False,'./textpacket1/file77.txt': False,'./textpacket1/file78.txt': True,'./textpacket1/file79.txt': False,
'./textpacket1/file80.txt': True,'./textpacket1/file81.txt': False,'./textpacket1/file82.txt': True,'./textpacket1/file83.txt': True,'./textpacket1/file84.txt': False,'./textpacket1/file85.txt': False,'./textpacket1/file86.txt': False,'./textpacket1/file87.txt': False,
'./textpacket1/file88.txt': True,'./textpacket1/file89.txt': False,'./textpacket1/file90.txt': False,'./textpacket1/file91.txt': True,'./textpacket1/file92.txt': False,'./textpacket1/file93.txt': False,'./textpacket1/file94.txt': False,'./textpacket1/file95.txt': False,
'./textpacket1/file96.txt': False,'./textpacket1/file97.txt': False,'./textpacket1/file98.txt': False,'./textpacket1/file99.txt': False, './textpacket1/file100.txt': False, './textpacket1/file101.txt': False, './textpacket1/file102.txt': True, './textpacket1/file103.txt': False,
'./textpacket1/file104.txt': False, './textpacket1/file105.txt': False, './textpacket1/file106.txt': False, './textpacket1/file107.txt': False, './textpacket1/file108.txt': False, './textpacket1/file109.txt': False, './textpacket1/file110.txt': False, './textpacket1/file120.txt': False, 
'./textpacket1/file111.txt': True, './textpacket1/file112.txt': False, './textpacket1/file113.txt': False, './textpacket1/file114.txt': True, './textpacket1/file115.txt': False, './textpacket1/file116.txt': True, './textpacket1/file118.txt': False,'./textpacket1/atest': False}

def make_dataset():
    dataset_loc = './textpacket1'
    records = [os.path.join(dataset_loc, f) for f in os.listdir(dataset_loc)] # dataset 
    punctuation = set(string.punctuation)
    dataset = []
    for file in records:
        text_list = []
        name = file
        to_write = {'filename': name, 'words':[], 'class': references[name]} # if bullying or not
        with open(file, 'r') as the_file:
            file_contents = the_file.read()  # Read file
            file_contents = ''.join(ch if ch not in punctuation else ' ' for ch in file_contents)  # Strip punctuation
            file_contents = ' '.join(file_contents.split())  # Remove whitespace
            file_contents = file_contents.lower()  # Convert to lowercase
            text_list.append(file_contents)
            vectorizer = CountVectorizer()
            bag_of_words = vectorizer.fit_transform(text_list) # counts word frequency and applies weights to words
            bag_of_words = bag_of_words.toarray() # converts from sparse matrix to 2D array
            words_lst = vectorizer.get_feature_names() # all feature names in list
            dist = np.sum(bag_of_words, axis=0)
            for tag, count in zip(words_lst, dist):
                to_write['words'] += [[tag, count]]
            dataset += [to_write]
    return dataset

def train_and_test(dataset):

    data_frame = pd.DataFrame(dataset) # make dataframe of dataset which is a list of dicts
    print(data_frame)
    train, test = train_test_split(data_frame, test_size = 0.1666)
    print(train.shape, test.shape)
    train_data = train.iloc[:,2]
    print(train_data)
    train_target = train.iloc[:,0]
    print(train_target)
    test_target = test.iloc[:,0]
    test_data = test.iloc[:,2]

    classifier = GaussianNB()
    classifier.fit(train_data, train_target)
    prediction = classifier.predict(test_data)
    print(prediction)

if __name__ == '__main__':
    dataset = make_dataset()
    train_and_test(dataset)
