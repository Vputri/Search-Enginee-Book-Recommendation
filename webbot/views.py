from django.shortcuts import render
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from urllib.request import urlopen

my_dir = os.path.dirname(__file__)
model_file_path = os.path.join(my_dir, 'Model.pkl')
book_file_path = os.path.join(my_dir, 'book_data.csv')

def index(request):
    return render(request, 'webbot/index.htm')


def bot_search(request):
    query = request.GET.get('query')
    book = pd.read_csv(book_file_path)   

    try: 
        output = open(model_file_path,'rb')
        new_dict = pickle.load(output)
        output.close()
        cosine_sim = cosine_similarity(new_dict, new_dict)

        def get_recommendations(title, cosine_sim=cosine_sim):
            idx = book.loc[book['book_title'].isin([title])]
            idx = idx.index
            sim_scores = list(enumerate(cosine_sim[idx][0]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:5]
            indices = [i[0] for i in sim_scores]
            judul = book[['book_title', 'image_url']].iloc[indices]
            hasil = judul.to_dict('records') #dictionarry
            return hasil

        result = get_recommendations(query)

        ans = result

    except Exception as e:
        ans = {'book_title': 'NOT FOUND'}

    return render(request, 'webbot/index.htm', {'ans': ans,'query': query})
