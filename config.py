from enum import Enum

import pandas as pd
from matplotlib.figure import Figure
from sklearn.base import BaseEstimator
from sklearn.preprocessing import StandardScaler
from sklearn.utils import Bunch

imb_learn_options = Enum("smote", "undersampling")
model_options = Enum("logistic", "xgboost")


class imb_learn_options(Enum):
    SMOTE = "smote"
    UNDERSAMPLING = "undersampling"


class model_options(Enum):
    LOGISTIC = "logistic"
    GRAD_BOOST = "grad_boost"
    RANDOM_FOREST = "random_forest"
    SVM = "svm"
    NAIV_BAYES = "naive_bayes"
    NEURAL_NETWORK = "neural_network"


class Config:
    def __init__(
        self,
        run_name: str,
        model_type: model_options,
        scoring="f1",
        test_split=0.3,
        cv_folds=5,
        imb_mode: imb_learn_options = imb_learn_options.UNDERSAMPLING,
    ) -> None:
        self.run_name = run_name
        self.random_state = 42
        self.test_split = test_split
        self.model_type: model_options = model_type
        self.scoring = scoring
        self.imb_mode: imb_learn_options = imb_mode
        self.cv_folds = cv_folds

        # init path
        self.path = f"data/final/{self.run_name}/"

        # Define the hyperparameter grid
        if model_type == model_options.GRAD_BOOST:
            self.hyperparam_grid = {
                "n_estimators": [50, 100, 150],
                "learning_rate": [0.1, 0.01],
                "max_depth": [3, 5, 9],
                "min_samples_split": [2, 8],
                "min_samples_leaf": [1, 5],
                "max_features": ["sqrt"],
                "subsample": [0.6, 1.0],
            }

        elif model_type == model_options.LOGISTIC:
            self.hyperparam_grid = {
                "penalty": ["l1", "l2", "elasticnet"],
                "C": [0.1, 0.5, 1, 5, 10],
                "solver": ["saga"],
            }
        elif model_type == model_options.RANDOM_FOREST:
            self.hyperparam_grid = {
                "n_estimators": [100],  # 50,
                "max_depth": [None],  # 5, 9,
                "min_samples_split": [2],  # , 8
                "min_samples_leaf": [1],  # , 5
                "max_features": ["sqrt"],
                "bootstrap": [False],  # True,
            }
        elif model_type == model_options.SVM:
            self.hyperparam_grid = {
                "C": [0.1, 1, 10, 100],
                "loss": ["hinge"],
                "penalty": ["l2"],
                "tol": [1e-4, 1e-3],
            }
        elif model_type == model_options.NAIV_BAYES:
            self.hyperparam_grid = {"var_smoothing": [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]}
        elif model_type == model_options.NEURAL_NETWORK:
            self.hyperparam_grid = {
                "hidden_layer_sizes": [(2,), (10,), (50,), (100,)],
                "activation": ["relu"],  #'tanh',
                "solver": ["adam"],  # 'sgd',
                "alpha": [0.0001, 0.01, 1.0],
                "learning_rate": ["constant", "adaptive"],
            }

    # test data
    X_test: pd.DataFrame = pd.DataFrame()
    y_test: pd.Series = pd.Series()

    # model
    model: BaseEstimator | None = None
    scaler: StandardScaler | None = None

    # evaluation
    feat_importance: Bunch | None = None
    accuracy: float = 0
    precision: float = 0
    recall: float = 0
    f1: float = 0
    auc_roc: float = 0
    model_report: str = ""
    model_report_dict: dict = dict()
    plt_confusion_matrix: Figure
    plt_roc: Figure
    plt_feat_importance: Figure
