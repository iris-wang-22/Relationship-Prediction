# Pairwise Relationships Prediction System

>   This is our group's SML Project 1 in 2020S2. 

## Introduction

Pairwise Relationship is a very common relationship in our daily life. We can use pairwise relationships to store many forms of data, including the relationship between friends, the connections between devices in a network. Finding a way to predict the edges between nodes is an important step, but it is not an easy task to find all missing edges in a graph. In this project, we have implemented a system to predict the pairwise relationships between nodes by using machine learning tools. 

## Usage

### Environment

Before you running the system, make sure you install `Python 3.6`+ in your computer.

The following packages are required in this system:

-   numpy
-   sklearn
-   tensorflow

If you haven't install them yet, please run `pip install` to install them first. 

### Data

The dataset used in this system are from 20,000 records of user-follow from Twitter, with a total of 4,867,136 users. We have also randomly generated negative data and train our model together with the original data from Twitter. The entire dataset is stored in `\data` folder.

### Model

We have built some machine learning models in this project, including neural networks. The `*.py` files are used for handling data, building the models and training data to generate predictions. The detailed description of files are follows:

-   `generate_data.py`: This file is used for generating random negative data and create features that are necessary for the models.
-   `preprocess.py` and `process_data.py`: These two files are used for preprocessing the generated data so that data can be fed into the models.
-   `graph.py`: This file is used for generating a graph, containing all the nodes and edges in the training data.
-   `similarity.py`: This file is used for calculating similarities between data.
-   `Jaccard.py`: This file is used for calculating Jaccard similarity, which is important for feature engineering.
-   `getfeatures_undirectedgraph_ipynb.py`: This file is used for generating features of undirected graph.
-   `getfeatures_directedgraph .py`: This file is used for generating features of directed graph.
-   `knn.py`: This file is used for building a model based on K-Nearest Neighbour.
-   `lr.py`: This file is used for building a model based on Logistic Regression.
-   `nb.py`: This file is used for building a model based on Naive Bayes.
-   `Decision Tree_Random Forest.py`: This file is used for building a model based on Decision Tree and Random Forest.
-   `nn_2.py`: This file is used for building a model based on Deep Neural Networks (2 hidden layers)
-   `nn_3.py`: This file is used for building a model based on Deep Neural Networks (3 hidden layers)
-   `nn_4.py`: This file is used for building a model based on Deep Neural Networks (4 hidden layers)

In particular, we have used DNN with 2 hidden layers as our final approach.

## Result

[Kaggle Competition](https://www.kaggle.com/c/comp90051-2020-sem2-proj1/leaderboard) AUC score **0.83799**

## Copyright

Copyright © 2020, [Xinnan SHEN](https://github.com/sxn2012), [Ziyue Wang](https://github.com/iris-wang-22), [Hanzhong Wang](https://github.com/HzJayden), released under the [GPL-3.0 License](https://github.com/sxn2012/SMLProject/blob/master/LICENSE).