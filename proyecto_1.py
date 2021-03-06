## MODULE TO EXECUTE PROJECT





"------------------------------------------------------------------------------"
#############
## Imports ##
#############


## Python libraries


## Ancillary modules

from src.utils.params import (
    data_path,
    ingestion_pickle_loc,
    transformation_pickle_loc,
    fe_pickle_loc_imp_features,
    fe_pickle_loc_feature_labs,
    y_test_pickle_loc,
    test_predict_scores_pickle_loc,
    aequitas_df_pickle_loc
)

from src.pipelines.ingestion import (
    ingest
)

from src.pipelines.transformation import (
    transform
)

from src.pipelines.feature_engineering import (
    feature_engineering
)

from src.pipelines.modeling import (
    modeling
)

from src.pipelines.model_evaluation import (
    model_evaluation
)

from src.pipelines.bias_fairness import (
    bias_fairness
)





"------------------------------------------------------------------------------"
###########################
## Main project function ##
###########################


## Master function that executes the project's modules.
def main():
    """
    Master function that executes the project's modules.
        args:
            -
        returns:
            -
    """

    ## Executing ingestion function
    ingest(data_path, ingestion_pickle_loc)

    ## Executing transformation function
    transform(ingestion_pickle_loc, transformation_pickle_loc)

    ## Executing feature engineering function
    feature_engineering(transformation_pickle_loc, fe_pickle_loc_imp_features, fe_pickle_loc_feature_labs)

    ## Executing modeling functions
    modeling(fe_pickle_loc_imp_features, fe_pickle_loc_feature_labs)

    ## Executing model evaluation functions
    model_evaluation(y_test_pickle_loc, test_predict_scores_pickle_loc)

    ## Executing aequitas analysis
    bias_fairness(aequitas_df_pickle_loc)





"------------------------------------------------------------------------------"
##########################################
## Conditional to execute main function ##
##########################################


if __name__ == "__main__":
    main()





"------------------------------------------------------------------------------"
#################
## End of file ##
#################
"------------------------------------------------------------------------------"
