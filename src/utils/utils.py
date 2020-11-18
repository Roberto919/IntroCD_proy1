## MODULE WITH FUNCTIONS TO SAVE AND LOAD PICKLE, AS WELL AS OTHER USEFULL FUNCTIONS.





"------------------------------------------------------------------------------"
#############
## Imports ##
#############

## Python libraries

import json

import pandas as pd

import sys


## Ancillary modules
sys.path.append("..")
from src.utils.data_dict import (
    data_dict
)





"------------------------------------------------------------------------------"
#################################
## Generic ancillary functions ##
#################################


## Pretty print a dictionary and preserving special characters
def json_dump_dict(dictionary):
    """
    Pretty print a dictionary and preserving special characters
        args:
            dictionary (dictionary): dict that will be pretty printed
        returns:
            -
    """

    print(json.dumps(dictionary, indent=4, ensure_ascii=False).encode("utf8").decode())

    return





"------------------------------------------------------------------------------"
##############################
## Data profiling functions ##
##############################


## Counting number of variables in data (¿Cuántas variables tenemos?)
def count_vars(data):
    """
    Counting number of variables in data
        args:
            data (dataframe): data that is being analyzed
        returns:
             res (int): number of variables in the data
    """

    res = data.shape[1]
    print("Número de variables en los datos --> {}".format(res))

    return



## Counting number of observations in data (¿Cuántas observaciones tenemos?)
def count_obs(data):
    """
    Counting number of observations in data
        args:
            data (dataframe): data that is being analyzed
        returns:
            res (int): number of observations in the data

    """

    res = data.shape[0]

    print("Número de observaciones en los datos --> {}".format(res))

    return



## Counting number of unique observations for all variables
def count_unique_obs(data):
    """
    Counting number of unique observations for all variables
        args:
        data (dataframe): data that is being analyzed
        returns:
        (series): number of unique observations for all variables
    """
    return data.nunique()



## Creting table with classification of variables based in definition dictionary.
def vars_classif_by_type():
    """
    Creting table with classification of variables based in definition dictionary.
        args:
            -
        returns:
            -
    """

    ## Creating and populating dictionary with classified variables according to data type.
    data_classif = {}

    for var in data_dict:

        dt = data_dict[var]["data_type"]

        if dt not in data_classif:
            data_classif[dt] = []
            data_classif[dt].append(var)

        else:
            data_classif[dt].append(var)


    ## Converting dictionary to dataframe and displaying results
    data_classif = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data_classif.items()])).fillna("-")

    print(display(data_classif))


    return



## Data profiling for numeric variables
def data_profiling_numeric(data, num_vars):
    """
    Data profiling for numeric variables
        Args:
            data(dataframe): dataframe that will be analyzed.
        num_vars (list): list of variables' names in the dataframe that will be analyzed.
        Retruns:
            Dataframe with the data profiling (type, number of observations, mean, sd, quartiles, max, min, unique observations, top 5 repeated observations, number of null variables)
            of the choosen numeric variables.
    """

    ## Copy of initial dataframe to select only numerical columns
    dfx = data.loc[:, num_vars]


    ## Pipeline to create dataframe with general data description
    print("*********************************")
    print("** General description of data **")
    print("*********************************")

    #### List where the resulting dataframes will be stored for further concatenation
    res_dfs = []

    #### Type of numeric variables
    dfx_dtype = dfx.dtypes.to_frame().T
    dfx_dtype.index = ["dtype"]
    res_dfs.append(dfx_dtype)

    #### Counting unique variables
    dfx_uniqvars = dfx.nunique().to_frame().T
    dfx_uniqvars.index = ["count_unique"]
    res_dfs.append(dfx_uniqvars)

    #### Counting missing values
    dfx_missing = dfx.isnull().sum().to_frame().T
    dfx_missing.index = ["missing_v"]
    res_dfs.append(dfx_missing)

    #### General description of the data and addition of min values
    dfx_desc = dfx.describe()
    dfx_desc.loc["min", :] = dfx.min(axis=0)
    res_dfs.append(dfx_desc)

    #### Concatenating resulting dataframes into one final result
    print(display(pd.concat(res_dfs, axis=0)))
    print("-"*75)
    print("-"*75)
    print("\n\n".format())


    ## Pipeline to obtain top repeated variables per column
    print("****************************")
    print("** Top repeated variables **")
    print("****************************")

    #### Initial variables
    tops = 5 #### Number of tops that will be selected
    i = 0 #### Counter to start joining dataframes

    #### Loop through all variables that will be processed
    for col_sel in dfx:

        #### Creating dataframe with top entries and count
        dfxx = dfx[col_sel].value_counts().iloc[:tops].to_frame()
        dfxx.reset_index(drop=False, inplace=True)
        dfxx["part"] = round(dfxx[col_sel]/dfx[col_sel].count()*100, 2)
        dfxx.columns = pd.MultiIndex.from_tuples([(col_sel, tag) for tag in ["value", "count", "part_notnull"]])

        #### Joining all the variables in one final dataframe
        if i == 0:
            df_tops = dfxx
            i += 1
        else:
            df_tops = df_tops.join(dfxx)

    ## Fill empty spaces of resulting dataframe and renaming index entries
    df_tops.fillna("-", inplace=True)
    df_tops.index = ["top_" + str(i) for i in range(1, df_tops.shape[0] + 1)]
    print(display(df_tops))
    print("-"*75)
    print("-"*75)
    print()
    return



## Create the data profiling of categorical variables.
def data_profiling_categ(data, cat_vars):
    """
    Create the data profiling of categorical variables.
        args:
            data (Data Frame): data set into Dataframe.
            cat_vars (list): list with categorical variables names.
        returns:
           display(): display the Dataframes with info.
    """

    print("*************************************")
    print("** Conteo y proporción de entradas **")
    print("*************************************")

    df_catVar_list = []

    for val in cat_vars:

        print("Variable categorica -> {}".format(val))

        catego  = data[val].value_counts()
        totalOb = len(data[val])
        can_Cat = len(catego)
        moda    = data[val].mode().values[0]
        valFal  = data[val].isnull().sum()
        top1    = [catego[0:1].index[0],catego[0:1].values[0]] if can_Cat >= 1 else 0
        top2    = [catego[1:2].index[0],catego[1:2].values[0]] if can_Cat >= 2 else 0
        top3    = [catego[2:3].index[0],catego[2:3].values[0]] if can_Cat >= 3 else 0

        elemVarCat = {
            "Info":val,
            "Num_Registros":[totalOb],
            "Num_de_categorias":[can_Cat],
            "Moda":[moda],
            "Valores_faltantes":[valFal],
            "Top1":[top1],
            "Top2":[top2],
            "Top3":[top3]
            }

        #primerdataframe
        df_catVar_list.append(pd.DataFrame(elemVarCat).set_index("Info").T)
        # print(display(pd.DataFrame(elemVarCat).set_index("Info").T))

        # print("Valores de las categorias y sus proporciones")
        #segundodataframe donde se muestra los valores de las categorias su cantidad y su proporción.
        pro = proporcion(catego, totalOb)
        dfProp = pd.DataFrame(pro, columns=['Categoría', 'Observaciones', 'Proporción']).set_index("Categoría")
        #mostrar primer data frame
        print(display(dfProp))
        print("\n\n".format())


    print("***************************************")
    print("** Impresión de resumen de variables **")
    print("***************************************")

    ## Print summary dataframe with results from categoric variables
    print(display(pd.concat(df_catVar_list, axis=1)))


    return



## Create the data profiling of categorical variables.
def data_profiling_date(data, date_vars):
    """
    Create the data profiling of categorical variables.
        args:
            data (Data Frame): project data set.
            date_vars (list): list with date variables names.
        returns:
            -
    """


    ## Craeting new dataframe with date columns and adjusting contents for profiling

    #### Working dataframe
    dfx = data.loc[:, date_vars]

    #### Filtering only hour in time data
    time_cols = ["hora_creacion"]
    for tc in time_cols:
        dfx[tc] = dfx[tc].apply(lambda x: x[:2] if x[2]==":" else "xx")

    #### Extracting date data from date column
    dfx["fecha_creacion_sep"] = dfx["fecha_creacion"].str.split(pat="/")

    date_desc = ["dia", "mes", "año"]
    for dd in date_desc:
        dfx[dd + "_creacion"] = dfx["fecha_creacion_sep"].apply(lambda x: x[date_desc.index(dd)])

    ###### Correcting years with length two
    dfx["año_creacion"] = dfx["año_creacion"].apply(lambda x: "20" + x if len(x)==2 else x)

    ###### Deleting acillary column
    dfx.drop("fecha_creacion_sep", axis=1, inplace=True)


    #### Deleting columns related with


    return dfx



## Process coordinates to clean dataframe.
def geo_transformation(data, variable_latlong, variable_drop):
    """
    Get the Latitude and Longitude columns from a specific column, then transform both columns to floats and finally remove the original column.
        args:
            data (geodataframe): Original data with Geo Point column
            variable (string): Name of column with longitude and latitude data
            variable_drop (string): name of columns that will be dropped.
        returns:
            Geodataframe with columns longitude and latitude
    """

    data[['latitud','longitud']] = data.loc[:, variable_latlong].str.split(",", expand = True)
    data[['latitud','longitud']] = data[['latitud','longitud']].astype('float')
    data = data.drop(columns = [variable_latlong, variable_drop])

    return data



## Function to print the number of decimals that each of the geo columns have
def geo_vars_precision(data, geo_vars):
    """
    Function to print the number of decimals that each of the geo columns have
        args:
            data (dataframe): dataset that contains the geospatial columns (e.g. "latitud" & "longitud")
            geo_vars (list - strings): list with the names of the geospatial columns (e.g. ["latitud", "longitud"])
        returns:
            -
    """

    ## List where the resulting dataframes will be stored for join
    list_dfs_res = []

    ## Looop to create precision dataframes and append to list
    for col in geo_vars:
        df_geo_decs = data[col].astype("str").str.split(pat=".", expand=True).loc[:, 1].str.len().value_counts().to_frame()
        df_geo_decs.columns = ["No. of entries - " + col]
        list_dfs_res.append(df_geo_decs)

    ## Joining precision dataframes and printing result
    dfres = list_dfs_res[0].join(list_dfs_res[1])
    dfres.index.name = "No. of decimals"
    print(display(dfres))

    return



## Transform columns' names to standard format
def clean_col_names(dataframe):
    """
    Transform columns' names to standard format (lowercase, no spaces, no points)
        args:
            dataframe (dataframe): df whose columns will be formatted.
        returns:
            dataframe (dataframe): df with columns cleaned.
    """

    ## Definition of cleaning funcitons that will be applied to the columns' names
    fun1 = lambda x: x.lower() ## convert to lowercase
    fun2 = lambda x: re.sub("( |¡|!|¿|\?|\.|,|;|:)", "_", x) ## eliminate spaces and punctuation signs for underscore
    fun3 = lambda x: unicodedata.normalize("NFD", x).encode("ascii", "ignore").decode("utf-8") ## substitute accents for normal letters
    funcs = [fun1, fun2, fun3]

    ## Applying the defined functions to the columns' names
    for fun in funcs:
        dataframe.columns = [fun(col) for col in dataframe.columns]

    return dataframe



## Converting observatios for selected columns into lowercase.
def convert_lower(data, vars_lower):
    """
     Converting observatios for selected columns into lowercase.
        args:
            data (dataframe): data that is being analyzed.
            vars_lower (list): list of the columns' names in the dataframe that will be changed to lowercase.
        returns:
            data(dataframe): dataframe that is being analyzed with the observations (of the selected columns) in lowercase.
    """
    for x in vars_lower:
        data[x]=data[x].str.lower()
    return data



## Function to correct selected entries in dataframe
def correct_selected_entries(data, correction_dict):
    """
    Function to correct selected entries in dataframe
        args:
            data (dataframe): dataset that contains entries that need to be corrected
        returns:
            correction_dict (dictionary): reference to correct bad entries
                dictionary format:
                    > keys --> name of the column that has bad entries
                    > values --> dictionary that contains bad word and required word (e.g. {catt: cat})
    """

    ## Loop to apply corrections
    for corr_col in correction_dict:
        for bad_ent in correction_dict[corr_col]:
            data[corr_col] = data[corr_col].replace(bad_ent, correction_dict[corr_col][bad_ent])

    return data



## Calculate the data proportion of categorical variables.
def proporcion(listaVar,n):
    """
    Calculate the data proportion of categorical variables.
        args:
            listaVar (Serie): Serie with unique values of categorical variables
                               to get use value_counts() into a Serie
            n (int): value of total observation of data set.
        returns:
           newList(list): List with name, count and proportion of each category.
    """
    newList = []
    for lis in listaVar.iteritems():
        newList.append([lis[0],lis[1],"{}%".format(round(100*(lis[1]/n),1))])
    return newList





"------------------------------------------------------------------------------"
#################
## END OF FILE ##
#################
"------------------------------------------------------------------------------"
