import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators import KubernetesOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.secret import Secret


def print_world():
    print('world')


default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2017, 6, 1),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}


secret_file = Secret('volume', '/etc/sql_conn',
                     'airflow-secrets', 'sql_alchemy_conn')
secret_env = Secret('env', 'SQL_CONN', 'airflow-secrets', 'sql_alchemy_conn')
volume_mount = VolumeMount('test-volume',
                           mount_path='/root/mount_file',
                           sub_path=None,
                           read_only=True)

volume_config = {
    'persistentVolumeClaim':
    {
        'claimName': 'test-volume'
    }
}
volume = Volume(name='test-volume', configs=volume_config)

affinity = {
    'nodeAffinity': {
        'preferredDuringSchedulingIgnoredDuringExecution': [
            {
                "weight": 1,
                "preference": {
                    "matchExpressions": {
                        "key": "disktype",
                        "operator": "In",
                        "values": ["ssd"]
                    }
                }
            }
        ]
    },
    "podAffinity": {
        "requiredDuringSchedulingIgnoredDuringExecution": [
            {
                "labelSelector": {
                    "matchExpressions": [
                        {
                            "key": "security",
                            "operator": "In",
                            "values": ["S1"]
                        }
                    ]
                },
                "topologyKey": "failure-domain.beta.kubernetes.io/zone"
            }
        ]
    },
    "podAntiAffinity": {
        "requiredDuringSchedulingIgnoredDuringExecution": [
            {
                "labelSelector": {
                    "matchExpressions": [
                        {
                            "key": "security",
                            "operator": "In",
                            "values": ["S2"]
                        }
                    ]
                },
                "topologyKey": "kubernetes.io/hostname"
            }
        ]
    }
}

tolerations = [
    {
        'key': "key",
        'operator': 'Equal',
        'value': 'value'
    }
]

with DAG('pretzel_test',
         default_args=default_args,
         schedule_interval='0 * * * *',
         ) as dag:

    print_hello = BashOperator(task_id='print_hello',
                               bash_command='echo "hello"')
    sleep = BashOperator(task_id='sleep',
                         bash_command='sleep 5')
    print_world = PythonOperator(task_id='print_world',
                                 python_callable=print_world)

    k = KubernetesPodOperator(namespace='default',
                              image="ubuntu:16.04",
                              cmds=["bash", "-cx"],
                              arguments=["echo", "10"],
                              labels={"foo": "bar"},
                              # secrets=[secret_file, secret_env],
                              volume=[volume],
                              volume_mounts=[volume_mount],
                              name="test",
                              task_id="kubernetes_task",
                              affinity=affinity,
                              is_delete_operator_pod=True,
                              hostnetwork=False,
                              tolerations=tolerations
                              )


print_hello >> sleep >> print_world
