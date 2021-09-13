from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import datetime
from airflow.utils.dates import timedelta
import os
cwd = os.getcwd()

# We're hardcoding this value here for the purpose of the demo, but in a production environment this
# would probably come from a config file and/or environment variables!
DBT_PROJECT_DIR = '/home/airflow/gcs/data/dbt'

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "jheck",
    "depends_on_past": False,
    "start_date": datetime(2021, 7, 22),
}

dag = DAG(
    "dbt_basic_dag",
    default_args=default_args,
    description="A sample Airflow DAG to invoke dbt runs using a BashOperator",
    schedule_interval=None,
    catchup=False,
)

def curr_dir():
    dbt = os.path.join(cwd, 'gcs/dbt')
    dir_list = os.listdir(dbt)
    print(dir_list)


with dag:
    # This task loads the CSV files from dbt/data into the local postgres database for the purpose of this demo.
    # In practice, we'd usually expect the data to have already been loaded to the database.

    # current_dir = PythonOperator(
    #     task_id='print_current_directory',
    #     python_callable=curr_dir,
    # )

    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command=f"dbt seed --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}"
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"dbt run --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}"
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"dbt test --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}"
    )

dbt_seed >> dbt_run >> dbt_test