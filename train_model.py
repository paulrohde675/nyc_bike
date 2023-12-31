import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC

from config import Config
from config import model_options


def init_model(cfg: Config) -> BaseEstimator:
    """Initilizes the classification model depending on the parameter set in config"""

    if cfg.model_type == model_options.LOGISTIC:
        return LogisticRegression()

    elif cfg.model_type == model_options.GRAD_BOOST:
        return GradientBoostingClassifier()

    elif cfg.model_type == model_options.RANDOM_FOREST:
        return RandomForestClassifier()

    elif cfg.model_type == model_options.SVM:
        return LinearSVC()

    elif cfg.model_type == model_options.NAIV_BAYES:
        return GaussianNB()

    elif cfg.model_type == model_options.NEURAL_NETWORK:
        return MLPClassifier()


def train_model(
    model: BaseEstimator, cfg: Config, X_train: pd.DataFrame, y_train: pd.DataFrame
) -> BaseEstimator:
    """This functions modifies the featurs accroding to the ML method"""

    # Create the GridSearchCV object
    grid_search = GridSearchCV(
        model,
        cfg.hyperparam_grid,
        refit=True,
        cv=cfg.cv_folds,
        n_jobs=3,
        verbose=3,
        scoring=cfg.scoring,
    )

    # Fit the GridSearchCV object to the training data
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_

    # save model
    cfg.model = best_model

    # Print the best hyperparameters found
    print("Best Hyperparameters: ", grid_search.best_params_)

    return best_model
