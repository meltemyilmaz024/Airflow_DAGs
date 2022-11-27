import os
from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def download_from_s3(key:str, bucket_name:str, local_path:str) -> str:
    hook = S3Hook('s3_conn')
    file_name = hook.download_file(key=key, bucket_name=bucket_name, local_path=local_path)
    return file_name


def rename_file(ti, new_name: str) -> None:
    download_file_name = ti.xcom_pull(task_ids=['download_from_s3'])
    #/Home/airflow/downloads/<file_new_name>
    downloaded_file_path='/'.join(download_file_name[0].split('/')[:-1])
    os.rename(src=download_file_name[0], dst=f"{downloaded_file_path}/{new_name}")


with DAG(
    dag_id='s3_download',
    schedule_interval='@daily',
    start_date=datetime(2022, 11, 24),
    catchup=False
) as dag:

    task_download_from_s3 = PythonOperator(
        task_id='download_from',
        python_callable=download_from_s3,
        op_kwargs={
            'key':'posts.json',
            'bucket_name':'de-airflow-bucket',
            'local_path':'/home/airflow/downloads/'
        }
    )

    task_rename_file = PythonOperator(
        task_id ='rename_file',
        python_callable=rename_file,
        op_kwargs={
            'new_name': 's3_downloaded_posts.json'
        }
    )