from django.shortcuts import render
import joblib
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import os.path

# Create your views here.
def predict(request):
	if request.POST:
		book = request.POST.get('book')
		book = book.lower()
		book = book.split()
		ps = PorterStemmer()
		book = [ps.stem(word) for word in book if not word in set(stopwords.words('english'))]
		book = ' '.join(book)
		vectorizer = joblib.load('C:/Users/Urvashi/Desktop/Online-Book-Exchange-Portal/se_project/classifier/model/vectorizer.joblib')
		x = vectorizer.transform([book])

		lr = joblib.load('C:/Users/Urvashi/Desktop/Online-Book-Exchange-Portal/se_project/classifier/model/logistic_regressor.joblib')
		prob = lr.predict_proba(x).reshape((6,))
		idx = np.argmax(prob)

		genres = ['Calendars', 'Comics & Graphic Novels', 'Mystery, Thriller & Suspense', 
				'Romance', 'Science Fiction & Fantasy', 'Test Preparation']

		context = {'genre': genres[idx]}
		print(genres[idx])
		return render(request, 'classifier/predict.html', context)
	return render(request, 'classifier/predict.html')
