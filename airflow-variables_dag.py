from datetime import datetime
from airflow.models import DAG, Variable
from airflow.operators.python import PythonOperator
from airflow.operators.python import PythonOperator

def print_variables() -> str:
    # Airflow UI-variable-list :
    # (user_email = dev@dev.com)
    # (sample_json = {"user":"Kemal", "address":{"city":"TR","street_name":"anadolu"}})
    var_user_email = Variable.get("user_email")
    var_sample_json = Variable.get("sample_json", desearialize_json=True)
    var_env_test = Variable.get("test")
    var_env_test_json = Variable.get("test_json", deserialize_json=True)

    return f"""
        var_user_email = {var_user_email},
        var_sample_json = {var_sample_json},
        var_env_test = {var_env_test},
        var_env_test_json = {var_env_test_json}
    """


with DAG(
    dag_id = "variables_dag",
    schedule_interval="@daily",
    start_date=datetime(2022, 11, 24),
    catchup=False
) as dag:

    task_print_variables = PythonOperator(
        task_id="print_variables",
        python_callable=print_variables
    )
