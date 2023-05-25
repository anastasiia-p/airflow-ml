# Airflow Example Pipeline for Machine Learning (Local Development)

This repository provides an example Apache Airflow pipeline for local development of machine learning projects. The pipeline demonstrates how to fetch news articles from an open data source and apply a zero-shot classification NLP model to classify them into predefined categories.

## Overview
In this example, we leverage Apache Airflow to automate the following steps:

1. Data Loader: The pipeline retrieves news articles from an open data source and prepares them for further processing.

2. Text Classification: We use a pre-trained NLP model for zero-shot classification to assign relevant categories to the news articles. This model can classify text into various categories without prior training on specific datasets.

3. Results Aggregation: This task focuses on aggregating the classified news articles.

The first and second tasks are executed in separate Docker-containers. By deploying the first two tasks in separate containers, we ensure efficient resource utilization and maintain modularity in the pipeline's execution environment. 

## Usage
To use this pipeline for local development, follow the steps below:

1. Ensure that your Docker Engine has sufficient memory allocated, as running the pipeline may require more memory in certain cases.

2. Сhange path to your local repo in `dags/news_classifier.py`. Replace "<path_to_your_airflow-ml_repo>/data" with your path.

3. Before the first Airflow run, prepare the environment by executing the following steps:

    - If you are working on Linux, specify the AIRFLOW_UID by running the command:

    ```bash
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```
    - Perform the database migration and create the initial user account by running the command:

    ```bash
    docker compose up airflow-init
    ```
    The created user account will have the login `airflow` and the password `airflow`.

4. Start Airflow and build custom images to run tasks in Docker-containers:

    ```bash
    docker compose up --build
    ```

5. Access the Airflow web interface in your browser at http://localhost:8080.

6. Trigger the DAG `financial_news` to initiate the pipeline execution.

7. When you are finished working and want to clean up your environment, run:

    ```bash
    docker compose down --volumes --rmi all
    ```
