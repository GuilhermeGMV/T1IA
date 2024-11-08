from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.neural_network import MLPClassifier

import pandas as pd

from jogo import jogar_jogo

pd.set_option('future.no_silent_downcasting', True)


def classificar(i, jogar):
    if i == '1':  # KNN
        nome = 'KNN'
        classifier = KNeighborsClassifier(n_neighbors=3)
    elif i == '2':  # MLP
        nome = 'MLP'
        classifier = MLPClassifier(hidden_layer_sizes=15, max_iter=10000)
    elif i == '3':  # Árvore de Decisão
        nome = 'Árvore de Decisão'
        classifier = DecisionTreeClassifier(max_depth=15)
    elif i == '4':  # Random Forest
        nome = 'Random Forest'
        classifier = RandomForestClassifier(n_estimators=70, max_depth=30)
    else:
        return 0

    classifier.fit(X_train, y_train)

    y_pred_val = classifier.predict(X_val)

    accuracy = accuracy_score(y_val, y_pred_val)
    precision = precision_score(y_val, y_pred_val, average='weighted', zero_division=0)
    recall = recall_score(y_val, y_pred_val, average='weighted', zero_division=0)
    f1 = f1_score(y_val, y_pred_val, average='weighted', zero_division=0)

    print(f"\n{nome}: \nAcurácia: {accuracy},\nPrecisão: {precision},\nRecall: {recall},\nF1-Score: {f1}.")
    if jogar:
        jogar_jogo(classifier)
    return 1


if __name__ == '__main__':
    ds = pd.read_csv("tic-tac-toe.data")

    map_input = {'x': 2, 'o': 1, 'b': 0}

    map_output = {'positive': 2, 'negative': 1, 'tie': 3, 'continue': 0}

    X = ds.drop(columns=["classe"]).replace(map_input).astype(int)
    y = ds["classe"].replace(map_output).astype(int)

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    while True:
        i = input("\nDigite:\n0 para sair\n1 para jogar knn\n2 para jogar mlp\n3 para jogar arvore de decisao\n4 para "
                  "jogar random forest\n5 para testar todos: ")
        v = 1
        if i == '5':
            for i in range(4):
                classificar(str(i + 1), False)
        else:
            v = classificar(i, True)
        if v == 0:
            break
