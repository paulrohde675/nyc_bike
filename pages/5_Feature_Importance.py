import pandas as pd
import streamlit as st

from config import Config
from config import model_options
from dashboard_sidebar import side_bar


def page_feature_importance():
    """This page shoes the feature importances for the differnt models"""
    st.title("Feature importance")

    st.write(
        """
             This section highlights the most influential features in our models. 
             Feature importance rankings help us understand which aspects have 
             the most impact on user classification. Feature importance is computed 
             using permutation."""
    )
    st.markdown("#")

    # render side_bar
    side_bar()

    # get session state and cfg
    state = st.session_state
    cfg: Config = state.cfg

    st.subheader("Permutaiton feature importance")
    st.pyplot(cfg.plt_feat_importance)


if __name__ == "__main__":
    page_feature_importance()
