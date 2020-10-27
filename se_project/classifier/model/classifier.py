import pandas as pd
import nltk
import concurrent.futures
import re
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
## This import is useful later 
from sklearn.metrics import classification_report, accuracy_score
# from xgboost import XGBClassifier
import joblib
from sklearn.linear_model import LogisticRegression

dataset = pd.read_csv("C:/Users/Urvashi/Desktop/Online-Book-Exchange-Portal/Dataset/books.csv", encoding="ISO-8859-1")
dataset.groupby('category').count()['name']

nltk.download('stopwords')

corpus = []
with concurrent.futures.ProcessPoolExecutor() as executor:
    for i in tqdm(range(0, dataset.shape[0])):
        book = re.sub('[^a-zA-Z]', ' ', dataset['name'][i]) # Filter non alphabetical chars
        book = book.lower() # Convert to lowercase
        book = book.split() # Split on spaces
        ps = PorterStemmer() # Stem
        book = [ps.stem(word) for word in book if not word in set(stopwords.words('english'))]
        book = ' '.join(book) 
        corpus.append(book)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

label_encoder = LabelEncoder()
y = dataset['category'].values # Get target categories
y[-1] = 'Romance'
print(y, y.shape)
y = label_encoder.fit_transform(y) # Encode category labels to integers

# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.01, random_state = 0)
print(X_train.shape, X_test.shape)

name_map = pd.DataFrame.from_dict(dict(zip(label_encoder.classes_, 
                                           label_encoder.transform(label_encoder.classes_))), 
                                  orient='index')
print(name_map)

lr = LogisticRegression(solver='sag',max_iter=200,random_state=450,
                                             n_jobs=4, verbose=True)
lr.fit(X_train, y_train)
        
# Evaluate on train and test set
print("Train set score:", lr.score(X_train, y_train))
print("Train set score:", lr.score(X_test, y_test))

# Generate classification report
y_pred = lr.predict(X_test)
print(classification_report(y_test.astype(int), y_pred))

joblib.dump(name_map, 'name_map.joblib', compress = True)
joblib.dump(lr, 'logistic_regressor.joblib', compress = True)

print('Ran successfully!')