# To bet or not to bet? Predicting volleyball outcomes for Polish PlusLiga
Maciej Zdanowicz
#
Following project aims to predict the volleyball outcomes in PlusLiga, highest professional volleyball league in Poland and create a profitable betting strategy. Data comes from the official plusliga website and is updated after each round played. Scrapped information is preprocessed and stored in the database, to then be transformed into final set of features used for modelling. Created featured can be devide into three categories: 

- Features based on team’s detailed performance, calculated for last n=1, 3 and 5 games

![image](https://github.com/Klakii/Volleyball_predictions/assets/100470483/828e835c-c841-4004-91e3-58b508aa6426)

- Features based on players’ characteristics
 
 ![image](https://github.com/Klakii/Volleyball_predictions/assets/100470483/7b39070a-ecc4-4245-a252-f2417b18dcce)

- Features based on team’s overall performance, calculated for last n=1, 3 and 5 games

![image](https://github.com/Klakii/Volleyball_predictions/assets/100470483/1360319f-758b-4d42-b401-02b434ad86b6)

Data for modelling was devided into in-sample, out-of-sample and out-of-time datasets. Distribution of matches' results is displayed below.

![image](https://github.com/Klakii/Volleyball_predictions/assets/100470483/ad2ae638-9824-45ca-8865-d559bba08257)

Performance from three machine learning algorithms was compared by using grid search and bayesian search to find the optimal set of hyperparameters. To generate final predictions, XGBoost model was used. 

Additionally, I have tested model performance after each round played for season 2022/2023, as this season was not previously used for model selection.

![image](https://github.com/Klakii/Volleyball_predictions/assets/100470483/de588ede-469f-460c-80d2-d9918427eacf)

Moreover, I have developed and tested few different betting strategies, and checked their profitability. Two most successful strategies are shown below: first one, where I have decided to bet 100 on each of the games played during the season, and the second strategy, based on using predicted probabilities to determine the bet amount for each bet placed. Bet value varied from 50 to 100 depending on each model’s predictions. Thus, we place more money on matches we are surer about, reducing the overall 
amount invested compared to the first betting strategy. 

![image](https://github.com/Klakii/Volleyball_predictions/assets/100470483/8aa43e68-d6c5-4db4-9f88-d36cccb4f556)

Created model managed to achieve around 5% return on investement.
