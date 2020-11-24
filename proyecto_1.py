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
    fe_pickle_loc
)

from src.pipelines.ingestion import (
    ingest
)

from src.pipelines.transformation import (
    transform
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
    # feature_enineering(path)





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
