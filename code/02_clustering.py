from matplotlib import pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

col_features = [
  'acousticness', 'danceability', 'energy', 
  'instrumentalness', 'liveness', 'loudness',
  'speechiness', 'valence']

df = pd.read_csv("./data/track_features.csv")
X = StandardScaler().fit_transform(df[col_features])

def calculate_wcss(data, cap):
  wcss = []
  for n in range(2, cap):
    kmeans = KMeans(n_clusters=n)
    kmeans.fit(X=data)
    wcss.append(kmeans.inertia_)
  return wcss
  
plt.plot(range(2, 21), calculate_wcss(X, 21), 'bx-')
plt.xlabel('Número de grupos')
plt.ylabel('Soma de quadrados interna')
plt.title('Método do cotovelo')
aux = plt.xticks(range(2, 21))
plt.show()

n_clust = 7
random_state = 1
y_pred = KMeans(n_clusters=n_clust, random_state=random_state).fit_predict(X)
df['cluster'] = y_pred

df.to_csv("./data/cluster_data.csv", sep = ',')
