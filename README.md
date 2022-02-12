Big-Data-Systems-Assignment-1
==============================

Processing Storm data from SEVIR dataset in Google Big Query and visualizing insights from it using Google Data Studio. Used csv files as the data source for this project.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

--------

Report source link: https://docs.google.com/document/d/15agB-fbBIva-FM_bUXEggcz9bDuFSzUiMBhUJdudBxQ/edit?usp=sharing

# Part I: 
Analysis of CATALOG.csv (the metadata file for SEVIR dataset) and Storm Events datasets for the years 2018 and 2019. 
## Steps for analyzing SEVIR metadata in Big Query and Data Studio
1. Download SEVIR Catalog dataset and Storm Events dataset for 2018 and 2019.
2. In the Google Cloud Console, create a new project in BigQuery. 
3. Enable the BigQuery API. 
4. Select the project name on the left side of the UI, then create a new dataset.
5. Create a new table within the newly created dataset
   - The following widget allows uploading files from your local system, Google Drive, and Google Cloud Storage.
   - Since we already have the CSV files for our project we use the upload functionality. It allows uploading files up to 100MB of size.
6. Name the table and choose a schema for the table
   - BigQuery offers a functionality to auto-detect the schema. However, it can also be done manually.
7. A load job is then created
   - Once the loading is complete we can view the table details where you can check the schema, details, and preview the dataset. 
8. In the query editor, add a query that you wish to run on the table. 
## Creating a data view in BigQuery for Analysis
1. Loading data directly to Google Data Studio for analysis has certain limitations. Data blending in Data Studio uses left outer join. 
2. As per our use case, we need to combine Storm-Event details files for the year 2018 and 2019. Since Google Data Studio does not allow union operation we perform this union in BigQuery. Run the following query in the query editor.
 
```
SELECT EPISODE_ID, EVENT_ID, STATE, YEAR, MONTH_NAME, EVENT_TYPE, CZ_NAME, CZ_TIMEZONE, INJURIES_DIRECT, DEATHS_DIRECT, DAMAGE_CROPS, DAMAGE_PROPERTY, MAGNITUDE, BEGIN_LAT, BEGIN_LON, STATE_FIPS 
FROM `assignment-1-340501.storm2018.storm_details2018`
UNION ALL 
SELECT EPISODE_ID, EVENT_ID, STATE, YEAR, MONTH_NAME, EVENT_TYPE, CZ_NAME, CZ_TIMEZONE, INJURIES_DIRECT, DEATHS_DIRECT, DAMAGE_CROPS, DAMAGE_PROPERTY, MAGNITUDE, BEGIN_LAT, BEGIN_LON, STATE_FIPS 
FROM `assignment-1-340501.storm2019.storm_details2019`
```

 
3. Now that we have a combined view of the Storm-Event dataset for2018 and 2019, we perform a left join on the new table with SEVIR's metadata file. Run the following query in the query editor on BigQuery.

```
SELECT E.EPISODE_ID, E.EVENT_ID, E.STATE, E.YEAR, E.MONTH_NAME, E.EVENT_TYPE, E.CZ_NAME, E.CZ_TIMEZONE, E.INJURIES_DIRECT, E.DEATHS_DIRECT, E.DAMAGE_CROPS, E.DAMAGE_PROPERTY, E.MAGNITUDE, E.BEGIN_LAT, E.BEGIN_LON, E.STATE_FIPS, S.id, S.file_name, S.file_index, S.img_type 
FROM `assignment-1-340501.storm_union.storm_details_all` as E LEFT JOIN `assignment-1-340501.catalog.sevir-catalog` as S ON E.EVENT_ID = S.event_id
```

4. Save the above view into a new table, this will be added as a source to Google Data Studio for analysis.





## Adding a data source and creating report using Google Data Studio and BigQuery connector
1. Open Google Data Studio. Click on the Blank Report template to create a new report.
2. Click on Add data on the toolbar on top of the window. Select BigQuery from Add data to report popup.
3. From My Projects, select the name of your project under which you are creating the report. Then select the name of the source dataset and the table name. Click on Add to 4. Report. The data source is now ready to be used.
4. Add charts on the report. Using the data tab on the window set dimensions, metrics, filter and other functionalities, for the information you would like to represent on the report.
5. We can also use customer queries for reports. In the data tab select BigQuery as the data source. A window will pop-up where you can select Custom Query as the source. A query editor will open up, run the query and save the view for the chart to utilize. 
6. The style tab allows formatting of the charts and their properties.

## Dashboard
Dashboard Link : https://datastudio.google.com/s/iR5pu5rj5qo

SEVIR and Storm-Event datasets analysis answers the following queries for the years 2018 and 2019.
1. Number of unique storm events (event_id) by state using a Geo-chart.
2. Breakdown of direct injuries (in percentage) by storm event type.
3. Total number of direct deaths by storm event type.
4. Count of images by image type and storm event type.
5. Highest magnitude of Thunderstorm-wind and Hail-storm by state.
   - For this we used a Custom Query

```
SELECT STATE, MAGNITUDE, EVENT_TYPE
FROM `assignment-1-340501.sevir_storm_leftjoin.storm_sevir_left`
WHERE EVENT_TYPE IN ('Hail', 'Thunderstorm Wind')
ORDER BY MAGNITUDE DESC
```

6. Total number of distinct storm events by state and season.
7. Total property damage (in Dollars) by state
8. Total crop damage (in Dollars) by state



## Part II: 
Storm EVent ImagRy (SEVIR) dataset for EventID: 835047 contains images of storm events captured by satellite and radar. SEVIR is a collection of thousands of "storm events", which are 4-hour sequences of weather recorded by five separate sensors. The dataset provides five sensing modalities. 
The data collected by the National Weather Service (NWS) can augment many of the events in SEVIR. This database includes the type of severe weather (high winds, tornado, hail), storm impacts (damage due to crop and properties, injuries, and deaths), and a summary of the event.

The two main components are Catalog and data files. Catalog primarily contains the metadata of the event and data files contain events for a certain sensor in an hierarchical format, where the data is stored as an integer type. Depending on the sensor type, these integers can be decoded into floating type values, which represent the actual values captured by the sensor. Decoding is performed either using linear scaling or an exponential transformation.
## References 
https://github.com/googlecodelabs/tools

https://www.ncdc.noaa.gov/stormevents/ftp.jsp

https://nbviewer.jupyter.org/github/MIT-AI-Accelerator/eie-sevir/blob/master/examples/SEVIR_Tutorial.ipynb

https://cloud.google.com/bigquery/docs/visualize-data-studio

https://github.com/MIT-AI-Accelerator/sevir_challenges

https://www.youtube.com/watch?v=Abzj-Vyhi74&ab_channel=GoogleCloudTech

## Submitted by:

![image](https://user-images.githubusercontent.com/37017771/153502035-dde7b1ec-5020-4505-954a-2e67528366e7.png)
