import pandas as pd
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import RFE

if __name__ == "__main__":
    label = pd.read_csv("./elliptic_bitcoin_dataset/elliptic_txs_classes.csv")
    label["class"].replace({"unknown": '0'}, inplace=True)
    edge = pd.read_csv("./elliptic_bitcoin_dataset/elliptic_txs_edgelist.csv")
    feature = pd.read_csv("./elliptic_bitcoin_dataset/elliptic_txs_features.csv", header=None)
    feature.columns = ["txId"] + ["graphId"] + [f"feature{i}" for i in range(len(feature.columns) - 2)]
    feature["illicit_input"] = [0 for i in range(len(feature))]
    feature["illicit_output"] = [0 for i in range(len(feature))]
    feature = pd.merge(feature, label, on="txId")
    for _, row in edge.iterrows():
        i = feature.index[feature["txId"] == row['txId1']].tolist()[0]
        o = feature.index[feature["txId"] == row['txId2']].tolist()[0]
        if feature.loc[i,'class'] == '1':
            feature.at[o,'illicit_input'] += 1
        if feature.loc[o,'class'] == '1':
            feature.at[i,'illicit_output'] += 1
    data = feature[(feature['class'] == '1') | (feature['class'] == '2')]
    X = data[[f"feature{i}" for i in range(len(feature.columns) - 5)] + ["illicit_input", "illicit_output"]]
    Y = data['class']
    Y.replace({"2": '0'}, inplace=True)
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=0,shuffle=True)
    # clf = LogisticRegressionCV(cv=10, max_iter=2000, random_state=0).fit(X_train, Y_train)
    # _predict = clf.predict(X_test)
    # precision,recall,f1,_ = precision_recall_fscore_support(Y_test,_predict)
    # print(f"logistic regression F1 = {f1[1]}")

    # clf = RandomForestClassifier(n_estimators=50,random_state=0).fit(X_train,Y_train)
    # _predict = clf.predict(X_test)
    # precision,recall,f1,_ = precision_recall_fscore_support(Y_test,_predict)
    # print(f"random forest F1 = {f1[1]}")

    # clf = make_pipeline(StandardScaler(), SVC()).fit(X_train,Y_train)
    # _predict = clf.predict(X_test)
    # precision,recall,f1,_ = precision_recall_fscore_support(Y_test,_predict)
    # print(f"SVM F1 = {f1[1]}")

    selector = RFE(estimator=SVC(), n_features_to_select=90, step=1).fit(X_train,Y_train)
    _predict = selector.predict(X_test)
    precision,recall,f1,_ = precision_recall_fscore_support(Y_test,_predict)
    print(f"SVM F1 = {f1[1]}")

    # pca = PCA(n_components=2).fit(X_train) 
    # pcaf = pca.transform(X_train)

    # trans = pd.DataFrame()
    # trans['x'] = pcaf[:,0]
    # trans['y'] = pcaf[:,1]
    # trans["illicit"] = Y_test

    # plt.figure(figsize=(16,10))
    # sns.scatterplot(
    # x="x", y="y",
    # hue="illicit",
    # palette=sns.color_palette("hls",2),
    # data=trans,
    # legend="full",
    # alpha=0.3
    # )

    # plt.show()
    # plt.savefig('illicit2D.png')