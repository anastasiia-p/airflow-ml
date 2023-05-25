from airflow.decorators import dag
from airflow.operators.python_operator import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount

from utils import aggregate_predictions

# Define path to data
raw_data_path = "/opt/airflow/data/raw/data__{{ ds }}.csv"
pred_data_path = "/opt/airflow/data/predict/labels__{{ ds }}.json"
result_data_path = "/opt/airflow/data/predict/result__{{ ds }}.json"

# Define keyword arguments to use for all DockerOperator tasks
dockerops_kwargs = {
    "mount_tmp_dir": False,
    "mounts": [
        Mount(
            source="<path_to_your_airflow-ml_repo>/data", # Change to your path
            target="/opt/airflow/data/",
            type="bind",
        )
    ],
    "retries": 1,
    "api_version": "1.30",
    "docker_url": "tcp://docker-socket-proxy:2375", 
    "network_mode": "bridge",
}


# Create DAG
@dag("financial_news", start_date=days_ago(0), schedule="@daily", catchup=False)
def taskflow():
    # Task 1
    news_load = DockerOperator(
        task_id="news_load",
        container_name="task__news_load",
        image="data-loader:latest",
        command=f"python data_load.py --data_path {raw_data_path}",
        **dockerops_kwargs,
    )

    # Task 2
    news_label = DockerOperator(
        task_id="news_label",
        container_name="task__news_label",
        image="model-prediction:latest",
        command=f"python model_predict.py --data_path {raw_data_path} --pred_path {pred_data_path}",
        **dockerops_kwargs,
    )

    # Task 3
    news_by_topic = PythonOperator(
        task_id="news_by_topic",
        python_callable=aggregate_predictions,
        op_kwargs={
            "pred_data_path": pred_data_path,
            "result_data_path": result_data_path,
        },
    )

    news_load >> news_label >> news_by_topic


taskflow()
